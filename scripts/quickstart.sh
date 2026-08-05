#!/bin/bash
# Quick start script for the Multi-Disease Prediction System

echo "=============================================="
echo "Multi-Disease Prediction System - Quick Start"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed" ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/installed
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Create directories
echo "Creating project directories..."
python scripts/setup_project.py

# Download datasets
if [ ! -d "data/raw" ] || [ -z "$(ls -A data/raw)" ]; then
    echo "Downloading datasets..."
    python scripts/download_datasets.py
else
    echo "✓ Datasets already exist"
fi

# Check if models are trained
if [ ! -d "models" ] || [ -z "$(ls -A models 2>/dev/null)" ]; then
    echo ""
    echo "Models not found. Would you like to train them now?"
    echo "This may take 30-60 minutes depending on your system."
    read -p "Train models? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Training models..."
        python scripts/train_all_diseases.py
    else
        echo "Skipping model training. You can train later with:"
        echo "  python scripts/train_all_diseases.py"
    fi
else
    echo "✓ Models already trained"
fi

# Generate diagrams
echo "Generating system diagrams..."
python scripts/generate_diagrams.py

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "To start the web application, run:"
echo "  streamlit run app/main.py"
echo ""
echo "Or use the start script:"
echo "  ./scripts/start_app.sh"
echo ""
echo "For more information, see README.md"
echo ""
