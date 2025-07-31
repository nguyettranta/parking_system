import re

class CarIdentityValidator:
    """Handles validation of car identity format"""
    
    @staticmethod
    def validate(car_identity):
        """
        Validate car identity format: XXX-XXXXX
        Where:
        - First part: 2 characters 1 digits
        - Hyphen separator
        - Second part: exactly 5 digits
        
        Examples: 59C-12345, 01E-00001
        """
        if not isinstance(car_identity, str) or not car_identity.strip():
            return False
            
        # Pattern: 2 characters 1 alphanumeric, hyphen, exactly 5 digits
        pattern = r'^[0-9]{2}[A-Z]{1}-\d{5}$'
        
        return bool(re.match(pattern, car_identity.upper()))
    
    @staticmethod
    def format_car_identity(car_identity):
        """
        Format car identity to uppercase for consistency
        """
        if not car_identity:
            return car_identity
        return car_identity.upper().strip()
