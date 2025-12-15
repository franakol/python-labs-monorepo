"""
File handler module for data persistence.

This module provides the FileHandler class which manages reading and writing
student, course, and enrollment data to JSON files.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from student_management.models.student import Student
from student_management.models.course import Course
from student_management.models.enrollment import Enrollment


class FileHandler:
    """
    Handles file I/O operations for the student management system.

    Manages reading and writing data for students, courses, and enrollments
    to JSON files. Provides backup functionality and error handling.

    Attributes:
        data_dir (Path): Directory where data files are stored

    Example:
        >>> handler = FileHandler(Path("data"))
        >>> students = handler.load_students()
        >>> handler.save_students(students)
    """

    def __init__(self, data_dir: Path = Path("data")) -> None:
        """
        Initialize the FileHandler.

        Args:
            data_dir: Directory for data files. Created if it doesn't exist.
        """
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_students(self) -> List[Student]:
        """
        Load students from JSON file.

        Returns:
            List of Student objects. Empty list if file doesn't exist.

        Raises:
            json.JSONDecodeError: If file contains invalid JSON

        Example:
            >>> handler = FileHandler()
            >>> students = handler.load_students()
            >>> len(students)
            2
        """
        file_path = self.data_dir / "students.json"

        if not file_path.exists():
            return []

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            students = [Student.from_dict(s) for s in data.get("students", [])]
            return students
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in {file_path}: {e}")

    def save_students(self, students: List[Student]) -> None:
        """
        Save students to JSON file.

        Args:
            students: List of Student objects to save

        Example:
            >>> handler = FileHandler()
            >>> students = [Student("S001", "John", "john@example.com", "CS")]
            >>> handler.save_students(students)
        """
        file_path = self.data_dir / "students.json"

        data = {
            "students": [s.to_dict() for s in students],
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "count": len(students),
            },
        }

        file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def load_courses(self) -> List[Course]:
        """
        Load courses from JSON file.

        Returns:
            List of Course objects. Empty list if file doesn't exist.

        Raises:
            json.JSONDecodeError: If file contains invalid JSON

        Example:
            >>> handler = FileHandler()
            >>> courses = handler.load_courses()
        """
        file_path = self.data_dir / "courses.json"

        if not file_path.exists():
            return []

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            courses = [Course.from_dict(c) for c in data.get("courses", [])]
            return courses
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in {file_path}: {e}")

    def save_courses(self, courses: List[Course]) -> None:
        """
        Save courses to JSON file.

        Args:
            courses: List of Course objects to save

        Example:
            >>> handler = FileHandler()
            >>> courses = [Course("CSC1234", "Intro to Programming", 3, "Dr. Smith")]
            >>> handler.save_courses(courses)
        """
        file_path = self.data_dir / "courses.json"

        data = {
            "courses": [c.to_dict() for c in courses],
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "count": len(courses),
            },
        }

        file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def load_enrollments(self) -> List[Enrollment]:
        """
        Load enrollments from JSON file.

        Returns:
            List of Enrollment objects. Empty list if file doesn't exist.

        Raises:
            json.JSONDecodeError: If file contains invalid JSON

        Example:
            >>> handler = FileHandler()
            >>> enrollments = handler.load_enrollments()
        """
        file_path = self.data_dir / "enrollments.json"

        if not file_path.exists():
            return []

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            enrollments = [Enrollment.from_dict(e) for e in data.get("enrollments", [])]
            return enrollments
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in {file_path}: {e}")

    def save_enrollments(self, enrollments: List[Enrollment]) -> None:
        """
        Save enrollments to JSON file.

        Args:
            enrollments: List of Enrollment objects to save

        Example:
            >>> handler = FileHandler()
            >>> enrollments = [Enrollment("S001", "CSC1234", grade=85.5)]
            >>> handler.save_enrollments(enrollments)
        """
        file_path = self.data_dir / "enrollments.json"

        data = {
            "enrollments": [e.to_dict() for e in enrollments],
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "count": len(enrollments),
            },
        }

        file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def create_backup(self, file_type: str) -> Optional[Path]:
        """
        Create a backup of a data file.

        Creates a timestamped backup copy of the specified data file.

        Args:
            file_type: Type of file to backup ("students", "courses", "enrollments")

        Returns:
            Path to the backup file, or None if source file doesn't exist

        Example:
            >>> handler = FileHandler()
            >>> backup_path = handler.create_backup("students")
            >>> backup_path.exists()
            True
        """
        file_map = {
            "students": "students.json",
            "courses": "courses.json",
            "enrollments": "enrollments.json",
        }

        if file_type not in file_map:
            raise ValueError(f"Invalid file type: {file_type}")

        source_file = self.data_dir / file_map[file_type]

        if not source_file.exists():
            return None

        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_type}_{timestamp}.bak"
        backup_path = self.data_dir / backup_name

        shutil.copy2(source_file, backup_path)

        return backup_path
