from pathlib import Path

from src.gold.dim_customers import save_dim_customers
from src.gold.dim_date import save_dim_date
from src.gold.dim_products import save_dim_products
from src.gold.fact_sales import save_fact_sales

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'
GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

TRANSFORMERS = {
    'dim_customers': save_dim_customers,
    'dim_date': save_dim_date,
    'dim_products': save_dim_products,
    'fact_sales': save_fact_sales,
}

def process_dataset(dataset_name: str) -> str:

    transformer = TRANSFORMERS[dataset_name]

    output_path, transformed_dataframe = transformer()

    print(f'[GOLD] {dataset_name}: {len(transformed_dataframe)} record(s) -> {output_path}')

    return output_path.as_posix()

def run_gold() -> list[str]:

    generated_files = []
    for dataset_name in TRANSFORMERS:
        try:
            output = process_dataset(dataset_name)
            generated_files.append(output)
        except (FileNotFoundError, KeyError, ValueError) as error:
            print(f'[ERROR] Gold layer processing failed: {error}')

    return generated_files