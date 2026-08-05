"""
Utility functions for model operations
"""
import joblib
import json
import numpy as np
from pathlib import Path


def save_model(model, filepath):
    """Save model to disk"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)
    print(f"✓ Model saved to {filepath}")


def load_model(filepath):
    """Load model from disk"""
    return joblib.load(filepath)


def save_metrics(metrics, filepath):
    """Save metrics to JSON file"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy types to Python types
    metrics_serializable = {}
    for key, value in metrics.items():
        if isinstance(value, (np.integer, np.floating)):
            metrics_serializable[key] = float(value)
        elif isinstance(value, np.ndarray):
            metrics_serializable[key] = value.tolist()
        else:
            metrics_serializable[key] = value
    
    with open(filepath, 'w') as f:
        json.dump(metrics_serializable, f, indent=4)
    
    print(f"✓ Metrics saved to {filepath}")


def load_metrics(filepath):
    """Load metrics from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def get_risk_level(probability, thresholds={'low': [0.0, 0.3], 'medium': [0.3, 0.7], 'high': [0.7, 1.0]}):
    """
    Classify probability into risk levels
    
    Args:
        probability: Model prediction probability
        thresholds: Dictionary with risk level thresholds
    
    Returns:
        Risk level (Low/Medium/High)
    """
    if probability < thresholds['medium'][0]:
        return "Low"
    elif probability < thresholds['high'][0]:
        return "Medium"
    else:
        return "High"
