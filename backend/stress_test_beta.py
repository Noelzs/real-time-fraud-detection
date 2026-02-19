import pandas as pd
import numpy as np
import time
from datetime import datetime
from model_utils import load_model_version, list_model_versions
from collections import deque

def convert_to_indian_rupees(amount):
    """Convert IEEE-CIS normalized amounts to realistic Indian Rupees"""
    if amount < 10:
        return max(500, amount * 100)
    elif amount < 100:
        return amount * 200 + 1000
    else:
        return min(50000, amount * 150 + 5000)

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    WHITE = "\033[97m"      # Unflagged legit
    GREEN = "\033[92m"      # Flagged and correct (true positive)
    RED = "\033[91m"        # Missed fraud (false negative)
    YELLOW = "\033[93m"     # Flagged but wrong (false positive)
    CYAN = "\033[96m"       # Stats/headers
    GRAY = "\033[90m"       # Dimmed text

def live_fraud_demo(model, features, transaction_data, max_transactions=10000, 
                   show_mode='all', threshold=0.063):
    """
    OPTIMIZED Live fraud detection demo with batch processing
    """
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}🎯 LIVE FRAUD DETECTION DEMO (OPTIMIZED){Colors.RESET}")
    print(f"{Colors.CYAN}Mode: {'ALL TRANSACTIONS' if show_mode == 'all' else 'INTERESTING ONLY'}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
    
    # Pre-process data for batch operations
    print(f"{Colors.CYAN}Preparing data for batch processing...{Colors.RESET}")
    
    # Convert to numpy arrays for faster access
    feature_names = features['feature_names']
    feature_matrix = transaction_data[feature_names].values[:max_transactions]
    amounts = transaction_data['TransactionAmt'].values[:max_transactions]
    
    # Get actual fraud labels if available
    if 'isFraud' in transaction_data.columns:
        fraud_labels = transaction_data['isFraud'].values[:max_transactions]
    else:
        fraud_labels = np.zeros(max_transactions, dtype=int)
    
    total_count = len(feature_matrix)
    
    print(f"{Colors.CYAN}Processing {total_count:,} transactions{Colors.RESET}")
    print(f"{Colors.CYAN}Threshold: {threshold}{Colors.RESET}")
    print(f"{Colors.CYAN}Batch size: 1000 transactions{Colors.RESET}")
    print(f"{Colors.CYAN}{'-'*70}{Colors.RESET}")
    
    # Legend
    print(f"\n{Colors.CYAN}🎨 COLOR LEGEND:{Colors.RESET}")
    if show_mode == 'all':
        print(f"{Colors.WHITE}  ○ Legitimate transaction{Colors.RESET}")
    print(f"{Colors.GREEN}  ✅ Correct fraud detection{Colors.RESET}")
    print(f"{Colors.RED}  ❌ Missed fraud{Colors.RESET}")
    print(f"{Colors.YELLOW}  ⚠️  False alarm{Colors.RESET}")
    print(f"{Colors.CYAN}{'-'*70}{Colors.RESET}\n")
    
    # Initialize counters
    fraud_count = 0
    detected_frauds = 0
    missed_frauds = 0
    false_positives = 0
    actual_frauds_in_sample = fraud_labels.sum()
    
    # Queue to store transactions for display
    display_queue = deque(maxlen=20)  # Keep last 20 interesting transactions
    
    # Track displayed counts
    whites_shown = 0
    interesting_shown = 0
    
    start_time = time.perf_counter()
    
    # Process in batches for speed
    batch_size = 1000
    processed_count = 0
    
    print(f"{Colors.CYAN}🏃 Starting batch processing...{Colors.RESET}\n")
    
    for batch_start in range(0, total_count, batch_size):
        batch_end = min(batch_start + batch_size, total_count)
        
        # Get batch data
        batch_features = feature_matrix[batch_start:batch_end]
        batch_labels = fraud_labels[batch_start:batch_end]
        batch_amounts = amounts[batch_start:batch_end]
        
        # BATCH PREDICTION - This is where the speed comes from
        batch_probs = model.predict_proba(batch_features)[:, 1]
        
        # Process batch results
        for i in range(len(batch_probs)):
            processed_count += 1
            fraud_prob = batch_probs[i]
            is_actual_fraud = batch_labels[i] == 1
            raw_amount = batch_amounts[i]
            
            is_flagged = fraud_prob > threshold
            
            # Determine transaction type
            if is_actual_fraud:
                if is_flagged:
                    # ✅ GREEN: Flagged and correct
                    color = Colors.GREEN
                    icon = "✅"
                    message = "Correct fraud detection!"
                    detected_frauds += 1
                    fraud_count += 1
                    is_interesting = True
                else:
                    # ❌ RED: Missed fraud
                    color = Colors.RED
                    icon = "❌"
                    message = "Missed actual fraud!"
                    missed_frauds += 1
                    is_interesting = True
            else:  # Not actual fraud
                if is_flagged:
                    # ⚠️ YELLOW: False alarm
                    color = Colors.YELLOW
                    icon = "⚠️"
                    message = "False alarm!"
                    false_positives += 1
                    fraud_count += 1
                    is_interesting = True
                else:
                    # ○ WHITE: Legitimate
                    color = Colors.WHITE
                    icon = "○"
                    message = ""
                    is_interesting = False
            
            # Add to display queue if interesting
            if is_interesting:
                display_queue.append({
                    'id': processed_count,
                    'color': color,
                    'icon': icon,
                    'amount': raw_amount,
                    'prob': fraud_prob,
                    'message': message,
                    'is_interesting': True
                })
                interesting_shown += 1
            elif show_mode == 'all':
                display_queue.append({
                    'id': processed_count,
                    'color': color,
                    'icon': icon,
                    'amount': raw_amount,
                    'prob': fraud_prob,
                    'message': message,
                    'is_interesting': False
                })
                whites_shown += 1
        
        # Display progress and queued transactions
        progress = processed_count / total_count * 100
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Calculate batch processing speed
        current_time = time.perf_counter()
        elapsed = current_time - start_time
        speed = processed_count / elapsed if elapsed > 0 else 0
        
        # Update progress bar
        print(f"\r{Colors.CYAN}[{bar}] {processed_count:,}/{total_count:,} | "
              f"Speed: {speed:,.0f} tx/sec | "
              f"🎯: {detected_frauds} | ❌: {missed_frauds} | ⚠️: {false_positives}{Colors.RESET}", 
              end="", flush=True)
        
        # Display queued transactions (if any)
        if display_queue:
            print()  # New line for transactions
            for tx in list(display_queue):
                # Filter based on show_mode
                if show_mode == 'all' or tx['is_interesting']:
                    display_amount = convert_to_indian_rupees(tx['amount'])
                    formatted_amount = f"₹{display_amount:,.0f}"
                    risk_percent = tx['prob'] * 100
                    
                    print(f"{tx['color']}{tx['icon']} TX-{tx['id']:04d} | "
                          f"Amount: {formatted_amount:>12} | "
                          f"Risk: {risk_percent:5.1f}% | "
                          f"{tx['message']}{Colors.RESET}")
            
            display_queue.clear()  # Clear after displaying
    
    # Final progress bar update
    end_time = time.perf_counter()
    processing_time = end_time - start_time
    final_speed = total_count / processing_time
    
    print(f"\r{Colors.CYAN}[{'█'*40}] {total_count:,}/{total_count:,} | "
          f"Speed: {final_speed:,.0f} tx/sec | "
          f"🎯: {detected_frauds} | ❌: {missed_frauds} | ⚠️: {false_positives}{Colors.RESET}")
    
    # Demo summary
    print(f"\n\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}📊 DEMO SUMMARY{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
    
    true_negatives = total_count - (detected_frauds + missed_frauds + false_positives)
    
    print(f"{Colors.CYAN}Transaction Outcomes:{Colors.RESET}")
    print(f"{Colors.WHITE if show_mode == 'all' else Colors.GRAY}○ Legitimate: {true_negatives:,}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Correct detections: {detected_frauds:,}{Colors.RESET}")
    print(f"{Colors.RED}❌ Missed frauds: {missed_frauds:,}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠️  False alarms: {false_positives:,}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}{'-'*70}{Colors.RESET}")
    
    print(f"{Colors.CYAN}Total transactions: {total_count:,}{Colors.RESET}")
    print(f"{Colors.CYAN}Transactions displayed: {whites_shown + interesting_shown:,}{Colors.RESET}")
    print(f"{Colors.CYAN}Alert rate: {(fraud_count/total_count)*100:.1f}%{Colors.RESET}")
    
    if actual_frauds_in_sample > 0:
        detection_rate = (detected_frauds / actual_frauds_in_sample * 100)
        print(f"{Colors.CYAN}Fraud detection rate: {detection_rate:.1f}%{Colors.RESET}")
    
    print(f"{Colors.CYAN}Processing speed: {final_speed:,.1f} transactions/second{Colors.RESET}")
    print(f"{Colors.CYAN}Total time: {processing_time:.3f} seconds{Colors.RESET}")
    print(f"{Colors.CYAN}Threshold: {threshold}{Colors.RESET}")
    
    # Performance note
    print(f"{Colors.GRAY}Note: Batch processing with size {batch_size}{Colors.RESET}")

def main():
    """Main function"""
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}🛡️  FRAUD DETECTION DEMO (OPTIMIZED){Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    
    # Show available models
    list_model_versions()
    
    # Model selection with v5 as default
    version_name = input(f"\n{Colors.CYAN}Model version (default v5_xg_20251109_154848): {Colors.RESET}").strip()
    if not version_name:
        version_name = "v5_xg_20251109_154848"
    
    print(f"\n{Colors.CYAN}Loading: {version_name}{Colors.RESET}")
    
    result = load_model_version(version_name)
    if result is None:
        print(f"{Colors.RED}❌ Failed to load model{Colors.RESET}")
        return
    
    model, features, performance = result
    print(f"{Colors.GREEN}✅ Loaded (AUC: {performance['roc_auc']:.3f}){Colors.RESET}")
    print(f"{Colors.CYAN}Features: {len(features['feature_names'])}{Colors.RESET}")
    
    # Load demo data
    try:
        demo_data_path = f"model_versions/{version_name}/demo_data.csv"
        demo_data = pd.read_csv(demo_data_path)
        print(f"{Colors.CYAN}Available transactions: {len(demo_data):,}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        return
    
    # Display mode selection
    print(f"\n{Colors.CYAN}Display mode:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Show ALL transactions{Colors.RESET}")
    print(f"{Colors.YELLOW}2. Interesting Only - Fraud flagged, caught, missed{Colors.RESET}")
    
    mode_choice = input(f"\n{Colors.CYAN}Choice (1 or 2, default 1): {Colors.RESET}").strip()
    show_mode = 'interesting' if mode_choice == '2' else 'all'
    
    # Transaction count (default 10,000)
    try:
        default_tx = 10000
        max_tx = int(input(f"\n{Colors.CYAN}Transactions (1-{len(demo_data):,}, default {default_tx:,}): {Colors.RESET}") or str(default_tx))
        max_tx = min(max_tx, len(demo_data))
    except:
        max_tx = default_tx
    
    # Threshold (default 0.063)
    try:
        threshold = float(input(f"{Colors.CYAN}Threshold (default 0.063): {Colors.RESET}") or "0.063")
        threshold = max(0.01, min(0.5, threshold))
    except:
        threshold = 0.063
    
    print(f"\n{Colors.CYAN}⚙️  Settings:{Colors.RESET}")
    print(f"{Colors.GRAY}   • Model: {version_name}{Colors.RESET}")
    print(f"{Colors.GRAY}   • Transactions: {max_tx:,}{Colors.RESET}")
    print(f"{Colors.GRAY}   • Threshold: {threshold}{Colors.RESET}")
    print(f"{Colors.GRAY}   • Mode: {'All transactions' if show_mode == 'all' else 'Interesting only'}{Colors.RESET}")
    print(f"{Colors.GREEN}   • Batch processing: 1000 transactions/batch{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}Press Enter to start demo...{Colors.RESET}")
    live_fraud_demo(model, features, demo_data, max_transactions=max_tx, 
                   show_mode=show_mode, threshold=threshold)

if __name__ == "__main__":
    main()