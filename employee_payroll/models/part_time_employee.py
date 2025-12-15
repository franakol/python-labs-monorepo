"""
Part-time employee implementation.
"""

from employee_payroll.models.employee import Employee


class PartTimeEmployee(Employee):
    """
    Part-time employee paid by the hour.

    Attributes:
        hourly_rate: Pay rate per hour.
        hours_worked: Number of hours worked in the pay period.
    """

    def __init__(
        self,
        employee_id: str,
        name: str,
        email: str,
        hourly_rate: float,
        hours_worked: float = 0.0,
    ) -> None:
        """Initialize a PartTimeEmployee."""
        super().__init__(employee_id, name, email)

        if hourly_rate < 0:
            raise ValueError("Hourly rate cannot be negative")
        if hours_worked < 0:
            raise ValueError("Hours worked cannot be negative")

        self._hourly_rate = hourly_rate
        self._hours_worked = hours_worked

    @property
    def hourly_rate(self) -> float:
        """Get the hourly rate."""
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float) -> None:
        """Set the hourly rate."""
        if value < 0:
            raise ValueError("Hourly rate cannot be negative")
        self._hourly_rate = value

    @property
    def hours_worked(self) -> float:
        """Get the hours worked."""
        return self._hours_worked

    @hours_worked.setter
    def hours_worked(self, value: float) -> None:
        """Set the hours worked."""
        if value < 0:
            raise ValueError("Hours worked cannot be negative")
        self._hours_worked = value

    def calculate_pay(self) -> float:
        """Calculate pay: (hourly_rate * hours_worked) * 0.85 (15% tax)."""
        gross_pay = self._hourly_rate * self._hours_worked
        tax = gross_pay * 0.15
        return gross_pay - tax

    def __str__(self) -> str:
        """Return string representation."""
        return f"PartTimeEmployee(ID: {self.employee_id}, Name: {self.name}, Rate: ${self.hourly_rate:.2f}/hr)"
