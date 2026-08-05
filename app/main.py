"""
Streamlit Web Application for Multi-Disease Prediction
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.prediction.prediction_system import MultiDiseasePredictionSystem
from src.utils.config_utils import load_config

# Page configuration
st.set_page_config(
    page_title="Disease Risk Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Elegant neutral theme
st.markdown("""
    <style>
    /* Main header styling - Dark elegant */
    .main-header {
        font-size: 2.8rem;
        font-weight: 600;
        color: #e2e8f0;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.3px;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Patient card - Dark gradient */
    .patient-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        color: #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        border: 1px solid #334155;
    }
    
    .patient-card h3 {
        color: #e2e8f0 !important;
        font-size: 1.4rem;
        margin: 0;
        font-weight: 600;
    }
    
    .patient-card p {
        color: rgba(226,232,240,0.85) !important;
        margin: 0.5rem 0 0 0;
    }
    
    /* Risk level styling - Muted, professional */
    .risk-low {
        color: #38a169;
        font-weight: 600;
        font-size: 1.9rem;
    }
    .risk-medium {
        color: #d69e2e;
        font-weight: 600;
        font-size: 1.9rem;
    }
    .risk-high {
        color: #e53e3e;
        font-weight: 600;
        font-size: 1.9rem;
    }
    
    /* Cards - Dark background */
    .info-card {
        background-color: #1e293b;
        padding: 1.5rem 1.8rem;
        border-radius: 8px;
        border: 1px solid #334155;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .info-card h3, .info-card h4 {
        color: #e2e8f0;
        margin-top: 0;
        font-weight: 600;
    }
    
    .info-card ul {
        color: #cbd5e0;
        margin-bottom: 0;
        line-height: 1.8;
    }
    
    .info-card li {
        margin: 0.7rem 0;
    }
    
    /* Page layout - Dark background */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background-color: #0f172a;
    }
    
    .main {
        background-color: #0f172a;
    }
    
    /* Input fields - Dark background */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #475569;
        padding: 0.6rem;
        font-size: 0.95rem;
        background-color: #1e293b;
        color: #e2e8f0;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        background-color: #1e293b;
    }
    
    /* Buttons - Dark theme with blue accent */
    .stButton > button {
        border-radius: 7px;
        font-weight: 500;
        transition: all 0.2s;
        border: none;
        font-size: 0.95rem;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #e2e8f0;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Tabs - Dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        font-weight: 500;
        color: #94a3b8;
        background-color: transparent;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1e293b;
        color: #3b82f6;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #3b82f6 !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #3b82f6;
    }
    
    /* Alert boxes - Dark theme */
    .stSuccess {
        background-color: #0f2922;
        border-left: 4px solid #38a169;
        padding: 1rem;
        border-radius: 6px;
        color: #9ae6b4;
    }
    
    .stWarning {
        background-color: #2c1b0e;
        border-left: 4px solid #d97706;
        padding: 1rem;
        border-radius: 6px;
        color: #fbbf24;
    }
    
    .stError {
        background-color: #2c1a1a;
        border-left: 4px solid #e53e3e;
        padding: 1rem;
        border-radius: 6px;
        color: #fc8181;
    }
    
    /* Text - Light colors for dark theme */
    body, p, span, div, li, h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0;
    }
    
    .stMarkdown {
        color: #e2e8f0;
    }
    
    /* Sidebar - Dark background */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0;
    }
    
    /* Expander - Dark background */
    .streamlit-expanderHeader {
        background-color: #1e293b;
        border-radius: 6px;
        font-weight: 500;
        color: #e2e8f0;
    }
    
    /* Overall app background */
    .stApp {
        background-color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_prediction_system():
    """Load the prediction system (cached)"""
    try:
        config = load_config()
        system = MultiDiseasePredictionSystem(config)
        system.load_all_models()
        return system, config
    except Exception as e:
        st.error(f"Error loading prediction system: {e}")
        return None, None


def get_example_values(disease_name):
    """Get example values for a specific disease"""
    examples = {
        'diabetes': {
            'low_risk': {
                'description': 'Low Risk Example (Healthy individual)',
                'values': {
                    'Pregnancies': 1,
                    'Glucose': 85,
                    'BloodPressure': 70,
                    'SkinThickness': 20,
                    'Insulin': 80,
                    'BMI': 22.0,
                    'DiabetesPedigreeFunction': 0.2,
                    'Age': 28
                }
            },
            'high_risk': {
                'description': 'High Risk Example (Pre-diabetic profile)',
                'values': {
                    'Pregnancies': 6,
                    'Glucose': 148,
                    'BloodPressure': 85,
                    'SkinThickness': 35,
                    'Insulin': 180,
                    'BMI': 33.5,
                    'DiabetesPedigreeFunction': 0.627,
                    'Age': 55
                }
            }
        },
        'heart_disease': {
            'low_risk': {
                'description': 'Low Risk Example (Healthy heart)',
                'values': {
                    'age': 35,
                    'sex': 0,
                    'cp': 0,
                    'trestbps': 110,
                    'chol': 180,
                    'fbs': 0,
                    'restecg': 0,
                    'thalach': 160,
                    'exang': 0,
                    'oldpeak': 0.5,
                    'slope': 1,
                    'ca': 0,
                    'thal': 2
                }
            },
            'high_risk': {
                'description': 'High Risk Example (Cardiovascular risk)',
                'values': {
                    'age': 62,
                    'sex': 1,
                    'cp': 3,
                    'trestbps': 150,
                    'chol': 280,
                    'fbs': 1,
                    'restecg': 2,
                    'thalach': 110,
                    'exang': 1,
                    'oldpeak': 3.0,
                    'slope': 2,
                    'ca': 2,
                    'thal': 3
                }
            }
        },
        'hypertension': {
            'low_risk': {
                'description': 'Low Risk Example (Normal blood pressure)',
                'values': {
                    'age': 30,
                    'sex': 0,
                    'cigsPerDay': 0,
                    'BPMeds': 0,
                    'prevalentStroke': 0,
                    'prevalentHyp': 0,
                    'diabetes': 0,
                    'totChol': 190,
                    'sysBP': 115,
                    'diaBP': 75,
                    'BMI': 23.0,
                    'heartRate': 72,
                    'glucose': 85
                }
            },
            'high_risk': {
                'description': 'High Risk Example (Hypertensive profile)',
                'values': {
                    'age': 58,
                    'sex': 1,
                    'cigsPerDay': 15,
                    'BPMeds': 1,
                    'prevalentStroke': 0,
                    'prevalentHyp': 1,
                    'diabetes': 1,
                    'totChol': 260,
                    'sysBP': 160,
                    'diaBP': 95,
                    'BMI': 31.5,
                    'heartRate': 88,
                    'glucose': 115
                }
            }
        }
    }
    
    return examples.get(disease_name, {})


def get_disease_input_form(disease_name, feature_names, patient_name=""):
    """Generate input form for a disease"""
    st.markdown(f"### 📋 Health Information for {disease_name.replace('_', ' ').title()}")
    
    # Patient name display if provided
    if patient_name:
        st.markdown(f"""
        <div class="patient-card">
            <h3 style="margin: 0;">👤 Patient: {patient_name}</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Checking risk for {disease_name.replace('_', ' ').title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    input_data = {}
    
    # Create columns for clean layout
    cols = st.columns(3)
    
    for idx, feature in enumerate(feature_names):
        col_idx = idx % 3
        
        with cols[col_idx]:
            # Generate appropriate input widget based on feature name
            
            if 'age' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature} (years)", 
                    min_value=0, 
                    max_value=120, 
                    value=None,
                    placeholder="e.g., 45",
                    help="Enter patient's age in years",
                    key=f"{disease_name}_{feature}"
                )
            elif any(x in feature.lower() for x in ['gender', 'sex']):
                input_data[feature] = st.selectbox(
                    feature, 
                    options=[None, 0, 1], 
                    index=0,
                    format_func=lambda x: "Select..." if x is None else ("Male" if x == 1 else "Female"),
                    key=f"{disease_name}_{feature}"
                )
            elif 'blood' in feature.lower() or 'pressure' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature} (mmHg)", 
                    min_value=0, 
                    max_value=300, 
                    value=None,
                    placeholder="e.g., 120",
                    help="Normal: 90-120, High: >140",
                    key=f"{disease_name}_{feature}"
                )
            elif 'glucose' in feature.lower() or 'sugar' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature} (mg/dL)", 
                    min_value=0, 
                    max_value=500, 
                    value=None,
                    placeholder="e.g., 95",
                    help="Normal: 70-100, Prediabetic: 100-125, Diabetic: >125",
                    key=f"{disease_name}_{feature}"
                )
            elif 'bmi' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature}", 
                    min_value=10.0, 
                    max_value=60.0, 
                    value=None,
                    placeholder="e.g., 24.5",
                    step=0.1,
                    help="Normal: 18.5-24.9, Overweight: 25-29.9, Obese: >30",
                    key=f"{disease_name}_{feature}"
                )
            elif 'pregnancies' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature} (count)", 
                    min_value=0, 
                    max_value=20, 
                    value=None,
                    placeholder="e.g., 2",
                    help="Number of pregnancies",
                    key=f"{disease_name}_{feature}"
                )
            elif 'insulin' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature} (μU/mL)", 
                    min_value=0, 
                    max_value=1000, 
                    value=None,
                    placeholder="e.g., 80",
                    help="2-hour serum insulin (Normal: 16-166)",
                    key=f"{disease_name}_{feature}"
                )
            else:
                input_data[feature] = st.number_input(
                    feature, 
                    value=None,
                    placeholder="Enter value",
                    help=f"Enter {feature} value",
                    key=f"{disease_name}_{feature}"
                )
    
    return input_data


def plot_feature_importance(feature_importance_data):
    """Plot feature importance"""
    if not feature_importance_data:
        return None
    
    df = pd.DataFrame(feature_importance_data)
    
    fig = go.Figure(go.Bar(
        x=df['importance'],
        y=df['feature'],
        orientation='h',
        marker=dict(
            color=df['importance'],
            colorscale='RdYlGn_r',
            showscale=True
        )
    ))
    
    fig.update_layout(
        title="Feature Importance (SHAP Values)",
        xaxis_title="Importance",
        yaxis_title="Features",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def plot_risk_gauge(probability):
    """Plot risk probability as gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Probability (%)"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig


def display_prediction_result(result):
    """Display prediction result with visualizations"""
    disease_name = result['disease'].replace('_', ' ').title()
    risk_level = result['risk_level']
    probability = result['probability']
    
    # Risk level styling
    risk_class = f"risk-{risk_level.lower()}"
    
    st.markdown("---")
    
    # Clean risk display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"## 📊 {disease_name} Risk Assessment")
        st.markdown(f'<div class="{risk_class}">{risk_level} Risk</div>', unsafe_allow_html=True)
        
        if risk_level == "High":
            st.error(f"**{probability:.0%} probability** - Immediate attention recommended")
        elif risk_level == "Medium":
            st.warning(f"**{probability:.0%} probability** - Preventive action advised")
        else:
            st.success(f"**{probability:.0%} probability** - Maintain healthy habits")
    
    with col2:
        # Risk gauge
        fig_gauge = plot_risk_gauge(probability)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # --- Confidence Score Meter (Kumar 2024: uncertainty quantification) ---
    st.markdown("### 🎯 AI Confidence Score")
    conf_col1, conf_col2, conf_col3 = st.columns(3)
    with conf_col1:
        st.metric(label="Disease Probability", value=f"{probability:.1%}")
    with conf_col2:
        st.metric(label="Healthy Probability", value=f"{1 - probability:.1%}")
    with conf_col3:
        if probability >= 0.80:
            conf_label = "🔴 Very High Confidence"
        elif probability >= 0.60:
            conf_label = "🟠 High Confidence"
        elif probability >= 0.40:
            conf_label = "🟡 Moderate Confidence"
        else:
            conf_label = "🟢 Low Confidence"
        st.metric(label="Model Confidence", value=conf_label)
    
    # Confidence progress bar
    st.progress(probability, text=f"Risk probability: {probability:.1%}")
    
    # --- SHAP Feature Importance (Raza 2024, Ali 2024: beeswarm improves trust) ---
    shap_data = result.get('shap_importance') or result.get('feature_importance')
    if shap_data:
        with st.expander("🔬 SHAP Feature Importance (Why this prediction?)", expanded=True):
            fig_shap = plot_feature_importance(shap_data)
            if fig_shap:
                st.plotly_chart(fig_shap, use_container_width=True)
                st.caption("📌 Features pushing toward disease risk (red/higher values) vs healthy (green/lower values)")
    
    # LIME explanation if available
    lime_data = result.get('lime_explanation')
    if lime_data:
        with st.expander("🧩 LIME Local Explanation (This patient specifically)", expanded=False):
            lime_features = lime_data if isinstance(lime_data, list) else []
            if lime_features:
                lime_df = pd.DataFrame(lime_features[:10], columns=["Feature Condition", "Impact"])
                st.dataframe(lime_df, use_container_width=True)
                st.caption("📌 LIME explains why THIS specific patient got this result (local explanation)")
    
    # Explanation in clean format
    if result['explanation']:
        with st.expander("📖 Medical Explanation", expanded=False):
            st.markdown(result['explanation'])
    
    # Simple action plan
    st.markdown("### 📋 Recommended Actions")
    
    if risk_level == "High":
        st.markdown("""
        <div class="info-card">
        <h4>🚨 Take Action This Week</h4>
        <ul>
        <li>📞 Schedule doctor appointment</li>
        <li>📋 Request medical screening</li>
        <li>💪 Begin lifestyle changes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "Medium":
        st.markdown("""
        <div class="info-card">
        <h4>⚠️ Prevention Steps</h4>
        <ul>
        <li>📅 Schedule checkup within 1-3 months</li>
        <li>🏃 Start regular exercise routine</li>
        <li>🥗 Improve diet and nutrition</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
        <h4>✅ Keep It Up</h4>
        <ul>
        <li>✓ Continue healthy lifestyle</li>
        <li>✓ Annual checkups recommended</li>
        <li>✓ Stay active and informed</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Clean header
    st.markdown('<h1 class="main-header">Explainable AI for Multi-Disease Prediction using Machine Learning </h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Simple AI-powered health screening • Clear results • Actionable insights</p>', unsafe_allow_html=True)
    
    # Load prediction system
    with st.spinner("Loading prediction system..."):
        system, config = load_prediction_system()
    
    if system is None:
        st.error("Failed to load prediction system. Please ensure models are trained.")
        st.info("💡 Run the training pipeline first: `python scripts/train_all_diseases.py`")
        return
    
    # Sidebar - Clean and organized
    st.sidebar.title("🎯 Start Here")
    
    # Patient Information Section
    st.sidebar.markdown("### 👤 Patient Information")
    patient_name = st.sidebar.text_input(
        "Patient Name",
        placeholder="Enter patient name...",
        help="Optional: Add patient name for personalized results"
    )
    
    if patient_name:
        st.sidebar.success(f"✓ {patient_name}")
    
    st.sidebar.markdown("---")
    
    # Disease selection with better UI
    st.sidebar.markdown("### 🏥 Select Disease(s) to Check")
    
    available_diseases = list(system.disease_models.keys())
    
    if not available_diseases:
        st.error("No trained models found. Please train the models first.")
        return
    
    # Group diseases by category for better organization
    selected_diseases = []
    
    with st.sidebar.expander("✓ Common Diseases", expanded=True):
        for disease in ['diabetes', 'heart_disease', 'hypertension']:
            if disease in available_diseases:
                display_name = disease.replace('_', ' ').title()
                if st.checkbox(display_name, value=(disease=='diabetes'), key=f"cb_{disease}"):
                    selected_diseases.append(disease)
    
    with st.sidebar.expander("✓ Other Diseases"):
        for disease in available_diseases:
            if disease not in ['diabetes', 'heart_disease', 'hypertension']:
                display_name = disease.replace('_', ' ').title()
                if st.checkbox(display_name, key=f"cb_{disease}"):
                    selected_diseases.append(disease)
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown("### ⚙️ Settings")
    show_explanations = st.sidebar.toggle("Show AI Explanations", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip**: Start by selecting 1-2 diseases, then add more if needed.")
    
    # Main content
    if not selected_diseases:
        st.info("👈 **Get Started:** Select a disease from the sidebar to begin your health assessment")
        
        # Show welcome message
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="info-card">
            <h3>🎯 Simple</h3>
            <p>Enter basic health info</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="info-card">
            <h3>🤖 Smart</h3>
            <p>AI analyzes your risk</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="info-card">
            <h3>📋 Clear</h3>
            <p>Get actionable results</p>
            </div>
            """, unsafe_allow_html=True)
        return
    
    # Show patient name if entered
    if patient_name:
        st.markdown(f"""
        <div class="patient-card">
            <h3>👤 Patient: {patient_name}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different diseases - cleaner design
    tabs = st.tabs([f"🔍 {disease.replace('_', ' ').title()}" for disease in selected_diseases])
    
    # Input forms for each disease
    for idx, disease in enumerate(selected_diseases):
        with tabs[idx]:
            feature_names = system.get_required_features(disease)
            
            if feature_names is None:
                st.error(f"Preprocessor not found for {disease}")
                continue
            
            # Input form
            with st.form(key=f"form_{disease}"):
                input_data = get_disease_input_form(disease, feature_names, patient_name)
                
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    submit_button = st.form_submit_button(
                        "🔍 Analyze Risk", 
                        use_container_width=True, 
                        type="primary"
                    )
                with col2:
                    st.form_submit_button("🔄 Reset", use_container_width=True)
            
            # Make prediction
            if submit_button:
                # Validate inputs
                missing_fields = [k for k, v in input_data.items() if v is None]
                
                if missing_fields:
                    st.error(f"⚠️ Please fill in all fields. Missing: {', '.join(missing_fields[:3])}...")
                else:
                    with st.spinner(f"🔬 Analyzing {disease.replace('_', ' ')}..."):
                        result = system.predict_single_disease(
                            disease,
                            input_data,
                            explain=show_explanations
                        )
                        
                        if result:
                            st.success("✅ Analysis Complete!")
                            display_prediction_result(result)
                        else:
                            st.error("❌ Analysis failed. Please try again.")
    
    # Footer - Soft, minimal
    st.markdown("---")
    st.markdown("""
        <div style="background-color: #fffaf0; 
                    padding: 1.5rem; 
                    border-radius: 8px; 
                    border: 1px solid #feebc8;
                    margin-top: 2rem;">
        <h4 style="color: #744210; margin-top: 0; font-weight: 600;">⚠️ Medical Disclaimer</h4>
        <p style="color: #744210; margin-bottom: 0; line-height: 1.7; font-size: 0.95rem;">
        <strong>This is NOT a diagnosis.</strong> This AI tool provides risk estimates only. 
        Always consult a qualified healthcare professional for medical advice, diagnosis, and treatment.
        </p>
        </div>
        <br>
        <div style="text-align: center; color: #a0aec0; font-size: 0.88rem; padding: 1.5rem 0;">
        <p style="margin: 0;">🎓 Educational AI Project | B.Tech Computer Science</p>
        <p style="margin: 0.4rem 0 0 0; font-size: 0.82rem;">Explainable AI • 20 Disease Models • January 2026</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
