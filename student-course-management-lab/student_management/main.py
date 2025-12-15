"""
Main entry point for the Student Course Management System.
"""

import sys
from pathlib import Path
from student_management.data.file_handler import FileHandler
from student_management.services.student_service import StudentService
from student_management.services.course_service import CourseService
from student_management.services.enrollment_service import EnrollmentService
from student_management.ui.cli import CLI


def main() -> None:
    """Initialize and run the application."""
    # Set up data directory
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    # Initialize components
    try:
        file_handler = FileHandler(data_dir)

        student_service = StudentService(file_handler)
        course_service = CourseService(file_handler)
        enrollment_service = EnrollmentService(
            file_handler, student_service, course_service
        )

        cli = CLI(student_service, course_service, enrollment_service)

        # Run application
        cli.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
