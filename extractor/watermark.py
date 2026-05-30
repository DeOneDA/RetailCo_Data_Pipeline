from extractor.db import get_connection


def get_watermark(entity_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT last_updated FROM raw.watermarks WHERE entity_name = %s",
        (entity_name,)
    )
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    return None


def save_watermark(entity_name: str, timestamp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO raw.watermarks (entity_name, last_updated)
        VALUES (%s, %s)
        ON CONFLICT (entity_name)
        DO UPDATE SET last_updated = EXCLUDED.last_updated;
    """, (entity_name, timestamp))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Watermark saved for {entity_name}: {timestamp}")