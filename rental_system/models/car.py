from dataclasses import dataclass
from rental_system.models.vehicle import Vehicle

@dataclass
class Car(Vehicle):
    """Represents a car for rent."""
    
    num_doors: int = 4
    transmission_type: str = "automatic"  # automatic or manual
    
    def calculate_rental_cost(self, days: int) -> float:
        """Calculate rental cost with car-specific pricing."""
        base_cost = self.rental_price_per_day * days
        
        # Premium for automatic transmission
        if self.transmission_type.lower() == "automatic":
            base_cost *= 1.1
        
        return round(base_cost, 2)
    
    def get_details(self) -> str:
        """Return formatted car details."""
        status = "Available" if self.is_available else f"Rented to {self._rented_by}"
        return f"""Car Details:
ID: {self.vehicle_id}
Vehicle: {self.year} {self.make} {self.model}
Doors: {self.num_doors}
Transmission: {self.transmission_type}
Price per day: ${self.rental_price_per_day:.2f}
Status: {status}"""
