import pandas as pd


def build_gross_revenue(fact_sales: pd.DataFrame) -> pd.DataFrame:

    gross_revenue = pd.DataFrame(
        [
            fact_sales['gross_amount'].sum().round(2)
        ],
        columns=['gross_revenue']
    )

    return gross_revenue