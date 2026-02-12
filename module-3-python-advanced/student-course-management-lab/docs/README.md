# Student Course Management System

## Overview

This repository contains a comprehensive Student Course Management System built with Python. The system provides functionality to manage:

- **Students**: Add, view, update, and delete student records
- **Courses**: Manage course offerings with details like credits and instructors
- **Enrollments**: Track student course enrollments and grades
- **Reports**: Generate transcripts, course rosters, and statistics

## Purpose

The system demonstrates:
- Object-oriented programming principles in Python
- Data structure implementation and management
- File I/O and data persistence
- Clean architecture with separation of concerns
- Test-driven development practices

## Key Features

### Student Management
- Create and maintain student profiles
- Store student information (ID, name, email, program)
- Search and filter students
- Update student details
- Remove student records

### Course Management
- Define course offerings
- Track course details (code, name, credits, instructor)
- Manage course catalog
- Update course information
- Remove courses from catalog

### Enrollment System
- Enroll students in courses
- Drop courses for students
- Record and update grades
- Calculate student GPA
- Generate student transcripts
- View course rosters

### Data Persistence
- Save data to JSON/CSV files
- Load data from files
- Maintain data integrity
- Handle file errors gracefully

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Poetry (Python dependency manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/franakol/student-course-management-lab.git
   cd student-course-management-lab
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Activate virtual environment**
   ```bash
   poetry shell
   ```

### Running the Application

```bash
poetry run student-management
```

Or within the Poetry shell:
```bash
python -m student_management.main
```

## Project Structure

```
student-course-management-lab/
├── docs/                     # Documentation
├── student_management/       # Main application package
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   ├── data/                # File I/O handlers
│   ├── ui/                  # User interface
│   └── utils/               # Utility functions
├── data/                    # Data files
├── tests/                   # Test suite
└── pyproject.toml          # Project configuration
```

## Documentation

Detailed documentation is available in the `docs/` directory:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design
- **[DATA_STRUCTURES.md](docs/DATA_STRUCTURES.md)** - Data structures and models
- **[FILE_FORMAT.md](docs/FILE_FORMAT.md)** - Data file format specifications
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - API documentation
- **[TESTING.md](docs/TESTING.md)** - Testing guide and procedures

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

```bash
# Format code
poetry run black student_management

# Lint code
poetry run flake8 student_management

# Type checking
poetry run mypy student_management
```

## Contributing

1. Create a feature branch from `development`
2. Make your changes with clear, focused commits
3. Write or update tests as needed
4. Ensure all tests pass and code quality checks succeed
5. Submit a Pull Request to the `development` branch

## License

This project is created for educational purposes.

## Contact

For questions or feedback, please open an issue on GitHub.
