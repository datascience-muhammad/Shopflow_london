from pydantic import BaseModel, Field
from typing import List


# ── Individual recommendation item ──────────────────────────────────────────
class RecommendationItem(BaseModel):
    product_id:      str
    product_name:    str
    category:        str
    predicted_score: float = Field(..., ge=0.0, le=1.0)


# ── Top-level response — matches Contract 2 exactly ─────────────────────────
class RecommendationResponse(BaseModel):
    customer_id:     str
    recommendations: List[RecommendationItem]
    model_version:   str
    timestamp:       str


# ── Error responses ──────────────────────────────────────────────────────────
class ErrorResponse(BaseModel):
    detail: str