"""Pytest configuration and fixtures for git-config-manager tests.

This module provides fixtures for creating temporary Git repositories
for testing Git operations in isolation.
"""

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import git
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that is cleaned up after the test.

    Yields:
        Path to the temporary directory.
    """
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_git_repo(temp_dir: Path) -> Generator[git.Repo, None, None]:
    """Create a temporary Git repository for testing.

    The repository is initialized with a 'main' branch and an initial
    commit containing a README file.

    Args:
        temp_dir: Temporary directory fixture.

    Yields:
        GitPython Repo object for the temporary repository.
    """
    # Initialize the repository
    repo = git.Repo.init(temp_dir, initial_branch="main")

    # Configure user for commits
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@example.com").release()

    # Create initial commit
    readme_path = temp_dir / "README.md"
    readme_path.write_text("# Test Repository\n")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")

    yield repo

    # Cleanup is handled by temp_dir fixture


@pytest.fixture
def temp_repo_with_config(temp_git_repo: git.Repo) -> Generator[git.Repo, None, None]:
    """Create a temp repository with an initial config file.

    The repository includes a sample JSON configuration file.

    Args:
        temp_git_repo: Base temporary Git repository fixture.

    Yields:
        GitPython Repo object with config file committed.
    """
    repo_path = Path(temp_git_repo.working_dir)

    # Create a sample config file
    config_path = repo_path / "app-config.json"
    config_content = """{
    "app_name": "test-app",
    "version": "1.0.0",
    "debug": false,
    "database": {
        "host": "localhost",
        "port": 5432
    }
}
"""
    config_path.write_text(config_content)
    temp_git_repo.index.add(["app-config.json"])
    temp_git_repo.index.commit("Add initial configuration")

    yield temp_git_repo


@pytest.fixture
def temp_repo_with_branches(
    temp_repo_with_config: git.Repo,
) -> Generator[git.Repo, None, None]:
    """Create a temp repository with main and a feature branch.

    The repository has:
    - main branch with initial config
    - feature/draft-config branch with modified config

    Args:
        temp_repo_with_config: Repository with config file.

    Yields:
        GitPython Repo object with multiple branches.
    """
    repo = temp_repo_with_config
    repo_path = Path(repo.working_dir)

    # Create feature branch
    feature_branch = repo.create_head("feature/draft-config")
    feature_branch.checkout()

    # Modify config on feature branch
    config_path = repo_path / "app-config.json"
    modified_config = """{
    "app_name": "test-app",
    "version": "1.1.0",
    "debug": true,
    "database": {
        "host": "localhost",
        "port": 5432
    },
    "new_feature": "enabled"
}
"""
    config_path.write_text(modified_config)
    repo.index.add(["app-config.json"])
    repo.index.commit("Update config for new feature")

    # Switch back to main
    repo.heads.main.checkout()

    yield repo


@pytest.fixture
def temp_repo_with_conflict(
    temp_repo_with_config: git.Repo,
) -> Generator[git.Repo, None, None]:
    """Create a temp repository with conflicting changes on two branches.

    This fixture sets up a merge conflict scenario:
    - main branch modifies app-config.json one way
    - feature/conflicting branch modifies the same file differently

    Args:
        temp_repo_with_config: Repository with config file.

    Yields:
        GitPython Repo object ready for conflict testing.
    """
    repo = temp_repo_with_config
    repo_path = Path(repo.working_dir)
    config_path = repo_path / "app-config.json"

    # Create feature branch from current main
    feature_branch = repo.create_head("feature/conflicting")

    # Modify config on main
    main_config = """{
    "app_name": "test-app",
    "version": "2.0.0",
    "debug": false,
    "database": {
        "host": "production-db.example.com",
        "port": 5432
    }
}
"""
    config_path.write_text(main_config)
    repo.index.add(["app-config.json"])
    repo.index.commit("Update config for production")

    # Switch to feature branch and make conflicting change
    feature_branch.checkout()

    # Reset to the commit before main's change
    repo.head.reset(repo.heads.main.commit.parents[0], index=True, working_tree=True)

    feature_config = """{
    "app_name": "test-app-v2",
    "version": "2.0.0-beta",
    "debug": true,
    "database": {
        "host": "staging-db.example.com",
        "port": 5433
    }
}
"""
    config_path.write_text(feature_config)
    repo.index.add(["app-config.json"])
    repo.index.commit("Update config for staging")

    # Switch back to main
    repo.heads.main.checkout()

    yield repo
