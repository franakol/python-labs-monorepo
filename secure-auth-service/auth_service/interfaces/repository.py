"""Abstract repository interface for user storage."""

from abc import ABC, abstractmethod

from auth_service.models import User


class UserRepository(ABC):
    """Abstract base class for user data storage.

    Implementations must provide methods for saving and retrieving users.
    This follows the Dependency Inversion Principle (DIP).
    """

    @abstractmethod
    def save(self, user: User) -> None:
        """Save a user to the repository.

        Args:
            user: The user entity to save.
        """
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to search for.

        Returns:
            The User if found, None otherwise.
        """
        pass

    @abstractmethod
    def exists(self, username: str) -> bool:
        """Check if a username already exists.

        Args:
            username: The username to check.

        Returns:
            True if the username exists, False otherwise.
        """
        pass
