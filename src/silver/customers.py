import re
from typing import Any

import pandas as pd

from src.silver.common import (
    is_null,
    normalize_identifier,
    normalize_text,
    parse_date,
)


def validate_cpf(value: Any) -> str | None:

    if is_null(value):
        return None

    normalized = str(value).strip()
    normalized = re.sub(r'\D', '', normalized)

    if len(normalized) != 11:
        return None

    return normalized

def validate_email(value) -> str | None:

    if is_null(value):
        return None

    normalized = str(value).strip()
    normalized = re.sub(r'\s', '', normalized)

    if not re.match(r'[^@]+@[^@]+\.[^@]+', normalized):
        return None

    return normalized

def parse_telephone(value) -> str | None:

    if is_null(value):
        return None

    normalized = str(value).strip()
    normalized = re.sub(r'\D', '', normalized)
    normalized = normalized.removeprefix('55')

    if len(normalized) not in [10, 11]:
        return None

    normalized = f'+55{normalized}'

    return normalized

def transform_customers(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe_copy = dataframe.copy()

    dataframe_copy['customer_id'] = dataframe_copy['customer_id'].map(
        normalize_identifier
    )
    dataframe_copy['name'] = dataframe_copy['name'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['email'] = dataframe_copy['email'].map(
        validate_email
    )
    dataframe_copy['email'] = dataframe_copy['email'].map(
        normalize_text, case='lower'
    )
    dataframe_copy['cpf'] = dataframe_copy['cpf'].map(
        validate_cpf
    )
    dataframe_copy['phone'] = dataframe_copy['phone'].map(
        parse_telephone
    )
    dataframe_copy['city'] = dataframe_copy['city'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['state'] = dataframe_copy['state'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['registration_date'] = dataframe_copy['registration_date'].map(
        parse_date
    )
    dataframe_copy['updated_at'] = dataframe_copy['updated_at'].map(
        parse_date
    )

    return dataframe_copy