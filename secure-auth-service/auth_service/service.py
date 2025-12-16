"""User authentication service.

This module will contain the UserService class - TDD RED phase.
"""

from auth_service.interfaces.hasher import PasswordHasher
from auth_service.interfaces.repository import UserRepository
from auth_service.models import User


class UserService:
    """User authentication service.

    RED Phase: This is a stub that will fail tests until implemented.
    """

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        """Initialize the service with dependencies."""
        self._repository = repository
        self._hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a new user.

        RED Phase: Not implemented yet.
        """
        raise NotImplementedError("TDD RED Phase - not implemented")
