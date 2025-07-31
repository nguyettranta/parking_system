from datetime import datetime

class ParkingRecord:
    def __init__(self, arrival_time, car_identity, frequent_parking_number=None):
        self.arrival_time = arrival_time
        self.car_identity = car_identity
        self.frequent_parking_number = frequent_parking_number

    def to_string(self):
        """Convert record to string format for file storage"""
        return f"{self.arrival_time},{self.car_identity},{self.frequent_parking_number}"
    
    @classmethod
    def from_string(cls, data_string):
        """Create ParkingRecord from string format"""
        content = data_string.strip().split(",")
        arrival_time = datetime.strptime(content[0], "%Y-%m-%d %H:%M:%S")
        car_id = content[1]
        freq_num = content[2] if len(content) > 2 and content[2] != "None" else None
        return cls(arrival_time, car_id, freq_num)
    
    def has_frequent_parking(self):
        """Check if this record has a valid frequent parking number"""
        return self.frequent_parking_number is not None