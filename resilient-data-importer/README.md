# Resilient Data Importer CLI

> Part of the [Python Labs Monorepo](https://github.com/franakol/python-labs-monorepo)

A resilient command-line tool for importing user data from CSV files into a JSON database. This project demonstrates robust exception handling, code quality best practices, Git Flow workflow, and comprehensive testing.

## 🎯 Lab Objectives

This lab focuses on:

- **Exception Handling**: Custom exception hierarchy, context managers, try/except/else/finally
- **Code Quality**: PEP 8 compliance, type hints, SOLID principles
- **Git Workflow**: Git Flow with feature branches and pull requests
- **Testing**: pytest with fixtures, parametrize, mocking, and high coverage

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/franakol/python-labs-monorepo.git
cd python-labs-monorepo/resilient-data-importer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Basic Usage

```bash
# Import users from CSV to JSON
python -m data_importer.cli --input data/sample_users.csv --output output/users.json

# Validate without importing (dry-run)
python -m data_importer.cli -i data/sample_users.csv -o output/users.json --dry-run

# Verbose mode for debugging
python -m data_importer.cli -i data/sample_users.csv -o output/users.json --verbose

# Strict mode (fail on any error)
python -m data_importer.cli -i data/sample_users.csv -o output/users.json --strict
```

## 📁 Project Structure

```
resilient-data-importer/
├── data_importer/
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # CLI entry point
│   ├── exceptions.py         # Custom exception hierarchy
│   ├── models/
│   │   └── user.py           # User dataclass
│   ├── parsers/
│   │   └── csv_parser.py     # CSV file parser with context manager
│   ├── validators/
│   │   └── user_validator.py # Data validation logic
│   ├── repositories/
│   │   └── json_repository.py # JSON storage layer
│   └── services/
│       └── import_service.py # Business logic orchestration
├── tests/
│   ├── conftest.py           # Shared test fixtures
│   ├── test_csv_parser.py
│   ├── test_user_validator.py
│   ├── test_json_repository.py
│   ├── test_import_service.py
│   └── test_cli.py
├── data/
│   └── sample_users.csv      # Sample input data
├── docs/
│   ├── architecture.md       # Architecture documentation
│   └── exceptions.md         # Exception handling guide
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
└── .pre-commit-config.yaml   # Pre-commit hooks
```

## 🏗️ Architecture

The project follows **SOLID principles** with a layered architecture:

```
┌─────────────────┐
│      CLI        │  Entry point (argparse)
└────────┬────────┘
         │
┌────────▼────────┐
│  ImportService  │  Business logic orchestration
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    │         │            │
┌───▼───┐ ┌───▼───┐ ┌──────▼──────┐
│Parser │ │Valid- │ │ Repository  │
│       │ │ator  │ │             │
└───────┘ └───────┘ └─────────────┘
```

- **CLI Layer**: Handles command-line arguments and user interaction
- **Service Layer**: Coordinates the import workflow
- **Parser**: Reads and parses CSV files
- **Validator**: Validates user data
- **Repository**: Persists data to JSON files

## 🛡️ Exception Handling

Custom exception hierarchy for precise error handling:

```python
ImporterError (Base)
├── FileFormatError   # Malformed CSV files
├── ValidationError   # Invalid data (email, user_id, etc.)
├── DuplicateUserError # Duplicate user entries
└── StorageError      # File I/O errors
```

Example usage:

```python
from data_importer.exceptions import ImporterError, ValidationError

try:
    service.run_import()
except ValidationError as e:
    print(f"Invalid data in field '{e.field}': {e.value}")
except ImporterError as e:
    print(f"Import failed: {e.message}")
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=data_importer --cov-report=html

# Run specific test file
pytest tests/test_csv_parser.py

# Run with verbose output
pytest -v
```

### Test Coverage

The test suite includes:

- **Unit tests** for each component
- **Integration tests** for the full import workflow
- **Parametrized tests** using `@pytest.mark.parametrize`
- **Fixture-based setup** using `conftest.py`
- **Error condition testing** for all exception types

## 📋 Code Quality

### Linting and Formatting

```bash
# Format code with Black
black data_importer tests

# Lint with Ruff
ruff check data_importer tests

# Type check with mypy
mypy data_importer
```

### Pre-commit Hooks

Pre-commit hooks automatically run on each commit:

- **Black**: Code formatting
- **Ruff**: Linting and import sorting
- **mypy**: Static type checking

## 🔄 Git Workflow

This project follows **Git Flow**:

1. **main**: Production-ready code
2. **development**: Integration branch
3. **feature/***: Feature branches

### Pull Request History

| PR | Title | Description |
|----|-------|-------------|
| #1 | Project Setup | Initial structure, exceptions, User model |
| #2 | CSV Parser | Context manager, header validation |
| #3 | Data Validation | Email, user_id, name validation |
| #4 | Storage Layer | JSON repository, import service |
| #5 | CLI | Argparse, logging, user output |
| #6 | Testing | Comprehensive test suite |
| #7 | Documentation | README, docs, final review |

## 📚 Other Labs in This Monorepo

- [Employee Payroll Tracker](../employee-payroll-tracker)
- [Library Inventory App](../library-inventory-app)
- [Student Course Management](../student-course-management-lab)
- [Vehicle Rental System](../vehicle-rental-system)

## 📝 License

MIT License - See [LICENSE](../LICENSE) for details.
