import psycopg2
from extractor.config import LAKE_DB_URL


def get_connection():
    return psycopg2.connect(LAKE_DB_URL)


def setup_schema():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'raw') THEN
            CREATE SCHEMA raw;
        END IF;
    END
    $$;
""")

    # WATERMARKS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.watermarks (
            entity_name   VARCHAR(100) PRIMARY KEY,
            last_updated  TIMESTAMP WITH TIME ZONE
        );
    """)

    # CUSTOMERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.customers (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            first_name      TEXT,
            last_name       TEXT,
            email           TEXT,
            phone           TEXT,
            segment         TEXT,
            tier            TEXT,
            address         TEXT,
            city            TEXT,
            state           TEXT,
            effective_from  TIMESTAMP,
            registered_at   TIMESTAMP,
            is_deleted      BOOLEAN DEFAULT FALSE,
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    # PRODUCTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.products (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            sku             TEXT,
            name            TEXT,
            category        TEXT,
            sub_category    TEXT,
            brand           TEXT,
            supplier        TEXT,
            cost_price      NUMERIC(12, 2),
            selling_price   NUMERIC(12, 2),
            effective_from  TIMESTAMP,
            is_deleted      BOOLEAN DEFAULT FALSE,
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    # STORES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.stores (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            name            TEXT,
            city            TEXT,
            state           TEXT,
            address         TEXT,
            phone           TEXT,
            manager_name    TEXT,
            opened_date     DATE,
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    # EMPLOYEES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.employees (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            store_id        VARCHAR(100),
            first_name      TEXT,
            last_name       TEXT,
            email           TEXT,
            role            TEXT,
            hired_date      DATE,
            is_deleted      BOOLEAN DEFAULT FALSE,
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    # ORDERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.orders (
            id               VARCHAR(100) PRIMARY KEY,
            team_id          VARCHAR(100),
            customer_id      VARCHAR(100),
            store_id         VARCHAR(100),
            employee_id      VARCHAR(100),
            status           TEXT,
            discount_code    TEXT,
            discount_amount  NUMERIC(12, 2),
            total_amount     NUMERIC(12, 2),
            ordered_at       TIMESTAMP,
            paid_at          TIMESTAMP,
            shipped_at       TIMESTAMP,
            delivered_at     TIMESTAMP,
            cancelled_at     TIMESTAMP,
            created_at       TIMESTAMP,
            updated_at       TIMESTAMP,
            _extracted_at    TIMESTAMP DEFAULT NOW()
        );
    """)

    # ORDER ITEMS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.order_items (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            order_id        VARCHAR(100),
            product_id      VARCHAR(100),
            quantity        INTEGER,
            unit_price      NUMERIC(12, 2),
            discount_pct    NUMERIC(5, 2),
            line_total      NUMERIC(12, 2),
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    # PAYMENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.payments (
            id                  VARCHAR(100) PRIMARY KEY,
            team_id             VARCHAR(100),
            order_id            VARCHAR(100),
            customer_id         VARCHAR(100),
            payment_method_id   VARCHAR(100),
            amount_paid         NUMERIC(12, 2),
            currency            TEXT,
            status              TEXT,
            payment_type        TEXT,
            reference           TEXT,
            paid_at             TIMESTAMP,
            created_at          TIMESTAMP,
            updated_at          TIMESTAMP,
            _extracted_at       TIMESTAMP DEFAULT NOW()
        );
    """)

    # INVENTORY MOVEMENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.inventory_movements (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            product_id      VARCHAR(100),
            store_id        VARCHAR(100),
            movement_type   TEXT,
            quantity        INTEGER,
            reference_id    VARCHAR(100),
            reference_type  TEXT,
            notes           TEXT,
            moved_at        TIMESTAMP,
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    # PAYMENT METHODS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.payment_methods (
            id              VARCHAR(100) PRIMARY KEY,
            team_id         VARCHAR(100),
            name            TEXT,
            provider        TEXT,
            is_digital      BOOLEAN DEFAULT FALSE,
            created_at      TIMESTAMP,
            updated_at      TIMESTAMP,
            _extracted_at   TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print(" Schema and tables created successfully.")