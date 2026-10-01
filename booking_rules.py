"""Isolated teaching model, not the private API or a reservation service."""
from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self):
        if self.end < self.start:
            raise ValueError('End date precedes start date')

    def overlaps(self, other):
        return self.start <= other.end and other.start <= self.end


def quote(*, owner_id: str, renter_id: str, price_per_day_cents: int,
          dates: DateRange, today: date, unavailable: Iterable[DateRange] = ()):
    if not owner_id or not renter_id or owner_id == renter_id:
        raise ValueError('A renter cannot book their own listing')
    if dates.start < today:
        raise ValueError('Cannot book in the past')
    if not isinstance(price_per_day_cents, int) or isinstance(price_per_day_cents, bool) or price_per_day_cents <= 0:
        raise ValueError('Price must be a positive number of cents')
    if any(dates.overlaps(period) for period in unavailable):
        raise ValueError('Dates unavailable')
    days = (dates.end - dates.start).days + 1
    return {
        'days': days,
        'total_cents': days * price_per_day_cents,
        'currency': 'EUR',
        'payment_method': 'cash',
        'payment_status': 'cash_to_collect',
    }
