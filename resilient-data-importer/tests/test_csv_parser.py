"""Tests for the CSV parser module."""

import tempfile
from pathlib import Path

import pytest

from data_importer.exceptions import FileFormatError, ImporterError
from data_importer.models.user import User
from data_importer.parsers.csv_parser import CSVParser


class TestCSVParser:
    """Tests for CSVParser class."""

    def test_parse_valid_csv(self, temp_csv_file: Path) -> None:
        """Test parsing a valid CSV file."""
        with CSVParser(temp_csv_file) as parser:
            users = list(parser.parse())

        assert len(users) == 3
        assert users[0].user_id == "U001"
        assert users[0].name == "Alice Johnson"
        assert users[0].email == "alice@example.com"

    def test_context_manager_opens_and_closes_file(
        self, temp_csv_file: Path
    ) -> None:
        """Test that context manager properly opens and closes file."""
        parser = CSVParser(temp_csv_file)

        # File should not be open before entering context
        assert parser._file_handle is None

        with parser:
            # File should be open inside context
            assert parser._file_handle is not None

        # File should be closed after exiting context
        assert parser._file_handle is None

    def test_file_not_found_raises_error(self) -> None:
        """Test that missing file raises ImporterError."""
        parser = CSVParser("nonexistent_file.csv")

        with pytest.raises(ImporterError) as exc_info:
            with parser:
                pass

        assert "not found" in str(exc_info.value).lower()

    def test_parse_without_context_raises_error(
        self, temp_csv_file: Path
    ) -> None:
        """Test that parsing without context manager raises error."""
        parser = CSVParser(temp_csv_file)

        with pytest.raises(ImporterError) as exc_info:
            list(parser.parse())

        assert "not open" in str(exc_info.value).lower()

    def test_missing_headers_raises_error(self, csv_missing_headers: str) -> None:
        """Test that missing required headers raises FileFormatError."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(csv_missing_headers)
            temp_path = Path(f.name)

        try:
            with CSVParser(temp_path) as parser:
                with pytest.raises(FileFormatError) as exc_info:
                    list(parser.parse())

            assert "header" in str(exc_info.value).lower()
        finally:
            temp_path.unlink()

    def test_malformed_row_raises_error(self, temp_malformed_csv: Path) -> None:
        """Test that malformed rows raise FileFormatError."""
        with CSVParser(temp_malformed_csv) as parser:
            with pytest.raises(FileFormatError) as exc_info:
                list(parser.parse())

        assert exc_info.value.line_number is not None

    @pytest.mark.parametrize(
        "csv_content,expected_count",
        [
            ("user_id,name,email\nU001,Alice,alice@test.com", 1),
            ("user_id,name,email\nU001,Alice,a@t.co\nU002,Bob,b@t.co", 2),
            ("user_id,name,email", 0),  # No data rows
        ],
    )
    def test_parse_various_row_counts(
        self, csv_content: str, expected_count: int
    ) -> None:
        """Test parsing CSV files with various row counts."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(csv_content)
            temp_path = Path(f.name)

        try:
            with CSVParser(temp_path) as parser:
                users = list(parser.parse())

            assert len(users) == expected_count
        finally:
            temp_path.unlink()

    def test_parse_returns_user_objects(self, temp_csv_file: Path) -> None:
        """Test that parser returns User objects."""
        with CSVParser(temp_csv_file) as parser:
            users = list(parser.parse())

        for user in users:
            assert isinstance(user, User)
            assert hasattr(user, "user_id")
            assert hasattr(user, "name")
            assert hasattr(user, "email")
