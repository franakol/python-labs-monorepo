from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Vehicle(ABC):
    """Abstract base class for all vehicles."""
    
    vehicle_id: str
    make: str
    model: str
    year: int
    _rental_price_per_day: float
    _is_available: bool = True
    _rented_by: Optional[str] = None
    
    @property
    def is_available(self) -> bool:
        """Check if vehicle is available for rent."""
        return self._is_available
    
    @property
    def rental_price_per_day(self) -> float:
        """Get the base rental price per day."""
        return self._rental_price_per_day
    
    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        """Calculate total rental cost based on vehicle type and duration."""
        pass
    
    @abstractmethod
    def get_details(self) -> str:
        """Return a formatted string of vehicle details."""
        pass
    
    def rent(self, customer_name: str) -> None:
        """Mark vehicle as rented."""
        if not self._is_available:
            raise ValueError(f"Vehicle {self.vehicle_id} is already rented.")
        self._is_available = False
        self._rented_by = customer_name
    
    def return_vehicle(self) -> None:
        """Mark vehicle as returned."""
        if self._is_available:
            raise ValueError(f"Vehicle {self.vehicle_id} is not currently rented.")
        self._is_available = True
        self._rented_by = None
    
    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model}"
