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

## Prerequisites

- Git
- Docker Engine
- Docker Compose
- Access to the ERP REST API
- GitHub account

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
RetailCo_Data_Pipeline/
├── dags/                  # Apache Airflow core DAG workflows
│   └── extract_dags.py    # Main orchestration pipeline definition
├── dlt_project/           # Data Load Tool (dlt) ingestion codes (CP3)
│   ├── sources/           # Source connect scripts for Data Lake extraction
│   ├── config.py          # Destination settings configuration
│   └── pipeline.py        # Core dlt schema/merge pipeline loading mechanics
├── extractor/             # Hand-written API Python Extractor (CP2)
│   ├── api_client.py      # REST Client managing ERP endpoint connections
│   ├── db.py              # Lake connectivity helper scripts
│   └── extract.py         # Main execution pipeline extracting the 9 endpoints
├── dbt_project/           # dbt analytical warehouse transform layer (CP4 & CP5)
│   ├── models/            # Staging, Snapshot, and Dimensional Mart models
│   ├── dbt_project.yml    # Main dbt architecture layout settings
│   └── profiles.yml       # Database connection profiles
├── design/                # Kimball Bus Matrix, Architecture design, and ERDs
├── .env.example           # Example workspace environment variables template
└── docker-compose.yml     # Service manager orchestrating the infrastructure stack

## Setup Instructions:
1. **Clone The Repository:**
   ```bash
   git clone (https://github.com/DeOneDA/RetailCo_Data_Pipeline/)
   cd RetailCo_Data_Pipeline
   ```
2. **Configure Environment Variables:**
   Create an active environment configuration file from the template provided by running:
   ```PowerShell
   cp .env.example .env
   ```
   Open the newly created .env file in your editor and input your actual credentials for ERP_API_KEY and ERP_BASE_URL.

3. **Configure Windows Execution Policy (Important):**
   To allow your local PowerShell terminal to execute the Python virtual environment activation script, run this command:
   ```PowerShell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```
4. **Initialize Your Python Virtual Environment:**
   Run the following commands to create a isolated local environment and install the required processing libraries:
   ```PowerShell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r dlt_project/requirements.txt
   pip install python-dotenv dlt[postgres] dbt-core dbt-postgres
   ```
5. **Spin up Infrastructure Containers:**
   Launch the database backend cluster in detached background mode:
   ```PowerShell
   docker compose up -d
   ```
   Note: Ensure Docker Desktop is allocated at least 4GB of RAM to handle parallel task orchestration and connection pipelines without interruption.

## How To Run The Pipeline
1. Launch your web browser and navigate to the local portal at http://localhost:8080.
2. Authenticate using the default admin cluster credentials (username: admin / password: admin).
3. Locate the extract_dags pipeline inside the DAG console list.
4. Click the toggle switch to change its status to Unpaused, then click the Trigger DAG (play) icon in the actions column to execute the pipeline.

## How To Query The Ware House
The analytical architecture exposes your transformed Star-Schema models on mapped local machine port 5435. You can connect to your data marts using any popular relational database GUI client (such as DBeaver, pgAdmin, or the VSCode PostgreSQL extension) with the connection details below:

Host: localhost

Port: 5435

Database: warehouse_db

Username: postgres

Password: (Defined inside your root .env or docker-compose.yml file)

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
