# Model Card — Recommendation Engine
## ShopFlow Customer Intelligence Platform — DS Team 2

**Model Name:** recommendation-model  
**Version:** v2.0 (@champion)  
**Type:** Collaborative Filtering - Truncated Singular Value Decomposition (TruncatedSVD)  
**Owner:** DS Team 2  
**Training Date:** 2026-02-28  
**Status:** Production (@champion alias in MLflow Model Registry)  
**API Endpoint:** GET /recommend/{customer_id}?n=5 - Port 8002  
**Response Time:** 143.28ms (target: < 300ms)


### 1. Model Purpose

This model provides personalised top-N product recommendations for ShopFlow customers. Given a customer ID, the model returns up to 5 products the customer is most likely to engage with, based on the purchasing and browsing behaviour of similar customers across the ShopFlow platform.

### 2. Business Context

ShopFlow's static recommendation system produced a 2% click-through rate. This model replaces rule-based recommendations with collaborative filtering, learning hidden patterns in customer-product interactions to surface relevant, personalised suggestions - targeting improved engagement and reduced cart abandonment.


### 3. Model Architecture

| Property | Detail |
|---|---|
| Algorithm | Truncated Singular Value Decomposition (TruncatedSVD) |
| Library | scikit-learn 1.4.2 |
| Approach | Matrix Factorisation — Collaborative Filtering |
| Input | Customer-product interaction matrix (99,973 × 5,000) |
| Latent Dimensions | 100 (n_components) |
| Iterations | 5 (n_iter) |
| Random State | 42 |
| Scoring | Dot product of customer and item latent factor vectors |
| Normalisation | Scores normalised to 0–1 range per customer |
| Filtering | Already-interacted products excluded from recommendations |

#### How It Works

1. The customer-product interaction matrix is decomposed into latent factor matrices
2. Each customer and product is represented as a 100-dimensional vector
3. Recommendations are scored by computing the dot product between a customer's vector and all item vectors
4. Products the customer has already interacted with are excluded
5. Top-N products by score are returned, enriched with product name and category


### 4. Training Data

| Property | Detail |
|---|---|
| Source | rec_features.parquet — data_science/feature_store/ |
| Customers | 99,973 unique customers |
| Products | 5,000 unique products |
| Interactions | 998,925 customer-product pairs |
| Matrix Sparsity | High — most customers interact with fewer than 10 products |
| Interaction Signal | Composite score: purchase_score × 0.4 + purchase_count × 0.3 + cart_count × 0.2 + view_count × 0.1 |
| Recency Weighting | time_decay = e^(−0.001 × days_since_last_order) applied to interaction_score |

#### Features Used

The model uses the `interaction_score` column from `rec_features.parquet`, pivoted into a customer-product matrix. Raw features that feed into this score:

- `purchase_score` - scaled purchase quantity per customer-product pair
- `purchase_count` - number of purchase events from event tracking
- `cart_count` - number of add-to-cart events
- `view_count` - number of product views
- `time_decay` - recency weight (recent interactions score higher)


### 5. Model Selection

Four models were trained, evaluated, and compared before selecting TruncatedSVD tuned:

| Model | Precision@5 | Recall@5 | F1@5 | NDCG@5 | Relevance@5 | Selected |
|---|---|---|---|---|---|---|
| Cosine Similarity | 0.0579 | 0.2897 | 0.0966 | 0.2399 | 0.0037 | No |
| TruncatedSVD (n_components=50) | 0.0372 | 0.1862 | 0.0621 | 0.1453 | 0.8016 | No |
| Alternating Least Squares | 0.0064 | 0.0322 | 0.0107 | 0.0287 | 0.6763 | No |
| **TruncatedSVD (n_components=100)** | **0.0699** | **0.3494** | **0.1165** | **0.2807** | **0.8004** | **Yes ✅** |

All experiments logged to: https://dagshub.com/marynguma6-cmyk/shopflow_mlflow.mlflow


### 6. Hyperparameter Tuning

Grid search over 12 combinations of n_components and n_iter:

| n_components | n_iter | Relevance@5 |
|---|---|---|
| **100** | **5** | **0.8314** - selected |
| 150 | 5 | 0.8314 |
| 50 | 5 | 0.8127 |
| 20 | 5 | 0.7881 |
| 150 | 10 | 0.7978 |
| 100 | 10 | 0.7964 |

**Key finding:** 
- Lower n_iter (5) consistently outperforms higher n_iter (10, 20) across all component sizes.
- Higher iterations overfit on sparse implicit feedback data.
- n_components=100 selected as it gives the best relevance without the computational cost of 150.


### 7. Evaluation Metrics

**Evaluation Method:** Leave-One-Out - last interaction hidden as test item.  
Evaluated on 500 sampled customers.

| Metric | Score | Notes |
|---|---|---|
| Precision@5 | 0.0699 | 1 in 14 recommendations is relevant |
| Recall@5 | 0.3494 | Model recovers 35% of relevant items in top 5 |
| F1@5 | 0.1165 | Balanced score between precision and recall |
| NDCG@5 | 0.2807 | Relevant items appear consistently high in ranked list |
| **Relevance@5** | **0.8004** | Primary metric — high confidence recommendations |
| Response Time | 143.28ms | Well within 300ms target |

#### Note on Evaluation Method

- Leave-One-Out evaluation was used instead of random 80/20 split.
- Most customers have 4–5 interactions total - a random split leaves most customers with 0 test products, making Precision/Recall/F1/NDCG impossible to compute meaningfully.
- Leave-One-Out hides the last interaction per customer as the test item, ensuring every customer with at least 2 interactions contributes to evaluation regardless of sparsity.


### 8. API Contract Compliance

The model output conforms exactly to Contract 2 agreed on Day 2 of the sprint:

```json
{
  "customer_id": "CUST000001",
  "recommendations": [
    {
      "product_id": "PROD01096",
      "product_name": "Hope Books",
      "category": "Books",
      "predicted_score": 1.0
    }
  ],
  "model_version": "rec-model-svd-v1.0",
  "timestamp": "2026-02-28T00:00:00Z"
}
```

- Recommendations sorted descending by predicted_score
- predicted_score normalised to 0.0–1.0
- n parameter supported (1–20, default 5)
- 404 returned for unknown customer_id
- 422 returned for n out of range


### 9. Limitations

- **Sparsity:** Most customers have fewer than 10 product interactions. Recommendations for new or low-activity customers may be less personalised.
- **Cold Start:** New customers with no interaction history cannot receive personalised recommendations. The model will return a 404 for customers not in the training matrix.
- **Static Model:** The model is trained on historical data. It does not update in real time as new interactions occur.
- **Implicit Feedback:** Interaction scores are derived from behavioural signals (views, carts, purchases) rather than explicit ratings. High scores reflect engagement, not necessarily satisfaction.


## 10. MLflow Registry

| Property | Detail |
|---|---|
| Experiment | recommendation-engine |
| Run | svd-tuned-final |
| Registered Model | recommendation-model |
| Version | 2 |
| Alias | @champion |
| Registry | https://dagshub.com/marynguma6-cmyk/shopflow_mlflow.mlflow |


### 11. Files

| File | Location | Description |
|---|---|---|
| rec_model_svd_v1.pkl | data_science/team2_recommendation/models/artifacts/ | Trained model bundle |
| rec_features.parquet | data_science/feature_store/ | Feature store input |
| schemas.py | data_science/team2_recommendation/ | Pydantic response schemas |
| model.py | data_science/team2_recommendation/ | Model loading and inference |
| main.py | data_science/team2_recommendation/ | FastAPI application |
| 01_eda.ipynb | data_science/team2_recommendation/ | Exploratory data analysis |
| 02_modeling.ipynb | data_science/team2_recommendation/ | Model training, evaluation and MLflow logging |
