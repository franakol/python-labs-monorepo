# System Architecture - Vehicle Rental System

## Overview

The Vehicle Rental System follows a **layered architecture** pattern with clear separation of concerns. The system is designed using Object-Oriented Programming principles to demonstrate inheritance, polymorphism, and property decorators.

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
- `Vehicle` (Abstract Base Class)
  - Defines common attributes: `vehicle_id`, `make`, `model`, `year`
  - Uses `@property` decorators for `is_available`, `rental_price_per_day`
  - Enforces contract via `@abstractmethod` for `calculate_rental_cost()` and `get_details()`
  
- `Car` (Concrete Class)
  - Attributes: `num_doors`, `transmission_type`
  - Polymorphic pricing: automatic transmission adds 10% premium
  
- `Bike` (Concrete Class)
  - Attributes: `bike_type`, `has_basket`
  - Polymorphic pricing: electric bikes cost 50% more, baskets add $5/day
  
- `Truck` (Concrete Class)
  - Attributes: `cargo_capacity`, `bed_length`
  - Polymorphic pricing: capacity-based multipliers (1.15x-1.3x)

### 2. Service Layer (`services/`)

**Purpose**: Business operations and orchestration

**Components**:
- `RentalManager`
  - **Fleet Control**: Add, remove, search vehicles
  - **Rental Operations**: Rent and return with cost calculation
  - **Persistence**: Save/load state

### 3. Data Layer (`utils/`)

**Purpose**: Data storage and retrieval

**Implementation**:
- JSON file format
- `Storage` utility class for serialization

### 4. Presentation Layer (`ui/`)

**Purpose**: User interaction

**Components**:
- `CLI`: Interactive menu system
