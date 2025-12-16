"""Tests for user login functionality.

TDD Red Phase: These tests will fail until we implement
the UserService.login() method.
"""

from unittest.mock import Mock

import pytest

from auth_service.exceptions import InvalidPasswordError, UserNotFoundError
from auth_service.interfaces.hasher import PasswordHasher
from auth_service.interfaces.repository import UserRepository
from auth_service.models import User
from auth_service.service import UserService


class TestUserLogin:
    """Tests for user login/credential verification."""

    def test_login_successfully_with_valid_credentials(self) -> None:
        """Test that a user can login with correct credentials.

        RED Phase: Fails because UserService.login() doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)

        # Setup: user exists with hashed password
        stored_user = User(username="john_doe", password_hash="hashed_password")
        mock_repo.find_by_username.return_value = stored_user
        mock_hasher.verify.return_value = True

        service = UserService(repository=mock_repo, hasher=mock_hasher)
        user = service.login("john_doe", "correct_password")

        assert user.username == "john_doe"
        mock_repo.find_by_username.assert_called_once_with("john_doe")
        mock_hasher.verify.assert_called_once_with(
            "correct_password", "hashed_password"
        )


class TestUserNotFoundError:
    """Tests for login with non-existent user."""

    def test_login_raises_error_for_unknown_user(self) -> None:
        """Test that login with unknown user raises error.

        RED Phase: Fails because UserService.login() doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)
        mock_repo.find_by_username.return_value = None

        service = UserService(repository=mock_repo, hasher=mock_hasher)

        with pytest.raises(UserNotFoundError) as exc_info:
            service.login("unknown_user", "password123")

        assert exc_info.value.username == "unknown_user"


class TestInvalidPasswordError:
    """Tests for login with wrong password."""

    def test_login_raises_error_for_wrong_password(self) -> None:
        """Test that login with wrong password raises error.

        RED Phase: Fails because UserService.login() doesn't exist.
        """
        mock_repo = Mock(spec=UserRepository)
        mock_hasher = Mock(spec=PasswordHasher)

        stored_user = User(username="john_doe", password_hash="hashed_password")
        mock_repo.find_by_username.return_value = stored_user
        mock_hasher.verify.return_value = False  # Wrong password

        service = UserService(repository=mock_repo, hasher=mock_hasher)

        with pytest.raises(InvalidPasswordError):
            service.login("john_doe", "wrong_password")
