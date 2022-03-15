from calendar import monthrange
from datetime import datetime, time, date


def convert_str_to_date(date_as_string: str) -> datetime:
    datetime_obj = datetime.strptime(date_as_string, "%Y%m%d")
    return datetime_obj


def generate_datetime(min_or_max_datetime: str = "min"):
    if min_or_max_datetime == "min":
        return datetime.combine(date.today().replace(day=1), time.min)
    last_day_in_month = date.today()
    last_day_in_month = last_day_in_month.replace(day=monthrange(last_day_in_month.year, last_day_in_month.month)[1])
    return datetime.combine(last_day_in_month, time.max)
