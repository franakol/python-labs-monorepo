from unittest.mock import MagicMock, patch

import pytest

from data_importer.exceptions import ImporterError, StorageError
from data_importer.parsers.csv_parser import CSVParser
from data_importer.repositories.json_repository import JSONRepository


class TestCornerCases:
    # --- CSVParser Tests ---
    def test_csv_parser_permission_error(self):
        """Test PermissionError during file open in CSVParser."""
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            parser = CSVParser("protected.csv")
            with pytest.raises(ImporterError) as exc:
                with parser:
                    pass
            assert "Permission denied" in str(exc.value)

    def test_csv_parser_generic_open_error(self):
        """Test generic Exception during file open in CSVParser."""
        with patch("builtins.open", side_effect=OSError("Disk fail")):
            parser = CSVParser("broken.csv")
            with pytest.raises(ImporterError) as exc:
                with parser:
                    pass
            assert "Failed to open CSV file" in str(exc.value)

    def test_csv_parser_parse_not_open_error(self):
        """Test Parse error when file not open."""
        parser = CSVParser("test.csv")
        with pytest.raises(ImporterError) as exc:
            list(parser.parse())
        assert "File not open" in str(exc.value)

    # --- JSONRepository Load Tests ---
    def test_json_repo_load_permission_error(self):
        """Test PermissionError during JSON load."""
        # Patch Path so it doesn't exist during init
        with patch("data_importer.repositories.json_repository.Path") as MockPath:
            MockPath.return_value.exists.return_value = False
            repo = JSONRepository("protected.json")

            # Now enable exists and mock open failure
            repo.file_path.exists.return_value = True
            repo.file_path.__str__.return_value = "protected.json"

            with patch("builtins.open", side_effect=PermissionError("No read access")):
                with pytest.raises(StorageError) as exc:
                    repo._load_existing()
                assert "Failed to load storage file" in str(exc.value)

    def test_json_repo_load_generic_error(self):
        """Test generic Exception during JSON load."""
        with patch("data_importer.repositories.json_repository.Path") as MockPath:
            MockPath.return_value.exists.return_value = False
            repo = JSONRepository("broken.json")

            repo.file_path.exists.return_value = True

            with patch("builtins.open", side_effect=OSError("Read fail")):
                with pytest.raises(StorageError) as exc:
                    repo._load_existing()
                assert "Failed to load storage file" in str(exc.value)

    # --- JSONRepository Persist Tests ---
    def test_json_repo_persist_permission_error(self):
        """Test PermissionError during persist."""
        # We need a repo that didn't fail on init.
        # So mocks Path to NOT exist initially.
        with patch("data_importer.repositories.json_repository.Path") as MockPath:
            MockPath.return_value.exists.return_value = False
            repo = JSONRepository("out.json")

            # Now setup repo.file_path for persist logic
            # _persist calls: self.file_path.parent.mkdir(...) and open(self.file_path, 'w')
            repo.file_path = MagicMock()
            repo.file_path.parent.mkdir.return_value = None
            repo.file_path.__str__.return_value = "out.json"

            with patch("builtins.open", side_effect=PermissionError("No write access")):
                with pytest.raises(StorageError) as exc:
                    repo._persist()
                # Updated assertion to match actual code message
                assert "Permission denied writing to file" in str(exc.value)

    def test_json_repo_persist_generic_error(self):
        """Test generic Exception during persist."""
        with patch("data_importer.repositories.json_repository.Path") as MockPath:
            MockPath.return_value.exists.return_value = False
            repo = JSONRepository("out.json")

            repo.file_path = MagicMock()
            repo.file_path.parent.mkdir.return_value = None

            with patch("builtins.open", side_effect=OSError("Write fail")):
                with pytest.raises(StorageError) as exc:
                    repo._persist()
                assert "Failed to save data" in str(exc.value)
