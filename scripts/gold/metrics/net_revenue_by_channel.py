import pandas as pd


def build_net_revenue_by_channel(fact_sales: pd.DataFrame) -> pd.DataFrame:

    net_revenue_by_channel = fact_sales.groupby(
        'channel'
    )['net_amount'].sum().round(2).reset_index(
        name='net_revenue'
    )

    return net_revenue_by_channel