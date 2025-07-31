from decimal import Decimal
import os
from .base_file_manager import BaseFileManager

class HistoryManager(BaseFileManager):
    """Handles parking history operations"""
    
    base_directory = os.path.join(os.getcwd(), "data")

    def __init__(self, payment_manager):
        self.payment_manager = payment_manager
    
    def generate_history(self, car_identity):
        """Generate and export parking history"""
        history_file = self.get_file_path(f"{car_identity}_history.txt")
        if not os.path.exists(history_file):
            return False, "No history found."

        total_payment = Decimal("0.0")
        parked_dates = []
        
        try:
            with open(history_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() == "":
                        continue
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        paid_str = parts[1].strip().replace("Paid: ", "")
                        parked_dates.append(f"{parts[0].strip()} - {paid_str}")
                        try:
                            amount = Decimal(paid_str)
                            total_payment += amount
                        except:
                            continue

            credit = self.payment_manager.get_credit(car_identity)
            export_file = self.get_file_path(f"{car_identity}.txt")
            
            with open(export_file, "w") as f:
                f.write(f"Total payment: ${total_payment}\n")
                f.write(f"Available credits: ${credit}\n")
                f.write("Parked Dates:\n")
                for d in parked_dates:
                    f.write(d + "\n")

            return True, f"History exported to {export_file}"
        except Exception as e:
            return False, f"Error generating history: {e}"