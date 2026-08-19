from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'
GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

COLUMNS = {
    'customer_id': 'customer_id',
    'name': 'customer_name',
    'email': 'email',
    'cpf': 'cpf',
    'phone': 'phone',
    'city': 'city',
    'state': 'state',
    'registration_date': 'registration_date',
}

def build_dim_customers() -> pd.DataFrame:

    dataframe = pd.read_parquet(
        SILVER_DIR /
        'customers' /
        'customers.parquet'
    )

    dim_customers = dataframe[COLUMNS.keys()]

    dim_customers = dim_customers.rename(
        columns=COLUMNS
    )

    dim_customers = dim_customers.reset_index(
        drop=True
    )

    dim_customers.insert(
        0,
        'customer_key',
        range(1, len(dim_customers) + 1)
    )

    return dim_customers

def build_output_path() -> Path:

    output_path = GOLD_DIR / 'dim_customers'

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_path / 'dim_customers.parquet'

def save_dim_customers() -> tuple[Path, pd.DataFrame]:

    dim_customers = build_dim_customers()
    output_path = build_output_path()

    dim_customers.to_parquet(
        output_path,
        index=False
    )

    return output_path, dim_customers