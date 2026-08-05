"""
Explainable AI module using SHAP and LIME
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shap
from lime import lime_tabular
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config

logger = setup_logger('explainability', 'logs/explainability.log')


class ExplainabilityEngine:
    """Explainable AI engine using SHAP and LIME"""
    
    def __init__(self, model, X_train, feature_names, config=None):
        """
        Initialize explainability engine
        
        Args:
            model: Trained ML model
            X_train: Training data for background distribution
            feature_names: List of feature names
            config: Configuration dictionary
        """
        if config is None:
            config = load_config()
        
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names
        self.config = config
        self.explainability_config = config['explainability']
        
        # Initialize SHAP explainer
        self.shap_explainer = None
        if self.explainability_config['shap']['enabled']:
            self.initialize_shap_explainer()
        
        # Initialize LIME explainer
        self.lime_explainer = None
        if self.explainability_config['lime']['enabled']:
            self.initialize_lime_explainer()
    
    def initialize_shap_explainer(self):
        """Initialize SHAP explainer"""
        try:
            logger.info("Initializing SHAP explainer...")
            
            # Use KernelExplainer for model-agnostic explanations
            # For tree-based models, TreeExplainer is faster
            model_type = type(self.model).__name__
            
            if 'RandomForest' in model_type or 'XGB' in model_type or 'GradientBoosting' in model_type or 'LGBM' in model_type or 'LightGBM' in model_type:
                self.shap_explainer = shap.TreeExplainer(self.model)
                logger.info("Using TreeExplainer for tree-based model")
            else:
                # Use a sample of training data as background
                background = shap.sample(self.X_train, min(100, len(self.X_train)))
                self.shap_explainer = shap.KernelExplainer(self.model.predict_proba, background)
                logger.info("Using KernelExplainer for non-tree model")
            
            logger.info("✓ SHAP explainer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize SHAP explainer: {e}")
            self.shap_explainer = None
    
    def initialize_lime_explainer(self):
        """Initialize LIME explainer"""
        try:
            logger.info("Initializing LIME explainer...")
            
            self.lime_explainer = lime_tabular.LimeTabularExplainer(
                self.X_train,
                feature_names=self.feature_names,
                class_names=['Negative', 'Positive'],
                mode='classification',
                random_state=42
            )
            
            logger.info("✓ LIME explainer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize LIME explainer: {e}")
            self.lime_explainer = None
    
    def get_shap_values(self, X):
        """
        Get SHAP values for given data
        
        Args:
            X: Input data (numpy array or pandas DataFrame)
            
        Returns:
            SHAP values
        """
        if self.shap_explainer is None:
            logger.warning("SHAP explainer not initialized")
            return None
        
        try:
            logger.info("Computing SHAP values...")
            
            model_type = type(self.model).__name__
            
            if 'RandomForest' in model_type or 'XGB' in model_type or 'GradientBoosting' in model_type or 'LGBM' in model_type or 'LightGBM' in model_type:
                shap_values = self.shap_explainer.shap_values(X)
                # For binary classification, take the positive class
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]
            else:
                shap_values = self.shap_explainer.shap_values(X)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]
            
            logger.info("✓ SHAP values computed")
            return shap_values
        
        except Exception as e:
            logger.error(f"Error computing SHAP values: {e}")
            return None
    
    def plot_shap_beeswarm(self, X, save_path=None):
        """
        Plot SHAP beeswarm plot (Raza 2024, Ali 2024: improves clinical trust)
        Shows distribution of SHAP values for each feature across all samples.
        
        Args:
            X: Input data
            save_path: Path to save the plot
        """
        if self.shap_explainer is None:
            logger.warning("SHAP explainer not initialized")
            return
        
        try:
            shap_values = self.get_shap_values(X)
            
            if shap_values is not None:
                plt.figure(figsize=(10, 8))
                shap.summary_plot(
                    shap_values, X,
                    feature_names=self.feature_names,
                    plot_type="dot",   # beeswarm style
                    show=False
                )
                plt.title("SHAP Beeswarm Plot — Feature Impact Distribution")
                
                if save_path:
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')
                    logger.info(f"✓ SHAP beeswarm plot saved to {save_path}")
                plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting SHAP beeswarm: {e}")
    
    def get_confidence_score(self, X_instance):
        """
        Return prediction probability as a confidence score (Kumar 2024: uncertainty display)
        
        Args:
            X_instance: Single patient input (1D or 2D array)
            
        Returns:
            dict with probability, confidence_level, and confidence_label
        """
        try:
            if len(np.array(X_instance).shape) == 1:
                X_instance = np.array(X_instance).reshape(1, -1)
            
            proba = self.model.predict_proba(X_instance)[0]
            positive_prob = float(proba[1])
            
            if positive_prob >= 0.80:
                confidence_label = "Very High Confidence"
                confidence_level = "high"
            elif positive_prob >= 0.60:
                confidence_label = "High Confidence"
                confidence_level = "medium-high"
            elif positive_prob >= 0.40:
                confidence_label = "Moderate Confidence"
                confidence_level = "medium"
            else:
                confidence_label = "Low Confidence"
                confidence_level = "low"
            
            return {
                'probability': positive_prob,
                'negative_probability': float(proba[0]),
                'confidence_label': confidence_label,
                'confidence_level': confidence_level
            }
        
        except Exception as e:
            logger.error(f"Error computing confidence score: {e}")
            return None
    
    def plot_shap_summary(self, X, save_path=None):
        """
        Plot SHAP summary plot
        
        Args:
            X: Input data
            save_path: Path to save the plot
        """
        if self.shap_explainer is None:
            logger.warning("SHAP explainer not initialized")
            return
        
        try:
            shap_values = self.get_shap_values(X)
            
            if shap_values is not None:
                plt.figure(figsize=(10, 8))
                shap.summary_plot(shap_values, X, feature_names=self.feature_names, show=False)
                
                if save_path:
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')
                    logger.info(f"✓ SHAP summary plot saved to {save_path}")
                plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting SHAP summary: {e}")
    
    def plot_shap_waterfall(self, X, instance_index=0, save_path=None):
        """
        Plot SHAP waterfall plot for a single instance
        
        Args:
            X: Input data
            instance_index: Index of instance to explain
            save_path: Path to save the plot
        """
        if self.shap_explainer is None:
            logger.warning("SHAP explainer not initialized")
            return
        
        try:
            shap_values = self.get_shap_values(X[instance_index:instance_index+1])
            
            if shap_values is not None:
                plt.figure(figsize=(10, 8))
                
                # Create explanation object
                if hasattr(self.shap_explainer, 'expected_value'):
                    expected_value = self.shap_explainer.expected_value
                    if isinstance(expected_value, list):
                        expected_value = expected_value[1]
                else:
                    expected_value = 0
                
                explanation = shap.Explanation(
                    values=shap_values[0],
                    base_values=expected_value,
                    data=X[instance_index],
                    feature_names=self.feature_names
                )
                
                shap.waterfall_plot(explanation, show=False)
                
                if save_path:
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')
                    logger.info(f"✓ SHAP waterfall plot saved to {save_path}")
                plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting SHAP waterfall: {e}")
    
    def get_shap_feature_importance(self, X, top_n=10):
        """
        Get feature importance from SHAP values
        
        Args:
            X: Input data
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importance
        """
        shap_values = self.get_shap_values(X)
        
        if shap_values is None:
            return None
        
        # Calculate mean absolute SHAP values
        importance = np.abs(shap_values).mean(axis=0)
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        })
        
        importance_df = importance_df.sort_values('importance', ascending=False).head(top_n)
        
        return importance_df
    
    def explain_instance_lime(self, instance, num_features=10):
        """
        Explain a single instance using LIME
        
        Args:
            instance: Single instance to explain (numpy array)
            num_features: Number of features to include in explanation
            
        Returns:
            LIME explanation object
        """
        if self.lime_explainer is None:
            logger.warning("LIME explainer not initialized")
            return None
        
        try:
            logger.info("Generating LIME explanation...")
            
            explanation = self.lime_explainer.explain_instance(
                instance,
                self.model.predict_proba,
                num_features=num_features,
                num_samples=self.explainability_config['lime']['num_samples']
            )
            
            logger.info("✓ LIME explanation generated")
            return explanation
        
        except Exception as e:
            logger.error(f"Error generating LIME explanation: {e}")
            return None
    
    def plot_lime_explanation(self, instance, save_path=None, num_features=10):
        """
        Plot LIME explanation for a single instance
        
        Args:
            instance: Single instance to explain
            save_path: Path to save the plot
            num_features: Number of features to show
        """
        explanation = self.explain_instance_lime(instance, num_features)
        
        if explanation is None:
            return
        
        try:
            fig = explanation.as_pyplot_figure()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"✓ LIME explanation plot saved to {save_path}")
            plt.close()
        
        except Exception as e:
            logger.error(f"Error plotting LIME explanation: {e}")
    
    def get_lime_feature_importance(self, instance, num_features=10):
        """
        Get feature importance from LIME for a single instance
        
        Args:
            instance: Single instance to explain
            num_features: Number of features to return
            
        Returns:
            DataFrame with feature importance
        """
        explanation = self.explain_instance_lime(instance, num_features)
        
        if explanation is None:
            return None
        
        # Get explanation as list
        exp_list = explanation.as_list()
        
        # Parse feature names and importances
        features = []
        importances = []
        
        for item in exp_list:
            feature_desc = item[0]
            importance = item[1]
            
            # Extract feature name (before comparison operator)
            feature_name = feature_desc.split('<=')[0].split('>')[0].split('<')[0].strip()
            
            features.append(feature_name)
            importances.append(importance)
        
        importance_df = pd.DataFrame({
            'feature': features,
            'importance': importances
        })
        
        # Sort by absolute importance
        importance_df['abs_importance'] = importance_df['importance'].abs()
        importance_df = importance_df.sort_values('abs_importance', ascending=False)
        importance_df = importance_df.drop('abs_importance', axis=1)
        
        return importance_df
    
    def generate_text_explanation(self, instance, prediction_proba, feature_importance_df, disease_name=None):
        """
        Generate human-readable text explanation with medical knowledge
        
        Args:
            instance: Input instance
            prediction_proba: Prediction probability
            feature_importance_df: DataFrame with feature importance
            disease_name: Name of the disease for medical context
            
        Returns:
            Text explanation string
        """
        # Try to use medical knowledge base
        if disease_name:
            try:
                from src.explainability.medical_knowledge import get_disease_explanation
                detailed_explanation = get_disease_explanation(
                    disease_name, 
                    prediction_proba, 
                    feature_importance_df, 
                    instance, 
                    self.feature_names
                )
                if detailed_explanation:
                    return detailed_explanation
            except Exception as e:
                logger.warning(f"Could not generate medical explanation: {e}")
        
        # Fallback to basic explanation
        risk_level = "High" if prediction_proba >= 0.7 else ("Medium" if prediction_proba >= 0.3 else "Low")
        
        explanation = f"**Risk Level: {risk_level}** (Probability: {prediction_proba:.2%})\n\n"
        explanation += "**Key Contributing Factors:**\n\n"
        
        for idx, row in feature_importance_df.head(5).iterrows():
            feature = row['feature']
            importance = row['importance']
            
            # Get feature index
            try:
                feature_idx = self.feature_names.index(feature)
                feature_value = instance[feature_idx]
                
                direction = "increases" if importance > 0 else "decreases"
                explanation += f"- **{feature}** (value: {feature_value:.2f}): {direction} risk\n"
            except:
                explanation += f"- **{feature}**: contributes to risk assessment\n"
        
        explanation += "\n**Medical Interpretation:**\n"
        explanation += "The model's prediction is based on the analysis of patient health parameters. "
        explanation += "Features with higher importance values have more influence on the prediction. "
        explanation += "Positive importance increases disease risk, while negative importance decreases it."
        
        return explanation
