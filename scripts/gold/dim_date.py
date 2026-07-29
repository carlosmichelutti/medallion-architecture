from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'
GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

COLUMNS = {
    'date_id': 'date_id',
    'date': 'date',
    'year': 'year',
    'quarter': 'quarter',
    'month': 'month',
    'month_name': 'month_name',
    'day': 'day',
    'day_of_week': 'day_of_week',
}

def build_dim_date() -> pd.DataFrame:

    dataframe = pd.read_parquet(
        SILVER_DIR /
        'orders' /
        'data.parquet'
    )

    start_date = dataframe['order_date'].min().date()
    finish_date = dataframe['order_date'].max().date()

    dates = pd.date_range(
        start=start_date,
        end=finish_date,
        freq='D'
    )

    dim_date = pd.DataFrame(dates, columns=['date'])

    dim_date['date_id'] = (
        dim_date['date'].dt.strftime('%Y%m%d').astype(int)
    )

    dim_date['year'] = dim_date['date'].dt.year
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['month_name'] = dim_date['date'].dt.month_name()
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['day_of_week'] = dim_date['date'].dt.dayofweek

    dim_date = dim_date[COLUMNS.keys()]

    return dim_date

def build_output_path() -> Path:

    output_path = GOLD_DIR / 'dim_date'

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_path / 'dim_date.parquet'

def save_dim_date() -> tuple[Path, pd.DataFrame]:

    dim_date = build_dim_date()
    output_path = build_output_path()

    dim_date.to_parquet(
        output_path,
        index=False
    )

    return output_path, dim_date