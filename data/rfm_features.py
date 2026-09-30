import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path(__file__).parent

INPUT_FILE = DATA_DIR / "customer_features.csv"
OUTPUT_FILE = DATA_DIR / "customer_rfm.csv"


# ============================================================
# LOAD CUSTOMER FEATURES
# ============================================================

print("Loading customer features...")

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df):,} customers")


# ============================================================
# PREPARE DATA
# ============================================================

df["last_order_date"] = pd.to_datetime(df["last_order_date"])

# Use the latest order date in the dataset as the reference date
reference_date = df["last_order_date"].max()

df["recency_days"] = (
    reference_date - df["last_order_date"]
).dt.days


# ============================================================
# RFM SCORES
# ============================================================

print("Calculating RFM scores...")

# Recency:
# Lower recency = better customer activity
df["R_score"] = pd.qcut(
    df["recency_days"],
    q=5,
    labels=[5, 4, 3, 2, 1],
    duplicates="drop"
)

# Frequency:
# More orders = better
df["F_score"] = pd.qcut(
    df["total_orders"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop"
)

# Monetary:
# More spending = better
df["M_score"] = pd.qcut(
    df["total_spent"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop"
)


# Convert scores to integers
df["R_score"] = df["R_score"].astype(int)
df["F_score"] = df["F_score"].astype(int)
df["M_score"] = df["M_score"].astype(int)


# ============================================================
# RFM TOTAL SCORE
# ============================================================

df["RFM_score"] = (
    df["R_score"]
    + df["F_score"]
    + df["M_score"]
)


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

def assign_segment(row):

    r = row["R_score"]
    f = row["F_score"]
    m = row["M_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 4 and f >= 3:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "New Customers"

    elif r <= 2 and f >= 4:
        return "At Risk High Value"

    elif r <= 2 and f >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2:
        return "Lost Customers"

    else:
        return "Potential Loyalists"


df["customer_segment"] = df.apply(
    assign_segment,
    axis=1
)


# ============================================================
# SAVE OUTPUT
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\nRFM feature engineering completed!")
print("-----------------------------------")

print(f"Customers processed: {len(df):,}")
print(f"Output file: {OUTPUT_FILE}")

print("\nCustomer Segments:")
print(
    df["customer_segment"]
    .value_counts()
)


print("\nSample:")
print(
    df[
        [
            "customer_id",
            "recency_days",
            "total_orders",
            "total_spent",
            "R_score",
            "F_score",
            "M_score",
            "RFM_score",
            "customer_segment"
        ]
    ].head()
)