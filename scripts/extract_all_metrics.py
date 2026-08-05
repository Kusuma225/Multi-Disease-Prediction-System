#!/usr/bin/env python3
"""
Extract all metrics from training log file - ALL DISEASES
"""
import re
import sys

log_file = 'logs/fast_training_20260219_213929.log'

# Read log file
try:
    with open(log_file, 'r') as f:
        content = f.read()
except Exception as e:
    print(f"Error reading log: {e}")
    sys.exit(1)

# Parse metrics
diseases = {}
current_disease = None

lines = content.split('\n')
current_algorithm = None

for line in lines:
    # Detect disease name
    if 'Training models for:' in line:
        match = re.search(r'Training models for:\s+(.+)', line)
        if match:
            current_disease = match.group(1).strip()
            if current_disease not in diseases:
                diseases[current_disease] = {}
            current_algorithm = None  # Reset algorithm when new disease starts
    
    # Detect algorithm name (format: "Training logistic_regression...")
    if 'Training' in line and '...' in line and current_disease:
        match = re.search(r'Training ([a-z_]+)\.\.\.', line)
        if match:
            current_algorithm = match.group(1).strip()
            if current_algorithm not in diseases[current_disease]:
                diseases[current_disease][current_algorithm] = {}
    
    # Extract metrics - only if we have a current disease and algorithm
    if current_disease and current_algorithm:
        if 'Accuracy:' in line:
            match = re.search(r'Accuracy:\s+([\d.]+)', line)
            if match:
                diseases[current_disease][current_algorithm]['Accuracy'] = float(match.group(1))
        
        if 'Precision:' in line:
            match = re.search(r'Precision:\s+([\d.]+)', line)
            if match:
                diseases[current_disease][current_algorithm]['Precision'] = float(match.group(1))
        
        if 'Recall:' in line:
            match = re.search(r'Recall:\s+([\d.]+)', line)
            if match:
                diseases[current_disease][current_algorithm]['Recall'] = float(match.group(1))
        
        if 'F1-Score:' in line:
            match = re.search(r'F1-Score:\s+([\d.]+)', line)
            if match:
                diseases[current_disease][current_algorithm]['F1-Score'] = float(match.group(1))
        
        if 'ROC-AUC:' in line:
            match = re.search(r'ROC-AUC:\s+([\d.]+)', line)
            if match:
                diseases[current_disease][current_algorithm]['ROC-AUC'] = float(match.group(1))

# Print comprehensive results
print("=" * 120)
print("FINAL TRAINING RESULTS - ALL 20 DISEASES")
print("=" * 120)
print()

for disease, algos in diseases.items():
    if not algos:
        continue
    
    print(f"\n{'='*120}")
    print(f"DISEASE: {disease.upper()}")
    print(f"{'='*120}")
    print(f"{'Algorithm':<20} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1-Score':>10} {'ROC-AUC':>10}")
    print("-" * 120)
    
    best_auc = 0
    best_algo = None
    
    for algo, metrics in algos.items():
        if not metrics:
            continue
        
        acc = metrics.get('Accuracy', 0)
        prec = metrics.get('Precision', 0)
        rec = metrics.get('Recall', 0)
        f1 = metrics.get('F1-Score', 0)
        auc = metrics.get('ROC-AUC', 0)
        
        if auc > best_auc:
            best_auc = auc
            best_algo = algo
        
        print(f"{algo:<20} {acc:>10.4f} {prec:>10.4f} {rec:>10.4f} {f1:>10.4f} {auc:>10.4f}")
    
    if best_algo:
        print("-" * 120)
        print(f"✅ BEST MODEL: {best_algo} (ROC-AUC: {best_auc:.4f})")

# Summary statistics
print("\n" + "=" * 120)
print("SUMMARY STATISTICS")
print("=" * 120)

all_aucs = []
all_accs = []

for disease, algos in diseases.items():
    best_auc = 0
    best_acc = 0
    for algo, metrics in algos.items():
        auc = metrics.get('ROC-AUC', 0)
        acc = metrics.get('Accuracy', 0)
        if auc > best_auc:
            best_auc = auc
        if acc > best_acc:
            best_acc = acc
    
    if best_auc > 0:
        all_aucs.append(best_auc)
        all_accs.append(best_acc)

if all_aucs:
    print(f"\nTotal Diseases Trained: {len(diseases)}")
    print(f"Average Best ROC-AUC: {sum(all_aucs)/len(all_aucs):.4f}")
    print(f"Average Best Accuracy: {sum(all_accs)/len(all_accs):.4f}")
    print(f"Highest ROC-AUC: {max(all_aucs):.4f}")
    print(f"Lowest ROC-AUC: {min(all_aucs):.4f}")
    
    # Count high performers
    excellent = sum(1 for auc in all_aucs if auc >= 0.90)
    good = sum(1 for auc in all_aucs if 0.80 <= auc < 0.90)
    fair = sum(1 for auc in all_aucs if 0.70 <= auc < 0.80)
    poor = sum(1 for auc in all_aucs if auc < 0.70)
    
    print(f"\nPerformance Distribution:")
    print(f"  Excellent (AUC ≥ 0.90): {excellent} diseases")
    print(f"  Good (0.80 ≤ AUC < 0.90): {good} diseases")
    print(f"  Fair (0.70 ≤ AUC < 0.80): {fair} diseases")
    print(f"  Poor (AUC < 0.70): {poor} diseases")

print("\n" + "=" * 120)
