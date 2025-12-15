import pytest
import os
from rental_system.services.rental_manager import RentalManager
from rental_system.models.car import Car
from rental_system.models.bike import Bike

@pytest.fixture
def test_db():
    file_path = "tests/test_rentals.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

def test_add_vehicle(test_db):
    manager = RentalManager(test_db)
    car = Car("1", "Toyota", "Camry", 2023, 50.0)
    manager.add_vehicle(car)
    
    assert len(manager.vehicles) == 1
    assert manager.get_vehicle("1") == car

def test_persistence(test_db):
    # Save
    manager1 = RentalManager(test_db)
    car = Car("1", "Toyota", "Camry", 2023, 50.0, num_doors=4, transmission_type="manual")
    manager1.add_vehicle(car)
    
    # Load
    manager2 = RentalManager(test_db)
    loaded_car = manager2.get_vehicle("1")
    
    assert isinstance(loaded_car, Car)
    assert loaded_car.make == "Toyota"
    assert loaded_car.transmission_type == "manual"

def test_rent_vehicle(test_db):
    manager = RentalManager(test_db)
    car = Car("1", "Toyota", "Camry", 2023, 50.0)
    manager.add_vehicle(car)
    
    cost = manager.rent_vehicle("1", "John Doe", 3)
    
    assert cost == 165.0
    assert not manager.get_vehicle("1").is_available

def test_return_vehicle(test_db):
    manager = RentalManager(test_db)
    car = Car("1", "Toyota", "Camry", 2023, 50.0)
    manager.add_vehicle(car)
    
    manager.rent_vehicle("1", "John Doe", 3)
    manager.return_vehicle("1")
    
    assert manager.get_vehicle("1").is_available

def test_get_available_vehicles(test_db):
    manager = RentalManager(test_db)
    car1 = Car("1", "Toyota", "Camry", 2023, 50.0)
    car2 = Car("2", "Honda", "Civic", 2023, 45.0)
    manager.add_vehicle(car1)
    manager.add_vehicle(car2)
    
    manager.rent_vehicle("1", "John Doe", 3)
    
    available = manager.get_available_vehicles()
    assert len(available) == 1
    assert available[0].vehicle_id == "2"
