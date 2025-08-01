from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from parking_record import ParkingRecord
from managers.file_manager import FileManager
from managers.payment_manager import PaymentManager
from managers.history_manager import HistoryManager
from validators.frequent_parking_validator import FrequentParkingValidator
from validators.car_identity_validator import CarIdentityValidator
from price.price_calculator import PriceCalculator

class ParkingSystem:
    """Main parking system class that coordinates all operations"""
    
    def __init__(self):
        self.records = {}
        self.validator = FrequentParkingValidator()
        self.car_validator = CarIdentityValidator()
        self.calculator = PriceCalculator()
        self.file_manager = FileManager()
        self.payment_manager = PaymentManager()
        self.history_manager = HistoryManager(self.payment_manager)
        self.load_existing_records()

    def load_existing_records(self):
        """Load existing parking records on startup"""
        self.records = self.file_manager.load_existing_records()

    def park_car(self):
        """Handle car parking process"""
        while True:
            car_identity = input("Enter car identity: ").strip()
            
            # Validate car identity format
            if self.car_validator.validate(car_identity):
                break
            else:
                print("Invalid car identity format. Please use format like: 59C-12345 or 01E-00001")
                print("Try again...")
        
        # Format car identity to uppercase for consistency
        car_identity = self.car_validator.format_car_identity(car_identity)
        if car_identity in self.records:
            print(f"Car {car_identity} is already parked.")
            return
        
        while True:
            arrival_time_str = input("Enter arrival time (YYYY-MM-DD HH:MM): ").strip()
            if arrival_time_str:
                try:
                    arrival_time = datetime.strptime(arrival_time_str, "%Y-%m-%d %H:%M")
                    break
                except ValueError:
                    print("Invalid datetime format. Please use YYYY-MM-DD HH:MM.")
            else:
                print("Arrival time cannot be empty.")

        frequent_parking_number = input("Enter frequent parking number (optional): ").strip()
        
        if frequent_parking_number == "":
            frequent_parking_number = None
        else:
            if not self.validator.validate(frequent_parking_number):
                frequent_parking_number = None
                print("Invalid frequent parking number.")
        
        record = ParkingRecord(arrival_time, car_identity, frequent_parking_number)
        self.records[car_identity] = record
        self.file_manager.save_record(car_identity, record)
        print(f"Car {car_identity} parked successfully.")

    def pickup_car(self):
        """Handle car pickup process"""
        while True:
            car_identity = input("Enter car identity to pickup: ").strip()
            # Format car identity to uppercase for consistency
            car_identity = self.car_validator.format_car_identity(car_identity)
            # Validate car identity format
            if self.car_validator.validate(car_identity):
                if car_identity in self.records:
                    break
                elif self.file_manager.get_car_record(car_identity):
                    self.records[car_identity] = self.file_manager.get_car_record(car_identity)
                    break
                else:
                    print("Car identity not found. Try again...")
            else:
                print("Invalid car identity format. Please use format like: 59C-12345 or 01E-00001")
                print("Try again...")

        record = self.records[car_identity]

        while True:
            leave_time_str = input("Enter leave time (YYYY-MM-DD HH:MM): ").strip()
            
            if leave_time_str:
                try:
                    leave_time = datetime.strptime(leave_time_str, "%Y-%m-%d %H:%M")
                    if leave_time > record.arrival_time:
                        break
                    else:
                        print("Leave time must be after arrival time. Try again...")
                except ValueError:
                    print("Invalid datetime format. Please use YYYY-MM-DD HH:MM.")
            else:
                print("Leave time cannot be empty.")
        

        price = self.calculator.calculate_price(record, leave_time)
        print(f"Parking fee: ${price}")


        while True:
            payment_input = input("Enter payment amount: ").strip()
            try:
                payment_amount = Decimal(payment_input)
            except:
                print("Invalid payment.")

            success, result = self.payment_manager.process_payment(car_identity, price, payment_amount)
            if success:
                break
            else:
                print(result)

        credit = result
        self.file_manager.save_payment(car_identity, price, record, leave_time, credit)
        current_credit = self.payment_manager.get_credit(car_identity)
        print(f"Payment accepted. Remaining credit: ${current_credit.quantize(Decimal('0.01'))}")
        
        del self.records[car_identity]
        self.file_manager.remove_record_file(car_identity)

    def history(self):
        """Handle history generation"""
        while True:
            car_identity = input("Enter car identity for history: ").strip()
            # Format car identity to uppercase for consistency
            car_identity = self.car_validator.format_car_identity(car_identity)
            # Validate car identity format
            if self.car_validator.validate(car_identity):
                if car_identity in self.records:
                    break
                elif self.history_manager.is_history_file_exist(car_identity):
                    break
                else:
                    print("Car identity not found. Try again...")
            else:
                print("Invalid car identity format. Please use format like: 59C-12345 or 01E-00001")
                print("Try again...")

        
        # Format car identity to uppercase for consistency
        car_identity = self.car_validator.format_car_identity(car_identity)
        
        success, message = self.history_manager.generate_history(car_identity)
        print(message)

def main():
    """Main function to run the parking system"""
    ps = ParkingSystem()

    while True:
        print("\n--- Console Parking System ---")
        print("1. Park Car")
        print("2. Pickup Car")
        print("3. History")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            ps.park_car()
        elif choice == "2":
            ps.pickup_car()
        elif choice == "3":
            ps.history()
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()