"""Git repository wrapper using GitPython.

This module provides a concrete implementation of GitRepositoryInterface
using GitPython for all Git operations.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import git
from git.exc import GitCommandError, InvalidGitRepositoryError

from gitconfig.exceptions import (
    BranchExistsError,
    BranchNotFoundError,
    CommitError,
    ConfigNotFoundError,
    InvalidRepoError,
)
from gitconfig.interfaces.repository import GitRepositoryInterface
from gitconfig.models import BranchInfo, CommitInfo, MergeResult

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class GitRepository(GitRepositoryInterface):
    """Git repository wrapper using GitPython.

    This class provides a high-level interface for Git operations,
    wrapping GitPython's Repo class.

    Attributes:
        _repo: The underlying GitPython Repo object.
        _path: Path to the repository root.
    """

    def __init__(self) -> None:
        """Initialize an empty GitRepository instance.

        Use init_repo() to create a new repository or from_path()
        to load an existing one.
        """
        self._repo: git.Repo | None = None
        self._path: Path | None = None

    @classmethod
    def from_path(cls, path: Path) -> GitRepository:
        """Create a GitRepository instance from an existing repository.

        Args:
            path: Path to the repository root.

        Returns:
            A GitRepository instance wrapping the existing repo.

        Raises:
            InvalidRepoError: If the path is not a valid Git repository.
        """
        instance = cls()
        try:
            instance._repo = git.Repo(path)
            instance._path = path
        except InvalidGitRepositoryError as err:
            raise InvalidRepoError(path, reason="Not a valid Git repository") from err
        return instance

    @property
    def path(self) -> Path:
        """Return the path to the repository root."""
        if self._path is None:
            raise InvalidRepoError("", reason="Repository not initialized")
        return self._path

    @property
    def current_branch(self) -> str:
        """Return the name of the currently checked-out branch."""
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")
        return self._repo.active_branch.name

    def init_repo(self, path: Path, initial_branch: str = "main") -> None:
        """Initialize a new Git repository.

        Args:
            path: Directory path where the repo should be created.
            initial_branch: Name of the initial branch (default: 'main').

        Raises:
            InvalidRepoError: If the repository cannot be created.
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            self._repo = git.Repo.init(path, initial_branch=initial_branch)
            self._path = path

            # Configure user for commits
            self._repo.config_writer().set_value(
                "user", "name", "Git Config Manager"
            ).release()
            self._repo.config_writer().set_value(
                "user", "email", "gitconfig@local"
            ).release()

            # Create initial commit to establish the branch
            readme = path / "README.md"
            readme.write_text("# Configuration Repository\n")
            self._repo.index.add(["README.md"])
            self._repo.index.commit("Initial commit")

            logger.info(
                f"Initialized repository at {path} with branch '{initial_branch}'"
            )
        except Exception as e:
            raise InvalidRepoError(path, reason=str(e)) from e

    def add_file(self, file_path: Path, content: str) -> None:
        """Write content to a file and stage it for commit.

        Args:
            file_path: Path to the file relative to repo root.
            content: Content to write to the file.

        Raises:
            InvalidRepoError: If the repository is not valid.
        """
        if self._repo is None or self._path is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        full_path = self._path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        self._repo.index.add([str(file_path)])

        logger.debug(f"Added file: {file_path}")

    def commit(self, message: str) -> CommitInfo:
        """Create a commit with staged changes.

        Args:
            message: The commit message.

        Returns:
            Information about the created commit.

        Raises:
            CommitError: If the commit fails (e.g., no changes staged).
        """
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        # Check if there are staged changes
        if not self._repo.index.diff("HEAD") and not self._repo.untracked_files:
            # Also check if index has any entries waiting
            try:
                staged = list(self._repo.index.diff("HEAD"))
                if not staged:
                    raise CommitError("No changes staged for commit")
            except git.exc.BadName:
                # No HEAD yet (first commit)
                pass

        try:
            commit = self._repo.index.commit(message)
            logger.info(f"Created commit: {commit.hexsha[:8]} - {message}")
            return CommitInfo(
                sha=commit.hexsha,
                message=message,
                author=str(commit.author),
                timestamp=datetime.fromtimestamp(commit.committed_date, tz=UTC),
            )
        except Exception as e:
            raise CommitError(str(e)) from e

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
        if self._repo is None or self._path is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        if ref is None:
            # Read from working directory
            full_path = self._path / file_path
            if not full_path.exists():
                raise ConfigNotFoundError(str(file_path))
            return full_path.read_text()
        else:
            # Read from specific ref
            try:
                blob = self._repo.commit(ref).tree / str(file_path)
                return blob.data_stream.read().decode("utf-8")
            except KeyError as err:
                raise ConfigNotFoundError(str(file_path), branch=ref) from err
            except git.exc.BadName as err:
                raise ConfigNotFoundError(str(file_path), branch=ref) from err

    def file_exists(self, file_path: Path, ref: str | None = None) -> bool:
        """Check if a file exists in the repository.

        Args:
            file_path: Path to the file relative to repo root.
            ref: Optional Git ref to check in.

        Returns:
            True if the file exists, False otherwise.
        """
        try:
            self.read_file(file_path, ref)
            return True
        except ConfigNotFoundError:
            return False

    def create_branch(self, name: str, from_ref: str | None = None) -> None:
        """Create a new branch.

        Args:
            name: Name for the new branch.
            from_ref: Optional ref to create the branch from.
                     If None, creates from current HEAD.

        Raises:
            BranchExistsError: If the branch already exists.
        """
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        if self.branch_exists(name):
            raise BranchExistsError(name)

        if from_ref:
            self._repo.create_head(name, from_ref)
        else:
            self._repo.create_head(name)

        logger.info(f"Created branch: {name}")

    def switch_branch(self, name: str) -> None:
        """Switch to a different branch.

        Args:
            name: Name of the branch to switch to.

        Raises:
            BranchNotFoundError: If the branch does not exist.
        """
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        if not self.branch_exists(name):
            raise BranchNotFoundError(name)

        self._repo.heads[name].checkout()
        logger.info(f"Switched to branch: {name}")

    def delete_branch(self, name: str, force: bool = False) -> None:
        """Delete a branch.

        Args:
            name: Name of the branch to delete.
            force: If True, delete even if not fully merged.

        Raises:
            BranchNotFoundError: If the branch does not exist or is current.
        """
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        if not self.branch_exists(name):
            raise BranchNotFoundError(name)

        if self.current_branch == name:
            raise BranchNotFoundError(
                name, message=f"Cannot delete current branch '{name}'"
            )

        self._repo.delete_head(name, force=force)
        logger.info(f"Deleted branch: {name}")

    def list_branches(self) -> list[BranchInfo]:
        """List all branches in the repository.

        Returns:
            List of branch information objects.
        """
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        branches = []
        current = self.current_branch

        for head in self._repo.heads:
            commit = head.commit
            branches.append(
                BranchInfo(
                    name=head.name,
                    is_current=(head.name == current),
                    last_commit=CommitInfo(
                        sha=commit.hexsha,
                        message=str(commit.message).strip(),
                        author=str(commit.author),
                        timestamp=datetime.fromtimestamp(commit.committed_date, tz=UTC),
                    ),
                )
            )

        return branches

    def branch_exists(self, name: str) -> bool:
        """Check if a branch exists.

        Args:
            name: Name of the branch to check.

        Returns:
            True if the branch exists, False otherwise.
        """
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        return name in [h.name for h in self._repo.heads]

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
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        if not self.branch_exists(source):
            raise BranchNotFoundError(source)

        if target and not self.branch_exists(target):
            raise BranchNotFoundError(target)

        # Switch to target if specified
        original_branch = self.current_branch
        if target and target != original_branch:
            self.switch_branch(target)

        target_branch = target or original_branch

        try:
            # Perform merge
            self._repo.git.merge(source)
            merge_message = message or f"Merge branch '{source}' into {target_branch}"

            return MergeResult(
                success=True,
                source_branch=source,
                target_branch=target_branch,
                commit_sha=self._repo.head.commit.hexsha,
                message=merge_message,
            )
        except GitCommandError as e:
            # Check for conflicts
            if "CONFLICT" in str(e) or "Merge conflict" in str(e):
                conflicting_files = [
                    Path(str(item)) for item in self._repo.index.unmerged_blobs()
                ]
                return MergeResult(
                    success=False,
                    source_branch=source,
                    target_branch=target_branch,
                    conflicts=conflicting_files,
                )
            raise

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
        if self._repo is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        commits = []
        commit_iter = (
            self._repo.iter_commits(paths=str(file_path), max_count=max_count)
            if max_count
            else self._repo.iter_commits(paths=str(file_path))
        )

        for commit in commit_iter:
            commits.append(
                CommitInfo(
                    sha=commit.hexsha,
                    message=str(commit.message).strip(),
                    author=str(commit.author),
                    timestamp=datetime.fromtimestamp(commit.committed_date, tz=UTC),
                )
            )

        return commits

    def checkout_file(self, file_path: Path, ref: str) -> None:
        """Checkout a specific version of a file.

        Args:
            file_path: Path to the file relative to repo root.
            ref: Git ref (commit SHA, branch, tag) to checkout from.

        Raises:
            ConfigNotFoundError: If the file doesn't exist at that ref.
        """
        if self._repo is None or self._path is None:
            raise InvalidRepoError("", reason="Repository not initialized")

        try:
            self._repo.git.checkout(ref, "--", str(file_path))
        except GitCommandError as err:
            raise ConfigNotFoundError(str(file_path), branch=ref) from err
