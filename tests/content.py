from calendar_generator import generate_calendar_dates

# Month lengths and cumulative day-of-year tables
_MONTH_LEN_COMMON = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
_MONTH_LEN_LEAP   = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
_CUM_COMMON = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
_CUM_LEAP   = (0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335)

def _is_leap_year(y: int) -> bool:
    return (y % 4 == 0) and (y % 100 != 0 or y % 400 == 0)


def _month_len(y: int, m: int) -> int:
    return (_MONTH_LEN_LEAP if _is_leap_year(y) else _MONTH_LEN_COMMON)[m - 1]


def _day_of_year(y: int, m: int, d: int) -> int:
    base = _CUM_LEAP if _is_leap_year(y) else _CUM_COMMON
    return base[m - 1] + d


def _month_len_py(y, m):
    return _month_len(y, m)


def test_no_invalid_days_1900():
    rows = generate_calendar_dates(1900, 1900)
    assert len(rows) == 365
    for r in rows:
        assert 1 <= r["month"] <= 12
        assert 1 <= r["day"] <= _month_len_py(r["year"], r["month"])
    print("Test passed.")


def test_doy_monotonic_per_year_1900():
    rows = [r for r in generate_calendar_dates(1900, 1900)]
    assert rows[0]["day_of_year"] == 1
    assert rows[-1]["day_of_year"] == 365
    for i in range(1, len(rows)):
        assert rows[i]["day_of_year"] == rows[i-1]["day_of_year"] + 1
    print("Test passed.")


test_no_invalid_days_1900()
test_doy_monotonic_per_year_1900()