"""
Student model module.

This module defines the Student class which represents a student
in the course management system.
"""

import re
from typing import Dict, List, Any


class Student:
    """
    Represents a student in the system.

    A student has a unique ID, name, email address, and is enrolled
    in an academic program.

    Attributes:
        student_id (str): Unique identifier for the student
        name (str): Student's full name
        email (str): Student's email address
        program (str): Academic program the student is enrolled in

    Example:
        >>> student = Student("S001", "John Doe", "john@example.com", "CS")
        >>> student.student_id
        'S001'
        >>> errors = student.validate()
        >>> len(errors)
        0
    """

    def __init__(self, student_id: str, name: str, email: str, program: str) -> None:
        """
        Initialize a new Student instance.

        Args:
            student_id: Unique student identifier
            name: Student's full name
            email: Student's email address
            program: Academic program name
        """
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program

    def validate(self) -> List[str]:
        """
        Validate the student data.

        Checks that all required fields are present and properly formatted.
        Email must be in valid email format.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> student = Student("", "John", "invalid", "CS")
            >>> errors = student.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Validate student_id
        if not self.student_id or not self.student_id.strip():
            errors.append("Student ID is required and cannot be empty")

        # Validate name
        if not self.name or not self.name.strip():
            errors.append("Name is required and cannot be empty")

        # Validate email
        if not self.email or not self.email.strip():
            errors.append("Email is required and cannot be empty")
        elif not self._is_valid_email(self.email):
            errors.append("Email format is invalid")

        # Validate program
        if not self.program or not self.program.strip():
            errors.append("Program is required and cannot be empty")

        return errors

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Check if email has valid format.

        Args:
            email: Email string to validate

        Returns:
            True if email format is valid, False otherwise
        """
        # Simple email regex pattern
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert student to dictionary representation.

        Returns:
            Dictionary containing all student attributes

        Example:
            >>> student = Student("S001", "John", "john@example.com", "CS")
            >>> data = student.to_dict()
            >>> data['student_id']
            'S001'
        """
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "program": self.program,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        Create a Student instance from a dictionary.

        Args:
            data: Dictionary containing student data with keys:
                  student_id, name, email, program

        Returns:
            New Student instance

        Example:
            >>> data = {"student_id": "S001", "name": "John",
            ...         "email": "john@example.com", "program": "CS"}
            >>> student = Student.from_dict(data)
            >>> student.student_id
            'S001'
        """
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            program=data["program"],
        )

    def __str__(self) -> str:
        """
        Return human-readable string representation.

        Returns:
            Formatted string with student info
        """
        return f"Student({self.student_id}: {self.name} - {self.program})"

    def __repr__(self) -> str:
        """
        Return developer-friendly string representation.

        Returns:
            String that could recreate the object
        """
        return (
            f"Student(student_id='{self.student_id}', "
            f"name='{self.name}', email='{self.email}', "
            f"program='{self.program}')"
        )
