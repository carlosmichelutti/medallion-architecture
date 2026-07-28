from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'
GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

COLUMNS = {
    'order_id': 'order_id',
    'customer_id': 'customer_id',
    'order_date': 'order_date',
    'status': 'status',
    'channel': 'channel',
    'shipping_fee': 'shipping_fee',
    'coupon': 'coupon',
    'total_amount': 'total_amount',
    'payment__method': 'payment_method',
    'order_item_id': 'order_item_id',
    'product_id': 'product_id',
    'quantity': 'quantity',
    'unit_price': 'unit_price',
    'discount': 'discount_rate',
    'customer_key': 'customer_key',
    'product_key': 'product_key',
}

def build_fact_sales() -> pd.DataFrame:

    orders = pd.read_parquet(
        SILVER_DIR /
        'orders' /
        'data.parquet'
    )

    order_items = pd.read_parquet(
        SILVER_DIR /
        'order_items' /
        'data.parquet'
    )

    dim_customers = pd.read_parquet(
        GOLD_DIR /
        'dim_customers' /
        'dim_customers.parquet'
    )

    dim_products = pd.read_parquet(
        GOLD_DIR /
        'dim_products' /
        'dim_products.parquet'
    )

    dim_date = pd.read_parquet(
        GOLD_DIR /
        'dim_date' /
        'dim_date.parquet'
    )

    fact_sales = orders.merge(
        order_items,
        left_on='order_id',
        right_on='order_id',
        how='inner'
    )

    fact_sales.insert(0, 'date_id', fact_sales['order_date'].dt.strftime('%Y%m%d').astype(int))

    fact_sales = fact_sales.merge(
        dim_customers[
            [
                'customer_key',
                'customer_id'
            ]
        ],
        left_on='customer_id',
        right_on='customer_id',
        how='inner'
    )

    fact_sales = fact_sales.merge(
        dim_products[
            [
                'product_key',
                'product_id'
            ]
        ],
        left_on='product_id',
        right_on='product_id',
        how='inner'
    )

    fact_sales = fact_sales.merge(
        dim_date[
            'date_id'
        ],
        left_on='date_id',
        right_on='date_id',
        how='inner'
    )

    fact_sales = fact_sales[COLUMNS.keys()]
    fact_sales = fact_sales.rename(columns=COLUMNS)

    return fact_sales

def build_output_path() -> Path:

    output_path = GOLD_DIR / 'fact_sales'

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_path / 'fact_sales.parquet'

def save_fact_sales() -> tuple[Path, pd.DataFrame]:

    fact_sales = build_fact_sales()
    output_path = build_output_path()

    fact_sales.to_parquet(
        output_path,
        index=False
    )

    return output_path, fact_sales