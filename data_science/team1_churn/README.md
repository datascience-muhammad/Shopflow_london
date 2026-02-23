# DS Team 1 — Churn Prediction

## Overview

This folder belongs to **DS Team 1**. We are responsible for building the customer churn prediction model and its FastAPI endpoint.

## Folder Structure

```
team1_churn/
├── README.md              # This file
├── notebooks/             # EDA and experimentation notebooks (clear outputs before committing)
├── src/                   # Source code
│   ├── preprocessing.py   # Feature engineering and preprocessing
│   ├── model.py           # Model training and evaluation
│   └── api.py             # FastAPI endpoint
├── tests/                 # Unit tests
└── requirements.txt       # Python dependencies
```

## Team Members & Task Assignments

> Team Lead: Update this section with member assignments.

| Member | Branch                        | Task                         |
| ------ | ----------------------------- | ---------------------------- |
| TBD    | `feature/feature-engineering` | Feature engineering pipeline |
| TBD    | `feature/baseline-model`      | XGBoost baseline model       |

## Sprint Milestones

- **Day 5:** Feature tables committed to `data_science/feature_store/`
- **Day 8:** FastAPI endpoint deployed to Render, URL posted to DS sub-group
- **Day 9:** Team branch ready for promotion to `dev`

## How to Work in This Folder

1. Always branch from `team/ds-churn` — never from `main` or `dev`
2. Work only in `data_science/team1_churn/` (and `data_science/feature_store/` on Day 5)
3. Follow commit message conventions: `feat:`, `fix:`, `docs:`
4. Clear Jupyter notebook outputs before committing

## Deliverables

- [ ] Feature engineering pipeline
- [ ] Trained XGBoost churn model (no `.pkl` files > 100MB — use S3)
- [ ] FastAPI endpoint with `/predict` route
- [ ] Feature table in `data_science/feature_store/`
- [ ] API contract updated in `data_science/contracts/`
