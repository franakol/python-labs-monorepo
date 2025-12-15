"""
Tests for the EnrollmentService class.

This module contains comprehensive tests for enrollment management operations
including enrolling students, assigning grades, and retrieving enrollments.
"""

import pytest
from student_management.services.enrollment_service import EnrollmentService
from student_management.services.student_service import StudentService
from student_management.services.course_service import CourseService
from student_management.data.file_handler import FileHandler
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
def student_service(file_handler):
    """Create a StudentService instance with sample data."""
    service = StudentService(file_handler)
    service.create_student("S001", "John Doe", "john@example.com", "CS")
    service.create_student("S002", "Jane Smith", "jane@example.com", "SE")
    return service


@pytest.fixture
def course_service(file_handler):
    """Create a CourseService instance with sample data."""
    service = CourseService(file_handler)
    service.create_course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
    service.create_course("MAT5678", "Calculus I", 4, "Prof. Johnson")
    return service


@pytest.fixture
def enrollment_service(file_handler, student_service, course_service):
    """Create an EnrollmentService instance."""
    return EnrollmentService(file_handler, student_service, course_service)


class TestEnrollmentServiceEnrollment:
    """Tests for enrolling students."""

    def test_enroll_student_success(self, enrollment_service):
        """Test enrolling a student in a course."""
        enrollment = enrollment_service.enroll_student("S001", "CSC1234")

        assert enrollment.student_id == "S001"
        assert enrollment.course_code == "CSC1234"
        assert enrollment.grade is None

    def test_enroll_student_persists_to_file(self, enrollment_service):
        """Test that enrollment is saved to file."""
        enrollment_service.enroll_student("S001", "CSC1234")

        # Load from service to verify persistence
        enrollments = enrollment_service.get_student_enrollments("S001")
        assert len(enrollments) == 1
        assert enrollments[0].course_code == "CSC1234"

    def test_enroll_nonexistent_student_raises_error(self, enrollment_service):
        """Test that enrolling non-existent student raises ValueError."""
        with pytest.raises(ValueError, match="Student.*not found"):
            enrollment_service.enroll_student("S999", "CSC1234")

    def test_enroll_nonexistent_course_raises_error(self, enrollment_service):
        """Test that enrolling in non-existent course raises ValueError."""
        with pytest.raises(ValueError, match="Course.*not found"):
            enrollment_service.enroll_student("S001", "NON9999")

    def test_enroll_duplicate_enrollment_raises_error(self, enrollment_service):
        """Test that duplicate enrollment raises ValueError."""
        enrollment_service.enroll_student("S001", "CSC1234")

        with pytest.raises(ValueError, match="already enrolled"):
            enrollment_service.enroll_student("S001", "CSC1234")


class TestEnrollmentServiceGrading:
    """Tests for assigning grades."""

    def test_assign_grade_success(self, enrollment_service):
        """Test assigning a grade to an enrollment."""
        enrollment_service.enroll_student("S001", "CSC1234")

        updated = enrollment_service.assign_grade("S001", "CSC1234", 85.5)

        assert updated.grade == 85.5
        assert updated.student_id == "S001"
        assert updated.course_code == "CSC1234"

    def test_assign_grade_persists_to_file(self, enrollment_service):
        """Test that assigned grade is persisted to file."""
        enrollment_service.enroll_student("S001", "CSC1234")
        enrollment_service.assign_grade("S001", "CSC1234", 90.0)

        # Reload
        enrollments = enrollment_service.get_student_enrollments("S001")
        assert enrollments[0].grade == 90.0

    def test_assign_invalid_grade_raises_error(self, enrollment_service):
        """Test that assigning invalid grade raises ValueError."""
        enrollment_service.enroll_student("S001", "CSC1234")

        with pytest.raises(ValueError):
            enrollment_service.assign_grade("S001", "CSC1234", 105.0)

    def test_assign_grade_nonexistent_enrollment_raises_error(self, enrollment_service):
        """Test that assigning grade to non-existent enrollment raises ValueError."""
        with pytest.raises(ValueError, match="not enrolled"):
            enrollment_service.assign_grade("S001", "MAT5678", 85.0)


class TestEnrollmentServiceRetrieval:
    """Tests for retrieving enrollments."""

    def test_get_student_enrollments(self, enrollment_service):
        """Test getting all enrollments for a student."""
        enrollment_service.enroll_student("S001", "CSC1234")
        enrollment_service.enroll_student("S001", "MAT5678")
        enrollment_service.enroll_student("S002", "CSC1234")

        enrollments = enrollment_service.get_student_enrollments("S001")

        assert len(enrollments) == 2
        codes = [e.course_code for e in enrollments]
        assert "CSC1234" in codes
        assert "MAT5678" in codes

    def test_get_course_enrollments(self, enrollment_service):
        """Test getting all enrollments for a course."""
        enrollment_service.enroll_student("S001", "CSC1234")
        enrollment_service.enroll_student("S002", "CSC1234")
        enrollment_service.enroll_student("S001", "MAT5678")

        enrollments = enrollment_service.get_course_enrollments("CSC1234")

        assert len(enrollments) == 2
        ids = [e.student_id for e in enrollments]
        assert "S001" in ids
        assert "S002" in ids

    def test_get_student_gpa(self, enrollment_service):
        """Test calculating student GPA (average grade)."""
        enrollment_service.enroll_student("S001", "CSC1234")
        enrollment_service.enroll_student("S001", "MAT5678")

        enrollment_service.assign_grade("S001", "CSC1234", 80.0)
        enrollment_service.assign_grade("S001", "MAT5678", 90.0)

        gpa = enrollment_service.get_student_gpa("S001")
        assert gpa == 85.0

    def test_get_course_average(self, enrollment_service):
        """Test calculating course average grade."""
        enrollment_service.enroll_student("S001", "CSC1234")
        enrollment_service.enroll_student("S002", "CSC1234")

        enrollment_service.assign_grade("S001", "CSC1234", 70.0)
        enrollment_service.assign_grade("S002", "CSC1234", 90.0)

        avg = enrollment_service.get_course_average("CSC1234")
        assert avg == 80.0


class TestEnrollmentServiceUnenrollment:
    """Tests for unenrolling students."""

    def test_unenroll_student_success(self, enrollment_service):
        """Test unenrolling a student."""
        enrollment_service.enroll_student("S001", "CSC1234")

        result = enrollment_service.unenroll_student("S001", "CSC1234")

        assert result is True
        enrollments = enrollment_service.get_student_enrollments("S001")
        assert len(enrollments) == 0

    def test_unenroll_nonexistent_enrollment_returns_false(self, enrollment_service):
        """Test that unenrolling non-existent enrollment returns False."""
        result = enrollment_service.unenroll_student("S001", "CSC1234")
        assert result is False

    def test_unenroll_persists_to_file(self, enrollment_service):
        """Test that unenrollment is persisted to file."""
        enrollment_service.enroll_student("S001", "CSC1234")
        enrollment_service.enroll_student("S001", "MAT5678")

        enrollment_service.unenroll_student("S001", "CSC1234")

        enrollments = enrollment_service.get_student_enrollments("S001")
        assert len(enrollments) == 1
        assert enrollments[0].course_code == "MAT5678"
