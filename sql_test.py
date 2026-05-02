import sqlite3
import pandas as pd
import os

# 1. Force Python to find the exact correct folders
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "sales_data.db")
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned_data.csv")

print(f"Connecting to database at: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)

# 2. THE NUCLEAR OPTION: Force the database to refresh right now
print("Forcing database refresh from cleaned CSV...")
try:
    df = pd.read_csv(CSV_PATH)
    
    # THE FIX: Strip the hidden BOM characters out of the column names
    df.columns = df.columns.str.replace('ï»¿', '')
    
    df.to_sql('sales', conn, if_exists='replace', index=False)
    print("✅ Database successfully overwritten with real data!")
except Exception as e:
    print(f"❌ Failed to load CSV into Database: {e}")

# 3. Run the Discount Impact query 
query = """
SELECT 
    discount,
    COUNT(order_id) AS Total_Orders,
    ROUND(AVG(profit_margin) * 100, 2) AS Avg_Margin_Pct
FROM sales
GROUP BY discount
"""

try:
    results = pd.read_sql_query(query, conn)
    print("\n📊 DISCOUNT IMPACT ANALYSIS:")
    print(results)
except Exception as e:
    print(f"\n❌ SQL Error: {e}")

conn.close()