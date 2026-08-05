"""
Utility functions for configuration management
"""
import yaml
import os
from pathlib import Path


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent


def create_directories():
    """Create necessary project directories"""
    root = get_project_root()
    
    directories = [
        'data/raw',
        'data/processed',
        'models',
        'results/plots',
        'results/metrics',
        'results/reports',
        'logs',
        'documentation/reports',
        'documentation/diagrams',
    ]
    
    # Create directories for each disease
    diseases = [
        'diabetes', 'heart_disease', 'liver_disease', 'kidney_disease',
        'breast_cancer', 'parkinsons', 'stroke', 'hypertension',
        'anemia', 'thyroid'
    ]
    
    for disease in diseases:
        directories.append(f'models/{disease}')
        directories.append(f'results/plots/{disease}')
        directories.append(f'results/metrics/{disease}')
    
    for directory in directories:
        dir_path = root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print("✓ All directories created successfully")


def get_disease_config(disease_name):
    """Get configuration for a specific disease"""
    config = load_config()
    for disease in config['diseases']:
        if disease['name'] == disease_name:
            return disease
    return None


def get_model_save_path(disease_name, model_name):
    """Get path to save/load model"""
    root = get_project_root()
    return root / 'models' / disease_name / f'{model_name}.pkl'


def get_data_path(disease_name, data_type='processed'):
    """Get path to data file"""
    root = get_project_root()
    return root / 'data' / data_type / f'{disease_name}.csv'


if __name__ == "__main__":
    create_directories()
