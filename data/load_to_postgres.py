import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

BASE_DIR = Path(__file__).parent


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "datamind")


# ============================================================
# DATABASE CONNECTION
# ============================================================

if not DB_PASSWORD:
    raise ValueError(
        "DB_PASSWORD is not set. "
        "Create a .env file with your PostgreSQL password."
    )


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(DATABASE_URL)


# ============================================================
# LOAD CSV FILES
# ============================================================

def load_data():

    print("Loading CSV files...")

    customers = pd.read_csv(
        BASE_DIR / "customers.csv"
    )

    products = pd.read_csv(
        BASE_DIR / "products.csv"
    )

    orders = pd.read_csv(
        BASE_DIR / "orders.csv"
    )

    order_items = pd.read_csv(
        BASE_DIR / "order_items.csv"
    )

    print("CSV files loaded successfully.")

    return (
        customers,
        products,
        orders,
        order_items
    )


# ============================================================
# INSERT INTO POSTGRESQL
# ============================================================

def insert_data(
    customers,
    products,
    orders,
    order_items
):

    print("\nUploading customers...")
    customers.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )

    print("Uploading products...")
    products.to_sql(
        "products",
        engine,
        if_exists="append",
        index=False
    )

    print("Uploading orders...")
    orders.to_sql(
        "orders",
        engine,
        if_exists="append",
        index=False
    )

    print("Uploading order items...")
    order_items.to_sql(
        "order_items",
        engine,
        if_exists="append",
        index=False
    )

    print("\nAll data uploaded successfully!")


# ============================================================
# VERIFY DATA
# ============================================================

def verify_data():

    print("\nChecking database...")

    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    with engine.connect() as connection:

        for table in tables:

            result = connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            )

            count = result.scalar()

            print(
                f"{table:<15} {count:,} rows"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    customers, products, orders, order_items = load_data()

    insert_data(
        customers,
        products,
        orders,
        order_items
    )

    verify_data()


if __name__ == "__main__":
    main()