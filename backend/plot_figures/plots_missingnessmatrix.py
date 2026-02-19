import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load only a small sample (20,000 rows is plenty)
df_sample = pd.read_csv('train_transaction.csv', nrows=20000)

# 2. Plotting - we use every 2nd or 3rd column to save even more space
columns_to_show = df_sample.columns[::2] 

plt.figure(figsize=(16, 8))
sns.heatmap(df_sample[columns_to_show].isnull(), cbar=False, cmap='viridis', yticklabels=False)

plt.title('Missingness Pattern (Sampled 20k Rows)', fontsize=16)
plt.xlabel('Columns (Showing every 2nd feature)', fontsize=12)
plt.xticks(rotation=90, fontsize=7)
plt.tight_layout()
plt.show()