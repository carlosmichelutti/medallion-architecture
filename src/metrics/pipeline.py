from pathlib import Path

import pandas as pd

from database.writer import write_dataframe_to_table
from src.metrics.gross_revenue import build_gross_revenue
from src.metrics.net_revenue import build_net_revenue
from src.metrics.net_revenue_by_channel import build_net_revenue_by_channel
from src.metrics.net_revenue_by_payment_method import (
    build_net_revenue_by_payment_method,
)
from src.metrics.orders_by_customer import build_orders_by_customer
from src.metrics.orders_by_date import build_orders_by_date
from src.metrics.orders_by_product import build_orders_by_product

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

def run_metrics() -> None:

    fact_sales = pd.read_parquet(
        GOLD_DIR /
        'fact_sales' /
        'fact_sales.parquet'
    )

    gross_revenue = build_gross_revenue(fact_sales)
    net_revenue = build_net_revenue(fact_sales)
    net_revenue_by_channel = build_net_revenue_by_channel(fact_sales)
    net_revenue_by_payment_method = build_net_revenue_by_payment_method(fact_sales)
    orders_by_customer = build_orders_by_customer(fact_sales)
    orders_by_date = build_orders_by_date(fact_sales)
    orders_by_product = build_orders_by_product(fact_sales)

    write_dataframe_to_table(gross_revenue, 'gross_revenue')
    write_dataframe_to_table(net_revenue, 'net_revenue')
    write_dataframe_to_table(net_revenue_by_channel, 'net_revenue_by_channel')
    write_dataframe_to_table(net_revenue_by_payment_method, 'net_revenue_by_payment_method')
    write_dataframe_to_table(orders_by_customer, 'orders_by_customer')
    write_dataframe_to_table(orders_by_date, 'orders_by_date')
    write_dataframe_to_table(orders_by_product, 'orders_by_product')