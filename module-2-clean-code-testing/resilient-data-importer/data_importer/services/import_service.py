"""Import service for orchestrating the data import process."""

import logging
from dataclasses import dataclass
from pathlib import Path

from data_importer.exceptions import (
    DuplicateUserError,
    FileFormatError,
    ImporterError,
    ValidationError,
)
from data_importer.models.user import User
from data_importer.parsers.csv_parser import CSVParser
from data_importer.repositories.json_repository import JSONRepository
from data_importer.validators.user_validator import UserValidator

logger = logging.getLogger(__name__)


@dataclass
class ImportResult:
    """Result of an import operation.

    Attributes:
        total_rows: Total number of rows processed.
        imported: Number of users successfully imported.
        skipped: Number of users skipped (duplicates or invalid).
        errors: List of error messages encountered.
    """

    total_rows: int
    imported: int
    skipped: int
    errors: list[str]

    @property
    def success(self) -> bool:
        """Check if import was successful (at least one user imported)."""
        return self.imported > 0

    @property
    def has_errors(self) -> bool:
        """Check if any errors occurred during import."""
        return len(self.errors) > 0


class ImportService:
    """Service for orchestrating user data import from CSV to JSON.

    This service coordinates the parsing, validation, and storage
    of user data. It follows the Single Responsibility Principle
    by delegating specific tasks to specialized components.

    Attributes:
        parser: CSV parser instance.
        validator: User validator instance.
        repository: JSON repository instance.

    Example:
        >>> service = ImportService("input.csv", "output.json")
        >>> result = service.run_import()
        >>> print(f"Imported {result.imported} users")
    """

    def __init__(
        self,
        input_path: str | Path,
        output_path: str | Path,
        skip_duplicates: bool = True,
        skip_invalid: bool = True,
    ) -> None:
        """Initialize ImportService with file paths.

        Args:
            input_path: Path to input CSV file.
            output_path: Path to output JSON file.
            skip_duplicates: If True, skip duplicate users instead of failing.
            skip_invalid: If True, skip invalid users instead of failing.
        """
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.skip_duplicates = skip_duplicates
        self.skip_invalid = skip_invalid

        # Initialize components (Dependency Inversion - could be injected)
        self.validator = UserValidator()

    def run_import(self) -> ImportResult:
        """Execute the full import process.

        Parses the CSV file, validates each user, and saves valid
        users to the JSON repository.

        Returns:
            ImportResult with statistics about the import.

        Raises:
            ImporterError: If a fatal error occurs during import.

        Example:
            >>> result = service.run_import()
            >>> if result.success:
            ...     print(f"Successfully imported {result.imported} users")
        """
        logger.info(f"Starting import: {self.input_path} -> {self.output_path}")

        total_rows = 0
        imported = 0
        skipped = 0
        errors: list[str] = []

        try:
            # Parse CSV and collect valid users
            valid_users: list[User] = []

            with CSVParser(self.input_path) as parser:
                for user in parser.parse():
                    total_rows += 1
                    try:
                        # Validate user
                        self.validator.validate(user)
                        valid_users.append(user)
                    except ValidationError as e:
                        error_msg = f"Validation failed for user {user.user_id}: {e}"
                        logger.warning(error_msg)
                        errors.append(error_msg)
                        if self.skip_invalid:
                            skipped += 1
                        else:
                            raise
                    except FileFormatError as e:
                        error_msg = f"Format error: {e}"
                        logger.warning(error_msg)
                        errors.append(error_msg)
                        if self.skip_invalid:
                            skipped += 1
                        else:
                            raise

            # Save valid users to repository
            with JSONRepository(self.output_path) as repo:
                for user in valid_users:
                    try:
                        repo.save(user)
                        imported += 1
                        logger.info(f"Imported user: {user.user_id} ({user.name})")
                    except DuplicateUserError:
                        error_msg = f"Duplicate user: {user.user_id}"
                        logger.warning(error_msg)
                        errors.append(error_msg)
                        if self.skip_duplicates:
                            skipped += 1
                        else:
                            raise

            logger.info(
                f"Import complete: {imported} imported, {skipped} skipped, "
                f"{len(errors)} errors"
            )

        except ImporterError:
            # Re-raise importer errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error during import: {e}")
            raise ImporterError(f"Import failed: {e}") from e

        return ImportResult(
            total_rows=total_rows,
            imported=imported,
            skipped=skipped,
            errors=errors,
        )

    def validate_only(self) -> ImportResult:
        """Validate input file without importing.

        Useful for dry-run validation before actual import.

        Returns:
            ImportResult with validation statistics.
        """
        logger.info(f"Validating input file: {self.input_path}")

        total_rows = 0
        valid = 0
        invalid = 0
        errors: list[str] = []

        try:
            with CSVParser(self.input_path) as parser:
                for user in parser.parse():
                    total_rows += 1
                    try:
                        self.validator.validate(user)
                        valid += 1
                    except ValidationError as e:
                        error_msg = f"Invalid user {user.user_id}: {e}"
                        errors.append(error_msg)
                        invalid += 1

            logger.info(f"Validation complete: {valid} valid, {invalid} invalid")

        except ImporterError:
            raise
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            raise ImporterError(f"Validation failed: {e}") from e

        return ImportResult(
            total_rows=total_rows,
            imported=valid,  # Using imported for valid count
            skipped=invalid,
            errors=errors,
        )
