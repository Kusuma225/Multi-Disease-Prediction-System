"""
Generate system architecture diagram using ASCII art
"""
from pathlib import Path


def generate_architecture_diagram():
    """Generate system architecture diagram"""
    
    diagram = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                  MULTI-DISEASE PREDICTION SYSTEM ARCHITECTURE                ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                              USER INTERFACE LAYER                            │
    │                                                                              │
    │  ┌────────────────────────────────────────────────────────────────────────┐ │
    │  │                      Streamlit Web Application                         │ │
    │  │  - Patient Data Input Forms                                            │ │
    │  │  - Disease Selection                                                   │ │
    │  │  - Visualization Dashboard                                             │ │
    │  │  - Explanation Display                                                 │ │
    │  └────────────────────────────────────────────────────────────────────────┘ │
    └──────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                           PREDICTION ENGINE LAYER                            │
    │                                                                              │
    │  ┌────────────────────────────────────────────────────────────────────────┐ │
    │  │              Multi-Disease Prediction System                           │ │
    │  │                                                                        │ │
    │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │ │
    │  │  │   Diabetes   │  │ Heart Disease│  │Liver Disease │  ...           │ │
    │  │  │   Predictor  │  │  Predictor   │  │  Predictor   │                │ │
    │  │  └──────────────┘  └──────────────┘  └──────────────┘                │ │
    │  │         │                  │                  │                        │ │
    │  │         └──────────────────┴──────────────────┘                        │ │
    │  │                            │                                           │ │
    │  │                            ▼                                           │ │
    │  │              ┌──────────────────────────┐                              │ │
    │  │              │  Risk Classification     │                              │ │
    │  │              │  (Low/Medium/High)       │                              │ │
    │  │              └──────────────────────────┘                              │ │
    │  └────────────────────────────────────────────────────────────────────────┘ │
    └──────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                       EXPLAINABILITY (XAI) LAYER                             │
    │                                                                              │
    │  ┌─────────────────────────────┐    ┌─────────────────────────────┐        │
    │  │  SHAP (Global + Local)      │    │  LIME (Local Explanations)  │        │
    │  │  - Feature Importance       │    │  - Instance-level           │        │
    │  │  - Summary Plots            │    │  - Model-agnostic           │        │
    │  │  - Waterfall Plots          │    │  - Local Approximation      │        │
    │  │  - Dependence Plots         │    │  - Feature Contribution     │        │
    │  └─────────────────────────────┘    └─────────────────────────────┘        │
    └──────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                            MODEL LAYER                                       │
    │                                                                              │
    │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
    │  │   Logistic     │  │  Random Forest │  │    XGBoost     │               │
    │  │  Regression    │  │                │  │                │               │
    │  └────────────────┘  └────────────────┘  └────────────────┘               │
    │                                                                              │
    │  ┌────────────────┐  ┌────────────────┐                                    │
    │  │      SVM       │  │ Neural Network │                                    │
    │  │                │  │     (MLP)      │                                    │
    │  └────────────────┘  └────────────────┘                                    │
    │                                                                              │
    │                  Model Selection (Best for each disease)                    │
    └──────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                      DATA PREPROCESSING LAYER                                │
    │                                                                              │
    │  ┌────────────────────────────────────────────────────────────────────────┐ │
    │  │                    Data Preprocessor                                   │ │
    │  │                                                                        │ │
    │  │  • Missing Value Imputation    • Feature Encoding                     │ │
    │  │  • Outlier Detection/Handling  • Feature Scaling                      │ │
    │  │  • Duplicate Removal           • Class Imbalance (SMOTE)              │ │
    │  └────────────────────────────────────────────────────────────────────────┘ │
    └──────────────────────────────────┬──────────────────────────────────────────┘
                                       │
                                       ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                            DATA LAYER                                        │
    │                                                                              │
    │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐ │
    │  │ Diabetes  │  │   Heart   │  │   Liver   │  │  Kidney   │  │  Breast  │ │
    │  │  Dataset  │  │  Disease  │  │  Disease  │  │  Disease  │  │  Cancer  │ │
    │  └───────────┘  └───────────┘  └───────────┘  └───────────┘  └──────────┘ │
    │                                                                              │
    │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐ │
    │  │Parkinsons │  │  Stroke   │  │Hypertension│ │   Anemia  │  │ Thyroid  │ │
    │  │  Dataset  │  │  Dataset  │  │  Dataset   │ │  Dataset  │  │ Dataset  │ │
    │  └───────────┘  └───────────┘  └───────────┘  └───────────┘  └──────────┘ │
    └─────────────────────────────────────────────────────────────────────────────┘

    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                              DATA FLOW                                       ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

    1. User Input → Web Interface
    2. Input Validation → Preprocessing
    3. Feature Engineering → Preprocessed Data
    4. Model Prediction → Probability Score
    5. Risk Classification → Low/Medium/High
    6. XAI Analysis → Feature Importance
    7. Explanation Generation → Human-readable Text
    8. Result Display → User Interface

    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                          TECHNOLOGY STACK                                    ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

    • Machine Learning: scikit-learn, XGBoost, TensorFlow/Keras
    • Explainability: SHAP, LIME
    • Data Processing: NumPy, Pandas
    • Visualization: Matplotlib, Seaborn, Plotly
    • Web Framework: Streamlit
    • Model Persistence: Joblib, Pickle
    """
    
    return diagram


def generate_workflow_diagram():
    """Generate workflow flowchart"""
    
    flowchart = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                     TRAINING WORKFLOW FLOWCHART                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

                                    ┌────────────┐
                                    │   START    │
                                    └──────┬─────┘
                                           │
                                           ▼
                                    ┌────────────┐
                                    │Load Dataset│
                                    └──────┬─────┘
                                           │
                                           ▼
                                    ┌────────────┐
                                    │    EDA     │
                                    │ Analysis   │
                                    └──────┬─────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │  Preprocessing │
                                    │  - Missing Val │
                                    │  - Outliers    │
                                    │  - Encoding    │
                                    │  - Scaling     │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Train-Test Split
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Class Imbalance│
                                    │    Handling    │
                                    │    (SMOTE)     │
                                    └──────┬─────────┘
                                           │
                   ┌───────────────────────┼───────────────────────┐
                   │                       │                       │
                   ▼                       ▼                       ▼
            ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
            │  Logistic   │        │   Random    │        │   XGBoost   │
            │ Regression  │        │   Forest    │        │             │
            └──────┬──────┘        └──────┬──────┘        └──────┬──────┘
                   │                       │                       │
                   │        ┌──────────────┼──────────────┐       │
                   │        │              │              │       │
                   ▼        ▼              ▼              ▼       ▼
            ┌─────────────┐        ┌─────────────┐
            │     SVM     │        │   Neural    │
            │             │        │   Network   │
            └──────┬──────┘        └──────┬──────┘
                   │                       │
                   └───────────────────────┼───────────────────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Hyperparameter │
                                    │    Tuning      │
                                    │ (GridSearchCV) │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Model Training │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │   Evaluation   │
                                    │  - Accuracy    │
                                    │  - Precision   │
                                    │  - Recall      │
                                    │  - F1-Score    │
                                    │  - ROC-AUC     │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Select Best    │
                                    │    Model       │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │  Save Model    │
                                    │  & Metrics     │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │    END         │
                                    └────────────────┘

                                    
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                     PREDICTION WORKFLOW FLOWCHART                            ║
    ╚══════════════════════════════════════════════════════════════════════════════╝

                                    ┌────────────┐
                                    │   START    │
                                    └──────┬─────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ User Inputs    │
                                    │ Patient Data   │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │Load Preprocessor
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │  Preprocess    │
                                    │  Input Data    │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │  Load Best     │
                                    │  Model         │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Make Prediction│
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Risk           │
                                    │ Classification │
                                    └──────┬─────────┘
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   │                                               │
                   ▼                                               ▼
            ┌─────────────┐                                 ┌─────────────┐
            │    SHAP     │                                 │    LIME     │
            │ Explanation │                                 │ Explanation │
            └──────┬──────┘                                 └──────┬──────┘
                   │                                               │
                   └───────────────────────┬───────────────────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │  Generate      │
                                    │  Human-readable│
                                    │  Explanation   │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │ Display Results│
                                    │ - Risk Level   │
                                    │ - Probability  │
                                    │ - Importance   │
                                    │ - Explanation  │
                                    └──────┬─────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │    END         │
                                    └────────────────┘
    """
    
    return flowchart


def save_diagrams():
    """Save all diagrams to files"""
    project_root = Path(__file__).parent.parent
    diagrams_dir = project_root / 'documentation' / 'diagrams'
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # System Architecture
    arch_diagram = generate_architecture_diagram()
    arch_file = diagrams_dir / 'system_architecture.txt'
    with open(arch_file, 'w') as f:
        f.write(arch_diagram)
    print(f"✓ System architecture diagram saved: {arch_file}")
    
    # Workflow Flowchart
    workflow_diagram = generate_workflow_diagram()
    workflow_file = diagrams_dir / 'workflow_flowchart.txt'
    with open(workflow_file, 'w') as f:
        f.write(workflow_diagram)
    print(f"✓ Workflow flowchart saved: {workflow_file}")
    
    # Display architecture
    print("\n" + arch_diagram)


if __name__ == "__main__":
    save_diagrams()
