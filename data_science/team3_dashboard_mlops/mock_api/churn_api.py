from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime
import uvicorn

app = FastAPI()

# Load the pre-trained model from the specified file path
try:
    model = joblib.load("models/churn_model.pkl")
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model file not found. Please ensure 'models/churn_model.pkl' exists.")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

MODEL_VERSION = "CHURN_MODEL_V1"  # Define a constant for the model version

# Define input data structure
class ChurnInput(BaseModel):
    customer_id: str
    age: int
    gender: str
    recent_purchases: int
    total_spent: float
    days_since_last_purchase: int
    num_of_products: int
    preferred_category: str

# Define output structure
class ChurnPrediction(BaseModel):
    customer_id: str
    churn_probability: float
    prediction_time: datetime
    model_version: str

@app.post("/predict_churn", response_model=ChurnPrediction)
def predict_churn(input_data: ChurnInput) -> ChurnPrediction:
    # Prepare the input data for prediction
    # Note: Categorical features like gender and preferred_category need encoding
    # This is a simplified version - you'll need to match your model's feature preprocessing
    
    x = [[
        input_data.age,
        input_data.recent_purchases,
        input_data.total_spent,
        input_data.days_since_last_purchase,
        input_data.num_of_products,
        # Add encoded categorical features here based on your model's requirements
    ]]

    # Make prediction using the loaded model
    if model:
        try:
            # Assuming the model has a predict_proba method
            churn_probability = float(model.predict_proba(x)[0][1])
        except Exception as e:
            print(f"Prediction error: {e}")
            churn_probability = 0.5  # Default value on error
    else:
        churn_probability = 0.5  # Default value when model is not available

    return ChurnPrediction(
        customer_id=input_data.customer_id,
        churn_probability=churn_probability,
        prediction_time=datetime.now(),
        model_version=MODEL_VERSION
    )

@app.get("/")
def root():
    return {"message": "Welcome to the Churn Prediction API. Use the /predict_churn endpoint to get predictions."}

@app.get("/health")
def health():
    status = "healthy" if model else "degraded (model not loaded)"
    return {"status": f"API is {status} and running."}

@app.get("/sample_input")
def sample_input():
    return {
        "customer_id": "12345",
        "age": 30,
        "gender": "Male",
        "recent_purchases": 5,
        "total_spent": 500.0,
        "days_since_last_purchase": 10,
        "num_of_products": 3,
        "preferred_category": "Electronics"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 