"""Unit tests for the ConfigManager service.

Tests follow TDD approach for the high-level configuration manager.
"""

from pathlib import Path

import git
import pytest

from gitconfig.core.config_manager import ConfigManager
from gitconfig.exceptions import ConfigNotFoundError
from gitconfig.models import ConfigEntry, ConfigFormat


class TestConfigManagerInit:
    """Tests for ConfigManager initialization."""

    def test_create_from_path(self, temp_git_repo: git.Repo) -> None:
        """Test creating ConfigManager from existing repo."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        assert manager is not None

    def test_create_new_repo(self, temp_dir: Path) -> None:
        """Test creating a new config repository."""
        repo_path = temp_dir / "new-config-repo"
        manager = ConfigManager.create(repo_path)

        assert manager is not None
        assert (repo_path / ".git").exists()


class TestConfigManagerOperations:
    """Tests for ConfigManager configuration operations."""

    def test_save_config_json(self, temp_git_repo: git.Repo) -> None:
        """Test saving a JSON configuration."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        config = ConfigEntry(
            name="app-settings",
            content={"database": {"host": "localhost"}},
            format=ConfigFormat.JSON,
        )

        manager.save(config, message="Add app settings")

        assert (repo_path / "app-settings.json").exists()

    def test_save_config_yaml(self, temp_git_repo: git.Repo) -> None:
        """Test saving a YAML configuration."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        config = ConfigEntry(
            name="app-settings",
            content={"database": {"host": "localhost"}},
            format=ConfigFormat.YAML,
        )

        manager.save(config, message="Add app settings")

        assert (repo_path / "app-settings.yaml").exists()

    def test_get_config(self, temp_git_repo: git.Repo) -> None:
        """Test retrieving a saved configuration."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        # Save config
        original = ConfigEntry(
            name="test-config",
            content={"key": "value", "number": 42},
            format=ConfigFormat.JSON,
        )
        manager.save(original, message="Add test config")

        # Retrieve config
        retrieved = manager.get("test-config")

        assert retrieved.name == "test-config"
        assert retrieved.content["key"] == "value"
        assert retrieved.content["number"] == 42

    def test_get_config_not_found(self, temp_git_repo: git.Repo) -> None:
        """Test that getting nonexistent config raises error."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        with pytest.raises(ConfigNotFoundError):
            manager.get("nonexistent")

    def test_list_configs(self, temp_git_repo: git.Repo) -> None:
        """Test listing all configurations."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        # Save multiple configs
        manager.save(
            ConfigEntry(name="config-a", content={"a": 1}),
            message="Add config A",
        )
        manager.save(
            ConfigEntry(name="config-b", content={"b": 2}),
            message="Add config B",
        )

        configs = manager.list_configs()

        assert len(configs) >= 2
        names = [c.name for c in configs]
        assert "config-a" in names
        assert "config-b" in names

    def test_delete_config(self, temp_git_repo: git.Repo) -> None:
        """Test deleting a configuration."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        # Save and then delete
        manager.save(
            ConfigEntry(name="to-delete", content={"x": 1}),
            message="Add config",
        )
        manager.delete("to-delete", message="Remove config")

        with pytest.raises(ConfigNotFoundError):
            manager.get("to-delete")


class TestConfigManagerBranching:
    """Tests for ConfigManager branch operations."""

    def test_create_draft(self, temp_git_repo: git.Repo) -> None:
        """Test creating a draft branch for config changes."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        manager.create_draft("feature/new-settings")

        assert manager.current_branch == "feature/new-settings"

    def test_switch_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test switching between branches."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        manager = ConfigManager.from_path(repo_path)

        manager.switch_to("feature/draft-config")

        assert manager.current_branch == "feature/draft-config"

    def test_merge_draft(self, temp_git_repo: git.Repo) -> None:
        """Test merging a draft branch back to main."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        # Create draft and make changes
        manager.create_draft("feature/new-config")
        manager.save(
            ConfigEntry(name="new-feature", content={"enabled": True}),
            message="Add new feature config",
        )

        # Merge back to main
        result = manager.merge_draft("feature/new-config", target="main")

        assert result.success
        assert manager.current_branch == "main"

    def test_get_config_from_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test getting config from a specific branch."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        manager = ConfigManager.from_path(repo_path)

        config = manager.get("app-config", branch="feature/draft-config")

        assert "1.1.0" in str(config.content)


class TestConfigManagerHistory:
    """Tests for ConfigManager history operations."""

    def test_get_history(self, temp_git_repo: git.Repo) -> None:
        """Test getting version history for a config."""
        repo_path = Path(temp_git_repo.working_dir)
        manager = ConfigManager.from_path(repo_path)

        # Create multiple versions
        manager.save(
            ConfigEntry(name="versioned", content={"version": 1}),
            message="v1",
        )
        manager.save(
            ConfigEntry(name="versioned", content={"version": 2}),
            message="v2",
        )

        history = manager.get_history("versioned")

        assert len(history) >= 2
