from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="weather_daily_pipeline",
    default_args=default_args,
    description="Daily Open-Meteo weather pipeline",
    schedule="@daily",
    start_date=datetime(2026, 9, 1),
    catchup=False,
    max_active_runs=1,
    tags=["weather", "data-engineering"],
) as dag:

    extract_and_load = BashOperator(
        task_id="extract_and_load",
        bash_command=(
            "cd /opt/airflow/ingestion && "
            "python -c "
            "\"from weather import run_pipeline; "
            "run_pipeline('{{ ds }}')\""
        ),
        execution_timeout=timedelta(minutes=5),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt run"
        ),
        execution_timeout=timedelta(minutes=5),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/dbt && "
            "dbt test"
        ),
        execution_timeout=timedelta(minutes=5),
    )

    extract_and_load >> dbt_run >> dbt_test