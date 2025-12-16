"""In-memory user repository implementation."""

from auth_service.interfaces.repository import UserRepository
from auth_service.models import User


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository.

    Stores users in a dictionary for testing and development.

    Attributes:
        _users: Dictionary mapping usernames to User objects.
    """

    def __init__(self) -> None:
        """Initialize empty user storage."""
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        """Save a user to the repository.

        Args:
            user: The user entity to save.
        """
        self._users[user.username] = user

    def find_by_username(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to search for.

        Returns:
            The User if found, None otherwise.
        """
        return self._users.get(username)

    def exists(self, username: str) -> bool:
        """Check if a username already exists.

        Args:
            username: The username to check.

        Returns:
            True if the username exists, False otherwise.
        """
        return username in self._users
