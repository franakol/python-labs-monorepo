# Secure Auth Service

> Part of the [Python Labs Monorepo](https://github.com/franakol/python-labs-monorepo)

A secure, reusable User Authentication Service Module built with strict TDD and SOLID principles.

## 🎯 Lab Objectives

- **TDD Workflow**: Red-Green-Refactor cycle with 100% test coverage
- **SOLID Principles**: Dependency injection with abstract interfaces
- **Security**: Bcrypt password hashing, password policies
- **Code Quality**: Type hints, Black, Ruff, mypy strict mode

## ⚡ Quick Start

```bash
cd secure-auth-service
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## 📁 Architecture

```
auth_service/
├── models.py                 # User dataclass
├── exceptions.py             # Custom exceptions
├── service.py                # UserService (entry point)
├── interfaces/
│   ├── repository.py         # UserRepository ABC
│   └── hasher.py             # PasswordHasher ABC
└── implementations/
    ├── memory_repository.py  # InMemoryUserRepository
    └── bcrypt_hasher.py      # BcryptPasswordHasher
```

## 🔐 Usage

```python
from auth_service.service import UserService
from auth_service.implementations.memory_repository import InMemoryUserRepository
from auth_service.implementations.bcrypt_hasher import BcryptPasswordHasher

# Create service with dependency injection
repo = InMemoryUserRepository()
hasher = BcryptPasswordHasher()
service = UserService(repository=repo, hasher=hasher)

# Register a user
user = service.register("john_doe", "SecurePass123!")

# Login
authenticated_user = service.login("john_doe", "SecurePass123!")
```

## 🧪 Testing

```bash
pytest -v
pytest --cov=auth_service --cov-report=term-missing --cov-fail-under=100
```

## 📝 License

MIT License
