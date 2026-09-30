import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path(__file__).resolve().parent

RFM_FILE = DATA_DIR / "customer_rfm.csv"
CLUSTERS_FILE = DATA_DIR / "customer_clusters.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"
ORDER_ITEMS_FILE = DATA_DIR / "order_items.csv"
PRODUCTS_FILE = DATA_DIR / "products.csv"

OUTPUT_FILE = DATA_DIR / "product_recommendations.csv"


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("Loading recommendation data...")

    rfm = pd.read_csv(RFM_FILE)
    clusters = pd.read_csv(CLUSTERS_FILE)
    orders = pd.read_csv(ORDERS_FILE)
    order_items = pd.read_csv(ORDER_ITEMS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)

    print(f"RFM rows: {len(rfm)}")
    print(f"Cluster rows: {len(clusters)}")
    print(f"Orders rows: {len(orders)}")
    print(f"Order items rows: {len(order_items)}")
    print(f"Products rows: {len(products)}")

    return rfm, clusters, orders, order_items, products


# ============================================================
# BUILD CUSTOMER PURCHASE HISTORY
# ============================================================

def build_customer_history(orders, order_items, products):

    print("\nBuilding customer purchase history...")

    # Only completed orders
    completed_orders = orders[
        orders["status"] == "Completed"
    ][["order_id", "customer_id"]]

    # Connect orders with products
    history = order_items.merge(
        completed_orders,
        on="order_id",
        how="inner"
    )

    history = history.merge(
        products[
            [
                "product_id",
                "product_name",
                "category",
                "price"
            ]
        ],
        on="product_id",
        how="left"
    )

    return history


# ============================================================
# PRODUCT POPULARITY
# ============================================================

def build_product_popularity(history):

    print("Calculating product popularity...")

    popularity = (
        history
        .groupby("product_id")
        .agg(
            total_quantity=("quantity", "sum"),
            unique_customers=("customer_id", "nunique"),
            purchase_count=("order_id", "nunique")
        )
        .reset_index()
    )

    # Normalize popularity components
    popularity["quantity_score"] = (
        popularity["total_quantity"]
        / popularity["total_quantity"].max()
    )

    popularity["customer_score"] = (
        popularity["unique_customers"]
        / popularity["unique_customers"].max()
    )

    popularity["purchase_score"] = (
        popularity["purchase_count"]
        / popularity["purchase_count"].max()
    )

    popularity["popularity_score"] = (
        popularity["quantity_score"] * 0.4
        + popularity["customer_score"] * 0.4
        + popularity["purchase_score"] * 0.2
    )

    return popularity


# ============================================================
# CUSTOMER CATEGORY PREFERENCES
# ============================================================

def build_category_preferences(history):

    print("Learning customer category preferences...")

    category_preferences = (
        history
        .groupby(
            ["customer_id", "category"]
        )
        .agg(
            category_quantity=("quantity", "sum"),
            category_orders=("order_id", "nunique")
        )
        .reset_index()
    )

    # Calculate preference score
    category_preferences["preference_score"] = (
        category_preferences["category_quantity"] * 0.6
        + category_preferences["category_orders"] * 0.4
    )

    # Normalize per customer
    category_preferences["preference_score"] = (
        category_preferences
        .groupby("customer_id")["preference_score"]
        .transform(
            lambda x: x / x.max()
        )
    )

    return category_preferences


# ============================================================
# CLUSTER PRODUCT PREFERENCES
# ============================================================

def build_cluster_preferences(history, clusters):

    print("Learning cluster-level product preferences...")

    history_with_cluster = history.merge(
        clusters[
            ["customer_id", "cluster"]
        ],
        on="customer_id",
        how="left"
    )

    cluster_products = (
        history_with_cluster
        .groupby(
            ["cluster", "product_id"]
        )
        .agg(
            cluster_quantity=("quantity", "sum"),
            cluster_customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    # Normalize within each cluster
    cluster_products["cluster_score"] = (
        cluster_products
        .groupby("cluster")["cluster_quantity"]
        .transform(
            lambda x: x / x.max()
        )
    )

    return cluster_products


# ============================================================
# GENERATE PERSONALIZED RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    rfm,
    clusters,
    history,
    products,
    popularity,
    category_preferences,
    cluster_preferences,
    top_n=5
):

    print("\nGenerating personalized recommendations...")

    customer_data = rfm.merge(
        clusters[
            ["customer_id", "cluster"]
        ],
        on="customer_id",
        how="left"
    )

    recommendations = []

    # --------------------------------------------------------
    # Process each customer
    # --------------------------------------------------------

    for _, customer in customer_data.iterrows():

        customer_id = customer["customer_id"]
        cluster = customer["cluster"]

        # Products already purchased
        purchased_products = set(
            history[
                history["customer_id"] == customer_id
            ]["product_id"]
        )

        # Customer's preferred categories
        customer_categories = category_preferences[
            category_preferences["customer_id"]
            == customer_id
        ]

        category_scores = dict(
            zip(
                customer_categories["category"],
                customer_categories["preference_score"]
            )
        )

        # Cluster product scores
        cluster_scores = cluster_preferences[
            cluster_preferences["cluster"]
            == cluster
        ]

        cluster_product_scores = dict(
            zip(
                cluster_scores["product_id"],
                cluster_scores["cluster_score"]
            )
        )

        # ----------------------------------------------------
        # Candidate products
        # ----------------------------------------------------

        candidates = products[
            ~products["product_id"].isin(
                purchased_products
            )
        ].copy()

        # Global popularity
        candidates = candidates.merge(
            popularity[
                [
                    "product_id",
                    "popularity_score"
                ]
            ],
            on="product_id",
            how="left"
        )

        candidates["popularity_score"] = (
            candidates["popularity_score"]
            .fillna(0)
        )

        # ----------------------------------------------------
        # Customer category preference
        # ----------------------------------------------------

        candidates["category_score"] = (
            candidates["category"]
            .map(category_scores)
            .fillna(0)
        )

        # ----------------------------------------------------
        # Cluster preference
        # ----------------------------------------------------

        candidates["cluster_score"] = (
            candidates["product_id"]
            .map(cluster_product_scores)
            .fillna(0)
        )

        # ----------------------------------------------------
        # Final recommendation score
        # ----------------------------------------------------

        candidates["recommendation_score"] = (
            candidates["category_score"] * 0.40
            + candidates["cluster_score"] * 0.35
            + candidates["popularity_score"] * 0.25
        )

        # Sort by score
        candidates = candidates.sort_values(
            "recommendation_score",
            ascending=False
        )

        # Top N
        top_products = candidates.head(top_n)

        # ----------------------------------------------------
        # Store recommendations
        # ----------------------------------------------------

        for rank, (_, product) in enumerate(
            top_products.iterrows(),
            start=1
        ):

            recommendations.append({

                "customer_id": customer_id,

                "cluster": cluster,

                "product_id": product["product_id"],

                "product_name": product["product_name"],

                "category": product["category"],

                "price": product["price"],

                "recommendation_score": round(
                    product["recommendation_score"],
                    4
                ),

                "rank": rank
            })

    return pd.DataFrame(recommendations)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 65)
    print("DATAMIND AI - PERSONALIZED PRODUCT RECOMMENDATION ENGINE")
    print("=" * 65)

    # Load data
    (
        rfm,
        clusters,
        orders,
        order_items,
        products
    ) = load_data()

    # Customer purchase history
    history = build_customer_history(
        orders,
        order_items,
        products
    )

    # Product popularity
    popularity = build_product_popularity(
        history
    )

    # Customer category preferences
    category_preferences = build_category_preferences(
        history
    )

    # Cluster-level preferences
    cluster_preferences = build_cluster_preferences(
        history,
        clusters
    )

    # Generate recommendations
    recommendations = generate_recommendations(
        rfm=rfm,
        clusters=clusters,
        history=history,
        products=products,
        popularity=popularity,
        category_preferences=category_preferences,
        cluster_preferences=cluster_preferences,
        top_n=5
    )

    # Save
    recommendations.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 65)
    print("RECOMMENDATION ENGINE COMPLETED")
    print("=" * 65)

    print(
        f"\nTotal recommendations: "
        f"{len(recommendations)}"
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )

    print("\nSample recommendations:")

    print(
        recommendations.head(15).to_string(
            index=False
        )
    )

    print("\nDone! Personalized recommendations generated successfully.")


if __name__ == "__main__":
    main()