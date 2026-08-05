#!/usr/bin/env python3
"""
Monitor max-performance training progress.
Usage:  python3 check_max_training.py
"""
import json
from pathlib import Path

project_root = Path(__file__).parent
metrics_root = project_root / 'results' / 'metrics'

ALL_DISEASES = [
    'copd','breast_cancer','liver_disease','hypertension','thyroid',
    'diabetes','stroke','anemia','heart_disease',
    'kidney_disease','parkinsons','pneumonia','alzheimers','asthma',
    'tuberculosis','malaria','hepatitis','osteoporosis','arthritis','covid19',
]

print(f"\n{'='*68}")
print(f"  MAX-PERFORMANCE TRAINING PROGRESS")
print(f"{'='*68}")
print(f"  {'Disease':<22} {'Best Model':<22} {'AUC':>8}  {'Status'}")
print(f"  {'-'*62}")

done, pending = 0, 0
auc_sum = 0.0

for disease in ALL_DISEASES:
    best_file = metrics_root / disease / 'best_model.json'
    if best_file.exists():
        data = json.loads(best_file.read_text())
        model = data.get('best_model', '?')
        auc   = data.get('best_score', 0.0)
        tag   = '✅ DONE' if auc >= 0.990 else ('⚠️  GOOD' if auc >= 0.950 else '❌ LOW')
        print(f"  {disease:<22} {model:<22} {auc:>8.4f}  {tag}")
        done += 1
        auc_sum += auc
    else:
        print(f"  {disease:<22} {'—':<22} {'—':>8}  ⏳ pending")
        pending += 1

print(f"\n  Completed : {done}/20")
print(f"  Pending   : {pending}/20")
if done:
    print(f"  Avg AUC   : {auc_sum/done:.4f}")

# Tail of training log
log_file = project_root / 'logs' / 'train_max_all_diseases.log'
if log_file.exists():
    lines = log_file.read_text().splitlines()
    print(f"\n  Last log lines ({log_file.name}):")
    for l in lines[-8:]:
        print(f"    {l}")
print(f"{'='*68}\n")
