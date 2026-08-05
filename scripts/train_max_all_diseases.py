"""
MAX-PERFORMANCE training script — all 20 diseases.
Uses 10-fold CV + expanded hyperparameter grids (see config.yaml).
Run after generate_maxperf_datasets.py has refreshed the 11 synthetic datasets.

Usage:
    python3 scripts/train_max_all_diseases.py
    # or background:
    nohup python3 scripts/train_max_all_diseases.py > logs/train_max_all.log 2>&1 &
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import sys
import time

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.preprocessing.data_preprocessor import DataPreprocessor
from src.preprocessing.eda import EDAAnalyzer
from src.models.model_trainer import ModelTrainer
from src.utils.logger import setup_logger
from src.utils.config_utils import load_config, get_disease_config

logger = setup_logger('train_max_all', 'logs/train_max_all.log')

# Remaining diseases — heart_disease (old Feb 20 run) + 11 synthetic (new N=10000 data)
ALL_DISEASES = [
    'heart_disease',
    'kidney_disease',
    'parkinsons',
    'pneumonia',
    'alzheimers',
    'asthma',
    'tuberculosis',
    'malaria',
    'hepatitis',
    'osteoporosis',
    'arthritis',
    'covid19',
]


def train_disease_model(disease_name: str, config: dict) -> bool:
    """Train all 6 models for a single disease and save results."""
    logger.info(f"\n{'='*65}")
    logger.info(f"  TRAINING: {disease_name.upper()}")
    logger.info(f"{'='*65}")

    try:
        # ── Resolve target column ──────────────────────────────────────
        disease_config = get_disease_config(disease_name)
        target_column = disease_config['target_column'] if disease_config else 'Outcome'

        # ── Load data ─────────────────────────────────────────────────
        data_path = project_root / 'data' / 'raw' / f'{disease_name}.csv'
        if not data_path.exists():
            logger.error(f"Dataset not found: {data_path}")
            return False

        df = pd.read_csv(data_path)
        logger.info(f"Loaded {data_path.name}  shape={df.shape}")

        # Fallback target column detection
        if target_column not in df.columns:
            candidates = [c for c in df.columns
                          if 'target' in c.lower() or 'outcome' in c.lower()
                          or 'classification' in c.lower() or 'status' in c.lower()
                          or 'positive' in c.lower()]
            target_column = candidates[0] if candidates else df.columns[-1]

        logger.info(f"Target column: '{target_column}'  "
                    f"pos_rate={df[target_column].mean():.1%}")

        # ── EDA (quick, non-blocking) ──────────────────────────────────
        try:
            eda = EDAAnalyzer(df, target_column)
            eda_dir = project_root / 'results' / 'eda' / disease_name
            eda.generate_full_report(eda_dir)
        except Exception as e:
            logger.warning(f"EDA skipped for {disease_name}: {e}")

        # ── Preprocess ────────────────────────────────────────────────
        preprocessor = DataPreprocessor(config)
        X_train, X_test, y_train, y_test, feature_names = \
            preprocessor.prepare_data(df, target_column)

        preprocessor.save_preprocessor(
            project_root / 'models' / disease_name / 'preprocessor.pkl')

        # ── Save training sample for SHAP/LIME ────────────────────────
        sample_size = min(200, len(X_train))
        idx = np.random.choice(len(X_train), sample_size, replace=False)
        joblib.dump(X_train[idx],
                    project_root / 'models' / disease_name / 'X_train_sample.pkl')
        logger.info(f"Saved {sample_size} training samples for explainer")

        # ── Train & evaluate all 6 models ─────────────────────────────
        trainer = ModelTrainer(config)
        t0 = time.time()
        results = trainer.train_all_models(
            X_train, y_train, X_test, y_test, tune_hyperparameters=True)
        elapsed = (time.time() - t0) / 60

        # ── Persist results ───────────────────────────────────────────
        trainer.save_results(disease_name, project_root)

        # ── Generate plots ────────────────────────────────────────────
        plots_dir = project_root / 'results' / 'plots' / disease_name
        plots_dir.mkdir(parents=True, exist_ok=True)
        for model_name in results:
            trainer.plot_confusion_matrix(
                model_name, plots_dir / f'{model_name}_confusion_matrix.png')
        trainer.plot_roc_curve(X_test, y_test, plots_dir / 'roc_curves.png')
        trainer.plot_model_comparison(plots_dir / 'model_comparison.png')

        # ── Summary line ──────────────────────────────────────────────
        best_auc = max(r['metrics']['roc_auc'] for r in results.values())
        logger.info(f"✅ {disease_name:22s}  best_AUC={best_auc:.4f}  "
                    f"({elapsed:.1f} min)")
        return True

    except Exception as exc:
        import traceback
        logger.error(f"✗ {disease_name}: {exc}")
        logger.error(traceback.format_exc())
        return False


def main():
    config = load_config()

    logger.info("\n" + "=" * 65)
    logger.info("  MAX-PERFORMANCE TRAINING — ALL 20 DISEASES")
    logger.info("  10-fold CV  |  Expanded grids  |  N=10,000 synthetic")
    logger.info("=" * 65)
    logger.info(f"Diseases: {', '.join(ALL_DISEASES)}\n")

    overall_start = time.time()
    ok, fail = 0, 0
    failed_list = []

    for i, disease in enumerate(ALL_DISEASES, 1):
        logger.info(f"\n[{i:02d}/{len(ALL_DISEASES)}] Starting {disease}...")
        success = train_disease_model(disease, config)
        if success:
            ok += 1
        else:
            fail += 1
            failed_list.append(disease)

    total_min = (time.time() - overall_start) / 60

    logger.info(f"\n{'='*65}")
    logger.info("  TRAINING COMPLETE")
    logger.info(f"{'='*65}")
    logger.info(f"  Successful : {ok}/{len(ALL_DISEASES)}")
    logger.info(f"  Failed     : {fail}")
    logger.info(f"  Total time : {total_min:.1f} minutes")
    if failed_list:
        logger.info(f"  Failed list: {', '.join(failed_list)}")
    logger.info("=" * 65)


if __name__ == "__main__":
    main()
