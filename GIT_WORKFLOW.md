# Repository Collaboration & Git Workflow

## ShopFlow 2-Week Sprint

> **Repository:** https://github.com/datascience-muhammad/Shopflow_london

---

## Branch Structure

```
main  (LOCKED — production-ready, PM Lead merges only)
  │
  └── dev  (integration testing — PM Team 1 coordinates)
       │
       ├── team/ds-churn              (DS Team 1 shared workspace)
       │    ├── feature/baseline-model
       │    └── feature/feature-engineering
       │
       ├── team/ds-recommendation     (DS Team 2 shared workspace)
       │    ├── feature/collab-filtering
       │    └── feature/api-development
       │
       └── team/ds-dashboard-mlops   (DS Team 3 shared workspace)
            ├── feature/mock-api
            └── feature/streamlit-dashboard
```

| Branch         | Pattern           | Who Uses                            | Lifetime    |
| -------------- | ----------------- | ----------------------------------- | ----------- |
| `main`         | `main`            | No direct pushes                    | Permanent   |
| `dev`          | `dev`             | PM Team 1 merges team branches here | Permanent   |
| Team Branch    | `team/ds-*`       | Entire DS team                      | Full sprint |
| Feature Branch | `feature/my-task` | Individual member                   | 1–3 days    |

---

## Step-by-Step Workflow

### 1. Create Your Feature Branch

```bash
# Switch to your team branch and pull latest
git checkout team/ds-churn          # replace with your team branch
git pull origin team/ds-churn

# Create your feature branch
git checkout -b feature/baseline-model

# Confirm
git branch
```

### 2. Do Your Work & Commit Often

Work **only inside your team folder:**

- DS Team 1 → `data_science/team1_churn/`
- DS Team 2 → `data_science/team2_recommendation/`
- DS Team 3 → `data_science/team3_dashboard_mlops/`

```bash
git add data_science/team1_churn/model.py
git commit -m "feat: add xgboost baseline model"
```

**Commit message format:**

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation

### 3. Push Feature Branch

```bash
git push origin feature/baseline-model
```

### 4. Create a Pull Request on GitHub

1. Go to https://github.com/datascience-muhammad/Shopflow_london/pulls
2. Click **New Pull Request**
3. ⚠️ Set **base** to your **team branch** (e.g. `team/ds-churn`), NOT `main`
4. Set **compare** to your feature branch
5. Assign your **team lead** as reviewer
6. Create PR

### 5. Team Lead Reviews & Merges

Team lead reviews, approves, and merges using **"Squash and merge"**.  
The feature branch can then be deleted.

---

## Cross-Team Milestones

### Day 5 — Feature Store Delivery (Teams 1 & 2)

1. Branch from team branch → add feature tables to `data_science/feature_store/`
2. Update `feature_store/README.md` with schema
3. **Coordinate on WhatsApp before updating the README** (one team at a time)
4. PR → team branch → team lead merges

### Day 8 — API Integration (Teams 1, 2 → Team 3)

1. Teams 1 & 2 confirm Render URLs are live → post to WhatsApp DS sub-group
2. Team 3 creates `feature/live-api-integration` branch
3. Updates `.env` with live URLs
4. PR → `team/ds-dashboard-mlops` → team lead merges

---

## Promoting Branches (PM Team 1 Coordinates)

**Team branch → `dev`** (after Day 5, 7, 9 milestones):

1. PM Team 1 confirms milestone complete with DS leads
2. PM Team 1 creates PR: `team/ds-*` → `dev`
3. DS Lead reviews & approves
4. PM Team 1 merges

**`dev` → `main`** (Day 10, after demo rehearsal):

1. PM Team 3 issues go/no-go
2. PM Lead creates PR: `dev` → `main`
3. DS Lead final review & approval
4. PM Lead merges

---

## Folder Ownership

| Team      | Owned Folder                          | Shared (coordinate first)                                |
| --------- | ------------------------------------- | -------------------------------------------------------- |
| DS Team 1 | `data_science/team1_churn/`           | `data_science/feature_store/`, `data_science/contracts/` |
| DS Team 2 | `data_science/team2_recommendation/`  | `data_science/feature_store/`, `data_science/contracts/` |
| DS Team 3 | `data_science/team3_dashboard_mlops/` | `data_science/contracts/`                                |

---

## Common Commands Reference

| Task                  | Command                             |
| --------------------- | ----------------------------------- |
| See current branch    | `git branch`                        |
| Switch to team branch | `git checkout team/ds-churn`        |
| Pull latest           | `git pull origin team/ds-churn`     |
| Create feature branch | `git checkout -b feature/my-task`   |
| Stage changes         | `git add .`                         |
| Commit                | `git commit -m "feat: description"` |
| Push branch           | `git push origin feature/my-task`   |
| Delete local branch   | `git branch -d feature/my-task`     |

---

## Decision Authority

| Decision                    | Who Decides         |
| --------------------------- | ------------------- |
| Task assignment within team | DS Team Lead        |
| Merge feature → team branch | DS Team Lead        |
| Promote team branch → `dev` | PM Team 1 + DS Lead |
| Merge `dev` → `main`        | PM Lead + DS Lead   |

---

## Troubleshooting

### Committed to wrong branch (not pushed yet)

```bash
git reset --soft HEAD~1     # undo last commit, keep changes
git checkout correct-branch
git add . && git commit -m "feat: description"
```

### Merge conflict

```bash
git pull origin team/ds-churn   # pull latest
# Open conflicting files, look for <<<<<<< markers, resolve
git add . && git commit -m "fix: resolve merge conflict"
```

### Accidentally worked on main (stop — do NOT push)

```bash
git checkout -b feature/my-work   # your changes move here
git checkout main
git pull origin main              # restore clean main
# Continue from feature branch
```

---

_Clear Jupyter outputs before committing: `jupyter nbconvert --clear-output --inplace notebook.ipynb`_  
_Do not commit CSV/pkl files > 100MB — upload to S3 and reference the path._
