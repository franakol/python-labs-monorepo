"""Custom exception hierarchy for the Data Importer."""


class ImporterError(Exception):
    """Base exception for all importer errors.

    All custom exceptions in this module inherit from ImporterError,
    allowing callers to catch all importer-related errors with a single
    except clause.

    Args:
        message: Human-readable error description.
        details: Optional additional context about the error.

    Example:
        >>> raise ImporterError("Import failed", details={"file": "users.csv"})
    """

    def __init__(self, message: str, details: dict | None = None) -> None:
        """Initialize ImporterError with message and optional details."""
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class FileFormatError(ImporterError):
    """Raised when file format is invalid or malformed.

    This exception is raised when:
    - CSV file has missing or incorrect headers
    - CSV row has wrong number of columns
    - File encoding is not supported

    Args:
        message: Description of the format error.
        line_number: Optional line number where error occurred.
        details: Optional additional context.

    Example:
        >>> raise FileFormatError("Invalid header", line_number=1)
    """

    def __init__(
        self,
        message: str,
        line_number: int | None = None,
        details: dict | None = None,
    ) -> None:
        """Initialize FileFormatError with line number context."""
        details = details or {}
        if line_number is not None:
            details["line_number"] = line_number
        super().__init__(message, details)
        self.line_number = line_number


class ValidationError(ImporterError):
    """Raised when data validation fails.

    This exception is raised when:
    - Email format is invalid
    - User ID format is incorrect
    - Required fields are missing
    - Data types are incorrect

    Args:
        message: Description of the validation failure.
        field: The field that failed validation.
        value: The invalid value.
        details: Optional additional context.

    Example:
        >>> raise ValidationError("Invalid email", field="email", value="not-an-email")
    """

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: str | None = None,
        details: dict | None = None,
    ) -> None:
        """Initialize ValidationError with field context."""
        details = details or {}
        if field is not None:
            details["field"] = field
        if value is not None:
            details["value"] = value
        super().__init__(message, details)
        self.field = field
        self.value = value


class DuplicateUserError(ImporterError):
    """Raised when a duplicate user entry is detected.

    This exception is raised when attempting to import a user
    whose user_id already exists in the database.

    Args:
        message: Description of the duplicate.
        user_id: The duplicate user ID.
        details: Optional additional context.

    Example:
        >>> raise DuplicateUserError("User already exists", user_id="U001")
    """

    def __init__(
        self,
        message: str,
        user_id: str | None = None,
        details: dict | None = None,
    ) -> None:
        """Initialize DuplicateUserError with user_id context."""
        details = details or {}
        if user_id is not None:
            details["user_id"] = user_id
        super().__init__(message, details)
        self.user_id = user_id


class StorageError(ImporterError):
    """Raised when storage operations fail.

    This exception is raised when:
    - JSON file cannot be read or written
    - File permissions are insufficient
    - Disk is full or unavailable

    Args:
        message: Description of the storage error.
        path: The file path involved.
        details: Optional additional context.

    Example:
        >>> raise StorageError("Cannot write file", path="/data/users.json")
    """

    def __init__(
        self,
        message: str,
        path: str | None = None,
        details: dict | None = None,
    ) -> None:
        """Initialize StorageError with path context."""
        details = details or {}
        if path is not None:
            details["path"] = path
        super().__init__(message, details)
        self.path = path
