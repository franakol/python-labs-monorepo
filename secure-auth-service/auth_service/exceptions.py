"""Custom exceptions for the authentication service."""


class AuthServiceError(Exception):
    """Base exception for all auth service errors."""

    pass


class UserAlreadyExistsError(AuthServiceError):
    """Raised when attempting to register a user that already exists."""

    def __init__(self, username: str) -> None:
        """Initialize with the duplicate username.

        Args:
            username: The username that already exists.
        """
        self.username = username
        super().__init__(f"User already exists: {username}")


class UserNotFoundError(AuthServiceError):
    """Raised when a user cannot be found."""

    def __init__(self, username: str) -> None:
        """Initialize with the missing username.

        Args:
            username: The username that was not found.
        """
        self.username = username
        super().__init__(f"User not found: {username}")


class InvalidPasswordError(AuthServiceError):
    """Raised when password verification fails."""

    def __init__(self) -> None:
        """Initialize the invalid password error."""
        super().__init__("Invalid password")


class WeakPasswordError(AuthServiceError):
    """Raised when a password doesn't meet policy requirements."""

    def __init__(self, reason: str) -> None:
        """Initialize with the policy violation reason.

        Args:
            reason: Description of why the password is weak.
        """
        self.reason = reason
        super().__init__(f"Weak password: {reason}")
