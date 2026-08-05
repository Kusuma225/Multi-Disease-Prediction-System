# Dataset Information

This directory contains datasets for 10 different diseases.

## Diseases and Datasets

### 1. Diabetes
- **File**: `diabetes.csv`
- **Source**: Kaggle - Pima Indians Diabetes Database
- **Features**: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
- **Target**: Outcome (0: No Diabetes, 1: Diabetes)

### 2. Heart Disease
- **File**: `heart_disease.csv`
- **Source**: UCI ML Repository - Cleveland Heart Disease Database
- **Features**: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
- **Target**: target (0: No Disease, 1: Disease)

### 3. Liver Disease
- **File**: `liver_disease.csv`
- **Source**: UCI ML Repository - Indian Liver Patient Records
- **Features**: Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Proteins, Albumin, Albumin_and_Globulin_Ratio
- **Target**: Dataset (1: Patient, 2: Non-patient)

### 4. Kidney Disease
- **File**: `kidney_disease.csv`
- **Source**: UCI ML Repository - Chronic Kidney Disease
- **Features**: age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc, sod, pot, hemo, pcv, wc, rc, htn, dm, cad, appet, pe, ane
- **Target**: classification (ckd, notckd)

### 5. Breast Cancer
- **File**: `breast_cancer.csv`
- **Source**: UCI ML Repository - Breast Cancer Wisconsin (Diagnostic)
- **Features**: radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean, compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean (and more)
- **Target**: diagnosis (M: Malignant, B: Benign)

### 6. Parkinson's Disease
- **File**: `parkinsons.csv`
- **Source**: UCI ML Repository - Parkinsons Data Set
- **Features**: MDVP:Fo(Hz), MDVP:Fhi(Hz), MDVP:Flo(Hz), MDVP:Jitter(%), MDVP:Jitter(Abs), MDVP:RAP, MDVP:PPQ, Jitter:DDP, MDVP:Shimmer, etc.
- **Target**: status (0: Healthy, 1: Parkinson's)

### 7. Stroke
- **File**: `stroke.csv`
- **Source**: Kaggle - Stroke Prediction Dataset
- **Features**: gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status
- **Target**: stroke (0: No Stroke, 1: Stroke)

### 8. Hypertension
- **File**: `hypertension.csv`
- **Source**: Synthetic (created from stroke and heart disease datasets)
- **Features**: age, gender, systolic_bp, diastolic_bp, cholesterol, glucose, bmi, smoking, alcohol, physical_activity, family_history
- **Target**: hypertension (0: No, 1: Yes)

### 9. Anemia
- **File**: `anemia.csv`
- **Source**: Kaggle - Anemia Types Classification
- **Features**: age, gender, hemoglobin, mch, mchc, mcv, rbc_count, wbc_count, platelet_count, iron, ferritin
- **Target**: anemia (0: No, 1: Yes)

### 10. Thyroid Disorder
- **File**: `thyroid.csv`
- **Source**: UCI ML Repository - Thyroid Disease Data
- **Features**: age, sex, TSH, T3, TT4, T4U, FTI
- **Target**: target (0: Normal, 1: Disorder)

## Data Preprocessing Steps

All datasets undergo the following preprocessing:

1. **Missing Value Handling**
   - Numeric: Median imputation
   - Categorical: Mode imputation

2. **Outlier Detection**
   - IQR method with capping

3. **Feature Encoding**
   - Label encoding for categorical variables

4. **Feature Scaling**
   - StandardScaler normalization

5. **Class Imbalance**
   - SMOTE oversampling

## Download Instructions

Run the dataset download script:

```bash
python scripts/download_datasets.py
```

This will create sample datasets for all 10 diseases in the `data/raw/` directory.

## Notes

- The datasets provided are samples for demonstration purposes
- For real clinical applications, use verified medical datasets
- Always ensure patient data privacy and ethical guidelines
- Consult with medical professionals for clinical deployment

## References

- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
