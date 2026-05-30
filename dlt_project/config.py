import os

LAKE_DB_HOST = os.getenv("LAKE_DB_HOST")
LAKE_DB_PORT = os.getenv("LAKE_DB_PORT", "5432")
LAKE_DB_NAME = os.getenv("LAKE_DB_NAME")
LAKE_DB_USER = os.getenv("LAKE_DB_USER")
LAKE_DB_PASSWORD = os.getenv("LAKE_DB_PASSWORD")

WAREHOUSE_DB_HOST = os.getenv("WAREHOUSE_DB_HOST")
WAREHOUSE_DB_PORT = os.getenv("WAREHOUSE_DB_PORT", "5432")
WAREHOUSE_DB_NAME = os.getenv("WAREHOUSE_DB_NAME")
WAREHOUSE_DB_USER = os.getenv("WAREHOUSE_DB_USER")
WAREHOUSE_DB_PASSWORD = os.getenv("WAREHOUSE_DB_PASSWORD")

raw_schema = "raw"

TABLES = [
    "customers",
    "products",
    "stores",
    "employees",
    "orders",
    "order_items",
    "payments",
    "inventory_movements",
    "payment_methods",
]
