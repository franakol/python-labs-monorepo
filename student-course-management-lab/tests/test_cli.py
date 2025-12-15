"""
Tests for the CLI module.

This module contains tests for the Command-Line Interface, mocking user input
and verifying output and service interactions.
"""

import pytest
from unittest.mock import Mock, patch, call
from student_management.ui.cli import CLI
from student_management.services.student_service import StudentService
from student_management.services.course_service import CourseService
from student_management.services.enrollment_service import EnrollmentService
from student_management.models.student import Student
from student_management.models.course import Course
from student_management.models.enrollment import Enrollment


@pytest.fixture
def mock_student_service():
    return Mock(spec=StudentService)


@pytest.fixture
def mock_course_service():
    return Mock(spec=CourseService)


@pytest.fixture
def mock_enrollment_service():
    return Mock(spec=EnrollmentService)


@pytest.fixture
def cli(mock_student_service, mock_course_service, mock_enrollment_service):
    return CLI(mock_student_service, mock_course_service, mock_enrollment_service)


class TestCLIMenu:
    """Tests for CLI menu navigation."""

    def test_main_menu_display(self, cli):
        """Test that main menu is displayed correctly."""
        with patch("builtins.print") as mock_print, patch(
            "builtins.input", side_effect=["0"]
        ):  # Exit immediately
            cli.run()

            # Verify menu options are printed
            mock_print.assert_any_call("\n=== Student Course Management System ===")
            mock_print.assert_any_call("1. Manage Students")
            mock_print.assert_any_call("2. Manage Courses")
            mock_print.assert_any_call("3. Manage Enrollments")
            mock_print.assert_any_call("0. Exit")

    def test_exit_option(self, cli):
        """Test selecting exit option."""
        with patch("builtins.input", side_effect=["0"]):
            cli.run()
            # Should exit without error


class TestStudentManagement:
    """Tests for student management CLI commands."""

    def test_add_student_flow(self, cli, mock_student_service):
        """Test adding a student via CLI."""
        mock_student_service.create_student.return_value = Student(
            "S001", "John", "john@example.com", "CS"
        )

        inputs = [
            "1",  # Manage Students
            "1",  # Add Student
            "S001",  # ID
            "John",  # Name
            "john@example.com",  # Email
            "CS",  # Program
            "0",  # Back
            "0",  # Exit
        ]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_student_service.create_student.assert_called_with(
                "S001", "John", "john@example.com", "CS"
            )
            mock_print.assert_any_call("Student added successfully!")

    def test_list_students_flow(self, cli, mock_student_service):
        """Test listing students via CLI."""
        mock_student_service.list_students.return_value = [
            Student("S001", "John", "john@example.com", "CS")
        ]

        inputs = [
            "1",  # Manage Students
            "2",  # List Students
            "0",  # Back
            "0",  # Exit
        ]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_student_service.list_students.assert_called_once()
            # Check if student info is printed (checking partial string match)
            # We can't easily check exact print calls for table formatting,
            # but we can check if the data appears in calls
            print_calls = [str(call) for call in mock_print.mock_calls]
            assert any("S001" in c for c in print_calls)
            assert any("John" in c for c in print_calls)

    def test_search_student_flow(self, cli, mock_student_service):
        """Test searching students via CLI."""
        mock_student_service.search_students.return_value = []

        inputs = [
            "1",  # Manage Students
            "3",  # Search Student
            "John",  # Name query
            "",  # Program query (empty)
            "0",  # Back
            "0",  # Exit
        ]

        with patch("builtins.input", side_effect=inputs):
            cli.run()

            mock_student_service.search_students.assert_called_with(
                name="John", program=None
            )


class TestCourseManagement:
    """Tests for course management CLI commands."""

    def test_add_course_flow(self, cli, mock_course_service):
        """Test adding a course via CLI."""
        mock_course_service.create_course.return_value = Course(
            "CSC101", "Intro", 3, "Dr. Smith"
        )

        inputs = [
            "2",  # Manage Courses
            "1",  # Add Course
            "CSC101",  # Code
            "Intro",  # Name
            "3",  # Credits
            "Dr. Smith",  # Instructor
            "0",  # Back
            "0",  # Exit
        ]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_course_service.create_course.assert_called_with(
                "CSC101", "Intro", 3, "Dr. Smith"
            )
            mock_print.assert_any_call("Course added successfully!")

    def test_add_course_invalid_credits(self, cli, mock_course_service):
        """Test handling invalid credit input."""
        inputs = [
            "2",  # Manage Courses
            "1",  # Add Course
            "CSC101",
            "Intro",
            "invalid",  # Invalid credits
            "3",  # Valid credits (retry)
            "Dr. Smith",
            "0",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_print.assert_any_call("Error: Credits must be a number.")


class TestEnrollmentManagement:
    """Tests for enrollment management CLI commands."""

    def test_enroll_student_flow(self, cli, mock_enrollment_service):
        """Test enrolling a student via CLI."""
        inputs = [
            "3",  # Manage Enrollments
            "1",  # Enroll Student
            "S001",  # Student ID
            "CSC101",  # Course Code
            "0",  # Back
            "0",  # Exit
        ]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_enrollment_service.enroll_student.assert_called_with("S001", "CSC101")
            mock_print.assert_any_call("Student enrolled successfully!")

    def test_assign_grade_flow(self, cli, mock_enrollment_service):
        """Test assigning a grade via CLI."""
        inputs = [
            "3",  # Manage Enrollments
            "2",  # Assign Grade
            "S001",  # Student ID
            "CSC101",  # Course Code
            "85.5",  # Grade
            "0",  # Back
            "0",  # Exit
        ]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_enrollment_service.assign_grade.assert_called_with(
                "S001", "CSC101", 85.5
            )
            mock_print.assert_any_call("Grade assigned successfully!")


class TestErrorHandling:
    """Tests for CLI error handling."""

    def test_service_error_handling(self, cli, mock_student_service):
        """Test that service errors are caught and displayed."""
        mock_student_service.create_student.side_effect = ValueError("Duplicate ID")

        inputs = ["1", "1", "S001", "John", "john@example.com", "CS", "0", "0"]

        with patch("builtins.input", side_effect=inputs), patch(
            "builtins.print"
        ) as mock_print:
            cli.run()

            mock_print.assert_any_call("Error: Duplicate ID")
