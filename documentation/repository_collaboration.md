# Repository Collaboration & Git Workflow

This document outlines the engineering workflow for the ShopFlow 2-week sprint. It ensures Project Managers and Data Science teams can collaborate without conflicts.

## 1. Branching Strategy

We use a simplified tiered branching model to ensure stability while allowing parallel development.

| Branch Type      | Pattern               | Description                                                    |
| :--------------- | :-------------------- | :------------------------------------------------------------- |
| **Main**         | `main`                | Production-ready code. Deployed to final environment. Locked.  |
| **Development**  | `dev`                 | Integration testing branch. All team branches merge here.      |
| **Team/Feature** | `team/<team-name>`    | Shared workspace for sub-teams (e.g., `team/ds-churn`).        |
| **Feature**      | `feature/<task-name>` | Individual work branch. Short-lived. Created from Team branch. |

## 2. Detailed Workflow Steps

### Step 1: Start a New Task

Always start from your **Team Branch**, not main or dev.

```bash
# 1. Checkout your team branch and pull latest changes
git checkout team/ds-churn
git pull origin team/ds-churn

# 2. Create a feature branch
git checkout -b feature/model-training-v1
```

### Step 2: Development & Commits

- **Data Science Churn Team:** `data_science/team1_churn/`
- **Data Science Recommendations Team:** `data_science/team2_recommendation/`
- **Dashboard Team:** `data_science/team3_dashboard_mlops/`
- **Common Data Processing:** `data_engineering/`

**Commit Message Format:** `<type>: <description>`

- `feat: add xgboost baseline model`
- `fix: resolve missing values in rfm features`
- `docs: update API latency requirements`

### Step 3: Pull Request (PR)

1.  Push your feature branch: `git push origin feature/model-training-v1`.
2.  Open a Pull Request on GitHub.
3.  **Important:** Set the **Base Branch** to your **Team Branch** (e.g., `team/ds-churn`), NOT `main`.
4.  Assign a reviewer from your sub-team (DS Lead check required for model changes).

### Step 4: Review & Merge

- **Reviewers:** Check for code quality, logic errors, and folder isolation.
- **Approvals:** At least 1 approval required.
- **Merge:** Squash and merge is recommended to keep history clean.

### Step 5: Promotion to Dev & Main

- **PM Technical Delivery:** Periodically merge `team/*` branches into `dev` for integration testing.
- **End of Sprint:** If `dev` passes all tests, it is merged into `main` for final demo.

## 3. Best Practices

- **Notebooks:** Clear outputs before committing `.ipynb` files to reduce bloat.
- **Large Files:** Do not commit CSVs or models larger than 100MB. Use S3 or included `.gitignore`.
- **Sync:** Pull from upstream `dev` frequently to avoid large merge conflicts later.
