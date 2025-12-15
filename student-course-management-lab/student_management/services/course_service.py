"""
Course service module.

This module provides the CourseService class which contains the business logic
for managing courses, including creation, retrieval, updates, and deletion.
"""

from typing import List, Optional
from student_management.data.file_handler import FileHandler
from student_management.models.course import Course


class CourseService:
    """
    Service class for course management.

    Handles business logic for course operations and interacts with the
    FileHandler for data persistence.
    """

    def __init__(self, file_handler: FileHandler) -> None:
        """
        Initialize the CourseService.

        Args:
            file_handler: Instance of FileHandler for data persistence.
        """
        self.file_handler = file_handler
        self.courses = self.file_handler.load_courses()

    def _save(self) -> None:
        """Save the current list of courses to file."""
        self.file_handler.save_courses(self.courses)

    def create_course(
        self, course_code: str, name: str, credits: int, instructor: str
    ) -> Course:
        """
        Create a new course.

        Args:
            course_code: Unique course code (e.g., "CSC1234").
            name: Course name.
            credits: Number of credits (1-6).
            instructor: Instructor's name.

        Returns:
            The created Course object.

        Raises:
            ValueError: If course_code already exists or data is invalid.
        """
        if self.get_course(course_code):
            raise ValueError(f"Course with code {course_code} already exists.")

        course = Course(course_code, name, credits, instructor)
        errors = course.validate()
        if errors:
            raise ValueError(f"Invalid course data: {'; '.join(errors)}")

        self.courses.append(course)
        self._save()
        return course

    def get_course(self, course_code: str) -> Optional[Course]:
        """
        Retrieve a course by code.

        Args:
            course_code: The code of the course to retrieve.

        Returns:
            The Course object if found, else None.
        """
        for course in self.courses:
            if course.course_code == course_code:
                return course
        return None

    def list_courses(self) -> List[Course]:
        """
        List all courses.

        Returns:
            A list of all Course objects.
        """
        return list(self.courses)

    def update_course(
        self,
        course_code: str,
        name: Optional[str] = None,
        credits: Optional[int] = None,
        instructor: Optional[str] = None,
    ) -> Course:
        """
        Update an existing course's information.

        Args:
            course_code: The code of the course to update.
            name: New name (optional).
            credits: New credits (optional).
            instructor: New instructor (optional).

        Returns:
            The updated Course object.

        Raises:
            ValueError: If course is not found or new data is invalid.
        """
        course = self.get_course(course_code)
        if not course:
            raise ValueError(f"Course with code {course_code} not found.")

        original_name = course.name
        original_credits = course.credits
        original_instructor = course.instructor

        if name is not None:
            course.name = name
        if credits is not None:
            course.credits = credits
        if instructor is not None:
            course.instructor = instructor

        errors = course.validate()
        if errors:
            # Revert changes if validation fails
            course.name = original_name
            course.credits = original_credits
            course.instructor = original_instructor
            raise ValueError(f"Invalid update data: {'; '.join(errors)}")

        self._save()
        return course

    def delete_course(self, course_code: str) -> bool:
        """
        Delete a course by code.

        Args:
            course_code: The code of the course to delete.

        Returns:
            True if course was deleted, False if not found.
        """
        course = self.get_course(course_code)
        if course:
            self.courses.remove(course)
            self._save()
            return True
        return False

    def search_courses(
        self,
        course_code: Optional[str] = None,
        name: Optional[str] = None,
        instructor: Optional[str] = None,
    ) -> List[Course]:
        """
        Search for courses by code, name, or instructor.

        Args:
            course_code: Partial code to search for (case-insensitive).
            name: Partial name to search for (case-insensitive).
            instructor: Partial instructor name to search for (case-insensitive).

        Returns:
            List of matching Course objects.
        """
        results = self.courses

        if course_code:
            code_lower = course_code.lower()
            results = [c for c in results if code_lower in c.course_code.lower()]

        if name:
            name_lower = name.lower()
            results = [c for c in results if name_lower in c.name.lower()]

        if instructor:
            instructor_lower = instructor.lower()
            results = [c for c in results if instructor_lower in c.instructor.lower()]

        return results
