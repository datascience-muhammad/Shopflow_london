import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

#-----------------------------------
# CONFIG
#-----------------------------------
# Base URL for the FastAPI backend
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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

# Initialize session state
if 'customer_data' not in st.session_state:
    st.session_state['customer_data'] = {}

#-----------------------------------
# SIDEBAR INPUT
#-----------------------------------
with st.sidebar:
    st.header("📊 Customer Information")
    
    customer_id = st.text_input("Customer ID", value="12345")
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
    total_spent = st.number_input("Total Spent ($)", min_value=0.0, value=500.0, step=10.0)
    num_purchases = st.number_input("Number of Purchases", min_value=0, value=10, step=1)
    last_purchase_date = st.date_input("Last Purchase Date", value=datetime(2024, 1, 1))
    preferred_category = st.selectbox("Preferred Category", options=["Electronics", "Clothing", "Home", "Books", "Other"])
    
    st.divider()
    st.markdown("### 🚀 Actions")
    
    predict_btn = st.button("🔮 Predict Churn", type="primary", use_container_width=True)
    recommend_btn = st.button("🎯 Generate Recommendations", use_container_width=True)

# Update session state
st.session_state['customer_data'] = {
    'customer_id': customer_id,
    'age': age,
    'gender': gender,
    'total_spent': total_spent,
    'num_purchases': num_purchases,
    'last_purchase_date': last_purchase_date,
    'preferred_category': preferred_category
}

#-----------------------------------
# HELPER FUNCTIONS
#-----------------------------------
def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def display_metrics():
    """Display customer metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    days_since_last = (datetime.now().date() - last_purchase_date).days
    avg_purchase = total_spent / num_purchases if num_purchases > 0 else 0
    
    with col1:
        st.metric("Customer ID", customer_id)
        st.metric("Age", age)
    
    with col2:
        st.metric("Total Spent", f"${total_spent:,.2f}")
        st.metric("Gender", gender)
    
    with col3:
        st.metric("Purchases", num_purchases)
        st.metric("Avg Purchase", f"${avg_purchase:,.2f}")
    
    with col4:
        st.metric("Days Since Last", f"{days_since_last}d")
        st.metric("Category", preferred_category)

#-----------------------------------
# MAIN CONTENT
#-----------------------------------
# Check backend connection
if check_backend():
    st.success("✅ Connected to backend successfully!")
else:
    st.error(f"❌ Cannot connect to backend at {BASE_URL}")
    st.info("💡 Run this command in terminal: uvicorn api:app --reload --port 8000")
    st.stop()

# Display customer metrics
st.subheader("📋 Customer Summary")
display_metrics()
st.divider()

#-----------------------------------
# PREDICT CHURN
#-----------------------------------
if predict_btn:
    input_data = {
        "customer_id": str(customer_id),
        "age": int(age),
        "gender": gender.lower(),
        "total_spent": float(total_spent),
        "num_purchases": int(num_purchases),
        "last_purchase_date": last_purchase_date.isoformat(),
        "preferred_category": preferred_category.lower()
    }
    
    with st.spinner("🤖 Analyzing churn risk..."):
        try:
            response = requests.post(
                f"{BASE_URL}/predict_churn", 
                json=input_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("🎯 Churn Prediction Result")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    prob = result.get('churn_probability', 0)
                    
                    # Color-coded probability
                    if prob < 0.3:
                        st.success(f"### {prob:.1%} Churn Probability")
                        st.markdown("#### ✅ Low Risk")
                    elif prob < 0.6:
                        st.warning(f"### {prob:.1%} Churn Probability")
                        st.markdown("#### ⚠️ Medium Risk")
                    else:
                        st.error(f"### {prob:.1%} Churn Probability")
                        st.markdown("#### 🔴 High Risk")
                    
                    if 'confidence' in result:
                        st.metric("Confidence", f"{result['confidence']:.1%}")
                
                with col2:
                    st.metric("Model Version", result.get('model_version', 'N/A'))
                    st.metric("Timestamp", result.get('timestamp', 'N/A')[:10])
                    
                    # Recommendations based on risk
                    st.divider()
                    st.write("**💡 Action Items:**")
                    if prob < 0.3:
                        st.info("• Upsell premium products\n• Invite to loyalty program")
                    elif prob < 0.6:
                        st.warning("• Send discount offer\n• Share personalized recommendations")
                    else:
                        st.error("• Immediate retention offer\n• Personal outreach needed")
            else:
                st.error(f"Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

#-----------------------------------
# GENERATE RECOMMENDATIONS
#-----------------------------------
if recommend_btn:
    with st.spinner("🔄 Generating recommendations..."):
        try:
            response = requests.get(
                f"{BASE_URL}/recommendations/{customer_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.subheader("✨ Personalized Recommendations")
                
                if result.get('recommendations'):
                    df = pd.DataFrame(result['recommendations'])
                    
                    # Format columns if they exist
                    if 'price' in df.columns:
                        df['price'] = df['price'].apply(lambda x: f"${x:,.2f}")
                    if 'predicted_score' in df.columns:
                        df['predicted_score'] = df['predicted_score'].apply(lambda x: f"{x:.1%}")
                    
                    # Select columns to display
                    display_cols = ['product_name', 'category', 'price', 'reason']
                    available_cols = [col for col in display_cols if col in df.columns]
                    
                    st.dataframe(df[available_cols], use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"Model: {result.get('model_version', 'N/A')}")
                    with col2:
                        st.caption(f"Generated: {result.get('timestamp', 'N/A')[:10]}")
                else:
                    st.info("No recommendations available")
            else:
                st.error(f"Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

#-----------------------------------
# FOOTER
#-----------------------------------
st.divider()
st.caption(f"🔗 Backend: {BASE_URL} | 🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")