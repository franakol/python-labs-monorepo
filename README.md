# Vehicle Rental System

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python-based Vehicle Rental System to manage cars, bikes, and trucks. This project demonstrates Object-Oriented Programming (OOP) principles including inheritance, polymorphism, and property decorators.

## 🎯 Features

- **Vehicle Management**:
  - **Cars**: Track transmission type and number of doors
  - **Bikes**: Manage bike types (mountain/road/electric) and accessories
  - **Trucks**: Track cargo capacity and bed length
- **Rental Operations**:
  - Rent vehicles with dynamic pricing
  - Return vehicles
  - Track availability status
- **Data Persistence**:
  - Automatic JSON-based storage (`data/rentals.json`)
  - Data persists between sessions
- **Interactive CLI**:
  - User-friendly menu system
  - Robust input validation

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the repository**
   ```bash
   cd vehicle-rental-system
   ```

2. **Set up Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install pytest black flake8 mypy
   ```

### Running the Application

```bash
python -m rental_system.main
```

## 📖 Usage Guide

### Main Menu
```
=== Vehicle Rental System ===
1. Add Vehicle
2. List All Vehicles
3. Rent Vehicle
4. Return Vehicle
5. View Available Vehicles
6. Exit
```

## 🧪 Testing

```bash
pytest -v
```

## 📁 Project Structure

```
vehicle-rental-system/
├── rental_system/
│   ├── models/          # Domain Entities
│   ├── services/        # Business Logic
│   ├── ui/              # User Interface
│   ├── utils/           # Utilities
│   └── main.py          # Entry Point
├── tests/               # Unit Tests
├── data/                # Data Storage
└── docs/                # Documentation
```

## 📝 License

This project is created for educational purposes.
