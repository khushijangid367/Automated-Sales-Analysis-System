import sqlite3
import pandas as pd

# 1. Connect to the database
conn = sqlite3.connect('sales_data.db')

# 2. Aggregation 1: Profitability by Segment & Region
query_profitability = """
SELECT 
    Customer_Segment, 
    Region, 
    SUM(Revenue) AS Total_Revenue, 
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(Profit_Margin) * 100, 2) AS Margin_Pct
FROM sales
GROUP BY Customer_Segment, Region
ORDER BY Total_Profit DESC;
"""

# 3. Aggregation 2: Discount Impact
query_discounts = """
SELECT 
    Discount_Percent,
    COUNT(Order_ID) AS Order_Count,
    SUM(Revenue) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(Profit_Margin) * 100, 2) AS Avg_Margin_Pct
FROM sales
GROUP BY Discount_Percent;
"""

# 4. Pull to DataFrames and Save to /outputs
profit_df = pd.read_sql_query(query_profitability, conn)
discount_df = pd.read_sql_query(query_discounts, conn)

profit_df.to_csv('outputs/segment_profitability.csv', index=False)
discount_df.to_csv('outputs/discount_impact.csv', index=False)

conn.close()
print("✅ Step 4 Complete: Aggregated tables saved to the /outputs folder!")