from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / 'data' / 'raw'

@dataclass(frozen=True)
class SourceConfig:
    source_path: Path
    file_name: str
    dataset_name: str
    reader_options: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source_path.exists():
            raise FileNotFoundError(
                f'The source file {self.source_path} does not exist.'
            )

SOURCES = [
    SourceConfig(
        source_path=RAW_DIR / 'customers' / 'customers.csv',
        file_name='customers.csv',
        dataset_name='customers',
        reader_options={
            'sep': ',',
            'encoding': 'utf-8'
        }
    ),
    SourceConfig(
        source_path=RAW_DIR / 'products' / 'products.xlsx',
        file_name='products.xlsx',
        dataset_name='products',
        reader_options={
            'sheet_name': 'products_raw'
        }
    ),
    SourceConfig(
        source_path=RAW_DIR / 'orders' / 'orders.json',
        file_name='orders.json',
        dataset_name='orders'
    ),
    SourceConfig(
        source_path=RAW_DIR / 'order_items' / 'order_items.csv',
        file_name='order_items.csv',
        dataset_name='order_items',
        reader_options={
            'sep': ';',
            'encoding': 'utf-8'
        }
    ),
]