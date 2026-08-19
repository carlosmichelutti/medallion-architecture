from src.bronze.pipeline import run_bronze
from src.gold.pipeline import run_gold
from src.metrics.pipeline import run_metrics
from src.silver.pipeline import run_silver


def main() -> None:

    print('Starting Medallion pipeline...')

    bronze_files = run_bronze()

    print(f'Bronze layer completed. {len(bronze_files)} files generated.')

    silver_files = run_silver()

    print(f'Silver layer completed. {len(silver_files)} files generated.')

    gold_files = run_gold()

    print(f'Gold layer completed. {len(gold_files)} files generated.')

    run_metrics()

    print('Metrics layer completed.')

if __name__ == '__main__':
    main()