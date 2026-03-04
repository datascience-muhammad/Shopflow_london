# Contract 2: Recommendation Endpoint

**Ownership:** DS Team 2  
**Status:** FROZEN - agreed Day 2. Changes require DS Lead approval.

---

## Endpoint

Method  GET  
Path  `/recommend/{customer_id}`  
Query param  `n` (int, default 5, range 1–20)  
Local port  8002  
Response time  < 300ms

---

## Response Schema

**Top-level fields**  
`customer_id` - string  
`recommendations` - array  
`model_version` - string  
`timestamp` - string (ISO 8601 UTC)

**Each item in `recommendations`**  
`product_id` - string  
`product_name` - string  
`category` - string  
`predicted_score` - float (0.0–1.0)

> Array must be sorted descending by `predicted_score`.

---

## Sample Response
```json
{
  "customer_id": "CUST000001",
  "recommendations": [
    {
      "product_id": "PROD00001",
      "product_name": "Cultural Home",
      "category": "Home",
      "predicted_score": 0.94
    }
  ],
  "model_version": "rec-model-v1.0",
  "timestamp": "2026-02-10T14:32:00Z"
}
```

---

## Error Handling

404 - `customer_id` not found  
422 - `n` out of range (<1 or >20)  
500 - model unavailable 
200, return what's available - Fewer products than `n` requested

---

## Change Log

Day 2 — Initial contract agreed — DS Lead