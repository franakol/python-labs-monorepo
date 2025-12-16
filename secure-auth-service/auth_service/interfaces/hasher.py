"""Abstract password hasher interface."""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Abstract base class for password hashing.

    Implementations must provide secure hashing and verification.
    This follows the Dependency Inversion Principle (DIP).
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plaintext password.

        Args:
            password: The plaintext password to hash.

        Returns:
            The hashed password string.
        """
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        """Verify a password against a hash.

        Args:
            password: The plaintext password to verify.
            hashed: The hashed password to check against.

        Returns:
            True if the password matches, False otherwise.
        """
        pass
