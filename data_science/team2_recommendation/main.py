import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from schemas import RecommendationResponse, RecommendationItem, ErrorResponse

# ── Lifespan — load model on startup ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    import threading
    from model import load_bundle
    thread = threading.Thread(target=load_bundle, daemon=True)
    thread.start()
    yield

# ── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "ShopFlow Recommendation API",
    description = "DS Team 2 — GET /recommend/{customer_id} — Contract 2",
    version     = "1.0.0",
    lifespan    = lifespan
)

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

# ── Recommendation endpoint ───────────────────────────────────────────────────
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
    from model import get_recommendations
    try:
        result = get_recommendations(customer_id=customer_id, n=n)
        return result
    except KeyError:
        raise HTTPException(
            status_code = 404,
            detail      = f"Customer '{customer_id}' not found."
        )
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = f"Prediction service unavailable: {str(e)}"
        )