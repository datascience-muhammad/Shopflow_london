from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional
import random
import uvicorn

app = FastAPI(title="ShopFlow API")

# Request/Response Models
class CustomerData(BaseModel):
    customer_id: str
    age: int = Field(..., ge=18, le=100)
    gender: str
    total_spent: float = Field(..., ge=0)
    num_purchases: int = Field(..., ge=0)
    last_purchase_date: date
    preferred_category: str

class ChurnResponse(BaseModel):
    customer_id: str
    churn_probability: float
    confidence: float
    model_version: str
    timestamp: datetime

class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    price: float
    predicted_score: float
    reason: str

class RecommendationsResponse(BaseModel):
    customer_id: str
    recommendations: List[Product]
    model_version: str
    timestamp: datetime

# Sample product database
PRODUCTS = [
    {"id": "P1001", "name": "Wireless Headphones", "category": "Electronics", "price": 99.99},
    {"id": "P1002", "name": "Smart Watch", "category": "Electronics", "price": 199.99},
    {"id": "P1003", "name": "Leather Jacket", "category": "Clothing", "price": 149.99},
    {"id": "P1004", "name": "Coffee Maker", "category": "Home", "price": 79.99},
    {"id": "P1005", "name": "Bestseller Novel", "category": "Books", "price": 24.99},
]

@app.get("/")
async def root():
    return {"message": "ShopFlow API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/predict_churn", response_model=ChurnResponse)
async def predict_churn(customer: CustomerData):
    """
    Predict churn probability for a customer
    """
    try:
        # Calculate days since last purchase
        days_since_last = (datetime.now().date() - customer.last_purchase_date).days
        
        # Simple rule-based churn prediction
        churn_score = 0.0
        
        # Days since last purchase
        if days_since_last > 60:
            churn_score += 0.4
        elif days_since_last > 30:
            churn_score += 0.2
        
        # Number of purchases
        if customer.num_purchases < 5:
            churn_score += 0.3
        elif customer.num_purchases < 10:
            churn_score += 0.15
        
        # Total spent
        if customer.total_spent < 100:
            churn_score += 0.2
        elif customer.total_spent < 500:
            churn_score += 0.1
        
        # Age factor
        if customer.age < 25:
            churn_score += 0.1
        elif customer.age > 50:
            churn_score -= 0.1
        
        # Add some randomness
        churn_score += random.uniform(-0.1, 0.1)
        
        # Ensure probability is between 0 and 1
        churn_probability = max(0.0, min(1.0, churn_score))
        
        return ChurnResponse(
            customer_id=customer.customer_id,
            churn_probability=round(churn_probability, 3),
            confidence=round(random.uniform(0.85, 0.95), 3),
            model_version="v1.0.0",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations/{customer_id}", response_model=RecommendationsResponse)
async def get_recommendations(customer_id: str):
    """
    Get personalized product recommendations for a customer
    """
    try:
        # Generate recommendations based on customer ID
        # In production, this would use a real ML model
        num_recs = random.randint(2, 4)
        
        # Select random products and add scores/reasons
        recommendations = []
        for product in random.sample(PRODUCTS, min(num_recs, len(PRODUCTS))):
            score = round(random.uniform(0.7, 0.98), 3)
            recommendations.append(
                Product(
                    product_id=product["id"],
                    product_name=product["name"],
                    category=product["category"],
                    price=product["price"],
                    predicted_score=score,
                    reason=f"Recommended based on your interest in {product['category'].lower()}"
                )g
        return RecommendationsResponse(
            customer_id=customer_id,
            recommendations=recommendations,
            model_version="rec-v1.0.0",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)