import re
from typing import Any

import pandas as pd

from src.silver.common import (
    is_null,
    normalize_identifier,
    normalize_text,
    parse_date,
    parse_integer,
    parse_money,
)


def parse_channel(value: Any) -> str | None:

    if is_null(value):
        return None

    normalized = str(value).strip().upper()
    normalized = re.sub(r'\s+', '_', normalized)

    return normalized

def transform_orders(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe_copy = dataframe.copy()

    dataframe_copy['order_id'] = dataframe_copy['order_id'].map(
        normalize_identifier
    )
    dataframe_copy['customer_id'] = dataframe_copy['customer_id'].map(
        normalize_identifier
    )
    dataframe_copy['order_date'] = dataframe_copy['order_date'].map(
        parse_date
    )
    dataframe_copy['status'] = dataframe_copy['status'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['channel'] = dataframe_copy['channel'].map(
        parse_channel
    )
    dataframe_copy['shipping_fee'] = dataframe_copy['shipping_fee'].map(
        parse_money
    ).astype('float64')
    dataframe_copy['coupon'] = dataframe_copy['coupon'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['total_amount'] = dataframe_copy['total_amount'].map(
        parse_money
    ).astype('float64')
    dataframe_copy['updated_at'] = dataframe_copy['updated_at'].map(
        parse_date
    )
    dataframe_copy['payment__method'] = dataframe_copy['payment__method'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['payment__installments'] = dataframe_copy['payment__installments'].map(
        parse_integer
    )
    dataframe_copy['shipping_address__city'] = dataframe_copy['shipping_address__city'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['shipping_address__state'] = dataframe_copy['shipping_address__state'].map(
        normalize_text, case='upper'
    )

    return dataframe_copy