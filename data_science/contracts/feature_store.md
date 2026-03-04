# Contract 3: Feature Store Schema

**Ownership:** DS Team 2 (rec_features.parquet)  
**Status:** FROZEN - agreed Day 2. Changes require DS Lead approval.  
**Location:** data_science/feature_store/  
**Read access:** DS Team 3 (dashboard visualisations)


## Rules

- All files must use `customer_id` as the primary key for joining across datasets
- Schema documentation is mandatory in `feature_store/README.md`
- Files larger than 100MB must be stored in S3 — commit only the S3 reference path
- Always pull from dev before committing to the feature store to avoid conflicts
- Do not attempt parallel edits to `feature_store/README.md` — coordinate in 
  WhatsApp DS sub-group and commit sequentially


## File

| File | Owner | Status |
|---|---|---|
| `rec_features.parquet` | DS Team 2 | Committed |


## rec_features.parquet - Agreed Schema

**Primary Key:** `customer_id` + `product_id` (composite)  
**Join Key for Team 3:** `customer_id`  
**Minimum required columns:**

| Column | Type | Description |
|---|---|---|
| `customer_id` | string | Unique customer identifier |
| `product_id` | string | Unique product identifier |
| `interaction_score` | float | Combined weighted interaction signal |

Full schema documented in `feature_store/README.md`

---

## Notes

- DS Team 3 joins on `customer_id` for dashboard visualisations
- File does not contain model predictions - raw engineered features only
- Committed before Day 5 end of day
```
