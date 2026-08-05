"""
Report generation module for project documentation
"""
from fpdf import FPDF
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config

logger = setup_logger('report_generator', 'logs/report_generator.log')


class ProjectReport(FPDF):
    """Custom PDF report generator"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """Page header"""
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Multi-Disease Prediction System', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Explainable AI for Disease Risk Assessment', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Page footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        """Chapter title"""
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, body):
        """Chapter body"""
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()


def generate_markdown_report(project_root):
    """Generate comprehensive markdown report"""
    
    logger.info("Generating markdown report...")
    
    project_root = Path(project_root)
    config = load_config()
    
    report_path = project_root / 'documentation' / 'reports' / 'project_report.md'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        # Title page
        f.write("# Explainable AI for Multi-Disease Prediction using Machine Learning\n\n")
        f.write("## B.Tech Final Year Project Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%B %Y')}\n\n")
        f.write("**Department:** Computer Science and Engineering\n\n")
        f.write("---\n\n")
        
        # Abstract
        f.write("## Abstract\n\n")
        f.write("This project presents a comprehensive machine learning system for predicting the risk of ")
        f.write("multiple diseases with explainable AI capabilities. The system integrates preprocessing, ")
        f.write("model training, and explainability techniques (SHAP and LIME) to provide transparent ")
        f.write("predictions for 10 different diseases. The web-based interface allows healthcare ")
        f.write("professionals and researchers to input patient data and receive interpretable risk ")
        f.write("assessments.\n\n")
        
        # Introduction
        f.write("## 1. Introduction\n\n")
        f.write("### 1.1 Background\n\n")
        f.write("Healthcare systems worldwide face challenges in early disease detection and risk assessment. ")
        f.write("Machine learning models can assist in predicting disease risk, but black-box models lack ")
        f.write("transparency. This project addresses this gap by implementing explainable AI techniques.\n\n")
        
        f.write("### 1.2 Objectives\n\n")
        f.write("- Develop a unified system for predicting 10 different diseases\n")
        f.write("- Implement multiple machine learning algorithms and compare performance\n")
        f.write("- Integrate explainable AI techniques (SHAP and LIME)\n")
        f.write("- Create an intuitive web interface for healthcare professionals\n")
        f.write("- Ensure reproducibility and ethical AI principles\n\n")
        
        f.write("### 1.3 Diseases Covered\n\n")
        for idx, disease in enumerate(config['diseases'], 1):
            f.write(f"{idx}. {disease['display_name']}\n")
        f.write("\n")
        
        # Methodology
        f.write("## 2. Methodology\n\n")
        
        f.write("### 2.1 System Architecture\n\n")
        f.write("The system consists of the following components:\n\n")
        f.write("1. **Data Preprocessing Module**: Handles missing values, outliers, encoding, and scaling\n")
        f.write("2. **Model Training Pipeline**: Trains and evaluates multiple ML algorithms\n")
        f.write("3. **Explainability Engine**: Implements SHAP and LIME for model interpretation\n")
        f.write("4. **Prediction System**: Unified interface for multi-disease prediction\n")
        f.write("5. **Web Application**: Streamlit-based user interface\n\n")
        
        f.write("### 2.2 Data Preprocessing\n\n")
        f.write("**Steps:**\n")
        f.write("- Missing value imputation (median for numeric, mode for categorical)\n")
        f.write("- Outlier detection and handling using IQR method\n")
        f.write("- Feature encoding (Label Encoding for categorical variables)\n")
        f.write("- Feature scaling (Standard Scaler)\n")
        f.write("- Class imbalance handling using SMOTE\n\n")
        
        f.write("### 2.3 Machine Learning Models\n\n")
        f.write("The following algorithms were implemented:\n\n")
        for algo in config['models']['algorithms']:
            f.write(f"- {algo.replace('_', ' ').title()}\n")
        f.write("\n")
        
        f.write("**Hyperparameter Tuning:** GridSearchCV with 5-fold cross-validation\n\n")
        
        f.write("### 2.4 Evaluation Metrics\n\n")
        f.write("Models were evaluated using:\n")
        for metric in config['evaluation']['metrics']:
            f.write(f"- {metric.replace('_', ' ').title()}\n")
        f.write(f"\n**Primary Metric:** {config['evaluation']['primary_metric'].replace('_', '-').upper()}\n\n")
        
        f.write("### 2.5 Explainable AI Techniques\n\n")
        f.write("**SHAP (SHapley Additive exPlanations):**\n")
        f.write("- Provides global and local feature importance\n")
        f.write("- Based on game theory (Shapley values)\n")
        f.write("- Generates summary plots, waterfall plots, and force plots\n\n")
        
        f.write("**LIME (Local Interpretable Model-agnostic Explanations):**\n")
        f.write("- Explains individual predictions\n")
        f.write("- Model-agnostic approach\n")
        f.write("- Provides local approximations of complex models\n\n")
        
        # Results
        f.write("## 3. Results and Analysis\n\n")
        
        # Load results for each disease
        results_summary = []
        
        for disease_config in config['diseases']:
            disease_name = disease_config['name']
            best_model_path = project_root / 'results' / 'metrics' / disease_name / 'best_model.json'
            
            if best_model_path.exists():
                with open(best_model_path, 'r') as jf:
                    best_info = json.load(jf)
                
                best_model_name = best_info['best_model']
                metrics_path = project_root / 'results' / 'metrics' / disease_name / f'{best_model_name}_metrics.json'
                
                if metrics_path.exists():
                    with open(metrics_path, 'r') as jf:
                        metrics = json.load(jf)
                    
                    results_summary.append({
                        'Disease': disease_config['display_name'],
                        'Best Model': best_model_name.replace('_', ' ').title(),
                        'Accuracy': f"{metrics.get('accuracy', 0):.4f}",
                        'Precision': f"{metrics.get('precision', 0):.4f}",
                        'Recall': f"{metrics.get('recall', 0):.4f}",
                        'F1-Score': f"{metrics.get('f1_score', 0):.4f}",
                        'ROC-AUC': f"{metrics.get('roc_auc', 0):.4f}"
                    })
        
        if results_summary:
            f.write("### 3.1 Model Performance Summary\n\n")
            
            # Create markdown table
            df_results = pd.DataFrame(results_summary)
            f.write(df_results.to_markdown(index=False))
            f.write("\n\n")
            
            # Calculate average performance
            avg_metrics = {
                'Accuracy': sum(float(r['Accuracy']) for r in results_summary) / len(results_summary),
                'Precision': sum(float(r['Precision']) for r in results_summary) / len(results_summary),
                'Recall': sum(float(r['Recall']) for r in results_summary) / len(results_summary),
                'F1-Score': sum(float(r['F1-Score']) for r in results_summary) / len(results_summary),
                'ROC-AUC': sum(float(r['ROC-AUC']) for r in results_summary) / len(results_summary)
            }
            
            f.write("### 3.2 Average Performance Across All Diseases\n\n")
            for metric, value in avg_metrics.items():
                f.write(f"- **{metric}:** {value:.4f}\n")
            f.write("\n")
        
        # Discussion
        f.write("## 4. Discussion\n\n")
        f.write("### 4.1 Key Findings\n\n")
        f.write("- Successfully implemented a multi-disease prediction system\n")
        f.write("- Explainable AI techniques provide transparency in model decisions\n")
        f.write("- Different diseases require different optimal algorithms\n")
        f.write("- Feature importance varies significantly across diseases\n\n")
        
        f.write("### 4.2 Challenges and Solutions\n\n")
        f.write("**Class Imbalance:** Addressed using SMOTE technique\n\n")
        f.write("**Missing Data:** Handled through median/mode imputation\n\n")
        f.write("**Model Interpretability:** Resolved using SHAP and LIME\n\n")
        
        f.write("### 4.3 Limitations\n\n")
        f.write("- Sample datasets used for demonstration purposes\n")
        f.write("- Real clinical validation required\n")
        f.write("- Computational complexity of SHAP for large datasets\n\n")
        
        # Conclusion
        f.write("## 5. Conclusion\n\n")
        f.write("This project successfully demonstrates the implementation of an explainable AI system ")
        f.write("for multi-disease prediction. The integration of SHAP and LIME techniques ensures ")
        f.write("transparency and interpretability, which are crucial for healthcare applications. ")
        f.write("The web-based interface provides an accessible platform for healthcare professionals ")
        f.write("to utilize these advanced ML models.\n\n")
        
        f.write("### 5.1 Future Work\n\n")
        f.write("- Integration with real clinical datasets\n")
        f.write("- Deep learning models (CNN, RNN)\n")
        f.write("- Real-time prediction API\n")
        f.write("- Mobile application development\n")
        f.write("- Multi-language support\n")
        f.write("- Enhanced visualization techniques\n\n")
        
        # References
        f.write("## 6. References\n\n")
        f.write("1. Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. NeurIPS.\n")
        f.write("2. Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). Why should I trust you? KDD.\n")
        f.write("3. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. KDD.\n")
        f.write("4. Breiman, L. (2001). Random forests. Machine learning.\n")
        f.write("5. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. JMLR.\n\n")
        
        # Appendix
        f.write("## 7. Appendix\n\n")
        f.write("### 7.1 System Requirements\n\n")
        f.write("- Python 3.8+\n")
        f.write("- 8GB RAM (minimum)\n")
        f.write("- Modern web browser\n\n")
        
        f.write("### 7.2 Installation Instructions\n\n")
        f.write("```bash\n")
        f.write("# Clone repository\n")
        f.write("cd /home/pavithran/Desktop/yugi1\n\n")
        f.write("# Create virtual environment\n")
        f.write("python -m venv venv\n")
        f.write("source venv/bin/activate\n\n")
        f.write("# Install dependencies\n")
        f.write("pip install -r requirements.txt\n\n")
        f.write("# Download datasets\n")
        f.write("python scripts/download_datasets.py\n\n")
        f.write("# Train models\n")
        f.write("python scripts/train_all_diseases.py\n\n")
        f.write("# Run application\n")
        f.write("streamlit run app/main.py\n")
        f.write("```\n\n")
        
        f.write("---\n")
        f.write(f"\n*Report generated on {datetime.now().strftime('%B %d, %Y')}*\n")
    
    logger.info(f"✓ Markdown report generated: {report_path}")
    return report_path


def generate_model_comparison_table(project_root):
    """Generate detailed model comparison table"""
    
    project_root = Path(project_root)
    config = load_config()
    
    comparison_data = []
    
    for disease_config in config['diseases']:
        disease_name = disease_config['name']
        metrics_dir = project_root / 'results' / 'metrics' / disease_name
        
        if not metrics_dir.exists():
            continue
        
        # Get all model results
        for metrics_file in metrics_dir.glob('*_metrics.json'):
            if metrics_file.stem != 'best_model':
                model_name = metrics_file.stem.replace('_metrics', '')
                
                with open(metrics_file, 'r') as f:
                    metrics = json.load(f)
                
                comparison_data.append({
                    'Disease': disease_config['display_name'],
                    'Model': model_name.replace('_', ' ').title(),
                    'Accuracy': metrics.get('accuracy', 0),
                    'Precision': metrics.get('precision', 0),
                    'Recall': metrics.get('recall', 0),
                    'F1-Score': metrics.get('f1_score', 0),
                    'ROC-AUC': metrics.get('roc_auc', 0)
                })
    
    if comparison_data:
        df = pd.DataFrame(comparison_data)
        
        # Save as CSV
        csv_path = project_root / 'documentation' / 'reports' / 'model_comparison.csv'
        df.to_csv(csv_path, index=False)
        logger.info(f"✓ Model comparison table saved: {csv_path}")
        
        # Save as formatted markdown
        md_path = project_root / 'documentation' / 'reports' / 'model_comparison.md'
        with open(md_path, 'w') as f:
            f.write("# Detailed Model Comparison\n\n")
            f.write(df.to_markdown(index=False))
        
        logger.info(f"✓ Model comparison markdown saved: {md_path}")
        
        return df
    
    return None


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    
    # Generate reports
    generate_markdown_report(project_root)
    generate_model_comparison_table(project_root)
    
    logger.info("✓ All reports generated successfully")
