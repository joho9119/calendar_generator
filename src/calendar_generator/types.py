__all__ = ['CalendarDateDict', ]

from datetime import date
from typing import TypedDict

class CalendarDateDict(TypedDict):
    year: int
    quarter: int
    month: int
    day: int
    day_of_year: int
    week: int
    weekday: int
    days_in_year: int
    is_leap_year: bool
    is_weekend: bool
    is_month_end: bool
    is_quarter_end: bool
    is_year_end: bool

