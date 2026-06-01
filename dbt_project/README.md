# Retailco dbt Project

## Overview
This dbt project transforms raw ERP data into a Kimball-style dimensional warehouse for RetailCo — a Nigerian retail chain with stores in Lagos, Abuja, Port Harcourt, and Kano.

## Project Structure
```
models/
├── staging/        # Raw → cleaned views (one per ERP entity)
└── marts/
    ├── dimensions/ # dim_date, dim_customer (SCD2), dim_product (SCD2),
    │               # dim_store, dim_employee, dim_payment_method
    └── facts/      # fct_sales, fct_payments, fct_inventory_daily,
                    # fct_order_lifecycle, flagged_payments

snapshots/          # SCD2 history capture for customer and product
tests/              # Custom data quality tests
```

## Setup
1. Install dbt: `pip install dbt-core dbt-postgres`
2. Configure `~/.dbt/profiles.yml` with your warehouse connection
3. Run `dbt debug` to verify connection

## Running the Pipeline
```bash
# Step 1 — capture SCD2 history
dbt snapshot

# Step 2 — build staging models
dbt run --select staging

# Step 3 — build mart models
dbt run --select marts

# Step 4 — run all tests
dbt test
```

## Models
| Model | Type | Grain |
|---|---|---|
| fct_sales | Transactional fact | One row per order line |
| fct_payments | Transactional fact | One row per payment |
| fct_inventory_daily | Periodic snapshot | Product × store × day |
| fct_order_lifecycle | Accumulating snapshot | One row per order |
| flagged_payments | Data quality | Anomalous payments |
