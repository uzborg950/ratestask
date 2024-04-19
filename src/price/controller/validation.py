from datetime import datetime

from src.utils.constants import DATE_FORMAT


def validate_date(value: str) -> bool:
    try:
        datetime.strptime(value, DATE_FORMAT)
        return True
    except:
        return False
