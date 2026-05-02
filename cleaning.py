import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """Loads the raw Superstore dataset."""
    print(f"Loading data from {file_path}...")
    
    # Using 'latin1' is the ultimate fallback for CSVs with weird characters
    return pd.read_csv(file_path, encoding='latin1')

def standardize_columns(df):
    """Converts column headers to lowercase, snake_case, and strips whitespaces."""
    print("Standardizing column names...")
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('-', '_'))
    return df

def clean_numeric_columns(df):
    """Removes currency symbols and commas, converting text to numbers."""
    print("Converting financial columns to numeric...")
    numeric_cols = ['sales', 'profit', 'quantity', 'discount']
    
    for col in numeric_cols:
        if col in df.columns:
            # Convert to string first just in case, then strip $ and commas
            df[col] = df[col].astype(str).str.replace('$', '', regex=False)
            df[col] = df[col].str.replace(',', '', regex=False)
            df[col] = df[col].str.replace('£', '', regex=False) # Catch pounds just in case
            
            # Force conversion to float (decimals)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def parse_dates(df, date_columns):
    """Standardizes string dates into proper datetime objects."""
    print("Parsing dates...")
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def handle_duplicates_and_nulls(df):
    """Handles duplicate rows and missing data anomalies."""
    print("Handling duplicates and nulls...")
    
    # Drop exact duplicate rows (Superstore can have multiple identical line items)
    initial_shape = df.shape[0]
    df = df.drop_duplicates()
    print(f"Dropped {initial_shape - df.shape[0]} duplicate rows.")
    
    # Superstore dataset often has missing Postal Codes for certain cities (e.g., Burlington, VT)
    if 'postal_code' in df.columns:
        df['postal_code'] = df['postal_code'].fillna('Unknown')
        
    # Drop rows where critical financial metrics are somehow missing
    df = df.dropna(subset=['sales', 'profit', 'quantity'])
    return df

def handle_outliers(df):
    """Caps extreme values to prevent skewed analysis."""
    print("Handling outliers...")
    
    # Cap suspiciously high quantities at the 99th percentile
    q99 = df['quantity'].quantile(0.99)
    df['quantity'] = np.where(df['quantity'] > q99, q99, df['quantity'])
    
    # Filter out any negative sales or zero quantities
    df = df[(df['sales'] >= 0) & (df['quantity'] > 0)]
    return df

def derive_business_columns(df):
    """Adds calculated columns for deeper business insights."""
    print("Deriving new business columns...")
    # Add Profit Margin (handling potential division by zero)
    df['profit_margin'] = np.where(df['sales'] > 0, df['profit'] / df['sales'], 0)
    
    # Extract time-based features for seasonal analysis
    df['order_year'] = df['order_date'].dt.year
    df['order_month'] = df['order_date'].dt.month
    return df

def execute_cleaning_pipeline(input_path, output_path):
    """Runs the full data cleaning process sequentially."""
    print("--- Starting Data Cleaning Pipeline ---")
    df = load_data(input_path)
    df = standardize_columns(df)
    df = clean_numeric_columns(df)
    df = parse_dates(df, ['order_date', 'ship_date'])
    df = handle_duplicates_and_nulls(df)
    df = handle_outliers(df)
    df = derive_business_columns(df)
    
    # Save the cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"--- Pipeline Complete ---")
    print(f"Cleaned data saved to {output_path}")
    print(f"Final Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

if __name__ == "__main__":
    import os
    
    # This finds the folder where cleaning.py lives (the 'scripts' folder)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # This goes UP one level to your main project folder
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    
    # Now we build the correct absolute paths
    RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw_sales.csv")
    CLEANED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned_data.csv")
    
    execute_cleaning_pipeline(RAW_DATA_PATH, CLEANED_DATA_PATH)