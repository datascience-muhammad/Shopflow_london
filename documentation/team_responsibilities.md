# Team Responsibilities

## 1. Project Management (PM) Teams - ~10 people

### PM Team 1: Technical Delivery (3-4 members)

**Technical Project Managers**

- **Infrastructure:** Local development environment setup, Docker containerization.
- **Integration:** Managing API integration between models and dashboard.
- **Tracking:** Daily monitoring of model development progress.
- **Deployment:** Assisting with local Docker deployment and troubleshooting.

### PM Team 2: Business Delivery (3-4 members)

**Product Owners / Business Analysts**

- **Stakeholder Management:** Communication updates and expectation setting.
- **Business Impact:** Translating model outputs (e.g., probability) to business value (e.g., £ saved).
- **KPIs:** Tracking success metrics against benchmarks (ROI analysis).
- **Validation:** Ensuring features align with business requirements.

### PM Team 3: QA & Documentation (3-4 members)

**QA Leads / Technical Writers**

- **Quality Assurance:** Model accuracy audits, API stress testing (100 concurrent requests).
- **Documentation:** Compiling API specs, model cards, and user guides.
- **Demo:** Coordinating the final stakeholder demonstration and rehearsal.
- **Validation:** Independent verification of Precision/Recall metrics.

---

## 2. Data Science (DS) Teams - ~10 people

### DS Team 1: Churn Prediction (3-4 members)

**Machine Learning Engineers**

- **Feature Engineering:** Building RFM and behavioral features for churn.
- **Modeling:** Training and tuning XGBoost/Random Forest models.
- **API:** Developing the `POST /predict/churn` FastAPI endpoint.
- **Optimization:** Achieving AUC > 0.75 and F1 > 0.70.

### DS Team 2: Recommendations (3-4 members)

**Algorithm Engineers**

- **Algorithm:** Building collaborative filtering (item-item similarity) logic.
- **API:** Developing the `GET /recommend/{id}` endpoint.
- **Prototype:** Ensuring relevance scores are functional and logical.
- **Performance:** Response latency < 300ms.

### DS Team 3: Dashboard & MLOps (3-4 members)

**Full Stack Data Scientists**

- **Visualization:** Building the Streamlit dashboard (predictions, key metrics).
- **MLOps:** Setting up experiment tracking (MLflow/W&B) and model registry.
- **Integration:** Consuming local APIs to display real-time insights.
- **Containerization:** Ensuring the dashboard runs smoothly in Docker.

---

## 3. Leadership Roles (Leads)

### PM Lead (1 person)

- **Responsibility:** Overall project coordination, sprint planning, and high-level stakeholder management.
- **Focus:** Removing cross-team blockers and ensuring timeline adherence.

### DS Lead (1 person)

- **Responsibility:** Technical architecture, code reviews, and model strategy.
- **Focus:** Ensuring code quality, API standards, and methodological rigor.
