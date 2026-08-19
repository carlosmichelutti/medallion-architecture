from pathlib import Path

import pandas as pd

from src.silver.customers import transform_customers
from src.silver.order_items import transform_order_items
from src.silver.orders import transform_orders
from src.silver.products import transform_products

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / 'data' / 'bronze'
SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'

TRANSFORMERS = {
    'customers': transform_customers,
    'products': transform_products,
    'orders': transform_orders,
    'order_items': transform_order_items,
}

def build_output_path(dataset_name: str) -> Path:

    output_directory = SILVER_DIR / dataset_name

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_directory / f'{dataset_name}.parquet'

def process_dataset(dataset_name: str) -> str:

    dataframe = pd.read_parquet(
        BRONZE_DIR /
        dataset_name /
        f'{dataset_name}.parquet'
    )

    transformer = TRANSFORMERS[dataset_name]

    transformed_dataframe = transformer(dataframe)

    output_path = build_output_path(
        dataset_name=dataset_name
    )

    transformed_dataframe.to_parquet(
        path=output_path,
        index=False
    )

    print(f'[SILVER] {dataset_name}: {len(transformed_dataframe)} record(s) -> {output_path}')

    return output_path.as_posix()

def run_silver() -> list[str]:

    generated_files = []
    for dataset_name in TRANSFORMERS:
        try:
            output = process_dataset(dataset_name)
            generated_files.append(output)
        except (FileNotFoundError, KeyError, ValueError) as error:
            print(f'[ERROR] Silver layer processing failed: {error}')

    return generated_files