"""Tests for concrete implementations."""

from auth_service.implementations.bcrypt_hasher import BcryptPasswordHasher
from auth_service.implementations.memory_repository import InMemoryUserRepository
from auth_service.models import User


class TestInMemoryUserRepository:
    """Tests for InMemoryUserRepository."""

    def test_save_and_find_user(self) -> None:
        """Test saving and finding a user."""
        repo = InMemoryUserRepository()
        user = User(username="john_doe", password_hash="hash123")

        repo.save(user)
        found = repo.find_by_username("john_doe")

        assert found is not None
        assert found.username == "john_doe"
        assert found.password_hash == "hash123"

    def test_find_returns_none_for_unknown_user(self) -> None:
        """Test that find returns None for unknown user."""
        repo = InMemoryUserRepository()

        found = repo.find_by_username("unknown")

        assert found is None

    def test_exists_returns_true_for_saved_user(self) -> None:
        """Test that exists returns True for saved user."""
        repo = InMemoryUserRepository()
        user = User(username="john_doe", password_hash="hash123")

        repo.save(user)

        assert repo.exists("john_doe") is True

    def test_exists_returns_false_for_unknown_user(self) -> None:
        """Test that exists returns False for unknown user."""
        repo = InMemoryUserRepository()

        assert repo.exists("unknown") is False


class TestBcryptPasswordHasher:
    """Tests for BcryptPasswordHasher."""

    def test_hash_returns_hashed_string(self) -> None:
        """Test that hash returns a hashed string."""
        hasher = BcryptPasswordHasher()

        hashed = hasher.hash("password123")

        assert hashed != "password123"
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt prefix

    def test_verify_returns_true_for_correct_password(self) -> None:
        """Test that verify returns True for correct password."""
        hasher = BcryptPasswordHasher()
        hashed = hasher.hash("SecurePass123!")

        result = hasher.verify("SecurePass123!", hashed)

        assert result is True

    def test_verify_returns_false_for_wrong_password(self) -> None:
        """Test that verify returns False for wrong password."""
        hasher = BcryptPasswordHasher()
        hashed = hasher.hash("SecurePass123!")

        result = hasher.verify("WrongPassword", hashed)

        assert result is False
