"""Data models for the git-config-manager application.

This module defines the core data structures used throughout
the application for representing configurations and Git metadata.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ConfigFormat(Enum):
    """Supported configuration file formats."""

    JSON = "json"
    YAML = "yaml"


@dataclass(frozen=True)
class CommitInfo:
    """Information about a Git commit.

    Attributes:
        sha: The commit SHA hash.
        message: The commit message.
        author: The commit author name.
        timestamp: When the commit was created.
    """

    sha: str
    message: str
    author: str
    timestamp: datetime


@dataclass
class ConfigEntry:
    """Represents a configuration entry.

    Attributes:
        name: Unique name identifying this configuration.
        content: The configuration data as a dictionary.
        format: The file format (JSON or YAML).
        path: Path to the config file relative to repo root.
    """

    name: str
    content: dict[str, Any]
    format: ConfigFormat = ConfigFormat.JSON
    path: Path | None = None

    def __post_init__(self) -> None:
        """Set default path if not provided."""
        if self.path is None:
            self.path = Path(f"{self.name}.{self.format.value}")


@dataclass
class ConfigVersion:
    """A specific version of a configuration.

    Represents the state of a configuration at a specific commit.

    Attributes:
        config: The configuration entry.
        commit: Information about the commit that created this version.
        branch: The branch this version exists on.
    """

    config: ConfigEntry
    commit: CommitInfo
    branch: str


@dataclass
class MergeResult:
    """Result of a merge operation.

    Attributes:
        success: Whether the merge completed without conflicts.
        source_branch: The branch that was merged from.
        target_branch: The branch that was merged into.
        commit_sha: The SHA of the merge commit (if successful).
        conflicts: List of conflicting file paths (if any).
        message: Human-readable result message.
    """

    success: bool
    source_branch: str
    target_branch: str
    commit_sha: str | None = None
    conflicts: list[Path] = field(default_factory=list)
    message: str = ""

    def __post_init__(self) -> None:
        """Set default message based on result."""
        if not self.message:
            if self.success:
                self.message = (
                    f"Successfully merged '{self.source_branch}' into "
                    f"'{self.target_branch}'"
                )
            else:
                conflict_count = len(self.conflicts)
                self.message = (
                    f"Merge of '{self.source_branch}' into '{self.target_branch}' "
                    f"failed with {conflict_count} conflict(s)"
                )


@dataclass
class BranchInfo:
    """Information about a Git branch.

    Attributes:
        name: The branch name.
        is_current: Whether this is the currently checked-out branch.
        last_commit: Information about the latest commit on this branch.
    """

    name: str
    is_current: bool = False
    last_commit: CommitInfo | None = None
