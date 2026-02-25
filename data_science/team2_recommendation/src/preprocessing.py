"""
DS Team 2: Preprocessing & Feature Engineering
Builds the User-Item Interaction Matrix and RFM features for the Recommendation Engine.
"""

import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()


def load_raw_data():
    """Load all raw datasets using the data_loader utility."""
    from data_loader import get_s3_data

    customers = get_s3_data('customers')
    products = get_s3_data('products')
    orders = get_s3_data('orders')
    events = get_s3_data('events')

    return customers, products, orders, events


def build_interaction_matrix(orders, events):
    """
    Combines purchase and browsing data into a weighted interaction matrix.

    Weights: view=1, cart=2, purchase=5

    Returns a DataFrame with columns: customer_id, product_id, implicit_score (0-1 normalized)
    """
    event_weights = {'view': 1, 'cart': 2, 'purchase': 5}

    # Score from events (views and carts)
    events_scored = events.copy()
    events_scored['weight'] = events_scored['event_type'].map(event_weights).fillna(0)
    event_interactions = (
        events_scored
        .groupby(['customer_id', 'product_id'])['weight']
        .sum()
        .reset_index()
        .rename(columns={'weight': 'event_score'})
    )

    # Score from orders (each order = purchase weight)
    order_interactions = (
        orders
        .groupby(['customer_id', 'product_id'])
        .size()
        .reset_index(name='order_count')
    )
    order_interactions['order_score'] = order_interactions['order_count'] * event_weights['purchase']
    order_interactions = order_interactions[['customer_id', 'product_id', 'order_score']]

    # Merge event scores and order scores
    interactions = pd.merge(
        event_interactions, order_interactions,
        on=['customer_id', 'product_id'],
        how='outer'
    ).fillna(0)

    # Combined raw score
    interactions['raw_score'] = interactions['event_score'] + interactions['order_score']

    # Normalize to [0, 1] range (contract requirement: predicted_score 0.0-1.0)
    max_score = interactions['raw_score'].max()
    if max_score > 0:
        interactions['implicit_score'] = interactions['raw_score'] / max_score
    else:
        interactions['implicit_score'] = 0.0

    return interactions[['customer_id', 'product_id', 'implicit_score', 'raw_score']]


def build_rfm_features(orders):
    """
    Calculates Recency, Frequency, and Monetary values for each customer.

    Returns a DataFrame with columns: customer_id, recency_days, frequency, monetary
    """
    orders = orders.copy()
    orders['timestamp'] = pd.to_datetime(orders['timestamp'])

    reference_date = orders['timestamp'].max() + pd.Timedelta(days=1)

    rfm = orders.groupby('customer_id').agg(
        recency_days=('timestamp', lambda x: (reference_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('amount', 'sum')
    ).reset_index()

    return rfm


def build_product_lookup(products):
    """
    Creates a lookup table mapping product_id to product_name and category.
    Needed by the API to return full product details per contract.
    """
    lookup = products[['product_id', 'product_name', 'category']].drop_duplicates()
    return lookup


def create_feature_store_output(interactions, rfm, product_lookup):
    """
    Merges interaction matrix with RFM and product metadata,
    then returns a combined DataFrame for the shared feature store.
    """
    rec_features = pd.merge(interactions, product_lookup, on='product_id', how='left')
    rec_features = pd.merge(rec_features, rfm, on='customer_id', how='left')
    return rec_features


if __name__ == "__main__":
    # Load data
    print("Loading raw data from S3...")
    customers, products, orders, events = load_raw_data()

    # Build interaction matrix
    print("Building User-Item Interaction Matrix...")
    interactions = build_interaction_matrix(orders, events)
    print(f"  Interactions: {len(interactions)} rows")
    print(f"  Users: {interactions['customer_id'].nunique()}, Products: {interactions['product_id'].nunique()}")
    print(f"  Score range: {interactions['implicit_score'].min():.4f} - {interactions['implicit_score'].max():.4f}")

    # Build RFM features
    print("Building RFM Features...")
    rfm = build_rfm_features(orders)
    print(f"  RFM profiles: {len(rfm)} customers")
    print(rfm.describe())

    # Build product lookup
    print("Building Product Lookup Table...")
    product_lookup = build_product_lookup(products)
    print(f"  Products in lookup: {len(product_lookup)}")

    # Create and save feature store output
    print("Creating rec_features.parquet...")
    rec_features = create_feature_store_output(interactions, rfm, product_lookup)

    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'feature_store', 'rec_features.parquet'
    )
    rec_features.to_parquet(output_path, index=False)
    print(f"  Saved to: {output_path}")
    print(f"  Total rows: {len(rec_features)}")
    print(f"  Columns: {list(rec_features.columns)}")
    print("Done.")
