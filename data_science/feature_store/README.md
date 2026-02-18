# Feature Store Schema Documentation

## Requirement

Both files must include `customer_id` as the primary key.
Schema documentation is mandatory in this file (`feature_store/README.md`) for each feature added.

## Files

- `churn_features.parquet` (DS Team 1 — RFM and behavioural features)
- `rec_features.parquet` (DS Team 2 — customer-product interaction data)

## Schema Details

### Churn Features (`churn_features.parquet`)

| Column Name | Type   | Description |
| ----------- | ------ | ----------- |
| customer_id | string | Primary Key |
| ...         | ...    | ...         |

### Recommendation Features (`rec_features.parquet`)

| Column Name | Type   | Description |
| ----------- | ------ | ----------- |
| customer_id | string | Primary Key |
| ...         | ...    | ...         |
