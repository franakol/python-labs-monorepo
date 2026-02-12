"""Tests for the user validator module."""

import pytest

from data_importer.exceptions import ValidationError
from data_importer.models.user import User
from data_importer.validators.user_validator import UserValidator


class TestUserValidator:
    """Tests for UserValidator class."""

    @pytest.fixture
    def validator(self) -> UserValidator:
        """Create a validator instance for testing."""
        return UserValidator()

    def test_validate_valid_user(
        self, validator: UserValidator, sample_user: User
    ) -> None:
        """Test validation passes for valid user."""
        result = validator.validate(sample_user)
        assert result is True

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@subdomain.example.com",
            "a@b.co",
        ],
    )
    def test_valid_emails(self, validator: UserValidator, email: str) -> None:
        """Test validation passes for valid email formats."""
        user = User(user_id="U001", name="Test User", email=email)
        assert validator.validate(user) is True

    @pytest.mark.parametrize(
        "email",
        [
            "invalid",
            "invalid@",
            "@example.com",
            "user@.com",
            "user@example.",
            "",
        ],
    )
    def test_invalid_emails(self, validator: UserValidator, email: str) -> None:
        """Test validation fails for invalid email formats."""
        user = User(user_id="U001", name="Test User", email=email)

        with pytest.raises(ValidationError) as exc_info:
            validator.validate(user)

        assert exc_info.value.field == "email"

    @pytest.mark.parametrize(
        "user_id",
        [
            "U001",
            "user-123",
            "USER_456",
            "a",
            "A1B2C3",
        ],
    )
    def test_valid_user_ids(self, validator: UserValidator, user_id: str) -> None:
        """Test validation passes for valid user IDs."""
        user = User(user_id=user_id, name="Test", email="test@example.com")
        assert validator.validate(user) is True

    @pytest.mark.parametrize(
        "user_id",
        [
            "",
            "-invalid",
            "_invalid",
            "has space",
            "has@special",
        ],
    )
    def test_invalid_user_ids(self, validator: UserValidator, user_id: str) -> None:
        """Test validation fails for invalid user IDs."""
        user = User(user_id=user_id, name="Test", email="test@example.com")

        with pytest.raises(ValidationError) as exc_info:
            validator.validate(user)

        assert exc_info.value.field == "user_id"

    @pytest.mark.parametrize(
        "name",
        [
            "Alice",
            "Bob Smith",
            "Mary Jane Watson-Parker",
            "José García",
        ],
    )
    def test_valid_names(self, validator: UserValidator, name: str) -> None:
        """Test validation passes for valid names."""
        user = User(user_id="U001", name=name, email="test@example.com")
        assert validator.validate(user) is True

    @pytest.mark.parametrize(
        "name",
        [
            "",
            "   ",
            "\t\n",
        ],
    )
    def test_invalid_names(self, validator: UserValidator, name: str) -> None:
        """Test validation fails for empty or whitespace-only names."""
        user = User(user_id="U001", name=name, email="test@example.com")

        with pytest.raises(ValidationError) as exc_info:
            validator.validate(user)

        assert exc_info.value.field == "name"

    def test_validate_batch_all_valid(
        self, validator: UserValidator, sample_users: list[User]
    ) -> None:
        """Test batch validation with all valid users."""
        valid_users = validator.validate_batch(sample_users)
        assert len(valid_users) == len(sample_users)

    def test_validate_batch_with_invalid(self, validator: UserValidator) -> None:
        """Test batch validation filters out invalid users."""
        users = [
            User(user_id="U001", name="Valid", email="valid@example.com"),
            User(user_id="U002", name="Invalid", email="invalid-email"),
            User(user_id="U003", name="Valid2", email="valid2@example.com"),
        ]

        valid_users = validator.validate_batch(users)
        assert len(valid_users) == 2
        assert all(u.user_id != "U002" for u in valid_users)
