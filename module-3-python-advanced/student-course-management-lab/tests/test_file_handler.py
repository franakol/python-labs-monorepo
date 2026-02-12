"""
Tests for the FileHandler class.

This module contains comprehensive tests for file I/O operations,
including reading, writing, backup, and error handling.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
from student_management.data.file_handler import FileHandler
from student_management.models.student import Student
from student_management.models.course import Course
from student_management.models.enrollment import Enrollment


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory for tests."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def file_handler(temp_data_dir):
    """Create a FileHandler instance with temporary directory."""
    return FileHandler(temp_data_dir)


@pytest.fixture
def sample_students():
    """Create sample students for testing."""
    return [
        Student("S001", "John Doe", "john@example.com", "Computer Science"),
        Student("S002", "Jane Smith", "jane@example.com", "Software Engineering"),
    ]


@pytest.fixture
def sample_courses():
    """Create sample courses for testing."""
    return [
        Course("CSC1234", "Intro to Programming", 3, "Dr. Smith"),
        Course("MAT5678", "Calculus I", 4, "Prof. Johnson"),
    ]


@pytest.fixture
def sample_enrollments():
    """Create sample enrollments for testing."""
    return [
        Enrollment("S001", "CSC1234", grade=85.5),
        Enrollment("S002", "MAT5678", grade=92.0),
    ]


class TestFileHandlerInitialization:
    """Tests for FileHandler initialization."""

    def test_init_with_existing_directory(self, temp_data_dir):
        """Test initialization with existing directory."""
        handler = FileHandler(temp_data_dir)
        assert handler.data_dir == temp_data_dir
        assert handler.data_dir.exists()

    def test_init_creates_directory_if_not_exists(self, tmp_path):
        """Test that initialization creates data directory if it doesn't exist."""
        data_dir = tmp_path / "new_data"
        handler = FileHandler(data_dir)
        assert data_dir.exists()
        assert data_dir.is_dir()

    def test_init_with_default_directory(self):
        """Test initialization with default directory."""
        handler = FileHandler()
        assert handler.data_dir == Path("data")


class TestLoadStudents:
    """Tests for loading students from file."""

    def test_load_students_from_existing_file(
        self, file_handler, temp_data_dir, sample_students
    ):
        """Test loading students from an existing file."""
        # Create file with sample data
        students_file = temp_data_dir / "students.json"
        data = {
            "students": [s.to_dict() for s in sample_students],
            "metadata": {"version": "1.0", "count": len(sample_students)},
        }
        students_file.write_text(json.dumps(data, indent=2))

        # Load students
        loaded = file_handler.load_students()

        assert len(loaded) == 2
        assert loaded[0].student_id == "S001"
        assert loaded[0].name == "John Doe"
        assert loaded[1].student_id == "S002"

    def test_load_students_empty_list_when_file_not_exists(self, file_handler):
        """Test that loading returns empty list when file doesn't exist."""
        loaded = file_handler.load_students()
        assert loaded == []

    def test_load_students_handles_corrupted_file(self, file_handler, temp_data_dir):
        """Test that loading handles corrupted JSON gracefully."""
        students_file = temp_data_dir / "students.json"
        students_file.write_text("{ invalid json")

        with pytest.raises(Exception):  # Should raise appropriate error
            file_handler.load_students()


class TestSaveStudents:
    """Tests for saving students to file."""

    def test_save_students_creates_file(
        self, file_handler, temp_data_dir, sample_students
    ):
        """Test that saving students creates a file."""
        file_handler.save_students(sample_students)

        students_file = temp_data_dir / "students.json"
        assert students_file.exists()

    def test_save_students_correct_format(
        self, file_handler, temp_data_dir, sample_students
    ):
        """Test that saved file has correct format."""
        file_handler.save_students(sample_students)

        students_file = temp_data_dir / "students.json"
        data = json.loads(students_file.read_text())

        assert "students" in data
        assert "metadata" in data
        assert data["metadata"]["version"] == "1.0"
        assert data["metadata"]["count"] == 2
        assert "last_updated" in data["metadata"]

    def test_save_students_preserves_data(
        self, file_handler, temp_data_dir, sample_students
    ):
        """Test that saved data can be loaded back correctly."""
        file_handler.save_students(sample_students)
        loaded = file_handler.load_students()

        assert len(loaded) == len(sample_students)
        assert loaded[0].student_id == sample_students[0].student_id
        assert loaded[0].name == sample_students[0].name

    def test_save_empty_student_list(self, file_handler, temp_data_dir):
        """Test saving an empty list of students."""
        file_handler.save_students([])

        students_file = temp_data_dir / "students.json"
        data = json.loads(students_file.read_text())

        assert data["students"] == []
        assert data["metadata"]["count"] == 0


class TestLoadCourses:
    """Tests for loading courses from file."""

    def test_load_courses_from_existing_file(
        self, file_handler, temp_data_dir, sample_courses
    ):
        """Test loading courses from an existing file."""
        courses_file = temp_data_dir / "courses.json"
        data = {
            "courses": [c.to_dict() for c in sample_courses],
            "metadata": {"version": "1.0", "count": len(sample_courses)},
        }
        courses_file.write_text(json.dumps(data, indent=2))

        loaded = file_handler.load_courses()

        assert len(loaded) == 2
        assert loaded[0].course_code == "CSC1234"
        assert loaded[1].course_code == "MAT5678"

    def test_load_courses_empty_list_when_file_not_exists(self, file_handler):
        """Test that loading returns empty list when file doesn't exist."""
        loaded = file_handler.load_courses()
        assert loaded == []


class TestSaveCourses:
    """Tests for saving courses to file."""

    def test_save_courses_creates_file(
        self, file_handler, temp_data_dir, sample_courses
    ):
        """Test that saving courses creates a file."""
        file_handler.save_courses(sample_courses)

        courses_file = temp_data_dir / "courses.json"
        assert courses_file.exists()

    def test_save_courses_preserves_data(self, file_handler, sample_courses):
        """Test that saved course data can be loaded back correctly."""
        file_handler.save_courses(sample_courses)
        loaded = file_handler.load_courses()

        assert len(loaded) == len(sample_courses)
        assert loaded[0].course_code == sample_courses[0].course_code
        assert loaded[0].credits == sample_courses[0].credits


class TestLoadEnrollments:
    """Tests for loading enrollments from file."""

    def test_load_enrollments_from_existing_file(
        self, file_handler, temp_data_dir, sample_enrollments
    ):
        """Test loading enrollments from an existing file."""
        enrollments_file = temp_data_dir / "enrollments.json"
        data = {
            "enrollments": [e.to_dict() for e in sample_enrollments],
            "metadata": {"version": "1.0", "count": len(sample_enrollments)},
        }
        enrollments_file.write_text(json.dumps(data, indent=2))

        loaded = file_handler.load_enrollments()

        assert len(loaded) == 2
        assert loaded[0].student_id == "S001"
        assert loaded[0].grade == 85.5

    def test_load_enrollments_empty_list_when_file_not_exists(self, file_handler):
        """Test that loading returns empty list when file doesn't exist."""
        loaded = file_handler.load_enrollments()
        assert loaded == []


class TestSaveEnrollments:
    """Tests for saving enrollments to file."""

    def test_save_enrollments_creates_file(
        self, file_handler, temp_data_dir, sample_enrollments
    ):
        """Test that saving enrollments creates a file."""
        file_handler.save_enrollments(sample_enrollments)

        enrollments_file = temp_data_dir / "enrollments.json"
        assert enrollments_file.exists()

    def test_save_enrollments_preserves_data(self, file_handler, sample_enrollments):
        """Test that saved enrollment data can be loaded back correctly."""
        file_handler.save_enrollments(sample_enrollments)
        loaded = file_handler.load_enrollments()

        assert len(loaded) == len(sample_enrollments)
        assert loaded[0].student_id == sample_enrollments[0].student_id
        assert loaded[0].grade == sample_enrollments[0].grade


class TestBackupFunctionality:
    """Tests for backup creation."""

    def test_create_backup_for_students(
        self, file_handler, temp_data_dir, sample_students
    ):
        """Test creating a backup of students file."""
        # First save some data
        file_handler.save_students(sample_students)

        # Create backup
        backup_path = file_handler.create_backup("students")

        assert backup_path.exists()
        assert "students" in backup_path.name
        assert backup_path.suffix == ".bak"

    def test_create_backup_for_courses(
        self, file_handler, temp_data_dir, sample_courses
    ):
        """Test creating a backup of courses file."""
        file_handler.save_courses(sample_courses)
        backup_path = file_handler.create_backup("courses")

        assert backup_path.exists()
        assert "courses" in backup_path.name

    def test_create_backup_preserves_data(
        self, file_handler, temp_data_dir, sample_students
    ):
        """Test that backup contains same data as original."""
        file_handler.save_students(sample_students)
        backup_path = file_handler.create_backup("students")

        # Read backup
        backup_data = json.loads(backup_path.read_text())
        original_data = json.loads((temp_data_dir / "students.json").read_text())

        assert backup_data["students"] == original_data["students"]

    def test_create_backup_when_file_not_exists(self, file_handler):
        """Test creating backup when original file doesn't exist."""
        result = file_handler.create_backup("students")
        assert result is None  # or appropriate behavior


class TestRoundtripOperations:
    """Tests for complete save/load cycles."""

    def test_roundtrip_students(self, file_handler, sample_students):
        """Test complete save and load cycle for students."""
        file_handler.save_students(sample_students)
        loaded = file_handler.load_students()

        assert len(loaded) == len(sample_students)
        for original, loaded_student in zip(sample_students, loaded):
            assert loaded_student.student_id == original.student_id
            assert loaded_student.name == original.name
            assert loaded_student.email == original.email
            assert loaded_student.program == original.program

    def test_roundtrip_courses(self, file_handler, sample_courses):
        """Test complete save and load cycle for courses."""
        file_handler.save_courses(sample_courses)
        loaded = file_handler.load_courses()

        assert len(loaded) == len(sample_courses)
        for original, loaded_course in zip(sample_courses, loaded):
            assert loaded_course.course_code == original.course_code
            assert loaded_course.name == original.name
            assert loaded_course.credits == original.credits
            assert loaded_course.instructor == original.instructor

    def test_roundtrip_enrollments(self, file_handler, sample_enrollments):
        """Test complete save and load cycle for enrollments."""
        file_handler.save_enrollments(sample_enrollments)
        loaded = file_handler.load_enrollments()

        assert len(loaded) == len(sample_enrollments)
        for original, loaded_enrollment in zip(sample_enrollments, loaded):
            assert loaded_enrollment.student_id == original.student_id
            assert loaded_enrollment.course_code == original.course_code
            assert loaded_enrollment.grade == original.grade


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_save_and_load_with_unicode_characters(self, file_handler):
        """Test handling of unicode characters in names."""
        students = [
            Student("S001", "José García", "jose@example.com", "CS"),
            Student("S002", "李明", "li@example.com", "SE"),
        ]
        file_handler.save_students(students)
        loaded = file_handler.load_students()

        assert loaded[0].name == "José García"
        assert loaded[1].name == "李明"

    def test_save_large_dataset(self, file_handler):
        """Test saving and loading a large number of records."""
        students = [
            Student(f"S{i:04d}", f"Student {i}", f"student{i}@example.com", "CS")
            for i in range(1000)
        ]
        file_handler.save_students(students)
        loaded = file_handler.load_students()

        assert len(loaded) == 1000
        assert loaded[0].student_id == "S0000"
        assert loaded[999].student_id == "S0999"

    def test_overwrite_existing_file(self, file_handler, sample_students):
        """Test that saving overwrites existing file."""
        file_handler.save_students(sample_students)

        new_students = [Student("S999", "New Student", "new@example.com", "CS")]
        file_handler.save_students(new_students)

        loaded = file_handler.load_students()
        assert len(loaded) == 1
        assert loaded[0].student_id == "S999"
