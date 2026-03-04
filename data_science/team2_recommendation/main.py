import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from schemas import RecommendationResponse, RecommendationItem, ErrorResponse
from model import get_recommendations

# ── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "ShopFlow Recommendation API",
    description = "DS Team 2 — GET /recommend/{customer_id} — Contract 2",
    version     = "1.0.0"
)

# Allow Team 3 dashboard and Postman to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)


# ── Health check ─────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status":    "ok",
        "team":      "DS Team 2 — Recommendations",
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }


# ── Recommendation endpoint — Contract 2 ─────────────────────────────────────
@app.get(
    "/recommend/{customer_id}",
    response_model = RecommendationResponse,
    responses      = {
        404: {"model": ErrorResponse, "description": "Customer not found"},
        422: {"model": ErrorResponse, "description": "Invalid value for n"},
    }
)
def recommend(
    customer_id: str,
    n: int = Query(default=5, ge=1, le=20, description="Number of recommendations (1–20)")
):
    """
    Returns top-n product recommendations for a customer.

    - **customer_id**: ShopFlow customer ID (e.g. CUST000001)
    - **n**: number of recommendations to return (default 5, max 20)
    """
    try:
        result = get_recommendations(customer_id=customer_id, n=n)
        return result

    except KeyError:
        # 404 — customer not in the model's training data
        raise HTTPException(
            status_code = 404,
            detail      = f"Customer '{customer_id}' not found."
        )

    except Exception as e:
        # 500 — unexpected error
        raise HTTPException(
            status_code = 500,
            detail      = f"Prediction service unavailable: {str(e)}"
        )