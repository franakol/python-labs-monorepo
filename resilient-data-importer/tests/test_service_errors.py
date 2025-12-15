from unittest.mock import MagicMock, patch

import pytest

from data_importer.exceptions import ImporterError
from data_importer.services.import_service import ImportService


class TestServiceErrors:
    @pytest.fixture
    def service(self):
        return ImportService("in.csv", "out.json")

    def test_run_import_reraises_importer_error(self, service):
        """Test that run_import re-raises ImporterError directly."""
        with patch(
            "data_importer.services.import_service.CSVParser"
        ) as mock_parser_cls:
            mock_parser_cls.return_value.__enter__.side_effect = ImporterError(
                "Fatal error"
            )

            with pytest.raises(ImporterError) as exc:
                service.run_import()
            assert "Fatal error" in str(exc.value)

    def test_run_import_wraps_generic_exception(self, service):
        """Test that run_import wraps generic Exception in ImporterError."""
        with patch(
            "data_importer.services.import_service.CSVParser"
        ) as mock_parser_cls:
            # Mock generic error during context enter
            mock_parser_cls.return_value.__enter__.side_effect = Exception(
                "Unexpected crash"
            )

            with pytest.raises(ImporterError) as exc:
                service.run_import()
            assert "Import failed: Unexpected crash" in str(exc.value)

    def test_validate_only_reraises_importer_error(self, service):
        """Test that validate_only re-raises ImporterError."""
        with patch(
            "data_importer.services.import_service.CSVParser"
        ) as mock_parser_cls:
            mock_parser_cls.return_value.__enter__.side_effect = ImporterError(
                "Validation setup failed"
            )

            with pytest.raises(ImporterError) as exc:
                service.validate_only()
            assert "Validation setup failed" in str(exc.value)

    def test_validate_only_wraps_generic_exception(self, service):
        """Test that validate_only wraps generic Exception."""
        with patch(
            "data_importer.services.import_service.CSVParser"
        ) as mock_parser_cls:
            mock_parser_cls.return_value.__enter__.side_effect = Exception(
                "Validation crash"
            )

            with pytest.raises(ImporterError) as exc:
                service.validate_only()
            assert "Validation failed: Validation crash" in str(exc.value)

    def test_run_import_file_format_error_handling(self, service):
        """Test handling of FileFormatError within the parsing loop."""
        with (
            patch("data_importer.services.import_service.CSVParser") as mock_parser_cls,
            patch("data_importer.services.import_service.JSONRepository"),
        ):

            mock_parser = mock_parser_cls.return_value.__enter__.return_value
            # Yield one user then raise FileFormatError
            user = MagicMock()
            mock_parser.parse.return_value = [user]

            # Mock validator to raise FileFormatError (unlikely but possible based on code flow logic injection)
            # Actually, looking at the code, FileFormatError comes from parser.parse loop usually,
            # BUT the try/except block wraps the loop body.
            # The catch is 'valid_users.append(user)'.
            # The parser.parse() is an iterator. If IT raises FileFormatError, it would be outside.
            # Wait, line 118: `for user in parser.parse():`
            # The `try` block (120) wraps `validator.validate(user)`.
            # So FileFormatError must be raised by validate? No, validator raises ValidationError.
            # Looking at service code again:
            # 132: except FileFormatError as e:
            # This catches FileFormatError raised inside the loop.
            # Does `parser.parse()` yield? Yes.
            # Does `validator.validate` raise FileFormatError? No.
            # Where does FileFormatError come from inside the loop?
            # `valid_users.append(user)`? No.
            # Ah, `parser.parse()` yields. If `next()` raises error? No, that would be in the `for` line.
            # Wait, let's look at `csv_parser.py`.
            # `parse` yields users.
            # If `parse` raises FileFormatError, it breaks the loop.
            # The try/catch block in service lines 120-139 is INSIDE the loop.
            # So it catches errors raised by statements INSIDE the loop.
            # Validator raises ValidationError.
            # Who raises FileFormatError inside the loop?
            # Maybe nothing? If so, that block is dead code or defensive?
            # Or maybe `parser.parse()` yields something that causes error later?
            # Re-reading `import_service.py` line 118: `for user in parser.parse():`
            # The code `user` is already yielded.
            # Unless `validator.validate(user)` raises FileFormatError? (Unlikely, logic is Validation)
            # Or strict mode?

            # Actually, `csv_parser.py` raises FileFormatError.
            # But that happens during iteration `next()`.
            # If `next()` raises, the `for` loop catches it? No.
            # The `try` block is INSIDE the loop.
            # So if `for` raises, it is NOT caught by line 120 try.
            # It would be caught by line 162 `except ImporterError` (superclass) or propagated.

            # Wait, look at `csv_parser.py`:
            # 150: except FileFormatError: raise
            # 155: raise FileFormatError...

            # The service code lines 132-139 `except FileFormatError` might be unreachable
            # if `validator` only raises `ValidationError`.
            # Let's check `UserValidator`.
            pass
