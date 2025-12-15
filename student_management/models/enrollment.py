"""
Enrollment model module.

This module defines the Enrollment class which represents a student's
enrollment in a course, including grade information.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional


class Enrollment:
    """
    Represents a student's enrollment in a course.

    An enrollment links a student to a course and optionally includes
    a grade. It tracks when the enrollment was created.

    Attributes:
        student_id (str): Reference to the student
        course_code (str): Reference to the course
        grade (Optional[float]): Numeric grade (0-100), None if not yet graded
        enrollment_date (datetime): When the enrollment was created

    Example:
        >>> enrollment = Enrollment("S001", "CSC1234", grade=85.5)
        >>> enrollment.calculate_letter_grade()
        'A'
        >>> errors = enrollment.validate()
        >>> len(errors)
        0
    """

    def __init__(
        self,
        student_id: str,
        course_code: str,
        grade: Optional[float] = None,
        enrollment_date: Optional[datetime] = None,
    ) -> None:
        """
        Initialize a new Enrollment instance.

        Args:
            student_id: ID of the enrolled student
            course_code: Code of the course
            grade: Numeric grade (0-100), optional
            enrollment_date: Date of enrollment, defaults to current time
        """
        self.student_id = student_id
        self.course_code = course_code
        self.grade = grade
        self.enrollment_date = enrollment_date or datetime.now()

    def validate(self) -> List[str]:
        """
        Validate the enrollment data.

        Checks that student_id and course_code are present.
        If grade is set, it must be between 0 and 100.

        Returns:
            List of validation error messages. Empty list if valid.

        Example:
            >>> enrollment = Enrollment("", "CSC1234", grade=150)
            >>> errors = enrollment.validate()
            >>> len(errors) > 0
            True
        """
        errors = []

        # Validate student_id
        if not self.student_id or not self.student_id.strip():
            errors.append("Student ID is required and cannot be empty")

        # Validate course_code
        if not self.course_code or not self.course_code.strip():
            errors.append("Course code is required and cannot be empty")

        # Validate grade (if present)
        if self.grade is not None:
            if not isinstance(self.grade, (int, float)):
                errors.append("Grade must be a number")
            elif not (0 <= self.grade <= 100):
                errors.append("Grade must be between 0 and 100")

        return errors

    def calculate_letter_grade(self) -> str:
        """
        Convert numeric grade to letter grade.

        Grading scale:
        - A+: 90-100
        - A:  85-89
        - B+: 80-84
        - B:  75-79
        - C+: 70-74
        - C:  65-69
        - D+: 60-64
        - D:  55-59
        - F:  0-54
        - N/A: No grade set

        Returns:
            Letter grade string

        Example:
            >>> enrollment = Enrollment("S001", "CSC1234", grade=85)
            >>> enrollment.calculate_letter_grade()
            'A'
        """
        if self.grade is None:
            return "N/A"

        if self.grade >= 90:
            return "A+"
        elif self.grade >= 85:
            return "A"
        elif self.grade >= 80:
            return "B+"
        elif self.grade >= 75:
            return "B"
        elif self.grade >= 70:
            return "C+"
        elif self.grade >= 65:
            return "C"
        elif self.grade >= 60:
            return "D+"
        elif self.grade >= 55:
            return "D"
        else:
            return "F"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert enrollment to dictionary representation.

        Returns:
            Dictionary containing all enrollment attributes

        Example:
            >>> enrollment = Enrollment("S001", "CSC1234", grade=85.5)
            >>> data = enrollment.to_dict()
            >>> data['grade']
            85.5
        """
        return {
            "student_id": self.student_id,
            "course_code": self.course_code,
            "grade": self.grade,
            "enrollment_date": self.enrollment_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Enrollment":
        """
        Create an Enrollment instance from a dictionary.

        Args:
            data: Dictionary containing enrollment data with keys:
                  student_id, course_code, grade, enrollment_date

        Returns:
            New Enrollment instance

        Example:
            >>> data = {"student_id": "S001", "course_code": "CSC1234",
            ...         "grade": 85.5, "enrollment_date": "2024-01-15T10:30:00"}
            >>> enrollment = Enrollment.from_dict(data)
            >>> enrollment.grade
            85.5
        """
        enrollment_date = None
        if "enrollment_date" in data:
            # Handle ISO format string
            if isinstance(data["enrollment_date"], str):
                enrollment_date = datetime.fromisoformat(data["enrollment_date"])
            else:
                enrollment_date = data["enrollment_date"]

        return cls(
            student_id=data["student_id"],
            course_code=data["course_code"],
            grade=data.get("grade"),
            enrollment_date=enrollment_date,
        )

    def __str__(self) -> str:
        """
        Return human-readable string representation.

        Returns:
            Formatted string with enrollment info
        """
        grade_str = (
            f"{self.grade} ({self.calculate_letter_grade()})"
            if self.grade is not None
            else "Not graded"
        )
        return f"Enrollment({self.student_id} in {self.course_code}: {grade_str})"

    def __repr__(self) -> str:
        """
        Return developer-friendly string representation.

        Returns:
            String that could recreate the object
        """
        return (
            f"Enrollment(student_id='{self.student_id}', "
            f"course_code='{self.course_code}', grade={self.grade}, "
            f"enrollment_date={self.enrollment_date!r})"
        )
