import pandas as pd


def build_net_revenue_by_payment_method(fact_sales: pd.DataFrame) -> pd.DataFrame:

    net_revenue_by_payment_method = fact_sales.groupby(
        'payment_method'
    )['net_amount'].sum().round(2).reset_index(
        name='net_revenue'
    )

    return net_revenue_by_payment_method