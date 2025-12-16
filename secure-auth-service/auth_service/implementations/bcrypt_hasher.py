"""Bcrypt password hasher implementation."""

import bcrypt  # type: ignore[import-not-found]

from auth_service.interfaces.hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Bcrypt implementation of PasswordHasher.

    Uses bcrypt for secure password hashing with automatic salting.
    """

    def hash(self, password: str) -> str:
        """Hash a plaintext password using bcrypt.

        Args:
            password: The plaintext password to hash.

        Returns:
            The bcrypt-hashed password string.
        """
        salt = bcrypt.gensalt()
        hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        """Verify a password against a bcrypt hash.

        Args:
            password: The plaintext password to verify.
            hashed: The bcrypt hash to check against.

        Returns:
            True if the password matches, False otherwise.
        """
        result: bool = bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        return result
