"""User data model."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class User:
    """User entity for authentication.

    Attributes:
        id: Unique identifier for the user.
        username: Unique username for login.
        password_hash: Bcrypt-hashed password (never store plaintext).
        created_at: Timestamp when user was created.
    """

    username: str
    password_hash: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
