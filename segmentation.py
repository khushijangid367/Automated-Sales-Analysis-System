import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

def load_clean_data(file_path):
    """Loads the pre-cleaned Superstore data."""
    print(f"Loading cleaned data from {file_path}...")
    return pd.read_csv(file_path)

def aggregate_customer_data(df):
    """Rolls up transaction data to the Customer level."""
    print("Aggregating metrics by Customer name...")
    customer_df = df.groupby('customer_name').agg({
        'sales': 'sum',
        'profit': 'sum',
        'discount': 'mean'
    }).reset_index()
    return customer_df

def perform_clustering(customer_df, n_clusters=3):
    """Scales data and runs K-Means clustering."""
    print("Performing K-Means clustering...")
    features = customer_df[['sales', 'profit', 'discount']]
    
    # Machine Learning requires scaled data so large sales numbers don't overpower small discount decimals
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Run K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    customer_df['cluster'] = kmeans.fit_predict(scaled_features)
    
    return customer_df

def assign_business_labels(customer_df):
    """Dynamically maps abstract cluster numbers to actual business segments."""
    print("Mapping cluster numbers to business labels...")
    
    # Calculate the mean profit for each cluster to figure out who is who
    cluster_summary = customer_df.groupby('cluster').agg({'profit': 'mean'}).reset_index()
    
    # Sort the clusters from lowest profit to highest
    cluster_summary = cluster_summary.sort_values(by='profit').reset_index(drop=True)
    
    # Since it's sorted: Index 0 is worst profit, Index 1 is middle, Index 2 is best
    label_mapping = {
        cluster_summary.loc[0, 'cluster']: 'Margin Killers',
        cluster_summary.loc[1, 'cluster']: 'Regular',
        cluster_summary.loc[2, 'cluster']: 'High Value'
    }
    
    # Apply the mapping to our dataframe
    customer_df['customer_segment'] = customer_df['cluster'].map(label_mapping)
    
    # Print a beautiful summary for the terminal
    print("\n--- Final Customer Segments Profile ---")
    summary_display = customer_df.groupby('customer_segment').agg({
        'sales': 'mean',
        'profit': 'mean',
        'discount': 'mean',
        'customer_name': 'count'
    }).rename(columns={'customer_name': 'total_customers'}).round(2)
    print(summary_display)
    print("---------------------------------------\n")
    
    return customer_df

def execute_segmentation(input_path, output_path):
    """Runs the full segmentation pipeline."""
    print("--- Starting Customer Segmentation ---")
    df = load_clean_data(input_path)
    customer_df = aggregate_customer_data(df)
    customer_df = perform_clustering(customer_df)
    customer_df = assign_business_labels(customer_df)
    
    # Save the mapped dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    customer_df.to_csv(output_path, index=False)
    print(f"Segmented data saved to {output_path}")

if __name__ == "__main__":
    import os
    
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    
    INPUT_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned_data.csv")
    OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data", "customer_segments.csv")
    
    execute_segmentation(INPUT_PATH, OUTPUT_PATH)