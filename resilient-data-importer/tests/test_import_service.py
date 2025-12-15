"""Tests for the import service module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from data_importer.exceptions import ImporterError
from data_importer.models.user import User
from data_importer.services.import_service import ImportResult, ImportService


class TestImportResult:
    """Tests for ImportResult dataclass."""

    def test_success_with_imports(self) -> None:
        """Test success property when imports exist."""
        result = ImportResult(total_rows=3, imported=3, skipped=0, errors=[])
        assert result.success is True

    def test_success_with_no_imports(self) -> None:
        """Test success property when no imports."""
        result = ImportResult(total_rows=3, imported=0, skipped=3, errors=[])
        assert result.success is False

    def test_has_errors(self) -> None:
        """Test has_errors property."""
        result_no_errors = ImportResult(total_rows=3, imported=3, skipped=0, errors=[])
        result_with_errors = ImportResult(
            total_rows=3, imported=2, skipped=1, errors=["Error 1"]
        )

        assert result_no_errors.has_errors is False
        assert result_with_errors.has_errors is True


class TestImportService:
    """Tests for ImportService class."""

    @pytest.fixture
    def csv_file(self) -> Path:
        """Create a temporary CSV file."""
        content = """user_id,name,email
U001,Alice Johnson,alice@example.com
U002,Bob Smith,bob@example.com
U003,Carol White,carol@example.com"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            return Path(f.name)

    @pytest.fixture
    def json_file(self) -> Path:
        """Create a temporary JSON file path."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            return Path(f.name)

    def test_run_import_success(self, csv_file: Path, json_file: Path) -> None:
        """Test successful import operation."""
        service = ImportService(csv_file, json_file)
        result = service.run_import()

        assert result.success is True
        assert result.imported == 3
        assert result.skipped == 0
        assert len(result.errors) == 0

        # Verify JSON file contains users
        with open(json_file) as f:
            data = json.load(f)
        assert len(data) == 3

    def test_run_import_with_invalid_users(self, json_file: Path) -> None:
        """Test import with some invalid users."""
        content = """user_id,name,email
U001,Alice Johnson,alice@example.com
U002,Bob Smith,invalid-email
U003,Carol White,carol@example.com"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            csv_path = Path(f.name)

        try:
            service = ImportService(csv_path, json_file, skip_invalid=True)
            result = service.run_import()

            assert result.imported == 2
            assert result.skipped == 1
            assert len(result.errors) == 1
        finally:
            csv_path.unlink()

    def test_validate_only(self, csv_file: Path, json_file: Path) -> None:
        """Test validation-only mode."""
        service = ImportService(csv_file, json_file)
        result = service.validate_only()

        assert result.total_rows == 3
        assert result.imported == 3  # All valid

        # JSON file should NOT be created/modified
        with open(json_file) as f:
            content = f.read()
        assert content == ""  # File should be empty

    def test_import_missing_file(self, json_file: Path) -> None:
        """Test import fails gracefully for missing file."""
        service = ImportService("nonexistent.csv", json_file)

        with pytest.raises(ImporterError):
            service.run_import()

    def test_import_with_duplicates_skip(self, json_file: Path) -> None:
        """Test import skips duplicates when configured."""
        content = """user_id,name,email
U001,Alice Johnson,alice@example.com
U001,Alice Duplicate,alice2@example.com
U002,Bob Smith,bob@example.com"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            csv_path = Path(f.name)

        try:
            service = ImportService(csv_path, json_file, skip_duplicates=True)
            result = service.run_import()

            assert result.imported == 2
            assert result.skipped == 1
        finally:
            csv_path.unlink()

    def test_import_strict_mode(self, json_file: Path) -> None:
        """Test strict mode fails on first error."""
        content = """user_id,name,email
U001,Alice Johnson,alice@example.com
U002,Bob Smith,invalid-email"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            csv_path = Path(f.name)

        try:
            service = ImportService(
                csv_path, json_file, skip_invalid=False, skip_duplicates=False
            )

            with pytest.raises(ImporterError):
                service.run_import()
        finally:
            csv_path.unlink()

    def test_import_to_existing_database(self, csv_file: Path) -> None:
        """Test importing to existing database file."""
        # Create existing database
        existing_users = [
            {"user_id": "E001", "name": "Existing", "email": "existing@example.com"}
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(existing_users, f)
            json_path = Path(f.name)

        try:
            service = ImportService(csv_file, json_path)
            result = service.run_import()

            assert result.imported == 3

            # Verify all users are in database
            with open(json_path) as f:
                data = json.load(f)
            assert len(data) == 4  # 1 existing + 3 new
        finally:
            json_path.unlink()
