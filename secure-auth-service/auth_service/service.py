"""User authentication service.

This module contains the UserService class for user registration and login.
"""

import logging

from auth_service.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
    WeakPasswordError,
)
from auth_service.interfaces.hasher import PasswordHasher
from auth_service.interfaces.repository import UserRepository
from auth_service.models import User

logger = logging.getLogger(__name__)

# Password policy constants
MIN_PASSWORD_LENGTH = 8


class UserService:
    """User authentication service.

    Handles user registration and login with dependency injection
    for repository and password hasher.

    Attributes:
        _repository: Storage for user data.
        _hasher: Password hashing implementation.
    """

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        """Initialize the service with dependencies.

        Args:
            repository: User storage implementation.
            hasher: Password hashing implementation.
        """
        self._repository = repository
        self._hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a new user.

        Args:
            username: Unique username for the new user.
            password: Plaintext password (will be hashed).

        Returns:
            The newly created User.

        Raises:
            UserAlreadyExistsError: If username is already taken.
            WeakPasswordError: If password doesn't meet policy.
        """
        logger.info(f"Attempting to register user: {username}")

        # Check password policy
        self._validate_password(password)

        # Check if user exists
        if self._repository.exists(username):
            logger.warning(f"Registration failed - user exists: {username}")
            raise UserAlreadyExistsError(username)

        # Hash password and create user
        password_hash = self._hasher.hash(password)
        user = User(username=username, password_hash=password_hash)

        # Save user
        self._repository.save(user)
        logger.info(f"User registered successfully: {username}")

        return user

    def _validate_password(self, password: str) -> None:
        """Validate password against policy.

        Args:
            password: The password to validate.

        Raises:
            WeakPasswordError: If password doesn't meet requirements.
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise WeakPasswordError(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters "
                f"(minimum length requirement)"
            )

    def login(self, username: str, password: str) -> User:
        """Authenticate a user with credentials.

        Args:
            username: The username to authenticate.
            password: The plaintext password to verify.

        Returns:
            The authenticated User.

        Raises:
            UserNotFoundError: If the username doesn't exist.
            InvalidPasswordError: If the password is incorrect.
        """
        logger.info(f"Login attempt for user: {username}")

        # Find user
        user = self._repository.find_by_username(username)
        if user is None:
            logger.warning(f"Login failed - user not found: {username}")
            raise UserNotFoundError(username)

        # Verify password
        if not self._hasher.verify(password, user.password_hash):
            logger.warning(f"Login failed - invalid password for: {username}")
            raise InvalidPasswordError()

        logger.info(f"User logged in successfully: {username}")
        return user
