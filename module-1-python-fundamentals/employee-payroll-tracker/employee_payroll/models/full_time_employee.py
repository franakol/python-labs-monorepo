"""
Full-time employee implementation.
"""

from employee_payroll.models.employee import Employee


class FullTimeEmployee(Employee):
    """
    Full-time employee with monthly salary and benefits.

    Attributes:
        monthly_salary: Monthly gross salary.
        benefits: Additional benefits amount.
    """

    def __init__(
        self,
        employee_id: str,
        name: str,
        email: str,
        monthly_salary: float,
        benefits: float = 0.0,
    ) -> None:
        """Initialize a FullTimeEmployee."""
        super().__init__(employee_id, name, email)

        if monthly_salary < 0:
            raise ValueError("Monthly salary cannot be negative")
        if benefits < 0:
            raise ValueError("Benefits cannot be negative")

        self._monthly_salary = monthly_salary
        self._benefits = benefits

    @property
    def monthly_salary(self) -> float:
        """Get the monthly salary."""
        return self._monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value: float) -> None:
        """Set the monthly salary."""
        if value < 0:
            raise ValueError("Monthly salary cannot be negative")
        self._monthly_salary = value

    @property
    def benefits(self) -> float:
        """Get the benefits amount."""
        return self._benefits

    @benefits.setter
    def benefits(self, value: float) -> None:
        """Set the benefits amount."""
        if value < 0:
            raise ValueError("Benefits cannot be negative")
        self._benefits = value

    def calculate_pay(self) -> float:
        """Calculate pay: (monthly_salary + benefits) * 0.8 (20% tax)."""
        gross_pay = self._monthly_salary + self._benefits
        tax = gross_pay * 0.20
        return gross_pay - tax

    def __str__(self) -> str:
        """Return string representation."""
        return f"FullTimeEmployee(ID: {self.employee_id}, Name: {self.name}, Monthly: ${self.monthly_salary:.2f})"
