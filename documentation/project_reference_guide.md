# Project Reference Guide

**ShopFlow Customer Intelligence Platform — 2-Week Sprint**  
**Project:** ShopFlow by PrimeCart Inc.  
**Audience:** All team members — PM and DS  
**Purpose:** Single reference for project specifications, data environment, model targets, tools, and API details. The **DS Coordination Guide** and **PM Coordination Guide** are the operational documents for day-to-day work. This document is the spec sheet both guides point to.

**Repository Path:** `documentation/project_reference_guide.md`  
**Last Updated:** February 2026

---

## 1. Project Team Organization

### Team Structure Overview

| Team          | Focus Area             | Members | Key Responsibilities                                          |
| :------------ | :--------------------- | :------ | :------------------------------------------------------------ |
| **PM Lead**   | Overall Coordination   | 1       | Sprint planning, stakeholder management, cross-team alignment |
| **PM Team 1** | Technical Delivery     | 3-4     | Environment setup, Render deployment support, API integration |
| **PM Team 2** | Business Delivery      | 3-4     | Stakeholder comms, KPI tracking, business impact translation  |
| **PM Team 3** | QA & Documentation     | 3-4     | Model validation, API testing, documentation, demo prep       |
| **DS Lead**   | Technical Architecture | 1       | Model strategy, technical decisions, code review              |
| **DS Team 1** | Churn Prediction       | 3-4     | EDA, churn model development, FastAPI deployment              |
| **DS Team 2** | Recommendations        | 3-4     | Collaborative filtering, recommendation API                   |
| **DS Team 3** | Dashboard & MLOps      | 3-4     | Streamlit dashboard, experiment tracking, model registry      |

**Total Team Size:** ~10 PMs + ~10 Data Scientists (flexible based on availability)  
**Note:** This model focuses on local development and deployment, with data infrastructure pre-provisioned for rapid prototyping.

---

## 2. Infrastructure & Technical Architecture

### Architecture Overview

The architecture is designed for **local development and prototyping**. Data is pre-provisioned, allowing DS teams to focus on modeling.

### Data Science Workflow

1.  **Data Access:** DS teams pull directly from **AWS S3 Curated Layer** with pre-cleaned core tables
2.  **Exploration:** Use Jupyter Notebooks for EDA on raw tables (`customers`, `orders`, `products`, `events`)
3.  **Feature Engineering:** Build your own feature sets through custom engineering - **do not use pre-computed `ml_features` table**
4.  **Model Development:** Train models using your engineered features (scikit-learn/XGBoost)
5.  **MLOps:** Track experiments and register models using **MLflow** or **Weights & Biases**
6.  **API Development:** Wrap models in **FastAPI**, test locally with **ngrok**, deploy to **Render** for production
7.  **Dashboard:** Build **Streamlit Dashboard** consuming both S3 data and local API predictions

---

## 3. Data Science (DS) Technical Scope

### 3.1 Provided Data Environment

DS teams start with raw curated tables. You will build your own features through feature engineering.

**Star Schema Access:**

**Dimension Tables:**

- `dim_customers`: 100,000+ records
  - **Fields:** customer_id, signup_date, demographics, loyalty_tier
- `dim_products`: 5,000+ items
  - **Fields:** product_id, category, brand, price, margin

**Fact Tables:**

- `fact_orders`: 500,000+ transactions
  - **Fields:** order_id, customer_id, product_id, amount, timestamp, payment_method
- `fact_events`: 2,000,000+ web interactions (sampled to 500K for 2-week sprint)
  - **Fields:** event_id, customer_id, session_id, event_type, timestamp, device

**Feature Engineering Expectations:**
You must build your own features, including:

- **Transactional Features (to engineer):**
  - Recency: Days since last purchase
  - Frequency: Number of orders
  - Monetary: Total spend
  - Tenure: Days since signup
  - Average order value
- **Behavioral Features (to engineer):**
  - Session counts and patterns
  - Cart abandonment rates
  - Category diversity
  - Device preferences
  - Purchase velocity

**Note:** There is **NO** pre-computed `ml_features` table. Feature engineering is a core deliverable of this sprint.

### 3.2 Model Requirements & API Specifications

| Model                | Goal                             | Target Metric              | API Endpoint                   | Response Time |
| :------------------- | :------------------------------- | :------------------------- | :----------------------------- | :------------ |
| **Churn Prediction** | Predict 90-day churn probability | AUC > 0.75, F1 > 0.70      | `POST /predict/churn`          | < 300ms       |
| **Recommendation**   | Top-5 product suggestions        | Relevance score functional | `GET /recommend/{customer_id}` | < 300ms       |

**MLOps Requirements:**

- **Experiment Tracking** (using MLflow or Weights & Biases):
  - Log all training runs with hyperparameters
  - Track metrics across experiments (accuracy, AUC, F1, precision, recall)
  - Compare model versions
  - Store training artifacts
- **Model Registry:**
  - Register trained models with versioning (v1.0, v1.1, etc.)
  - Include model metadata (training date, features used, performance metrics)
  - Track model lineage and dependencies
  - Enable model rollback if needed

**API Request/Response Formats:**

**Churn Prediction Endpoint:**

- **Method:** `POST /predict/churn`
- **Request includes:** `customer_id`, features (recency, frequency, monetary, tenure, etc.)
- **Response includes:** `customer_id`, `churn_probability`, `churn_prediction` (high_risk/low_risk), `confidence`, `model_version`, `timestamp`

**Recommendation Endpoint:**

- **Method:** `GET /recommend/{customer_id}?n=5`
- **Response includes:** `customer_id`, list of recommendations (`product_id`, `product_name`, `category`, `predicted_score`, `reason`), `model_version`, `timestamp`

---

## 4. Project Management (PM) Governance

### 4.1 Sprint Lifecycle (2-Week Timeline)

**Week 1: Foundation & Build**

- **PM Team 1 (Technical Delivery):**
  - Ensure data access credentials and S3 permissions configured
  - Set up local Docker development environment
  - Set up MLOps tools (MLflow or Weights & Biases)
  - Track model development progress in Jira
  - Prepare local infrastructure for API deployment
- **PM Team 2 (Business Delivery):**
  - Validate feature selection aligns with business KPIs
  - Document stakeholder requirements
  - Begin drafting success metrics framework
  - Prepare mid-sprint stakeholder update
- **PM Team 3 (QA & Documentation):**
  - Review EDA findings for data quality issues
  - Begin drafting API documentation templates
  - Set up testing environments
- **DS Teams:**
  - Focus on feature selection and baseline models
  - Conduct EDA and statistical validation
  - Begin model training iterations

**Week 2: Integrate, Deploy & Finalize**

- **PM Team 1 (Technical Delivery):**
  - Assist DS teams with local Docker deployment
  - Validate API integration points
  - Monitor local deployment and API latency
  - Coordinate final integration testing
- **PM Team 2 (Business Delivery):**
  - Align model performance with business outcomes
  - Prepare final presentation and ROI analysis
  - Coordinate stakeholder demo
  - Document business impact metrics
- **PM Team 3 (QA & Documentation):**
  - Independently verify model metrics before production sign-off
  - Conduct API stress testing (target: 100 concurrent requests)
  - Finalize all documentation (API specs, model cards, deployment guides)
  - Prepare demo environment and materials
- **DS Teams:**
  - Finalize model training and validation
  - Deploy FastAPI endpoints locally via Docker
  - Implement MLOps: experiment tracking and model registry
  - Build and test Streamlit dashboard
  - Conduct end-to-end integration testing

### 4.2 Quality Assurance (PM Team 3 Checklist)

**API Validation:**

- [ ] Endpoints return valid JSON predictions
- [ ] Response time < 300ms (average across 100 requests)
- [ ] Error handling covers edge cases (missing features, invalid IDs)
- [ ] API documentation (Swagger/OpenAPI) is complete and accurate

**Model Accuracy Audit:**

- [ ] Independently verify Precision/Recall on test set
- [ ] Confirm AUC scores meet targets (Churn: > 0.75)
- [ ] Review confusion matrices for class imbalance handling
- [ ] Validate feature importance rankings are business-logical

**Dashboard Validation:**

- [ ] All visualizations render correctly
- [ ] Real-time predictions display without lag
- [ ] Filters and controls function as expected
- [ ] Dashboard loads in < 5 seconds

**Documentation Review:**

- [ ] Model cards include methodology, features, performance
- [ ] API documentation tested with sample requests
- [ ] Deployment guide enables reproducible setup
- [ ] Data dictionary covers all features used

---

## 5. Communication & Success Criteria

### 5.1 Daily Communication Protocol

**Morning Standup (15 min) - 9:00 AM**

- **Agenda:**
  - DS Updates: Model iterations, metric improvements, technical blockers
  - PM Updates: Infrastructure status, stakeholder feedback, dependency management
  - Alignment: Quick wins, priority adjustments, resource needs
- **Format:**
  - What was completed yesterday?
  - What's planned for today?
  - Any blockers or dependencies?

**End-of-Day Sync (10 min) - 5:00 PM**

- **Agenda:**
  - Review progress against sprint goals
  - Update Jira board and burn-down chart
  - Flag risks for next-day resolution
  - Celebrate small wins

---

## 6. Tools & Platforms Reference

**Project Management:**

- **Jira:** Sprint planning, task tracking, velocity monitoring
- **Confluence:** Documentation, decision logs, knowledge base
- **Slack/Teams:** Real-time team communication
- **GitHub:** Code repository, version control, pull requests

**Development:**

- **Jupyter Notebooks:** EDA, model experimentation
- **VS Code / PyCharm:** IDE for Python development
- **Docker Desktop:** Local containerization and testing
- **Postman:** API endpoint testing

**AWS Services (Read-Only Access):**

- **S3:** Data lake for reading curated tables
- **IAM:** Access credentials for S3
- **Note:** No AWS deployment required - all work is local via Docker

**Data Science:**

- **Python 3.9+**
- **Libraries:** `pandas`, `numpy`, `scikit-learn`, `xgboost`, `fastapi`, `streamlit`, `plotly`
- **MLOps:** **MLflow** or **Weights & Biases** for experiment tracking and model registry.
