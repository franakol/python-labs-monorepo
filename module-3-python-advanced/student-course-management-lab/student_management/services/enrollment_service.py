"""
Enrollment service module.

This module provides the EnrollmentService class which contains the business logic
for managing enrollments, including enrolling students, assigning grades,
and generating reports.
"""

from typing import List, Optional
from student_management.data.file_handler import FileHandler
from student_management.models.enrollment import Enrollment
from student_management.services.student_service import StudentService
from student_management.services.course_service import CourseService


class EnrollmentService:
    """
    Service class for enrollment management.

    Handles business logic for enrollment operations and interacts with the
    FileHandler for data persistence. Requires StudentService and CourseService
    to validate references.
    """

    def __init__(
        self,
        file_handler: FileHandler,
        student_service: StudentService,
        course_service: CourseService,
    ) -> None:
        """
        Initialize the EnrollmentService.

        Args:
            file_handler: Instance of FileHandler for data persistence.
            student_service: Instance of StudentService for validation.
            course_service: Instance of CourseService for validation.
        """
        self.file_handler = file_handler
        self.student_service = student_service
        self.course_service = course_service
        self.enrollments = self.file_handler.load_enrollments()

    def _save(self) -> None:
        """Save the current list of enrollments to file."""
        self.file_handler.save_enrollments(self.enrollments)

    def enroll_student(self, student_id: str, course_code: str) -> Enrollment:
        """
        Enroll a student in a course.

        Args:
            student_id: The ID of the student.
            course_code: The code of the course.

        Returns:
            The created Enrollment object.

        Raises:
            ValueError: If student/course not found or already enrolled.
        """
        # Validate student exists
        if not self.student_service.get_student(student_id):
            raise ValueError(f"Student with ID {student_id} not found.")

        # Validate course exists
        if not self.course_service.get_course(course_code):
            raise ValueError(f"Course with code {course_code} not found.")

        # Check for duplicate enrollment
        for enrollment in self.enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.course_code == course_code
            ):
                raise ValueError(
                    f"Student {student_id} is already enrolled in {course_code}."
                )

        enrollment = Enrollment(student_id, course_code)
        errors = enrollment.validate()
        if errors:
            raise ValueError(f"Invalid enrollment data: {'; '.join(errors)}")

        self.enrollments.append(enrollment)
        self._save()
        return enrollment

    def assign_grade(
        self, student_id: str, course_code: str, grade: float
    ) -> Enrollment:
        """
        Assign a grade to a student for a course.

        Args:
            student_id: The ID of the student.
            course_code: The code of the course.
            grade: The numeric grade (0-100).

        Returns:
            The updated Enrollment object.

        Raises:
            ValueError: If enrollment not found or grade is invalid.
        """
        enrollment = self._get_enrollment(student_id, course_code)
        if not enrollment:
            raise ValueError(
                f"Student {student_id} is not enrolled in course {course_code}."
            )

        original_grade = enrollment.grade
        enrollment.grade = grade

        errors = enrollment.validate()
        if errors:
            enrollment.grade = original_grade
            raise ValueError(f"Invalid grade: {'; '.join(errors)}")

        self._save()
        return enrollment

    def unenroll_student(self, student_id: str, course_code: str) -> bool:
        """
        Unenroll a student from a course.

        Args:
            student_id: The ID of the student.
            course_code: The code of the course.

        Returns:
            True if unenrolled, False if enrollment not found.
        """
        enrollment = self._get_enrollment(student_id, course_code)
        if enrollment:
            self.enrollments.remove(enrollment)
            self._save()
            return True
        return False

    def get_student_enrollments(self, student_id: str) -> List[Enrollment]:
        """
        Get all enrollments for a student.

        Args:
            student_id: The ID of the student.

        Returns:
            List of Enrollment objects.
        """
        return [e for e in self.enrollments if e.student_id == student_id]

    def get_course_enrollments(self, course_code: str) -> List[Enrollment]:
        """
        Get all enrollments for a course.

        Args:
            course_code: The code of the course.

        Returns:
            List of Enrollment objects.
        """
        return [e for e in self.enrollments if e.course_code == course_code]

    def get_student_gpa(self, student_id: str) -> float:
        """
        Calculate the average grade (GPA) for a student.

        Args:
            student_id: The ID of the student.

        Returns:
            Average grade as a float, or 0.0 if no graded enrollments.
        """
        enrollments = self.get_student_enrollments(student_id)
        graded_enrollments = [e for e in enrollments if e.grade is not None]

        if not graded_enrollments:
            return 0.0

        total = sum(e.grade for e in graded_enrollments)  # type: ignore
        return total / len(graded_enrollments)

    def get_course_average(self, course_code: str) -> float:
        """
        Calculate the average grade for a course.

        Args:
            course_code: The code of the course.

        Returns:
            Average grade as a float, or 0.0 if no graded enrollments.
        """
        enrollments = self.get_course_enrollments(course_code)
        graded_enrollments = [e for e in enrollments if e.grade is not None]

        if not graded_enrollments:
            return 0.0

        total = sum(e.grade for e in graded_enrollments)  # type: ignore
        return total / len(graded_enrollments)

    def _get_enrollment(
        self, student_id: str, course_code: str
    ) -> Optional[Enrollment]:
        """Helper to find an enrollment."""
        for enrollment in self.enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.course_code == course_code
            ):
                return enrollment
        return None
