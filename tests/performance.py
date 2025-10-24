

def run_performance_test(
        run_start: int = 1900,
        run_end: int = 2100,
        iterations: int = 100) -> None:
    print("=== generate_calendar_dates (dicts) ===")
    _test_loop_performance_dicts(run_start, run_end, iterations)
    print("\n=== datetime.date/timedelta ===")
    _test_loop_performance_datetime(run_start, run_end, iterations)
    print("\n=== calendar.Calendar.itermonthdates ===")
    _test_loop_performance_calendar(run_start, run_end, iterations)


def _test_loop_performance_dicts(
        run_start: int,
        run_end: int,
        iterations: int = 100) -> None:
    """
    Measures loop performance using basic timestamps. Defaults to 100 loops.
    """
    import time
    from calendar_generator import generate_calendar_dates

    data = []

    start_time = time.perf_counter()

    for r in range(0, iterations):
        data = generate_calendar_dates(run_start, run_end)

    end_time = time.perf_counter()

    avg_per_loop = (end_time-start_time)/iterations

    print(f"Completed {iterations} iterations.")
    print(f"Generated {len(data)} CalendarDate records.")
    print(f"Elapsed time: {end_time - start_time:.4f} seconds.")
    print(f"Avg. time per loop: {avg_per_loop:.4f} seconds.")
    for d in data[:10]:
        print(d) # show sample


def _test_loop_performance_datetime(
        start_year: int,
        end_year: int,
        num_loops: int = 100) -> None:
    """
    Measures loop performance using datetime.date and timedelta.
    """
    import time
    import datetime

    data = []
    start_time = time.perf_counter()
    for r in range(num_loops):
        data = []
        d = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        while d <= end_date:
            # Generate all equivalent fields as in CalendarDateDict
            year = d.year
            month = d.month
            day = d.day
            quarter = ((month - 1) // 3) + 1
            day_of_year = (d - datetime.date(year, 1, 1)).days + 1
            iso_year, iso_week, iso_weekday = d.isocalendar()
            is_weekend = d.weekday() >= 5
            # is_month_end: next day is in next month
            next_day = d + datetime.timedelta(days=1)
            is_month_end = next_day.month != month
            # is_quarter_end: next day is in next quarter
            is_quarter_end = ((next_day.month - 1) // 3) + 1 != quarter
            # is_year_end: next day is in next year
            is_year_end = next_day.year != year
            # is_leap_year
            is_leap_year = (
                year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
            )
            data.append({
                "date": d.isoformat(),
                "year": year,
                "month": month,
                "day": day,
                "quarter": quarter,
                "day_of_year": day_of_year,
                "iso_year": iso_year,
                "iso_week": iso_week,
                "iso_weekday": iso_weekday,
                "is_weekend": is_weekend,
                "is_month_end": is_month_end,
                "is_quarter_end": is_quarter_end,
                "is_year_end": is_year_end,
                "is_leap_year": is_leap_year,
            })
            d += datetime.timedelta(days=1)

    end_time = time.perf_counter()

    avg_per_loop = (end_time-start_time)/num_loops

    print(f"Completed {num_loops} iterations. (datetime)")
    print(f"Generated {len(data)} CalendarDate records.")
    print(f"Elapsed time: {end_time - start_time:.4f} seconds.")
    print(f"Avg. time per loop: {avg_per_loop:.4f} seconds.")
    print(data[:10])  # show sample


def _test_loop_performance_calendar(start_year: int, end_year: int, num_loops: int = 100) -> None:
    """
    Measures loop performance using calendar.Calendar().itermonthdates.
    """
    import time
    import calendar
    import datetime

    data = []
    start_time = time.perf_counter()
    for r in range(num_loops):
        data = []
        cal = calendar.Calendar()
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                for d in cal.itermonthdates(year, month):
                    if d.year == year and d.month == month:
                        # Generate all equivalent fields as in CalendarDateDict
                        day = d.day
                        quarter = ((month - 1) // 3) + 1
                        day_of_year = (d - datetime.date(year, 1, 1)).days + 1
                        iso_year, iso_week, iso_weekday = d.isocalendar()
                        is_weekend = d.weekday() >= 5
                        next_day = d + datetime.timedelta(days=1)
                        is_month_end = next_day.month != month
                        is_quarter_end = ((next_day.month - 1) // 3) + 1 != quarter
                        is_year_end = next_day.year != year
                        is_leap_year = (
                            year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
                        )
                        data.append({
                            "date": d.isoformat(),
                            "year": year,
                            "month": month,
                            "day": day,
                            "quarter": quarter,
                            "day_of_year": day_of_year,
                            "iso_year": iso_year,
                            "iso_week": iso_week,
                            "iso_weekday": iso_weekday,
                            "is_weekend": is_weekend,
                            "is_month_end": is_month_end,
                            "is_quarter_end": is_quarter_end,
                            "is_year_end": is_year_end,
                            "is_leap_year": is_leap_year,
                        })
    end_time = time.perf_counter()
    avg_per_loop = (end_time-start_time)/num_loops
    print(f"Completed {num_loops} iterations. (calendar)")
    print(f"Generated {len(data)} CalendarDate records.")
    print(f"Elapsed time: {end_time - start_time:.4f} seconds.")
    print(f"Avg. time per loop: {avg_per_loop:.4f} seconds.")
    print(data[:10])  # show sample


run_performance_test()