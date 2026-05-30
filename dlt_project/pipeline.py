from dotenv import load_dotenv

load_dotenv()

import dlt

from dlt_project.config import (
    WAREHOUSE_DB_HOST,
    WAREHOUSE_DB_PORT,
    WAREHOUSE_DB_NAME,
    WAREHOUSE_DB_USER,
    WAREHOUSE_DB_PASSWORD,
    raw_schema,
)

from dlt_project.sources.lake_source import lake_source


def get_warehouse_credentials():
    return {
        "drivername": "postgresql",
        "host": WAREHOUSE_DB_HOST,
        "port": int(WAREHOUSE_DB_PORT),
        "database": WAREHOUSE_DB_NAME,
        "username": WAREHOUSE_DB_USER,
        "password": WAREHOUSE_DB_PASSWORD,
    }


def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="retailco_lake_to_warehouse",
        destination=dlt.destinations.postgres(
            credentials=get_warehouse_credentials()
        ),
        dataset_name=raw_schema,
    )

    load_info = pipeline.run(lake_source())
    print(load_info)


if __name__ == "__main__":
    run_pipeline()
