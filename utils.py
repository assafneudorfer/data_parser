from datetime import datetime
from struct import Struct
from typing import List, Dict, TextIO

# month that have 31 days
LONG_MONTHS = [1, 3, 5, 7, 8, 10, 12]


def get_current_date(date):
    # split the field date
    year = int(date[:4])
    month = int(date[4:])
    day = 30
    if month == 2:
        day = 28  # for February
    elif month in LONG_MONTHS:
        day = 31
    return datetime(year=year, month=month, day=day)


def check_situation(status):
    # for each potential char
    for c in status:
        if not (c.isdigit() and 1 <= int(c) <= 6):
            return False
    return True


def get_file_name(file_names, ext):
    # will return the first string in the list that end with the extension ext
    return next(filter(lambda x: x.endswith(ext), file_names))


def extract_line(line: bytes, widths: List[int], names: List[str]) -> Dict[str, str]:
    # example format '5s 6s 2s 11s 3x 2s 12s 12s 12s 12s' s the field will be parser x the field will be skip
    format_str = ' '.join(f"{abs(fw)}{'x' if fw < 0 else 's'}" for fw in widths)

    # unpack base on formt and decode the bytes to string
    fields = list(s.decode() for s in Struct(format_str).unpack_from(line))

    # return dict and remove unused char
    fields = {k: v.replace(',', "").replace(" ", "") for k, v in zip(names, fields)}
    return fields
