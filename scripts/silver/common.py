import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

import pandas as pd

NULL_STRINGS = [
    '',
    'N/A',
    'NA',
    'NONE',
    'NULL',
]

DATE_FORMATS = [
    '%Y-%m-%dT%H:%M:%S%z',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%d-%m-%Y %H:%M:%S',
    '%d/%m/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M',
    '%d/%m/%Y',
    '%d-%m-%Y',
    '%m-%d-%Y %H:%M:%S',
    '%m/%d/%Y %H:%M:%S',
    '%m/%d/%Y %H:%M',
    '%m/%d/%Y',
    '%m-%d-%Y',
]

BOOLEN_VALUES = {
    'TRUE': True,
    'T': True,
    'YES': True,
    'ACTIVE': True,
    'Y': True,
    '1': True,
    1: True,
    'FALSE': False,
    'F': False,
    'NO': False,
    'INACTIVE': False,
    'N': False,
    '0': False,
    0: False,
}

def is_null(value: Any) -> bool:

    if value is None:
        return True

    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass

    if isinstance(value, str):
        normalized = value.strip().upper()
        if normalized in NULL_STRINGS:
            return True

    return False

def normalize_text(value: Any, case: Literal['upper', 'lower', 'title']) -> str | None:

    if case not in ['upper', 'lower', 'title']:
        raise ValueError(f'Invalid case option: {case}. Must be one of "upper", "lower", or "title".')

    if is_null(value):
        return None

    normalized = str(value).strip()
    normalized = re.sub(r'\s+', ' ', normalized)

    if case == 'upper':
        normalized = normalized.upper()
    elif case == 'lower':
        normalized = normalized.lower()
    elif case == 'title':
        normalized = normalized.title()

    return normalized

def normalize_identifier(value: Any) -> str | None:

    if is_null(value):
        return None

    normalized = str(value).strip().upper()
    normalized = re.sub(r'\s+', '', normalized)

    return normalized

def normalize_percentage(value: Any) -> float | None:

    if is_null(value):
        return None

    if isinstance(value, (int, float)):
        if 0 <= value <= 1:
            return value * 100
        if 1 < value <= 100:
            return value
        return None

    normalized = str(value).strip()
    normalized = re.sub(r'[^\d+.]', '', normalized)

    if not normalized:
        return None

    normalized = float(normalized)

    if 0 <= normalized <= 1:
        return normalized * 100
    if 1 < normalized <= 100:
        return normalized
    return None

def parse_money(value: Any) -> Decimal | None:

    if is_null(value):
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, Decimal):
        return value

    if isinstance(value, (int, float)):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None

    normalized = str(value).strip()
    normalized = re.sub(r'[^\d,.\-+]', '', normalized)

    if not normalized:
        return None

    first_comma = normalized.find(',')
    first_dot = normalized.find('.')

    if ',' in normalized and '.' not in normalized:
        normalized = normalized.replace(',', '.')

    if first_comma != -1 and first_dot != -1:
        if first_comma < first_dot:
            normalized = normalized.replace(',', '')
        else:
            normalized = normalized.replace('.', '')
            normalized = normalized.replace(',', '.')

    return Decimal(normalized)

def parse_integer(value: Any) -> int | None:

    if is_null(value):
        return None

    if isinstance(value, int):
        return value

    normalized = str(value).strip()
    normalized = re.sub(r'[^\d\-+]', '', normalized)

    if not normalized:
        return None

    return int(normalized)

def parse_date(value: Any) -> datetime | None:

    if is_null(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    text = str(value).strip()

    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(
                text,
                date_format
            )
        except ValueError:
            continue

    return None

def parse_boolean(value: Any):

    if is_null(value):
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)) and value in [0, 1]:
        return BOOLEN_VALUES.get(value)

    if isinstance(value, str) and value.strip().upper() in BOOLEN_VALUES:
        normalized = value.strip().upper()
        return BOOLEN_VALUES.get(normalized)

    return None