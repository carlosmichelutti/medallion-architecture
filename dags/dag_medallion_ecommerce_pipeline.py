import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from airflow.decorators import dag, task
from airflow.sdk import TaskInstance
from airflow.sdk.types import DagRunProtocol

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, PROJECT_ROOT.as_posix())

@dag(
    dag_id='dag_medallion_ecommerce_pipeline',
    start_date=datetime(2026, 8, 19, tzinfo=timezone.utc),
    schedule='@daily',
    catchup=False,
    tags=['medallion', 'ecommerce', 'pipeline'],
    default_args={
        'owner': 'airflow',
        'retries': 2,
        'retry_delay': timedelta(minutes=1)
    }
)
def dag_medallion_ecommerce_pipeline():

    @task(task_id='generate_batch_id', do_xcom_push=True)
    def generate_batch_id(dag_run: DagRunProtocol) -> str:
        return dag_run.logical_date.strftime('%Y%m%d%H%M%S')

    @task(task_id='bronze')
    def bronze(task_instance: TaskInstance) -> None:
        from src.bronze.pipeline import run_bronze

        batch_id = task_instance.xcom_pull(
            task_ids='generate_batch_id',
            key='return_value'
        )

        bronze_files = run_bronze(batch_id=batch_id)

        print(f'Bronze layer completed. {len(bronze_files)} files generated.')

    @task(task_id='silver')
    def silver() -> None:
        from src.silver.pipeline import run_silver

        silver_files = run_silver()

        print(f'Silver layer completed. {len(silver_files)} files generated.')

    @task(task_id='gold')
    def gold() -> None:
        from src.gold.pipeline import run_gold

        gold_files = run_gold()

        print(f'Gold layer completed. {len(gold_files)} files generated.')

    @task(task_id='metrics')
    def metrics() -> None:
        from src.metrics.pipeline import run_metrics

        run_metrics()

        print('Metrics layer completed.')

    generate_batch_id() >> bronze() >> silver() >> gold() >> metrics()

dag_medallion_ecommerce_pipeline()