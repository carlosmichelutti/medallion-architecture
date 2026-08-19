import pandas as pd

from src.silver.common import (
    normalize_identifier,
    normalize_text,
    parse_boolean,
    parse_date,
    parse_integer,
    parse_money,
)


def transform_products(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe_copy = dataframe.copy()

    dataframe_copy['product_id'] = dataframe_copy['product_id'].map(
        normalize_identifier
    )
    dataframe_copy['sku'] = dataframe_copy['sku'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['product_name'] = dataframe_copy['product_name'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['category'] = dataframe_copy['category'].map(
        normalize_text, case='upper'
    )
    dataframe_copy['unit_price'] = dataframe_copy['unit_price'].map(
        parse_money
    ).astype('float64')
    dataframe_copy['unit_cost'] = dataframe_copy['unit_cost'].map(
        parse_money
    ).astype('float64')
    dataframe_copy['active'] = dataframe_copy['active'].map(
        parse_boolean
    )
    dataframe_copy['stock_quantity'] = dataframe_copy['stock_quantity'].map(
        parse_integer
    )
    dataframe_copy['updated_at'] = dataframe_copy['updated_at'].map(
        parse_date
    )

    return dataframe_copy