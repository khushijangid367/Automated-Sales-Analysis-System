import sqlite3
import pandas as pd
import os

def setup_database():
    print("🔄 Refreshing the SQLite Database...")
    
    # 1. Get the exact path of the current folder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Build the paths directly from the base directory
    csv_path = os.path.join(BASE_DIR, "data", "cleaned_data.csv")
    db_path = os.path.join(BASE_DIR, "sales_data.db")
    
    # 3. Read the newly cleaned Kaggle data
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 4. Connect to the database
    conn = sqlite3.connect(db_path)
    
    # 5. Push the data to SQL (replacing the old fake data completely)
    print("Pushing new data to SQLite...")
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    print("✅ Database successfully updated with real Superstore data!")
    conn.close()

if __name__ == "__main__":
    setup_database()