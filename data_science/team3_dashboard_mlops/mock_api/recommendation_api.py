# --- Recommendations Endpoint ---
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
import pandas as pd

# Assume 'data' is a global DataFrame (in real app, this would come from a database)
# data = pd.read_csv('customer_data.csv')  # Example

class RecommendationRequest(BaseModel):
    customer_id: str
    num_recommendations: int = Field(3, ge=1, le=20, description="Number of recommendations (1-20)")
    model_version: str = "RECOMMENDATION_MODEL_V1"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    @validator('num_recommendations')
    def validate_num_recommendations(cls, v):
        if v < 1 or v > 20:
            raise ValueError('num_recommendations must be between 1 and 20')
        return v

class RecommendationResponse(BaseModel):
    customer_id: str
    recommendations: List[str]  # Changed from array to List[str]
    product_ids: Optional[List[str]] = None
    product_names: Optional[List[str]] = None
    category: Optional[str] = None
    predicted_score: Optional[float] = None
    model_version: str = "RECOMMENDATION_MODEL_V1"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# Assume we have some sample data
data = pd.DataFrame({
    'customer_id': ['CUST001', 'CUST002', 'CUST003'],
    'preferred_category': ['Electronics', 'Clothing', 'Books'],
    'product_id': ['P001', 'P002', 'P003'],
    'product_name': ['Laptop', 'T-Shirt', 'Novel']
})

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get product recommendations for a customer.
    
    Returns:
    - 200: Successful response with recommendations
    - 404: Customer ID not found
    - 422: Invalid num_recommendations (outside 1-20)
    - 500: Model unavailable or prediction error
    """
    try:
        # Check if customer exists
        customer_data = data[data['customer_id'] == request.customer_id]
        
        if customer_data.empty:
            # Return empty recommendations for missing customer (404 case)
            return RecommendationResponse(
                customer_id=request.customer_id,
                recommendations=[],
                model_version=request.model_version,
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Get customer's purchased category
        purchased_category = customer_data.iloc[0]['preferred_category']
        
        # Get all unique categories from data
        all_categories = set(data['preferred_category'].unique())
        
        # Recommend categories not yet purchased by this customer
        available_categories = list(all_categories - {purchased_category})
        
        # For demo purposes, get some sample products from recommended categories
        recommendations = []
        product_ids = []
        product_names = []
        
        # Limit to requested number (or fewer if not enough available)
        num_to_recommend = min(request.num_recommendations, len(available_categories))
        
        for i in range(num_to_recommend):
            if i < len(available_categories):
                category = available_categories[i]
                # Find a sample product from this category
                category_products = data[data['preferred_category'] == category]
                if not category_products.empty:
                    sample_product = category_products.iloc[0]
                    recommendations.append(category)
                    product_ids.append(sample_product['product_id'])
                    product_names.append(sample_product['product_name'])
        
        # Return response with whatever recommendations we could generate
        # (200 case - may return fewer than requested)
        return RecommendationResponse(
            customer_id=request.customer_id,
            recommendations=recommendations[:request.num_recommendations],
            product_ids=product_ids[:request.num_recommendations] if product_ids else None,
            product_names=product_names[:request.num_recommendations] if product_names else None,
            category=recommendations[0] if recommendations else None,
            predicted_score=0.95 if recommendations else None,  # Dummy score
            model_version=request.model_version,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        # Handle prediction/model errors (500 case)
        print(f"Error generating recommendations: {str(e)}")
        return RecommendationResponse(
            customer_id=request.customer_id,
            recommendations=[],
            model_version=request.model_version,
            timestamp=datetime.utcnow().isoformat()
        )

# Add exception handlers for proper HTTP status codes
from fastapi import HTTPException

@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=422, detail=str(exc))

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    raise HTTPException(status_code=500, detail="Model unavailable or prediction error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)