from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import sys
sys.path.insert(0, "/opt/airflow")

from extractor.extract import extract_entity
from extractor.db import setup_schema

def run_dlt_pipeline():
    from dlt_project.pipeline import run_pipeline
    run_pipeline()


default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
}


with DAG(
    dag_id="retailco_end_to_end_pipeline",
    description="End-to-end RetailCo pipeline: Extract, Load, dbt snapshot, staging, marts and tests",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=True,
    tags=["retailco", "extract", "dlt", "dbt", "warehouse"],
) as dag:

    setup_task = PythonOperator(
        task_id="setup_lake_schema",
        python_callable=setup_schema,
    )

    extract_payment_methods = PythonOperator(
        task_id="extract_payment_methods",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "payment_methods"},
    )

    extract_stores = PythonOperator(
        task_id="extract_stores",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "stores"},
    )

    extract_products = PythonOperator(
        task_id="extract_products",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "products"},
    )

    extract_customers = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "customers"},
    )

    extract_employees = PythonOperator(
        task_id="extract_employees",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "employees"},
    )

    extract_orders = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "orders"},
    )

    extract_order_items = PythonOperator(
        task_id="extract_order_items",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "order_items"},
    )

    extract_payments = PythonOperator(
        task_id="extract_payments",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "payments"},
    )

    extract_inventory = PythonOperator(
        task_id="extract_inventory_movements",
        python_callable=extract_entity,
        op_kwargs={"entity_name": "inventory_movements"},
    )

    load_dlt_to_warehouse = PythonOperator(
        task_id="load_dlt_to_warehouse",
        python_callable=run_dlt_pipeline,
    )
    
    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command="cd /opt/airflow/dbt_project && dbt snapshot --profiles-dir /opt/airflow/dbt_project",
    )

    dbt_run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command="cd /opt/airflow/dbt_project && dbt run --select staging --profiles-dir /opt/airflow/dbt_project",
    )

    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command="cd /opt/airflow/dbt_project && dbt run --select marts --profiles-dir /opt/airflow/dbt_project",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt_project && dbt test --profiles-dir /opt/airflow/dbt_project",
    )

    setup_task >> [
        extract_payment_methods,
        extract_stores,
        extract_products,
    ]

    extract_stores >> [extract_customers, extract_employees]
    [extract_customers, extract_employees] >> extract_orders
    extract_orders >> [extract_order_items, extract_payments]
    [extract_products, extract_stores] >> extract_inventory

    [
        extract_payment_methods,
        extract_order_items,
        extract_payments,
        extract_inventory,
    ] >> load_dlt_to_warehouse

    load_dlt_to_warehouse >> dbt_snapshot >> dbt_run_staging >> dbt_run_marts >> dbt_test
