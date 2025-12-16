# Git-Powered Configuration Management CLI

A Python CLI tool that uses Git as a backend for managing versioned configurations. Store, track, and manage application configurations with full Git history, branching, and merging capabilities.

## 🎯 Learning Objectives

- **Git as a Data Store**: Use Git for structured data versioning
- **GitPython Library**: Work with Git programmatically
- **Test-Driven Development**: Build features test-first
- **SOLID Principles**: Apply clean architecture patterns
- **Click CLI Framework**: Build user-friendly command-line tools

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Initialize a config repository
gitconfig init ./my-configs

# Save a configuration
gitconfig -r ./my-configs save app-settings '{"database": {"host": "localhost", "port": 5432}}'

# Retrieve the configuration
gitconfig -r ./my-configs get app-settings
```

## 📖 CLI Commands

### Repository Management

```bash
# Initialize a new config repository
gitconfig init <path> [--branch main]

# List all configurations
gitconfig -r <path> list

# List all branches
gitconfig -r <path> branches
```

### Configuration Operations

```bash
# Save a configuration (JSON format)
gitconfig -r <path> save <name> '<json_content>' [-m "commit message"]

# Save a YAML configuration
gitconfig -r <path> save <name> '<yaml_content>' --format yaml

# Get a configuration
gitconfig -r <path> get <name> [--branch feature/new]

# Delete a configuration
gitconfig -r <path> delete <name> [-m "commit message"]
```

### Branching & Merging

```bash
# Create a draft branch for changes
gitconfig -r <path> draft feature/new-settings

# Switch between branches
gitconfig -r <path> switch main

# Merge a draft into main
gitconfig -r <path> merge feature/new-settings --target main
```

### Version History

```bash
# View configuration history
gitconfig -r <path> history app-settings --limit 10
```

## 🏗️ Architecture

```
gitconfig/
├── cli.py                 # Click CLI entry point
├── core/
│   ├── config_manager.py  # High-level orchestration
│   ├── git_repository.py  # Git operations wrapper
│   └── parsers.py         # JSON/YAML parsers
├── exceptions.py          # Custom exception hierarchy
├── interfaces/
│   ├── parser.py          # ConfigParserInterface
│   └── repository.py      # GitRepositoryInterface
└── models.py              # Data models
```

### Key Design Patterns

- **Repository Pattern**: `GitRepository` abstracts Git operations
- **Strategy Pattern**: `ConfigParser` interface for JSON/YAML
- **Dependency Injection**: `ConfigManager` receives dependencies
- **Factory Methods**: `from_path()` and `create()` for initialization

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gitconfig --cov-report=html

# Run specific test file
pytest tests/unit/test_git_repository.py -v
```

### Test Structure

- **17 fixture tests**: Verify temporary Git repository setup
- **29 repository tests**: Git operations (branches, commits, merges)
- **20 parser tests**: JSON/YAML parsing and serialization
- **13 manager tests**: High-level configuration operations
- **7 CLI tests**: Command-line interface integration

## 📚 Usage Examples

### Managing Application Configurations

```python
from pathlib import Path
from gitconfig.core.config_manager import ConfigManager
from gitconfig.models import ConfigEntry, ConfigFormat

# Create a new config repository
manager = ConfigManager.create(Path("./configs"))

# Save database configuration
db_config = ConfigEntry(
    name="database",
    content={
        "host": "localhost",
        "port": 5432,
        "name": "myapp",
        "pool_size": 10
    },
    format=ConfigFormat.JSON
)
manager.save(db_config, message="Add database config")

# Create a staging branch
manager.create_draft("staging")

# Update config for staging
staging_config = ConfigEntry(
    name="database",
    content={
        "host": "staging-db.example.com",
        "port": 5432,
        "name": "myapp_staging",
        "pool_size": 5
    }
)
manager.save(staging_config, message="Configure for staging")

# Get production config from main
prod_config = manager.get("database", branch="main")
print(f"Production DB: {prod_config.content['host']}")

# View version history
history = manager.get_history("database", max_count=5)
for commit in history:
    print(f"{commit.sha[:8]} - {commit.message}")
```

### Handling Merge Conflicts

```python
# Create feature branch and make changes
manager.create_draft("feature/cache-settings")
manager.save(
    ConfigEntry(name="cache", content={"ttl": 3600}),
    message="Add cache config"
)

# Switch back and merge
manager.switch_to("main")
result = manager.merge_draft("feature/cache-settings")

if result.success:
    print(f"Merged successfully: {result.commit_sha}")
else:
    print(f"Conflicts in: {result.conflicts}")
    # Handle conflicts manually
```

## 🔧 Configuration Formats

### JSON (default)

```json
{
  "app": {
    "name": "MyApplication",
    "version": "1.0.0",
    "debug": false
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(message)s"
  }
}
```

### YAML

```yaml
app:
  name: MyApplication
  version: "1.0.0"
  debug: false

logging:
  level: INFO
  format: "%(asctime)s - %(message)s"
```

## 📋 Requirements

- Python 3.10+
- Git (installed and accessible in PATH)
- GitPython
- Click
- PyYAML

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Write tests first (TDD)
4. Implement the feature
5. Run tests and linting: `pytest && pre-commit run --all-files`
6. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.
