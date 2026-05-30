from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
sys.path.insert(0, "/opt/airflow")

from extractor.extract import extract_entity
from extractor.db import setup_schema
from dlt_project.pipeline import run_pipeline

default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="erp_extract_dag",
    description="Daily extraction from ERP API into lake PostgreSQL and dlt load to warehouse",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["extraction", "lake", "erp", "dlt", "warehouse"],
) as dag:

    setup_task = PythonOperator(
        task_id="setup_schema",
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
        python_callable=run_pipeline,
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
