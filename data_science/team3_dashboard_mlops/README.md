# DS Team 3 — Dashboard & MLOps

## Overview

This folder belongs to **DS Team 3**. We are responsible for the Streamlit dashboard, mock API (for development before real APIs are live), and MLOps setup.

## Folder Structure

```
team3_dashboard_mlops/
├── README.md              # This file
├── mock_api/              # Mock FastAPI server (mirrors Team 1 & 2 contracts)
│   └── main.py            # Mock endpoints for dashboard development
├── dashboard/             # Streamlit dashboard app
│   ├── app.py             # Main Streamlit app
│   └── components/        # Reusable UI components
├── mlops/                 # MLOps configuration (MLflow, monitoring)
├── tests/                 # Unit tests
├── .env                   # Local env vars — DO NOT COMMIT (use sample.env)
└── requirements.txt       # Python dependencies
```

## Team Members & Task Assignments

> Team Lead: Update this section with member assignments.

| Member | Branch                        | Task                 |
| ------ | ----------------------------- | -------------------- |
| TBD    | `feature/mock-api`            | Mock API development |
| TBD    | `feature/streamlit-dashboard` | Streamlit dashboard  |

## Sprint Milestones

- **Day 1–7:** Use mock API for dashboard development (no waiting on Teams 1 & 2)
- **Day 8:** Switch `.env` to live Render URLs from Teams 1 & 2 (post URLs in WhatsApp DS sub-group)
- **Day 9:** Dashboard fully integrated with live APIs; team branch ready for `dev`

## How to Work in This Folder

1. Always branch from `team/ds-dashboard-mlops` — never from `main` or `dev`
2. Work only in `data_science/team3_dashboard_mlops/`
3. **Never commit `.env`** — update `sample.env` instead if adding new variables
4. Follow commit message conventions: `feat:`, `fix:`, `docs:`
5. Clear Jupyter notebook outputs before committing

## Day 8 — Switching to Live APIs

When Teams 1 & 2 post their Render URLs to the WhatsApp DS sub-group:

1. Create a feature branch: `git checkout -b feature/live-api-integration`
2. Update `.env` with the live Render URLs
3. Test dashboard against live APIs
4. Create PR to `team/ds-dashboard-mlops`
5. Team lead reviews and merges

## Deliverables

- [ ] Mock API server mirroring contracts in `data_science/contracts/`
- [ ] Streamlit dashboard (churn predictions + recommendations)
- [ ] MLflow experiment tracking setup
- [ ] `.env` updated with live Render URLs by Day 8
- [ ] All dashboard pages functional with live data by Day 9
