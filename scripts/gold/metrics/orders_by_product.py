import pandas as pd


def build_orders_by_product(fact_sales: pd.DataFrame) -> pd.DataFrame:

    orders_by_product = fact_sales.groupby(
        'product_id'
    )['order_id'].nunique().reset_index(
        name='total_orders'
    )

    return orders_by_product