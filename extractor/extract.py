from datetime import datetime, timezone
from extractor.db import get_connection, setup_schema
from extractor.watermark import get_watermark, save_watermark
from extractor.api_client import fetch_all_pages
from extractor.config import ENTITIES


# payment-methods uses hyphen in URL but we store it as payment_methods
# This maps the entity name to its table name
ENTITY_TABLE_NAMES = {
    "customers":            "customers",
    "products":             "products",
    "stores":               "stores",
    "employees":            "employees",
    "orders":               "orders",
    "order_items":          "order_items",
    "payments":             "payments",
    "inventory_movements":  "inventory_movements",
    "payment_methods":      "payment_methods",
}

# All entities use 'id' as primary key
ENTITY_PRIMARY_KEYS = {
    "customers":            "id",
    "products":             "id",
    "stores":               "id",
    "employees":            "id",
    "orders":               "id",
    "order_items":          "id",
    "payments":             "id",
    "inventory_movements":  "id",
    "payment_methods":      "id",
}

# Maps camelCase API fields to snake_case database columns
FIELD_MAPPINGS = {
    "teamId":           "team_id",
    "firstName":        "first_name",
    "lastName":         "last_name",
    "effectiveFrom":    "effective_from",
    "registeredAt":     "registered_at",
    "isDeleted":        "is_deleted",
    "createdAt":        "created_at",
    "updatedAt":        "updated_at",
    "subCategory":      "sub_category",
    "costPrice":        "cost_price",
    "sellingPrice":     "selling_price",
    "managerName":      "manager_name",
    "openedDate":       "opened_date",
    "hiredDate":        "hired_date",
    "storeId":          "store_id",
    "customerId":       "customer_id",
    "employeeId":       "employee_id",
    "discountCode":     "discount_code",
    "discountAmount":   "discount_amount",
    "totalAmount":      "total_amount",
    "orderedAt":        "ordered_at",
    "paidAt":           "paid_at",
    "shippedAt":        "shipped_at",
    "deliveredAt":      "delivered_at",
    "cancelledAt":      "cancelled_at",
    "orderId":          "order_id",
    "productId":        "product_id",
    "unitPrice":        "unit_price",      
    "discountPct":      "discount_pct",
    "lineTotal":        "line_total",
    "paymentMethodId":  "payment_method_id",
    "amountPaid":       "amount_paid",
    "paymentType":      "payment_type",
    "referenceId":      "reference_id",
    "referenceType":    "reference_type",
    "movedAt":          "moved_at",
    "movementType":     "movement_type",
    "isDigital":        "is_digital",
}

def rename_fields(row: dict) -> dict:
    """Convert camelCase API fields to snake_case for the database."""
    return {
        FIELD_MAPPINGS.get(key, key): value
        for key, value in row.items()
    }


def upsert_rows(table_name: str, rows: list, primary_key: str):
    if not rows:
        print(f"  No rows to upsert for {table_name}.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    table = f"raw.{table_name}"
    upserted_count = 0

    for row in rows:
        # Rename camelCase to snake_case
        row = rename_fields(row)

        # Add extraction timestamp
        row["_extracted_at"] = datetime.now(timezone.utc).isoformat()

        columns = list(row.keys())
        values = list(row.values())

        col_list = ", ".join(columns)
        placeholder_list = ", ".join(["%s"] * len(columns))
        update_set = ", ".join([
            f"{col} = EXCLUDED.{col}"
            for col in columns
            if col != primary_key
        ])

        sql = f"""
            INSERT INTO {table} ({col_list})
            VALUES ({placeholder_list})
            ON CONFLICT ({primary_key})
            DO UPDATE SET {update_set};
        """

        cursor.execute(sql, values)
        upserted_count += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"   Upserted {upserted_count} rows into {table}.")


def get_max_updated_at(rows: list):
    timestamps = [
        row.get("updatedAt") or row.get("updated_at")
        for row in rows
        if row.get("updatedAt") or row.get("updated_at")
    ]
    if not timestamps:
        return None
    return max(timestamps)


def extract_entity(entity_name: str):
    print(f"\n{'='*50}")
    print(f"🚀 Starting extraction: {entity_name}")
    print(f"{'='*50}")

    watermark = get_watermark(entity_name)

    if watermark:
        print(f"   Watermark found: {watermark} — INCREMENTAL extract")
    else:
        print(f"   No watermark — FULL extract (first run)")

    rows = fetch_all_pages(entity_name, updated_after=watermark)

    print(f"  📦 Total rows fetched: {len(rows)}")

    if not rows:
        print(f"   No new data for {entity_name}.")
        return

    table_name = ENTITY_TABLE_NAMES[entity_name]
    primary_key = ENTITY_PRIMARY_KEYS[entity_name]
    upsert_rows(table_name, rows, primary_key)

    max_timestamp = get_max_updated_at(rows)
    if max_timestamp:
        save_watermark(entity_name, max_timestamp)

    print(f"   Done: {entity_name}")


def extract_all_entities():
    setup_schema()
    for entity in ENTITIES:
        extract_entity(entity)
    print(" All entities extracted successfully!")