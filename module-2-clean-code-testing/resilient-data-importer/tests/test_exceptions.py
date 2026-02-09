from data_importer.exceptions import (
    DuplicateUserError,
    FileFormatError,
    ImporterError,
    StorageError,
    ValidationError,
)


class TestExceptions:
    def test_importer_error_str(self):
        err = ImporterError("Base error")
        assert str(err) == "Base error"

        err_with_details = ImporterError("Base error", details={"code": 123})
        assert str(err_with_details) == "Base error | Details: {'code': 123}"

    def test_file_format_error_init(self):
        err = FileFormatError("Bad format", line_number=5, details={"col": "a"})
        assert err.line_number == 5
        assert err.details["line_number"] == 5
        assert err.details["col"] == "a"

        err_no_line = FileFormatError("Bad format")
        assert err_no_line.line_number is None
        assert "line_number" not in err_no_line.details

    def test_validation_error_init(self):
        err = ValidationError("Bad val", field="email", value="x", details={"id": 1})
        assert err.field == "email"
        assert err.value == "x"
        assert err.details["field"] == "email"
        assert err.details["value"] == "x"
        assert err.details["id"] == 1

        err_defaults = ValidationError("Bad val")
        assert err_defaults.field is None
        assert err_defaults.value is None
        assert "field" not in err_defaults.details

    def test_duplicate_user_error_init(self):
        err = DuplicateUserError("Dup", user_id="U1")
        assert err.user_id == "U1"
        assert err.details["user_id"] == "U1"

        err_defaults = DuplicateUserError("Dup")
        assert err_defaults.user_id is None
        assert "user_id" not in err_defaults.details

    def test_storage_error_init(self):
        err = StorageError("Disk full", path="/tmp/x")
        assert err.path == "/tmp/x"
        assert err.details["path"] == "/tmp/x"

        err_defaults = StorageError("Disk full")
        assert err_defaults.path is None
        assert "path" not in err_defaults.details
