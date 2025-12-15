"""
Tests for the Course model.

This module contains comprehensive tests for the Course class,
including validation, serialization, and edge cases.
"""

import pytest
from student_management.models.course import Course


class TestCourseCreation:
    """Tests for creating Course instances."""

    def test_create_course_with_valid_data(self):
        """Test creating a course with all valid data."""
        course = Course(
            course_code="CSC1234",
            name="Introduction to Programming",
            credits=3,
            instructor="Dr. Smith",
        )
        assert course.course_code == "CSC1234"
        assert course.name == "Introduction to Programming"
        assert course.credits == 3
        assert course.instructor == "Dr. Smith"

    def test_create_course_with_different_credits(self):
        """Test creating courses with different credit values."""
        for credits in [1, 2, 3, 4, 5, 6]:
            course = Course("CSC1234", "Test Course", credits, "Instructor")
            assert course.credits == credits


class TestCourseValidation:
    """Tests for Course validation."""

    def test_validate_valid_course(self):
        """Test that a valid course passes validation."""
        course = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        errors = course.validate()
        assert len(errors) == 0

    def test_validate_empty_course_code(self):
        """Test validation fails with empty course code."""
        course = Course("", "Intro to Programming", 3, "Dr. Smith")
        errors = course.validate()
        assert len(errors) > 0
        assert any("course" in err.lower() and "code" in err.lower() for err in errors)

    def test_validate_invalid_course_code_format(self):
        """Test validation fails with invalid course code format."""
        invalid_codes = [
            "ABC123",  # Missing one digit
            "AB1234",  # Missing one letter
            "ABCD1234",  # Too many letters
            "abc1234",  # Lowercase letters
            "CSC12345",  # Too many digits
            "123ABCD",  # Numbers first
            "CS-1234",  # Special character
        ]
        for code in invalid_codes:
            course = Course(code, "Test Course", 3, "Instructor")
            errors = course.validate()
            assert len(errors) > 0, f"Expected validation error for code: {code}"

    def test_validate_valid_course_code_formats(self):
        """Test validation passes with valid course code formats."""
        valid_codes = ["CSC1234", "MAT5678", "ENG1000", "PHY9999"]
        for code in valid_codes:
            course = Course(code, "Test Course", 3, "Instructor")
            errors = course.validate()
            assert len(errors) == 0, f"Expected no errors for code: {code}"

    def test_validate_empty_name(self):
        """Test validation fails with empty name."""
        course = Course("CSC1234", "", 3, "Dr. Smith")
        errors = course.validate()
        assert len(errors) > 0
        assert any("name" in err.lower() for err in errors)

    def test_validate_whitespace_only_name(self):
        """Test validation fails with whitespace-only name."""
        course = Course("CSC1234", "   ", 3, "Dr. Smith")
        errors = course.validate()
        assert len(errors) > 0

    def test_validate_credits_below_minimum(self):
        """Test validation fails with credits below 1."""
        invalid_credits = [0, -1, -5]
        for credits in invalid_credits:
            course = Course("CSC1234", "Test Course", credits, "Instructor")
            errors = course.validate()
            assert len(errors) > 0, f"Expected error for credits: {credits}"
            assert any("credit" in err.lower() for err in errors)

    def test_validate_credits_above_maximum(self):
        """Test validation fails with credits above 6."""
        invalid_credits = [7, 10, 100]
        for credits in invalid_credits:
            course = Course("CSC1234", "Test Course", credits, "Instructor")
            errors = course.validate()
            assert len(errors) > 0, f"Expected error for credits: {credits}"
            assert any("credit" in err.lower() for err in errors)

    def test_validate_valid_credits_range(self):
        """Test validation passes for credits in valid range (1-6)."""
        for credits in range(1, 7):
            course = Course("CSC1234", "Test Course", credits, "Instructor")
            errors = course.validate()
            assert len(errors) == 0, f"Expected no errors for credits: {credits}"

    def test_validate_empty_instructor(self):
        """Test validation fails with empty instructor."""
        course = Course("CSC1234", "Test Course", 3, "")
        errors = course.validate()
        assert len(errors) > 0
        assert any("instructor" in err.lower() for err in errors)

    def test_validate_multiple_errors(self):
        """Test validation returns multiple errors when multiple fields are invalid."""
        course = Course("", "", 0, "")
        errors = course.validate()
        assert len(errors) >= 3  # At least one error per invalid field


class TestCourseSerialization:
    """Tests for Course serialization and deserialization."""

    def test_to_dict(self):
        """Test converting course to dictionary."""
        course = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        data = course.to_dict()

        assert isinstance(data, dict)
        assert data["course_code"] == "CSC1234"
        assert data["name"] == "Intro to Programming"
        assert data["credits"] == 3
        assert data["instructor"] == "Dr. Smith"

    def test_from_dict(self):
        """Test creating course from dictionary."""
        data = {
            "course_code": "MAT5678",
            "name": "Calculus I",
            "credits": 4,
            "instructor": "Prof. Johnson",
        }
        course = Course.from_dict(data)

        assert course.course_code == "MAT5678"
        assert course.name == "Calculus I"
        assert course.credits == 4
        assert course.instructor == "Prof. Johnson"

    def test_to_dict_from_dict_roundtrip(self):
        """Test that to_dict and from_dict are inverses."""
        original = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        data = original.to_dict()
        restored = Course.from_dict(data)

        assert restored.course_code == original.course_code
        assert restored.name == original.name
        assert restored.credits == original.credits
        assert restored.instructor == original.instructor


class TestCourseStringRepresentation:
    """Tests for Course string representation."""

    def test_str_representation(self):
        """Test __str__ method returns readable format."""
        course = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        str_repr = str(course)

        assert "CSC1234" in str_repr
        assert "Intro to Programming" in str_repr

    def test_repr_representation(self):
        """Test __repr__ method returns developer-friendly format."""
        course = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        repr_str = repr(course)

        assert "Course" in repr_str
        assert "CSC1234" in repr_str


class TestCourseEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_long_course_name(self):
        """Test course with very long name."""
        long_name = "A" * 100
        course = Course("CSC1234", long_name, 3, "Dr. Smith")
        assert course.name == long_name

    def test_special_characters_in_instructor_name(self):
        """Test instructor name with special characters."""
        names = [
            "Dr. O'Brien",
            "Prof. José García",
            "Dr. Anne-Marie Smith",
            "李教授",  # Chinese characters
        ]
        for name in names:
            course = Course("CSC1234", "Test Course", 3, name)
            assert course.instructor == name

    def test_case_sensitivity_in_code(self):
        """Test that course codes are case-sensitive."""
        course1 = Course("csc1234", "Test Course", 3, "Instructor")
        course2 = Course("CSC1234", "Test Course", 3, "Instructor")
        # While lowercase won't pass validation, they are stored as-is
        assert course1.course_code != course2.course_code
