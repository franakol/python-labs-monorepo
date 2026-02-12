from typing import List, Optional, Dict, Any
from rental_system.models.vehicle import Vehicle
from rental_system.models.car import Car
from rental_system.models.bike import Bike
from rental_system.models.truck import Truck
from rental_system.utils.storage import Storage

class RentalManager:
    """Manages vehicle inventory and rental operations."""
    
    def __init__(self, storage_file: str = "data/rentals.json"):
        self.storage_file = storage_file
        self.vehicles: List[Vehicle] = []
        self._load_vehicles()
        
    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Add a new vehicle to the fleet."""
        if any(v.vehicle_id == vehicle.vehicle_id for v in self.vehicles):
            raise ValueError(f"Vehicle with ID {vehicle.vehicle_id} already exists.")
        
        self.vehicles.append(vehicle)
        self._save_vehicles()
        
    def remove_vehicle(self, vehicle_id: str) -> None:
        """Remove a vehicle by ID."""
        vehicle = self.get_vehicle(vehicle_id)
        if vehicle:
            if not vehicle.is_available:
                raise ValueError(f"Cannot remove vehicle {vehicle_id} - currently rented.")
            self.vehicles.remove(vehicle)
            self._save_vehicles()
            
    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        """Find a vehicle by ID."""
        return next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
        
    def get_all_vehicles(self) -> List[Vehicle]:
        """Return all vehicles."""
        return self.vehicles
    
    def get_available_vehicles(self) -> List[Vehicle]:
        """Return only available vehicles."""
        return [v for v in self.vehicles if v.is_available]
    
    def rent_vehicle(self, vehicle_id: str, customer_name: str, days: int) -> float:
        """Rent a vehicle and return the total cost."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle {vehicle_id} not found.")
        
        vehicle.rent(customer_name)
        cost = vehicle.calculate_rental_cost(days)
        self._save_vehicles()
        
        return cost
    
    def return_vehicle(self, vehicle_id: str) -> None:
        """Return a rented vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle {vehicle_id} not found.")
        
        vehicle.return_vehicle()
        self._save_vehicles()
        
    def _save_vehicles(self) -> None:
        """Persist vehicles to storage."""
        data = [self._vehicle_to_dict(v) for v in self.vehicles]
        Storage.save_data(self.storage_file, data)
        
    def _load_vehicles(self) -> None:
        """Load vehicles from storage."""
        data = Storage.load_data(self.storage_file)
        self.vehicles = [self._dict_to_vehicle(d) for d in data]
        
    def _vehicle_to_dict(self, vehicle: Vehicle) -> Dict[str, Any]:
        """Convert vehicle object to dictionary."""
        data = {
            "type": vehicle.__class__.__name__,
            "vehicle_id": vehicle.vehicle_id,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "_rental_price_per_day": vehicle._rental_price_per_day,
            "_is_available": vehicle._is_available,
            "_rented_by": vehicle._rented_by
        }
        
        if isinstance(vehicle, Car):
            data.update({
                "num_doors": vehicle.num_doors,
                "transmission_type": vehicle.transmission_type
            })
        elif isinstance(vehicle, Bike):
            data.update({
                "bike_type": vehicle.bike_type,
                "has_basket": vehicle.has_basket
            })
        elif isinstance(vehicle, Truck):
            data.update({
                "cargo_capacity": vehicle.cargo_capacity,
                "bed_length": vehicle.bed_length
            })
            
        return data
        
    def _dict_to_vehicle(self, data: Dict[str, Any]) -> Vehicle:
        """Convert dictionary to vehicle object."""
        veh_type = data.pop("type")
        
        if veh_type == "Car":
            return Car(**data)
        elif veh_type == "Bike":
            return Bike(**data)
        elif veh_type == "Truck":
            return Truck(**data)
        else:
            raise ValueError(f"Unknown vehicle type: {veh_type}")
