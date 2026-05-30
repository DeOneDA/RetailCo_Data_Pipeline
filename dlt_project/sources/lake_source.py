from dotenv import load_dotenv

load_dotenv()

import dlt
import psycopg2
from psycopg2.extras import RealDictCursor

from dlt_project.config import (
    LAKE_DB_HOST,
    LAKE_DB_PORT,
    LAKE_DB_NAME,
    LAKE_DB_USER,
    LAKE_DB_PASSWORD,
    raw_schema,
    TABLES,
)


def get_lake_connection():
    return psycopg2.connect(
        host=LAKE_DB_HOST,
        port=LAKE_DB_PORT,
        dbname=LAKE_DB_NAME,
        user=LAKE_DB_USER,
        password=LAKE_DB_PASSWORD,
    )


def create_table_resource(table_name: str):
    @dlt.resource(
        name=table_name,
        primary_key="id",
        write_disposition="merge",
    )
    def table_resource(
        updated_at=dlt.sources.incremental(
            "updated_at",
            initial_value="1900-01-01T00:00:00",
        )
    ):
        conn = get_lake_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = f"""
            SELECT *
            FROM {raw_schema}.{table_name}
            WHERE updated_at >= %s
            ORDER BY updated_at ASC
        """

        cursor.execute(query, (updated_at.last_value,))

        for row in cursor:
            yield dict(row)

        cursor.close()
        conn.close()

    return table_resource


@dlt.source
def lake_source():
    for table_name in TABLES:
        yield create_table_resource(table_name)
