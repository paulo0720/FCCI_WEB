import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not found in .env")

sqlite_db = "database/fcci.db"

print("Connecting to SQLite...")
sqlite_conn = sqlite3.connect(sqlite_db)
sqlite_conn.row_factory = sqlite3.Row
sqlite_cur = sqlite_conn.cursor()

print("Connecting to Supabase PostgreSQL...")
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cur = pg_conn.cursor()

tables = [
    "users",
    "members",
    "payments",
    "attendance",
    "donations",
    "expenses",
    "withdrawals",
]

for table in tables:

    print(f"\nMigrating {table}...")

    try:
        sqlite_cur.execute(f"SELECT * FROM {table}")
        rows = sqlite_cur.fetchall()

        if not rows:
            print(f"  {table}: no records")
            continue

        columns = rows[0].keys()

        col_list = ",".join(columns)

        placeholders = ",".join(["%s"] * len(columns))

        pg_cur.execute(
            f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"
        )

        values = [
            tuple(row[col] for col in columns)
            for row in rows
        ]

        execute_values(
            pg_cur,
            f"""
            INSERT INTO {table}
            ({col_list})
            VALUES %s
            """,
            values
        )

        pg_conn.commit()

        print(
            f"  SUCCESS: {len(values)} records copied"
        )

    except Exception as e:
        pg_conn.rollback()
        print(f"  ERROR: {e}")

sqlite_conn.close()
pg_conn.close()

print("\nDONE!")