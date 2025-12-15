"""JSON Repository for persisting user data."""

import json
import logging
from pathlib import Path
from typing import Dict, List

from data_importer.exceptions import DuplicateUserError, StorageError
from data_importer.models.user import User

logger = logging.getLogger(__name__)


class JSONRepository:
    """Repository for storing and retrieving users from JSON files.

    This class provides a persistent storage layer using JSON files.
    It implements the repository pattern for clean separation of
    data access from business logic.

    Attributes:
        file_path: Path to the JSON storage file.

    Example:
        >>> repo = JSONRepository("users.json")
        >>> with repo:
        ...     repo.save(user)
        ...     users = repo.load_all()
    """

    def __init__(self, file_path: str | Path) -> None:
        """Initialize JSONRepository with file path.

        Args:
            file_path: Path to the JSON storage file.
        """
        self.file_path = Path(file_path)
        self._users: Dict[str, User] = {}
        self._loaded = False

    def __enter__(self) -> "JSONRepository":
        """Enter context manager and load existing data.

        Returns:
            Self reference for use in with statement.
        """
        self._load_existing()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit context manager and save data if no error.

        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value if an error occurred.
            exc_tb: Exception traceback if an error occurred.

        Returns:
            False to propagate any exceptions.
        """
        if exc_type is None:
            self._persist()
        return False

    def _load_existing(self) -> None:
        """Load existing users from JSON file if it exists."""
        if self.file_path.exists():
            try:
                logger.info(f"Loading existing data from: {self.file_path}")
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Load users from JSON
                if isinstance(data, list):
                    for user_data in data:
                        user = User.from_dict(user_data)
                        self._users[user.user_id] = user

                logger.info(f"Loaded {len(self._users)} existing users")

            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in file: {e}")
                raise StorageError(
                    f"Invalid JSON format in storage file",
                    path=str(self.file_path),
                    details={"error": str(e)},
                ) from e
            except Exception as e:
                logger.error(f"Error loading storage file: {e}")
                raise StorageError(
                    f"Failed to load storage file: {e}",
                    path=str(self.file_path),
                ) from e
        else:
            logger.info(f"No existing data file found: {self.file_path}")

        self._loaded = True

    def _persist(self) -> None:
        """Persist users to JSON file."""
        try:
            # Ensure parent directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Saving {len(self._users)} users to: {self.file_path}")

            # Convert users to list of dicts
            data = [user.to_dict() for user in self._users.values()]

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info("Data saved successfully")

        except PermissionError as e:
            logger.error(f"Permission denied writing to: {self.file_path}")
            raise StorageError(
                f"Permission denied writing to file",
                path=str(self.file_path),
            ) from e
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            raise StorageError(
                f"Failed to save data: {e}",
                path=str(self.file_path),
            ) from e

    def exists(self, user_id: str) -> bool:
        """Check if a user with the given ID exists.

        Args:
            user_id: User ID to check.

        Returns:
            True if user exists, False otherwise.
        """
        return user_id in self._users

    def get(self, user_id: str) -> User | None:
        """Get a user by ID.

        Args:
            user_id: User ID to retrieve.

        Returns:
            User object if found, None otherwise.
        """
        return self._users.get(user_id)

    def save(self, user: User, allow_update: bool = False) -> None:
        """Save a user to the repository.

        Args:
            user: User object to save.
            allow_update: If True, allow updating existing users.

        Raises:
            DuplicateUserError: If user exists and allow_update is False.

        Example:
            >>> repo.save(User("U001", "Alice", "alice@example.com"))
        """
        if self.exists(user.user_id) and not allow_update:
            logger.warning(f"Duplicate user detected: {user.user_id}")
            raise DuplicateUserError(
                f"User with ID '{user.user_id}' already exists",
                user_id=user.user_id,
            )

        self._users[user.user_id] = user
        logger.debug(f"Saved user: {user.user_id}")

    def save_batch(
        self, users: List[User], skip_duplicates: bool = False
    ) -> tuple[int, int]:
        """Save multiple users to the repository.

        Args:
            users: List of User objects to save.
            skip_duplicates: If True, skip duplicates instead of raising.

        Returns:
            Tuple of (saved_count, skipped_count).

        Raises:
            DuplicateUserError: If duplicate found and skip_duplicates is False.
        """
        saved = 0
        skipped = 0

        for user in users:
            try:
                self.save(user)
                saved += 1
            except DuplicateUserError:
                if skip_duplicates:
                    logger.info(f"Skipping duplicate user: {user.user_id}")
                    skipped += 1
                else:
                    raise

        logger.info(f"Batch save complete: {saved} saved, {skipped} skipped")
        return saved, skipped

    def load_all(self) -> List[User]:
        """Load all users from the repository.

        Returns:
            List of all User objects in the repository.
        """
        return list(self._users.values())

    def count(self) -> int:
        """Get the number of users in the repository.

        Returns:
            Number of users stored.
        """
        return len(self._users)

    def clear(self) -> None:
        """Clear all users from the repository.

        Note:
            This does not persist changes until context manager exits.
        """
        self._users.clear()
        logger.info("Repository cleared")
