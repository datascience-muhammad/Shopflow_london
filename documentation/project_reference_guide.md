# ShopFlow: AI-Powered Customer Intelligence & Predictive Personalization

**Industry / Sector:** E-commerce | Retail Tech | Predictive Analytics  
**Duration:** 2 Weeks  
**Team Composition:** Project Managers + Data Scientists

---

## 1. Company Overview
ShopFlow by PrimeCart Inc. is a London-based retail technology leader founded in 2018. The company's mission is to transform the UK and European e-commerce landscape through intelligent, data-driven customer experiences. While ShopFlow operates as a dynamic marketplace for fashion and electronics across major cities like London, Manchester, and Berlin, it has evolved into a pioneer of predictive analytics. With over 500,000 active monthly customers, ShopFlow leverages machine learning to anticipate customer needs, optimize stock availability, and maximize retention in a highly competitive market.

## 2. Business Challenge
*   **High Monthly Churn:** 15% monthly churn rate leading to a £2M annual revenue loss.
*   **Cart Abandonment:** 68% of customers abandon purchases before completion (£800K missed revenue).
*   **Ineffective Personalization:** Static recommendations resulting in a low 2% click-through rate.
*   **Operational Inefficiency:** 20% stockout and 30% overstock rates due to manual inventory planning.
*   **Fragmented Data:** Customer interactions and transaction records exist in siloed systems.
*   **Reactive Strategy:** Lack of predictive capability to identify at-risk customers before they leave.

## 3. Rationale for the Project
Customer retention and personalization are the primary drivers of profitability in the British e-commerce sector. Transitioning from reactive engagement to predictive intelligence allows ShopFlow to recover lost revenue and improve the efficiency of marketing and supply chain operations.

**This 2-week sprint focuses on:**
*   **Predictive Modeling:** Building a production-ready churn prediction model.
*   **Basic Personalization:** Implementing simplified recommendation logic.
*   **Proof of Concept Dashboard:** Creating a functional Streamlit prototype.
*   **Foundation for Scale:** Establishing patterns for future full deployment.

## 4. Project Objectives (2-Week Scope)
**Core Deliverables:**
*   **Churn Prediction Model:** Train and validate a binary classification model (Target: AUC > 0.75).
*   **Basic Recommendation Engine:** Rule-based + collaborative filtering prototype.
*   **Single FastAPI Endpoint:** Deploy churn prediction API with <300ms latency.
*   **Streamlit Dashboard:** Interactive prototype showing model predictions and key metrics.
*   **Documentation Package:** Model cards, API specs, and deployment guide.

## 5. Dataset
**Core Tables:**
*   `customers`: 100,000+ records (IDs, demographics, signup dates, total spend).
*   `orders`: 500,000+ records (transactional data, amount, payment methods).
*   `products`: 5,000+ items (categories, brands).
*   `events`: 2,000,000+ web logs (sessions, clicks, timestamps) - Sampled to 500K for speed.

**Feature Engineering Focus:**
*   RFM (Recency, Frequency, Monetary) metrics.
*   Session-based behavioral features.
*   Purchase patterns and category preferences.

## 6. Technology Stack
| Category | Tools / Services |
| :--- | :--- |
| **Project Management** | Jira, Confluence, GitHub |
| **Cloud / Infrastructure** | AWS S3 (Data Lake), AWS Lambda/EC2 |
| **Data Processing** | Python (Pandas, NumPy), dbt |
| **Machine Learning** | scikit-learn, XGBoost, Random Forest |
| **API Development** | FastAPI, Streamlit |
| **Visualization** | Seaborn, Plotly, Streamlit |
| **Environment** | Local development + Docker containers (Week 1), AWS deployment (Week 2) |

**Model Selection:**
*   **Churn Prediction:** XGBoost/Random Forest (binary classification).
*   **Recommendations:** Collaborative filtering (item-item similarity).

## 7. 2-Week Project Plan

### Team Structure
*   **PM Lead (1):** Overall coordination, stakeholder management.
*   **PMs (~10):** Technical Delivery, Business Delivery, QA & Documentation.
*   **DS Lead (1):** Technical architecture and model strategy.
*   **Data Scientists (~10):** Churn Modeling, Recommendation Engine, Dashboard/Integration.

### Week 1: Foundation & Build

**Days 1-2: Setup & Exploration**
*   **PM:** Define charter/metrics, setup Jira/Confluence, risk register, standups, access credentials.
*   **DS:** Setup env/pipelines, load/validate data, EDA, baseline metrics dashboard.
*   *Key Deliverable:* EDA report with data quality assessment.

**Days 3-5: Feature Engineering & Baseline Models**
*   **PM:** Track features, manage dependencies, document decisions, midweek status.
*   **DS:** Engineer RFM/behavioral features, baseline churn model (Logistic Regression), train/test splits.
*   *Key Deliverable:* Feature dataset ready for modeling; Baseline model metrics.

### Week 2: Build, Deploy & Finalize

**Days 6-8: Model Optimization & API Development**
*   **PM:** Monitor metrics, coordinate API timeline, review docs, prepare demo env.
*   **DS:** Train XGBoost (tuned), build Rec engine, develop FastAPI endpoint, serialize models.
*   *Key Deliverable:* Trained models + functional API endpoint.

**Days 9-10: Dashboard & Integration**
*   **PM:** End-to-end QA, verify metrics, document API, final presentation/demo.
*   **DS:** Build Streamlit dashboard (predictions, recs, feature importance), deploy local Docker, integration test.
*   *Key Deliverable:* Working Streamlit dashboard + locally deployed API.

## 8. PM Governance & Quality Assurance
**PM Sub-Team Structure:**
*   **Team 1 (Technical Delivery):** Local env, tracking, API/Docker support.
*   **Team 2 (Business Delivery):** Stakeholder comms, KPIs, ROI analysis.
*   **Team 3 (QA & Documentation):** Validation, stress testing, documentation, demo prep.

**Daily Syncs:**
*   Morning (15m): DS technical blockers, PM alignment.
*   End-of-Day (10m): Progress vs goals, risk flagging.

## 9. Technical Challenges & Mitigation
| Challenge | 2-Week Solution |
| :--- | :--- |
| Time Constraints | Focus on single high-impact model (churn). |
| AWS Complexity | Use local Docker deployment. |
| Data Volume | Sample events data to 500K records. |
| Class Imbalance | SMOTE or class weighting. |
| Feature Engineering | Limit to RFM + 5-10 behavioral features. |

## 10. Success Metrics
*   **Churn Model:** AUC > 0.75, Balanced F1 > 0.70.
*   **API Performance:** Latency < 300ms.
*   **Dashboard:** Real-time predictions working, functional prototype.

## 11. Deliverables
*   **PM:** Charter, Risk Register, Status Reports, Retrospective, Final Deck, Jira Report.
*   **DS:** Trained models (.pkl), FastAPI code, Streamlit code, Perf report.
*   **Docs:** API specs (Swagger), Model card, Deployment guide.

## 12. Learning Outcomes
*   **PMs:** Agile ML management, risk/scope management, technical coordination.
*   **DS:** Rapid MVP, End-to-end ML workflow, FastAPI/Streamlit, time-constrained optimization.

## 14. Assessment & Evaluation
*   **Technical:** Model performance (holdout), API stress test, Dashboard usability.
*   **Business:** Objective alignment, ROI projection.
*   **Process:** Retrospective, Velocity, Documentation quality.
