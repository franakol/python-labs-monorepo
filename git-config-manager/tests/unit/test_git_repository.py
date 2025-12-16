"""Unit tests for the GitRepository class.

Tests follow TDD - these tests are written first and should fail
until the GitRepository implementation is complete.
"""

from pathlib import Path

import git
import pytest

from gitconfig.core.git_repository import GitRepository
from gitconfig.exceptions import (
    BranchExistsError,
    BranchNotFoundError,
    CommitError,
    ConfigNotFoundError,
    InvalidRepoError,
)
from gitconfig.models import CommitInfo


class TestGitRepositoryInit:
    """Tests for GitRepository initialization and repo creation."""

    def test_init_repo_creates_directory(self, temp_dir: Path) -> None:
        """Test that init_repo creates a Git repository."""
        repo_path = temp_dir / "new-repo"
        repo = GitRepository()
        repo.init_repo(repo_path)

        assert repo_path.exists()
        assert (repo_path / ".git").exists()

    def test_init_repo_sets_path_property(self, temp_dir: Path) -> None:
        """Test that path property returns the repo path after init."""
        repo_path = temp_dir / "new-repo"
        repo = GitRepository()
        repo.init_repo(repo_path)

        assert repo.path == repo_path

    def test_init_repo_creates_main_branch(self, temp_dir: Path) -> None:
        """Test that init_repo creates a main branch by default."""
        repo_path = temp_dir / "new-repo"
        repo = GitRepository()
        repo.init_repo(repo_path)

        assert repo.current_branch == "main"

    def test_init_repo_with_custom_branch(self, temp_dir: Path) -> None:
        """Test that init_repo can use a custom initial branch name."""
        repo_path = temp_dir / "new-repo"
        repo = GitRepository()
        repo.init_repo(repo_path, initial_branch="develop")

        assert repo.current_branch == "develop"

    def test_from_existing_repo(self, temp_git_repo: git.Repo) -> None:
        """Test loading an existing repository."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        assert repo.path == repo_path

    def test_from_invalid_path_raises_error(self, temp_dir: Path) -> None:
        """Test that loading a non-repo path raises InvalidRepoError."""
        with pytest.raises(InvalidRepoError):
            GitRepository.from_path(temp_dir)


class TestGitRepositoryFileOperations:
    """Tests for file operations (add, read, write)."""

    def test_add_file_creates_file(self, temp_git_repo: git.Repo) -> None:
        """Test that add_file creates and stages a new file."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.add_file(Path("test.txt"), "Hello, World!")

        assert (repo_path / "test.txt").exists()
        assert (repo_path / "test.txt").read_text() == "Hello, World!"

    def test_add_file_stages_file(self, temp_git_repo: git.Repo) -> None:
        """Test that add_file stages the file for commit."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.add_file(Path("staged.txt"), "content")

        # File should exist in the working directory
        assert (repo_path / "staged.txt").exists()

    def test_add_file_in_subdirectory(self, temp_git_repo: git.Repo) -> None:
        """Test that add_file creates parent directories."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.add_file(Path("configs/app/settings.json"), '{"key": "value"}')

        assert (repo_path / "configs/app/settings.json").exists()

    def test_read_file_returns_content(self, temp_repo_with_config: git.Repo) -> None:
        """Test that read_file returns file content."""
        repo_path = Path(temp_repo_with_config.working_dir)
        repo = GitRepository.from_path(repo_path)

        content = repo.read_file(Path("app-config.json"))

        assert "app_name" in content
        assert "test-app" in content

    def test_read_file_from_ref(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that read_file can read from a specific ref."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        repo = GitRepository.from_path(repo_path)

        # Read from feature branch
        content = repo.read_file(Path("app-config.json"), ref="feature/draft-config")

        assert "1.1.0" in content
        assert "new_feature" in content

    def test_read_nonexistent_file_raises_error(self, temp_git_repo: git.Repo) -> None:
        """Test that reading a nonexistent file raises ConfigNotFoundError."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        with pytest.raises(ConfigNotFoundError):
            repo.read_file(Path("nonexistent.json"))

    def test_file_exists_returns_true(self, temp_repo_with_config: git.Repo) -> None:
        """Test that file_exists returns True for existing files."""
        repo_path = Path(temp_repo_with_config.working_dir)
        repo = GitRepository.from_path(repo_path)

        assert repo.file_exists(Path("app-config.json"))

    def test_file_exists_returns_false(self, temp_git_repo: git.Repo) -> None:
        """Test that file_exists returns False for nonexistent files."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        assert not repo.file_exists(Path("nonexistent.json"))


class TestGitRepositoryCommit:
    """Tests for commit operations."""

    def test_commit_creates_commit(self, temp_git_repo: git.Repo) -> None:
        """Test that commit creates a new commit."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.add_file(Path("new-file.txt"), "content")
        commit_info = repo.commit("Add new file")

        assert isinstance(commit_info, CommitInfo)
        assert commit_info.message == "Add new file"

    def test_commit_returns_sha(self, temp_git_repo: git.Repo) -> None:
        """Test that commit returns a valid SHA."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.add_file(Path("file.txt"), "content")
        commit_info = repo.commit("Test commit")

        assert len(commit_info.sha) == 40
        assert all(c in "0123456789abcdef" for c in commit_info.sha)

    def test_commit_with_no_changes_raises_error(self, temp_git_repo: git.Repo) -> None:
        """Test that committing without changes raises CommitError."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        with pytest.raises(CommitError):
            repo.commit("Empty commit")


class TestGitRepositoryBranches:
    """Tests for branch operations."""

    def test_create_branch(self, temp_git_repo: git.Repo) -> None:
        """Test that create_branch creates a new branch."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.create_branch("feature/new-feature")

        assert repo.branch_exists("feature/new-feature")

    def test_create_existing_branch_raises_error(self, temp_git_repo: git.Repo) -> None:
        """Test that creating an existing branch raises BranchExistsError."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        with pytest.raises(BranchExistsError):
            repo.create_branch("main")

    def test_switch_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that switch_branch changes the current branch."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.switch_branch("feature/draft-config")

        assert repo.current_branch == "feature/draft-config"

    def test_switch_nonexistent_branch_raises_error(
        self, temp_git_repo: git.Repo
    ) -> None:
        """Test that switching to nonexistent branch raises BranchNotFoundError."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        with pytest.raises(BranchNotFoundError):
            repo.switch_branch("nonexistent")

    def test_delete_branch(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that delete_branch removes a branch."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        repo = GitRepository.from_path(repo_path)

        repo.delete_branch("feature/draft-config", force=True)

        assert not repo.branch_exists("feature/draft-config")

    def test_delete_current_branch_raises_error(self, temp_git_repo: git.Repo) -> None:
        """Test that deleting the current branch raises an error."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        with pytest.raises(BranchNotFoundError):
            repo.delete_branch("main")

    def test_list_branches(self, temp_repo_with_branches: git.Repo) -> None:
        """Test that list_branches returns all branches."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        repo = GitRepository.from_path(repo_path)

        branches = repo.list_branches()

        branch_names = [b.name for b in branches]
        assert "main" in branch_names
        assert "feature/draft-config" in branch_names

    def test_list_branches_marks_current(
        self, temp_repo_with_branches: git.Repo
    ) -> None:
        """Test that list_branches marks the current branch."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        repo = GitRepository.from_path(repo_path)

        branches = repo.list_branches()

        current_branches = [b for b in branches if b.is_current]
        assert len(current_branches) == 1
        assert current_branches[0].name == "main"

    def test_branch_exists_returns_true(
        self, temp_repo_with_branches: git.Repo
    ) -> None:
        """Test that branch_exists returns True for existing branches."""
        repo_path = Path(temp_repo_with_branches.working_dir)
        repo = GitRepository.from_path(repo_path)

        assert repo.branch_exists("main")
        assert repo.branch_exists("feature/draft-config")

    def test_branch_exists_returns_false(self, temp_git_repo: git.Repo) -> None:
        """Test that branch_exists returns False for nonexistent branches."""
        repo_path = Path(temp_git_repo.working_dir)
        repo = GitRepository.from_path(repo_path)

        assert not repo.branch_exists("nonexistent")


class TestGitRepositoryHistory:
    """Tests for commit history operations."""

    def test_get_file_history(self, temp_repo_with_config: git.Repo) -> None:
        """Test that get_file_history returns commit history."""
        repo_path = Path(temp_repo_with_config.working_dir)
        repo = GitRepository.from_path(repo_path)

        history = repo.get_file_history(Path("app-config.json"))

        assert len(history) >= 1
        assert all(isinstance(c, CommitInfo) for c in history)

    def test_get_file_history_with_limit(self, temp_repo_with_config: git.Repo) -> None:
        """Test that get_file_history respects max_count."""
        repo_path = Path(temp_repo_with_config.working_dir)
        repo = GitRepository.from_path(repo_path)

        # Add more commits
        repo.add_file(Path("app-config.json"), '{"version": "2"}')
        repo.commit("Update config v2")
        repo.add_file(Path("app-config.json"), '{"version": "3"}')
        repo.commit("Update config v3")

        history = repo.get_file_history(Path("app-config.json"), max_count=2)

        assert len(history) == 2
