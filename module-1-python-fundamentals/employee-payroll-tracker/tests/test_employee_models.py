"""
Tests for the Employee models.
"""

import pytest
from employee_payroll.models.employee import Employee
from employee_payroll.models.full_time_employee import FullTimeEmployee
from employee_payroll.models.part_time_employee import PartTimeEmployee
from employee_payroll.models.intern import Intern


class TestEmployee:
    """Tests for the base Employee class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that Employee cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Employee("E001", "John Doe", "john@example.com")


class TestFullTimeEmployee:
    """Tests for FullTimeEmployee class."""

    def test_create_full_time_employee(self):
        """Test creating a full-time employee."""
        emp = FullTimeEmployee(
            "FT001", "Alice Smith", "alice@example.com", 5000.0, 500.0
        )
        assert emp.employee_id == "FT001"
        assert emp.name == "Alice Smith"
        assert emp.monthly_salary == 5000.0
        assert emp.benefits == 500.0

    def test_full_time_employee_calculate_pay(self):
        """Test salary calculation: (5000 + 500) * 0.8 = 4400."""
        emp = FullTimeEmployee("FT001", "Alice", "alice@example.com", 5000.0, 500.0)
        assert emp.calculate_pay() == 4400.0

    def test_negative_salary_raises_error(self):
        """Test that negative salary raises ValueError."""
        with pytest.raises(ValueError, match="Monthly salary cannot be negative"):
            FullTimeEmployee("FT001", "Alice", "alice@example.com", -1000.0)


class TestPartTimeEmployee:
    """Tests for PartTimeEmployee class."""

    def test_create_part_time_employee(self):
        """Test creating a part-time employee."""
        emp = PartTimeEmployee("PT001", "Bob", "bob@example.com", 50.0, 80.0)
        assert emp.employee_id == "PT001"
        assert emp.hourly_rate == 50.0
        assert emp.hours_worked == 80.0

    def test_part_time_employee_calculate_pay(self):
        """Test pay calculation: (50 * 80) * 0.85 = 3400."""
        emp = PartTimeEmployee("PT001", "Bob", "bob@example.com", 50.0, 80.0)
        assert emp.calculate_pay() == 3400.0

    def test_negative_rate_raises_error(self):
        """Test that negative rate raises ValueError."""
        with pytest.raises(ValueError, match="Hourly rate cannot be negative"):
            PartTimeEmployee("PT001", "Bob", "bob@example.com", -50.0)


class TestIntern:
    """Tests for Intern class."""

    def test_create_intern(self):
        """Test creating an intern."""
        emp = Intern("IN001", "Carol", "carol@example.com", 1500.0)
        assert emp.employee_id == "IN001"
        assert emp.stipend == 1500.0

    def test_intern_calculate_pay(self):
        """Test pay calculation: Full stipend, no tax."""
        emp = Intern("IN001", "Carol", "carol@example.com", 1500.0)
        assert emp.calculate_pay() == 1500.0

    def test_negative_stipend_raises_error(self):
        """Test that negative stipend raises ValueError."""
        with pytest.raises(ValueError, match="Stipend cannot be negative"):
            Intern("IN001", "Carol", "carol@example.com", -1000.0)


class TestEmployeeValidation:
    """Tests for validation across all employee types."""

    def test_empty_id_raises_error(self):
        """Test that empty employee ID raises ValueError."""
        with pytest.raises(ValueError, match="Employee ID cannot be empty"):
            FullTimeEmployee("", "Test", "test@example.com", 5000.0)

    def test_invalid_email_raises_error(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Email must contain @"):
            FullTimeEmployee("E001", "Test", "invalid-email", 5000.0)

    def test_property_setters(self):
        """Test updating via property setters."""
        emp = FullTimeEmployee("E001", "Original", "orig@example.com", 5000.0)
        emp.name = "Updated"
        emp.email = "updated@example.com"
        assert emp.name == "Updated"
        assert emp.email == "updated@example.com"
