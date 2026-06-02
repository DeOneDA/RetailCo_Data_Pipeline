# RetailCo_Data_Pipeline.
End-to-end modern data pipeline for RetailCo - a Nigerian Retail Chain with stores in Lagos, Abuja, Port Harcourt, and Kano.                                        
Tools: Apache Airflow, PostgreSQL, dbt, dlt, Docker, and Kimball dimensional modelling.

# Architecture 

## Team Members and Their Responsibilities:
| Slack ID | Full Name | Role, Contribution & Responsibility |
| De One | Oluwadamilare Deboh-Ajiga | 
| God's Favourite_DA | 
| Taliat | Taliat Samuel Oladimeji
| Diane | 

## Project Structure:
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
