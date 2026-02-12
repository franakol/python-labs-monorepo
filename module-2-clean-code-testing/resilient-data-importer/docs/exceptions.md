# Exception Handling Guide

## Overview

This project demonstrates Python's exception handling best practices through a custom exception hierarchy. This guide explains how exceptions are designed, raised, and caught throughout the codebase.

## Exception Hierarchy

```
Exception (built-in)
    │
    └── ImporterError (base)
            │
            ├── FileFormatError
            │       • Malformed CSV files
            │       • Missing headers
            │       • Invalid row format
            │
            ├── ValidationError
            │       • Invalid email format
            │       • Invalid user ID format
            │       • Empty/missing fields
            │
            ├── DuplicateUserError
            │       • User ID already exists
            │       • Duplicate entries in CSV
            │
            └── StorageError
                    • File not writable
                    • Invalid JSON format
                    • Disk full
```

## Base Exception: ImporterError

All custom exceptions inherit from `ImporterError`, allowing callers to catch any importer-related error with a single `except` clause:

```python
class ImporterError(Exception):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
```

**Key Features:**
- `message`: Human-readable error description
- `details`: Optional dictionary with additional context
- Custom `__str__` method for detailed output

## Specialized Exceptions

### FileFormatError

Raised when CSV file format is invalid:

```python
class FileFormatError(ImporterError):
    def __init__(
        self,
        message: str,
        line_number: int | None = None,
        details: dict | None = None,
    ) -> None:
        # Automatically adds line_number to details
```

**When raised:**
- Missing required headers (user_id, name, email)
- Row has wrong number of columns
- File encoding issues

**Example:**
```python
raise FileFormatError(
    "Missing required CSV headers",
    line_number=1,
    details={"found": ["id", "name"], "missing": ["email"]}
)
```

### ValidationError

Raised when data fails validation:

```python
class ValidationError(ImporterError):
    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: str | None = None,
        details: dict | None = None,
    ) -> None:
        # Automatically adds field and value to details
```

**When raised:**
- Invalid email format
- Invalid user ID format
- Empty or whitespace-only name

**Example:**
```python
raise ValidationError(
    "Invalid email format",
    field="email",
    value="invalid-email"
)
```

### DuplicateUserError

Raised when a duplicate user is detected:

```python
class DuplicateUserError(ImporterError):
    def __init__(
        self,
        message: str,
        user_id: str | None = None,
        details: dict | None = None,
    ) -> None:
        # Automatically adds user_id to details
```

**When raised:**
- User ID already exists in database
- Duplicate in same CSV file

### StorageError

Raised when storage operations fail:

```python
class StorageError(ImporterError):
    def __init__(
        self,
        message: str,
        path: str | None = None,
        details: dict | None = None,
    ) -> None:
        # Automatically adds path to details
```

**When raised:**
- Cannot write to file (permissions)
- Invalid JSON in existing file
- Disk full or unavailable

## Usage Patterns

### Try/Except/Else/Finally

Complete error handling pattern:

```python
try:
    with CSVParser(path) as parser:
        users = list(parser.parse())
except FileNotFoundError as e:
    logger.error(f"File not found: {path}")
    raise ImporterError(f"CSV file not found: {path}") from e
except FileFormatError as e:
    logger.error(f"Format error at line {e.line_number}")
    raise
else:
    logger.info(f"Successfully parsed {len(users)} users")
finally:
    logger.debug("Parsing complete")
```

### Context Managers

Using context managers for safe resource handling:

```python
with CSVParser(path) as parser:  # Opens file
    for user in parser.parse():
        process(user)
# File automatically closed, even on error
```

### Exception Chaining

Preserving original exception context:

```python
try:
    self._file_handle = open(self.file_path, "r")
except FileNotFoundError as e:
    raise ImporterError(
        f"CSV file not found: {self.file_path}"
    ) from e  # Chains the original exception
```

### Catching Hierarchy

Catching at different levels:

```python
# Catch specific exception
try:
    validator.validate(user)
except ValidationError as e:
    print(f"Invalid {e.field}: {e.value}")

# Catch any import error
try:
    service.run_import()
except ImporterError as e:
    print(f"Import failed: {e}")

# Let unexpected errors propagate
try:
    service.run_import()
except ImporterError:
    handle_import_error()
# Other exceptions propagate up
```

## Best Practices Demonstrated

1. **Custom exceptions** for domain-specific errors
2. **Exception hierarchy** for flexible catching
3. **Context information** via `details` dict
4. **Exception chaining** with `from` keyword
5. **Context managers** for resource cleanup
6. **Logging** at appropriate levels
7. **try/except/else/finally** for complete control

## Testing Exceptions

Using pytest to test exception behavior:

```python
def test_missing_file_raises_error(self):
    parser = CSVParser("nonexistent.csv")

    with pytest.raises(ImporterError) as exc_info:
        with parser:
            pass

    assert "not found" in str(exc_info.value).lower()
```
