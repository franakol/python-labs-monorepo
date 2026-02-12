from dataclasses import dataclass
from rental_system.models.vehicle import Vehicle

@dataclass
class Truck(Vehicle):
    """Represents a truck for rent."""
    
    cargo_capacity: float = 1000.0  # in lbs
    bed_length: float = 6.5  # in feet
    
    def calculate_rental_cost(self, days: int) -> float:
        """Calculate rental cost with truck-specific pricing."""
        base_cost = self.rental_price_per_day * days
        
        # Larger capacity trucks cost more
        if self.cargo_capacity >= 2000:
            base_cost *= 1.3
        elif self.cargo_capacity >= 1500:
            base_cost *= 1.15
        
        return round(base_cost, 2)
    
    def get_details(self) -> str:
        """Return formatted truck details."""
        status = "Available" if self.is_available else f"Rented to {self._rented_by}"
        return f"""Truck Details:
ID: {self.vehicle_id}
Vehicle: {self.year} {self.make} {self.model}
Cargo Capacity: {self.cargo_capacity} lbs
Bed Length: {self.bed_length} ft
Price per day: ${self.rental_price_per_day:.2f}
Status: {status}"""
