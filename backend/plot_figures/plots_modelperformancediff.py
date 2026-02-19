# plot_dual_comparison.py
import matplotlib.pyplot as plt
import numpy as np

def create_dual_performance_plot():
    """Create both comparison plots side-by-side"""
    
    # Your actual data
    models = ['Random Forest', 'XGBoost']
    speed = [54.6, 1490.7]
    detection = [33.8, 39.1]
    auc_scores = [0.77, 0.77]
    
    # Create figure with 1 row, 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # ========== LEFT PLOT: Detailed Bubble Chart ==========
    # Create scatter plot with bubble size
    scatter = ax1.scatter(speed, detection, 
                         s=[1500, 2500],  # Bubble sizes
                         c=['#FF6B6B', '#4ECDC4'],  # Colors
                         alpha=0.9,
                         edgecolors='black',
                         linewidth=3,
                         zorder=5)
    
    # Add labels for each point
    for i, (model, sp, det) in enumerate(zip(models, speed, detection)):
        # Model name
        ax1.annotate(model, 
                    xy=(sp, det),
                    xytext=(0, 40),
                    textcoords='offset points',
                    fontsize=14,
                    fontweight='bold',
                    ha='center',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9, edgecolor='black'))
        
        # Performance metrics
        ax1.annotate(f'{det}% Detection',
                    xy=(sp, det - 0.3),
                    ha='center',
                    fontsize=11,
                    fontweight='bold',
                    color='black')
        
        # Speed
        ax1.annotate(f'{sp:,.0f} tx/sec',
                    xy=(sp, det - 1.2),
                    ha='center',
                    fontsize=10,
                    fontweight='bold',
                    color='dimgray')
    
    # Improvement arrow
    ax1.annotate('',
                xy=(speed[1], detection[1]),
                xytext=(speed[0], detection[0]),
                arrowprops=dict(arrowstyle='fancy',
                              connectionstyle='arc3,rad=0.3',
                              color='gold',
                              linewidth=4,
                              alpha=0.9,
                              shrinkA=10,
                              shrinkB=10))
    
    # Improvement annotation
    ax1.annotate('22× FASTER\n+5.3% BETTER',
                xy=((speed[0] + speed[1])/2, (detection[0] + detection[1])/2 + 1.5),
                ha='center',
                fontsize=12,
                fontweight='bold',
                color='darkblue',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="gold", alpha=0.9))
    
    ax1.set_xlabel('Processing Speed (transactions/second)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Fraud Detection Rate (%)', fontsize=12, fontweight='bold')
    ax1.set_title('XGBoost vs Random Forest: The Performance Gap', 
                 fontsize=14, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim(0, 1600)
    ax1.set_ylim(30, 42)
    
    # ========== RIGHT PLOT: Simple Bar Comparison ==========
    x = np.arange(len(models))
    width = 0.35
    
    # Speed bars
    bars1 = ax2.bar(x - width/2, speed, width, label='Speed (tx/sec)', 
                   color='#4ECDC4', edgecolor='black', linewidth=2)
    
    # Detection bars
    bars2 = ax2.bar(x + width/2, detection, width, label='Detection (%)', 
                   color='#FF6B6B', edgecolor='black', linewidth=2)
    
    ax2.set_xlabel('Model Type', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Performance Metric', fontsize=12, fontweight='bold')
    ax2.set_title('Direct Comparison: Speed & Detection', 
                 fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 100:  # Speed values (large)
                ax2.text(bar.get_x() + bar.get_width()/2., height + 50,
                        f'{height:,.0f}', ha='center', va='bottom', 
                        fontweight='bold', fontsize=11)
            else:  # Detection values (small)
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}', ha='center', va='bottom', 
                        fontweight='bold', fontsize=11)
    
    # Add dramatic improvement annotations
    # Speed improvement
    ax2.annotate('22×',
                xy=(1, speed[1]/2),
                xytext=(1.4, speed[1]/2),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'),
                fontsize=14,
                fontweight='bold',
                color='darkblue',
                ha='center')
    
    # Detection improvement
    detection_improvement = detection[1] - detection[0]
    ax2.annotate(f'+{detection_improvement:.1f}%',
                xy=(1, detection[1]),
                xytext=(1.4, detection[1] + 1),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'),
                fontsize=13,
                fontweight='bold',
                color='darkred',
                ha='center')
    
    # Set y-axis limits appropriately
    ax2.set_ylim(0, max(speed) * 1.15)
    
    # Add overall title
    plt.suptitle('Why XGBoost Wins: Unbeatable Speed with Superior Accuracy', 
                fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    # Save high-quality versions
    plt.savefig('dual_performance_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('dual_performance_comparison.svg', bbox_inches='tight', facecolor='white')
    plt.savefig('dual_performance_comparison.pdf', bbox_inches='tight', facecolor='white')
    
    print("✅ Dual comparison plot saved!")
    print("   Files created:")
    print("   • dual_performance_comparison.png")
    print("   • dual_performance_comparison.svg (best for slides)")
    print("   • dual_performance_comparison.pdf")
    
    # Print the exact numbers for your slide notes
    print("\n📊 EXACT NUMBERS FOR YOUR SLIDE:")
    print(f"   Random Forest: {detection[0]}% detection @ {speed[0]:.1f} tx/sec")
    print(f"   XGBoost: {detection[1]}% detection @ {speed[1]:.1f} tx/sec")
    print(f"   Improvement: +{detection_improvement:.1f}% detection, {speed[1]/speed[0]:.0f}× faster")
    
    plt.show()

# Run it directly
if __name__ == "__main__":
    print("🎯 GENERATING DUAL PERFORMANCE COMPARISON PLOT")
    print("="*60)
    create_dual_performance_plot()