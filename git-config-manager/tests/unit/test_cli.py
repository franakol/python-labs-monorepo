"""Tests for the CLI using Click's testing utilities."""

from pathlib import Path

from click.testing import CliRunner

from gitconfig.cli import cli


class TestCLIInit:
    """Tests for the init command."""

    def test_init_creates_repo(self, temp_dir: Path) -> None:
        """Test that init creates a new repository."""
        runner = CliRunner()
        repo_path = temp_dir / "new-repo"

        result = runner.invoke(cli, ["init", str(repo_path)])

        assert result.exit_code == 0
        assert "Initialized" in result.output
        assert (repo_path / ".git").exists()


class TestCLIConfigOperations:
    """Tests for save, get, list, delete commands."""

    def test_save_and_get_config(self, temp_dir: Path) -> None:
        """Test saving and retrieving a config."""
        runner = CliRunner()
        repo_path = temp_dir / "repo"

        # Init repo
        runner.invoke(cli, ["init", str(repo_path)])

        # Save config
        result = runner.invoke(
            cli,
            ["-r", str(repo_path), "save", "test-config", '{"key": "value"}'],
        )
        assert result.exit_code == 0
        assert "Saved" in result.output

        # Get config
        result = runner.invoke(cli, ["-r", str(repo_path), "get", "test-config"])
        assert result.exit_code == 0
        assert "key" in result.output

    def test_list_configs(self, temp_dir: Path) -> None:
        """Test listing configurations."""
        runner = CliRunner()
        repo_path = temp_dir / "repo"

        runner.invoke(cli, ["init", str(repo_path)])
        runner.invoke(
            cli,
            ["-r", str(repo_path), "save", "config-a", '{"a": 1}'],
        )
        runner.invoke(
            cli,
            ["-r", str(repo_path), "save", "config-b", '{"b": 2}'],
        )

        result = runner.invoke(cli, ["-r", str(repo_path), "list"])

        assert result.exit_code == 0
        assert "config-a" in result.output
        assert "config-b" in result.output

    def test_delete_config(self, temp_dir: Path) -> None:
        """Test deleting a configuration."""
        runner = CliRunner()
        repo_path = temp_dir / "repo"

        runner.invoke(cli, ["init", str(repo_path)])
        runner.invoke(
            cli,
            ["-r", str(repo_path), "save", "to-delete", '{"x": 1}'],
        )

        result = runner.invoke(cli, ["-r", str(repo_path), "delete", "to-delete"])

        assert result.exit_code == 0
        assert "Deleted" in result.output


class TestCLIBranching:
    """Tests for draft, switch, merge commands."""

    def test_draft_and_switch(self, temp_dir: Path) -> None:
        """Test creating and switching branches."""
        runner = CliRunner()
        repo_path = temp_dir / "repo"

        runner.invoke(cli, ["init", str(repo_path)])

        # Create draft
        result = runner.invoke(cli, ["-r", str(repo_path), "draft", "feature/test"])
        assert result.exit_code == 0
        assert "Created draft branch" in result.output

        # Switch back to main
        result = runner.invoke(cli, ["-r", str(repo_path), "switch", "main"])
        assert result.exit_code == 0
        assert "Switched to" in result.output

    def test_branches(self, temp_dir: Path) -> None:
        """Test listing branches."""
        runner = CliRunner()
        repo_path = temp_dir / "repo"

        runner.invoke(cli, ["init", str(repo_path)])
        runner.invoke(cli, ["-r", str(repo_path), "draft", "feature/new"])

        result = runner.invoke(cli, ["-r", str(repo_path), "branches"])

        assert result.exit_code == 0
        assert "main" in result.output
        assert "feature/new" in result.output


class TestCLIHistory:
    """Tests for history command."""

    def test_history(self, temp_dir: Path) -> None:
        """Test showing version history."""
        runner = CliRunner()
        repo_path = temp_dir / "repo"

        runner.invoke(cli, ["init", str(repo_path)])
        runner.invoke(
            cli,
            ["-r", str(repo_path), "save", "versioned", '{"v": 1}', "-m", "v1"],
        )
        runner.invoke(
            cli,
            ["-r", str(repo_path), "save", "versioned", '{"v": 2}', "-m", "v2"],
        )

        result = runner.invoke(cli, ["-r", str(repo_path), "history", "versioned"])

        assert result.exit_code == 0
        assert "v1" in result.output
        assert "v2" in result.output
