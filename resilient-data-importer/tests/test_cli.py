"""Tests for the CLI module."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from data_importer.cli import create_parser, main


class TestCLIParser:
    """Tests for CLI argument parser."""

    def test_parser_requires_input(self) -> None:
        """Test that --input is required."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--output", "out.json"])

    def test_parser_requires_output(self) -> None:
        """Test that --output is required."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--input", "in.csv"])

    def test_parser_accepts_required_args(self) -> None:
        """Test parser accepts required arguments."""
        parser = create_parser()
        args = parser.parse_args(["--input", "in.csv", "--output", "out.json"])

        assert args.input == Path("in.csv")
        assert args.output == Path("out.json")

    def test_parser_short_args(self) -> None:
        """Test parser accepts short argument forms."""
        parser = create_parser()
        args = parser.parse_args(["-i", "in.csv", "-o", "out.json"])

        assert args.input == Path("in.csv")
        assert args.output == Path("out.json")

    def test_parser_verbose_flag(self) -> None:
        """Test --verbose flag."""
        parser = create_parser()
        args = parser.parse_args(["-i", "in.csv", "-o", "out.json", "--verbose"])

        assert args.verbose is True

    def test_parser_dry_run_flag(self) -> None:
        """Test --dry-run flag."""
        parser = create_parser()
        args = parser.parse_args(["-i", "in.csv", "-o", "out.json", "--dry-run"])

        assert args.dry_run is True

    def test_parser_strict_flag(self) -> None:
        """Test --strict flag."""
        parser = create_parser()
        args = parser.parse_args(["-i", "in.csv", "-o", "out.json", "--strict"])

        assert args.strict is True


class TestCLIMain:
    """Tests for CLI main function."""

    @pytest.fixture
    def csv_file(self) -> Path:
        """Create a temporary CSV file."""
        content = """user_id,name,email
U001,Alice Johnson,alice@example.com
U002,Bob Smith,bob@example.com"""

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

    def test_main_success(self, csv_file: Path, json_file: Path) -> None:
        """Test successful CLI execution."""
        exit_code = main(["-i", str(csv_file), "-o", str(json_file)])
        assert exit_code == 0

    def test_main_missing_file(self, json_file: Path) -> None:
        """Test CLI with missing input file."""
        exit_code = main(["-i", "nonexistent.csv", "-o", str(json_file)])
        assert exit_code == 1

    def test_main_dry_run(self, csv_file: Path, json_file: Path) -> None:
        """Test CLI dry-run mode."""
        exit_code = main(["-i", str(csv_file), "-o", str(json_file), "--dry-run"])
        assert exit_code == 0

    def test_main_verbose(self, csv_file: Path, json_file: Path) -> None:
        """Test CLI verbose mode."""
        exit_code = main(["-i", str(csv_file), "-o", str(json_file), "-v"])
        assert exit_code == 0
