#!/bin/bash

# Complete Installation and Setup Guide
# Multi-Disease Prediction System

echo "================================================================"
echo "  MULTI-DISEASE PREDICTION SYSTEM"
echo "  Complete Installation and Setup"
echo "  B.Tech Final Year Project"
echo "================================================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if running from project root
if [ ! -f "config.yaml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Running from correct directory"
echo ""

# Step 1: Check Python version
echo "Step 1: Checking Python Version"
echo "--------------------------------"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
print_info "Python version: $python_version"

required_version="3.8"
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python version is compatible"
else
    print_error "Python 3.8 or higher is required"
    exit 1
fi
echo ""

# Step 2: Create virtual environment
echo "Step 2: Setting Up Virtual Environment"
echo "--------------------------------------"
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Recreate it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_status "Virtual environment recreated"
    fi
else
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"
echo ""

# Step 3: Upgrade pip
echo "Step 3: Upgrading pip"
echo "--------------------"
pip install --upgrade pip --quiet
print_status "pip upgraded"
echo ""

# Step 4: Install dependencies
echo "Step 4: Installing Dependencies"
echo "-------------------------------"
print_info "This may take 5-10 minutes..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    print_status "All dependencies installed"
else
    print_error "Error installing dependencies"
    exit 1
fi
echo ""

# Step 5: Create directories
echo "Step 5: Creating Project Directories"
echo "------------------------------------"
python scripts/setup_project.py
if [ $? -eq 0 ]; then
    print_status "All directories created"
else
    print_error "Error creating directories"
    exit 1
fi
echo ""

# Step 6: Download datasets
echo "Step 6: Downloading Datasets"
echo "---------------------------"
if [ -d "data/raw" ] && [ "$(ls -A data/raw)" ]; then
    print_warning "Datasets already exist"
    read -p "Re-download? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python scripts/download_datasets.py
        print_status "Datasets downloaded"
    fi
else
    python scripts/download_datasets.py
    print_status "Datasets downloaded"
fi
echo ""

# Step 7: Generate diagrams
echo "Step 7: Generating Documentation"
echo "--------------------------------"
python scripts/generate_diagrams.py
print_status "System diagrams generated"
echo ""

# Step 8: Verify setup
echo "Step 8: Verifying Installation"
echo "------------------------------"
python scripts/verify_setup.py
echo ""

# Step 9: Training prompt
echo "Step 9: Model Training (Optional)"
echo "--------------------------------"
if [ -d "models" ] && [ "$(ls -A models 2>/dev/null)" ]; then
    print_warning "Models already trained"
else
    print_info "Models need to be trained before using the system"
    print_info "Training typically takes 30-60 minutes"
    echo ""
    read -p "Train models now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        print_info "Starting model training..."
        python scripts/train_all_diseases.py
        if [ $? -eq 0 ]; then
            print_status "Model training completed"
        else
            print_error "Model training failed"
        fi
    else
        print_info "You can train models later with:"
        print_info "  python scripts/train_all_diseases.py"
    fi
fi
echo ""

# Final summary
echo "================================================================"
echo "  INSTALLATION COMPLETE!"
echo "================================================================"
echo ""
print_status "Project is ready to use"
echo ""
echo "Next Steps:"
echo "-----------"
echo ""
echo "1. ${GREEN}Train Models${NC} (if not done):"
echo "   python scripts/train_all_diseases.py"
echo ""
echo "2. ${GREEN}Start Web Application${NC}:"
echo "   streamlit run app/main.py"
echo "   ${BLUE}or${NC}"
echo "   ./scripts/start_app.sh"
echo ""
echo "3. ${GREEN}Generate Reports${NC}:"
echo "   python src/visualization/report_generator.py"
echo ""
echo "4. ${GREEN}Run Tests${NC}:"
echo "   python tests/test_system.py"
echo ""
echo "Documentation:"
echo "-------------"
echo "- README.md           - Main documentation"
echo "- QUICKSTART.md       - Quick reference guide"
echo "- PROJECT_SUMMARY.md  - Project overview"
echo "- documentation/      - Detailed documentation"
echo ""
echo "================================================================"
echo ""
print_info "For help, see README.md or QUICKSTART.md"
echo ""
