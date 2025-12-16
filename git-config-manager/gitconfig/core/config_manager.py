"""ConfigManager - High-level configuration management service.

This module provides the main orchestration layer that combines
GitRepository and ConfigParser to manage versioned configurations.
"""

from __future__ import annotations

import logging
from pathlib import Path

from gitconfig.core.git_repository import GitRepository
from gitconfig.core.parsers import JsonParser, YamlParser
from gitconfig.exceptions import ConfigNotFoundError
from gitconfig.interfaces.parser import ConfigParserInterface
from gitconfig.models import (
    BranchInfo,
    CommitInfo,
    ConfigEntry,
    ConfigFormat,
    MergeResult,
)

logger = logging.getLogger(__name__)


class ConfigManager:
    """High-level configuration management service.

    Provides a simple API for managing versioned configurations
    using Git as the backend storage.

    Attributes:
        _repo: The underlying Git repository.
        _parsers: Mapping of format to parser implementation.
    """

    def __init__(self, repo: GitRepository) -> None:
        """Initialize ConfigManager with a Git repository.

        Args:
            repo: GitRepository instance to use for storage.
        """
        self._repo = repo
        self._parsers: dict[ConfigFormat, ConfigParserInterface] = {
            ConfigFormat.JSON: JsonParser(),
            ConfigFormat.YAML: YamlParser(),
        }

    @classmethod
    def from_path(cls, path: Path) -> ConfigManager:
        """Create a ConfigManager from an existing repository.

        Args:
            path: Path to the Git repository.

        Returns:
            ConfigManager instance wrapping the repository.
        """
        repo = GitRepository.from_path(path)
        return cls(repo)

    @classmethod
    def create(cls, path: Path, initial_branch: str = "main") -> ConfigManager:
        """Create a new configuration repository.

        Args:
            path: Path where the repository should be created.
            initial_branch: Name of the initial branch.

        Returns:
            ConfigManager instance for the new repository.
        """
        repo = GitRepository()
        repo.init_repo(path, initial_branch=initial_branch)
        return cls(repo)

    @property
    def current_branch(self) -> str:
        """Return the current branch name."""
        return self._repo.current_branch

    def save(
        self,
        config: ConfigEntry,
        message: str | None = None,
    ) -> CommitInfo:
        """Save a configuration to the repository.

        Args:
            config: Configuration entry to save.
            message: Optional commit message.

        Returns:
            Information about the created commit.
        """
        parser = self._parsers[config.format]
        content = parser.serialize(config.content)

        # Determine file path
        file_path = config.path or Path(f"{config.name}.{parser.file_extension}")

        # Write and commit
        self._repo.add_file(file_path, content)
        commit_message = message or f"Update configuration: {config.name}"
        commit = self._repo.commit(commit_message)

        logger.info(f"Saved config '{config.name}' in commit {commit.sha[:8]}")
        return commit

    def get(
        self,
        name: str,
        branch: str | None = None,
        format: ConfigFormat = ConfigFormat.JSON,
    ) -> ConfigEntry:
        """Retrieve a configuration by name.

        Args:
            name: Name of the configuration.
            branch: Optional branch to read from.
            format: Expected format of the configuration.

        Returns:
            The configuration entry.

        Raises:
            ConfigNotFoundError: If the configuration doesn't exist.
        """
        # Try JSON first, then YAML if not found
        for fmt, p in self._parsers.items():
            try_path = Path(f"{name}.{p.file_extension}")
            if self._repo.file_exists(try_path, ref=branch):
                content = self._repo.read_file(try_path, ref=branch)
                parsed = p.parse(content)
                return ConfigEntry(
                    name=name,
                    content=parsed,
                    format=fmt,
                    path=try_path,
                )

        raise ConfigNotFoundError(name, branch=branch)

    def list_configs(self) -> list[ConfigEntry]:
        """List all configurations in the repository.

        Returns:
            List of configuration entries.
        """
        configs = []
        repo_path = self._repo.path

        # Find all JSON and YAML files
        for fmt, parser in self._parsers.items():
            pattern = f"*.{parser.file_extension}"
            for file_path in repo_path.glob(pattern):
                if file_path.is_file():
                    name = file_path.stem
                    try:
                        config = self.get(name, format=fmt)
                        configs.append(config)
                    except ConfigNotFoundError:
                        pass

        return configs

    def delete(self, name: str, message: str | None = None) -> CommitInfo:
        """Delete a configuration.

        Args:
            name: Name of the configuration to delete.
            message: Optional commit message.

        Returns:
            Information about the commit.

        Raises:
            ConfigNotFoundError: If the configuration doesn't exist.
        """
        # Find the file
        for parser in self._parsers.values():
            file_path = Path(f"{name}.{parser.file_extension}")
            full_path = self._repo.path / file_path
            if full_path.exists():
                full_path.unlink()
                self._repo._repo.index.remove([str(file_path)])  # type: ignore[union-attr]
                commit_message = message or f"Delete configuration: {name}"
                return self._repo.commit(commit_message)

        raise ConfigNotFoundError(name)

    def create_draft(self, branch_name: str) -> None:
        """Create a new draft branch for config changes.

        Args:
            branch_name: Name for the new branch.
        """
        self._repo.create_branch(branch_name)
        self._repo.switch_branch(branch_name)
        logger.info(f"Created draft branch: {branch_name}")

    def switch_to(self, branch_name: str) -> None:
        """Switch to a different branch.

        Args:
            branch_name: Name of the branch to switch to.
        """
        self._repo.switch_branch(branch_name)

    def merge_draft(
        self,
        source: str,
        target: str = "main",
        message: str | None = None,
    ) -> MergeResult:
        """Merge a draft branch into target.

        Args:
            source: Name of the source branch to merge.
            target: Name of the target branch.
            message: Optional merge commit message.

        Returns:
            Result of the merge operation.
        """
        # Switch to target if not already there
        if self.current_branch != target:
            self.switch_to(target)

        result = self._repo.merge_branch(source, message=message)
        logger.info(f"Merged '{source}' into '{target}': {result.message}")
        return result

    def get_history(
        self,
        name: str,
        max_count: int | None = None,
    ) -> list[CommitInfo]:
        """Get version history for a configuration.

        Args:
            name: Name of the configuration.
            max_count: Maximum number of versions to return.

        Returns:
            List of commits that modified the configuration.
        """
        # Find the file path
        for parser in self._parsers.values():
            file_path = Path(f"{name}.{parser.file_extension}")
            if self._repo.file_exists(file_path):
                return self._repo.get_file_history(file_path, max_count=max_count)

        raise ConfigNotFoundError(name)

    def list_branches(self) -> list[BranchInfo]:
        """List all branches in the repository.

        Returns:
            List of branch information.
        """
        return self._repo.list_branches()
