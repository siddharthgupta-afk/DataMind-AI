from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RECOMMENDATIONS_FILE = (
    BASE_DIR / "data" / "product_recommendations.csv"
)

RFM_FILE = (
    BASE_DIR / "data" / "customer_rfm.csv"
)

FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
INDEX_FILE = FRONTEND_DIR / "templates" / "index.html"


# ============================================================
# LOAD RECOMMENDATIONS
# ============================================================

try:

    recommendations_df = pd.read_csv(
        RECOMMENDATIONS_FILE
    )

    print(
        f"Loaded {len(recommendations_df)} "
        "recommendations successfully."
    )

except Exception as e:

    print(
        f"Error loading recommendations: {e}"
    )

    recommendations_df = pd.DataFrame()
    
# ============================================================
# LOAD CUSTOMER RFM DATA
# ============================================================

try:

    rfm_df = pd.read_csv(
        RFM_FILE
    )

    print(
        f"Loaded {len(rfm_df)} customer RFM records successfully."
    )

except Exception as e:

    print(
        f"Error loading RFM data: {e}"
    )

    rfm_df = pd.DataFrame()


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="DataMind-AI API",
    description=(
        "AI-powered customer segmentation "
        "and personalized product recommendation API."
    ),
    version="1.0.0"
)

# ============================================================
# FRONTEND STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
def root():

    return FileResponse(INDEX_FILE)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "recommendations_loaded": (
            not recommendations_df.empty
        )
    }

# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

@app.get("/customer/{customer_id}/insights")
def get_customer_insights(customer_id: int):

    if rfm_df.empty:

        raise HTTPException(
            status_code=500,
            detail="Customer RFM data is not loaded."
        )

    customer_data = rfm_df[
        rfm_df["customer_id"] == customer_id
    ]

    if customer_data.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No customer insights found "
                f"for customer {customer_id}."
            )
        )

    row = customer_data.iloc[0]

    # Get cluster from recommendation data
    cluster = None

    cluster_data = recommendations_df[
        recommendations_df["customer_id"] == customer_id
    ]

    if not cluster_data.empty:

        cluster = int(
            cluster_data.iloc[0]["cluster"]
        )

    return {

        "customer_id": int(
            row["customer_id"]
        ),

        "cluster": cluster,

        "total_orders": int(
            row["total_orders"]
        ),

        "total_spent": float(
            row["total_spent"]
        ),

        "average_order_value": float(
            row["average_order_value"]
        ),

        "last_order_date": str(
            row["last_order_date"]
        ),

        "recency_days": int(
            row["recency_days"]
        ),

        "r_score": int(
            row["R_score"]
        ),

        "f_score": int(
            row["F_score"]
        ),

        "m_score": int(
            row["M_score"]
        ),

        "rfm_score": int(
            row["RFM_score"]
        ),

        "customer_segment": str(
            row["customer_segment"]
        )
    }

# ============================================================
# GET CUSTOMER RECOMMENDATIONS
# ============================================================

@app.get("/recommendations/{customer_id}")
def get_recommendations(customer_id: int):

    if recommendations_df.empty:

        raise HTTPException(
            status_code=500,
            detail="Recommendation data is not loaded."
        )

    customer_data = recommendations_df[
        recommendations_df["customer_id"]
        == customer_id
    ].sort_values("rank")

    if customer_data.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No recommendations found "
                f"for customer {customer_id}."
            )
        )

    recommendations = []

    for _, row in customer_data.iterrows():

        recommendations.append({

            "product_id": int(
                row["product_id"]
            ),

            "product_name": str(
                row["product_name"]
            ),

            "category": str(
                row["category"]
            ),

            "price": float(
                row["price"]
            ),

            "recommendation_score": float(
                row["recommendation_score"]
            ),

            "rank": int(
                row["rank"]
            )
        })

    return {

        "customer_id": customer_id,

        "cluster": int(
            customer_data.iloc[0]["cluster"]
        ),

        "recommendations": recommendations
    }


# ============================================================
# GET ALL CUSTOMERS
# ============================================================

@app.get("/customers")
def get_customers():

    if recommendations_df.empty:

        raise HTTPException(
            status_code=500,
            detail="Recommendation data is not loaded."
        )

    customers = sorted(
        recommendations_df[
            "customer_id"
        ]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    return {

        "total_customers": len(customers),

        "customer_ids": customers
    }