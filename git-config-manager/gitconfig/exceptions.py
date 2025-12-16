"""Custom exceptions for the git-config-manager application.

This module defines a hierarchy of exceptions for handling various
error conditions in Git operations and configuration management.
"""

from dataclasses import dataclass, field
from pathlib import Path


class GitConfigError(Exception):
    """Base exception for all git-config-manager errors.

    All custom exceptions in this application inherit from this class,
    allowing callers to catch all application-specific errors.

    Attributes:
        message: Human-readable error description.
    """

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error description.
        """
        self.message = message
        super().__init__(message)


class ConfigNotFoundError(GitConfigError):
    """Raised when a requested configuration file does not exist.

    Attributes:
        config_name: Name of the configuration that was not found.
        branch: Optional branch where the config was searched.
    """

    def __init__(
        self, config_name: str, branch: str | None = None, message: str | None = None
    ) -> None:
        """Initialize the exception.

        Args:
            config_name: Name of the configuration that was not found.
            branch: Optional branch where the config was searched.
            message: Optional custom message.
        """
        self.config_name = config_name
        self.branch = branch
        if message is None:
            if branch:
                message = (
                    f"Configuration '{config_name}' not found on branch '{branch}'"
                )
            else:
                message = f"Configuration '{config_name}' not found"
        super().__init__(message)


class InvalidRepoError(GitConfigError):
    """Raised when the repository is invalid or not properly initialized.

    Attributes:
        path: Path to the invalid repository.
        reason: Explanation of why the repository is invalid.
    """

    def __init__(
        self, path: Path | str, reason: str | None = None, message: str | None = None
    ) -> None:
        """Initialize the exception.

        Args:
            path: Path to the invalid repository.
            reason: Explanation of why the repository is invalid.
            message: Optional custom message.
        """
        self.path = Path(path) if isinstance(path, str) else path
        self.reason = reason
        if message is None:
            message = f"Invalid repository at '{path}'"
            if reason:
                message = f"{message}: {reason}"
        super().__init__(message)


class BranchNotFoundError(GitConfigError):
    """Raised when a specified branch does not exist.

    Attributes:
        branch_name: Name of the branch that was not found.
    """

    def __init__(self, branch_name: str, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            branch_name: Name of the branch that was not found.
            message: Optional custom message.
        """
        self.branch_name = branch_name
        if message is None:
            message = f"Branch '{branch_name}' not found"
        super().__init__(message)


class BranchExistsError(GitConfigError):
    """Raised when attempting to create a branch that already exists.

    Attributes:
        branch_name: Name of the branch that already exists.
    """

    def __init__(self, branch_name: str, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            branch_name: Name of the branch that already exists.
            message: Optional custom message.
        """
        self.branch_name = branch_name
        if message is None:
            message = f"Branch '{branch_name}' already exists"
        super().__init__(message)


@dataclass
class ConflictFile:
    """Represents a file with merge conflicts.

    Attributes:
        path: Path to the conflicted file relative to repo root.
        ours: Content from our branch (current).
        theirs: Content from their branch (being merged).
        base: Common ancestor content (if available).
    """

    path: Path
    ours: str | None = None
    theirs: str | None = None
    base: str | None = None


@dataclass
class MergeConflictError(GitConfigError):
    """Raised when a merge operation results in conflicts.

    This exception provides detailed information about the conflicting
    files and guidance for resolution.

    Attributes:
        source_branch: The branch being merged from.
        target_branch: The branch being merged into.
        conflicting_files: List of files with conflicts.
    """

    source_branch: str
    target_branch: str
    conflicting_files: list[ConflictFile] = field(default_factory=list)
    message: str = ""

    def __post_init__(self) -> None:
        """Set default message if not provided."""
        if not self.message:
            file_list = ", ".join(str(f.path) for f in self.conflicting_files)
            self.message = (
                f"Merge conflict when merging '{self.source_branch}' into "
                f"'{self.target_branch}'. Conflicting files: {file_list}"
            )
        super().__init__(self.message)

    def get_resolution_guide(self) -> str:
        """Generate a human-readable guide for resolving conflicts.

        Returns:
            A string with step-by-step instructions for conflict resolution.
        """
        lines = [
            "=== Merge Conflict Resolution Guide ===",
            f"Source branch: {self.source_branch}",
            f"Target branch: {self.target_branch}",
            "",
            "Conflicting files:",
        ]
        for conf_file in self.conflicting_files:
            lines.append(f"  - {conf_file.path}")

        lines.extend(
            [
                "",
                "To resolve:",
                "1. Open each conflicting file and look for conflict markers:",
                "   <<<<<<< HEAD",
                "   (your changes)",
                "   =======",
                "   (their changes)",
                "   >>>>>>> branch-name",
                "",
                "2. Edit the file to keep the desired content",
                "3. Remove the conflict markers",
                "4. Stage the resolved files: git add <file>",
                "5. Complete the merge: git commit",
            ]
        )
        return "\n".join(lines)


class CommitError(GitConfigError):
    """Raised when a commit operation fails.

    Attributes:
        reason: Explanation of why the commit failed.
    """

    def __init__(self, reason: str, message: str | None = None) -> None:
        """Initialize the exception.

        Args:
            reason: Explanation of why the commit failed.
            message: Optional custom message.
        """
        self.reason = reason
        if message is None:
            message = f"Commit failed: {reason}"
        super().__init__(message)


class ParseError(GitConfigError):
    """Raised when configuration file parsing fails.

    Attributes:
        file_path: Path to the file that failed to parse.
        format_type: The expected format (e.g., 'json', 'yaml').
        parse_error: The underlying parsing error message.
    """

    def __init__(
        self,
        file_path: Path | str,
        format_type: str,
        parse_error: str,
        message: str | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            file_path: Path to the file that failed to parse.
            format_type: The expected format (e.g., 'json', 'yaml').
            parse_error: The underlying parsing error message.
            message: Optional custom message.
        """
        self.file_path = Path(file_path) if isinstance(file_path, str) else file_path
        self.format_type = format_type
        self.parse_error = parse_error
        if message is None:
            message = f"Failed to parse '{file_path}' as {format_type}: {parse_error}"
        super().__init__(message)
