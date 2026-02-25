import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_s3_data(table_name):
    """
    Loads a parquet file from S3 based on the table name.
    Available tables: 'customers', 'products', 'orders', 'events'
    """
    s3_path = os.getenv('S3_DATA_PATH')
    
    # Construct full S3 path
    full_path = f"{s3_path}{table_name}.parquet"
    
    # Storage options for S3 access
    storage_options = {
        "key": os.getenv('AWS_ACCESS_KEY_ID'),
        "secret": os.getenv('AWS_SECRET_ACCESS_KEY'),
        "client_kwargs": {
            "region_name": os.getenv('AWS_REGION')
        }
    }
    
    print(f"Fetching {table_name} from {full_path}...")
    try:
        # Note: requires pip install s3fs pyarrow
        df = pd.read_parquet(full_path, storage_options=storage_options)
        print(f"Successfully loaded {table_name} with {len(df)} rows.")
        return df
    except Exception as e:
        print(f"Error loading {table_name}: {e}")
        return None

if __name__ == "__main__":
    # Test loading available tables
    tables = ['customers', 'products', 'orders', 'events']
    
    for table in tables:
        df = get_s3_data(table)
        if df is not None:
            print(f"\nSample data from {table}:")
            print(df.head())
            print("-" * 30)
        else:
            print(f"\nFailed to retrieve {table}.")
