"""
Payroll Service.

This module handles employee management and payroll calculations.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from employee_payroll.models.employee import Employee
from employee_payroll.models.full_time_employee import FullTimeEmployee
from employee_payroll.models.part_time_employee import PartTimeEmployee
from employee_payroll.models.intern import Intern


class PayrollService:
    """Service for managing employees and calculating payroll."""

    def __init__(self, data_file: Optional[Path] = None) -> None:
        """Initialize the PayrollService."""
        self.employees: List[Employee] = []
        self.data_file = data_file or Path("data/employees.json")

        if self.data_file.exists():
            self.load_employees()

    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the payroll system."""
        if self.get_employee(employee.employee_id):
            raise ValueError(f"Employee with ID {employee.employee_id} already exists")
        self.employees.append(employee)

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get an employee by ID."""
        for emp in self.employees:
            if emp.employee_id == employee_id:
                return emp
        return None

    def remove_employee(self, employee_id: str) -> bool:
        """Remove an employee from the system."""
        employee = self.get_employee(employee_id)
        if employee:
            self.employees.remove(employee)
            return True
        return False

    def get_all_employees(self) -> List[Employee]:
        """Get all employees."""
        return self.employees.copy()

    def calculate_total_payroll(self) -> float:
        """Calculate total payroll for all employees."""
        return sum(emp.calculate_pay() for emp in self.employees)

    def generate_payroll_report(self) -> str:
        """Generate a formatted payroll report."""
        if not self.employees:
            return "No employees in the system."

        lines = ["=" * 80, "PAYROLL REPORT".center(80), "=" * 80, ""]

        for emp in self.employees:
            pay = emp.calculate_pay()
            lines.extend(
                [
                    f"ID: {emp.employee_id}",
                    f"Name: {emp.name}",
                    f"Type: {emp.__class__.__name__}",
                    f"Net Pay: ${pay:,.2f}",
                    "-" * 80,
                ]
            )

        lines.extend(
            ["", f"Total Payroll: ${self.calculate_total_payroll():,.2f}", "=" * 80]
        )
        return "\n".join(lines)

    def save_employees(self) -> None:
        """Save all employees to JSON file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = {"employees": [self._employee_to_dict(emp) for emp in self.employees]}
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_employees(self) -> None:
        """Load employees from JSON file."""
        if not self.data_file.exists():
            return
        with open(self.data_file, "r") as f:
            data = json.load(f)
        self.employees = [
            self._dict_to_employee(emp_data) for emp_data in data.get("employees", [])
        ]

    def _employee_to_dict(self, employee: Employee) -> Dict[str, Any]:
        """Convert an employee to a dictionary."""
        base_data = {
            "type": employee.__class__.__name__,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
        }

        if isinstance(employee, FullTimeEmployee):
            base_data.update(
                {
                    "monthly_salary": employee.monthly_salary,
                    "benefits": employee.benefits,
                }
            )
        elif isinstance(employee, PartTimeEmployee):
            base_data.update(
                {
                    "hourly_rate": employee.hourly_rate,
                    "hours_worked": employee.hours_worked,
                }
            )
        elif isinstance(employee, Intern):
            base_data.update({"stipend": employee.stipend})

        return base_data

    def _dict_to_employee(self, data: Dict[str, Any]) -> Employee:
        """Convert a dictionary to an employee object."""
        emp_type = data.get("type")
        employee_id, name, email = data["employee_id"], data["name"], data["email"]

        if emp_type == "FullTimeEmployee":
            return FullTimeEmployee(
                employee_id,
                name,
                email,
                data["monthly_salary"],
                data.get("benefits", 0.0),
            )
        elif emp_type == "PartTimeEmployee":
            return PartTimeEmployee(
                employee_id,
                name,
                email,
                data["hourly_rate"],
                data.get("hours_worked", 0.0),
            )
        elif emp_type == "Intern":
            return Intern(employee_id, name, email, data["stipend"])
        else:
            raise ValueError(f"Unknown employee type: {emp_type}")
