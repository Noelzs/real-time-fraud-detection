import pandas as pd
import matplotlib.pyplot as plt

# 1. Load your data
# Using usecols makes loading much faster and saves RAM
train_trans = pd.read_csv('train_transaction.csv', usecols=['TransactionID', 'isFraud'])
train_id = pd.read_csv('train_identity.csv', usecols=['TransactionID'])

# 2. Prepare the Identity Subset (Intersection)
# Inner join keeps only TransactionIDs present in BOTH files
merged_df = pd.merge(train_id, train_trans, on='TransactionID', how='inner')

# 3. Setup Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
colors = ['#2ecc71', '#e74c3c']  # Green for Not Fraud (0), Red for Fraud (1)

def annotated_bar_plot(df, ax, title):
    counts = df['isFraud'].value_counts().sort_index()
    total = len(df)
    
    # Create the bars
    bars = ax.bar(counts.index.astype(str), counts.values, color=colors)
    
    # Labeling
    ax.set_title(title, fontsize=15, fontweight='bold', pad=20)
    ax.set_ylabel('TransactionID count', fontsize=12)
    ax.set_xlabel('isFraud Status', fontsize=12)
    ax.set_xticklabels(['Not Fraud (0)', 'Fraud (1)'])
    
    # Add percentage labels on top of bars
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height + (total * 0.005),
                f'{percentage:.2f}%', ha='center', va='bottom', 
                fontsize=12, fontweight='bold')
    
    # Visual cleanup
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# 4. Generate the two charts
annotated_bar_plot(train_trans, ax1, 'Fraud Distribution: Full Dataset')
annotated_bar_plot(merged_df, ax2, 'Fraud Distribution: Identity Subset')

plt.tight_layout()
plt.show()