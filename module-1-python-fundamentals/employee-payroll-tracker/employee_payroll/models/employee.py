"""
Base Employee class.

This module defines the abstract base class for all employee types.
"""

from abc import ABC, abstractmethod


class Employee(ABC):
    """
    Abstract base class for all employees.

    Attributes:
        employee_id: Unique identifier for the employee.
        name: Full name of the employee.
        email: Email address of the employee.
    """

    def __init__(self, employee_id: str, name: str, email: str) -> None:
        """
        Initialize an Employee.

        Args:
            employee_id: Unique identifier for the employee.
            name: Full name of the employee.
            email: Email address of the employee.

        Raises:
            ValueError: If any required field is empty.
        """
        if not employee_id or not employee_id.strip():
            raise ValueError("Employee ID cannot be empty")
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        if "@" not in email:
            raise ValueError("Email must contain @")

        self._employee_id = employee_id.strip()
        self._name = name.strip()
        self._email = email.strip()

    @property
    def employee_id(self) -> str:
        """Get the employee ID."""
        return self._employee_id

    @property
    def name(self) -> str:
        """Get the employee name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the employee name."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self) -> str:
        """Get the employee email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set the employee email."""
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")
        if "@" not in value:
            raise ValueError("Email must contain @")
        self._email = value.strip()

    @abstractmethod
    def calculate_pay(self) -> float:
        """
        Calculate the employee's pay.

        This method must be implemented by all subclasses.

        Returns:
            The calculated pay amount.
        """
        pass

    def __str__(self) -> str:
        """Return string representation of the employee."""
        return f"{self.__class__.__name__}(ID: {self.employee_id}, Name: {self.name})"

    def __repr__(self) -> str:
        """Return detailed representation of the employee."""
        return f"{self.__class__.__name__}(employee_id='{self.employee_id}', name='{self.name}', email='{self.email}')"
