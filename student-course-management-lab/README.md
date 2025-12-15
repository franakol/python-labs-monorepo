# Student Course Management System

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-181%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive Python-based system for managing student information, course offerings, enrollments, and academic records. This project demonstrates modern Python development practices including Test-Driven Development (TDD), layered architecture, and robust data persistence.

## 🎯 Features

- **Student Management**: 
  - Create, update, delete, and search student records
  - Validation for email and ID formats
  - Duplicate prevention
- **Course Management**: 
  - Manage course catalog with details and instructors
  - Credit validation (1-6 range)
  - Search by code, name, or instructor
- **Enrollment System**: 
  - Track student course enrollments
  - Prevent duplicate enrollments
  - Validate student and course existence
- **Grading & Reporting**: 
  - Record and update numerical grades (0-100)
  - Automatic Letter Grade calculation (A+, A, B+, etc.)
  - Automatic GPA computation
  - Course average calculation
- **Data Persistence**: 
  - JSON-based storage for all entities
  - Automatic backup functionality
  - Data integrity checks
- **CLI Interface**: 
  - User-friendly interactive menu system
  - Robust input handling and validation

## 📋 Requirements

- Python 3.11 or higher
- Poetry (for dependency management)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/franakol/student-course-management-lab.git
cd student-course-management-lab

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Alternative Installation (Standard Pip)

If you encounter issues with Poetry (like `dyld: Library not loaded`), you can use standard Python tools:

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install pytest pytest-cov black flake8 mypy

# 4. Run the application
python -m student_management.main
```

### Running the Application

```bash
# Run from Poetry (Recommended)
poetry run student-management

# Or using Python module syntax (Standard Pip)
python -m student_management.main
```

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[README.md](docs/README.md)** - Detailed project overview
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design
- **[DATA_STRUCTURES.md](docs/DATA_STRUCTURES.md)** - Data models and structures
- **[FILE_FORMAT.md](docs/FILE_FORMAT.md)** - Data file format specifications
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API documentation
- **[TESTING.md](docs/TESTING.md)** - Testing guide and procedures

## 🏗️ Project Structure

```
student-course-management-lab/
├── docs/                          # Documentation
├── student_management/            # Main application package
│   ├── models/                   # Data models (Student, Course, Enrollment)
│   ├── services/                 # Business logic layer
│   ├── data/                     # File I/O handlers
│   ├── ui/                       # User interface (CLI menu)
│   └── utils/                    # Utility functions
├── data/                         # Data files (JSON)
├── tests/                        # Test suite
├── pyproject.toml               # Poetry configuration
└── README.md                    # This file
```

## 🧪 Testing

```bash
# Option 1: Using Poetry
poetry run pytest

# Option 2: Using Standard Pip (if you used Alternative Installation)
pytest
```

### Running Specific Tests

```bash
# Run with coverage report
pytest --cov=student_management --cov-report=term-missing

# Run a specific test file
pytest tests/test_student_service.py
```
# Run with coverage report
poetry run pytest --cov=student_management --cov-report=html

# View coverage report
open htmlcov/index.html

## 🛠️ Development

### Code Quality Tools

```bash
# Format code with Black
poetry run black student_management

# Lint code with Flake8
poetry run flake8 student_management

# Type checking with Mypy
poetry run mypy student_management

# Run all quality checks
poetry run black student_management && poetry run flake8 student_management && poetry run mypy student_management
```

### Development Workflow

1. Create a feature branch from `development`
2. Make changes with clear, focused commits
3. Write or update tests
4. Ensure all tests pass and code quality checks succeed
5. Submit a Pull Request to `development`

## 📊 System Architecture

The system follows a layered architecture:

```
┌─────────────────────────────────┐
│     Presentation Layer (UI)     │
├─────────────────────────────────┤
│   Business Logic (Services)     │
├─────────────────────────────────┤
│      Domain Layer (Models)      │
├─────────────────────────────────┤
│   Data Access Layer (Files)     │
└─────────────────────────────────┘
```

## 💡 Usage Examples

### Student Management

```python
from student_management.services.student_service import StudentService

# Create a student
student = student_service.create_student(
    student_id="S001",
    name="John Doe",
    email="john.doe@example.com",
    program="Computer Science"
)

# Search for students
students = student_service.search_students(program="Computer Science")

# Update student information
updated = student_service.update_student("S001", email="newemail@example.com")
```

### Course Management

```python
from student_management.services.course_service import CourseService

# Create a course
course = course_service.create_course(
    course_code="CSC1234",
    name="Introduction to Programming",
    credits=3,
    instructor="Dr. Smith"
)
```

### Enrollment and Grades

```python
from student_management.services.enrollment_service import EnrollmentService

# Enroll a student in a course
enrollment = enrollment_service.enroll_student("S001", "CSC1234")

# Update grade
enrollment_service.update_grade("S001", "CSC1234", 85.5)

# Calculate GPA
gpa = enrollment_service.calculate_gpa("S001")

# Get transcript
transcript = enrollment_service.get_transcript("S001")
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is created for educational purposes.

## 🔗 Links

- **Repository**: [https://github.com/franakol/student-course-management-lab](https://github.com/franakol/student-course-management-lab)
- **Issues**: [https://github.com/franakol/student-course-management-lab/issues](https://github.com/franakol/student-course-management-lab/issues)

## � Troubleshooting

### Common Issues

#### `dyld: Library not loaded` (macOS)
**Error:** `dyld[xxxxx]: Library not loaded: .../Python.framework/Versions/3.13/Python`
**Cause:** This happens when the Python version Poetry was installed with has been updated or removed (often by Homebrew), breaking the `poetry` executable.

**Fix:**
1. **Reinstall Poetry**: The best long-term fix is to reinstall Poetry so it links to your current Python version.
2. **Use Standard Pip**: Follow the [Alternative Installation](#alternative-installation-standard-pip) instructions above to bypass Poetry entirely. This is often the quickest solution for labs.

#### `command not found: poetry`
**Fix:** Ensure Poetry is in your PATH, or use the Standard Pip method described above.

## �📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Python and Poetry**
