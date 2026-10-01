from datetime import date
import unittest
from booking_rules import DateRange, quote


class BookingRulesTests(unittest.TestCase):
    def setUp(self):
        self.args = dict(owner_id='demo-owner', renter_id='demo-renter', price_per_day_cents=1250,
                         today=date(2026, 10, 1), dates=DateRange(date(2026, 10, 10), date(2026, 10, 12)))

    def test_inclusive_dates_and_cash_at_handover(self):
        result = quote(**self.args)
        self.assertEqual(result, dict(days=3, total_cents=3750, currency='EUR', payment_method='cash', payment_status='cash_to_collect'))

    def test_one_day(self):
        result = quote(**{**self.args, 'dates': DateRange(date(2026, 10, 10), date(2026, 10, 10))})
        self.assertEqual(result['days'], 1)

    def test_owner_cannot_rent_to_self(self):
        with self.assertRaises(ValueError):
            quote(**{**self.args, 'renter_id': 'demo-owner'})

    def test_past_and_inverted_dates(self):
        with self.assertRaises(ValueError):
            quote(**{**self.args, 'today': date(2026, 10, 11)})
        with self.assertRaises(ValueError):
            DateRange(date(2026, 10, 12), date(2026, 10, 10))

    def test_overlap_boundaries_are_inclusive(self):
        for start, end in [(9, 10), (10, 12), (11, 11), (12, 15), (1, 30)]:
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                quote(**self.args, unavailable=[DateRange(date(2026, 10, start), date(2026, 10, end))])

    def test_adjacent_days_remain_available(self):
        result = quote(**self.args, unavailable=[DateRange(date(2026, 10, 8), date(2026, 10, 9)), DateRange(date(2026, 10, 13), date(2026, 10, 14))])
        self.assertEqual(result['days'], 3)

    def test_invalid_prices(self):
        for value in [0, -1, 1.25, True, '1250']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                quote(**{**self.args, 'price_per_day_cents': value})


if __name__ == '__main__':
    unittest.main()
