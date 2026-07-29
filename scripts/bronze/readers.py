import json
from pathlib import Path
from typing import Any

import pandas as pd


def read_csv_file(file_path: Path, **options: Any) -> pd.DataFrame:

    return pd.read_csv(
        file_path,
        dtype=object,
        keep_default_na=False,
        **options
    )

def read_excel_file(file_path: Path, **options: Any) -> pd.DataFrame:

    return pd.read_excel(
        file_path,
        dtype=object,
        keep_default_na=False,
        **options
    )

def read_json_file(file_path: Path, **options: Any) -> pd.DataFrame:

    with file_path.open('r', encoding='utf-8') as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise TypeError(
            f'The file {file_path.name} does not contain a list of records.'
        )

    return pd.json_normalize(
        records,
        sep='__',
        **options
    )

READERS = {
    '.csv': read_csv_file,
    '.xlsx': read_excel_file,
    '.xls': read_excel_file,
    '.json': read_json_file
}

def read_source(
    file_path: Path,
    reader_options: dict[str, Any] | None
) -> pd.DataFrame:

    extension = file_path.suffix.lower()
    reader = READERS.get(extension)
    if reader is None:
        raise ValueError(
            f'Unsupported extension: {extension}. '
            f'File: {file_path.name}'
        )

    return reader(file_path=file_path, **(reader_options or {}))