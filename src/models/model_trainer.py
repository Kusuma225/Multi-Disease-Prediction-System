"""
Model training module with multiple ML algorithms
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
try:
    from lightgbm import LGBMClassifier
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score

# Models with large search spaces → RandomizedSearchCV
_RANDOM_SEARCH_MODELS = {'random_forest', 'xgboost', 'lightgbm', 'neural_network'}
_RANDOM_SEARCH_ITER = 20   # 20 random draws × 5-fold CV = 100 fits per model
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix, 
                             classification_report, roc_curve)
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — required for background/headless runs
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config
from src.utils.model_utils import save_model, save_metrics

logger = setup_logger('model_training', 'logs/model_training.log')


class ModelTrainer:
    """Model training and evaluation class"""
    
    def __init__(self, config=None):
        if config is None:
            config = load_config()
        self.config = config
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.results = {}
        
    def initialize_models(self):
        """Initialize all ML models"""
        logger.info("Initializing models...")
        
        random_state = self.config['preprocessing']['random_state']
        
        self.models = {
            'logistic_regression': LogisticRegression(
                max_iter=1000,
                random_state=random_state
            ),
            'random_forest': RandomForestClassifier(
                random_state=random_state
            ),
            'xgboost': XGBClassifier(
                random_state=random_state,
                eval_metric='logloss'
            ),
            'svm': SVC(
                probability=True,
                random_state=random_state
            ),
            'neural_network': MLPClassifier(
                max_iter=1000,
                random_state=random_state
            )
        }
        
        # Add LightGBM if available (Patel 2024: outperforms XGBoost for tabular medical data)
        if LIGHTGBM_AVAILABLE:
            self.models['lightgbm'] = LGBMClassifier(
                random_state=random_state,
                verbose=-1
            )
            logger.info("✓ LightGBM added to model pool")
        
        logger.info(f"✓ {len(self.models)} models initialized")
        return self.models
    
    def get_param_grid(self, model_name):
        """Get hyperparameter grid for model"""
        hyperparams = self.config['models']['hyperparameters']
        
        param_grids = {
            'logistic_regression': {
                'C': hyperparams['logistic_regression']['C']
            },
            'random_forest': {
                'n_estimators': hyperparams['random_forest']['n_estimators'],
                'max_depth': hyperparams['random_forest']['max_depth'],
                'min_samples_split': hyperparams['random_forest']['min_samples_split']
            },
            'xgboost': {
                'n_estimators': hyperparams['xgboost']['n_estimators'],
                'max_depth': hyperparams['xgboost']['max_depth'],
                'learning_rate': hyperparams['xgboost']['learning_rate']
            },
            'svm': {
                'C': hyperparams['svm']['C'],
                'kernel': hyperparams['svm']['kernel'],
                'gamma': hyperparams['svm']['gamma']
            },
            'neural_network': {
                'hidden_layer_sizes': hyperparams['neural_network']['hidden_layers'],
                'activation': hyperparams['neural_network']['activation'],
                'learning_rate_init': hyperparams['neural_network']['learning_rate']
            },
            'lightgbm': {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.05, 0.1],
                'num_leaves': [31, 63]
            }
        }
        
        return param_grids.get(model_name, {})
    
    def train_model(self, model_name, X_train, y_train, tune_hyperparameters=True):
        """
        Train a single model with optional hyperparameter tuning
        
        Args:
            model_name: Name of the model
            X_train: Training features
            y_train: Training labels
            tune_hyperparameters: Whether to perform hyperparameter tuning
            
        Returns:
            Trained model
        """
        logger.info(f"Training {model_name}...")
        
        model = self.models[model_name]
        
        if tune_hyperparameters:
            param_grid = self.get_param_grid(model_name)

            if param_grid:
                if model_name in _RANDOM_SEARCH_MODELS:
                    logger.info(f"RandomizedSearchCV (n_iter={_RANDOM_SEARCH_ITER}) for {model_name}...")
                    search = RandomizedSearchCV(
                        model,
                        param_grid,
                        n_iter=_RANDOM_SEARCH_ITER,
                        cv=self.config['preprocessing']['cv_folds'],
                        scoring=self.config['evaluation']['primary_metric'],
                        n_jobs=-1,
                        random_state=42,
                        verbose=0,
                    )
                else:
                    logger.info(f"GridSearchCV for {model_name}...")
                    search = GridSearchCV(
                        model,
                        param_grid,
                        cv=self.config['preprocessing']['cv_folds'],
                        scoring=self.config['evaluation']['primary_metric'],
                        n_jobs=-1,
                        verbose=0,
                    )

                search.fit(X_train, y_train)
                model = search.best_estimator_
                logger.info(f"Best parameters for {model_name}: {search.best_params_}")
            else:
                model.fit(X_train, y_train)
        else:
            model.fit(X_train, y_train)
        
        logger.info(f"✓ {model_name} training completed")
        return model
    
    def evaluate_model(self, model, model_name, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            model: Trained model
            model_name: Name of the model
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of metrics
        """
        logger.info(f"Evaluating {model_name}...")
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='binary', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='binary', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='binary', zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 0.0,
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred, zero_division=0)
        }
        
        logger.info(f"✓ {model_name} evaluation completed")
        logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall: {metrics['recall']:.4f}")
        logger.info(f"  F1-Score: {metrics['f1_score']:.4f}")
        logger.info(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
        
        return metrics
    
    def train_all_models(self, X_train, y_train, X_test, y_test, tune_hyperparameters=True):
        """
        Train and evaluate all models
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_test: Test features
            y_test: Test labels
            tune_hyperparameters: Whether to perform hyperparameter tuning
            
        Returns:
            Dictionary of results for all models
        """
        self.initialize_models()
        
        for model_name in self.models.keys():
            try:
                # Train model
                trained_model = self.train_model(model_name, X_train, y_train, tune_hyperparameters)
                
                # Evaluate model
                metrics = self.evaluate_model(trained_model, model_name, X_test, y_test)
                
                # Store results
                self.results[model_name] = {
                    'model': trained_model,
                    'metrics': metrics
                }
                
            except Exception as e:
                logger.error(f"Error training {model_name}: {e}")
                continue
        
        # Select best model
        self.select_best_model()
        
        return self.results
    
    def select_best_model(self):
        """Select the best performing model based on primary metric"""
        primary_metric = self.config['evaluation']['primary_metric']
        
        best_score = -1
        best_name = None
        
        for model_name, result in self.results.items():
            score = result['metrics'][primary_metric]
            if score > best_score:
                best_score = score
                best_name = model_name
        
        if best_name:
            self.best_model_name = best_name
            self.best_model = self.results[best_name]['model']
            logger.info(f"✓ Best model: {best_name} ({primary_metric}: {best_score:.4f})")
        
        return self.best_model, self.best_model_name
    
    def plot_confusion_matrix(self, model_name, save_path=None):
        """Plot confusion matrix for a model"""
        if model_name not in self.results:
            logger.error(f"Model {model_name} not found in results")
            return
        
        cm = np.array(self.results[model_name]['metrics']['confusion_matrix'])
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Negative', 'Positive'],
                   yticklabels=['Negative', 'Positive'])
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Confusion matrix saved to {save_path}")
        plt.close()
    
    def plot_roc_curve(self, X_test, y_test, save_path=None):
        """Plot ROC curves for all models"""
        plt.figure(figsize=(10, 8))
        
        for model_name, result in self.results.items():
            model = result['model']
            
            if hasattr(model, 'predict_proba'):
                y_pred_proba = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
                auc = result['metrics']['roc_auc']
                
                plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves - Model Comparison')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ ROC curves saved to {save_path}")
        plt.close()
    
    def plot_model_comparison(self, save_path=None):
        """Plot comparison of all models"""
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        comparison_data = {}
        for metric in metrics:
            comparison_data[metric] = []
            for model_name in self.results.keys():
                comparison_data[metric].append(self.results[model_name]['metrics'][metric])
        
        df_comparison = pd.DataFrame(comparison_data, index=list(self.results.keys()))
        
        fig, ax = plt.subplots(figsize=(12, 6))
        df_comparison.plot(kind='bar', ax=ax)
        plt.title('Model Performance Comparison')
        plt.xlabel('Models')
        plt.ylabel('Score')
        plt.legend(title='Metrics')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Model comparison plot saved to {save_path}")
        plt.close()
        
        return df_comparison
    
    def save_results(self, disease_name, output_dir):
        """Save all models and results"""
        output_dir = Path(output_dir)
        
        # Save each model
        for model_name, result in self.results.items():
            model_path = output_dir / 'models' / disease_name / f'{model_name}.pkl'
            save_model(result['model'], model_path)
            
            # Save metrics
            metrics_path = output_dir / 'results' / 'metrics' / disease_name / f'{model_name}_metrics.json'
            save_metrics(result['metrics'], metrics_path)
        
        # Save best model indicator
        best_model_info = {
            'best_model': self.best_model_name,
            'best_score': self.results[self.best_model_name]['metrics'][self.config['evaluation']['primary_metric']]
        }
        best_model_path = output_dir / 'results' / 'metrics' / disease_name / 'best_model.json'
        save_metrics(best_model_info, best_model_path)
        
        logger.info(f"✓ All results saved for {disease_name}")
