# Contract 1: Churn Prediction Endpoint

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
