# DS Team 2 — Recommendation Engine

## Overview

This folder belongs to **DS Team 2**. We are responsible for building the product recommendation engine and its FastAPI endpoint.

## Folder Structure

```
team2_recommendation/
├── README.md              # This file
├── notebooks/             # EDA and experimentation notebooks (clear outputs before committing)
├── src/                   # Source code
│   ├── preprocessing.py   # Data preprocessing and feature extraction
│   ├── model.py           # Collaborative filtering model
│   └── api.py             # FastAPI endpoint
├── tests/                 # Unit tests
└── requirements.txt       # Python dependencies
```

## Team Members & Task Assignments

> Team Lead: Update this section with member assignments.

| Member | Branch                     | Task                          |
| ------ | -------------------------- | ----------------------------- |
| TBD    | `feature/collab-filtering` | Collaborative filtering model |
| TBD    | `feature/api-development`  | FastAPI endpoint development  |

## Sprint Milestones

- **Day 5:** Feature tables committed to `data_science/feature_store/`
- **Day 8:** FastAPI endpoint deployed to Render, URL posted to DS sub-group
- **Day 9:** Team branch ready for promotion to `dev`

## How to Work in This Folder

1. Always branch from `team/ds-recommendation` — never from `main` or `dev`
2. Work only in `data_science/team2_recommendation/` (and `data_science/feature_store/` on Day 5)
3. Follow commit message conventions: `feat:`, `fix:`, `docs:`
4. Clear Jupyter notebook outputs before committing

## Deliverables

- [ ] Collaborative filtering recommendation engine
- [ ] FastAPI endpoint with `/recommend` route
- [ ] Feature table in `data_science/feature_store/`
- [ ] API contract updated in `data_science/contracts/`
