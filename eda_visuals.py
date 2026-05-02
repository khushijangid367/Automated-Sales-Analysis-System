import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the cleaned data
df = pd.read_csv('data/cleaned_data.csv')

# Set the style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))

# 2. Visualization: Profit vs Revenue colored by Discount
# This will visually "clump" the negative profit orders together.
scatter = sns.scatterplot(
    data=df, 
    x='sales', 
    y='profit', 
    hue='discount', 
    palette='vlag', 
    size='quantity'
)

# Add a horizontal line at 0 profit to highlight the "Loss Zone"
plt.axhline(0, color='red', linestyle='--', linewidth=1.5)
plt.title('The Loss Zone: Impact of High Discounts on Profitability', fontsize=15)
plt.xlabel('sales per Order ($)', fontsize=12)
plt.ylabel('profit per Order ($)', fontsize=12)

# 3. Save the insight
plt.tight_layout()
plt.savefig('outputs/profit_loss_scatter.png')
print("📸 Step 5 Complete: 'profit_loss_scatter.png' saved to /outputs!")
plt.show()