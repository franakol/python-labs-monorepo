"""
Intern employee implementation.
"""

from employee_payroll.models.employee import Employee


class Intern(Employee):
    """
    Intern employee with a fixed stipend.

    Attributes:
        stipend: Monthly stipend amount (no tax deduction).
    """

    def __init__(
        self,
        employee_id: str,
        name: str,
        email: str,
        stipend: float,
    ) -> None:
        """Initialize an Intern."""
        super().__init__(employee_id, name, email)

        if stipend < 0:
            raise ValueError("Stipend cannot be negative")

        self._stipend = stipend

    @property
    def stipend(self) -> float:
        """Get the stipend amount."""
        return self._stipend

    @stipend.setter
    def stipend(self, value: float) -> None:
        """Set the stipend amount."""
        if value < 0:
            raise ValueError("Stipend cannot be negative")
        self._stipend = value

    def calculate_pay(self) -> float:
        """Calculate pay: Full stipend with no tax deduction."""
        return self._stipend

    def __str__(self) -> str:
        """Return string representation."""
        return f"Intern(ID: {self.employee_id}, Name: {self.name}, Stipend: ${self.stipend:.2f})"
