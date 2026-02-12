"""
Tests for the CourseService class.

This module contains comprehensive tests for course management operations
including CRUD operations and search functionality.
"""

import pytest
from student_management.services.course_service import CourseService
from student_management.data.file_handler import FileHandler
from student_management.models.course import Course


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
def course_service(file_handler):
    """Create a CourseService instance."""
    return CourseService(file_handler)


class TestCourseServiceCreation:
    """Tests for creating courses."""

    def test_create_course_with_valid_data(self, course_service):
        """Test creating a course with valid data."""
        course = course_service.create_course(
            "CSC1234", "Intro to Programming", 3, "Dr. Smith"
        )

        assert course.course_code == "CSC1234"
        assert course.name == "Intro to Programming"
        assert course.credits == 3
        assert course.instructor == "Dr. Smith"

    def test_create_course_persists_to_file(self, course_service):
        """Test that created course is saved to file."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        # Load from service to verify persistence
        courses = course_service.list_courses()
        assert len(courses) == 1
        assert courses[0].course_code == "CSC1234"

    def test_create_course_with_invalid_data_raises_error(self, course_service):
        """Test that creating course with invalid data raises ValueError."""
        with pytest.raises(ValueError):
            course_service.create_course("", "Intro to Programming", 3, "Dr. Smith")

    def test_create_course_with_invalid_code_format_raises_error(self, course_service):
        """Test that invalid course code format raises ValueError."""
        with pytest.raises(ValueError):
            course_service.create_course(
                "INVALID", "Intro to Programming", 3, "Dr. Smith"
            )

    def test_create_duplicate_course_raises_error(self, course_service):
        """Test that creating duplicate course code raises ValueError."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        with pytest.raises(ValueError, match="already exists"):
            course_service.create_course(
                "CSC1234", "Advanced Programming", 4, "Prof. Jones"
            )


class TestCourseServiceRetrieval:
    """Tests for retrieving courses."""

    def test_get_course_by_code(self, course_service):
        """Test getting a course by code."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        course = course_service.get_course("CSC1234")
        assert course is not None
        assert course.course_code == "CSC1234"
        assert course.name == "Intro to Programming"

    def test_get_nonexistent_course_returns_none(self, course_service):
        """Test that getting non-existent course returns None."""
        course = course_service.get_course("NON9999")
        assert course is None

    def test_list_courses_empty(self, course_service):
        """Test listing courses when none exist."""
        courses = course_service.list_courses()
        assert courses == []

    def test_list_courses_with_data(self, course_service):
        """Test listing all courses."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")

        courses = course_service.list_courses()
        assert len(courses) == 2
        assert courses[0].course_code == "CSC1234"
        assert courses[1].course_code == "MAT5678"


class TestCourseServiceUpdate:
    """Tests for updating courses."""

    def test_update_course_instructor(self, course_service):
        """Test updating course instructor."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        updated = course_service.update_course("CSC1234", instructor="Prof. Jones")

        assert updated.instructor == "Prof. Jones"
        assert updated.name == "Intro to Programming"  # Other fields unchanged

    def test_update_course_name(self, course_service):
        """Test updating course name."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        updated = course_service.update_course("CSC1234", name="Advanced Programming")

        assert updated.name == "Advanced Programming"

    def test_update_course_credits(self, course_service):
        """Test updating course credits."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        updated = course_service.update_course("CSC1234", credits=4)

        assert updated.credits == 4

    def test_update_multiple_fields(self, course_service):
        """Test updating multiple fields at once."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        updated = course_service.update_course(
            "CSC1234", name="Advanced Programming", credits=4
        )

        assert updated.name == "Advanced Programming"
        assert updated.credits == 4

    def test_update_nonexistent_course_raises_error(self, course_service):
        """Test that updating non-existent course raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            course_service.update_course("NON9999", name="Test")

    def test_update_with_invalid_credits_raises_error(self, course_service):
        """Test that updating with invalid credits raises ValueError."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        with pytest.raises(ValueError):
            course_service.update_course("CSC1234", credits=10)

    def test_update_persists_to_file(self, course_service):
        """Test that updates are persisted to file."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.update_course("CSC1234", instructor="Prof. Jones")

        # Reload from file
        courses = course_service.list_courses()
        assert courses[0].instructor == "Prof. Jones"


class TestCourseServiceDeletion:
    """Tests for deleting courses."""

    def test_delete_course(self, course_service):
        """Test deleting a course."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        result = course_service.delete_course("CSC1234")

        assert result is True
        assert course_service.get_course("CSC1234") is None

    def test_delete_nonexistent_course_returns_false(self, course_service):
        """Test that deleting non-existent course returns False."""
        result = course_service.delete_course("NON9999")
        assert result is False

    def test_delete_persists_to_file(self, course_service):
        """Test that deletion is persisted to file."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")

        course_service.delete_course("CSC1234")

        courses = course_service.list_courses()
        assert len(courses) == 1
        assert courses[0].course_code == "MAT5678"


class TestCourseServiceSearch:
    """Tests for searching courses."""

    def test_search_courses_by_name(self, course_service):
        """Test searching courses by name."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")
        course_service.create_course("CSC2000", "Advanced Programming", 3, "Dr. Smith")

        results = course_service.search_courses(name="Programming")

        assert len(results) == 2
        assert all("Programming" in c.name for c in results)

    def test_search_courses_by_instructor(self, course_service):
        """Test searching courses by instructor."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")
        course_service.create_course("CSC2000", "Advanced Programming", 3, "Dr. Smith")

        results = course_service.search_courses(instructor="Dr. Smith")

        assert len(results) == 2
        assert all(c.instructor == "Dr. Smith" for c in results)

    def test_search_courses_by_code(self, course_service):
        """Test searching courses by code."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")

        results = course_service.search_courses(course_code="CSC")

        assert len(results) == 1
        assert results[0].course_code == "CSC1234"

    def test_search_courses_case_insensitive(self, course_service):
        """Test that search is case-insensitive."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        results = course_service.search_courses(name="programming")

        assert len(results) == 1

    def test_search_courses_multiple_criteria(self, course_service):
        """Test searching with multiple criteria."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        course_service.create_course("CSC2000", "Advanced Programming", 3, "Dr. Smith")
        course_service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")

        results = course_service.search_courses(
            name="Programming", instructor="Dr. Smith"
        )

        assert len(results) == 2

    def test_search_courses_no_results(self, course_service):
        """Test search with no matching results."""
        course_service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")

        results = course_service.search_courses(name="Nonexistent")

        assert results == []


class TestCourseServicePersistence:
    """Tests for data persistence and loading."""

    def test_loads_existing_courses_on_creation(self, file_handler):
        """Test that service loads existing courses from file on creation."""
        # Manually save some courses
        courses = [
            Course("CSC1234", "Intro to Programming", 3, "Dr. Smith"),
            Course("MAT5678", "Calculus I", 4, "Prof. Johnson"),
        ]
        file_handler.save_courses(courses)

        # Create new service instance
        service = CourseService(file_handler)
        loaded = service.list_courses()

        assert len(loaded) == 2
        assert loaded[0].course_code == "CSC1234"
