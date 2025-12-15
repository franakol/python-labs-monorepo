# Python Labs Monorepo

A collection of Python lab projects demonstrating object-oriented programming, design patterns, and testing practices.

## Labs Included

| Lab | Description |
|-----|-------------|
| [tdd-weather-api](./tdd-weather-api) | TDD-based mock Weather API with SOLID principles |
| [resilient-data-importer](./resilient-data-importer) | CLI tool for importing CSV data with robust exception handling |
| [employee-payroll-tracker](./employee-payroll-tracker) | Employee payroll management system |
| [library-inventory-app](./library-inventory-app) | Library inventory management application |
| [student-course-management-lab](./student-course-management-lab) | Student and course management system |
| [vehicle-rental-system](./vehicle-rental-system) | Vehicle rental management system |

## Getting Started

Each lab is a self-contained Python project. To run any lab:

```bash
cd <lab-name>
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running Tests

Each lab includes its own test suite:

```bash
cd <lab-name>
pytest
```

## Project Structure

```
labs-monorepo/
├── resilient-data-importer/
├── employee-payroll-tracker/
├── library-inventory-app/
├── student-course-management-lab/
├── vehicle-rental-system/
└── README.md
```

## Requirements

- Python 3.10+
- pytest (for running tests)

## License

MIT License
