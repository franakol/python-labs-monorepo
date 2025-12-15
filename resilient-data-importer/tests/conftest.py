"""Shared test fixtures for the data importer tests."""

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from data_importer.models.user import User


@pytest.fixture
def sample_user() -> User:
    """Create a sample valid user for testing."""
    return User(user_id="U001", name="Alice Johnson", email="alice@example.com")


@pytest.fixture
def sample_users() -> list[User]:
    """Create a list of sample users for testing."""
    return [
        User(user_id="U001", name="Alice Johnson", email="alice@example.com"),
        User(user_id="U002", name="Bob Smith", email="bob@example.com"),
        User(user_id="U003", name="Carol White", email="carol@example.com"),
    ]


@pytest.fixture
def valid_csv_content() -> str:
    """Valid CSV content for testing."""
    return """user_id,name,email
U001,Alice Johnson,alice@example.com
U002,Bob Smith,bob@example.com
U003,Carol White,carol@example.com"""


@pytest.fixture
def malformed_csv_content() -> str:
    """CSV content with malformed rows."""
    return """user_id,name,email
U001,Alice Johnson,alice@example.com
U002,Bob Smith
U003,Carol White,carol@example.com"""


@pytest.fixture
def csv_missing_headers() -> str:
    """CSV content with missing required headers."""
    return """id,full_name,contact
U001,Alice Johnson,alice@example.com"""


@pytest.fixture
def csv_with_duplicates() -> str:
    """CSV content with duplicate user IDs."""
    return """user_id,name,email
U001,Alice Johnson,alice@example.com
U001,Alice Duplicate,alice2@example.com
U002,Bob Smith,bob@example.com"""


@pytest.fixture
def temp_csv_file(valid_csv_content: str) -> Generator[Path, None, None]:
    """Create a temporary CSV file with valid content."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write(valid_csv_content)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_malformed_csv(malformed_csv_content: str) -> Generator[Path, None, None]:
    """Create a temporary CSV file with malformed content."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write(malformed_csv_content)
        temp_path = Path(f.name)

    yield temp_path

    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_json_file() -> Generator[Path, None, None]:
    """Create a temporary JSON file path."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        temp_path = Path(f.name)

    yield temp_path

    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def temp_json_with_users(sample_users: list[User]) -> Generator[Path, None, None]:
    """Create a temporary JSON file with existing users."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        data = [user.to_dict() for user in sample_users]
        json.dump(data, f)
        temp_path = Path(f.name)

    yield temp_path

    if temp_path.exists():
        temp_path.unlink()
