"""
Loads processed Star-Schema CSVs into the relational SQLite database.
Built using standard library sqlite3 and csv for 100% universal zero-dependency execution.
"""

import os
import csv
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "database", "energy_intelligence.db")
DDL_PATH = os.path.join(BASE_DIR, "database", "schema_ddl.sql")


def load_csv_to_table(cursor, csv_path: str, table_name: str):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        placeholders = ", ".join(["?"] * len(headers))
        col_names = ", ".join(headers)
        sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
        cursor.executemany(sql, reader)
    logging.info(f"Loaded {table_name} from {os.path.basename(csv_path)}")


def init_and_load_database():
    logging.info(f"Initializing SQLite Database at: {DB_PATH}")
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read and execute DDL
    with open(DDL_PATH, "r", encoding="utf-8") as f:
        ddl_script = f.read()
    
    cursor.executescript(ddl_script)
    conn.commit()
    logging.info("Star-Schema DDL successfully executed.")

    # Load tables from CSV
    load_csv_to_table(cursor, os.path.join(PROCESSED_DATA_DIR, "dim_country.csv"), "dim_country")
    load_csv_to_table(cursor, os.path.join(PROCESSED_DATA_DIR, "dim_technology.csv"), "dim_technology")
    load_csv_to_table(cursor, os.path.join(PROCESSED_DATA_DIR, "dim_time.csv"), "dim_time")
    load_csv_to_table(cursor, os.path.join(PROCESSED_DATA_DIR, "fact_power_generation.csv"), "fact_power_generation")

    conn.commit()

    # Verification counts
    cursor.execute("SELECT COUNT(*) FROM dim_country")
    count_country = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM dim_technology")
    count_tech = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fact_power_generation")
    count_fact = cursor.fetchone()[0]

    logging.info("=== Database Ingestion Verification ===")
    logging.info(f"Dim_Country records: {count_country}")
    logging.info(f"Dim_Technology records: {count_tech}")
    logging.info(f"Fact_PowerGeneration records: {count_fact}")

    conn.close()
    logging.info("Database loaded successfully and ready for analytical queries!")


if __name__ == "__main__":
    init_and_load_database()
