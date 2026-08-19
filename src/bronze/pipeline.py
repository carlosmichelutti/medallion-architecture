import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.bronze.config import SOURCES, SourceConfig
from src.bronze.readers import read_source

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / 'data' / 'bronze'

def value_to_raw_string(value: Any) -> str | None:

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True
        )

    return str(value)

def convert_business_columns_to_string(dataframe: pd.DataFrame) -> pd.DataFrame:

    dataframe_copy = dataframe.copy()

    for column in dataframe_copy.columns:
        dataframe_copy[column] = dataframe_copy[column].map(value_to_raw_string)

    return dataframe_copy

def calculate_record_hash(
    dataframe: pd.DataFrame,
    business_columns: list[str]
) -> pd.Series:

    def hash_row(row: pd.Series) -> str:

        serialized_record = {
            column: row[column]
            for column in business_columns
        }

        payload = json.dumps(
            serialized_record,
            ensure_ascii=False,
            sort_keys=True,
            default=str
        )

        return hashlib.sha256(
            payload.encode('utf-8')
        ).hexdigest()

    return dataframe.apply(hash_row, axis=1)

def add_bronze_metadata(
    dataframe: pd.DataFrame,
    source_path: Path,
    batch_id: str,
    ingestion_timestamp: datetime
) -> pd.DataFrame:

    dataframe_copy = dataframe.copy()
    dataframe_columns = dataframe_copy.columns.to_list()

    dataframe_copy['_source_file'] = source_path.name
    dataframe_copy['_source_extension'] = source_path.suffix.lower()
    dataframe_copy['_source_path'] = str(source_path)
    dataframe_copy['_source_row_number'] = range(1, len(dataframe_copy) + 1)
    dataframe_copy['_ingestion_batch_id'] = batch_id
    dataframe_copy['_ingested_at_utc'] = ingestion_timestamp
    dataframe_copy['_record_hash'] = calculate_record_hash(dataframe_copy, dataframe_columns)

    return dataframe_copy

def build_output_path(dataset_name: str) -> Path:

    output_directory = BRONZE_DIR / dataset_name

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_directory / f'{dataset_name}.parquet'

def ingest_source(config: SourceConfig, batch_id: str) -> str:

    ingestion_timestamp = datetime.now(timezone.utc)

    dataframe = read_source(
        file_path=config.source_path,
        reader_options=config.reader_options
    )

    dataframe = convert_business_columns_to_string(
        dataframe=dataframe
    )

    dataframe = add_bronze_metadata(
        dataframe=dataframe,
        source_path=config.source_path,
        batch_id=batch_id,
        ingestion_timestamp=ingestion_timestamp
    )

    output_path = build_output_path(
        dataset_name=config.dataset_name
    )

    dataframe.to_parquet(
        path=output_path,
        engine='pyarrow',
        index=False
    )

    print(f'[BRONZE] {config.file_name}: {len(dataframe)} record(s) -> {output_path}')

    return output_path.as_posix()

def run_bronze(batch_id: str | None = None) -> list[str]:

    generated_files = []
    batch_id = batch_id or datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    for source_config in SOURCES:
        try:
            output_path = ingest_source(source_config, batch_id)
            generated_files.append(output_path)
        except (FileNotFoundError, OSError, ValueError) as error:
            print(f'[ERROR] Processing failed {source_config.file_name}: {error}')

    return generated_files