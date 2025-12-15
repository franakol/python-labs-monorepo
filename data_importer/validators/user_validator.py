"""User data validator module."""

import logging
import re
from typing import List

from data_importer.exceptions import ValidationError
from data_importer.models.user import User

logger = logging.getLogger(__name__)


class UserValidator:
    """Validator for User data objects.

    This class provides validation methods for User objects,
    checking email format, user ID format, and other constraints.

    Attributes:
        EMAIL_PATTERN: Regex pattern for validating email addresses.
        USER_ID_PATTERN: Regex pattern for validating user IDs.

    Example:
        >>> validator = UserValidator()
        >>> user = User("U001", "Alice", "alice@example.com")
        >>> validator.validate(user)  # Returns True or raises ValidationError
    """

    # Simple but effective email regex
    EMAIL_PATTERN = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    # User ID pattern: alphanumeric with optional hyphens/underscores
    USER_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")

    def __init__(self) -> None:
        """Initialize UserValidator."""
        self._errors: List[ValidationError] = []

    def validate(self, user: User) -> bool:
        """Validate a User object.

        Performs all validation checks on the user and raises
        ValidationError if any checks fail.

        Args:
            user: User object to validate.

        Returns:
            True if user is valid.

        Raises:
            ValidationError: If any validation check fails.

        Example:
            >>> validator = UserValidator()
            >>> validator.validate(User("U001", "Alice", "alice@example.com"))
            True
        """
        logger.debug(f"Validating user: {user.user_id}")

        self._validate_user_id(user.user_id)
        self._validate_name(user.name)
        self._validate_email(user.email)

        logger.info(f"User {user.user_id} passed validation")
        return True

    def _validate_user_id(self, user_id: str) -> None:
        """Validate user ID format.

        Args:
            user_id: User ID string to validate.

        Raises:
            ValidationError: If user ID is empty or invalid format.
        """
        if not user_id:
            raise ValidationError(
                "User ID cannot be empty",
                field="user_id",
                value=user_id,
            )

        if len(user_id) < 1 or len(user_id) > 50:
            raise ValidationError(
                "User ID must be between 1 and 50 characters",
                field="user_id",
                value=user_id,
            )

        if not self.USER_ID_PATTERN.match(user_id):
            raise ValidationError(
                "User ID must start with alphanumeric and contain only "
                "letters, numbers, hyphens, and underscores",
                field="user_id",
                value=user_id,
            )

    def _validate_name(self, name: str) -> None:
        """Validate user name.

        Args:
            name: Name string to validate.

        Raises:
            ValidationError: If name is empty or too long.
        """
        if not name:
            raise ValidationError(
                "Name cannot be empty",
                field="name",
                value=name,
            )

        if len(name) < 1 or len(name) > 200:
            raise ValidationError(
                "Name must be between 1 and 200 characters",
                field="name",
                value=name,
            )

        # Check for only whitespace
        if not name.strip():
            raise ValidationError(
                "Name cannot contain only whitespace",
                field="name",
                value=name,
            )

    def _validate_email(self, email: str) -> None:
        """Validate email address format.

        Args:
            email: Email string to validate.

        Raises:
            ValidationError: If email is empty or invalid format.
        """
        if not email:
            raise ValidationError(
                "Email cannot be empty",
                field="email",
                value=email,
            )

        if not self.EMAIL_PATTERN.match(email):
            raise ValidationError(
                "Invalid email format",
                field="email",
                value=email,
            )

    def validate_batch(self, users: List[User]) -> List[User]:
        """Validate a batch of users, returning only valid ones.

        Args:
            users: List of User objects to validate.

        Returns:
            List of valid User objects.

        Note:
            Invalid users are logged but not included in the result.
        """
        valid_users: List[User] = []

        for user in users:
            try:
                self.validate(user)
                valid_users.append(user)
            except ValidationError as e:
                logger.warning(f"Skipping invalid user {user.user_id}: {e}")

        logger.info(f"Validated {len(valid_users)}/{len(users)} users")
        return valid_users
