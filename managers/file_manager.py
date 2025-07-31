import os
from parking_record import ParkingRecord
from .base_file_manager import BaseFileManager

class FileManager(BaseFileManager):
    """Handles all file operations"""
    
    def save_record(self, car_identity, record):
        """Save parking record to file"""
        file_path = self.get_file_path(f"{car_identity}_record.txt")
        with open(file_path, "w") as f:
            f.write(record.to_string())
    
    def remove_record_file(self, car_identity):
        """Remove parking record file"""
        file_path = self.get_file_path(f"{car_identity}_record.txt")
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def save_payment(self, car_identity, amount, record, leave_time, credit):
        """Save payment history to file"""
        file_path = self.get_file_path(f"{car_identity}_history.txt")
        print(f"{record.arrival_time} - {leave_time}, Paid: {amount}, Credit: {credit}\n")
        with open(file_path, "a") as f:
            f.write(f"{record.arrival_time} - {leave_time}, Paid: {amount}, Credit: {credit}\n")
    
    def load_existing_records(self):
        """Load all existing parking records from files"""
        records = {}
        # Create the directory if it doesn't exist
        os.makedirs(self.base_directory, exist_ok=True)
        for filename in os.listdir():
            if filename.endswith("_record.txt"):
                car_identity = filename.replace("_record.txt", "")
                try:
                    with open(filename, "r") as f:
                        content = f.read().strip()
                        record = ParkingRecord.from_string(content)
                        records[car_identity] = record
                except Exception as e:
                    print(f"Error loading record for {car_identity}: {e}")
        return records