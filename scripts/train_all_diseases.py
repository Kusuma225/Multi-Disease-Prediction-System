"""
Main training script for all diseases
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import sys
import gc
import warnings
import os

# Suppress joblib resource tracker warnings
warnings.filterwarnings('ignore', category=UserWarning, module='joblib')
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.preprocessing.data_preprocessor import DataPreprocessor
from src.preprocessing.eda import EDAAnalyzer
from src.models.model_trainer import ModelTrainer
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config, get_disease_config

logger = setup_logger('train_all', 'logs/train_all.log')


def train_disease_model(disease_name, config):
    """
    Train models for a single disease
    
    Args:
        disease_name: Name of the disease
        config: Configuration dictionary
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Training models for: {disease_name.upper()}")
    logger.info(f"{'='*60}")
    
    try:
        # Get disease configuration
        disease_config = get_disease_config(disease_name)
        if disease_config is None:
            logger.error(f"Configuration not found for {disease_name}")
            return False
        
        target_column = disease_config['target_column']
        
        # Load data
        data_path = project_root / 'data' / 'raw' / f'{disease_name}.csv'
        if not data_path.exists():
            logger.error(f"Dataset not found: {data_path}")
            return False
        
        logger.info(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        logger.info(f"Data loaded. Shape: {df.shape}")
        
        # Perform EDA
        logger.info("Performing Exploratory Data Analysis...")
        eda = EDAAnalyzer(df, target_column)
        eda_output_dir = project_root / 'results' / 'eda' / disease_name
        eda.generate_full_report(eda_output_dir)
        
        # Preprocess data
        logger.info("Preprocessing data...")
        preprocessor = DataPreprocessor(config)
        X_train, X_test, y_train, y_test, feature_names = preprocessor.prepare_data(df, target_column)
        
        # Save preprocessor
        preprocessor_path = project_root / 'models' / disease_name / 'preprocessor.pkl'
        preprocessor.save_preprocessor(preprocessor_path)
        
        # Save a sample of training data for SHAP explainer
        logger.info("Saving training sample for explainer...")
        import numpy as np
        sample_size = min(100, len(X_train))
        sample_indices = np.random.choice(len(X_train), sample_size, replace=False)
        X_train_sample = X_train[sample_indices]
        
        train_sample_path = project_root / 'models' / disease_name / 'X_train_sample.pkl'
        joblib.dump(X_train_sample, train_sample_path)
        logger.info(f"Saved {sample_size} training samples for explainer")
        
        # Train models
        logger.info("Training models...")
        trainer = ModelTrainer(config)
        results = trainer.train_all_models(X_train, y_train, X_test, y_test, tune_hyperparameters=True)
        
        # Save results
        trainer.save_results(disease_name, project_root)
        
        # Generate visualizations
        logger.info("Generating visualizations...")
        plots_dir = project_root / 'results' / 'plots' / disease_name
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Confusion matrices
        for model_name in results.keys():
            cm_path = plots_dir / f'{model_name}_confusion_matrix.png'
            trainer.plot_confusion_matrix(model_name, cm_path)
        
        # ROC curves
        roc_path = plots_dir / 'roc_curves.png'
        trainer.plot_roc_curve(X_test, y_test, roc_path)
        
        # Model comparison
        comparison_path = plots_dir / 'model_comparison.png'
        trainer.plot_model_comparison(comparison_path)
        
        logger.info(f"✓ Training completed for {disease_name}")
        logger.info(f"Best model: {trainer.best_model_name}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error training {disease_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def train_all_diseases():
    """Train models for all diseases"""
    logger.info("\n" + "="*60)
    logger.info("MULTI-DISEASE MODEL TRAINING PIPELINE")
    logger.info("="*60)
    
    # Load configuration
    config = load_config()
    
    # Get list of diseases
    diseases = [d['name'] for d in config['diseases']]
    
    logger.info(f"\nDiseases to train: {len(diseases)}")
    for disease in diseases:
        logger.info(f"  - {disease}")
    
    # Train each disease
    results = {}
    for disease in diseases:
        success = train_disease_model(disease, config)
        results[disease] = success
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TRAINING SUMMARY")
    logger.info("="*60)
    
    successful = sum(results.values())
    failed = len(results) - successful
    
    logger.info(f"\nTotal diseases: {len(results)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    
    if failed > 0:
        logger.info("\nFailed diseases:")
        for disease, success in results.items():
            if not success:
                logger.info(f"  - {disease}")
    
    logger.info("\n" + "="*60)
    logger.info("✓ TRAINING PIPELINE COMPLETED")
    logger.info("="*60)


if __name__ == "__main__":
    import time
    start_time = time.time()
    
    train_all_diseases()
    
    elapsed_time = time.time() - start_time
    logger.info(f"\nTotal execution time: {elapsed_time/60:.2f} minutes")
    
    # Cleanup
    gc.collect()
    import time
    time.sleep(0.5)  # Give resources time to cleanup
