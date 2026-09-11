import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("WAREHOUSE_HOST", "postgres"),
        port=os.getenv("WAREHOUSE_PORT", "5432"),
        dbname=os.getenv("WAREHOUSE_DB", "warehouse"),
        user=os.getenv("WAREHOUSE_USER", "de"),
        password=os.getenv("WAREHOUSE_PASSWORD", "de"),
    )


CREATE_TABLE_SQL = """
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.weather_daily (
    city TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    weather_date DATE NOT NULL,
    temperature_2m_max DOUBLE PRECISION,
    temperature_2m_min DOUBLE PRECISION,
    temperature_2m_mean DOUBLE PRECISION,
    precipitation_sum DOUBLE PRECISION,
    wind_speed_10m_max DOUBLE PRECISION,
    PRIMARY KEY (city, weather_date)
);
"""


def get_connection():
    return psycopg2.connect(
        host="postgres",
        port=5432,
        dbname="warehouse",
        user="de",
        password="de",
    )


def load_weather(rows):
    if not rows:
        return

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)

                # Delete the logical date before inserting it again.
                # This makes reruns idempotent.
                dates = sorted({row["weather_date"] for row in rows})

                for weather_date in dates:
                    cur.execute(
                        """
                        DELETE FROM raw.weather_daily
                        WHERE weather_date = %s
                        """,
                        (weather_date,),
                    )

                for row in rows:
                    cur.execute(
                        """
                        INSERT INTO raw.weather_daily (
                            city,
                            latitude,
                            longitude,
                            weather_date,
                            temperature_2m_max,
                            temperature_2m_min,
                            temperature_2m_mean,
                            precipitation_sum,
                            wind_speed_10m_max
                        )
                        VALUES (
                            %(city)s,
                            %(latitude)s,
                            %(longitude)s,
                            %(weather_date)s,
                            %(temperature_2m_max)s,
                            %(temperature_2m_min)s,
                            %(temperature_2m_mean)s,
                            %(precipitation_sum)s,
                            %(wind_speed_10m_max)s
                        )
                        """,
                        row,
                    )

    finally:
        conn.close()