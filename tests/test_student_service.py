"""
Tests for the StudentService class.

This module contains comprehensive tests for student management operations
including CRUD operations and search functionality.
"""

import pytest
from pathlib import Path
from student_management.services.student_service import StudentService
from student_management.data.file_handler import FileHandler
from student_management.models.student import Student


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
def student_service(file_handler):
    """Create a StudentService instance."""
    return StudentService(file_handler)


class TestStudentServiceCreation:
    """Tests for creating students."""

    def test_create_student_with_valid_data(self, student_service):
        """Test creating a student with valid data."""
        student = student_service.create_student(
            "S001", "John Doe", "john@example.com", "Computer Science"
        )

        assert student.student_id == "S001"
        assert student.name == "John Doe"
        assert student.email == "john@example.com"
        assert student.program == "Computer Science"

    def test_create_student_persists_to_file(self, student_service):
        """Test that created student is saved to file."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        # Load from service to verify persistence
        students = student_service.list_students()
        assert len(students) == 1
        assert students[0].student_id == "S001"

    def test_create_student_with_invalid_data_raises_error(self, student_service):
        """Test that creating student with invalid data raises ValueError."""
        with pytest.raises(ValueError):
            student_service.create_student("", "John Doe", "john@example.com", "CS")

    def test_create_student_with_invalid_email_raises_error(self, student_service):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError):
            student_service.create_student("S001", "John Doe", "invalid-email", "CS")

    def test_create_duplicate_student_raises_error(self, student_service):
        """Test that creating duplicate student ID raises ValueError."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        with pytest.raises(ValueError, match="already exists"):
            student_service.create_student("S001", "Jane Doe", "jane@example.com", "SE")


class TestStudentServiceRetrieval:
    """Tests for retrieving students."""

    def test_get_student_by_id(self, student_service):
        """Test getting a student by ID."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        student = student_service.get_student("S001")
        assert student is not None
        assert student.student_id == "S001"
        assert student.name == "John Doe"

    def test_get_nonexistent_student_returns_none(self, student_service):
        """Test that getting non-existent student returns None."""
        student = student_service.get_student("S999")
        assert student is None

    def test_list_students_empty(self, student_service):
        """Test listing students when none exist."""
        students = student_service.list_students()
        assert students == []

    def test_list_students_with_data(self, student_service):
        """Test listing all students."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "Jane Smith", "jane@example.com", "SE")

        students = student_service.list_students()
        assert len(students) == 2
        assert students[0].student_id == "S001"
        assert students[1].student_id == "S002"


class TestStudentServiceUpdate:
    """Tests for updating students."""

    def test_update_student_email(self, student_service):
        """Test updating student email."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        updated = student_service.update_student("S001", email="newemail@example.com")

        assert updated.email == "newemail@example.com"
        assert updated.name == "John Doe"  # Other fields unchanged

    def test_update_student_name(self, student_service):
        """Test updating student name."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        updated = student_service.update_student("S001", name="John Smith")

        assert updated.name == "John Smith"

    def test_update_student_program(self, student_service):
        """Test updating student program."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        updated = student_service.update_student("S001", program="Software Engineering")

        assert updated.program == "Software Engineering"

    def test_update_multiple_fields(self, student_service):
        """Test updating multiple fields at once."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        updated = student_service.update_student(
            "S001", name="John Smith", email="john.smith@example.com"
        )

        assert updated.name == "John Smith"
        assert updated.email == "john.smith@example.com"

    def test_update_nonexistent_student_raises_error(self, student_service):
        """Test that updating non-existent student raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            student_service.update_student("S999", name="Test")

    def test_update_with_invalid_email_raises_error(self, student_service):
        """Test that updating with invalid email raises ValueError."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        with pytest.raises(ValueError):
            student_service.update_student("S001", email="invalid-email")

    def test_update_persists_to_file(self, student_service):
        """Test that updates are persisted to file."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.update_student("S001", name="John Smith")

        # Reload from file
        students = student_service.list_students()
        assert students[0].name == "John Smith"


class TestStudentServiceDeletion:
    """Tests for deleting students."""

    def test_delete_student(self, student_service):
        """Test deleting a student."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        result = student_service.delete_student("S001")

        assert result is True
        assert student_service.get_student("S001") is None

    def test_delete_nonexistent_student_returns_false(self, student_service):
        """Test that deleting non-existent student returns False."""
        result = student_service.delete_student("S999")
        assert result is False

    def test_delete_persists_to_file(self, student_service):
        """Test that deletion is persisted to file."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "Jane Smith", "jane@example.com", "SE")

        student_service.delete_student("S001")

        students = student_service.list_students()
        assert len(students) == 1
        assert students[0].student_id == "S002"


class TestStudentServiceSearch:
    """Tests for searching students."""

    def test_search_students_by_name(self, student_service):
        """Test searching students by name."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "Jane Smith", "jane@example.com", "SE")
        student_service.create_student("S003", "John Smith", "jsmith@example.com", "CS")

        results = student_service.search_students(name="John")

        assert len(results) == 2
        assert all("John" in s.name for s in results)

    def test_search_students_by_program(self, student_service):
        """Test searching students by program."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "Jane Smith", "jane@example.com", "SE")
        student_service.create_student("S003", "Bob Johnson", "bob@example.com", "CS")

        results = student_service.search_students(program="CS")

        assert len(results) == 2
        assert all(s.program == "CS" for s in results)

    def test_search_students_by_name_and_program(self, student_service):
        """Test searching with both name and program filters."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "John Smith", "jsmith@example.com", "SE")
        student_service.create_student("S003", "Jane Doe", "jane@example.com", "CS")

        results = student_service.search_students(name="John", program="CS")

        assert len(results) == 1
        assert results[0].student_id == "S001"

    def test_search_students_case_insensitive(self, student_service):
        """Test that search is case-insensitive."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        results = student_service.search_students(name="john")

        assert len(results) == 1

    def test_search_students_partial_match(self, student_service):
        """Test that search supports partial matching."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        results = student_service.search_students(name="Doe")

        assert len(results) == 1

    def test_search_students_no_results(self, student_service):
        """Test search with no matching results."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")

        results = student_service.search_students(name="Nonexistent")

        assert results == []

    def test_search_students_no_criteria_returns_all(self, student_service):
        """Test that search with no criteria returns all students."""
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "Jane Smith", "jane@example.com", "SE")

        results = student_service.search_students()

        assert len(results) == 2


class TestStudentServicePersistence:
    """Tests for data persistence and loading."""

    def test_loads_existing_students_on_creation(self, file_handler):
        """Test that service loads existing students from file on creation."""
        # Manually save some students
        students = [
            Student("S001", "John Doe", "john@example.com", "CS"),
            Student("S002", "Jane Smith", "jane@example.com", "SE"),
        ]
        file_handler.save_students(students)

        # Create new service instance
        service = StudentService(file_handler)
        loaded = service.list_students()

        assert len(loaded) == 2
        assert loaded[0].student_id == "S001"

    def test_multiple_operations_persist(self, student_service):
        """Test that multiple operations are persisted correctly."""
        # Create multiple students
        student_service.create_student("S001", "John Doe", "john@example.com", "CS")
        student_service.create_student("S002", "Jane Smith", "jane@example.com", "SE")

        # Update one
        student_service.update_student("S001", name="John Smith")

        # Delete one
        student_service.delete_student("S002")

        # Verify final state
        students = student_service.list_students()
        assert len(students) == 1
        assert students[0].student_id == "S001"
        assert students[0].name == "John Smith"
