from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
from .pricing import PRICING

class PriceCalculator:
    """Handles parking price calculations"""
    
    def __init__(self):
        self.pricing = PRICING
    
    def get_time_slot(self, hour):
        """Determine which time slot an hour falls into"""
        if 0 <= hour < 8:
            return "00:00-07:59"
        elif 8 <= hour < 17:
            return "08:00-16:59"
        else:
            return "17:00-23:59"
    
    def calculate_price(self, record, leave_time):
        """Calculate total parking price for a record"""
        total_price = Decimal("0.0")
        visited_slots = set()  # to avoid charging twice for 00:00–07:59 one-time
        arrival_time = record.arrival_time

        while arrival_time < leave_time:
            week_day = arrival_time.weekday()  # Monday=0 ... Sunday=6
            hour = arrival_time.hour
            slot = self.get_time_slot(hour)
            print(f"Calculating for week day: {week_day}, hour: {hour}, slot: {slot}")
            slot_info = self.pricing[week_day].get(slot)
            print(f"Calculating for slot: {slot}, arrival time: {arrival_time}, week day: {week_day}, hour: {hour}, slot info: {slot_info}")

            rate = slot_info["rate"]
            if "onetime" in slot_info:
                # Charge once per day
                key = (arrival_time.date(), slot)
                if key not in visited_slots:
                    visited_slots.add(key)
                    rate = self._apply_discount(rate, record, slot)
                    total_price += rate
                arrival_time += timedelta(hours=1)
                continue
            elif slot_info["max_hours"] is None:
                # No max hours, charge for all hours in this slot
                hr_rate = self._apply_discount(rate, record, slot)
                total_price += hr_rate
                arrival_time += timedelta(hours=1)
            else:
                max_hours = slot_info["max_hours"]
                slot_hours = 0
                temp = arrival_time
                while temp < leave_time and self.get_time_slot(temp.hour) == slot and temp.weekday() == week_day:
                    slot_hours += 1
                    temp += timedelta(hours=1)

                normal_hours = min(slot_hours, max_hours)
                exceed_hours = max(0, slot_hours - max_hours)
                normal_price = self._apply_discount(rate * normal_hours, record, slot)
                exceed_price = self._apply_discount(rate * 2 * exceed_hours, record, slot)
                total_price +=  normal_price + exceed_price

                arrival_time = temp

        return total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def _apply_discount(self, rate, record, slot):
        """Apply frequent parking discounts"""
        if not record.has_frequent_parking():
            return rate
        
        if slot in ["00:00-07:59", "17:00-23:59"]:
            return rate * Decimal("0.5")
        else:
            return rate * Decimal("0.9")