import pickle
import numpy as np
import pandas as pd
import datetime
import scipy.sparse as sp
import mlflow
import mlflow.tracking
import os

from dotenv import load_dotenv
load_dotenv()

# ── Global variables ──────────────────────────────────────────────────────────
bundle           = None
svd              = None
customer_factors = None
item_factors     = None
customer_index   = None
product_index    = None
products_raw     = None
sparse_matrix    = None

MODEL_VERSION = "rec-model-svd-v1.0"


# ── Load model bundle from Dagshub ────────────────────────────────────────────
def load_bundle():
    global bundle, svd, customer_factors, item_factors
    global customer_index, product_index, products_raw, sparse_matrix

    # ── Credentials from environment variables — never hardcoded ─────────────
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    username     = os.getenv('MLFLOW_TRACKING_USERNAME')
    password     = os.getenv('MLFLOW_TRACKING_PASSWORD')

    if not all([tracking_uri, username, password]):
        raise EnvironmentError(
            "Missing MLflow credentials. Set MLFLOW_TRACKING_URI, "
            "MLFLOW_TRACKING_USERNAME and MLFLOW_TRACKING_PASSWORD "
            "as environment variables."
        )

    os.environ['MLFLOW_TRACKING_URI']      = tracking_uri
    os.environ['MLFLOW_TRACKING_USERNAME'] = username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = password

    mlflow.set_tracking_uri(tracking_uri)

    # ── Download latest svd-tuned-final bundle from Dagshub ───────────────────
    print("Connecting to Dagshub...")
    client = mlflow.tracking.MlflowClient()

    experiment = client.get_experiment_by_name("recommendation-engine")
    if experiment is None:
        raise ValueError("Experiment 'recommendation-engine' not found on Dagshub.")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="tags.mlflow.runName = 'svd-tuned-final'",
        order_by=["start_time DESC"],
        max_results=1
    )

    if not runs:
        raise ValueError("No svd-tuned-final run found in experiment.")

    run_id = runs[0].info.run_id
    print(f"Found run: {run_id}")

    print("Downloading model bundle from Dagshub...")
    local_path = client.download_artifacts(
        run_id=run_id,
        path="bundle/rec_model_svd_v1.pkl"
    )

    # ── Load bundle ───────────────────────────────────────────────────────────
    print("Loading model bundle...")
    with open(local_path, "rb") as f:
        bundle = pickle.load(f)

    svd              = bundle["svd"]
    customer_factors = bundle["customer_factors"]
    item_factors     = bundle["item_factors"]
    products_raw     = bundle["products_raw"]
    customer_index   = bundle["customer_index"]
    product_index    = bundle["product_index"]
    sparse_matrix    = bundle["customer_product_matrix"]

    print(f"Model loaded successfully ✅")
    print(f"Customers: {len(customer_index)}")
    print(f"Products:  {len(product_index)}")


# ── Recommendation function ───────────────────────────────────────────────────
def get_recommendations(customer_id: str, n: int = 5) -> dict:
    """
    Returns top-n recommendations for a given customer_id.
    Raises KeyError for unknown customers.
    """

    if customer_index is None:
        raise RuntimeError("Model not loaded. Call load_bundle() first.")

    if customer_id not in customer_index:
        raise KeyError(f"Customer '{customer_id}' not found.")

    customer_idx    = customer_index.index(customer_id)
    customer_vector = customer_factors[customer_idx]

    scores = np.dot(item_factors, customer_vector)

    customer_row   = sparse_matrix.getrow(customer_idx)
    interacted_idx = customer_row.nonzero()[1].tolist()
    scores[interacted_idx] = 0

    top_indices  = np.argsort(scores)[::-1][:n]
    top_products = [product_index[i] for i in top_indices]
    top_scores   = scores[top_indices].copy()

    if top_scores.max() > 0:
        top_scores = top_scores / top_scores.max()

    top_n = pd.DataFrame({
        "product_id":      top_products,
        "predicted_score": top_scores
    })
    top_n = top_n.merge(products_raw, on="product_id", how="left")
    top_n = top_n.sort_values("predicted_score", ascending=False)

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