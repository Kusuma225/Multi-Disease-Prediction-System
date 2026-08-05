#!/usr/bin/env python3
"""
Generate PDF Project Brief for Explainable AI Multi-Disease Prediction System
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime

def create_project_brief_pdf(output_filename="Project_Brief.pdf"):
    """Create a comprehensive PDF brief for the project"""
    
    # Create PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=A4,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    # Container for PDF elements
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0d47a1'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#1565c0'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # Title
    title = Paragraph("Explainable AI for Multi-Disease Prediction<br/>using Machine Learning", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Project Type
    project_type = Paragraph("<b>B.Tech Final Year Project</b><br/>Department of Computer Science/Information Technology", 
                            ParagraphStyle('Center', parent=body_style, alignment=TA_CENTER))
    story.append(project_type)
    story.append(Spacer(1, 0.3*inch))
    
    # Abstract
    story.append(Paragraph("Abstract", heading_style))
    abstract_text = """
    This project implements a comprehensive intelligent healthcare system capable of predicting risk for 20 different 
    diseases using multiple machine learning algorithms. The system integrates Explainable AI (XAI) techniques including 
    SHAP and LIME to provide transparent, interpretable predictions with Low/Medium/High risk classifications. 
    Built with Streamlit for an interactive web interface, the system serves as a decision support tool for healthcare 
    professionals and researchers, ensuring ethical AI deployment through transparent model explanations.
    """
    story.append(Paragraph(abstract_text, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Key Features
    story.append(Paragraph("Key Features", heading_style))
    features = [
        "Multi-Disease Prediction: Unified system for 20 different diseases",
        "Multiple ML Algorithms: Logistic Regression, Random Forest, XGBoost, SVM, Neural Networks",
        "Explainable AI: SHAP (global/local importance) and LIME (instance-level explanations)",
        "Risk Classification: Automated Low/Medium/High risk assessment",
        "Interactive UI: Streamlit-based web application with real-time predictions",
        "Comprehensive Evaluation: Accuracy, Precision, Recall, F1-Score, ROC-AUC metrics"
    ]
    for feature in features:
        story.append(Paragraph(f"• {feature}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Diseases Trained
    story.append(Paragraph("Diseases Trained (20 Total)", heading_style))
    
    story.append(Paragraph("Original 10 Diseases:", subheading_style))
    original_diseases = [
        ["1. Diabetes", "2. Heart Disease", "3. Liver Disease"],
        ["4. Kidney Disease", "5. Breast Cancer", "6. Parkinson's Disease"],
        ["7. Stroke", "8. Hypertension", "9. Anemia"],
        ["10. Thyroid Disorder", "", ""]
    ]
    
    disease_table = Table(original_diseases, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
    disease_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#263238')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(disease_table)
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Additional 10 Diseases:", subheading_style))
    new_diseases = [
        ["11. COPD", "12. Pneumonia", "13. Alzheimer's Disease"],
        ["14. Asthma", "15. Tuberculosis", "16. Malaria"],
        ["17. COVID-19", "18. Hepatitis", "19. Osteoporosis"],
        ["20. Arthritis", "", ""]
    ]
    
    disease_table2 = Table(new_diseases, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
    disease_table2.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#263238')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(disease_table2)
    story.append(Spacer(1, 0.2*inch))
    
    # Methodology
    story.append(Paragraph("Methodology", heading_style))
    
    story.append(Paragraph("Data Preprocessing:", subheading_style))
    preprocessing = [
        "Missing value imputation using statistical methods",
        "Outlier detection and handling",
        "Feature scaling and normalization",
        "Feature selection using correlation and importance analysis",
        "Class imbalance handling using SMOTE"
    ]
    for item in preprocessing:
        story.append(Paragraph(f"• {item}", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Model Training:", subheading_style))
    training = [
        "5-fold cross-validation for robust evaluation",
        "Hyperparameter tuning using GridSearchCV",
        "Model comparison and best model selection per disease",
        "Comprehensive performance evaluation"
    ]
    for item in training:
        story.append(Paragraph(f"• {item}", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Explainable AI Implementation:", subheading_style))
    xai = [
        "SHAP: Global feature importance and local explanations",
        "LIME: Instance-level prediction explanations",
        "Visual interpretation dashboards",
        "Feature contribution analysis"
    ]
    for item in xai:
        story.append(Paragraph(f"• {item}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # System Architecture
    story.append(Paragraph("System Architecture", heading_style))
    architecture_text = """
    The system follows a modular architecture with separate components for data preprocessing, model training, 
    prediction engine, explainability modules, and web interface. Each disease has dedicated trained models stored 
    in the models directory, with evaluation metrics and visualizations stored in the results directory. 
    The Streamlit application provides a unified interface for all 20 disease predictions.
    """
    story.append(Paragraph(architecture_text, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # How to Run
    story.append(Paragraph("Running the Application", heading_style))
    story.append(Paragraph("Prerequisites: Python 3.8 or higher, pip package manager", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    run_steps = [
        "<b>Step 1:</b> Activate virtual environment: <font face='Courier'>source venv/bin/activate</font>",
        "<b>Step 2:</b> Install dependencies: <font face='Courier'>pip install -r requirements.txt</font>",
        "<b>Step 3:</b> Download datasets: <font face='Courier'>python scripts/download_datasets.py</font>",
        "<b>Step 4:</b> Preprocess data: <font face='Courier'>python src/preprocessing/preprocess_all.py</font>",
        "<b>Step 5:</b> Train models: <font face='Courier'>python src/models/train_all_models.py</font>",
        "<b>Step 6:</b> Launch web app: <font face='Courier'>streamlit run app/main.py --server.fileWatcherType none</font>"
    ]
    for step in run_steps:
        story.append(Paragraph(step, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    note = Paragraph("<i>Note: The --server.fileWatcherType none flag prevents inotify watch limit errors on Linux systems.</i>", 
                    body_style)
    story.append(note)
    story.append(Spacer(1, 0.2*inch))
    
    # Results and Outputs
    story.append(Paragraph("Results and Outputs", heading_style))
    outputs_text = """
    The system generates comprehensive evaluation results for each disease including:
    Performance metrics (accuracy, precision, recall, F1-score, ROC-AUC), confusion matrices, 
    ROC curves, feature importance plots, SHAP summary plots, and LIME explanations. 
    All artifacts are organized per-disease in the results directory.
    """
    story.append(Paragraph(outputs_text, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Ethical Considerations
    story.append(Paragraph("Ethical Considerations", heading_style))
    ethics = [
        "Transparent decision-making through Explainable AI",
        "No black-box predictions - all decisions are interpretable",
        "Clear explanation of model limitations and confidence levels",
        "Privacy-preserving practices in data handling",
        "Bias detection and mitigation strategies"
    ]
    for item in ethics:
        story.append(Paragraph(f"• {item}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Applications
    story.append(Paragraph("Applications", heading_style))
    applications_text = """
    This system serves as a clinical decision support tool for healthcare professionals, an educational 
    platform for medical students, a research tool for healthcare AI studies, and a demonstration of 
    ethical AI deployment in healthcare. The explainability features ensure trust and transparency in 
    AI-assisted medical diagnosis.
    """
    story.append(Paragraph(applications_text, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Technology Stack
    story.append(Paragraph("Technology Stack", heading_style))
    tech_data = [
        ["Category", "Technologies"],
        ["ML Libraries", "scikit-learn, XGBoost, TensorFlow/Keras"],
        ["XAI Tools", "SHAP, LIME"],
        ["Data Processing", "pandas, NumPy, imbalanced-learn"],
        ["Visualization", "matplotlib, seaborn, plotly"],
        ["Web Framework", "Streamlit"],
        ["Development", "Python 3.8+, Jupyter Notebooks"]
    ]
    
    tech_table = Table(tech_data, colWidths=[1.8*inch, 4.5*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"""
    <b>Project Type:</b> B.Tech Final Year Project<br/>
    <b>Department:</b> Computer Science/Information Technology<br/>
    <b>Purpose:</b> Academic Research and Development<br/>
    <b>Date:</b> January 2026<br/>
    <b>Data Sources:</b> Kaggle and UCI ML Repository
    """
    story.append(Paragraph(footer_text, 
                          ParagraphStyle('Footer', parent=body_style, fontSize=9, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF brief generated successfully: {output_filename}")
    return output_filename

if __name__ == "__main__":
    create_project_brief_pdf("Project_Brief.pdf")
