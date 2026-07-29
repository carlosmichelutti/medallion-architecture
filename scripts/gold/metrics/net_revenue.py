import pandas as pd


def build_net_revenue(fact_sales: pd.DataFrame) -> pd.DataFrame:

    net_revenue = pd.DataFrame(
        [
            (fact_sales['net_amount']).sum().round(2)
        ],
        columns=['net_revenue']
    )

    return net_revenue