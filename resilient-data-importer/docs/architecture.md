# Architecture Documentation

## Overview

The Resilient Data Importer CLI follows a **layered architecture** that separates concerns and adheres to SOLID principles. This document describes the design decisions and component interactions.

## Architecture Diagram

```
                    ┌──────────────────────────────────────────┐
                    │                   CLI                     │
                    │        (data_importer/cli.py)             │
                    │                                           │
                    │  • Argument parsing (argparse)            │
                    │  • Logging configuration                  │
                    │  • User-friendly output                   │
                    └──────────────────┬───────────────────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────────┐
                    │            ImportService                  │
                    │   (data_importer/services/import_service.py)     │
                    │                                           │
                    │  • Orchestrates the import workflow       │
                    │  • Coordinates parser, validator, repo    │
                    │  • Handles error aggregation              │
                    └───────┬──────────────┬──────────────┬────┘
                            │              │              │
              ┌─────────────▼──┐    ┌──────▼──────┐    ┌──▼─────────────┐
              │   CSVParser    │    │ UserValidator│    │ JSONRepository │
              │  (parsers/)    │    │ (validators/)│    │ (repositories/)│
              │                │    │              │    │                │
              │ • Context mgr  │    │ • Email regex│    │ • Context mgr  │
              │ • Header valid │    │ • ID format  │    │ • CRUD ops     │
              │ • Row parsing  │    │ • Name check │    │ • Batch save   │
              └────────────────┘    └──────────────┘    └────────────────┘
                            │              │              │
                            └──────────────┼──────────────┘
                                           │
                                           ▼
                              ┌────────────────────────┐
                              │         User           │
                              │   (models/user.py)     │
                              │                        │
                              │  • Dataclass           │
                              │  • Serialization       │
                              └────────────────────────┘
```

## SOLID Principles

### Single Responsibility Principle (SRP)

Each class has one reason to change:

| Class | Responsibility |
|-------|----------------|
| `CSVParser` | Read and parse CSV files only |
| `UserValidator` | Validate user data only |
| `JSONRepository` | Persist data to JSON only |
| `ImportService` | Coordinate the workflow only |
| `CLI` | Handle user interaction only |

### Open/Closed Principle (OCP)

Components are open for extension but closed for modification:

- Add new validators by extending `UserValidator`
- Support new file formats by creating new parsers
- Add new storage backends by implementing repository interface

### Liskov Substitution Principle (LSP)

Custom exceptions extend base `ImporterError`:

```python
ImporterError           # Can be caught for any importer error
├── FileFormatError     # Substitutable for ImporterError
├── ValidationError     # Substitutable for ImporterError
├── DuplicateUserError  # Substitutable for ImporterError
└── StorageError        # Substitutable for ImporterError
```

### Interface Segregation Principle (ISP)

Components depend only on methods they use:

- `ImportService` uses `parse()` from parser
- `ImportService` uses `validate()` from validator
- `ImportService` uses `save()` from repository

### Dependency Inversion Principle (DIP)

High-level modules don't depend on low-level modules:

- `ImportService` creates its own dependencies (could be injected)
- Components communicate through data objects (`User`)

## Data Flow

### Import Workflow

```
1. CLI parses arguments
         │
         ▼
2. ImportService instantiated
         │
         ▼
3. CSVParser opens file (context manager)
         │
         ▼
4. For each row:
   a. Parse row into User object
   b. Validate User with UserValidator
   c. Save User to JSONRepository
         │
         ▼
5. CSVParser closes file (context manager)
         │
         ▼
6. JSONRepository persists data (context manager)
         │
         ▼
7. Return ImportResult with statistics
```

### Error Handling Flow

```
Try block
    │
    ├── FileNotFoundError → ImporterError("File not found")
    │
    ├── CSV format issues → FileFormatError(line_number)
    │
    ├── Data validation fails → ValidationError(field, value)
    │
    ├── Duplicate user → DuplicateUserError(user_id)
    │
    └── Storage fails → StorageError(path)

Catch block
    │
    ├── Skip and log (skip_invalid=True)
    │
    └── Re-raise (strict mode)
```

## Context Managers

Both `CSVParser` and `JSONRepository` implement the context manager protocol:

```python
# CSVParser
with CSVParser(path) as parser:
    for user in parser.parse():
        process(user)
# File automatically closed

# JSONRepository
with JSONRepository(path) as repo:
    repo.save(user)
# Data automatically persisted
```

## Logging

Structured logging with Python's `logging` module:

```python
# Format
"%(asctime)s - %(levelname)s - %(message)s"

# Levels
DEBUG: Detailed parsing info
INFO: Import progress
WARNING: Skipped rows, validation failures
ERROR: Import failures
```

## Future Improvements

1. **Dependency Injection**: Inject parser, validator, repo into service
2. **Async Support**: Use `aiofiles` for async I/O
3. **Database Support**: Add SQLite/PostgreSQL repositories
4. **Plugin System**: Dynamically load validators and parsers
5. **Configuration File**: YAML/TOML config for import settings
