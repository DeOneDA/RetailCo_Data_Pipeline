import os

lake_db_url = os.getenv("lake_db_url")
warehouse_db_url = os.getenv("warehouse_db_url")

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
