"""
Unified prediction system for all diseases
"""
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config, get_model_save_path
from src.utils.model_utils import get_risk_level
from src.explainability.xai_engine import ExplainabilityEngine

logger = setup_logger('prediction', 'logs/prediction.log')


class MultiDiseasePredictionSystem:
    """Unified prediction system for multiple diseases"""
    
    def __init__(self, config=None):
        if config is None:
            config = load_config()
        
        self.config = config
        self.diseases = [d['name'] for d in config['diseases']]
        self.disease_models = {}
        self.disease_preprocessors = {}
        self.disease_explainers = {}
        
    def load_disease_model(self, disease_name):
        """Load best model for a specific disease"""
        try:
            # Load best model info
            project_root = Path(__file__).parent.parent.parent
            best_model_path = project_root / 'results' / 'metrics' / disease_name / 'best_model.json'
            
            if not best_model_path.exists():
                logger.error(f"Best model info not found for {disease_name}")
                return None
            
            import json
            with open(best_model_path, 'r') as f:
                best_model_info = json.load(f)
            
            best_model_name = best_model_info['best_model']
            
            # Load model
            model_path = project_root / 'models' / disease_name / f'{best_model_name}.pkl'
            model = joblib.load(model_path)
            
            logger.info(f"✓ Loaded {best_model_name} for {disease_name}")
            return model
        
        except Exception as e:
            logger.error(f"Error loading model for {disease_name}: {e}")
            return None
    
    def load_disease_preprocessor(self, disease_name):
        """Load preprocessor for a specific disease"""
        try:
            project_root = Path(__file__).parent.parent.parent
            preprocessor_path = project_root / 'models' / disease_name / 'preprocessor.pkl'
            
            if not preprocessor_path.exists():
                logger.error(f"Preprocessor not found for {disease_name}")
                return None
            
            preprocessor_data = joblib.load(preprocessor_path)
            
            logger.info(f"✓ Loaded preprocessor for {disease_name}")
            return preprocessor_data
        
        except Exception as e:
            logger.error(f"Error loading preprocessor for {disease_name}: {e}")
            return None
    
    def load_all_models(self):
        """Load models for all diseases"""
        logger.info("Loading all disease models...")
        
        for disease in self.diseases:
            model = self.load_disease_model(disease)
            preprocessor = self.load_disease_preprocessor(disease)
            
            if model is not None:
                self.disease_models[disease] = model
            
            if preprocessor is not None:
                self.disease_preprocessors[disease] = preprocessor
                
                # Initialize explainer with training data sample
                try:
                    project_root = Path(__file__).parent.parent.parent
                    train_data_path = project_root / 'models' / disease / 'X_train_sample.pkl'
                    
                    if train_data_path.exists():
                        X_train_sample = joblib.load(train_data_path)
                        self.initialize_explainer(disease, X_train_sample)
                    else:
                        logger.warning(f"No training sample found for {disease}, explanations will be limited")
                except Exception as e:
                    logger.warning(f"Could not initialize explainer for {disease}: {e}")
        
        logger.info(f"✓ Loaded models for {len(self.disease_models)} diseases")
    
    def initialize_explainer(self, disease_name, X_train_sample):
        """Initialize explainability engine for a disease"""
        if disease_name not in self.disease_models:
            logger.error(f"Model not loaded for {disease_name}")
            return None
        
        try:
            model = self.disease_models[disease_name]
            preprocessor = self.disease_preprocessors[disease_name]
            feature_names = preprocessor['feature_names']
            
            explainer = ExplainabilityEngine(
                model=model,
                X_train=X_train_sample,
                feature_names=feature_names,
                config=self.config
            )
            
            self.disease_explainers[disease_name] = explainer
            logger.info(f"✓ Explainer initialized for {disease_name}")
            return explainer
        
        except Exception as e:
            logger.error(f"Error initializing explainer for {disease_name}: {e}")
            return None
    
    def preprocess_input(self, disease_name, input_data):
        """
        Preprocess input data for prediction
        
        Args:
            disease_name: Name of the disease
            input_data: Dictionary or DataFrame with input features
            
        Returns:
            Preprocessed numpy array
        """
        if disease_name not in self.disease_preprocessors:
            logger.error(f"Preprocessor not loaded for {disease_name}")
            return None
        
        try:
            preprocessor = self.disease_preprocessors[disease_name]
            feature_names = preprocessor['feature_names']
            scaler = preprocessor['scaler']
            label_encoders = preprocessor['label_encoders']
            
            # Log raw input for debugging
            logger.info(f"Raw input for {disease_name}: {input_data}")
            
            # Convert to DataFrame if dictionary
            if isinstance(input_data, dict):
                input_df = pd.DataFrame([input_data])
            else:
                input_df = input_data.copy()
            
            # Ensure all required features are present
            for feature in feature_names:
                if feature not in input_df.columns:
                    logger.error(f"Missing feature: {feature}")
                    return None
            
            # Select and order features
            input_df = input_df[feature_names]
            logger.info(f"Ordered features for {disease_name}: {input_df.values[0].tolist()}")
            
            # Apply label encoding if needed
            for col, encoder in label_encoders.items():
                if col in input_df.columns and col in feature_names:
                    try:
                        input_df[col] = encoder.transform(input_df[col].astype(str))
                    except:
                        pass
            
            # Scale features
            input_scaled = scaler.transform(input_df)
            logger.info(f"Scaled features (first 5): {input_scaled[0][:5].tolist()}")
            
            return input_scaled
        
        except Exception as e:
            logger.error(f"Error preprocessing input for {disease_name}: {e}")
            return None
    
    def predict_single_disease(self, disease_name, input_data, explain=True):
        """
        Predict for a single disease with explanations
        
        Args:
            disease_name: Name of the disease
            input_data: Input features (dict or DataFrame)
            explain: Whether to generate explanations
            
        Returns:
            Dictionary with prediction and explanations
        """
        if disease_name not in self.disease_models:
            logger.error(f"Model not loaded for {disease_name}")
            return None
        
        try:
            # Preprocess input
            input_processed = self.preprocess_input(disease_name, input_data)
            
            if input_processed is None:
                return None
            
            # Make prediction
            model = self.disease_models[disease_name]
            prediction = model.predict(input_processed)[0]
            prediction_proba = model.predict_proba(input_processed)[0, 1]
            
            # Log prediction results
            logger.info(f"Prediction for {disease_name}: class={prediction}, probability={prediction_proba:.4f}")
            
            # Get risk level
            risk_level = get_risk_level(prediction_proba, self.config['risk_thresholds'])
            
            result = {
                'disease': disease_name,
                'prediction': int(prediction),
                'probability': float(prediction_proba),
                'risk_level': risk_level,
                'explanation': None,
                'feature_importance': None
            }
            
            # Generate explanations if requested
            if explain and disease_name in self.disease_explainers:
                explainer = self.disease_explainers[disease_name]
                
                # Get SHAP feature importance
                shap_importance = explainer.get_shap_feature_importance(input_processed, top_n=10)
                
                if shap_importance is not None:
                    result['feature_importance'] = shap_importance.to_dict('records')
                    
                    # Generate text explanation with disease name for medical context
                    text_explanation = explainer.generate_text_explanation(
                        input_processed[0],
                        prediction_proba,
                        shap_importance,
                        disease_name=disease_name
                    )
                    result['explanation'] = text_explanation
            
            logger.info(f"✓ Prediction completed for {disease_name}: {risk_level} risk")
            return result
        
        except Exception as e:
            logger.error(f"Error predicting for {disease_name}: {e}")
            return None
    
    def predict_all_diseases(self, input_data_dict, explain=True):
        """
        Predict for all diseases
        
        Args:
            input_data_dict: Dictionary with disease names as keys and input data as values
            explain: Whether to generate explanations
            
        Returns:
            Dictionary with predictions for all diseases
        """
        results = {}
        
        for disease_name in self.diseases:
            if disease_name in input_data_dict and disease_name in self.disease_models:
                result = self.predict_single_disease(
                    disease_name,
                    input_data_dict[disease_name],
                    explain
                )
                
                if result is not None:
                    results[disease_name] = result
        
        return results
    
    def get_disease_info(self, disease_name):
        """Get information about a disease"""
        for disease in self.config['diseases']:
            if disease['name'] == disease_name:
                return disease
        return None
    
    def get_required_features(self, disease_name):
        """Get list of required features for a disease"""
        if disease_name not in self.disease_preprocessors:
            return None
        
        return self.disease_preprocessors[disease_name]['feature_names']
