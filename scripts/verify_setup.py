"""
Project verification and health check script
"""
import sys
from pathlib import Path
import importlib.util

project_root = Path(__file__).parent.parent


def check_directory_structure():
    """Verify all required directories exist"""
    print("\n📁 Checking Directory Structure...")
    
    required_dirs = [
        'src/preprocessing',
        'src/models',
        'src/explainability',
        'src/prediction',
        'src/utils',
        'src/visualization',
        'app',
        'scripts',
        'tests',
        'data/raw',
        'data/processed',
        'documentation/reports',
        'documentation/diagrams',
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - MISSING")
            all_exist = False
    
    return all_exist


def check_required_files():
    """Verify all required files exist"""
    print("\n📄 Checking Required Files...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'config.yaml',
        '.gitignore',
        'QUICKSTART.md',
        'src/__init__.py',
        'src/preprocessing/data_preprocessor.py',
        'src/models/model_trainer.py',
        'src/explainability/xai_engine.py',
        'src/prediction/prediction_system.py',
        'src/utils/config_utils.py',
        'src/utils/logger.py',
        'src/utils/model_utils.py',
        'app/main.py',
        'scripts/download_datasets.py',
        'scripts/train_all_diseases.py',
        'scripts/setup_project.py',
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n📦 Checking Python Packages...")
    
    required_packages = [
        'numpy',
        'pandas',
        'sklearn',
        'xgboost',
        'shap',
        'lime',
        'matplotlib',
        'seaborn',
        'streamlit',
        'yaml',
    ]
    
    all_installed = True
    for package in required_packages:
        # Handle special cases
        if package == 'sklearn':
            package_name = 'scikit-learn'
        elif package == 'yaml':
            package_name = 'pyyaml'
        else:
            package_name = package
        
        spec = importlib.util.find_spec(package)
        if spec is not None:
            print(f"  ✓ {package_name}")
        else:
            print(f"  ✗ {package_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_configuration():
    """Verify configuration file is valid"""
    print("\n⚙️  Checking Configuration...")
    
    try:
        import yaml
        config_path = project_root / 'config.yaml'
        
        if not config_path.exists():
            print("  ✗ config.yaml not found")
            return False
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['project', 'diseases', 'models', 'preprocessing', 'evaluation']
        
        for key in required_keys:
            if key in config:
                print(f"  ✓ {key} section present")
            else:
                print(f"  ✗ {key} section missing")
                return False
        
        print(f"  ✓ {len(config['diseases'])} diseases configured")
        print(f"  ✓ {len(config['models']['algorithms'])} ML algorithms configured")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error loading configuration: {e}")
        return False


def check_datasets():
    """Check if datasets exist"""
    print("\n💾 Checking Datasets...")
    
    data_dir = project_root / 'data' / 'raw'
    
    if not data_dir.exists():
        print("  ✗ data/raw directory not found")
        return False
    
    diseases = [
        'diabetes', 'heart_disease', 'liver_disease', 'kidney_disease',
        'breast_cancer', 'parkinsons', 'stroke', 'hypertension',
        'anemia', 'thyroid'
    ]
    
    datasets_found = 0
    for disease in diseases:
        dataset_path = data_dir / f'{disease}.csv'
        if dataset_path.exists():
            print(f"  ✓ {disease}.csv")
            datasets_found += 1
        else:
            print(f"  ✗ {disease}.csv - NOT FOUND")
    
    if datasets_found == 0:
        print("\n  ⚠️  No datasets found. Run: python scripts/download_datasets.py")
        return False
    elif datasets_found < len(diseases):
        print(f"\n  ⚠️  Only {datasets_found}/{len(diseases)} datasets found")
        return False
    
    return True


def check_models():
    """Check if models are trained"""
    print("\n🤖 Checking Trained Models...")
    
    models_dir = project_root / 'models'
    
    if not models_dir.exists():
        print("  ✗ models directory not found")
        return False
    
    diseases = [
        'diabetes', 'heart_disease', 'liver_disease', 'kidney_disease',
        'breast_cancer', 'parkinsons', 'stroke', 'hypertension',
        'anemia', 'thyroid'
    ]
    
    models_found = 0
    for disease in diseases:
        disease_dir = models_dir / disease
        if disease_dir.exists() and any(disease_dir.glob('*.pkl')):
            print(f"  ✓ {disease}")
            models_found += 1
        else:
            print(f"  ✗ {disease} - NO MODELS")
    
    if models_found == 0:
        print("\n  ⚠️  No models found. Run: python scripts/train_all_diseases.py")
        return False
    elif models_found < len(diseases):
        print(f"\n  ⚠️  Only {models_found}/{len(diseases)} diseases trained")
        return False
    
    return True


def print_summary(checks):
    """Print verification summary"""
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    total = len(checks)
    passed = sum(checks.values())
    failed = total - passed
    
    print(f"\nTotal Checks: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    
    if failed == 0:
        print("\n🎉 All checks passed! Project is ready.")
        print("\nNext steps:")
        print("  1. Train models (if not done): python scripts/train_all_diseases.py")
        print("  2. Start app: streamlit run app/main.py")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        
        if not checks['packages']:
            print("\nTo install packages: pip install -r requirements.txt")
        
        if not checks['datasets']:
            print("To download datasets: python scripts/download_datasets.py")
        
        if not checks['models']:
            print("To train models: python scripts/train_all_diseases.py")
    
    print("\n" + "="*60)
    
    return failed == 0


def main():
    """Main verification function"""
    print("="*60)
    print("MULTI-DISEASE PREDICTION SYSTEM")
    print("Project Verification & Health Check")
    print("="*60)
    
    checks = {
        'directories': check_directory_structure(),
        'files': check_required_files(),
        'packages': check_python_packages(),
        'configuration': check_configuration(),
        'datasets': check_datasets(),
        'models': check_models(),
    }
    
    success = print_summary(checks)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
