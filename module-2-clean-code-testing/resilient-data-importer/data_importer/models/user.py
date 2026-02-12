"""User data model."""

from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    """Represents a user entity for import/export operations.

    This dataclass represents user data with required fields for
    identification and contact information.

    Attributes:
        user_id: Unique identifier for the user (e.g., "U001").
        name: Full name of the user.
        email: Email address of the user.

    Example:
        >>> user = User(user_id="U001", name="Alice", email="alice@example.com")
        >>> print(user)
        User(user_id='U001', name='Alice', email='alice@example.com')
    """

    user_id: str
    name: str
    email: str

    def to_dict(self) -> dict[str, Any]:
        """Convert User to dictionary representation.

        Returns:
            Dictionary with user_id, name, and email keys.

        Example:
            >>> user = User("U001", "Alice", "alice@example.com")
            >>> user.to_dict()
            {'user_id': 'U001', 'name': 'Alice', 'email': 'alice@example.com'}
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        """Create User instance from dictionary.

        Args:
            data: Dictionary containing user_id, name, and email.

        Returns:
            User instance created from the dictionary data.

        Raises:
            KeyError: If required fields are missing from the dictionary.

        Example:
            >>> data = {"user_id": "U001", "name": "Alice", "email": "alice@example.com"}
            >>> user = User.from_dict(data)
        """
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
        )
