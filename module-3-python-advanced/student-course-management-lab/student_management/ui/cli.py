"""
Command-Line Interface module.

This module provides the CLI class which handles user interaction,
menu navigation, and calls to the underlying services.
"""

from typing import Optional
from student_management.services.student_service import StudentService
from student_management.services.course_service import CourseService
from student_management.services.enrollment_service import EnrollmentService


class CLI:
    """
    Command-Line Interface for the Student Course Management System.
    """

    def __init__(
        self,
        student_service: StudentService,
        course_service: CourseService,
        enrollment_service: EnrollmentService,
    ) -> None:
        """
        Initialize the CLI.

        Args:
            student_service: Service for student operations.
            course_service: Service for course operations.
            enrollment_service: Service for enrollment operations.
        """
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service

    def run(self) -> None:
        """Start the CLI main loop."""
        while True:
            self._show_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self._handle_student_menu()
            elif choice == "2":
                self._handle_course_menu()
            elif choice == "3":
                self._handle_enrollment_menu()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def _show_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n=== Student Course Management System ===")
        print("1. Manage Students")
        print("2. Manage Courses")
        print("3. Manage Enrollments")
        print("0. Exit")

    def _handle_student_menu(self) -> None:
        """Handle student management operations."""
        while True:
            print("\n--- Student Management ---")
            print("1. Add Student")
            print("2. List Students")
            print("3. Search Students")
            print("0. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._list_students()
            elif choice == "3":
                self._search_students()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_student(self) -> None:
        """Prompt user for student details and create student."""
        print("\nAdding New Student")
        student_id = input("Enter Student ID: ").strip()
        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()
        program = input("Enter Program: ").strip()

        try:
            self.student_service.create_student(student_id, name, email, program)
            print("Student added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def _list_students(self) -> None:
        """List all students."""
        print("\nList of Students:")
        students = self.student_service.list_students()
        if not students:
            print("No students found.")
        else:
            for student in students:
                print(student)

    def _search_students(self) -> None:
        """Search for students."""
        print("\nSearch Students")
        name = input("Enter Name (leave empty to skip): ").strip() or None
        program = input("Enter Program (leave empty to skip): ").strip() or None

        results = self.student_service.search_students(name=name, program=program)
        if not results:
            print("No matching students found.")
        else:
            for student in results:
                print(student)

    def _handle_course_menu(self) -> None:
        """Handle course management operations."""
        while True:
            print("\n--- Course Management ---")
            print("1. Add Course")
            print("2. List Courses")
            print("3. Search Courses")
            print("0. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self._add_course()
            elif choice == "2":
                self._list_courses()
            elif choice == "3":
                self._search_courses()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_course(self) -> None:
        """Prompt user for course details and create course."""
        print("\nAdding New Course")
        course_code = input("Enter Course Code: ").strip()
        name = input("Enter Course Name: ").strip()

        while True:
            try:
                credits_str = input("Enter Credits: ").strip()
                credits = int(credits_str)
                break
            except ValueError:
                print("Error: Credits must be a number.")

        instructor = input("Enter Instructor Name: ").strip()

        try:
            self.course_service.create_course(course_code, name, credits, instructor)
            print("Course added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def _list_courses(self) -> None:
        """List all courses."""
        print("\nList of Courses:")
        courses = self.course_service.list_courses()
        if not courses:
            print("No courses found.")
        else:
            for course in courses:
                print(course)

    def _search_courses(self) -> None:
        """Search for courses."""
        print("\nSearch Courses")
        code = input("Enter Code (leave empty to skip): ").strip() or None
        name = input("Enter Name (leave empty to skip): ").strip() or None
        instructor = input("Enter Instructor (leave empty to skip): ").strip() or None

        results = self.course_service.search_courses(
            course_code=code, name=name, instructor=instructor
        )
        if not results:
            print("No matching courses found.")
        else:
            for course in results:
                print(course)

    def _handle_enrollment_menu(self) -> None:
        """Handle enrollment management operations."""
        while True:
            print("\n--- Enrollment Management ---")
            print("1. Enroll Student")
            print("2. Assign Grade")
            print("3. View Student Enrollments")
            print("0. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self._enroll_student()
            elif choice == "2":
                self._assign_grade()
            elif choice == "3":
                self._view_enrollments()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

    def _enroll_student(self) -> None:
        """Enroll a student in a course."""
        print("\nEnroll Student")
        student_id = input("Enter Student ID: ").strip()
        course_code = input("Enter Course Code: ").strip()

        try:
            self.enrollment_service.enroll_student(student_id, course_code)
            print("Student enrolled successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def _assign_grade(self) -> None:
        """Assign a grade to an enrollment."""
        print("\nAssign Grade")
        student_id = input("Enter Student ID: ").strip()
        course_code = input("Enter Course Code: ").strip()

        while True:
            try:
                grade_str = input("Enter Grade (0-100): ").strip()
                grade = float(grade_str)
                break
            except ValueError:
                print("Error: Grade must be a number.")

        try:
            self.enrollment_service.assign_grade(student_id, course_code, grade)
            print("Grade assigned successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def _view_enrollments(self) -> None:
        """View enrollments for a student."""
        print("\nView Enrollments")
        student_id = input("Enter Student ID: ").strip()

        enrollments = self.enrollment_service.get_student_enrollments(student_id)
        if not enrollments:
            print("No enrollments found for this student.")
        else:
            print(f"Enrollments for {student_id}:")
            for enrollment in enrollments:
                print(enrollment)

            gpa = self.enrollment_service.get_student_gpa(student_id)
            print(f"GPA: {gpa:.2f}")
