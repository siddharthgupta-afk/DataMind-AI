import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# ============================================================
# LOAD RFM DATA
# ============================================================

print("Loading customer RFM data...")

df = pd.read_csv("data/customer_rfm.csv")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# SELECT FEATURES FOR CLUSTERING
# ============================================================

features = [
    "recency_days",
    "total_orders",
    "total_spent"
]

X = df[features].copy()


# ============================================================
# SCALE FEATURES
# ============================================================

print("\nScaling features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# FIND BEST NUMBER OF CLUSTERS
# ============================================================

print("\nTesting different numbers of clusters...")

silhouette_scores = {}

for k in range(2, 9):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    score = silhouette_score(X_scaled, labels)

    silhouette_scores[k] = score

    print(f"K={k} → Silhouette Score: {score:.4f}")


# ============================================================
# SELECT BEST K
# ============================================================

best_k = max(
    silhouette_scores,
    key=silhouette_scores.get
)

print(f"\nBest number of clusters: {best_k}")


# ============================================================
# TRAIN FINAL K-MEANS MODEL
# ============================================================

print("\nTraining final clustering model...")

kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X_scaled)


# ============================================================
# CLUSTER SUMMARY
# ============================================================

print("\nCluster Summary:")

summary = df.groupby("cluster")[features].mean().round(2)

print(summary)


# ============================================================
# SAVE CLUSTERED DATA
# ============================================================

output_file = "data/customer_clusters.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"\nClustered customer data saved to: {output_file}")

print("\nCluster counts:")

print(
    df["cluster"]
    .value_counts()
    .sort_index()
)

print("\nDone! Customer clustering completed successfully.")