class FrequentParkingValidator:
    """Handles validation of frequent parking numbers"""
    
    @staticmethod
    def validate(number_str):
        """Validate frequent parking number using check digit algorithm"""
        if len(number_str) != 5 or not number_str.isdigit():
            return False
        body = number_str[:4]
        check_digit = int(number_str[4])
        weights = [5, 4, 3, 2]
        total = sum(int(d) * w for d, w in zip(body, weights))
        remainder = total % 11
        calculated_check_digit = 11 - remainder
        if calculated_check_digit == 10:
            return False
        elif calculated_check_digit == 11:
            calculated_check_digit = 0
        print(f"Body: {body}, Check Digit: {check_digit}, Total: {total}, Remainder: {remainder}, Calculated Check Digit: {calculated_check_digit}")

        return check_digit == calculated_check_digit