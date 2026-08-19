import pandas as pd


def build_orders_by_customer(fact_sales: pd.DataFrame) -> pd.DataFrame:

    orders_by_customer = fact_sales.groupby(
        'customer_id'
    )['order_id'].nunique().reset_index(
        name='total_orders'
    )

    return orders_by_customer