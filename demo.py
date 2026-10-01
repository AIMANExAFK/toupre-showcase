from datetime import date
from booking_rules import DateRange, quote


if __name__ == '__main__':
    result = quote(
        owner_id='demo-owner', renter_id='demo-renter', price_per_day_cents=1250,
        dates=DateRange(date(2026, 10, 10), date(2026, 10, 12)), today=date(2026, 10, 1),
    )
    print(result)
    print('Offline example only. No real booking or payment.')
