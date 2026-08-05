"""
EDA (Exploratory Data Analysis) utilities
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger

logger = setup_logger('eda', 'logs/eda.log')


class EDAAnalyzer:
    """Exploratory Data Analysis class"""
    
    def __init__(self, df, target_column):
        self.df = df.copy()
        self.target_column = target_column
        
    def get_basic_info(self):
        """Get basic information about the dataset"""
        info = {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicates': self.df.duplicated().sum()
        }
        return info
    
    def get_statistical_summary(self):
        """Get statistical summary of numeric columns"""
        return self.df.describe()
    
    def get_target_distribution(self):
        """Get distribution of target variable"""
        return self.df[self.target_column].value_counts()
    
    def plot_target_distribution(self, save_path=None):
        """Plot target variable distribution"""
        plt.figure(figsize=(8, 6))
        self.df[self.target_column].value_counts().plot(kind='bar')
        plt.title(f'Distribution of {self.target_column}')
        plt.xlabel(self.target_column)
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Target distribution plot saved to {save_path}")
        plt.close()
    
    def plot_correlation_matrix(self, save_path=None):
        """Plot correlation matrix"""
        plt.figure(figsize=(12, 10))
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        
        sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('Correlation Matrix')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Correlation matrix saved to {save_path}")
        plt.close()
    
    def plot_feature_distributions(self, save_path=None):
        """Plot distributions of all numeric features"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != self.target_column]
        
        n_cols = 4
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes]
        
        for idx, col in enumerate(numeric_cols):
            if idx < len(axes):
                self.df[col].hist(bins=30, ax=axes[idx])
                axes[idx].set_title(col)
                axes[idx].set_xlabel('Value')
                axes[idx].set_ylabel('Frequency')
        
        # Hide unused subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Feature distributions saved to {save_path}")
        plt.close()
    
    def plot_boxplots(self, save_path=None):
        """Plot boxplots for outlier detection"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != self.target_column]
        
        n_cols = 4
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes]
        
        for idx, col in enumerate(numeric_cols):
            if idx < len(axes):
                self.df.boxplot(column=col, ax=axes[idx])
                axes[idx].set_title(col)
        
        # Hide unused subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Boxplots saved to {save_path}")
        plt.close()
    
    def generate_full_report(self, output_dir):
        """Generate complete EDA report with all visualizations"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Generating EDA report...")
        
        # Save basic info
        info = self.get_basic_info()
        with open(output_dir / 'basic_info.txt', 'w') as f:
            f.write("Dataset Information\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Shape: {info['shape']}\n")
            f.write(f"Duplicates: {info['duplicates']}\n\n")
            f.write("Missing Values:\n")
            for col, missing in info['missing_values'].items():
                if missing > 0:
                    f.write(f"  {col}: {missing}\n")
        
        # Generate plots
        self.plot_target_distribution(output_dir / 'target_distribution.png')
        self.plot_correlation_matrix(output_dir / 'correlation_matrix.png')
        self.plot_feature_distributions(output_dir / 'feature_distributions.png')
        self.plot_boxplots(output_dir / 'boxplots.png')
        
        logger.info(f"✓ EDA report generated at {output_dir}")
