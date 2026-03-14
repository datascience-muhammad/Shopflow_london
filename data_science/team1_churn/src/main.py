import json
import os
from datetime import datetime, timezone

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.schemas import PredictRequest, PredictResponse

APP_NAME = "ShopFlow Churn API"
MODEL_VERSION = "1.0.0"
THRESHOLD_DEFAULT = 0.5

# team1_churn/src/main.py -> team1_churn/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

MODEL_PATH = os.path.join(ARTIFACT_DIR, "churn_model.joblib")
FEATURES_PATH = os.path.join(ARTIFACT_DIR, "feature_names.json")

app = FastAPI(title=APP_NAME, version=MODEL_VERSION)

model = None
feature_columns = None


@app.on_event("startup")
def load_artifacts():
    global model, feature_columns

    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model not found at: {MODEL_PATH}")

    if not os.path.exists(FEATURES_PATH):
        raise RuntimeError(f"Feature schema not found at: {FEATURES_PATH}")

    model = joblib.load(MODEL_PATH)

    with open(FEATURES_PATH, "r") as f:
        feature_columns = json.load(f)

    if not isinstance(feature_columns, list) or len(feature_columns) == 0:
        raise RuntimeError("feature_names.json must be a non-empty list")

    print(f"[Startup] Loaded model and {len(feature_columns)} feature columns.")


@app.get("/")
def home():
    return {
        "service": APP_NAME,
        "status": "running",
        "version": MODEL_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "n_features": len(feature_columns) if feature_columns else None,
        "version": MODEL_VERSION,
    }


def build_feature_row(payload: dict) -> pd.DataFrame:
    """
    Build a 1-row dataframe with columns in the exact order expected by the model.
    Missing features are set to 0. Extra features are ignored.
    """
    row = {col: 0 for col in feature_columns}

    for k, v in payload.items():
        if k in row:
            row[k] = v

    X = pd.DataFrame([row], columns=feature_columns)

    for col in X.columns:
        if X[col].dtype == "object":
            X[col] = pd.to_numeric(X[col], errors="ignore")

    return X


@app.post("/predict/churn", response_model=PredictResponse)
def predict(req: PredictRequest, threshold: float = THRESHOLD_DEFAULT):
    if model is None or feature_columns is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    if not (0.0 < threshold < 1.0):
        raise HTTPException(status_code=400, detail="threshold must be between 0 and 1")

    try:
        X = build_feature_row(req.features)
        proba = float(model.predict_proba(X)[:, 1][0])

        churn_prediction = "high_risk" if proba >= threshold else "low_risk"
        confidence = float(max(proba, 1 - proba))

        return PredictResponse(
            customer_id=req.customer_id,
            churn_probability=proba,
            churn_prediction=churn_prediction,
            confidence=confidence,
            model_version=MODEL_VERSION,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")git