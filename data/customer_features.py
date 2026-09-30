import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "datamind")


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# LOAD CUSTOMER FEATURES
# ============================================================

def load_customer_features():

    query = """
        SELECT *
        FROM customer_features
    """

    df = pd.read_sql(query, engine)

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading customer features from PostgreSQL...")

    df = load_customer_features()

    print("\nData loaded successfully!")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    df.to_csv("data/customer_features.csv", index=False)
    
if __name__ == "__main__":
    main()