"""Tests for the pytest fixtures in conftest.py.

These tests verify that the temporary Git repository fixtures
are correctly set up for use in other tests.
"""

from pathlib import Path

import git
import pytest


class TestTempDirFixture:
    """Tests for the temp_dir fixture."""

    def test_temp_dir_exists(self, temp_dir: Path) -> None:
        """Test that temp_dir creates an existing directory."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()

    def test_temp_dir_is_empty(self, temp_dir: Path) -> None:
        """Test that temp_dir is initially empty."""
        assert list(temp_dir.iterdir()) == []

    def test_temp_dir_can_create_files(self, temp_dir: Path) -> None:
        """Test that files can be created in temp_dir."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("hello")
        assert test_file.exists()
        assert test_file.read_text() == "hello"


class TestTempGitRepoFixture:
    """Tests for the temp_git_repo fixture."""

    def test_repo_is_initialized(self, temp_git_repo: git.Repo) -> None:
        """Test that the repository is properly initialized."""
        assert not temp_git_repo.bare
        assert temp_git_repo.working_dir is not None

    def test_repo_has_main_branch(self, temp_git_repo: git.Repo) -> None:
        """Test that the repository has a main branch."""
        branch_names = [b.name for b in temp_git_repo.heads]
        assert "main" in branch_names

    def test_repo_has_initial_commit(self, temp_git_repo: git.Repo) -> None:
        """Test that the repository has an initial commit."""
        commits = list(temp_git_repo.iter_commits())
        assert len(commits) >= 1
        assert commits[0].message.strip() == "Initial commit"

    def test_repo_has_readme(self, temp_git_repo: git.Repo) -> None:
        """Test that the repository has a README.md file."""
        repo_path = Path(temp_git_repo.working_dir)
        readme = repo_path / "README.md"
        assert readme.exists()

    def test_repo_has_user_config(self, temp_git_repo: git.Repo) -> None:
        """Test that the repository has user configuration for commits."""
        reader = temp_git_repo.config_reader()
        name = reader.get_value("user", "name")
        email = reader.get_value("user", "email")
        assert name == "Test User"
        assert email == "test@example.com"


class TestTempRepoWithConfigFixture:
    """Tests for the temp_repo_with_config fixture."""

    def test_has_config_file(self, temp_repo_with_config: git.Repo) -> None:
        """Test that the repository has a config file."""
        repo_path = Path(temp_repo_with_config.working_dir)
        config_file = repo_path / "app-config.json"
        assert config_file.exists()

    def test_config_file_is_committed(self, temp_repo_with_config: git.Repo) -> None:
        """Test that the config file is committed."""
        commits = list(temp_repo_with_config.iter_commits())
        assert len(commits) >= 2
        assert "configuration" in commits[0].message.lower()


class TestTempRepoWithBranchesFixture:
    """Tests for the temp_repo_with_branches fixture."""

    def test_has_main_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that main branch exists."""
        branch_names = [b.name for b in temp_repo_with_branches.heads]
        assert "main" in branch_names

    def test_has_feature_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that feature branch exists."""
        branch_names = [b.name for b in temp_repo_with_branches.heads]
        assert "feature/draft-config" in branch_names

    def test_is_on_main_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that we're on the main branch after fixture setup."""
        assert temp_repo_with_branches.active_branch.name == "main"

    def test_branches_have_different_content(
        self, temp_repo_with_branches: git.Repo
    ) -> None:
        """Test that main and feature branch have different config content."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        config_path = repo_path / "app-config.json"

        # Read main content
        main_content = config_path.read_text()

        # Switch to feature and read content
        temp_repo_with_branches.heads["feature/draft-config"].checkout()
        feature_content = config_path.read_text()

        # Switch back to main
        temp_repo_with_branches.heads.main.checkout()

        assert main_content != feature_content
        assert "1.0.0" in main_content
        assert "1.1.0" in feature_content


class TestTempRepoWithConflictFixture:
    """Tests for the temp_repo_with_conflict fixture."""

    def test_has_conflicting_branch(self, temp_repo_with_conflict: git.Repo) -> None:
        """Test that the conflicting branch exists."""
        branch_names = [b.name for b in temp_repo_with_conflict.heads]
        assert "feature/conflicting" in branch_names

    def test_is_on_main_branch(self, temp_repo_with_conflict: git.Repo) -> None:
        """Test that we're on main after fixture setup."""
        assert temp_repo_with_conflict.active_branch.name == "main"

    def test_merge_would_conflict(self, temp_repo_with_conflict: git.Repo) -> None:
        """Test that merging the feature branch would cause a conflict."""
        # Try to merge and expect a conflict
        try:
            temp_repo_with_conflict.git.merge("feature/conflicting")
            # If no exception, the merge succeeded unexpectedly
            pytest.fail("Expected merge conflict but merge succeeded")
        except git.GitCommandError as e:
            # Expected - merge conflict occurred
            assert "Merge conflict" in str(e) or "CONFLICT" in str(e)
            # Reset the repo state
            temp_repo_with_conflict.git.merge("--abort")
