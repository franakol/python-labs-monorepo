from unittest.mock import patch

from data_importer.cli import main
from data_importer.services.import_service import ImportResult


class TestCLIErrors:
    def test_main_keyboard_interrupt(self, capsys):
        """Test handling of KeyboardInterrupt."""
        with patch("data_importer.cli.ImportService") as mock_service_cls:
            mock_service = mock_service_cls.return_value
            # Mock run_import to raise KeyboardInterrupt
            mock_service.run_import.side_effect = KeyboardInterrupt()

            with patch(
                "sys.argv", ["prog", "--input", "in.csv", "--output", "out.json"]
            ):
                exit_code = main()

            assert exit_code == 130
            stderr = capsys.readouterr().err
            assert "Import cancelled" in stderr

    def test_main_generic_exception(self, capsys):
        """Test handling of unexpected exceptions."""
        with patch("data_importer.cli.ImportService") as mock_service_cls:
            mock_service = mock_service_cls.return_value
            # Mock run_import to raise a generic Exception
            mock_service.run_import.side_effect = Exception(
                "Unexpected infrastructure fail"
            )

            with patch(
                "sys.argv", ["prog", "--input", "in.csv", "--output", "out.json"]
            ):
                exit_code = main()

            assert exit_code == 1
            stderr = capsys.readouterr().err
            assert "Unexpected error: Unexpected infrastructure fail" in stderr

    def test_main_many_errors_display(self, capsys):
        """Test display truncation when there are many errors."""
        with patch("data_importer.cli.ImportService") as mock_service_cls:
            mock_service = mock_service_cls.return_value
            # return result with 15 errors
            errors = [f"Error {i}" for i in range(15)]
            mock_service.run_import.return_value = ImportResult(
                total_rows=20, imported=5, skipped=15, errors=errors
            )

            with patch(
                "sys.argv", ["prog", "--input", "in.csv", "--output", "out.json"]
            ):
                exit_code = main()

            assert exit_code == 0  # Imported > 0 is partial success

            captured = capsys.readouterr()
            assert "Error 0" in captured.out
            assert "Error 9" in captured.out
            assert "... and 5 more errors" in captured.out
            assert "Error 10" not in captured.out

    def test_main_import_failure_result(self, caplog):
        """Test exit code 1 when result.success is False."""
        with patch("data_importer.cli.ImportService") as mock_service_cls:
            mock_service = mock_service_cls.return_value
            # Result with errors means success=False
            mock_service.run_import.return_value = ImportResult(
                total_rows=1, imported=0, skipped=1, errors=["Some error"]
            )

            with patch(
                "sys.argv", ["prog", "--input", "in.csv", "--output", "out.json"]
            ):
                exit_code = main()

            assert exit_code == 1
            assert "Import completed with issues" in caplog.text
