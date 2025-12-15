"""
Tests for the Enrollment model.

This module contains comprehensive tests for the Enrollment class,
including validation, grade calculation, serialization, and edge cases.
"""

import pytest
from datetime import datetime
from student_management.models.enrollment import Enrollment


class TestEnrollmentCreation:
    """Tests for creating Enrollment instances."""

    def test_create_enrollment_without_grade(self):
        """Test creating an enrollment without a grade."""
        enrollment = Enrollment("S001", "CSC1234")
        assert enrollment.student_id == "S001"
        assert enrollment.course_code == "CSC1234"
        assert enrollment.grade is None
        assert isinstance(enrollment.enrollment_date, datetime)

    def test_create_enrollment_with_grade(self):
        """Test creating an enrollment with a grade."""
        enrollment = Enrollment("S001", "CSC1234", grade=85.5)
        assert enrollment.grade == 85.5

    def test_create_enrollment_with_custom_date(self):
        """Test creating an enrollment with a custom enrollment date."""
        custom_date = datetime(2024, 1, 15, 10, 30, 0)
        enrollment = Enrollment("S001", "CSC1234", enrollment_date=custom_date)
        assert enrollment.enrollment_date == custom_date


class TestEnrollmentValidation:
    """Tests for Enrollment validation."""

    def test_validate_valid_enrollment_without_grade(self):
        """Test that a valid enrollment without grade passes validation."""
        enrollment = Enrollment("S001", "CSC1234")
        errors = enrollment.validate()
        assert len(errors) == 0

    def test_validate_valid_enrollment_with_grade(self):
        """Test that a valid enrollment with grade passes validation."""
        enrollment = Enrollment("S001", "CSC1234", grade=85.5)
        errors = enrollment.validate()
        assert len(errors) == 0

    def test_validate_empty_student_id(self):
        """Test validation fails with empty student ID."""
        enrollment = Enrollment("", "CSC1234")
        errors = enrollment.validate()
        assert len(errors) > 0
        assert any("student" in err.lower() and "id" in err.lower() for err in errors)

    def test_validate_empty_course_code(self):
        """Test validation fails with empty course code."""
        enrollment = Enrollment("S001", "")
        errors = enrollment.validate()
        assert len(errors) > 0
        assert any("course" in err.lower() for err in errors)

    def test_validate_grade_below_zero(self):
        """Test validation fails with grade below 0."""
        invalid_grades = [-1, -10, -0.1]
        for grade in invalid_grades:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            errors = enrollment.validate()
            assert len(errors) > 0, f"Expected error for grade: {grade}"
            assert any("grade" in err.lower() for err in errors)

    def test_validate_grade_above_hundred(self):
        """Test validation fails with grade above 100."""
        invalid_grades = [100.1, 101, 150]
        for grade in invalid_grades:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            errors = enrollment.validate()
            assert len(errors) > 0, f"Expected error for grade: {grade}"
            assert any("grade" in err.lower() for err in errors)

    def test_validate_valid_grade_range(self):
        """Test validation passes for grades in valid range (0-100)."""
        valid_grades = [0, 0.0, 50, 75.5, 99.9, 100]
        for grade in valid_grades:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            errors = enrollment.validate()
            assert len(errors) == 0, f"Expected no errors for grade: {grade}"


class TestLetterGradeCalculation:
    """Tests for letter grade calculation."""

    def test_letter_grade_a_plus(self):
        """Test letter grade for A+ range."""
        for grade in [90, 95, 100]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "A+"

    def test_letter_grade_a(self):
        """Test letter grade for A range."""
        for grade in [85, 87, 89]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "A"

    def test_letter_grade_b_plus(self):
        """Test letter grade for B+ range."""
        for grade in [80, 82, 84]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "B+"

    def test_letter_grade_b(self):
        """Test letter grade for B range."""
        for grade in [75, 77, 79]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "B"

    def test_letter_grade_c_plus(self):
        """Test letter grade for C+ range."""
        for grade in [70, 72, 74]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "C+"

    def test_letter_grade_c(self):
        """Test letter grade for C range."""
        for grade in [65, 67, 69]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "C"

    def test_letter_grade_d_plus(self):
        """Test letter grade for D+ range."""
        for grade in [60, 62, 64]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "D+"

    def test_letter_grade_d(self):
        """Test letter grade for D range."""
        for grade in [55, 57, 59]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "D"

    def test_letter_grade_f(self):
        """Test letter grade for F range."""
        for grade in [0, 25, 50, 54]:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == "F"

    def test_letter_grade_without_grade(self):
        """Test letter grade when no grade is set."""
        enrollment = Enrollment("S001", "CSC1234")
        assert enrollment.calculate_letter_grade() == "N/A"

    def test_letter_grade_boundary_values(self):
        """Test letter grade at exact boundary values."""
        boundaries = [
            (90, "A+"),
            (89, "A"),
            (85, "A"),
            (84, "B+"),
            (80, "B+"),
            (79, "B"),
            (75, "B"),
            (74, "C+"),
            (70, "C+"),
            (69, "C"),
            (65, "C"),
            (64, "D+"),
            (60, "D+"),
            (59, "D"),
            (55, "D"),
            (54, "F"),
            (0, "F"),
        ]
        for grade, expected_letter in boundaries:
            enrollment = Enrollment("S001", "CSC1234", grade=grade)
            assert enrollment.calculate_letter_grade() == expected_letter


class TestEnrollmentSerialization:
    """Tests for Enrollment serialization and deserialization."""

    def test_to_dict_without_grade(self):
        """Test converting enrollment without grade to dictionary."""
        enrollment = Enrollment("S001", "CSC1234")
        data = enrollment.to_dict()

        assert isinstance(data, dict)
        assert data["student_id"] == "S001"
        assert data["course_code"] == "CSC1234"
        assert data["grade"] is None
        assert "enrollment_date" in data

    def test_to_dict_with_grade(self):
        """Test converting enrollment with grade to dictionary."""
        enrollment = Enrollment("S001", "CSC1234", grade=85.5)
        data = enrollment.to_dict()

        assert data["grade"] == 85.5

    def test_from_dict(self):
        """Test creating enrollment from dictionary."""
        data = {
            "student_id": "S001",
            "course_code": "CSC1234",
            "grade": 85.5,
            "enrollment_date": "2024-01-15T10:30:00",
        }
        enrollment = Enrollment.from_dict(data)

        assert enrollment.student_id == "S001"
        assert enrollment.course_code == "CSC1234"
        assert enrollment.grade == 85.5
        assert isinstance(enrollment.enrollment_date, datetime)

    def test_to_dict_from_dict_roundtrip(self):
        """Test that to_dict and from_dict are inverses."""
        original = Enrollment("S001", "CSC1234", grade=85.5)
        data = original.to_dict()
        restored = Enrollment.from_dict(data)

        assert restored.student_id == original.student_id
        assert restored.course_code == original.course_code
        assert restored.grade == original.grade


class TestEnrollmentStringRepresentation:
    """Tests for Enrollment string representation."""

    def test_str_representation_with_grade(self):
        """Test __str__ method with grade."""
        enrollment = Enrollment("S001", "CSC1234", grade=85.5)
        str_repr = str(enrollment)

        assert "S001" in str_repr
        assert "CSC1234" in str_repr
        assert "85.5" in str_repr or "A" in str_repr

    def test_str_representation_without_grade(self):
        """Test __str__ method without grade."""
        enrollment = Enrollment("S001", "CSC1234")
        str_repr = str(enrollment)

        assert "S001" in str_repr
        assert "CSC1234" in str_repr

    def test_repr_representation(self):
        """Test __repr__ method."""
        enrollment = Enrollment("S001", "CSC1234", grade=85.5)
        repr_str = repr(enrollment)

        assert "Enrollment" in repr_str
        assert "S001" in repr_str
        assert "CSC1234" in repr_str


class TestEnrollmentEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_decimal_grade(self):
        """Test enrollment with decimal grade."""
        enrollment = Enrollment("S001", "CSC1234", grade=85.75)
        assert enrollment.grade == 85.75

    def test_zero_grade(self):
        """Test enrollment with zero grade."""
        enrollment = Enrollment("S001", "CSC1234", grade=0)
        assert enrollment.grade == 0
        assert enrollment.calculate_letter_grade() == "F"

    def test_perfect_grade(self):
        """Test enrollment with perfect grade."""
        enrollment = Enrollment("S001", "CSC1234", grade=100)
        assert enrollment.grade == 100
        assert enrollment.calculate_letter_grade() == "A+"

    def test_update_grade(self):
        """Test updating grade after creation."""
        enrollment = Enrollment("S001", "CSC1234")
        assert enrollment.grade is None

        enrollment.grade = 85.5
        assert enrollment.grade == 85.5
        assert enrollment.calculate_letter_grade() == "A"
