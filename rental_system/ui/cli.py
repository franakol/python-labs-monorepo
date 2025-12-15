import sys
from rental_system.services.rental_manager import RentalManager
from rental_system.models.car import Car
from rental_system.models.bike import Bike
from rental_system.models.truck import Truck

class CLI:
    """Command-line interface for the Vehicle Rental System."""
    
    def __init__(self):
        self.manager = RentalManager()
        
    def start(self):
        """Start the CLI application."""
        while True:
            self._display_menu()
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self._add_vehicle_menu()
            elif choice == '2':
                self._list_all_vehicles()
            elif choice == '3':
                self._rent_vehicle()
            elif choice == '4':
                self._return_vehicle()
            elif choice == '5':
                self._view_available_vehicles()
            elif choice == '6':
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")
                
    def _display_menu(self):
        print("\n=== Vehicle Rental System ===")
        print("1. Add Vehicle")
        print("2. List All Vehicles")
        print("3. Rent Vehicle")
        print("4. Return Vehicle")
        print("5. View Available Vehicles")
        print("6. Exit")
        
    def _add_vehicle_menu(self):
        print("\nSelect Vehicle Type:")
        print("1. Car")
        print("2. Bike")
        print("3. Truck")
        
        type_choice = input("Choice (1-3): ")
        
        try:
            if type_choice == '1':
                self._add_car()
            elif type_choice == '2':
                self._add_bike()
            elif type_choice == '3':
                self._add_truck()
            else:
                print("Invalid vehicle type.")
        except ValueError as e:
            print(f"\nError: {e}")
            
    def _get_common_details(self):
        vehicle_id = input("Vehicle ID: ")
        make = input("Make: ")
        model = input("Model: ")
        year = int(input("Year: "))
        price = float(input("Price per day ($): "))
        return vehicle_id, make, model, year, price
        
    def _add_car(self):
        vehicle_id, make, model, year, price = self._get_common_details()
        num_doors = int(input("Number of doors: "))
        transmission = input("Transmission (automatic/manual): ")
        
        car = Car(
            vehicle_id=vehicle_id,
            make=make,
            model=model,
            year=year,
            _rental_price_per_day=price,
            num_doors=num_doors,
            transmission_type=transmission
        )
        self.manager.add_vehicle(car)
        print("\nCar added successfully!")
        
    def _add_bike(self):
        vehicle_id, make, model, year, price = self._get_common_details()
        bike_type = input("Bike type (mountain/road/electric): ")
        has_basket = input("Has basket? (yes/no): ").lower() == 'yes'
        
        bike = Bike(
            vehicle_id=vehicle_id,
            make=make,
            model=model,
            year=year,
            _rental_price_per_day=price,
            bike_type=bike_type,
            has_basket=has_basket
        )
        self.manager.add_vehicle(bike)
        print("\nBike added successfully!")
        
    def _add_truck(self):
        vehicle_id, make, model, year, price = self._get_common_details()
        cargo_capacity = float(input("Cargo capacity (lbs): "))
        bed_length = float(input("Bed length (ft): "))
        
        truck = Truck(
            vehicle_id=vehicle_id,
            make=make,
            model=model,
            year=year,
            _rental_price_per_day=price,
            cargo_capacity=cargo_capacity,
            bed_length=bed_length
        )
        self.manager.add_vehicle(truck)
        print("\nTruck added successfully!")
        
    def _list_all_vehicles(self):
        vehicles = self.manager.get_all_vehicles()
        if not vehicles:
            print("\nNo vehicles in the system.")
            return
            
        print(f"\nTotal Vehicles: {len(vehicles)}")
        for v in vehicles:
            print("-" * 50)
            print(v.get_details())
            
    def _rent_vehicle(self):
        vehicle_id = input("\nVehicle ID to rent: ")
        customer_name = input("Customer name: ")
        days = int(input("Number of days: "))
        
        try:
            cost = self.manager.rent_vehicle(vehicle_id, customer_name, days)
            print(f"\nVehicle rented successfully!")
            print(f"Total cost for {days} days: ${cost:.2f}")
        except ValueError as e:
            print(f"\nError: {e}")
            
    def _return_vehicle(self):
        vehicle_id = input("\nVehicle ID to return: ")
        
        try:
            self.manager.return_vehicle(vehicle_id)
            print("\nVehicle returned successfully!")
        except ValueError as e:
            print(f"\nError: {e}")
            
    def _view_available_vehicles(self):
        vehicles = self.manager.get_available_vehicles()
        if not vehicles:
            print("\nNo available vehicles.")
            return
            
        print(f"\nAvailable Vehicles: {len(vehicles)}")
        for v in vehicles:
            print("-" * 50)
            print(v.get_details())
