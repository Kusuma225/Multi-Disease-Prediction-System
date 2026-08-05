"""
Data preprocessing module for all diseases
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config

logger = setup_logger('preprocessing', 'logs/preprocessing.log')


class DataPreprocessor:
    """Data preprocessing class for medical datasets"""
    
    def __init__(self, config=None):
        if config is None:
            config = load_config()
        self.config = config
        self.preprocessing_config = config['preprocessing']
        self.scaler = None
        self.label_encoders = {}
        self.feature_names = None
        
    def load_data(self, filepath):
        """Load dataset from CSV file"""
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Data loaded. Shape: {df.shape}")
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        logger.info("Handling missing values...")
        
        # Separate numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Handle numeric columns
        if len(numeric_cols) > 0:
            strategy = self.preprocessing_config['missing_value_strategy']['numeric']
            numeric_imputer = SimpleImputer(strategy=strategy)
            df[numeric_cols] = numeric_imputer.fit_transform(df[numeric_cols])
        
        # Handle categorical columns
        if len(categorical_cols) > 0:
            strategy = self.preprocessing_config['missing_value_strategy']['categorical']
            cat_imputer = SimpleImputer(strategy='most_frequent')
            df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
        
        logger.info(f"✓ Missing values handled")
        return df
    
    def encode_categorical(self, df, target_column):
        """Encode categorical variables"""
        logger.info("Encoding categorical variables...")
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col != target_column]
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
        
        # Encode target if it's categorical
        if df[target_column].dtype == 'object':
            le = LabelEncoder()
            df[target_column] = le.fit_transform(df[target_column])
            self.label_encoders[target_column] = le
        
        logger.info(f"✓ Categorical encoding completed")
        return df
    
    def remove_duplicates(self, df):
        """Remove duplicate rows"""
        initial_shape = df.shape
        df = df.drop_duplicates()
        removed = initial_shape[0] - df.shape[0]
        logger.info(f"✓ Removed {removed} duplicate rows")
        return df
    
    def handle_outliers(self, df, target_column, method='iqr', threshold=1.5):
        """Handle outliers using IQR method"""
        logger.info("Handling outliers...")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != target_column]
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            # Cap outliers instead of removing
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        logger.info(f"✓ Outliers handled")
        return df
    
    def scale_features(self, X_train, X_test):
        """Scale features using StandardScaler or MinMaxScaler"""
        logger.info("Scaling features...")
        
        scaling_method = self.preprocessing_config['scaling_method']
        
        if scaling_method == 'standard':
            self.scaler = StandardScaler()
        elif scaling_method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            self.scaler = StandardScaler()
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        logger.info(f"✓ Features scaled using {scaling_method}")
        return X_train_scaled, X_test_scaled
    
    def handle_imbalance(self, X_train, y_train):
        """Handle class imbalance using SMOTE"""
        logger.info("Handling class imbalance...")
        
        method = self.preprocessing_config['imbalance_handling']['method']
        
        if method == 'smote':
            try:
                smote = SMOTE(random_state=self.preprocessing_config['random_state'])
                X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
                logger.info(f"✓ Class imbalance handled using SMOTE")
                logger.info(f"Original shape: {X_train.shape}, Balanced shape: {X_train_balanced.shape}")
                return X_train_balanced, y_train_balanced
            except Exception as e:
                logger.warning(f"SMOTE failed: {e}. Using original data.")
                return X_train, y_train
        else:
            return X_train, y_train
    
    def prepare_data(self, df, target_column):
        """
        Complete preprocessing pipeline
        
        Args:
            df: Input dataframe
            target_column: Name of target column
            
        Returns:
            X_train, X_test, y_train, y_test, feature_names
        """
        logger.info("Starting preprocessing pipeline...")
        
        # Remove duplicates
        df = self.remove_duplicates(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Encode categorical variables
        df = self.encode_categorical(df, target_column)
        
        # Handle outliers
        df = self.handle_outliers(df, target_column)
        
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        self.feature_names = X.columns.tolist()
        
        # Split data
        test_size = self.preprocessing_config['test_size']
        random_state = self.preprocessing_config['random_state']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Train set size: {X_train.shape}, Test set size: {X_test.shape}")
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        # Handle imbalance (only on training set)
        X_train_balanced, y_train_balanced = self.handle_imbalance(X_train_scaled, y_train)
        
        logger.info("✓ Preprocessing pipeline completed")
        
        return X_train_balanced, X_test_scaled, y_train_balanced, y_test, self.feature_names
    
    def save_preprocessor(self, filepath):
        """Save preprocessor objects"""
        import joblib
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }
        
        joblib.dump(preprocessor_data, filepath)
        logger.info(f"✓ Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath):
        """Load preprocessor objects"""
        import joblib
        preprocessor_data = joblib.load(filepath)
        
        self.scaler = preprocessor_data['scaler']
        self.label_encoders = preprocessor_data['label_encoders']
        self.feature_names = preprocessor_data['feature_names']
        
        logger.info(f"✓ Preprocessor loaded from {filepath}")
