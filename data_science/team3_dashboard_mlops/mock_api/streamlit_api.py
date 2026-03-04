import streamlit as st
import requests
import pandas as pd
from datetime import datetime

#-----------------------------------
# CONFIG
#-----------------------------------
# Base URL for the FastAPI backend
# Change this to your actual backend URL when deployed
BASE_URL = "http://localhost:8000"  # Default for local development
# For production, you might want to use environment variable:
# import os
# BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

#-----------------------------------
# PAGE CONFIG
#-----------------------------------
st.set_page_config(
    page_title="ShopFlow Churn Dashboard", 
    page_icon="🛍️",
    layout="wide"
)

#-----------------------------------
# HEADER
#-----------------------------------
st.title("🛍️ ShopFlow Customer Intelligence Dashboard")
st.markdown("Predict customer churn and generate personalized recommendations")
st.divider()

#-----------------------------------
# SIDEBAR INPUT
#-----------------------------------
st.sidebar.header("📊 Customer Information")

customer_id = st.sidebar.text_input("Customer ID", value="12345")
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
gender = st.sidebar.selectbox("Gender", options=["Male", "Female", "Other"])
total_spent = st.sidebar.number_input("Total Spent ($)", min_value=0.0, value=500.0, step=10.0)
num_purchases = st.sidebar.number_input("Number of Purchases", min_value=0, value=10, step=1)
last_purchase_date = st.sidebar.date_input("Last Purchase Date", value=datetime(2024, 1, 1))
preferred_category = st.sidebar.selectbox("Preferred Category", options=["Electronics", "Clothing", "Home", "Books", "Other"])

st.sidebar.divider()
st.sidebar.markdown("### 🚀 Actions")

# Store customer data in session state for persistence
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = {
        'customer_id': customer_id,
        'age': age,
        'gender': gender,
        'total_spent': total_spent,
        'num_purchases': num_purchases,
        'last_purchase_date': last_purchase_date,
        'preferred_category': preferred_category
    }

# Update session state with current values
st.session_state['customer_data'].update({
    'customer_id': customer_id,
    'age': age,
    'gender': gender,
    'total_spent': total_spent,
    'num_purchases': num_purchases,
    'last_purchase_date': last_purchase_date,
    'preferred_category': preferred_category
})

#-----------------------------------
# HELPER FUNCTIONS
#-----------------------------------
def check_backend_health():
    """Check if the backend is available"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def format_currency(value):
    """Format currency values"""
    return f"${value:,.2f}"

#-----------------------------------
# MAIN CONTENT AREA - Customer Summary
#-----------------------------------
col1, col2 = st.columns([1, 3])

with col1:
    if check_backend_health():
        st.success("✅ Backend Connected")
    else:
        st.error(f"❌ Cannot connect to backend at {BASE_URL}")
        st.info("💡 Make sure the FastAPI server is running on port 8000")

# Customer summary section
with st.container():
    st.subheader("📋 Customer Summary")
    
    # Calculate metrics
    days_since_last = (datetime.now().date() - last_purchase_date).days
    avg_purchase_value = total_spent / num_purchases if num_purchases > 0 else 0
    
    # Create metrics in columns
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Customer ID", customer_id)
        st.metric("Age", age)
    
    with metric_col2:
        st.metric("Total Spent", format_currency(total_spent))
        st.metric("Gender", gender)
    
    with metric_col3:
        st.metric("Num Purchases", num_purchases)
        st.metric("Avg Purchase", format_currency(avg_purchase_value))
    
    with metric_col4:
        st.metric("Days Since Last Purchase", f"{days_since_last} days")
        st.metric("Preferred Category", preferred_category)

st.divider()

#-----------------------------------
# PREDICT CHURN BUTTON
#-----------------------------------
if st.sidebar.button("🔮 Predict Churn", type="primary", use_container_width=True):
    # Prepare input data
    input_data = {
        "customer_id": str(customer_id),
        "age": int(age),
        "gender": gender.lower(),
        "total_spent": float(total_spent),
        "num_purchases": int(num_purchases),
        "last_purchase_date": last_purchase_date.isoformat(),
        "preferred_category": preferred_category.lower()
    }
    
    # Show loading spinner
    with st.spinner("🤖 Analyzing customer data for churn prediction..."):
        try:
            response = requests.post(
                f"{BASE_URL}/predict_churn", 
                json=input_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display churn prediction results
                st.subheader("🎯 Churn Prediction Result")
                
                # Create columns for result display
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    # Extract churn probability (handle different response formats)
                    churn_prob = result.get('churn_probability', 0)
                    
                    # Color-coded probability
                    if churn_prob < 0.3:
                        st.success(f"### Churn Probability: {churn_prob:.2%}")
                        st.markdown("#### ✅ Low Risk Customer")
                    elif churn_prob < 0.6:
                        st.warning(f"### Churn Probability: {churn_prob:.2%}")
                        st.markdown("#### ⚠️ Medium Risk Customer")
                    else:
                        st.error(f"### Churn Probability: {churn_prob:.2%}")
                        st.markdown("#### 🔴 High Risk Customer")
                    
                    # Display additional fields if present
                    if 'churn_prediction' in result:
                        st.write(f"**Prediction:** {result['churn_prediction']}")
                    if 'confidence' in result:
                        st.write(f"**Confidence:** {result['confidence']:.2%}")
                
                with res_col2:
                    st.write("**Model Information:**")
                    st.write(f"📊 Model Version: {result.get('model_version', 'N/A')}")
                    st.write(f"🕐 Timestamp: {result.get('timestamp', 'N/A')}")
                    
                    # Add recommendation based on churn probability
                    st.divider()
                    st.write("**💡 Recommended Actions:**")
                    
                    if churn_prob < 0.3:
                        st.info("• Consider upselling premium products\n• Invite to loyalty program")
                    elif churn_prob < 0.6:
                        st.warning("• Send personalized email with discount\n• Target with relevant recommendations")
                    else:
                        st.error("• Offer immediate retention incentives\n• Personal outreach required")
                
                # Store result in session state
                st.session_state['last_churn_result'] = result
                
            else:
                st.error(f"❌ Error predicting churn. Status code: {response.status_code}")
                if response.text:
                    st.error(f"Details: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {BASE_URL}")
            st.info("💡 Make sure the FastAPI server is running: `uvicorn api:app --reload --port 8000`")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Backend might be overloaded.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

#-----------------------------------
# GENERATE RECOMMENDATIONS BUTTON
#-----------------------------------
if st.sidebar.button("🎯 Generate Recommendations", use_container_width=True):
    try:
        with st.spinner("🔄 Generating personalized recommendations..."):
            response = requests.get(
                f"{BASE_URL}/recommendations/{customer_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("✨ Personalized Recommendations")
                
                # Display recommendations
                if 'recommendations' in result and result['recommendations']:
                    recommendations = result['recommendations']
                    
                    # Convert to DataFrame for better display
                    df = pd.DataFrame(recommendations)
                    
                    # Select columns to display (with fallbacks)
                    display_columns = []
                    for col in ["product_id", "product_name", "category", "price", "predicted_score", "reason"]:
                        if col in df.columns:
                            display_columns.append(col)
                    
                    if display_columns:
                        # Format price if present
                        if 'price' in df.columns:
                            df['price'] = df['price'].apply(lambda x: f"${x:,.2f}" if isinstance(x, (int, float)) else x)
                        
                        # Format score if present
                        if 'predicted_score' in df.columns:
                            df['predicted_score'] = df['predicted_score'].apply(
                                lambda x: f"{x:.2%}" if isinstance(x, (int, float)) else x
                            )
                        
                        st.dataframe(df[display_columns], use_container_width=True, hide_index=True)
                    else:
                        st.table(recommendations)
                    
                    # Display metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"📊 Model Version: {result.get('model_version', 'N/A')}")
                    with col2:
                        st.info(f"🕐 Generated: {result.get('timestamp', 'N/A')}")
                    
                    st.markdown("---")
                    st.caption("**Note:** Recommendations are based on the customer's purchase history and preferences.")
                    
                else:
                    st.warning("No recommendations available for this customer.")
                    
            elif response.status_code == 404:
                st.warning(f"Customer {customer_id} not found. No recommendations available.")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
                
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {BASE_URL}")
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

#-----------------------------------
# DISPLAY SAMPLE RESPONSE FORMATS (Hidden in expander)
#-----------------------------------
with st.sidebar.expander("📝 API Reference", expanded=False):
    st.markdown("""
    **Churn Prediction Response:**
    ```json
    {
        "customer_id": "C12345", 
        "churn_probability": 0.85,
        "churn_prediction": "High Risk",
        "confidence": 0.92,
        "model_version": "1.0.0", 
        "timestamp": "2024-06-01T12:00:00Z"
    }
    ```
    
    **Recommendations Response:**
    ```json
    {
        "customer_id": "C12345", 
        "recommendations": [
            {
                "product_id": "P67890", 
                "product_name": "Wireless Headphones", 
                "category": "Electronics",
                "price": 99.99,
                "predicted_score": 0.95,
                "reason": "Based on your interest in electronics"
            }
        ], 
        "model_version": "1.0.0",
        "timestamp": "2024-06-01T12:05:00Z"
    }
    ```
    """)

#-----------------------------------
# FOOTER
#-----------------------------------
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"🔗 Backend: {BASE_URL}")
with col2:
    st.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col3:
    st.caption("🛍️ ShopFlow Analytics v1.0")