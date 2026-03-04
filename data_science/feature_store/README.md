# Feature Store - rec_features.parquet

**Committed by:** DS Team 2  
**Date:** February 2026  
**Primary key:** `customer_id` + `product_id`  
**Shape:** 998,925 rows × 30 columns


## Purpose
Customer-product interaction features engineered from orders, events, and product data.
Used to build the customer-product interaction matrix for collaborative filtering.

## Interaction Features

`customer_id` — Unique identifier for each ShopFlow customer  
`product_id` — Unique identifier for each product in the catalogue  
`purchase_score` — Total quantity of this product purchased by this customer from order records, scaled 0–1  
`cart_count` — Number of times this customer added this product to their cart, scaled 0–1  
`purchase_count` — Number of times a purchase event was recorded for this customer-product pair from event tracking, scaled 0–1  
`view_count` — Number of times this customer viewed this product, scaled 0–1
`time_decay` — Recency weight per customer-product pair calculated as e^(−0.001 × days_since_most_recent_order). Values ranges from 0–1 where 1 means purchased today and lower values indicate older interactions. Multiplied into interaction_score to prioritise recent customer behaviour.
`interaction_score` — Combined weighted interaction signal (purchase_score × 0.4 + purchase_count × 0.3 + cart_count × 0.2 + view_count × 0.1). Higher score means stronger customer-product relationship



## Product Features

`product_name` — Human-readable product name from the ShopFlow catalogue  
`purchase_popularity` — Number of unique customers who have purchased this product. Higher means more widely bought  
`average_rating` — Average interaction score across all customers for this product. Reflects overall engagement depth beyond just purchase frequency  
`stock_status_encoded` — Product availability encoded as 0 (Out of Stock), 1 (Low Stock), 2 (In Stock). Used to deprioritise unavailable products in recommendations  
`prod_Beauty` — 1 if this product belongs to the Beauty category, 0 otherwise  
`prod_Books` — 1 if this product belongs to the Books category, 0 otherwise  
`prod_Clothing` — 1 if this product belongs to the Clothing category, 0 otherwise  
`prod_Electronics` — 1 if this product belongs to the Electronics category, 0 otherwise  
`prod_Home` — 1 if this product belongs to the Home category, 0 otherwise  
`prod_Sports` — 1 if this product belongs to the Sports category, 0 otherwise  


## Customer Features

`loyalty_tier` — Customer loyalty level encoded as 0 (Churned), 1 (Low Value), 2 (Medium Value), 3 (High Value)  
`tenure_days` — Number of days since the customer first signed up to ShopFlow  
`total_spend` — Total amount in £ spent by this customer across all orders  
`average_order` — Average £ value per order for this customer  
`orders_frequency` — Total number of orders placed by this customer  
`unique_products` — Number of distinct products this customer has purchased  
`cust_Beauty` — 1 if this customer's most frequently purchased category is Beauty, 0 otherwise  
`cust_Books` — 1 if this customer's most frequently purchased category is Books, 0 otherwise  
`cust_Clothing` — 1 if this customer's most frequently purchased category is Clothing, 0 otherwise  
`cust_Electronics` — 1 if this customer's most frequently purchased category is Electronics, 0 otherwise  
`cust_Home` — 1 if this customer's most frequently purchased category is Home, 0 otherwise  
`cust_Sports` — 1 if this customer's most frequently purchased category is Sports, 0 otherwise  
`cust_Unknown` — 1 if this customer has no purchase history to derive a category preference from, 0 otherwise  


## How This Data Is Used
The interaction_score column is pivoted into a customer-product matrix:

- Rows: unique customers (99,973)
- Columns: unique products (5,000)
- Values: interaction_score

This matrix is the input to the TruncatedSVD collaborative filtering model.


## Notes

- All interaction signal columns (purchase_score, cart_count, purchase_count, view_count) are MinMax scaled to 0–1 for comparability
- Matrix sparsity is high -  most customers interact with fewer than 10 products  
- Customer-product pairs with no interaction in one source table are filled with 0  
- One-hot encoded category columns use prefix cust_ for customer preferences and prod_ for product categories to avoid confusion  
- Primary key is the combination of customer_id and product_id - neither alone is unique in this table
- time_decay ensures recent interactions are weighted more heavily than older ones


**Primary key:** `customer_id` + `product_id` (composite)  
**Join key for Team 3:** `customer_id`  
**Note:** customer_id is not unique in this table. 
Each customer appears once per product interaction. 
Join on customer_id will produce multiple rows per customer.