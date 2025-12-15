"""
Command-Line Interface for the Employee Payroll Tracker.
"""

from employee_payroll.services.payroll_service import PayrollService
from employee_payroll.models.full_time_employee import FullTimeEmployee
from employee_payroll.models.part_time_employee import PartTimeEmployee
from employee_payroll.models.intern import Intern


class CLI:
    """Command-Line Interface for the Employee Payroll Tracker."""

    def __init__(self, payroll_service: PayrollService) -> None:
        """Initialize the CLI."""
        self.payroll_service = payroll_service

    def run(self) -> None:
        """Start the CLI main loop."""
        print("\n" + "=" * 50)
        print("Employee Payroll Tracker".center(50))
        print("=" * 50)

        while True:
            self._show_main_menu()
            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self._add_employee()
            elif choice == "2":
                self._view_all_employees()
            elif choice == "3":
                self._generate_payroll_report()
            elif choice == "4":
                self._save_data()
            elif choice == "0":
                self._exit()
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def _show_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "-" * 50)
        print("Main Menu")
        print("-" * 50)
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Generate Payroll Report")
        print("4. Save Data")
        print("0. Exit")
        print("-" * 50)

    def _add_employee(self) -> None:
        """Prompt user to add a new employee."""
        print("\n--- Add New Employee ---")
        print("1. Full-Time Employee")
        print("2. Part-Time Employee")
        print("3. Intern")

        emp_type = input("Enter type (1-3): ").strip()

        try:
            employee_id = input("Employee ID: ").strip()
            name = input("Name: ").strip()
            email = input("Email: ").strip()

            if emp_type == "1":
                monthly_salary = float(input("Monthly Salary: $").strip())
                benefits = float(input("Benefits (0 if none): $").strip() or "0")
                employee = FullTimeEmployee(
                    employee_id, name, email, monthly_salary, benefits
                )
            elif emp_type == "2":
                hourly_rate = float(input("Hourly Rate: $").strip())
                hours_worked = float(input("Hours Worked: ").strip())
                employee = PartTimeEmployee(
                    employee_id, name, email, hourly_rate, hours_worked
                )
            elif emp_type == "3":
                stipend = float(input("Monthly Stipend: $").strip())
                employee = Intern(employee_id, name, email, stipend)
            else:
                print("❌ Invalid employee type.")
                return

            self.payroll_service.add_employee(employee)
            print(f"✅ Employee {name} added successfully!")

        except ValueError as e:
            print(f"❌ Error: {e}")

    def _view_all_employees(self) -> None:
        """Display all employees."""
        print("\n--- All Employees ---")
        employees = self.payroll_service.get_all_employees()

        if not employees:
            print("No employees in the system.")
            return

        for emp in employees:
            pay = emp.calculate_pay()
            print(f"\n{emp}")
            print(f"  Net Pay: ${pay:,.2f}")

    def _generate_payroll_report(self) -> None:
        """Generate and display the payroll report."""
        print()
        report = self.payroll_service.generate_payroll_report()
        print(report)

    def _save_data(self) -> None:
        """Save employee data to file."""
        try:
            self.payroll_service.save_employees()
            print(f"✅ Data saved to {self.payroll_service.data_file}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def _exit(self) -> None:
        """Exit the application."""
        save = input("\nSave before exiting? (y/n): ").strip().lower()
        if save == "y":
            self._save_data()
        print("\nThank you for using Employee Payroll Tracker! 👋\n")


def main() -> None:
    """Main entry point for the application."""
    payroll_service = PayrollService()
    cli = CLI(payroll_service)
    cli.run()


if __name__ == "__main__":
    main()
