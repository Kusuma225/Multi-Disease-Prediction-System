"""
Visualization utilities for model results and predictions
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.logger import setup_logger

logger = setup_logger('visualization', 'logs/visualization.log')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


class ResultVisualizer:
    """Visualization class for model results"""
    
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else Path('results/plots')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_training_history(self, history, save_path=None):
        """Plot training history for neural networks"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Accuracy
        ax1.plot(history.history['accuracy'], label='Train Accuracy')
        if 'val_accuracy' in history.history:
            ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Loss
        ax2.plot(history.history['loss'], label='Train Loss')
        if 'val_loss' in history.history:
            ax2.plot(history.history['val_loss'], label='Val Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Training history saved to {save_path}")
        plt.close()
    
    def plot_multi_disease_comparison(self, results_dict, save_path=None):
        """
        Plot comparison across multiple diseases
        
        Args:
            results_dict: Dictionary with disease names as keys and metrics as values
        """
        diseases = list(results_dict.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        data = {metric: [] for metric in metrics}
        
        for disease in diseases:
            for metric in metrics:
                data[metric].append(results_dict[disease].get(metric, 0))
        
        df = pd.DataFrame(data, index=diseases)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        df.plot(kind='bar', ax=ax, width=0.8)
        
        plt.title('Multi-Disease Model Performance Comparison', fontsize=16, fontweight='bold')
        plt.xlabel('Disease', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.legend(title='Metrics', fontsize=10)
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 1.1)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Multi-disease comparison saved to {save_path}")
        plt.close()
        
        return df
    
    def plot_feature_importance_comparison(self, feature_importance_dict, top_n=15, save_path=None):
        """
        Plot feature importance comparison across models
        
        Args:
            feature_importance_dict: Dict with model names as keys and feature importance as values
        """
        fig, axes = plt.subplots(len(feature_importance_dict), 1, 
                                figsize=(12, 4*len(feature_importance_dict)))
        
        if len(feature_importance_dict) == 1:
            axes = [axes]
        
        for idx, (model_name, importance_df) in enumerate(feature_importance_dict.items()):
            importance_df = importance_df.head(top_n).sort_values('importance')
            
            axes[idx].barh(importance_df['feature'], importance_df['importance'])
            axes[idx].set_title(f'Feature Importance - {model_name}', fontsize=12, fontweight='bold')
            axes[idx].set_xlabel('Importance')
            axes[idx].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Feature importance comparison saved to {save_path}")
        plt.close()
    
    def create_interactive_model_comparison(self, results_dict, save_path=None):
        """Create interactive Plotly comparison chart"""
        diseases = list(results_dict.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        fig = go.Figure()
        
        for metric in metrics:
            values = [results_dict[disease].get(metric, 0) for disease in diseases]
            
            fig.add_trace(go.Bar(
                name=metric.replace('_', ' ').title(),
                x=diseases,
                y=values,
                text=[f'{v:.3f}' for v in values],
                textposition='auto',
            ))
        
        fig.update_layout(
            title='Multi-Disease Model Performance',
            xaxis_title='Disease',
            yaxis_title='Score',
            barmode='group',
            height=600,
            showlegend=True,
            hovermode='x unified'
        )
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"✓ Interactive comparison saved to {save_path}")
        
        return fig
    
    def plot_confusion_matrix_grid(self, confusion_matrices, save_path=None):
        """
        Plot grid of confusion matrices for multiple diseases
        
        Args:
            confusion_matrices: Dict with disease names as keys and confusion matrices as values
        """
        n_diseases = len(confusion_matrices)
        n_cols = 3
        n_rows = (n_diseases + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten()
        
        for idx, (disease, cm) in enumerate(confusion_matrices.items()):
            if idx < len(axes):
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                           xticklabels=['Negative', 'Positive'],
                           yticklabels=['Negative', 'Positive'])
                axes[idx].set_title(f'{disease.replace("_", " ").title()}')
                axes[idx].set_ylabel('True Label')
                axes[idx].set_xlabel('Predicted Label')
        
        # Hide unused subplots
        for idx in range(len(confusion_matrices), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Confusion matrix grid saved to {save_path}")
        plt.close()
    
    def create_performance_radar_chart(self, metrics_dict, save_path=None):
        """Create radar chart for model performance"""
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        fig = go.Figure()
        
        for model_name, model_metrics in metrics_dict.items():
            values = [model_metrics.get(m, 0) for m in metrics]
            values.append(values[0])  # Close the polygon
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics + [metrics[0]],
                fill='toself',
                name=model_name
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title='Model Performance Radar Chart',
            height=600
        )
        
        if save_path:
            fig.write_html(save_path)
            logger.info(f"✓ Radar chart saved to {save_path}")
        
        return fig
    
    def plot_risk_distribution(self, predictions, save_path=None):
        """Plot distribution of risk predictions"""
        risk_counts = pd.Series(predictions).value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Bar chart
        risk_counts.plot(kind='bar', ax=ax1, color=['green', 'orange', 'red'])
        ax1.set_title('Risk Level Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Risk Level')
        ax1.set_ylabel('Count')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
        
        # Pie chart
        ax2.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%',
               colors=['green', 'orange', 'red'], startangle=90)
        ax2.set_title('Risk Level Percentage', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Risk distribution saved to {save_path}")
        plt.close()


def generate_all_visualizations(project_root):
    """Generate all visualizations for the project"""
    logger.info("Generating all visualizations...")
    
    project_root = Path(project_root)
    visualizer = ResultVisualizer(project_root / 'results' / 'plots')
    
    # Load all results
    results_dict = {}
    diseases = ['diabetes', 'heart_disease', 'liver_disease', 'kidney_disease',
               'breast_cancer', 'parkinsons', 'stroke', 'hypertension', 'anemia', 'thyroid']
    
    for disease in diseases:
        best_model_path = project_root / 'results' / 'metrics' / disease / 'best_model.json'
        if best_model_path.exists():
            import json
            with open(best_model_path, 'r') as f:
                best_info = json.load(f)
            
            best_model_name = best_info['best_model']
            metrics_path = project_root / 'results' / 'metrics' / disease / f'{best_model_name}_metrics.json'
            
            if metrics_path.exists():
                with open(metrics_path, 'r') as f:
                    metrics = json.load(f)
                results_dict[disease] = metrics
    
    if results_dict:
        # Multi-disease comparison
        comparison_path = project_root / 'results' / 'plots' / 'multi_disease_comparison.png'
        visualizer.plot_multi_disease_comparison(results_dict, comparison_path)
        
        # Interactive comparison
        interactive_path = project_root / 'results' / 'plots' / 'interactive_comparison.html'
        visualizer.create_interactive_model_comparison(results_dict, interactive_path)
        
        # Confusion matrix grid
        confusion_matrices = {}
        for disease, metrics in results_dict.items():
            if 'confusion_matrix' in metrics:
                confusion_matrices[disease] = np.array(metrics['confusion_matrix'])
        
        if confusion_matrices:
            cm_grid_path = project_root / 'results' / 'plots' / 'confusion_matrix_grid.png'
            visualizer.plot_confusion_matrix_grid(confusion_matrices, cm_grid_path)
        
        logger.info("✓ All visualizations generated")
    else:
        logger.warning("No results found to visualize")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    generate_all_visualizations(project_root)
