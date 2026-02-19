import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and Merge Data
train_trans = pd.read_csv('train_transaction.csv', usecols=['TransactionID', 'isFraud'])
train_id = pd.read_csv('train_identity.csv', usecols=['TransactionID', 'DeviceType'])
df = pd.merge(train_trans, train_id, on='TransactionID', how='inner')
df = df[df['DeviceType'].isin(['mobile', 'desktop'])]

# 2. Create the Cross-Tabulation
# This counts how many 0s and 1s are in each DeviceType
cross_tab = pd.crosstab(df['DeviceType'], df['isFraud'])

# 3. Normalize by Column (This is the "Secret Sauce")
# This makes it so the sum of all "Normal" (0) bars = 1.0 
# and the sum of all "Fraud" (1) bars = 1.0
normalized_df = cross_tab.div(cross_tab.sum(axis=0), axis=1)

# 4. Plotting
# Swapping labels to match your request: 0 = Green, 1 = Red
colors = ['#2ecc71', '#e74c3c'] 
ax = normalized_df.plot(kind='bar', figsize=(10, 6), color=colors, width=0.7)

# 5. Formatting
plt.title('Relative Distribution of Fraud vs. Normal across Devices', fontsize=14, fontweight='bold')
plt.ylabel('Proportion (Normalized)', fontsize=12)
plt.xlabel('Device Type', fontsize=12)
plt.legend(['Normal (0)', 'Fraud (1)'], title="Status")
plt.xticks(rotation=0)

# Add percentage labels on top of each bar
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2%}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 9), 
                textcoords='offset points',
                fontweight='bold')

plt.tight_layout()
plt.show()