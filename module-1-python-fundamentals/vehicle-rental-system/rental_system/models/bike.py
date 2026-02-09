from dataclasses import dataclass
from rental_system.models.vehicle import Vehicle

@dataclass
class Bike(Vehicle):
    """Represents a bike for rent."""
    
    bike_type: str = "mountain"  # mountain, road, or electric
    has_basket: bool = False
    
    def calculate_rental_cost(self, days: int) -> float:
        """Calculate rental cost with bike-specific pricing."""
        base_cost = self.rental_price_per_day * days
        
        # Electric bikes cost more
        if self.bike_type.lower() == "electric":
            base_cost *= 1.5
        
        # Basket adds small fee
        if self.has_basket:
            base_cost += 5.0 * days
        
        return round(base_cost, 2)
    
    def get_details(self) -> str:
        """Return formatted bike details."""
        status = "Available" if self.is_available else f"Rented to {self._rented_by}"
        basket_info = "Yes" if self.has_basket else "No"
        return f"""Bike Details:
ID: {self.vehicle_id}
Vehicle: {self.year} {self.make} {self.model}
Type: {self.bike_type}
Basket: {basket_info}
Price per day: ${self.rental_price_per_day:.2f}
Status: {status}"""
