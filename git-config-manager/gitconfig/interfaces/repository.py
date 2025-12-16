"""Abstract interface for Git repository operations.

This module defines the contract for Git repository interactions,
allowing for different implementations (e.g., GitPython, subprocess).
"""

from abc import ABC, abstractmethod
from pathlib import Path

from gitconfig.models import BranchInfo, CommitInfo, MergeResult


class GitRepositoryInterface(ABC):
    """Abstract interface for Git repository operations.

    This interface defines all Git operations needed by the
    git-config-manager application. Implementations should
    wrap a specific Git library (e.g., GitPython).
    """

    @property
    @abstractmethod
    def path(self) -> Path:
        """Return the path to the repository root."""
        ...

    @property
    @abstractmethod
    def current_branch(self) -> str:
        """Return the name of the currently checked-out branch."""
        ...

    @abstractmethod
    def init_repo(self, path: Path, initial_branch: str = "main") -> None:
        """Initialize a new Git repository.

        Args:
            path: Directory path where the repo should be created.
            initial_branch: Name of the initial branch (default: 'main').

        Raises:
            InvalidRepoError: If the repository cannot be created.
        """
        ...

    @abstractmethod
    def add_file(self, file_path: Path, content: str) -> None:
        """Write content to a file and stage it for commit.

        Args:
            file_path: Path to the file relative to repo root.
            content: Content to write to the file.

        Raises:
            InvalidRepoError: If the repository is not valid.
        """
        ...

    @abstractmethod
    def commit(self, message: str) -> CommitInfo:
        """Create a commit with staged changes.

        Args:
            message: The commit message.

        Returns:
            Information about the created commit.

        Raises:
            CommitError: If the commit fails.
        """
        ...

    @abstractmethod
    def read_file(self, file_path: Path, ref: str | None = None) -> str:
        """Read a file's content from the repository.

        Args:
            file_path: Path to the file relative to repo root.
            ref: Optional Git ref (branch, tag, commit) to read from.
                 If None, reads from the working directory.

        Returns:
            The file content as a string.

        Raises:
            ConfigNotFoundError: If the file does not exist.
        """
        ...

    @abstractmethod
    def file_exists(self, file_path: Path, ref: str | None = None) -> bool:
        """Check if a file exists in the repository.

        Args:
            file_path: Path to the file relative to repo root.
            ref: Optional Git ref to check in.

        Returns:
            True if the file exists, False otherwise.
        """
        ...

    @abstractmethod
    def create_branch(self, name: str, from_ref: str | None = None) -> None:
        """Create a new branch.

        Args:
            name: Name for the new branch.
            from_ref: Optional ref to create the branch from.
                     If None, creates from current HEAD.

        Raises:
            BranchExistsError: If the branch already exists.
        """
        ...

    @abstractmethod
    def switch_branch(self, name: str) -> None:
        """Switch to a different branch.

        Args:
            name: Name of the branch to switch to.

        Raises:
            BranchNotFoundError: If the branch does not exist.
        """
        ...

    @abstractmethod
    def delete_branch(self, name: str, force: bool = False) -> None:
        """Delete a branch.

        Args:
            name: Name of the branch to delete.
            force: If True, delete even if not fully merged.

        Raises:
            BranchNotFoundError: If the branch does not exist.
        """
        ...

    @abstractmethod
    def list_branches(self) -> list[BranchInfo]:
        """List all branches in the repository.

        Returns:
            List of branch information objects.
        """
        ...

    @abstractmethod
    def branch_exists(self, name: str) -> bool:
        """Check if a branch exists.

        Args:
            name: Name of the branch to check.

        Returns:
            True if the branch exists, False otherwise.
        """
        ...

    @abstractmethod
    def merge_branch(
        self, source: str, target: str | None = None, message: str | None = None
    ) -> MergeResult:
        """Merge a branch into another.

        Args:
            source: Name of the branch to merge from.
            target: Name of the branch to merge into.
                   If None, merges into the current branch.
            message: Optional custom merge commit message.

        Returns:
            Result of the merge operation.

        Raises:
            BranchNotFoundError: If source or target branch doesn't exist.
            MergeConflictError: If the merge has conflicts.
        """
        ...

    @abstractmethod
    def get_file_history(
        self, file_path: Path, max_count: int | None = None
    ) -> list[CommitInfo]:
        """Get the commit history for a specific file.

        Args:
            file_path: Path to the file relative to repo root.
            max_count: Maximum number of commits to return.

        Returns:
            List of commits that modified the file, newest first.
        """
        ...

    @abstractmethod
    def checkout_file(self, file_path: Path, ref: str) -> None:
        """Checkout a specific version of a file.

        Args:
            file_path: Path to the file relative to repo root.
            ref: Git ref (commit SHA, branch, tag) to checkout from.

        Raises:
            ConfigNotFoundError: If the file doesn't exist at that ref.
        """
        ...
