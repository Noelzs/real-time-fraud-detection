import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and Merge Data
train_trans = pd.read_csv('train_transaction.csv', usecols=['TransactionID', 'isFraud'])
train_id = pd.read_csv('train_identity.csv', usecols=['TransactionID', 'id_23'])
df = pd.merge(train_trans, train_id, on='TransactionID', how='inner')

# 2. Clean and Filter Proxy Data
# We only care about the three proxy types mentioned
proxy_types = ['IP_PROXY:ANONYMOUS', 'IP_PROXY:HIDDEN', 'IP_PROXY:TRANSPARENT']
df = df[df['id_23'].isin(proxy_types)]

# 3. Create the Cross-Tabulation
cross_tab = pd.crosstab(df['id_23'], df['isFraud'])

# 4. Normalize by Column (Status)
# Green bars = % of all Normal transactions using that proxy
# Red bars = % of all Fraud transactions using that proxy
normalized_df = cross_tab.div(cross_tab.sum(axis=0), axis=1)

# 5. Plotting
colors = ['#2ecc71', '#e74c3c'] 
ax = normalized_df.plot(kind='bar', figsize=(12, 7), color=colors, width=0.8)

# Formatting
plt.title('Relative Distribution of Fraud vs. Normal across Proxy Types (id_23)', fontsize=14, fontweight='bold')
plt.ylabel('Proportion (Normalized)', fontsize=12)
plt.xlabel('Proxy Status', fontsize=12)
plt.legend(['Normal (0)', 'Fraud (1)'], title="Status")
plt.xticks(rotation=0) # Keeps labels horizontal for readability

# Add percentage labels
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2%}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 9), 
                textcoords='offset points',
                fontweight='bold')

plt.tight_layout()
plt.show()