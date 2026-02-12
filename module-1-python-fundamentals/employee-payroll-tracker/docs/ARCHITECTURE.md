# System Architecture - Employee Payroll Tracker

## Overview

The Employee Payroll Tracker follows a **layered architecture** pattern with clear separation of concerns. The system is designed using Object-Oriented Programming principles to demonstrate inheritance, polymorphism, and encapsulation.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│              (UI/CLI)                   │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Service Layer                   │
│       (Business Logic)                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Domain Layer                    │
│          (Models)                       │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Data Layer                      │
│      (File Persistence)                 │
└─────────────────────────────────────────┘
```

## Layer Details

### 1. Domain Layer (`models/`)

**Purpose**: Core business entities and rules

**Components**:
- `Employee` (Abstract Base Class)
  - Defines common attributes: `employee_id`, `name`, `email`
  - Enforces `calculate_pay()` contract via `@abstractmethod`
  - Implements validation via property decorators
  
- `FullTimeEmployee` (Concrete Class)
  - Attributes: `monthly_salary`, `benefits`
  - Tax Rate: 20%
  - Formula: `(salary + benefits) * 0.80`
  
- `PartTimeEmployee` (Concrete Class)
  - Attributes: `hourly_rate`, `hours_worked`
  - Tax Rate: 15%
  - Formula: `(rate × hours) * 0.85`
  
- `Intern` (Concrete Class)
  - Attributes: `stipend`
  - Tax Rate: 0%
  - Formula: `stipend` (no deduction)

**Design Patterns**:
- **Template Method**: Base class defines structure, subclasses implement details
- **Strategy Pattern**: Different calculation strategies per employee type

### 2. Service Layer (`services/`)

**Purpose**: Business operations and orchestration

**Components**:
- `PayrollService`
  - **CRUD Operations**: Add, get, remove employees
  - **Calculations**: Total payroll aggregation
  - **Reporting**: Formatted payroll reports
  - **Persistence**: JSON serialization/deserialization

**Responsibilities**:
- Manage employee collection
- Enforce business rules (e.g., unique employee IDs)
- Coordinate between domain and data layers
- Provide high-level operations to UI

### 3. Data Layer (Embedded in Service)

**Purpose**: Data storage and retrieval

**Implementation**:
- JSON file format for simplicity
- Location: `data/employees.json`
- Operations:
  - `save_employees()`: Serialize to JSON
  - `load_employees()`: Deserialize from JSON
  - Type-safe conversion via `_employee_to_dict()` / `_dict_to_employee()`

### 4. Presentation Layer (`ui/`)

**Purpose**: User interaction

**Components**:
- `CLI` (Command-Line Interface)
  - Interactive menu system
  - Input collection and validation
  - Output formatting
  - Error handling and user feedback

**Flow**:
1. Display menu
2. Get user choice
3. Collect input data
4. Invoke service methods
5. Display results
6. Repeat

## OOP Principles Applied

### 1. Inheritance

```python
class Employee(ABC):          # Base class
    @abstractmethod
    def calculate_pay(self):
        pass

class FullTimeEmployee(Employee):  # Derived class
    def calculate_pay(self):
        # Specific implementation
        return (self.monthly_salary + self.benefits) * 0.80
```

**Benefits**:
- Code reuse (common attributes in base class)
- Polymorphic behavior
- Enforced contracts via abstract methods

### 2. Polymorphism

```python
employees = [
    FullTimeEmployee(...),
    PartTimeEmployee(...),
    Intern(...)
]

# Same method call, different behavior per type
for emp in employees:
    pay = emp.calculate_pay()  # Polymorphic call
```

**Benefits**:
- Single interface for multiple implementations
- Extensibility (easy to add new employee types)
- Dynamic dispatch at runtime

### 3. Encapsulation

```python
class FullTimeEmployee(Employee):
    def __init__(self, ..., monthly_salary, ...):
        self._monthly_salary = monthly_salary  # Private attribute
    
    @property
    def monthly_salary(self) -> float:
        return self._monthly_salary  # Controlled access
    
    @monthly_salary.setter
    def monthly_salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._monthly_salary = value  # Validated mutation
```

**Benefits**:
- Data protection
- Validation on mutation
- Implementation hiding

### 4. Abstraction

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    @abstractmethod
    def calculate_pay(self) -> float:
        """All employees must implement this."""
        pass
```

**Benefits**:
- Enforced interface contracts
- Clear expectations for subclasses
- Prevents instantiation of incomplete classes

## Data Flow

### Adding an Employee

```
User Input (CLI)
    ↓
Create Employee Object (Model)
    ↓
Validate via Properties (Model)
    ↓
Add to Collection (Service)
    ↓
Check Uniqueness (Service)
    ↓
Success/Error Feedback (CLI)
```

### Generating Report

```
User Request (CLI)
    ↓
Get All Employees (Service)
    ↓
Calculate Pay for Each (Model - Polymorphic)
    ↓
Format Report (Service)
    ↓
Display to User (CLI)
```

### Persistence

```
Save Request (CLI)
    ↓
Convert Objects to Dicts (Service)
    ↓
Write JSON to File (Service)
    ↓
Success Confirmation (CLI)

Load on Startup (Service)
    ↓
Read JSON from File (Service)
    ↓
Convert Dicts to Objects (Service)
    ↓
Ready for Operations
```

## Technology Stack

- **Language**: Python 3.11+
- **Testing**: pytest
- **Code Formatting**: Black
- **Linting**: Flake8
- **Type Checking**: MyPy
- **Persistence**: JSON (stdlib)

## Design Decisions

### Why JSON over Database?
- **Simplicity**: Easy to read and debug
- **Portability**: Works anywhere without setup
- **Suitable for scale**: Appropriate for lab requirements

### Why Abstract Base Class?
- **Type Safety**: Enforces contract at class level
- **Clear Intent**: Makes inheritance explicit
- **Python Best Practice**: Standard approach for interfaces

### Why Property Decorators?
- **Pythonic**: Idiomatic Python for getters/setters  
- **Validation**: Centralized data validation
- **Encapsulation**: Protects internal state

## Testing Strategy

### Unit Tests
- **Models**: Test each employee type independently
- **Service**: Test CRUD operations, calculations, persistence
- **Coverage**: 19 tests covering critical paths

### Test Organization
```
tests/
├── test_employee_models.py    # 13 tests
└── test_payroll_service.py    # 6 tests
```

## Extensibility

### Adding New Employee Types

1. Create new class inheriting from `Employee`
2. Implement `calculate_pay()` method
3. Add to `_dict_to_employee()` in `PayrollService`
4. Update CLI menu options
5. Add corresponding tests

### Adding New Features

- **Bonus calculations**: Add methods to employee classes
- **Tax brackets**: Implement utility functions
- **Database support**: Create new data layer module
- **Web UI**: Add Flask/Django presentation layer

## Security Considerations

- **Input Validation**: All user inputs validated
- **Type Safety**: Type hints throughout
- **Error Handling**: Graceful failure on invalid data
- **Data Integrity**: Unique ID enforcement

## Performance Characteristics

- **Time Complexity**:
  - Add employee: O(n) due to uniqueness check
  - Get employee: O(n) linear search
  - Calculate total: O(n) iteration
  
- **Space Complexity**: O(n) for n employees

- **Optimizations Possible**:
  - Use dict for O(1) employee lookup
  - Cache total payroll calculation
  - Add database indexing for large datasets

## Conclusion

This architecture demonstrates professional software design principles while meeting all lab requirements for OOP, modularity, and code quality.
