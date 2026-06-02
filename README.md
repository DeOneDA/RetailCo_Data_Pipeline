# RetailCo_Data_Pipeline.

End-to-end modern data pipeline for RetailCo, a Nigerian Retail Chain with stores in Lagos, Abuja, Port Harcourt, and Kano.                                        
Tools: Apache Airflow, PostgreSQL, dbt, dlt, Docker, and Kimball dimensional modelling.

## Architecture

```text
ERP API (9 Entity Endpoints)
            │
            │ HTTPS
            ▼
Python Extractor
            │
            ▼
PostgreSQL Data Lake (lake_db)
         (raw schema)
            │
            │ dlt Pipeline
            ▼
PostgreSQL Warehouse (warehouse_db)
          (raw schema)
            │
            ▼
dbt staging
(cleaning & type casting)
            │
            ▼
dbt snapshots
(SCD Type 2 tracking)
            │
            ▼
dbt marts
(6 Dimensions + 4 Facts +
 Flagged Payments)
            │
            ▼
dbt tests
(data quality validation)

────────────────────────────

Apache Airflow DAG (@daily)

Extract
  ↓
Load (dlt)
  ↓
dbt snapshot
  ↓
dbt staging
  ↓
dbt marts
  ↓
dbt test

────────────────────────────

Docker Compose Environment

├── Airflow Container
├── Python Extractor Container
├── PostgreSQL Lake Container
├── PostgreSQL Warehouse Container
├── dlt Service
└── dbt Service
```

# Prerequisites
(to be filled) 

## Required Tools

| Layer | Tool | Version Requirement |
|---------|---------|---------|
| Orchestration | Apache Airflow | 2.9+ |
| Extraction | Python (Hand-written Extractor) | 3.11+ |
| Lake Storage | PostgreSQL | 15+ |
| Loading | dlt | Latest |
| Warehouse Storage | PostgreSQL | 15+ |
| Transformation | dbt-core + dbt-postgres | 1.7+ |
| Containerization | Docker + Docker Compose | Latest Stable |

## Team Members and Responsibilities

| Slack ID | Full Name | Role & Responsibilities |
|-----------|-----------|-----------|
| De One | Oluwadamilare Deboh-Ajiga | Team Lead; designed the Architecture Diagram, Warehouse ERD, and Kimball Bus Matrix. |
| God's Favourite_DA | Ogbonna Favour Amarachi | Developed the data extraction process and completed Checkpoint 2; contributed to the Business Insights Document. |
| Taliat | Taliat Samuel Oladimeji | Completed Checkpoint 3 and assisted with Checkpoints 4 and 5. |
| Diane | Halimat Abu | Completed Checkpoint 4 and refined the project README documentation. |

## Project Structure:
(Also needs to be worked on as well)
RetailCo_Data_Pipeline/
|- airflow/dags/
|- dbt_project/
|- design/
|- dlt_project/
|- extractor/

## Setup Instructions:
(To be filled)

## How To Run The Pipeline
(To be filled)

## How To Query The Ware House
(To be filled)

## Checkpoint 3: dlt Loader

The dlt loader moves raw data from the lake PostgreSQL database into the warehouse PostgreSQL database.

Source:
- Database: `lake`
- Schema: `raw`
- Tables: customers, products, stores, employees, orders, order_items, payments, inventory_movements, payment_methods

Destination:
- Database: `warehouse_db`
- Schema: `raw`

The loader uses `updated_at` for incremental loading and `id` as the primary key for merge loading. This prevents duplicate records when the pipeline is run more than once.

CP3 files:
- `dlt_project/config.py`
- `dlt_project/pipeline.py`
- `dlt_project/sources/lake_source.py`
- `dlt_project/requirements.txt`

The dlt load is called from the Airflow DAG after all extraction tasks complete.
