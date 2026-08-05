#!/bin/bash
# Start the Streamlit web application

echo "Starting Multi-Disease Prediction System..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if models exist
if [ ! -d "models" ] || [ -z "$(ls -A models 2>/dev/null)" ]; then
    echo "⚠️  Warning: Models not found!"
    echo "Please train the models first:"
    echo "  python scripts/train_all_diseases.py"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start Streamlit app
echo "Opening web application..."
echo "The app will open in your default browser."
echo "Press Ctrl+C to stop the server."
echo ""

streamlit run app/main.py
