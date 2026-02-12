# API Reference

## Overview

This document provides a comprehensive reference for all modules, classes, and functions in the Student Course Management System.

## Module Structure

```
student_management/
├── models/              # Data models
├── services/            # Business logic
├── data/                # Data persistence
├── ui/                  # User interface
└── utils/               # Utilities
```

---

## Models Module

### `student_management.models.student`

#### Class: `Student`

Represents a student entity.

**Constructor**:
```python
def __init__(self, student_id: str, name: str, email: str, program: str)
```

**Parameters**:
- `student_id` (str): Unique student identifier
- `name` (str): Student's full name
- `email` (str): Student's email address
- `program` (str): Academic program name

**Methods**:

##### `validate() -> List[str]`
Validates student data.

**Returns**: List of validation error messages (empty if valid)

**Example**:
```python
student = Student("S001", "John Doe", "john@example.com", "CS")
errors = student.validate()
if errors:
    print(f"Validation failed: {errors}")
```

##### `to_dict() -> Dict[str, Any]`
Converts student to dictionary.

**Returns**: Dictionary representation

**Example**:
```python
student_dict = student.to_dict()
# {'student_id': 'S001', 'name': 'John Doe', ...}
```

##### `from_dict(data: Dict[str, Any]) -> Student` (classmethod)
Creates student from dictionary.

**Parameters**:
- `data` (dict): Student data dictionary

**Returns**: Student instance

**Example**:
```python
data = {'student_id': 'S001', 'name': 'John Doe', ...}
student = Student.from_dict(data)
```

---

### `student_management.models.course`

#### Class: `Course`

Represents a course entity.

**Constructor**:
```python
def __init__(self, course_code: str, name: str, credits: int, instructor: str)
```

**Parameters**:
- `course_code` (str): Unique course code (format: XXX1234)
- `name` (str): Course name
- `credits` (int): Credit hours (1-6)
- `instructor` (str): Instructor name

**Methods**:

##### `validate() -> List[str]`
Validates course data.

##### `to_dict() -> Dict[str, Any]`
Converts course to dictionary.

##### `from_dict(data: Dict[str, Any]) -> Course` (classmethod)
Creates course from dictionary.

---

### `student_management.models.enrollment`

#### Class: `Enrollment`

Represents a student's enrollment in a course.

**Constructor**:
```python
def __init__(
    self,
    student_id: str,
    course_code: str,
    grade: Optional[float] = None,
    enrollment_date: Optional[datetime] = None
)
```

**Parameters**:
- `student_id` (str): Reference to student
- `course_code` (str): Reference to course
- `grade` (Optional[float]): Numeric grade (0-100)
- `enrollment_date` (Optional[datetime]): Enrollment date (defaults to now)

**Methods**:

##### `validate() -> List[str]`
Validates enrollment data.

##### `calculate_letter_grade() -> str`
Converts numeric grade to letter grade.

**Returns**: Letter grade (A+, A, B+, etc.) or "N/A" if no grade

**Example**:
```python
enrollment = Enrollment("S001", "CSC1234", grade=85.5)
letter = enrollment.calculate_letter_grade()  # "A"
```

##### `to_dict() -> Dict[str, Any]`
Converts enrollment to dictionary.

##### `from_dict(data: Dict[str, Any]) -> Enrollment` (classmethod)
Creates enrollment from dictionary.

---

## Services Module

### `student_management.services.student_service`

#### Class: `StudentService`

Manages student-related operations.

**Constructor**:
```python
def __init__(self, file_handler: FileHandler)
```

**Methods**:

##### `create_student(student_id: str, name: str, email: str, program: str) -> Student`
Creates and adds a new student.

**Parameters**: Student attributes

**Returns**: Created student

**Raises**:
- `ValueError`: If validation fails or student ID exists

**Example**:
```python
service = StudentService(file_handler)
student = service.create_student("S001", "John Doe", "john@example.com", "CS")
```

##### `get_student(student_id: str) -> Optional[Student]`
Retrieves a student by ID.

**Parameters**:
- `student_id` (str): Student ID to find

**Returns**: Student if found, None otherwise

##### `list_students() -> List[Student]`
Lists all students.

**Returns**: List of all students

##### `update_student(student_id: str, **kwargs) -> Student`
Updates student information.

**Parameters**:
- `student_id` (str): Student ID to update
- `**kwargs`: Fields to update (name, email, program)

**Returns**: Updated student

**Raises**:
- `ValueError`: If student not found or validation fails

**Example**:
```python
updated = service.update_student("S001", email="newemail@example.com")
```

##### `delete_student(student_id: str) -> bool`
Deletes a student.

**Parameters**:
- `student_id` (str): Student ID to delete

**Returns**: True if deleted, False if not found

**Example**:
```python
success = service.delete_student("S001")
```

##### `search_students(name: str = None, program: str = None) -> List[Student]`
Searches students by criteria.

**Parameters**:
- `name` (Optional[str]): Name to search for (partial match)
- `program` (Optional[str]): Program to filter by

**Returns**: List of matching students

---

### `student_management.services.course_service`

#### Class: `CourseService`

Manages course-related operations.

**Methods**: Similar structure to `StudentService`

- `create_course(course_code, name, credits, instructor) -> Course`
- `get_course(course_code) -> Optional[Course]`
- `list_courses() -> List[Course]`
- `update_course(course_code, **kwargs) -> Course`
- `delete_course(course_code) -> bool`
- `search_courses(name=None, instructor=None) -> List[Course]`

---

### `student_management.services.enrollment_service`

#### Class: `EnrollmentService`

Manages enrollment and grade operations.

**Constructor**:
```python
def __init__(
    self,
    file_handler: FileHandler,
    student_service: StudentService,
    course_service: CourseService
)
```

**Methods**:

##### `enroll_student(student_id: str, course_code: str) -> Enrollment`
Enrolls a student in a course.

**Parameters**:
- `student_id` (str): Student to enroll
- `course_code` (str): Course to enroll in

**Returns**: Created enrollment

**Raises**:
- `ValueError`: If student or course not found, or already enrolled

**Example**:
```python
enrollment = service.enroll_student("S001", "CSC1234")
```

##### `drop_course(student_id: str, course_code: str) -> bool`
Drops a course for a student.

**Returns**: True if dropped, False if not enrolled

##### `update_grade(student_id: str, course_code: str, grade: float) -> Enrollment`
Updates grade for an enrollment.

**Parameters**:
- `student_id` (str): Student ID
- `course_code` (str): Course code
- `grade` (float): New grade (0-100)

**Returns**: Updated enrollment

**Raises**:
- `ValueError`: If enrollment not found or invalid grade

##### `get_student_enrollments(student_id: str) -> List[Enrollment]`
Gets all enrollments for a student.

**Returns**: List of enrollments

##### `get_course_enrollments(course_code: str) -> List[Enrollment]`
Gets all enrollments for a course.

**Returns**: List of enrollments

##### `calculate_gpa(student_id: str) -> float`
Calculates GPA for a student.

**Returns**: GPA (0.0-4.0 scale)

**Example**:
```python
gpa = service.calculate_gpa("S001")
print(f"GPA: {gpa:.2f}")
```

##### `get_transcript(student_id: str) -> Dict[str, Any]`
Generates a transcript for a student.

**Returns**: Dictionary with student info, courses, grades, and GPA

**Example**:
```python
transcript = service.get_transcript("S001")
print(f"Student: {transcript['student']['name']}")
print(f"GPA: {transcript['gpa']}")
```

---

## Data Module

### `student_management.data.file_handler`

#### Class: `FileHandler`

Manages file I/O operations.

**Constructor**:
```python
def __init__(self, data_dir: Path = Path("data"))
```

**Methods**:

##### `load_students() -> List[Student]`
Loads students from file.

**Returns**: List of students

**Raises**:
- `FileFormatError`: If file format is invalid

##### `save_students(students: List[Student]) -> None`
Saves students to file.

**Parameters**:
- `students` (List[Student]): Students to save

##### `load_courses() -> List[Course]`
Loads courses from file.

##### `save_courses(courses: List[Course]) -> None`
Saves courses to file.

##### `load_enrollments() -> List[Enrollment]`
Loads enrollments from file.

##### `save_enrollments(enrollments: List[Enrollment]) -> None`
Saves enrollments to file.

##### `create_backup(file_type: str) -> Path`
Creates a backup of a data file.

**Parameters**:
- `file_type` (str): One of "students", "courses", "enrollments"

**Returns**: Path to backup file

---

## UI Module

### `student_management.ui.menu`

#### Class: `Menu`

CLI menu interface.

**Constructor**:
```python
def __init__(
    self,
    student_service: StudentService,
    course_service: CourseService,
    enrollment_service: EnrollmentService
)
```

**Methods**:

##### `run() -> None`
Starts the main menu loop.

##### `display_main_menu() -> None`
Displays the main menu options.

##### `handle_student_menu() -> None`
Handles student management submenu.

##### `handle_course_menu() -> None`
Handles course management submenu.

##### `handle_enrollment_menu() -> None`
Handles enrollment management submenu.

---

## Utilities Module

### `student_management.utils.helpers`

#### Functions:

##### `is_valid_email(email: str) -> bool`
Validates email format.

**Parameters**:
- `email` (str): Email to validate

**Returns**: True if valid, False otherwise

##### `format_grade(grade: Optional[float]) -> str`
Formats grade for display.

**Parameters**:
- `grade` (Optional[float]): Grade to format

**Returns**: Formatted string (e.g., "85.50" or "N/A")

##### `get_user_input(prompt: str, validator: Callable = None) -> str`
Gets validated user input.

**Parameters**:
- `prompt` (str): Prompt to display
- `validator` (Optional[Callable]): Validation function

**Returns**: Validated input

---

## Error Handling

### Custom Exceptions

```python
class StudentManagementError(Exception):
    """Base exception for the application."""
    pass

class ValidationError(StudentManagementError):
    """Data validation error."""
    pass

class NotFoundError(StudentManagementError):
    """Resource not found."""
    pass

class DuplicateError(StudentManagementError):
    """Duplicate resource."""
    pass

class FileFormatError(StudentManagementError):
    """File format error."""
    pass
```

---

## Type Hints

The codebase uses Python type hints throughout:

```python
from typing import List, Dict, Optional, Any

def example_function(
    required_param: str,
    optional_param: Optional[int] = None
) -> List[str]:
    """Example with type hints."""
    pass
```

---

## Usage Examples

### Complete Example

```python
from pathlib import Path
from student_management.data.file_handler import FileHandler
from student_management.services.student_service import StudentService
from student_management.services.course_service import CourseService
from student_management.services.enrollment_service import EnrollmentService

# Initialize
file_handler = FileHandler(Path("data"))
student_service = StudentService(file_handler)
course_service = CourseService(file_handler)
enrollment_service = EnrollmentService(
    file_handler, student_service, course_service
)

# Create student
student = student_service.create_student(
    "S001", "John Doe", "john@example.com", "CS"
)

# Create course
course = course_service.create_course(
    "CSC1234", "Intro to Programming", 3, "Dr. Smith"
)

# Enroll student
enrollment = enrollment_service.enroll_student("S001", "CSC1234")

# Update grade
enrollment_service.update_grade("S001", "CSC1234", 85.5)

# Calculate GPA
gpa = enrollment_service.calculate_gpa("S001")
print(f"GPA: {gpa:.2f}")

# Get transcript
transcript = enrollment_service.get_transcript("S001")
```
