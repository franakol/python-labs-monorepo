"""Tests for PayrollService."""

import pytest
from pathlib import Path
from employee_payroll.services.payroll_service import PayrollService
from employee_payroll.models.full_time_employee import FullTimeEmployee
from employee_payroll.models.part_time_employee import PartTimeEmployee
from employee_payroll.models.intern import Intern


@pytest.fixture
def temp_data_file(tmp_path):
    """Create a temporary data file path."""
    return tmp_path / "test_employees.json"


@pytest.fixture
def payroll_service(temp_data_file):
    """Create a PayrollService instance."""
    return PayrollService(data_file=temp_data_file)


class TestPayrollService:
    """Tests for PayrollService class."""

    def test_add_employee(self, payroll_service):
        """Test adding an employee."""
        emp = FullTimeEmployee("FT001", "Alice", "alice@example.com", 5000.0)
        payroll_service.add_employee(emp)
        assert len(payroll_service.employees) == 1

    def test_add_duplicate_raises_error(self, payroll_service):
        """Test that duplicate IDs raise error."""
        emp1 = FullTimeEmployee("FT001", "Alice", "alice@example.com", 5000.0)
        emp2 = FullTimeEmployee("FT001", "Bob", "bob@example.com", 6000.0)
        payroll_service.add_employee(emp1)
        with pytest.raises(ValueError, match="already exists"):
            payroll_service.add_employee(emp2)

    def test_get_employee(self, payroll_service):
        """Test retrieving an employee."""
        emp = PartTimeEmployee("PT001", "Bob", "bob@example.com", 50.0, 80.0)
        payroll_service.add_employee(emp)
        retrieved = payroll_service.get_employee("PT001")
        assert retrieved == emp

    def test_remove_employee(self, payroll_service):
        """Test removing an employee."""
        emp = Intern("IN001", "Carol", "carol@example.com", 1500.0)
        payroll_service.add_employee(emp)
        result = payroll_service.remove_employee("IN001")
        assert result is True
        assert len(payroll_service.employees) == 0

    def test_calculate_total_payroll(self, payroll_service):
        """Test total payroll calculation."""
        emp1 = FullTimeEmployee("FT001", "Alice", "alice@example.com", 5000.0, 500.0)
        emp2 = PartTimeEmployee("PT001", "Bob", "bob@example.com", 50.0, 80.0)
        emp3 = Intern("IN001", "Carol", "carol@example.com", 1500.0)

        payroll_service.add_employee(emp1)
        payroll_service.add_employee(emp2)
        payroll_service.add_employee(emp3)

        total = payroll_service.calculate_total_payroll()
        expected = 4400 + 3400 + 1500  # (5500*0.8) + (4000*0.85) + 1500
        assert total == expected

    def test_save_and_load(self, payroll_service, temp_data_file):
        """Test saving and loading employees."""
        emp1 = FullTimeEmployee("FT001", "Alice", "alice@example.com", 5000.0, 500.0)
        emp2 = Intern("IN001", "Carol", "carol@example.com", 1500.0)

        payroll_service.add_employee(emp1)
        payroll_service.add_employee(emp2)
        payroll_service.save_employees()

        # Load into new service
        new_service = PayrollService(data_file=temp_data_file)
        assert len(new_service.employees) == 2

        loaded_ft = new_service.get_employee("FT001")
        assert isinstance(loaded_ft, FullTimeEmployee)
        assert loaded_ft.monthly_salary == 5000.0
