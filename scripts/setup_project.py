"""
Complete project setup script
"""
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_utils import create_directories

logger = setup_logger('setup', 'logs/setup.log')


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✓ Python version is compatible")
    return True


def create_project_directories():
    """Create all necessary directories"""
    print_header("Creating Project Directories")
    
    try:
        create_directories()
        print("✓ All directories created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating directories: {e}")
        return False


def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    requirements_file = project_root / 'requirements.txt'
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)])
        print("✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def download_datasets():
    """Download/create sample datasets"""
    print_header("Downloading Datasets")
    
    download_script = project_root / 'scripts' / 'download_datasets.py'
    
    if not download_script.exists():
        print("❌ Download script not found")
        return False
    
    try:
        subprocess.check_call([sys.executable, str(download_script)])
        print("✓ Datasets downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading datasets: {e}")
        return False


def create_init_files():
    """Create __init__.py files for Python packages"""
    print_header("Creating Package Init Files")
    
    packages = [
        'src',
        'src/preprocessing',
        'src/models',
        'src/explainability',
        'src/prediction',
        'src/utils',
        'src/visualization',
        'app',
        'scripts'
    ]
    
    for package in packages:
        init_file = project_root / package / '__init__.py'
        init_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not init_file.exists():
            init_file.touch()
    
    print("✓ All __init__.py files created")
    return True


def display_next_steps():
    """Display next steps for the user"""
    print_header("Setup Complete!")
    
    print("🎉 Project setup completed successfully!\n")
    print("Next Steps:\n")
    print("1. Train Models:")
    print("   python scripts/train_all_diseases.py\n")
    print("2. Run Web Application:")
    print("   streamlit run app/main.py\n")
    print("3. Generate Reports:")
    print("   python src/visualization/report_generator.py\n")
    print("4. Generate Visualizations:")
    print("   python src/visualization/visualizer.py\n")
    print("\nFor more information, see README.md")
    print("\n" + "=" * 70 + "\n")


def main():
    """Main setup function"""
    print_header("Multi-Disease Prediction System Setup")
    print("B.Tech Final Year Project")
    print("Explainable AI for Multi-Disease Prediction\n")
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating directories", create_project_directories),
        ("Creating package files", create_init_files),
        ("Installing dependencies", install_dependencies),
        ("Downloading datasets", download_datasets),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Unexpected error in {step_name}: {e}")
            failed_steps.append(step_name)
    
    if failed_steps:
        print_header("Setup Failed")
        print("The following steps failed:")
        for step in failed_steps:
            print(f"  ❌ {step}")
        print("\nPlease fix the errors and run setup again.")
        return False
    
    display_next_steps()
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
