# Labs & Projects Monorepo

## Overview
This monorepo contains my completed labs and projects from various modules, demonstrating skills in Python development, testing, database fundamentals, and web development.

## Repository Structure

### Module 2: Clean Code, Testing, Git
- **Lab 1: [Resilient Data Importer CLI](./module-2-clean-code-testing/resilient-data-importer)**
  - CLI tool for importing user data from CSV to JSON database
  - Implements robust exception handling with custom exceptions
  - Adheres to PEP 8, SOLID principles, and Git Flow workflow
  - Comprehensive test suite with >90% coverage

- **Lab 2: [Git Config Manager](./module-2-clean-code-testing/git-config-manager)**
  - TDD-based API Service Stub (mapped to Git Config Manager based on structure)

### Module 3: Python Advanced
- **[Student Course Management System](./module-3-python-advanced/student-course-management-lab)**
  - Student Grade Analytics Tool
  - Processes student records from CSV/JSON files
  - Uses advanced collections (Counter, defaultdict, OrderedDict, deque)
  - Implements dataclasses with comprehensive type hints
  - Generates statistical reports and visualizations

- **[Async Web Scraper](./module-3-python-advanced/async-web-scraper)**
    - Asynchronous web scraper

### Module 4: Database Fundamentals
- **[Logistics Shipment Tracking](./module-4-database-fundamentals/logistics-shipment-tracking)**
  - E-Commerce Analytics Data Pipeline
  - Normalized PostgreSQL schema for e-commerce platform
  - Transactional CRUD operations using psycopg2
  - NoSQL integration (Redis for caching, MongoDB for sessions)
  - Complex SQL queries with window functions and CTEs
  - Query optimization with EXPLAIN ANALYZE and indexing

- **[Data Processing Pipeline](./module-4-database-fundamentals/data-processing-pipeline)**
    - Data processing pipeline

### Module 5: Flask/Django Web Development
- **[URL Shortener Microservice](./module-5-web-development/url-shortener)**
  - Flask/Django application using application factory pattern and blueprints
  - Dependency injection
  - Docker containerization with Redis
  - REST API with OpenAPI/Swagger documentation
  - Production-ready deployment configuration

- **[Secure Auth Service](./module-5-web-development/secure-auth-service)**
    - Secure authentication service

### Module 1: Initial lab work and setup / Additional Projects
- **[Employee Payroll Tracker](./module-1-python-fundamentals/employee-payroll-tracker)**
- **[Library Inventory App](./module-1-python-fundamentals/library-inventory-app)**
- **[Vehicle Rental System](./module-1-python-fundamentals/vehicle-rental-system)**

## 🛠️ Common Features Across Projects
- **Code Quality**: PEP 8 compliance, type hints, comprehensive docstrings
- **Testing**: High test coverage with pytest, mocking, and fixtures
- **Git Workflow**: Proper branching strategies with pull requests
- **Pre-commit Hooks**: Automated code quality checks
- **Documentation**: Detailed README files and usage instructions

##  Getting Started

### Prerequisites
- Python 3.11+
- Git
- Docker & Docker Compose (for Module 4 & 5)
- PostgreSQL, Redis, MongoDB (for Module 4)

### Installation
Each module contains its own `requirements.txt` file. Navigate to the specific project directory and install dependencies:

```bash
cd module-2-clean-code-testing/resilient-data-importer
pip install -r requirements.txt
```

### Running Projects
Detailed setup and execution instructions are available in each module's README file.

## Skills Demonstrated
- **Python Development**: Clean code, SOLID principles, advanced data structures
- **Testing**: TDD, BDD, unit testing, integration testing
- **Databases**: SQL (PostgreSQL), NoSQL (Redis, MongoDB), query optimization
- **Web Development**: Flask, REST APIs, microservices, containerization
- **DevOps**: Docker, Git workflows, CI/CD practices
- **Documentation**: API documentation, code comments, project READMEs
