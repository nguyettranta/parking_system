from decimal import Decimal
PRICING = {
    0: {  # Monday
        "08:00-16:59": {"rate": Decimal("10.00"), "max_hours": 2},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },
    1: {  # Tuesday
        "08:00-16:59": {"rate": Decimal("10.00"), "max_hours": 2},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },
    2: {  # Wednesday
        "08:00-16:59": {"rate": Decimal("10.00"), "max_hours": 2},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },
    3: {  # Thursday
        "08:00-16:59": {"rate": Decimal("10.00"), "max_hours": 2},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },
    4: {  # Friday
        "08:00-16:59": {"rate": Decimal("10.00"), "max_hours": 2},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },
    5: {  # Saturday
        "08:00-16:59": {"rate": Decimal("3.00"), "max_hours": 4},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },
    6: {  # Sunday
        "08:00-16:59": {"rate": Decimal("2.00"), "max_hours": 8},
        "17:00-23:59": {"rate": Decimal("5.00"), "max_hours": None},
        "00:00-07:59": {"rate": Decimal("20.00"), "max_hours": None, "onetime": True}
    },

}