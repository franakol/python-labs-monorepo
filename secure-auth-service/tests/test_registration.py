"""Tests for user registration functionality.

TDD Red Phase: These tests will fail until we implement
the UserService, InMemoryUserRepository, and BcryptPasswordHasher.
"""

from unittest.mock import Mock

import pytest

from auth_service.exceptions import UserAlreadyExistsError, WeakPasswordError
from auth_service.interfaces.hasher import PasswordHasher
from auth_service.interfaces.repository import UserRepository
from auth_service.service import UserService


class TestUserRegistration:
    """Tests for user registration."""

    def test_register_user_successfully(self) -> None:
        """Test that a user can be registered successfully.

        RED Phase: Fails because UserService doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)

        mock_repo.exists.return_value = False
        mock_hasher.hash.return_value = "hashed_password_123"

        service = UserService(repository=mock_repo, hasher=mock_hasher)
        user = service.register("john_doe", "SecurePass123!")

        assert user.username == "john_doe"
        assert user.password_hash == "hashed_password_123"
        mock_repo.save.assert_called_once()
        mock_hasher.hash.assert_called_once_with("SecurePass123!")

    def test_register_calls_repository_exists_check(self) -> None:
        """Test that registration checks if user already exists.

        RED Phase: Fails because UserService doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)
        mock_repo.exists.return_value = False
        mock_hasher.hash.return_value = "hashed"

        service = UserService(repository=mock_repo, hasher=mock_hasher)
        service.register("new_user", "SecurePass123!")

        mock_repo.exists.assert_called_once_with("new_user")


class TestUserAlreadyExistsError:
    """Tests for duplicate user registration."""

    def test_register_raises_error_for_existing_user(self) -> None:
        """Test that registering an existing user raises error.

        RED Phase: Fails because UserService doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)
        mock_repo.exists.return_value = True

        service = UserService(repository=mock_repo, hasher=mock_hasher)

        with pytest.raises(UserAlreadyExistsError) as exc_info:
            service.register("existing_user", "SecurePass123!")

        assert exc_info.value.username == "existing_user"


class TestPasswordPolicy:
    """Tests for password policy enforcement."""

    def test_register_raises_error_for_short_password(self) -> None:
        """Test that weak passwords are rejected.

        RED Phase: Fails because UserService doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)
        mock_repo.exists.return_value = False

        service = UserService(repository=mock_repo, hasher=mock_hasher)

        with pytest.raises(WeakPasswordError) as exc_info:
            service.register("john_doe", "short")

        assert "minimum" in exc_info.value.reason.lower()

    def test_register_accepts_strong_password(self) -> None:
        """Test that strong passwords are accepted.

        RED Phase: Fails because UserService doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)
        mock_repo.exists.return_value = False
        mock_hasher.hash.return_value = "hashed"

        service = UserService(repository=mock_repo, hasher=mock_hasher)

        # Should not raise
        user = service.register("john_doe", "SecurePass123!")
        assert user is not None
