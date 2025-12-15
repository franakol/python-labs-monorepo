"""
Student service module.

This module provides the StudentService class which contains the business logic
for managing students, including creation, retrieval, updates, and deletion.
"""

from typing import List, Optional
from student_management.data.file_handler import FileHandler
from student_management.models.student import Student


class StudentService:
    """
    Service class for student management.

    Handles business logic for student operations and interacts with the
    FileHandler for data persistence.
    """

    def __init__(self, file_handler: FileHandler) -> None:
        """
        Initialize the StudentService.

        Args:
            file_handler: Instance of FileHandler for data persistence.
        """
        self.file_handler = file_handler
        self.students = self.file_handler.load_students()

    def _save(self) -> None:
        """Save the current list of students to file."""
        self.file_handler.save_students(self.students)

    def create_student(
        self, student_id: str, name: str, email: str, program: str
    ) -> Student:
        """
        Create a new student.

        Args:
            student_id: Unique student ID.
            name: Student's full name.
            email: Student's email address.
            program: Student's academic program.

        Returns:
            The created Student object.

        Raises:
            ValueError: If student_id already exists or data is invalid.
        """
        if self.get_student(student_id):
            raise ValueError(f"Student with ID {student_id} already exists.")

        student = Student(student_id, name, email, program)
        errors = student.validate()
        if errors:
            raise ValueError(f"Invalid student data: {'; '.join(errors)}")

        self.students.append(student)
        self._save()
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        """
        Retrieve a student by ID.

        Args:
            student_id: The ID of the student to retrieve.

        Returns:
            The Student object if found, else None.
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def list_students(self) -> List[Student]:
        """
        List all students.

        Returns:
            A list of all Student objects.
        """
        return list(self.students)

    def update_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        program: Optional[str] = None,
    ) -> Student:
        """
        Update an existing student's information.

        Args:
            student_id: The ID of the student to update.
            name: New name (optional).
            email: New email (optional).
            program: New program (optional).

        Returns:
            The updated Student object.

        Raises:
            ValueError: If student is not found or new data is invalid.
        """
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found.")

        original_name = student.name
        original_email = student.email
        original_program = student.program

        if name is not None:
            student.name = name
        if email is not None:
            student.email = email
        if program is not None:
            student.program = program

        errors = student.validate()
        if errors:
            # Revert changes if validation fails
            student.name = original_name
            student.email = original_email
            student.program = original_program
            raise ValueError(f"Invalid update data: {'; '.join(errors)}")

        self._save()
        return student

    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student by ID.

        Args:
            student_id: The ID of the student to delete.

        Returns:
            True if student was deleted, False if not found.
        """
        student = self.get_student(student_id)
        if student:
            self.students.remove(student)
            self._save()
            return True
        return False

    def search_students(
        self, name: Optional[str] = None, program: Optional[str] = None
    ) -> List[Student]:
        """
        Search for students by name or program.

        Args:
            name: Partial name to search for (case-insensitive).
            program: Exact program match (case-sensitive).

        Returns:
            List of matching Student objects.
        """
        results = self.students

        if name:
            name_lower = name.lower()
            results = [s for s in results if name_lower in s.name.lower()]

        if program:
            results = [s for s in results if s.program == program]

        return results
