import pickle
import numpy as np
import pandas as pd
import datetime
import os
import mlflow
import scipy.sparse as sp


# ── Load model bundle ────────────────────────────────────────────────────────

# Set DagsHub credentials
os.environ["MLFLOW_TRACKING_USERNAME"] = os.environ.get("DAGSHUB_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.environ.get("DAGSHUB_TOKEN")

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

# Load model bundle from MLflow registry
bundle = mlflow.sklearn.load_model("models:/recommendation-model/1")

svd              = bundle["svd"]
customer_factors = bundle["customer_factors"]
item_factors     = bundle["item_factors"]
customer_index   = bundle["customer_index"]
product_index    = bundle["product_index"]
products_raw     = bundle["products_raw"]
sparse_matrix    = bundle["customer_product_matrix"]  # scipy sparse matrix

MODEL_VERSION = "rec-model-svd-v1.0"


# ── Recommendation function ──────────────────────────────────────────────────
def get_recommendations(customer_id: str, n: int = 5) -> dict:
    """
    Returns top-n recommendations for a given customer_id.
    Raises KeyError for unknown customers.
    """

    # 404 — customer not in matrix
    if customer_id not in customer_index:
        raise KeyError(f"Customer '{customer_id}' not found.")

    # Get customer latent vector
    customer_idx    = customer_index.index(customer_id)
    customer_vector = customer_factors[customer_idx]

    # Score all items
    scores = np.dot(item_factors, customer_vector)

    # Zero out already-interacted products
    customer_row   = sparse_matrix.getrow(customer_idx)
    interacted_idx = customer_row.nonzero()[1].tolist()
    scores[interacted_idx] = 0

    # Top n indices
    top_indices  = np.argsort(scores)[::-1][:n]
    top_products = [product_index[i] for i in top_indices]
    top_scores   = scores[top_indices]

    # Normalise to 0-1
    if top_scores.max() > 0:
        top_scores = top_scores / top_scores.max()

    # Build DataFrame and enrich
    top_n = pd.DataFrame({
        "product_id":      top_products,
        "predicted_score": top_scores
    })
    top_n = top_n.merge(products_raw, on="product_id", how="left")
    top_n = top_n.sort_values("predicted_score", ascending=False)

    # Build recommendations list
    recommendations = []
    for _, row in top_n.iterrows():
        recommendations.append({
            "product_id":      row["product_id"],
            "product_name":    row["product_name"],
            "category":        row["category"],
            "predicted_score": round(float(row["predicted_score"]), 4)
        })

    return {
        "customer_id":     customer_id,
        "recommendations": recommendations,
        "model_version":   MODEL_VERSION,
        "timestamp":       datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }