"""
Tests for the Student model.

This module contains comprehensive tests for the Student class,
including validation, serialization, and edge cases.
"""

import pytest
from student_management.models.student import Student


class TestStudentCreation:
    """Tests for creating Student instances."""

    def test_create_student_with_valid_data(self):
        """Test creating a student with all valid data."""
        student = Student(
            student_id="S001",
            name="John Doe",
            email="john.doe@example.com",
            program="Computer Science",
        )
        assert student.student_id == "S001"
        assert student.name == "John Doe"
        assert student.email == "john.doe@example.com"
        assert student.program == "Computer Science"

    def test_create_student_with_different_program(self):
        """Test creating students with different programs."""
        student = Student(
            "S002", "Jane Smith", "jane@example.com", "Software Engineering"
        )
        assert student.program == "Software Engineering"


class TestStudentValidation:
    """Tests for Student validation."""

    def test_validate_valid_student(self):
        """Test that a valid student passes validation."""
        student = Student("S001", "John Doe", "john@example.com", "CS")
        errors = student.validate()
        assert len(errors) == 0

    def test_validate_empty_student_id(self):
        """Test validation fails with empty student ID."""
        student = Student("", "John Doe", "john@example.com", "CS")
        errors = student.validate()
        assert len(errors) > 0
        assert any("student_id" in err.lower() or "id" in err.lower() for err in errors)

    def test_validate_whitespace_only_student_id(self):
        """Test validation fails with whitespace-only student ID."""
        student = Student("   ", "John Doe", "john@example.com", "CS")
        errors = student.validate()
        assert len(errors) > 0

    def test_validate_empty_name(self):
        """Test validation fails with empty name."""
        student = Student("S001", "", "john@example.com", "CS")
        errors = student.validate()
        assert len(errors) > 0
        assert any("name" in err.lower() for err in errors)

    def test_validate_whitespace_only_name(self):
        """Test validation fails with whitespace-only name."""
        student = Student("S001", "   ", "john@example.com", "CS")
        errors = student.validate()
        assert len(errors) > 0

    def test_validate_invalid_email_format(self):
        """Test validation fails with invalid email format."""
        invalid_emails = [
            "not-an-email",
            "missing@domain",
            "@nodomain.com",
            "no@.com",
            "",
            "   ",
        ]
        for email in invalid_emails:
            student = Student("S001", "John Doe", email, "CS")
            errors = student.validate()
            assert len(errors) > 0, f"Expected validation error for email: {email}"
            assert any("email" in err.lower() for err in errors)

    def test_validate_valid_email_formats(self):
        """Test validation passes with various valid email formats."""
        valid_emails = [
            "john@example.com",
            "jane.smith@university.edu",
            "student123@school.ac.uk",
            "first.last@sub.domain.com",
        ]
        for email in valid_emails:
            student = Student("S001", "John Doe", email, "CS")
            errors = student.validate()
            assert len(errors) == 0, f"Expected no errors for email: {email}"

    def test_validate_empty_program(self):
        """Test validation fails with empty program."""
        student = Student("S001", "John Doe", "john@example.com", "")
        errors = student.validate()
        assert len(errors) > 0
        assert any("program" in err.lower() for err in errors)

    def test_validate_multiple_errors(self):
        """Test validation returns multiple errors when multiple fields are invalid."""
        student = Student("", "", "invalid-email", "")
        errors = student.validate()
        assert len(errors) >= 3  # At least one error per invalid field


class TestStudentSerialization:
    """Tests for Student serialization and deserialization."""

    def test_to_dict(self):
        """Test converting student to dictionary."""
        student = Student("S001", "John Doe", "john@example.com", "CS")
        data = student.to_dict()

        assert isinstance(data, dict)
        assert data["student_id"] == "S001"
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["program"] == "CS"

    def test_from_dict(self):
        """Test creating student from dictionary."""
        data = {
            "student_id": "S001",
            "name": "John Doe",
            "email": "john@example.com",
            "program": "Computer Science",
        }
        student = Student.from_dict(data)

        assert student.student_id == "S001"
        assert student.name == "John Doe"
        assert student.email == "john@example.com"
        assert student.program == "Computer Science"

    def test_to_dict_from_dict_roundtrip(self):
        """Test that to_dict and from_dict are inverses."""
        original = Student("S001", "John Doe", "john@example.com", "CS")
        data = original.to_dict()
        restored = Student.from_dict(data)

        assert restored.student_id == original.student_id
        assert restored.name == original.name
        assert restored.email == original.email
        assert restored.program == original.program


class TestStudentStringRepresentation:
    """Tests for Student string representation."""

    def test_str_representation(self):
        """Test __str__ method returns readable format."""
        student = Student("S001", "John Doe", "john@example.com", "CS")
        str_repr = str(student)

        assert "S001" in str_repr
        assert "John Doe" in str_repr

    def test_repr_representation(self):
        """Test __repr__ method returns developer-friendly format."""
        student = Student("S001", "John Doe", "john@example.com", "CS")
        repr_str = repr(student)

        assert "Student" in repr_str
        assert "S001" in repr_str


class TestStudentEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_long_name(self):
        """Test student with very long name."""
        long_name = "A" * 100
        student = Student("S001", long_name, "john@example.com", "CS")
        assert student.name == long_name

    def test_special_characters_in_name(self):
        """Test name with special characters."""
        names = ["O'Brien", "José García", "Anne-Marie", "李明"]  # Chinese characters
        for name in names:
            student = Student("S001", name, "john@example.com", "CS")
            assert student.name == name

    def test_case_sensitivity_in_id(self):
        """Test that student IDs are case-sensitive."""
        student1 = Student("s001", "John Doe", "john@example.com", "CS")
        student2 = Student("S001", "Jane Doe", "jane@example.com", "CS")
        assert student1.student_id != student2.student_id

    def test_equality_not_implemented(self):
        """Test that students with same data are different objects."""
        student1 = Student("S001", "John Doe", "john@example.com", "CS")
        student2 = Student("S001", "John Doe", "john@example.com", "CS")
        # They should be different objects (unless __eq__ is implemented)
        assert student1 is not student2
