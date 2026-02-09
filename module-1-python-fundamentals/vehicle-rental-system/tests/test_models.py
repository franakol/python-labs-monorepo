import pytest
from rental_system.models.car import Car
from rental_system.models.bike import Bike
from rental_system.models.truck import Truck

def test_car_creation():
    car = Car("1", "Toyota", "Camry", 2023, 50.0, num_doors=4, transmission_type="automatic")
    assert car.make == "Toyota"
    assert car.is_available == True
    assert "Toyota" in car.get_details()

def test_car_pricing():
    car = Car("1", "Toyota", "Camry", 2023, 50.0, transmission_type="automatic")
    cost = car.calculate_rental_cost(3)
    assert cost == 165.0  # 50 * 3 * 1.1

def test_bike_creation():
    bike = Bike("2", "Trek", "Mountain X", 2023, 30.0, bike_type="electric", has_basket=True)
    assert bike.bike_type == "electric"
    assert bike.has_basket == True

def test_bike_pricing():
    bike = Bike("2", "Trek", "Mountain X", 2023, 30.0, bike_type="electric", has_basket=True)
    cost = bike.calculate_rental_cost(2)
    assert cost == 100.0  # (30 * 1.5 + 5) * 2

def test_truck_creation():
    truck = Truck("3", "Ford", "F-150", 2023, 75.0, cargo_capacity=2000, bed_length=6.5)
    assert truck.cargo_capacity == 2000
    assert truck.bed_length == 6.5

def test_truck_pricing():
    truck = Truck("3", "Ford", "F-150", 2023, 75.0, cargo_capacity=2000)
    cost = truck.calculate_rental_cost(2)
    assert cost == 195.0  # 75 * 2 * 1.3

def test_vehicle_rent_and_return():
    car = Car("1", "Toyota", "Camry", 2023, 50.0)
    assert car.is_available == True
    
    car.rent("John Doe")
    assert car.is_available == False
    assert car._rented_by == "John Doe"
    
    car.return_vehicle()
    assert car.is_available == True
    assert car._rented_by == None
