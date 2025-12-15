# Employee Payroll Tracker

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-19%20passing-success)
![License](https://img.shields.io/badge/license-MIT-green)

A Python-based Employee Payroll Tracker demonstrating Object-Oriented Programming principles including inheritance, polymorphism, encapsulation, and property decorators.

## 🎯 Features

### OOP Principles
- **Inheritance**: Base `Employee` class with specialized subclasses
- **Polymorphism**: Role-specific salary calculation methods
- **Encapsulation**: Property decorators for data validation
- **Abstraction**: Abstract base class enforcing contracts

### Employee Types
1. **Full-Time Employee**: Monthly salary + benefits (20% tax deduction)
2. **Part-Time Employee**: Hourly rate × hours worked (15% tax deduction)
3. **Intern**: Fixed monthly stipend (no tax deduction)

### Core Functionality
- ✅ Add/remove employees with validation
- ✅ Calculate individual and total payroll
- ✅ Generate formatted payroll reports
- ✅ Persist data to JSON files
- ✅ Interactive command-line interface

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/franakol/employee-payroll-tracker.git
cd employee-payroll-tracker

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install pytest black flake8 mypy
```

### Step 2: Run the Application

**There are two ways to run the CLI:**

#### Option 1: Run as a module (Recommended)
```bash
python -m employee_payroll.ui.cli
```

#### Option 2: Run directly
```bash
python employee_payroll/ui/cli.py
```

### Step 3: Using the Application

Once the CLI starts, you'll see a menu with these options:

```
==================================================
          Employee Payroll Tracker
==================================================

--------------------------------------------------
Main Menu
--------------------------------------------------
1. Add Employee
2. View All Employees
3. Generate Payroll Report
4. Save Data
0. Exit
--------------------------------------------------
```

**Adding Employees:**
1. Choose option `1` from the main menu
2. Select employee type:
   - `1` for Full-Time Employee (salary + benefits)
   - `2` for Part-Time Employee (hourly rate)
   - `3` for Intern (stipend)
3. Enter employee details when prompted
4. Data is automatically validated

**Example Session:**
```bash
Enter your choice: 1
Select employee type: 1
Employee ID: FT001
Name: Alice Smith
Email: alice@company.com
Monthly Salary: $5000
Benefits (0 if none): $500
✅ Employee Alice Smith added successfully!
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=employee_payroll --cov-report=term-missing

# Run specific test file
pytest tests/test_employee_models.py -v
```

### Code Quality

```bash
# Format code with Black
black employee_payroll tests

# Lint with Flake8
flake8 employee_payroll tests

# Type check with MyPy
mypy employee_payroll
```

## 📁 Project Structure

```
employee-payroll-tracker/
├── employee_payroll/          # Main package
│   ├── __init__.py
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   ├── employee.py        # Abstract base class
│   │   ├── full_time_employee.py
│   │   ├── part_time_employee.py
│   │   └── intern.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── payroll_service.py # CRUD & calculations
│   ├── ui/                    # User interface
│   │   ├── __init__.py
│   │   └── cli.py             # Command-line interface
│   └── utils/                 # Utilities
│       └── __init__.py
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_employee_models.py   # 13 tests
│   └── test_payroll_service.py   # 6 tests
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md
│   └── GRADING.md
├── data/                      # Data files (gitignored)
│   └── employees.json
├── .gitignore
├── pyproject.toml            # Poetry configuration
└── README.md
```

## 💡 Usage Examples

### Adding Employees

```python
from employee_payroll.services.payroll_service import PayrollService
from employee_payroll.models.full_time_employee import FullTimeEmployee

# Initialize service
payroll = PayrollService()

# Add a full-time employee
emp = FullTimeEmployee("FT001", "Alice Smith", "alice@company.com", 5000.0, 500.0)
payroll.add_employee(emp)

# Calculate pay
net_pay = emp.calculate_pay()  # Returns 4400.0 (5500 * 0.80)
```

### Generating Reports

```python
# Generate payroll report
report = payroll.generate_payroll_report()
print(report)

# Calculate total payroll
total = payroll.calculate_total_payroll()
print(f"Total Payroll: ${total:,.2f}")
```

### Data Persistence

```python
# Save to file
payroll.save_employees()

# Load from file
payroll.load_employees()
```

## 🧪 Testing

The project includes comprehensive unit tests:

- **Employee Models** (13 tests)
  - Abstract class enforcement
  - Property validation
  - Salary calculations
  - Error handling

- **Payroll Service** (6 tests)
  - CRUD operations
  - Total payroll calculations
  - Report generation
  - File persistence

**Total: 19 tests passing** ✅

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and OOP patterns
- [Grading Criteria](docs/GRADING.md) - Lab requirements checklist

## 🛠️ Development

### Git Workflow

This project follows a phased development approach with feature branches:

1. **Phase 1**: Project Setup (pyproject.toml, structure)
2. **Phase 2**: Employee Models (OOP implementation)
3. **Phase 3**: PayrollService (business logic)
4. **Phase 4**: CLI (user interface)

Each phase has its own Pull Request for code review.

### Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest tests/ -v`
4. Format code: `black employee_payroll tests`
5. Submit a Pull Request

## 📊 Lab Requirements Met

- ✅ Numerical operations and data structures
- ✅ Modular functions for salary computation
- ✅ Inheritance and polymorphism
- ✅ Property decorators for validation
- ✅ Virtual environment setup
- ✅ Comprehensive testing
- ✅ Code documentation

## 📝 License

This project is created for educational purposes as part of Python programming.

## 👨‍💻 Author

Francis Akol.
