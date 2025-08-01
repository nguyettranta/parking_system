from decimal import Decimal
import os
from .base_file_manager import BaseFileManager

class PaymentManager(BaseFileManager):
    """Handles payment processing and credit management"""
    
    def __init__(self):
        self.credits = {}
    
    def process_payment(self, car_identity, price, payment_amount):
        """Process payment and update credits"""
        remaining_credit = self.get_remaining_credit(car_identity)
        if (payment_amount + remaining_credit) < price:
            return False, "Payment insufficient."
        
        
        credit = payment_amount + remaining_credit - price
        self.credits[car_identity] = self.credits.get(car_identity, Decimal("0.0")) + credit
        return True, credit
    
    def get_credit(self, car_identity):
        """Get current credit for a car"""
        return self.credits.get(car_identity, Decimal("0.0"))
    
    def get_remaining_credit(self, car_identity):
        """Get remaining credit for a car"""
        history_file = self.get_file_path(f"{car_identity}_history.txt")
        
        last_line = None
        with open(history_file, 'r') as file:
            for line in file:
                last_line = line

        if last_line:
            parts = last_line.strip().split(",")
            if len(parts) >= 2:
                credit_str = parts[2].strip().replace("Credit: ", "")
                try:
                    return Decimal(credit_str)
                except:
                    return Decimal("0.0")

        return Decimal("0.0")