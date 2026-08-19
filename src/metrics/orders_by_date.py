import pandas as pd


def build_orders_by_date(fact_sales: pd.DataFrame) -> pd.DataFrame:

    orders_by_date = fact_sales.groupby(
        fact_sales['order_date'].dt.date
    )['order_id'].nunique().reset_index(
        name='total_orders'
    )

    return orders_by_date