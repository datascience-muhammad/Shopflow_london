# Contract 2: Recommendation Endpoint

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
