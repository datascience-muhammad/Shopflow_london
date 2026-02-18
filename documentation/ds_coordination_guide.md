# Data Science Coordination & Implementation Guide

**ShopFlow Customer Intelligence Platform — 2-Week Sprint**  
**Project:** ShopFlow by PrimeCart Inc.  
**Audience:**

- DS Team 1 (Churn Prediction)
- DS Team 2 (Recommendations)
- DS Team 3 (Dashboard & MLOps)  
  **Repository Path:** `documentation/ds_coordination_guide.md`

---

## Before You Start: Understanding How the Three Teams Connect

There are three DS teams working in parallel on this sprint, and each team's output feeds into the next. Understanding this flow before Day 1 is essential — it explains every coordination decision in this guide.

- **DS Team 1** builds the churn prediction model and exposes it as a local API endpoint.
- **DS Team 2** builds the recommendation engine and exposes it as a local API endpoint.
- **DS Team 3** consumes both endpoints to power the Streamlit dashboard, and also owns the shared MLOps infrastructure that all three teams use from Day 1 onwards.

The critical dependency is this: **Team 3 cannot build a real dashboard without working endpoints from Teams 1 and 2.** In a 2-week sprint, waiting for those endpoints before starting would leave Team 3 idle for most of Week 1. This guide solves that problem through a contract-first approach — described in full below — and defines the exact steps and handoffs across the 10-day sprint.

---

## Part 1: Team Responsibilities at a Glance

| Team          | Core Deliverable                                  | Shared Output                             |
| :------------ | :------------------------------------------------ | :---------------------------------------- |
| **DS Team 1** | Churn prediction model + FastAPI endpoint         | `churn_features.parquet` in feature store |
| **DS Team 2** | Recommendation engine + FastAPI endpoint          | `rec_features.parquet` in feature store   |
| **DS Team 3** | Streamlit dashboard + MLOps infrastructure        | Shared MLflow server + Model Registry     |
| **DS Lead**   | Technical oversight, code reviews, model sign-off | Final Production approval in MLflow       |

Each team works within their own folder in the repository (`data_science/team1_churn/`, `data_science/team2_recommendation/`, `data_science/team3_dashboard_mlops/`).
The only shared folders that multiple teams write to are `data_science/contracts/` and `data_science/feature_store/` — both explained in detail below.

---

## Part 2: The Contract-First Approach

### What Is a Contract and Why Does It Matter?

An API contract is a written specification that defines exactly what an endpoint will return. It is agreed by all three teams **before any development begins**, and once committed to the repository it is treated as frozen.

The reason this matters: once Team 3 knows exactly what the churn API and recommendation API will return, they can build the entire dashboard immediately — against a mock server that mimics those responses. When the real endpoints are ready in Week 2, Team 3 makes a single configuration change and the dashboard switches to live data. No rework required.

### Step 1 — Contract Session (Days 1–2, All Teams)

All three DS teams and the DS Lead meet to agree on the following three contracts. The output of this session is a set of files committed to `data_science/contracts/`. Nothing in these contracts changes after Day 2 without DS Lead approval.

#### Contract 1: Churn Prediction Endpoint

**Ownership:** DS Team 1

```
Endpoint:   POST /predict/churn
Port:       8001 (local)

Request:    customer_id, plus engineered features (recency, frequency,
            monetary, tenure, and behavioural signals)

Response:
  customer_id         string
  churn_probability   float    (0.0 – 1.0)
  churn_prediction    string   ("high_risk" or "low_risk")
  confidence          float    (0.0 – 1.0)
  model_version       string
  timestamp           string   (ISO 8601)
```

#### Contract 2: Recommendation Endpoint

**Ownership:** DS Team 2

```
Endpoint:   GET /recommend/{customer_id}?n=5
Port:       8002 (local)

Response:
  customer_id       string
  recommendations   list of up to 5 items, each containing:
    product_id        string
    product_name      string
    category          string
    predicted_score   float   (0.0 – 1.0)
  model_version     string
  timestamp         string   (ISO 8601)
```

#### Contract 3: Feature Store Schema

**Ownership:** DS Teams 1 and 2 (DS Team 3 reads)

```
Location:   data_science/feature_store/

Files:
  churn_features.parquet    (DS Team 1 — RFM and behavioural features)
  rec_features.parquet      (DS Team 2 — customer-product interaction data)

Requirement: Both files must include customer_id as the primary key.
Schema documentation is mandatory in feature_store/README.md.
```

### Step 2 — DS Team 3 Builds the Mock Server (Days 2–3)

Immediately after the contract session, DS Team 3 creates a local mock server at `data_science/team3_dashboard_mlops/mock_api/`. This mock server returns hardcoded sample responses that conform exactly to the two endpoint contracts above.

The Streamlit dashboard is configured to point to this mock server from the start. This allows Team 3 to build, test, and refine the full dashboard — all panels, visualisations, and interactions — without waiting for the real models to be trained.

The entire mock-to-live switch is handled by two lines in the `.env` file:

```bash
# .env — Team 3 updates these on Day 8 when real endpoints are confirmed
CHURN_API_URL=http://localhost:8001
REC_API_URL=http://localhost:8002
```

No dashboard code changes. No rework. The switch is validated in Postman before it is made.

---

## Part 3: Shared MLOps Infrastructure

### Why Team 3 Sets This Up Before the Dashboard

DS Team 3 owns the shared MLflow tracking infrastructure. This is the **first task Team 3 completes** — before any dashboard work — because DS Teams 1 and 2 need it running from Day 3 to log their experiments. A late MLflow setup means fragmented experiment history across three teams, which defeats the purpose of having a shared registry.

The MLflow server is hosted on **Dagshub** (a free cloud service built for ML experiment tracking). All three teams connect to the same tracking URL. No local Docker setup required.

### MLflow Setup Instructions (DS Team 3 — Day 2)

**Step 1: Create a Dagshub Account and Project**

1. Go to https://dagshub.com and sign up (free account, no credit card)
2. Click "New Repository"
3. Name it: `shopflow-mlflow`
4. Make it **Private** (only your team can access)
5. Click "Create Repository"

**Step 2: Get the MLflow Tracking URL**

1. Once the repository is created, click on the "Remote" tab in the left sidebar
2. You will see your MLflow tracking URL. It looks like:
   `https://dagshub.com/<your-username>/shopflow-mlflow.mlflow`
3. Copy this URL — you will share it with Teams 1 and 2

**Step 3: Generate Access Token**

1. Click on your profile icon (top right) → Settings
2. Go to "Access Tokens" in the left menu
3. Click "New Token"
4. Name it: `ShopFlow Sprint`
5. Copy the token immediately (you won't see it again)

**Step 4: Share Credentials with Teams 1 and 2**
Post the following in the WhatsApp DS sub-group:

> **MLflow Tracking Server is live:**
> Tracking URL: `https://dagshub.com/<your-username>/shopflow-mlflow.mlflow`
> Username: `<your-dagshub-username>`
> Token: `<paste-the-token-here>`
>
> **Add this to your code before logging experiments:**
>
> ```python
> import os
> os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/<your-username>/shopflow-mlflow.mlflow'
> os.environ['MLFLOW_TRACKING_USERNAME'] = '<your-dagshub-username>'
> os.environ['MLFLOW_TRACKING_PASSWORD'] = '<your-token>'
> ```
>
> Teams 1 and 2: Confirm you can connect by running a test experiment.

**Step 5: Test the Connection**
Run this code to confirm it works:

```python
import mlflow
import os

# Set credentials
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/<your-username>/shopflow-mlflow.mlflow'
os.environ['MLFLOW_TRACKING_USERNAME'] = '<your-dagshub-username>'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '<your-token>'

# Start a test experiment
mlflow.set_experiment("test-connection")
with mlflow.start_run():
    mlflow.log_param("test", "success")
    mlflow.log_metric("test_metric", 1.0)

print("MLflow connection successful! Check Dagshub to see your run.")
```

If this runs without errors, the server is live.
Go to your Dagshub repository in the browser and click "Experiments" to see the logged run.

**Step 6: Confirm All Teams Can Connect (Day 3 Morning Standup)**
At the Day 3 standup, confirm that:

- [ ] DS Team 1 has run the test code and can see their run in Dagshub
- [ ] DS Team 2 has run the test code and can see their run in Dagshub
- [ ] DS Team 3 can see all runs from all teams in the Dagshub UI

Once confirmed, mark the Jira milestone "MLflow server live" as complete.

### MLflow Responsibilities by Team

**DS Team 3 — sets up and maintains:**

- The Dagshub MLflow project and access credentials
- The Model Registry structure, including staging and production stages
- Version tagging and metadata for all registered models
- Monitoring the Dagshub UI to ensure all teams are logging correctly

**DS Teams 1 and 2 — log to the shared server for every training run:**

- All hyperparameters used in that run
- Performance metrics: AUC, F1, Precision, Recall, and training time
- The trained model artifact (`.pkl` file)
- The complete list of features used

**DS Lead — final approval:**

- Reviews the Model Registry in Dagshub before any model is promoted from Staging to Production
- Production status is the gate that confirms a model is ready for the dashboard and the demo

**Important:** Do not create a local or isolated MLflow tracking instance. All experiment logging goes to the shared Dagshub server. Running separate trackers makes cross-team comparison impossible and fragments your experiment history.

### How to Log Experiments (All DS Teams)

Every time you train a model, wrap it in MLflow tracking:

```python
import mlflow
import os

# Set credentials (do this once at the top of your script)
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/<your-username>/shopflow-mlflow.mlflow'
os.environ['MLFLOW_TRACKING_USERNAME'] = '<your-dagshub-username>'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '<your-token>'

# Set your experiment name (use your team name)
mlflow.set_experiment("churn-prediction")  # Team 1
# mlflow.set_experiment("recommendation-engine")  # Team 2

# Start a run
with mlflow.start_run(run_name="xgboost-baseline"):
    # Log hyperparameters
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("learning_rate", 0.1)
    mlflow.log_param("n_estimators", 100)

    # Train your model
    model = XGBClassifier(max_depth=5, learning_rate=0.1, n_estimators=100)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    auc = roc_auc_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Log metrics
    mlflow.log_metric("auc", auc)
    mlflow.log_metric("f1", f1)

    # Log the model
    mlflow.sklearn.log_model(model, "model")
    print(f"Run logged: AUC={auc}, F1={f1}")
```

Every run appears in Dagshub immediately. Go to your Dagshub repository → Experiments tab to see all runs from all teams.

### Model Registry: The Promotion Path

Each model follows a defined progression through the registry:

```
Training runs logged  →  Best run identified  →  Promoted to Staging
        →  DS Lead review  →  Promoted to Production  →  Dashboard consumes
```

**How to promote a model to Staging (DS Teams 1 and 2):**

1. Go to your Dagshub repository → Experiments tab
2. Find your best run (highest AUC, best F1)
3. Click on the run
4. In the "Artifacts" section, click on the model folder
5. Click "Register Model"
6. Model name: `churn-model` (Team 1) or `recommendation-model` (Team 2)
7. Stage: Select "Staging"
8. Click "Register"
9. Notify DS Lead in the WhatsApp DS sub-group that your model is in Staging and ready for review.

**How DS Lead promotes to Production:**

1. DS Lead reviews the model in Dagshub (checks metrics, features used, training parameters)
2. If approved, DS Lead clicks "Transition to Production" in the Dagshub UI
3. DS Lead notifies DS Team 3 that the Production model is ready
4. DS Team 3 connects the dashboard to the Production model

Teams 1 and 2 are responsible for identifying their best run and promoting it to Staging. DS Lead reviews and approves the move to Production. Team 3 connects the dashboard to the Production model.

### Dagshub Resources

- **Documentation:** [Getting started](https://dagshub.com/docs/) | [MLflow integration](https://dagshub.com/docs/integration_guide/mlflow_tracking/)
- **Video Tutorial:** [MLflow on Dagshub (5 min)](https://www.youtube.com/watch?v=19OvF9K6_BI)
- **Support:** If you encounter issues, check the Dagshub Docs or raise it in the WhatsApp DS sub-group.

---

## Part 3.5: API Deployment (DS Teams 1 and 2)

### The Problem

Your FastAPI runs on `localhost:8001/8002`. Team 3's Streamlit dashboard cannot connect to localhost on your machine. You need a public URL.

### The Solution

- **Week 1 (Days 1-7): ngrok for testing** — temporary URLs, instant setup
- **Week 2 (Days 8-10): Render for demo** — permanent URLs, stable deployment

### Setup 1: ngrok (Week 1 Testing)

**Step 1: Install ngrok**
Download from https://ngrok.com/download or `sudo snap install ngrok`

**Step 2: Run your FastAPI**

```bash
cd data_science/team1_churn  # or team2_recommendation
uvicorn main:app --reload --port 8001  # Team 1: 8001, Team 2: 8002
```

**Step 3: Expose it**
New terminal:

```bash
ngrok http 8001  # Team 1 uses 8001, Team 2 uses 8002
```

Output shows:
`Forwarding  https://abc123.ngrok-free.app -> http://localhost:8001`

**Step 4: Share with Team 3**
Post in WhatsApp DS sub-group:

> Team 1 Churn API: `https://abc123.ngrok-free.app/predict/churn`
> Test: `https://abc123.ngrok-free.app/docs`

Team 3 updates `.env`:
`CHURN_API_URL=https://abc123.ngrok-free.app`

_Note: ngrok URL changes each restart. Keep ngrok running while Team 3 tests._
[Video: ngrok quickstart (3 min)](https://www.youtube.com/watch?v=6K9gASLnSN4)

### Setup 2: Render (Week 2 Final Deployment)

**Step 1: Push code to GitHub**

```bash
git add .
git commit -m "Final API ready"
git push origin team/ds-churn  # or team/ds-recommendation
```

**Step 2: Create Render account**
Sign up at https://render.com with GitHub (free, no card needed)

**Step 3: Deploy**

1. Click "New +" → "Web Service"
2. Connect GitHub repo: `shopflow-project`
3. Configure:
   - **Name:** `churn-api` (Team 1) or `rec-api` (Team 2)
   - **Branch:** `team/ds-churn` (or `team/ds-recommendation`)
   - **Root Directory:** `data_science/team1_churn` (or `team2_recommendation`)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Click "Create Web Service"
5. Wait 2-3 minutes for deployment.

**Step 4: Test**
Go to `https://churn-api.onrender.com/docs` — you should see FastAPI Swagger UI.

**Step 5: Share with Team 3**

> Team 1 Churn API deployed: `https://churn-api.onrender.com/predict/churn`
> Docs: `https://churn-api.onrender.com/docs`
> URL is permanent.

Team 3 updates `.env`:
`CHURN_API_URL=https://churn-api.onrender.com`

_Note: Free tier spins down after 15 min idle. First request takes ~30 sec to wake. This is normal._
[Video: FastAPI on Render (8 min)](https://www.youtube.com/watch?v=6K-UT8mD58g)

### Requirements File

Before deploying to Render, add `requirements.txt` to your team folder:

```
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
xgboost==2.0.2
pandas==2.1.3
numpy==1.26.2
pydantic==2.5.0
```

Or generate automatically: `pip freeze > requirements.txt`
Commit and push before deploying.

### Timeline

| Day      | Teams 1 & 2                                          | Team 3                                 | Method     |
| :------- | :--------------------------------------------------- | :------------------------------------- | :--------- |
| **1-7**  | Develop locally, expose with ngrok when Team 3 needs | Build on mock, test real API via ngrok | **ngrok**  |
| **8**    | Deploy to Render, share URL                          | Update `.env`, integration test        | **Render** |
| **9-10** | Monitor Render                                       | Dashboard live on Render APIs          | **Render** |

### Troubleshooting

- **ngrok rate limit:** Wait 1 hour or restart session
- **Render build failed:** Check `requirements.txt` exists, start command is exact: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Render slow wake:** Expected on free tier after 15 min idle

---

## Part 4: Feature Store

When DS Teams 1 and 2 complete feature engineering (Days 4–5), they commit their feature tables to the shared feature store. DS Team 3 uses these tables for dashboard visualisations.

### Repository Structure

```
data_science/
└── feature_store/
    ├── README.md                 ← mandatory schema documentation
    ├── churn_features.parquet    ← committed by DS Team 1
    └── rec_features.parquet      ← committed by DS Team 2
```

### Rules for the Feature Store

- All files must use `customer_id` as the primary key so Team 3 can join datasets
- `feature_store/README.md` must be updated with every column name and a plain-English description for each feature added — this is a required deliverable, not optional documentation
- Files larger than 100MB must be stored in S3. Commit only the S3 reference path to the repository
- Pull from `dev` before committing anything to the feature store to avoid conflicts

---

## Part 5: Day-by-Day Sprint Plan

| Day    | DS Team 1 — Churn                                                        | DS Team 2 — Recommendations                                            | DS Team 3 — Dashboard & MLOps                                                             |
| :----- | :----------------------------------------------------------------------- | :--------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| **1**  | Contract session (all teams)                                             | Contract session (all teams)                                           | Contract session + begin MLflow DagsHub setup                                             |
| **2**  | EDA on `customers`, `orders`, `events`                                   | EDA on `products`, `orders`, `events`                                  | ✅ **MLflow server live** — confirm Teams 1 & 2 can connect. Mock API development begins. |
| **3**  | Feature engineering: RFM + behavioural features                          | Feature engineering: customer-product interaction matrix               | MLflow confirmed by all teams. Dashboard skeleton built and wired to mock API.            |
| **4**  | Baseline model training — log all runs to shared MLflow                  | Baseline collaborative filtering — log all runs to shared MLflow       | Dashboard panels consuming mock API responses. Model Registry structure configured.       |
| **5**  | ✅ **Commit `churn_features.parquet` to feature store with schema docs** | ✅ **Commit `rec_features.parquet` to feature store with schema docs** | Pull feature store data for dashboard visualisations.                                     |
| **6**  | XGBoost hyperparameter tuning — multiple runs logged                     | Collaborative filtering tuning — multiple runs logged                  | Dashboard near-complete on mocks. Integration test environment prepared.                  |
| **7**  | ✅ **Promote best churn model to MLflow Staging**                        | ✅ **Promote best rec model to MLflow Staging**                        | Validate Staging models against contracts. DS Lead review.                                |
| **8**  | ✅ **FastAPI churn endpoint live locally on port 8001**                  | ✅ **FastAPI rec endpoint live locally on port 8002**                  | Validate both endpoints in Postman. Update `.env`. Full dashboard integration test.       |
| **9**  | End-to-end testing. Promote churn model to Production.                   | End-to-end testing. Promote rec model to Production.                   | Dashboard fully live on real APIs. Final polish. PM Team 3 QA begins.                     |
| **10** | Demo readiness check                                                     | Demo readiness check                                                   | Demo readiness check                                                                      |

**Bold entries indicate cross-team handoff points. These are sprint milestones and must be communicated to the PM Lead when complete.**

---

## Part 6: GitHub Collaboration for Shared Resources

The full branching strategy and PR workflow is in `repository_collaboration.md`. The rules below apply specifically to the two shared directories that multiple teams write to.

### Shared Directories: `contracts/` and `feature_store/`

These are the only directories where more than one team commits files. Follow these rules strictly:

1. Always pull from `dev` before writing to either shared directory
2. Force pushes to these directories are not permitted
3. If two teams need to update `feature_store/README.md` at the same time, coordinate the timing in the **WhatsApp DS sub-group** and commit sequentially — do not attempt parallel edits

### Endpoint Handoff Protocol

When DS Team 1 or DS Team 2 has a working endpoint ready, they follow this exact process:

1. Test the endpoint locally in Postman and confirm it matches the contract
2. Message DS Team 3 in the **WhatsApp DS sub-group** with the port number and a link to the PR
3. DS Team 3 independently validates the endpoint in Postman before updating `.env`
4. Confirmation is posted in the **WhatsApp general group** and noted at the next standup

The `.env` switch is not made until DS Team 3 has independently confirmed the endpoint is contract-compliant.

### DS Lead Review Checkpoints

The DS Lead conducts formal reviews at two points:

- **End of Day 5** — reviews feature engineering outputs from Teams 1 and 2 before they are committed to the feature store
- **Day 9** — reviews all three team branches before final merge into `dev` for sprint integration

---

## Part 7: Definition of Done

### DS Team 1 — Churn Prediction

- [ ] Churn model registered in MLflow at **Production** status, with version tag, training date, feature list, and performance metrics documented
- [ ] `POST /predict/churn` endpoint returning valid JSON responses within 300ms
- [ ] `churn_features.parquet` committed to feature store with fully documented schema in `README.md`
- [ ] All code reviewed and merged into `team/ds-churn`

### DS Team 2 — Recommendations

- [ ] Recommendation model registered in MLflow at **Production** status, with version tag, training date, feature list, and performance metrics documented
- [ ] `GET /recommend/{id}` endpoint returning valid top-5 JSON responses within 300ms
- [ ] `rec_features.parquet` committed to feature store with fully documented schema in `README.md`
- [ ] All code reviewed and merged into `team/ds-recommendation`

### DS Team 3 — Dashboard & MLOps

- [ ] Streamlit dashboard tested against both the mock API and the live APIs — not just one
- [ ] MLflow tracking server running in Docker and confirmed accessible to all teams
- [ ] Model Registry populated with versioned, Production-status models from both Teams 1 and 2
- [ ] Dashboard loading within 5 seconds and displaying live predictions from both endpoints
- [ ] All code reviewed and merged into `team/ds-dashboard-mlops`

---

## Part 8: Tools and Environment Reference

### Development Environment

| Category           | Tool/Library               | Purpose/Used For                                           |
| :----------------- | :------------------------- | :--------------------------------------------------------- |
| **Tools**          | Python 3.12+               | Primary language for all modeling, API, and dashboard work |
|                    | Jupyter Notebooks          | EDA and model experimentation                              |
|                    | VS Code or PyCharm         | IDE for scripted development                               |
|                    | Docker Desktop             | Running the MLflow server and FastAPI endpoints locally    |
|                    | Postman                    | Testing and validating API endpoints against contracts     |
| **Core Libraries** | Pandas, NumPy              | Data loading and feature engineering                       |
|                    | Scikit-learn, XGBoost      | Model training and evaluation                              |
|                    | FastAPI                    | Wrapping trained models as local API endpoints             |
|                    | Streamlit                  | Dashboard development (DS Team 3)                          |
|                    | MLflow or Weights & Biases | Experiment tracking and model registry                     |
|                    | Plotly                     | Dashboard visualisations                                   |

### Data Source

All data is accessed from **AWS S3** in read-only mode. **You do not write back to S3.**

| Table           | Type      | Records        | Key Fields                                                           |
| :-------------- | :-------- | :------------- | :------------------------------------------------------------------- |
| `dim_customers` | Dimension | 100,000+       | customer_id, signup_date, demographics, loyalty_tier                 |
| `dim_products`  | Dimension | 5,000+         | product_id, category, brand, price, margin                           |
| `fact_orders`   | Fact      | 500,000+       | order_id, customer_id, product_id, amount, timestamp, payment_method |
| `fact_events`   | Fact      | 500K (sampled) | event_id, customer_id, session_id, event_type, timestamp, device     |

_Access credentials and S3 bucket paths are provided in the `.env` file at the root of the repository. Do not commit credentials to GitHub._

### GitHub Repository Structure

The repository is already scaffolded. Work only within your team's designated folder.

```
customer-intelligence-platform/
├── assets/
├── data_science/
│   ├── contracts/            ← shared — API contracts committed here
│   ├── feature_store/        ← shared — feature tables committed here
│   ├── team1_churn/          ← DS Team 1 workspace
│   ├── team2_recommendation/ ← DS Team 2 workspace
│   └── team3_dashboard_mlops/← DS Team 3 workspace
│       └── mock_api/         ← Team 3 mock server lives here
├── documentation/
│   ├── ds_coordination_guide.md
│   ├── pm_coordination_guide.md
│   ├── project_reference_guide.md
│   ├── repository_collaboration.md
│   └── team_responsibilities.md
├── .env                      ← credentials and API URLs (never commit changes here)
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

### Communication Channels

| Channel                      | Purpose                                                                    |
| :--------------------------- | :------------------------------------------------------------------------- |
| **WhatsApp — General Group** | Sprint-wide updates, milestone confirmations, announcements from PM Lead   |
| **WhatsApp — DS Sub-Group**  | Technical updates between DS teams, model iteration notes, endpoint status |
| **GitHub Issues**            | QA bugs, documentation gaps, and cross-team technical flags                |
| **Standup (daily, 15 min)**  | Blocker clearing — what was done, what is planned, what is blocked         |

---

## Part 9: Managing Blockers

If a cross-team dependency is at risk, raise it at the **next morning standup** — naming the specific deliverable, the team responsible, and the day it was due. The PM Lead is informed immediately. The affected team continues on mock data and does not pause. If a live endpoint is not ready by Day 9, the dashboard is demonstrated using mock data, which is an acceptable outcome provided it is communicated to the PM Lead and documented in advance.

---

_For Git and branching workflow, refer to:_ `repository_collaboration.md`  
_For individual team ownership and responsibilities, refer to:_ `team_responsibilities.md`  
_For full project specifications, model targets, and API details, refer to:_ `project_reference_guide.md`
