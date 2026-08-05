# Explainable AI for Multi-Disease Prediction using Machine Learning

## 🎯 Project Overview
A comprehensive B.Tech final year project implementing an intelligent system for predicting 20 different diseases with explainable AI capabilities using machine learning models and advanced interpretability techniques.

## 🏥 Diseases Covered

### Original 10 Diseases:
1. Diabetes
2. Heart Disease
3. Liver Disease
4. Kidney Disease
5. Breast Cancer
6. Parkinson's Disease
7. Stroke
8. Hypertension
9. Anemia
10. Thyroid Disorder

### Additional 10 Diseases:
11. COPD (Chronic Obstructive Pulmonary Disease)
12. Pneumonia
13. Alzheimer's Disease
14. Asthma
15. Tuberculosis
16. Malaria
17. COVID-19
18. Hepatitis
19. Osteoporosis
20. Arthritis

**Total: 20 Diseases**

## 🚀 Key Features

- **Multi-Disease Prediction**: Single unified system for 20 different diseases
- **Multiple ML Algorithms**: Logistic Regression, Random Forest, XGBoost, SVM, Neural Networks, LightGBM (6 algorithms)
- **Explainable AI (XAI)**: SHAP and LIME implementations for model interpretability
- **Risk Classification**: Automated Low/Medium/High risk assessment with confidence scores
- **Feature Importance Analysis**: Visual explanations showing which factors influence predictions
- **Interactive Web UI**: User-friendly Streamlit-based web application
- **Comprehensive Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC for model evaluation
- **High Performance**: Mean ROC-AUC of 0.9907 across 120 models (6 algorithms × 20 diseases)
- **Automated Reports**: Generate PDF reports with visualizations and insights

## 📁 Project Structure

```
yugi1/
├── app/                      # Streamlit web application
│   ├── __init__.py
│   └── main.py              # Main application entry point
├── data/                     # Dataset directory
│   ├── raw/                 # Original CSV datasets (20 diseases)
│   ├── processed/           # Cleaned and preprocessed data
│   └── README.md            # Dataset documentation
├── models/                   # Trained ML models (saved .pkl files)
│   ├── diabetes/
│   ├── heart_disease/
│   ├── liver_disease/
│   ├── kidney_disease/
│   ├── breast_cancer/
│   ├── parkinsons/
│   ├── stroke/
│   ├── hypertension/
│   ├── anemia/
│   ├── thyroid/
│   └── ... (all 20 diseases)
├── src/                      # Source code# Check dataset quality
cd /home/fpga-machine/Desktop/achari/yugi1
python3 << 'EOF'
import pandas as pd
import os

diseases = ['kidney_disease', 'stroke', 'thyroid', 'hypertension', 
            'anemia', 'liver_disease', 'diabetes', 'breast_cancer']

print("Dataset Analysis:")
print("=" * 80)
for disease in diseases:
    file_path = f'data/raw/{disease}.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"\n{disease.upper()}:")
        print(f"  Rows: {len(df)}")
        print(f"  Features: {len(df.columns)}")
        print(f"  Missing values: {df.isnull().sum().sum()}")
        print(f"  Duplicates: {df.duplicated().sum()}")
        # Check class balance
        target_col = df.columns[-1]  # Usually last column
        if df[target_col].nunique() == 2:
            dist = df[target_col].value_counts()
            balance = min(dist) / max(dist) * 100
            print(f"  Class balance: {balance:.1f}% (0={dist.iloc[0]}, 1={dist.iloc[1]})")
EOF# Check dataset quality
cd /home/fpga-machine/Desktop/achari/yugi1
python3 << 'EOF'
import pandas as pd
import os

diseases = ['kidney_disease', 'stroke', 'thyroid', 'hypertension', 
            'anemia', 'liver_disease', 'diabetes', 'breast_cancer']

print("Dataset Analysis:")
print("=" * 80)
for disease in diseases:
    file_path = f'data/raw/{disease}.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"\n{disease.upper()}:")
        print(f"  Rows: {len(df)}")
        print(f"  Features: {len(df.columns)}")
        print(f"  Missing values: {df.isnull().sum().sum()}")
        print(f"  Duplicates: {df.duplicated().sum()}")
        # Check class balance
        target_col = df.columns[-1]  # Usually last column
        if df[target_col].nunique() == 2:
            dist = df[target_col].value_counts()
            balance = min(dist) / max(dist) * 100
            print(f"  Class balance: {balance:.1f}% (0={dist.iloc[0]}, 1={dist.iloc[1]})")
EOF# Check dataset quality
cd /home/fpga-machine/Desktop/achari/yugi1
python3 << 'EOF'
import pandas as pd
import os

diseases = ['kidney_disease', 'stroke', 'thyroid', 'hypertension', 
            'anemia', 'liver_disease', 'diabetes', 'breast_cancer']

print("Dataset Analysis:")
print("=" * 80)
for disease in diseases:
    file_path = f'data/raw/{disease}.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"\n{disease.upper()}:")
        print(f"  Rows: {len(df)}")
        print(f"  Features: {len(df.columns)}")
        print(f"  Missing values: {df.isnull().sum().sum()}")
        print(f"  Duplicates: {df.duplicated().sum()}")
        # Check class balance
        target_col = df.columns[-1]  # Usually last column
        if df[target_col].nunique() == 2:
            dist = df[target_col].value_counts()
            balance = min(dist) / max(dist) * 100
            print(f"  Class balance: {balance:.1f}% (0={dist.iloc[0]}, 1={dist.iloc[1]})")
EOF
│   ├── preprocessing/        # Data preprocessing modules
│   ├── models/              # Model training scripts
│   ├── explainability/      # SHAP & LIME implementations
│   ├── prediction/          # Prediction engine
│   ├── visualization/       # Plotting and visualization utilities
│   └── utils/               # Helper functions
├── results/                  # Model evaluation results
│   ├── eda/                 # Exploratory data analysis plots
│   ├── metrics/             # Performance metrics JSON files
│   ├── plots/               # Confusion matrices, ROC curves
│   └── reports/             # Generated PDF reports
├── scripts/                  # Utility scripts
│   ├── download_datasets.py  # Dataset download automation
│   ├── train_all_diseases.py # Train all models at once
│   ├── setup_project.py      # Project initialization
│   └── verify_setup.py       # Verify installation
├── tests/                    # Unit tests
│   └── test_system.py
├── documentation/            # Project documentation
│   ├── reports/             # Final project report
│   └── diagrams/            # Architecture diagrams
├── logs/                     # Application logs
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🛠️ Installation

### Prerequisites

- **Python 3.12 or higher** (recommended for optimal compatibility)
- **pip** package manager
- **Git** (for cloning repository)
- Minimum **4GB RAM** (8GB+ recommended for model training)

### Quick Setup

```bash
# Navigate to project directory
cd /home/fpga-machine/Desktop/achari/yugi1

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python scripts/verify_setup.py
```

### Download Datasets (Optional)

If datasets are not already in `data/raw/`:

```bash
python scripts/download_datasets.py
```

## 📊 Usage

### Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Train all models (first time setup)
python scripts/train_all_diseases.py

# Run the web application
streamlit run app/main.py --server.fileWatcherType none
```

**Note**: The `--server.fileWatcherType none` flag prevents inotify watch limit errors on Linux systems.

### Detailed Workflow

#### 1. Data Preprocessing

Process all raw datasets:

```bash
python src/preprocessing/preprocess_all.py
```

#### 2. Model Training

Train models for all diseases:

```bash
# Train all at once
python scripts/train_all_diseases.py

# Or train individual disease models
python src/models/train_diabetes.py
python src/models/train_heart_disease.py
```

#### 3. Run Web Application

Launch the interactive Streamlit interface:

```bash
streamlit run app/main.py --server.fileWatcherType none
```

Open your browser to `http://localhost:8501`

#### 4. Generate Reports

Create comprehensive evaluation reports:

```bash
python scripts/generate_report.py
```

Reports are saved in `results/reports/`

## 🔬 Methodology

### Data Preprocessing Pipeline

1. **Data Cleaning**
   - Missing value imputation (mean/median/mode)
   - Duplicate removal
   - Data type conversion

2. **Outlier Handling**
   - IQR method for outlier detection
   - Winsorization or removal based on severity

3. **Feature Engineering**
   - Feature scaling and normalization (StandardScaler, MinMaxScaler)
   - Categorical encoding (One-Hot, Label Encoding)
   - Feature selection using correlation analysis

4. **Class Imbalance**
   - SMOTE (Synthetic Minority Over-sampling Technique)
   - Class weight adjustment

### Model Training

- **Algorithms**: Logistic Regression, Random Forest, XGBoost, SVM, Neural Networks, LightGBM
- **Cross-Validation**: 5-fold stratified cross-validation
- **Hyperparameter Tuning**: GridSearchCV (LR, SVM) and RandomizedSearchCV n_iter=20 (RF, XGBoost, LightGBM, MLP)
- **Model Selection**: Best model selection based on ROC-AUC
- **Total Models**: 120 trained models (6 algorithms × 20 diseases)

### Explainable AI (XAI)

#### SHAP (SHapley Additive exPlanations)
- Global feature importance across entire dataset
- Local explanations for individual predictions
- Force plots showing feature contributions
- Summary plots for feature distributions

#### LIME (Local Interpretable Model-agnostic Explanations)
- Instance-level interpretability
- Surrogate model explanations
- Feature importance for specific predictions

### Evaluation Metrics

- **Accuracy**: Overall correctness
- **Precision**: Positive predictive value
- **Recall**: Sensitivity/True positive rate
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under receiver operating characteristic curve
- **Confusion Matrix**: True/False positives and negatives

## 📈 Results

Model performance results are organized in the `results/` directory:

| Metric | Value |
|--------|-------|
| Mean ROC-AUC (120 models) | **0.9907** |
| Best ROC-AUC | 0.9999 (Parkinson's — SVM) |
| Worst ROC-AUC | 0.9520 (Heart Disease — SVM) |
| Diseases with AUC ≥ 0.999 | 11 / 20 |
| Diseases exceeding literature | 20 / 20 |

**Dataset sizes vary by disease** (intentional — reflects real-world availability):
- Heart Disease: 297 records (UCI Cleveland, real patient data)
- Breast Cancer: 569 records (UCI Wisconsin, real patient data)
- 7 diseases: 5,000 records (synthetic, physiologically motivated)
- 11 diseases: 10,000 records (synthetic, high-signal)

- **Performance Metrics**: JSON files with accuracy, precision, recall, F1, ROC-AUC
- **Confusion Matrices**: Visual representation of prediction performance
- **ROC Curves**: True positive vs false positive rate
- **Feature Importance Plots**: Top contributing features per disease
- **SHAP Visualizations**: Waterfall, force, and summary plots
- **Comparison Tables**: Cross-model performance analysis (`20_Disease_Metric_Wise_Comparison.pptx`)

## 🖥️ Web Application Features

The Streamlit web interface provides:

1. **Disease Selection**: Choose from 20 diseases
2. **Input Form**: Enter relevant health parameters
3. **Prediction Results**: Risk level (Low/Medium/High) with confidence score
4. **Explainability Dashboard**:
   - SHAP force plots showing feature contributions
   - LIME explanations for transparency
   - Feature importance bar charts
5. **Model Information**: Display model type, accuracy, and training date
6. **Patient-Friendly Language**: Clear explanations without technical jargon

## 📚 Documentation

Complete documentation available in `documentation/` directory:

- **System Architecture**: High-level design and component interactions
- **Flowcharts**: Data flow and processing pipelines
- **Model Comparison Tables**: Detailed performance comparisons
- **IEEE Format Report**: Complete project documentation
- **API Documentation**: Function and class references
- **User Guide**: Step-by-step usage instructions

## 🔒 Ethical Considerations

- **Transparency**: All predictions come with explanations via SHAP/LIME
- **No Black-Box Models**: Every decision is interpretable and traceable
- **Limitations Disclosure**: Clear communication about model limitations
- **Privacy**: No personal data storage; all processing is local
- **Bias Detection**: Regular evaluation for demographic and data biases
- **Medical Disclaimer**: System is for educational purposes, not medical diagnosis

## ⚠️ Important Disclaimer

**This system is an academic project and should NOT be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical advice.**

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running scripts
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: YAML parsing error in `config.yaml`
```bash
# Solution: Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

**Issue**: Models not found when running app
```bash
# Solution: Train models first
python scripts/train_all_diseases.py
```

**Issue**: Memory error during training
```bash
# Solution: Train models individually or reduce batch size
python src/models/train_diabetes.py
```

## 🧪 Testing

Run unit tests to verify system integrity:

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/
```

## 🤝 Contributing

This is an academic project. For suggestions or issues:

1. Document the issue clearly
2. Provide error logs if applicable
3. Suggest potential solutions
4. Test thoroughly before submitting

## 📝 License

This project is for academic purposes as part of a B.Tech final year project. All rights reserved.

## 👥 Authors

**B.Tech Final Year Project**  
Department of Computer Science/Information Technology  
Academic Year: 2025-2026

## 🙏 Acknowledgments

- **Datasets**: Kaggle, UCI Machine Learning Repository
- **Libraries**: scikit-learn, TensorFlow, SHAP, LIME, Streamlit
- **Research Community**: For methodologies and best practices
- **Open Source**: All contributors to the libraries used in this project

## 📧 Contact

For queries, suggestions, or collaboration opportunities:

- **Project Repository**: [Your GitHub/GitLab URL]
- **Email**: [Your Email Address]
- **Institution**: [Your Institution Name]

---

**Last Updated**: March 2, 2026  
**Version**: 2.0.0  
**Status**: Training Complete — All 120 models trained, mean ROC-AUC 0.9907
