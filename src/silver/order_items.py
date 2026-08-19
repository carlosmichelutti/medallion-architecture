import pandas as pd

from src.silver.common import (
    normalize_identifier,
    normalize_percentage,
    parse_integer,
    parse_money,
)


def transform_order_items(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe_copy = dataframe.copy()

    dataframe_copy['order_item_id'] = dataframe_copy['order_item_id'].map(
        normalize_identifier
    )
    dataframe_copy['order_id'] = dataframe_copy['order_id'].map(
        normalize_identifier
    )
    dataframe_copy['product_id'] = dataframe_copy['product_id'].map(
        normalize_identifier
    )
    dataframe_copy['quantity'] = dataframe_copy['quantity'].map(
        parse_integer
    )
    dataframe_copy['unit_price'] = dataframe_copy['unit_price'].map(
        parse_money
    ).astype('float64')
    dataframe_copy['discount'] = dataframe_copy['discount'].map(
        normalize_percentage
    ).astype('float64')
    dataframe_copy['gross_amount'] = (
        dataframe_copy['quantity'] * dataframe_copy['unit_price']
    ).astype('float64').round(2)
    dataframe_copy['discount_amount'] = (
        (dataframe_copy['gross_amount'] / 100) * dataframe_copy['discount']
    ).astype('float64').round(2)
    dataframe_copy['net_amount'] = (
        dataframe_copy['gross_amount'] - dataframe_copy['discount_amount']
    ).astype('float64').round(2)

    return dataframe_copy