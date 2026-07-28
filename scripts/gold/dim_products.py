from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'
GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

COLUMNS = {
    'product_id': 'product_id',
    'sku': 'sku',
    'product_name': 'product_name',
    'category': 'category',
    'unit_price': 'unit_price',
    'unit_cost': 'unit_cost',
    'active': 'active',
    'stock_quantity': 'stock_quantity',
}

def build_dim_products() -> pd.DataFrame:

    dataframe = pd.read_parquet(
        SILVER_DIR /
        'products' /
        'data.parquet'
    )

    dim_products = dataframe[COLUMNS.keys()]

    dim_products = dim_products.rename(
        columns=COLUMNS
    )

    dim_products = dim_products.reset_index(
        drop=True
    )

    dim_products.insert(
        0,
        'product_key',
        range(1, len(dim_products) + 1)
    )

    return dim_products

def build_output_path() -> Path:

    output_path = GOLD_DIR / 'dim_products'

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_path / 'dim_products.parquet'

def save_dim_products() -> tuple[Path, pd.DataFrame]:

    dim_products = build_dim_products()
    output_path = build_output_path()

    dim_products.to_parquet(
        output_path,
        index=False
    )

    return output_path, dim_products