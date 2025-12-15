"""
Course model module.

This module defines the Course class which represents a course
in the course management system.
"""

import re
from typing import Dict, List, Any


class Course:
    """
    Represents a course in the system.

    A course has a unique code, name, number of credits, and an instructor.

    Attributes:
        course_code (str): Unique identifier for the course (format: XXX1234)
        name (str): Course name
        credits (int): Number of credit hours (1-6)
        instructor (str): Name of the course instructor

    Example:
        >>> course = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
        >>> course.course_code
        'CSC1234'
        >>> errors = course.validate()
        >>> len(errors)
        0
    """

    def __init__(
        self, course_code: str, name: str, credits: int, instructor: str
    ) -> None:
        """
        Initialize a new Course instance.

        Args:
            course_code: Unique course identifier (format: XXX1234)
            name: Course name
            credits: Number of credit hours (1-6)
            instructor: Instructor's name
        """
        self.course_code = course_code
        self.name = name
        self.credits = credits
        self.instructor = instructor

    def validate(self) -> List[str]:
        """
        Validate the course data.

        Checks that all required fields are present and properly formatted.
        Course code must be in format XXX1234 (three uppercase letters, four digits).
        Credits must be between 1 and 6.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> course = Course("INVALID", "Test", 0, "")
            >>> errors = course.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Validate course_code
        if not self.course_code or not self.course_code.strip():
            errors.append("Course code is required and cannot be empty")
        elif not self._is_valid_course_code(self.course_code):
            errors.append(
                "Course code must be in format XXX1234 "
                "(three uppercase letters followed by four digits)"
            )

        # Validate name
        if not self.name or not self.name.strip():
            errors.append("Course name is required and cannot be empty")

        # Validate credits
        if not isinstance(self.credits, int):
            errors.append("Credits must be an integer")
        elif not (1 <= self.credits <= 6):
            errors.append("Credits must be between 1 and 6")

        # Validate instructor
        if not self.instructor or not self.instructor.strip():
            errors.append("Instructor name is required and cannot be empty")

        return errors

    @staticmethod
    def _is_valid_course_code(code: str) -> bool:
        """
        Check if course code has valid format.

        Format: Three uppercase letters followed by four digits (e.g., CSC1234)

        Args:
            code: Course code string to validate

        Returns:
            True if code format is valid, False otherwise
        """
        pattern = r"^[A-Z]{3}\d{4}$"
        return bool(re.match(pattern, code))

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert course to dictionary representation.

        Returns:
            Dictionary containing all course attributes

        Example:
            >>> course = Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")
            >>> data = course.to_dict()
            >>> data['course_code']
            'CSC1234'
        """
        return {
            "course_code": self.course_code,
            "name": self.name,
            "credits": self.credits,
            "instructor": self.instructor,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Course":
        """
        Create a Course instance from a dictionary.

        Args:
            data: Dictionary containing course data with keys:
                  course_code, name, credits, instructor

        Returns:
            New Course instance

        Example:
            >>> data = {"course_code": "CSC1234", "name": "Intro to Programming",
            ...         "credits": 3, "instructor": "Dr. Smith"}
            >>> course = Course.from_dict(data)
            >>> course.course_code
            'CSC1234'
        """
        return cls(
            course_code=data["course_code"],
            name=data["name"],
            credits=data["credits"],
            instructor=data["instructor"],
        )

    def __str__(self) -> str:
        """
        Return human-readable string representation.

        Returns:
            Formatted string with course info
        """
        return f"Course({self.course_code}: {self.name} - {self.credits} credits)"

    def __repr__(self) -> str:
        """
        Return developer-friendly string representation.

        Returns:
            String that could recreate the object
        """
        return (
            f"Course(course_code='{self.course_code}', "
            f"name='{self.name}', credits={self.credits}, "
            f"instructor='{self.instructor}')"
        )
