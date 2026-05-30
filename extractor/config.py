import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ERP_API_KEY")
BASE_URL = os.getenv("ERP_BASE_URL")

LAKE_DB_URL = (
    f"postgresql://{os.getenv('LAKE_DB_USER')}:{os.getenv('LAKE_DB_PASSWORD')}"
    f"@{os.getenv('LAKE_DB_HOST')}:{os.getenv('LAKE_DB_PORT')}/{os.getenv('LAKE_DB_NAME')}"
)

PAGE_LIMIT = 100
MAX_RETRIES = 5
BASE_BACKOFF = 1

ENTITIES = [
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