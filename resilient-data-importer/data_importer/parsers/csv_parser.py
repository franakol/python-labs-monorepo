"""CSV Parser module for reading user data from CSV files."""

import csv
import logging
from pathlib import Path
from typing import Iterator

from data_importer.exceptions import FileFormatError, ImporterError
from data_importer.models.user import User

logger = logging.getLogger(__name__)


class CSVParser:
    """Parser for reading user data from CSV files.

    This class provides methods for parsing CSV files containing user data.
    It implements the context manager protocol for safe file handling and
    provides robust error handling for malformed data.

    Attributes:
        file_path: Path to the CSV file to parse.
        expected_headers: List of required column headers.

    Example:
        >>> parser = CSVParser("users.csv")
        >>> with parser:
        ...     for user in parser.parse():
        ...         print(user.name)
    """

    EXPECTED_HEADERS = ["user_id", "name", "email"]

    def __init__(self, file_path: str | Path) -> None:
        """Initialize CSVParser with file path.

        Args:
            file_path: Path to the CSV file to parse.
        """
        self.file_path = Path(file_path)
        self._file_handle = None
        self._reader = None

    def __enter__(self) -> "CSVParser":
        """Enter context manager and open file.

        Returns:
            Self reference for use in with statement.

        Raises:
            ImporterError: If file cannot be opened.
        """
        try:
            logger.info(f"Opening CSV file: {self.file_path}")
            self._file_handle = open(self.file_path, "r", encoding="utf-8", newline="")
            return self
        except FileNotFoundError as e:
            logger.error(f"File not found: {self.file_path}")
            raise ImporterError(
                f"CSV file not found: {self.file_path}",
                details={"path": str(self.file_path)},
            ) from e
        except PermissionError as e:
            logger.error(f"Permission denied: {self.file_path}")
            raise ImporterError(
                f"Permission denied accessing file: {self.file_path}",
                details={"path": str(self.file_path)},
            ) from e
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            raise ImporterError(
                f"Failed to open CSV file: {e}",
                details={"path": str(self.file_path)},
            ) from e

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit context manager and close file.

        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.

        Returns:
            False to propagate any exceptions.
        """
        if self._file_handle:
            logger.info(f"Closing CSV file: {self.file_path}")
            self._file_handle.close()
            self._file_handle = None
        return False

    def _validate_headers(self, headers: list[str]) -> None:
        """Validate that CSV has required headers.

        Args:
            headers: List of header names from CSV file.

        Raises:
            FileFormatError: If required headers are missing.
        """
        # Normalize headers (strip whitespace, lowercase)
        normalized_headers = [h.strip().lower() for h in headers]

        missing_headers = []
        for expected in self.EXPECTED_HEADERS:
            if expected.lower() not in normalized_headers:
                missing_headers.append(expected)

        if missing_headers:
            logger.error(f"Missing required headers: {missing_headers}")
            raise FileFormatError(
                f"Missing required CSV headers: {missing_headers}",
                line_number=1,
                details={"found_headers": headers, "missing": missing_headers},
            )

    def parse(self) -> Iterator[User]:
        """Parse CSV file and yield User objects.

        Yields:
            User objects created from valid CSV rows.

        Raises:
            FileFormatError: If CSV format is invalid.
            ImporterError: If file is not open.

        Example:
            >>> with CSVParser("users.csv") as parser:
            ...     users = list(parser.parse())
        """
        if self._file_handle is None:
            raise ImporterError("File not open. Use context manager.")

        self._file_handle.seek(0)
        reader = csv.DictReader(self._file_handle)

        # Validate headers
        if reader.fieldnames is None:
            raise FileFormatError("Empty CSV file or missing headers", line_number=1)

        self._validate_headers(list(reader.fieldnames))

        # Parse rows
        for line_number, row in enumerate(reader, start=2):
            try:
                user = self._parse_row(row, line_number)
                if user:
                    yield user
            except FileFormatError:
                # Re-raise format errors with context
                raise
            except Exception as e:
                logger.warning(f"Skipping malformed row at line {line_number}: {e}")
                raise FileFormatError(
                    f"Malformed row at line {line_number}",
                    line_number=line_number,
                    details={"row": dict(row), "error": str(e)},
                ) from e

    def _parse_row(self, row: dict[str, str], line_number: int) -> User | None:
        """Parse a single CSV row into a User object.

        Args:
            row: Dictionary of column name to value.
            line_number: Current line number for error reporting.

        Returns:
            User object if row is valid, None if row should be skipped.

        Raises:
            FileFormatError: If row data is malformed.
        """
        # Extract and clean values
        user_id = row.get("user_id", "").strip()
        name = row.get("name", "").strip()
        email = row.get("email", "").strip()

        # Check for empty required fields
        if not user_id or not name or not email:
            missing_fields = []
            if not user_id:
                missing_fields.append("user_id")
            if not name:
                missing_fields.append("name")
            if not email:
                missing_fields.append("email")

            logger.warning(f"Line {line_number}: Missing fields {missing_fields}")
            raise FileFormatError(
                f"Missing required fields at line {line_number}",
                line_number=line_number,
                details={"missing_fields": missing_fields, "row": dict(row)},
            )

        logger.debug(f"Parsed user: {user_id} - {name}")
        return User(user_id=user_id, name=name, email=email)
