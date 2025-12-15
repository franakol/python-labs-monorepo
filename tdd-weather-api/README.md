# TDD Weather API Service

> Part of the [Python Labs Monorepo](https://github.com/franakol/python-labs-monorepo)

A mock Weather API service built using strict Test-Driven Development (TDD) methodology. This project demonstrates the Red-Green-Refactor cycle, SOLID principles, and trunk-based Git workflow.

## 🎯 Lab Objectives

This lab focuses on:

- **TDD Workflow**: Red-Green-Refactor cycle demonstrated in commit history
- **Testing**: pytest with fixtures, parametrize, mocking, near 100% coverage
- **SOLID Principles**: Dependency injection, abstract interfaces
- **Code Quality**: Type hints, Black, Ruff, mypy in strict mode
- **Git Workflow**: Trunk-based development with short-lived feature branches

## ⚡ Quick Start

### Installation

```bash
# Navigate to the project
cd tdd-weather-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Basic Usage

```python
from weather_service.service import WeatherService

# Create service instance
service = WeatherService()

# Get weather forecast for a city
forecast = service.get_forecast("London")
print(f"Temperature in {forecast.city}: {forecast.temperature}°C")
```

## 📁 Project Structure

```
tdd-weather-api/
├── weather_service/
│   ├── __init__.py           # Package initialization
│   ├── exceptions.py         # Custom exception hierarchy
│   ├── models.py             # Request/response dataclasses
│   ├── service.py            # WeatherService class
│   └── providers/
│       ├── __init__.py
│       ├── base.py           # Abstract WeatherProvider interface
│       └── mock_provider.py  # Mock implementation
├── tests/
│   ├── conftest.py           # Shared test fixtures
│   ├── test_weather_service.py
│   ├── test_exceptions.py
│   └── test_providers.py
├── pyproject.toml            # Project configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
└── README.md
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=weather_service --cov-report=html

# Check coverage threshold (fails if under 95%)
pytest --cov=weather_service --cov-fail-under=95

# Run with verbose output
pytest -v
```

## 📋 Code Quality

```bash
# Format code with Black
black weather_service tests

# Lint with Ruff
ruff check weather_service tests

# Type check with mypy (strict mode)
mypy weather_service --strict
```

## 🔄 Git Workflow

This project follows **trunk-based development**:

| PR | Title | Description |
|----|-------|-------------|
| #1 | Project Setup | Initial structure, configs, pre-commit hooks |
| #2 | First TDD Cycle | Failing test → implementation → refactor |
| #3 | Error Handling | Exception handling, structured logging |
| #4 | SOLID Refactor | Dependency injection, abstract provider |
| #5 | Documentation | README, docstrings, coverage report |

## 📚 Other Labs in This Monorepo

- [Resilient Data Importer](../resilient-data-importer)
- [Employee Payroll Tracker](../employee-payroll-tracker)
- [Library Inventory App](../library-inventory-app)
- [Student Course Management](../student-course-management-lab)
- [Vehicle Rental System](../vehicle-rental-system)

## 📝 License

MIT License - See [LICENSE](../LICENSE) for details.
