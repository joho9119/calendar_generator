__all__ = ['generate_calendar_dates_dicts', ]

from datetime import date
from .types import CalendarDateDict


def generate_calendar_dates_dicts(start_year: int, end_year: int) -> list[CalendarDateDict]:
    """
    Generates calendar dates using date arithmetic.
    """

    # initialize variables
    running_year = start_year
    running_quarter = 1
    running_month = 1
    running_day = 1
    running_day_of_year = 1
    running_week = 1
    days_in_year = _get_days_in_year(_is_leap_year(start_year))
    is_leap_year = _is_leap_year(start_year)
    is_month_end = _is_month_end(running_year, running_month, running_day)
    is_quarter_end = _is_quarter_end(running_day, running_month)
    is_year_end = _is_year_end(running_day, running_year)

    # Set initial start date object to get the weekday number and run weekend check.
    # This is adjusted in the loop after initialization, and is the only instantiation of a date object in the script.
    dt = date(running_year, running_month, running_day)

    # Get weekday integer and run weekend check.
    running_weekday = dt.weekday()
    is_weekend = _is_weekend(running_weekday)

    # initialize list that accepts CalendarDate objects.
    generated: list[CalendarDateDict] = []
    append = generated.append


    while running_year <= end_year:

        d = CalendarDateDict(
            year=running_year,
            quarter=running_quarter,
            month=running_month,
            day=running_day,
            day_of_year=running_day_of_year,
            days_in_year=days_in_year,
            week=running_week,
            weekday=running_weekday,
            is_weekend=is_weekend,
            is_month_end=is_month_end,
            is_leap_year=is_leap_year,
            is_quarter_end=is_quarter_end,
            is_year_end=is_year_end
        )

        generated.append(d)

        # increment base values for next loop
        running_month = running_month if not is_month_end else _increment_month(running_month)
        running_quarter = _get_quarter(running_month)
        running_day = running_day + 1 if not is_month_end else 1
        running_weekday = running_weekday + 1 if running_weekday <= 6 else 0

        # Account for year-end case
        if is_year_end:
            running_year = running_year + 1
            running_day_of_year = 1
            running_week = 1
            days_in_year = _get_days_in_year(running_year)
            is_leap_year = _is_leap_year(running_year)
        else:
            running_day_of_year = running_day_of_year + 1
            running_week = running_week if running_weekday <= 6 else running_week + 1

        # check for next loop
        is_month_end = _is_month_end(running_year, running_month, running_day)
        is_year_end = _is_year_end(running_day_of_year, running_year)

    return generated


def _is_leap_year(year: int) -> bool:
    """
    Determines whether a given year is a leap year.
    A year is a leap year if it is divisible by 4, or divisible by 100 but not by 400.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def _get_quarter(month: int) -> int:
    """
    Return the quarter of the year for the given month.
    """
    if month in {1, 2, 3}:
        return 1
    if month in {4, 5, 6}:
        return 2
    if month in {7, 8, 9}:
        return 3
    if month in {10, 11, 12}:
        return 4
    raise ValueError(f"Month ({month}) is out of range (1-12).")


def _get_month_end(year: int, month: int) -> int:
    """Checks to see the day is the last day of the month."""
    if month == 2 and not _is_leap_year(year): return 28
    if month == 2 and _is_leap_year(year): return 29
    if month in {4, 6, 9, 11}: return 30
    if month in {1, 3, 5, 7, 8, 10, 12}: return 31
    raise ValueError(f"Month ({month}) is out of range (1-12).")


def _is_weekend(day: int) -> bool:
    """Checks whether the provided day number is a weekend."""
    if day in {5, 6}:
        return True
    return False


def _is_quarter_end(day: int, month: int) -> bool:
    return (
        (month ==  3 and day == 31) or
        (month ==  6 and day == 30) or
        (month ==  9 and day == 31) or
        (month == 12 and day == 31)
    )


def _increment_month(month: int) -> int:
    """Returns 1 if the month provided is 12, else increments by + 1."""
    if month >= 12: return 1
    return month + 1


def _is_month_end(year: int, month: int, day: int) -> bool:
    """Return True if the given day is the last day of the month."""
    return day == _get_month_end(year, month)


def _is_year_end(day_number: int, year: int) -> bool:
    """Checks to see if the day is 366 for leap years, or 365 for typical years."""
    if _is_leap_year(year): return day_number == 366
    return day_number == 365


def _get_days_in_year(is_leap: bool) -> int:
    """Returns 366 for leap years, or 365 for typical years."""
    if is_leap: return 366
    return 365


