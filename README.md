# ShopFlow: Customer Intelligence Platform

**ShopFlow by PrimeCart Inc.** is a retail technology initiative to build a predictive analytics engine for churn prediction and product recommendations.

## 📚 Project Documentation & Coordination

This project follows a strict coordination strategy between Data Science (DS) and Product Management (PM) teams.

- **[DS Coordination & Implementation Guide](documentation/ds_coordination_guide.md)**: The primary source of truth for team responsibilities, API contracts, folder structure, and the 2-week sprint plan. **Start here.**
- **[Project Reference Guide](documentation/project_reference_guide.md)**: High-level overview of business challenges, objectives, and success metrics.
- **[PM Coordination Guide](documentation/pm_coordination_guide.md)**: Product management workflows and coordination.
- **[Repository Collaboration](documentation/repository_collaboration.md)**: Git workflow, branching strategy, and PR guidelines.
- **[Team Responsibilities](documentation/team_responsibilities.md)**: Detailed breakdown of roles for DS and PM members.

## 🗂 Project Structure

The repository is organized to support parallel workstreams for Churn, Recommendations, and Dashboard/MLOps teams, with specific shared contracts.

```
customer-intelligence-platform/
├── .github/                        # CI/CD workflows
├── assets/                         # Project assets (images, logos)
├── data_science/                   # Main DS workstreams
│   ├── contracts/                  # API contracts & schema definitions (Shared)
│   ├── feature_store/              # Shared feature store (Parquet files & Schema)
│   ├── team1_churn/                # DS Team 1: Churn Prediction Model & API
│   ├── team2_recommendation/       # DS Team 2: Recommendation Engine & API
│   └── team3_dashboard_mlops/      # DS Team 3: Streamlit Dashboard & MLOps
│       └── mock_api/               # Mock server for frontend development
├── documentation/                  # Project documentation & guides
├── .gitignore                      # Git ignore file (excludes datasets)
└── README.md                       # This file
```

## 🚀 Key Deliverables

1.  **Churn Prediction Model**: XGBoost/Random Forest model to predict customer churn risk.
2.  **Recommendation Engine**: Collaborative filtering system for personalized product suggestions.
3.  **Streamlit Dashboard**: Interactive dashboard visualizing predictions and recommendations.
4.  **API Endpoints**: FastAPI implementations for both models (`/predict/churn` and `/recommend/{id}`).

## 🛠 Setup & Installation

Please refer to the **[DS Coordination Guide](documentation/ds_coordination_guide.md)** for detailed setup instructions, including:

- Environment setup
- MLflow configuration
- API development
- Feature store usage

## 📦 Data & Feature Store

Large datasets and feature store files (`*.parquet`) are excluded from the repository.

- **Feature Store Location**: `data_science/feature_store/`
- **S3 Integration**: Files larger than 100MB are stored in S3, with references committed to the repo.

## 🤝 Collaboration

- **Contracts**: API contracts in `data_science/contracts/` are the single source of truth for integration.
- **Feature Store**: All features must be documented in `data_science/feature_store/README.md`.
- **Branching**: Follow the strategy outlined in `documentation/repository_collaboration.md`.

---

**ShopFlow - PrimeCart Inc.**
