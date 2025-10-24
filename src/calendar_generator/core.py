__all__ = ['CalendarDate', 'generate_calendar_dates', ]

from datetime import date

from calendar_generator.types import CalendarDate

# Added 0-index placeholder so index matches month.
_MONTHS_COMMON = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
_MONTHS_LEAP   = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def generate_calendar_dates(start_year: int, end_year: int) -> list[CalendarDate]:
    """
    Generates calendar dates using date arithmetic.
    """
    # Initialize all variables to keep alive during loop iterations; loop just reads/writes
    # to these while constructing CalendarDate dictionaries.
    running_year = start_year
    running_quarter = 1
    running_month = 1
    running_day = 1
    running_day_of_year = 1
    running_week = 1
    is_leap_year = (running_year % 4 == 0 and running_year % 100 != 0) or (running_year % 400 == 0)
    days_in_month = _MONTHS_COMMON[running_month] if not is_leap_year else _MONTHS_LEAP[running_month]
    days_in_year = 365 if not is_leap_year else 366
    # At start, these will always be False.
    is_month_end = False
    is_quarter_end = False
    is_year_end = False

    # Set initial start date object to get the weekday number and run weekend check.
    # This is the only instantiation of a date object in the script.
    start_date = date(running_year, running_month, running_day)

    # Get weekday integer and run weekend check; drop start_date from memory.
    running_weekday, start_date = start_date.weekday(), None
    is_weekend = running_weekday >= 5

    # String construction remains same during loop.
    running_date = (f"{running_year}"
                    f"-{running_month if running_month >= 10 else f'0{running_month}'}"
                    f"-{running_day if running_day >= 10 else f'0{running_day}'}")

    # initialize list to accept CalendarDate objects.
    generated: list[CalendarDate] = []
    # Cache append callable to maximize speed.
    append = generated.append

    while running_year <= end_year:
        append(CalendarDate(
            d=running_date,
            year=running_year,
            quarter=running_quarter,
            month=running_month,
            day=running_day,
            day_of_year=running_day_of_year,
            week=running_week,
            weekday=running_weekday,
            days_in_month=days_in_month,
            days_in_year=days_in_year,
            is_weekend=is_weekend,
            is_month_end=is_month_end,
            is_leap_year=is_leap_year,
            is_quarter_end=is_quarter_end,
            is_year_end=is_year_end
        ))

        # Increment base values for next loop.
        running_day = running_day + 1 if not is_month_end else 1
        running_day_of_year = running_day_of_year + 1
        running_week = running_week if running_weekday < 6 else running_week + 1

        # Account for year-end case.
        if is_year_end:
            running_year = running_year + 1
            running_day_of_year = 1
            running_week = 1
            days_in_year = 365 if not is_leap_year else 366
            is_leap_year = (running_year % 4 == 0 and running_year % 100 != 0) or (running_year % 400 == 0)

        # Account for month-end case.
        if is_month_end:
            running_month = running_month + 1 if running_month < 12 else 1
            days_in_month = _MONTHS_COMMON[running_month] if not is_leap_year else _MONTHS_LEAP[running_month]

        # Update values dependent on case checks for next iteration.
        running_weekday = running_weekday + 1 if running_weekday < 6 else 0
        running_quarter = ((running_month - 1) // 3) + 1
        running_date = (f"{running_year}"
                        f"-{running_month if running_month >= 10 else f'0{running_month}'}"
                        f"-{running_day if running_day >= 10 else f'0{running_day}'}")

        # Checks for next iteration.
        is_weekend = running_weekday >= 5
        is_month_end = running_day == days_in_month
        is_quarter_end = (
            (running_month == 3 and running_day == 31) or
            (running_month == 6 and running_day == 30) or
            (running_month == 9 and running_day == 30) or
            (running_month == 12 and running_day == 31)
        )
        is_year_end = running_day_of_year == days_in_year

    return generated


def _is_leap_year(year: int) -> bool:
    """
    Determines whether a given year is a leap year.
    A year is a leap year if it is divisible by 4, or divisible by 100 but not by 400.
    Replaced with inline expression.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def _get_days_in_month(year: int, month: int) -> int:
    """
    Checks to see the day is the last day of the month.
    Replaced with index check.
    """
    if month == 2 and not _is_leap_year(year): return 28
    if month == 2 and _is_leap_year(year): return 29
    if month in {4, 6, 9, 11}: return 30
    if month in {1, 3, 5, 7, 8, 10, 12}: return 31
    raise ValueError(f"Month ({month}) is out of range (1-12).")


def _is_weekend(day: int) -> bool:
    """
    Checks whether the provided day number is a weekend.
    Replaced with inline expression.
    """
    if day in {5, 6}:
        return True
    return False


def _is_quarter_end(month: int, day: int) -> bool:
    """
    Returns True if the month/day match a quarter end combination.
    Replaced by inline expression.
    """
    return (
        (month ==  3 and day == 31) or
        (month ==  6 and day == 30) or
        (month ==  9 and day == 30) or
        (month == 12 and day == 31)
    )


def _increment_month(month: int) -> int:
    """
    Returns 1 if the month provided is 12, else increments by + 1.
    Replaced by inline expression.
    """
    if month >= 12: return 1
    return month + 1


def _is_month_end(year: int, month: int, day: int) -> bool:
    """
    Return True if the given day is the last day of the month.
    Replaced by index check.
    """
    return day == _get_days_in_month(year, month)


def _is_year_end(day_number: int, year: int) -> bool:
    """
    Returns true if the day is 366 for leap years, or 365 for common years.
    Replaced by index check.
    """
    if _is_leap_year(year): return day_number == 366
    return day_number == 365


def _get_days_in_year(is_leap: bool) -> int:
    """
    Returns 366 for leap years, or 365 for typical years.
    Replaced by inline expression.
    """
    if is_leap: return 366
    return 365


