"""
Medical Knowledge Base for Disease Explanations
Provides information about causes, risk factors, and treatments
"""

DISEASE_KNOWLEDGE = {
    'diabetes': {
        'name': 'Diabetes',
        'description': 'A metabolic disorder characterized by elevated blood sugar levels over a prolonged period.',
        'causes': [
            'Insulin resistance (body cells don\'t respond properly to insulin)',
            'Insufficient insulin production by the pancreas',
            'Genetic predisposition and family history',
            'Obesity and excess body weight (especially abdominal fat)',
            'Sedentary lifestyle and lack of physical activity',
            'Poor diet high in refined carbohydrates and sugars',
            'Age (risk increases after 45)',
            'Hormonal imbalances and conditions (e.g., PCOS)'
        ],
        'risk_factors': {
            'age': 'Age over 45 increases risk significantly',
            'glucose': 'Elevated blood glucose (>100 mg/dL fasting) indicates impaired glucose regulation',
            'bmi': 'BMI over 25 increases risk; obesity (BMI >30) is a major risk factor',
            'blood_pressure': 'High blood pressure (>140/90) often accompanies diabetes',
            'insulin': 'High insulin levels suggest insulin resistance',
            'pregnancies': 'Multiple pregnancies increase risk, especially with gestational diabetes history'
        },
        'prevention': [
            'Maintain healthy weight (BMI 18.5-24.9)',
            'Regular physical activity (at least 150 minutes moderate exercise per week)',
            'Eat a balanced diet rich in whole grains, vegetables, and lean proteins',
            'Limit intake of refined sugars, processed foods, and saturated fats',
            'Regular health screenings, especially if family history exists',
            'Manage stress through meditation, yoga, or other relaxation techniques',
            'Get adequate sleep (7-9 hours per night)',
            'Avoid smoking and excessive alcohol consumption'
        ],
        'treatment': [
            'Lifestyle modifications (diet and exercise) as first-line treatment',
            'Blood glucose monitoring and HbA1c testing every 3-6 months',
            'Oral medications: Metformin (first-line), sulfonylureas, DPP-4 inhibitors',
            'Injectable medications: Insulin therapy (various types), GLP-1 agonists',
            'Regular consultation with endocrinologist and diabetes educator',
            'Eye exams, foot care, and kidney function monitoring',
            'Nutritional counseling and meal planning',
            'Continuous glucose monitoring (CGM) for better control'
        ]
    },
    
    'heart_disease': {
        'name': 'Heart Disease',
        'description': 'Conditions affecting the heart and blood vessels, including coronary artery disease and heart attacks.',
        'causes': [
            'Atherosclerosis (plaque buildup in arteries)',
            'High cholesterol levels (especially LDL)',
            'High blood pressure damaging artery walls',
            'Smoking and tobacco use',
            'Obesity and metabolic syndrome',
            'Diabetes and insulin resistance',
            'Chronic inflammation',
            'Genetic factors and family history'
        ],
        'risk_factors': {
            'age': 'Risk increases with age (men >45, women >55)',
            'cholesterol': 'Total cholesterol >200 mg/dL, LDL >100 mg/dL increases risk',
            'blood_pressure': 'Systolic >130 or diastolic >80 mmHg indicates hypertension',
            'max_heart_rate': 'Lower maximum heart rate may indicate poor cardiovascular fitness',
            'chest_pain': 'Chest pain (angina) indicates reduced blood flow to heart',
            'exercise_induced_angina': 'Pain during exercise suggests coronary artery disease'
        },
        'prevention': [
            'Control blood pressure (<120/80 mmHg)',
            'Maintain healthy cholesterol levels (LDL <100 mg/dL)',
            'Regular aerobic exercise (30 minutes, 5 days/week)',
            'Heart-healthy diet (Mediterranean or DASH diet)',
            'Maintain healthy weight and waist circumference',
            'Quit smoking and avoid secondhand smoke',
            'Limit alcohol consumption (1-2 drinks/day maximum)',
            'Manage stress and get adequate sleep',
            'Control diabetes and blood sugar levels'
        ],
        'treatment': [
            'Medications: Statins, ACE inhibitors, beta-blockers, aspirin',
            'Lifestyle changes: Diet, exercise, weight loss',
            'Cardiac rehabilitation programs',
            'Procedures: Angioplasty, stent placement, bypass surgery',
            'Regular cardiology follow-ups and stress tests',
            'Blood pressure and cholesterol monitoring',
            'Antiplatelet therapy to prevent blood clots',
            'Implantable devices (pacemaker, defibrillator) if needed'
        ]
    },
    
    'liver_disease': {
        'name': 'Liver Disease',
        'description': 'Damage to the liver affecting its ability to function properly, including fatty liver, hepatitis, and cirrhosis.',
        'causes': [
            'Chronic alcohol consumption',
            'Non-alcoholic fatty liver disease (NAFLD)',
            'Viral hepatitis (Hepatitis B, C)',
            'Autoimmune conditions',
            'Genetic disorders (hemochromatosis, Wilson\'s disease)',
            'Obesity and metabolic syndrome',
            'Certain medications and toxins',
            'Bile duct diseases'
        ],
        'risk_factors': {
            'albumin': 'Low albumin (<3.5 g/dL) indicates impaired liver function',
            'bilirubin': 'Elevated bilirubin (>1.2 mg/dL) suggests liver dysfunction or bile duct problems',
            'alkaline_phosphatase': 'High levels indicate bile duct obstruction or liver damage',
            'alt': 'Elevated ALT indicates liver cell damage',
            'ast': 'High AST levels suggest liver injury',
            'age': 'Risk of liver disease increases with age'
        },
        'prevention': [
            'Limit or avoid alcohol consumption',
            'Maintain healthy weight to prevent fatty liver',
            'Get vaccinated against Hepatitis A and B',
            'Practice safe behaviors to avoid Hepatitis C',
            'Use medications as prescribed; avoid overuse',
            'Eat a balanced diet low in saturated fats',
            'Regular exercise to prevent obesity',
            'Avoid exposure to toxic chemicals'
        ],
        'treatment': [
            'Abstinence from alcohol if alcohol-related',
            'Antiviral medications for viral hepatitis',
            'Weight loss and exercise for fatty liver disease',
            'Medications: Ursodiol for bile duct disease, immunosuppressants for autoimmune',
            'Management of complications (ascites, varices, encephalopathy)',
            'Regular monitoring with liver function tests and imaging',
            'Nutritional support and vitamin supplementation',
            'Liver transplant for advanced cirrhosis or liver failure'
        ]
    },
    
    'kidney_disease': {
        'name': 'Chronic Kidney Disease',
        'description': 'Gradual loss of kidney function over time, affecting the body\'s ability to filter waste and excess fluids.',
        'causes': [
            'Diabetes (diabetic nephropathy)',
            'High blood pressure (hypertensive nephropathy)',
            'Glomerulonephritis (kidney inflammation)',
            'Polycystic kidney disease',
            'Prolonged urinary tract obstruction',
            'Recurrent kidney infections',
            'Autoimmune diseases (lupus)',
            'Prolonged use of certain medications (NSAIDs)'
        ],
        'risk_factors': {
            'blood_pressure': 'Hypertension damages kidney blood vessels',
            'blood_glucose': 'High blood sugar damages kidney filtration units',
            'serum_creatinine': 'Elevated creatinine (>1.2 mg/dL) indicates reduced kidney function',
            'blood_urea': 'High BUN levels suggest impaired kidney function',
            'hemoglobin': 'Low hemoglobin may indicate kidney disease anemia',
            'albumin': 'Low albumin suggests protein loss through kidneys',
            'age': 'Kidney function naturally declines with age'
        },
        'prevention': [
            'Control blood pressure (<130/80 mmHg)',
            'Manage diabetes with target HbA1c <7%',
            'Maintain healthy weight and exercise regularly',
            'Stay hydrated but avoid excessive fluid intake',
            'Limit salt intake (<2,300 mg sodium/day)',
            'Avoid NSAIDs and nephrotoxic medications',
            'Regular kidney function screening if at risk',
            'Treat urinary tract infections promptly'
        ],
        'treatment': [
            'Blood pressure control with ACE inhibitors or ARBs',
            'Diabetes management to slow progression',
            'Dietary modifications (low protein, low salt, low potassium)',
            'Management of complications (anemia, bone disease, electrolyte imbalances)',
            'Medications: Phosphate binders, erythropoietin, vitamin D',
            'Regular monitoring of kidney function (eGFR, creatinine)',
            'Dialysis (hemodialysis or peritoneal) for advanced disease',
            'Kidney transplantation for end-stage renal disease'
        ]
    },
    
    'breast_cancer': {
        'name': 'Breast Cancer',
        'description': 'Malignant tumor developing in breast tissue, most commonly in ducts or lobules.',
        'causes': [
            'Genetic mutations (BRCA1, BRCA2 genes)',
            'Hormonal factors (estrogen exposure)',
            'Family history of breast or ovarian cancer',
            'Age (risk increases after 50)',
            'Previous breast conditions (atypical hyperplasia)',
            'Radiation exposure to chest',
            'Obesity and lack of physical activity',
            'Alcohol consumption and smoking'
        ],
        'risk_factors': {
            'age': 'Risk increases significantly after age 50-55',
            'radius_mean': 'Larger tumor radius indicates more advanced cancer',
            'texture_mean': 'Tumor texture irregularity may indicate malignancy',
            'perimeter': 'Larger perimeter suggests larger tumor size',
            'area': 'Tumor area correlates with cancer stage',
            'concave_points': 'More concave points suggest irregular, malignant morphology'
        },
        'prevention': [
            'Regular breast self-examinations monthly',
            'Mammography screening (annually after 40-50)',
            'Maintain healthy weight through diet and exercise',
            'Limit alcohol consumption (max 1 drink/day)',
            'Breastfeed if possible (reduces risk)',
            'Avoid hormone replacement therapy when possible',
            'Genetic counseling and testing if family history exists',
            'Consider preventive surgery if high genetic risk'
        ],
        'treatment': [
            'Surgery: Lumpectomy (breast-conserving) or mastectomy',
            'Radiation therapy to destroy remaining cancer cells',
            'Chemotherapy (before or after surgery)',
            'Hormone therapy for hormone receptor-positive cancers',
            'Targeted therapy (Herceptin for HER2-positive)',
            'Immunotherapy for certain types',
            'Regular follow-up with oncologist',
            'Reconstruction surgery options',
            'Support groups and psychological counseling'
        ]
    },
    
    'parkinsons': {
        'name': "Parkinson's Disease",
        'description': 'Progressive neurological disorder affecting movement, caused by loss of dopamine-producing brain cells.',
        'causes': [
            'Loss of dopamine-producing neurons in substantia nigra',
            'Genetic mutations (LRRK2, PARK7, PINK1, PRKN genes)',
            'Environmental toxins exposure (pesticides, heavy metals)',
            'Age-related neuronal degeneration',
            'Oxidative stress and mitochondrial dysfunction',
            'Accumulation of alpha-synuclein protein (Lewy bodies)',
            'Head trauma history',
            'Combination of genetic and environmental factors'
        ],
        'risk_factors': {
            'age': 'Risk increases with age, typically onset after 60',
            'mdvp_fo': 'Vocal fundamental frequency changes indicate motor control issues',
            'mdvp_jitter': 'Increased voice jitter suggests vocal cord instability',
            'mdvp_shimmer': 'Voice shimmer indicates amplitude variation problems',
            'nhr': 'Noise-to-harmonics ratio reflects voice quality deterioration',
            'hnr': 'Low harmonics-to-noise ratio indicates voice impairment'
        },
        'prevention': [
            'Regular physical exercise (improves brain health)',
            'Mediterranean diet rich in antioxidants',
            'Avoid exposure to pesticides and industrial chemicals',
            'Maintain social engagement and mental stimulation',
            'Adequate sleep and stress management',
            'Caffeine consumption may have protective effect',
            'Avoid head injuries (wear protective gear)',
            'Regular medical check-ups for early detection'
        ],
        'treatment': [
            'Levodopa/Carbidopa (gold standard medication)',
            'Dopamine agonists (pramipexole, ropinirole)',
            'MAO-B inhibitors (selegiline, rasagiline)',
            'COMT inhibitors to prolong levodopa effect',
            'Physical therapy to maintain mobility',
            'Occupational therapy for daily activities',
            'Speech therapy for communication difficulties',
            'Deep brain stimulation (DBS) for advanced cases',
            'Regular exercise and movement therapy',
            'Support groups and counseling'
        ]
    },
    
    'stroke': {
        'name': 'Stroke',
        'description': 'Sudden interruption of blood supply to the brain, causing brain cell death.',
        'causes': [
            'Ischemic stroke: Blood clot blocking brain artery',
            'Hemorrhagic stroke: Ruptured blood vessel in brain',
            'Atherosclerosis (narrowed arteries)',
            'Atrial fibrillation (irregular heartbeat)',
            'High blood pressure damaging blood vessels',
            'Diabetes weakening blood vessel walls',
            'High cholesterol and lipid buildup',
            'Blood clotting disorders'
        ],
        'risk_factors': {
            'age': 'Risk doubles each decade after age 55',
            'hypertension': 'High blood pressure is the single most important risk factor',
            'heart_disease': 'Heart conditions increase stroke risk 2-4 fold',
            'glucose': 'Diabetes increases stroke risk by 2-4 times',
            'bmi': 'Obesity (BMI >30) significantly increases risk',
            'smoking': 'Smoking doubles stroke risk'
        },
        'prevention': [
            'Control blood pressure (<120/80 mmHg)',
            'Manage diabetes and keep blood sugar controlled',
            'Maintain healthy cholesterol levels',
            'Exercise regularly (150 minutes/week)',
            'Eat heart-healthy diet (low sodium, high fruits/vegetables)',
            'Quit smoking and avoid secondhand smoke',
            'Limit alcohol consumption',
            'Treat atrial fibrillation with anticoagulants',
            'Maintain healthy weight',
            'Manage stress and get adequate sleep'
        ],
        'treatment': [
            'Emergency treatment: tPA (clot-buster) within 3-4.5 hours',
            'Mechanical thrombectomy for large vessel occlusion',
            'Blood pressure management in acute phase',
            'Antiplatelet therapy (aspirin, clopidogrel)',
            'Anticoagulation for atrial fibrillation',
            'Statin therapy for cholesterol management',
            'Rehabilitation: Physical, occupational, speech therapy',
            'Carotid endarterectomy if significant stenosis',
            'Lifestyle modifications to prevent recurrence',
            'Regular neurologist follow-up'
        ]
    },
    
    'hypertension': {
        'name': 'Hypertension (High Blood Pressure)',
        'description': 'Persistently elevated blood pressure in the arteries (≥130/80 mmHg).',
        'causes': [
            'Essential hypertension (no identifiable cause, 90-95% cases)',
            'Kidney disease or dysfunction',
            'Hormonal disorders (thyroid, adrenal problems)',
            'Obesity and excess body weight',
            'High sodium intake in diet',
            'Excessive alcohol consumption',
            'Chronic stress and anxiety',
            'Genetic predisposition and family history',
            'Sedentary lifestyle',
            'Sleep apnea'
        ],
        'risk_factors': {
            'age': 'Risk increases with age, especially after 45',
            'systolic_bp': 'Systolic BP ≥130 mmHg indicates hypertension',
            'diastolic_bp': 'Diastolic BP ≥80 mmHg indicates hypertension',
            'bmi': 'Obesity significantly increases hypertension risk',
            'sodium_intake': 'High salt diet (>2,300 mg/day) raises BP',
            'family_history': 'Genetic predisposition increases risk 2-fold'
        },
        'prevention': [
            'Reduce sodium intake (<2,300 mg/day, ideally <1,500 mg)',
            'DASH diet (Dietary Approaches to Stop Hypertension)',
            'Regular aerobic exercise (30 min/day, 5 days/week)',
            'Maintain healthy weight (BMI 18.5-24.9)',
            'Limit alcohol (men: 2 drinks/day, women: 1 drink/day)',
            'Quit smoking',
            'Manage stress through relaxation techniques',
            'Adequate sleep (7-9 hours per night)',
            'Regular blood pressure monitoring'
        ],
        'treatment': [
            'Lifestyle modifications as first-line approach',
            'ACE inhibitors (lisinopril, enalapril)',
            'ARBs (losartan, valsartan)',
            'Calcium channel blockers (amlodipine)',
            'Diuretics (hydrochlorothiazide)',
            'Beta-blockers if indicated',
            'Combination therapy for difficult-to-control BP',
            'Regular home blood pressure monitoring',
            'Periodic lab tests (kidney function, electrolytes)',
            'Annual eye and kidney screening'
        ]
    },
    
    'anemia': {
        'name': 'Anemia',
        'description': 'Condition characterized by insufficient red blood cells or hemoglobin to carry adequate oxygen.',
        'causes': [
            'Iron deficiency (most common cause)',
            'Vitamin B12 or folate deficiency',
            'Chronic diseases (kidney disease, cancer, inflammation)',
            'Blood loss (menstruation, GI bleeding)',
            'Bone marrow disorders',
            'Hemolysis (red blood cell destruction)',
            'Inherited conditions (sickle cell, thalassemia)',
            'Medications affecting blood cell production'
        ],
        'risk_factors': {
            'hemoglobin': 'Low hemoglobin (<13 g/dL men, <12 g/dL women) defines anemia',
            'mcv': 'Mean corpuscular volume indicates type of anemia',
            'mch': 'Mean corpuscular hemoglobin helps classify anemia',
            'iron': 'Low iron levels indicate iron deficiency anemia',
            'ferritin': 'Low ferritin (<30 ng/mL) suggests depleted iron stores',
            'age': 'Infants, adolescents, and elderly at higher risk'
        },
        'prevention': [
            'Iron-rich diet (red meat, beans, leafy greens, fortified cereals)',
            'Vitamin C to enhance iron absorption',
            'Adequate B12 intake (animal products, fortified foods)',
            'Folate-rich foods (leafy vegetables, citrus, legumes)',
            'Address heavy menstrual bleeding if applicable',
            'Regular health screenings, especially during pregnancy',
            'Treat underlying conditions causing anemia',
            'Avoid excessive tea/coffee with meals (inhibits iron absorption)'
        ],
        'treatment': [
            'Iron supplementation (ferrous sulfate, ferrous gluconate)',
            'Vitamin B12 injections or supplements',
            'Folic acid supplementation',
            'Treat underlying cause (bleeding, kidney disease, etc.)',
            'Erythropoietin injections for chronic kidney disease',
            'Blood transfusion for severe anemia',
            'Bone marrow transplant for severe marrow disorders',
            'Dietary counseling and nutritional support',
            'Regular monitoring of hemoglobin and ferritin levels',
            'Endoscopy/colonoscopy if GI bleeding suspected'
        ]
    },
    
    'thyroid': {
        'name': 'Thyroid Disorder',
        'description': 'Dysfunction of the thyroid gland causing abnormal hormone production (hypothyroidism or hyperthyroidism).',
        'causes': [
            'Autoimmune conditions (Hashimoto\'s, Graves\' disease)',
            'Iodine deficiency or excess',
            'Thyroid nodules or goiter',
            'Thyroiditis (inflammation)',
            'Medications affecting thyroid function',
            'Pregnancy-related changes',
            'Pituitary gland disorders',
            'Thyroid cancer',
            'Radiation therapy to neck area',
            'Genetic predisposition'
        ],
        'risk_factors': {
            'tsh': 'Abnormal TSH (high in hypothyroidism, low in hyperthyroidism)',
            't3': 'Elevated T3 in hyperthyroidism, low in hypothyroidism',
            't4': 'High T4 in hyperthyroidism, low in hypothyroidism',
            'age': 'Risk increases with age, especially in women over 60',
            'gender': 'Women 5-8 times more likely to develop thyroid disorders',
            'family_history': 'Genetic predisposition increases risk'
        },
        'prevention': [
            'Adequate iodine intake (150 mcg/day for adults)',
            'Regular thyroid function screening if at risk',
            'Manage stress levels',
            'Avoid exposure to radiation when possible',
            'Maintain healthy weight',
            'Treat autoimmune conditions if present',
            'Discuss thyroid monitoring if pregnant or planning pregnancy',
            'Be aware of symptoms and seek early medical attention'
        ],
        'treatment': [
            'Hypothyroidism: Levothyroxine (synthetic T4) replacement',
            'Hyperthyroidism: Anti-thyroid drugs (methimazole, PTU)',
            'Radioactive iodine therapy for hyperthyroidism',
            'Beta-blockers to manage hyperthyroid symptoms',
            'Thyroid surgery if indicated (nodules, cancer, large goiter)',
            'Regular monitoring of TSH, T3, T4 levels',
            'Dose adjustments based on symptoms and lab results',
            'Dietary modifications (ensure adequate iodine, selenium)',
            'Treatment of underlying autoimmune conditions',
            'Lifelong monitoring and medication for most patients'
        ]
    }
}


def get_disease_explanation(disease_name, prediction_proba, feature_importance_df, instance, feature_names):
    """
    Generate comprehensive medical explanation with causes and treatment
    
    Args:
        disease_name: Name of the disease
        prediction_proba: Prediction probability
        feature_importance_df: DataFrame with feature importance
        instance: Input instance values
        feature_names: List of feature names
    
    Returns:
        Detailed medical explanation
    """
    disease_key = disease_name.lower()
    
    if disease_key not in DISEASE_KNOWLEDGE:
        return None
    
    knowledge = DISEASE_KNOWLEDGE[disease_key]
    risk_level = "High" if prediction_proba >= 0.7 else ("Medium" if prediction_proba >= 0.3 else "Low")
    
    # Build explanation
    explanation = f"# {knowledge['name']} Risk Assessment\n\n"
    explanation += f"**Risk Level: {risk_level}** (Probability: {prediction_proba:.1%})\n\n"
    explanation += f"**About {knowledge['name']}:**\n{knowledge['description']}\n\n"
    
    # Your specific risk factors
    explanation += f"## 📊 Your Key Risk Indicators:\n\n"
    
    for idx, row in feature_importance_df.head(5).iterrows():
        feature = row['feature']
        importance = row['importance']
        
        try:
            feature_idx = feature_names.index(feature)
            feature_value = instance[feature_idx]
            
            direction = "⬆️ Increases" if importance > 0 else "⬇️ Decreases"
            explanation += f"**{idx+1}. {feature.replace('_', ' ').title()}** = {feature_value:.2f}\n"
            explanation += f"   - {direction} risk (importance: {abs(importance):.3f})\n"
            
            # Add specific interpretation if available
            if feature in knowledge['risk_factors']:
                explanation += f"   - *{knowledge['risk_factors'][feature]}*\n"
            explanation += "\n"
        except:
            pass
    
    # Why it occurs
    explanation += f"## 🔬 Why {knowledge['name']} Occurs:\n\n"
    explanation += "Common causes and contributing factors:\n\n"
    for cause in knowledge['causes'][:6]:
        explanation += f"- {cause}\n"
    explanation += "\n"
    
    # PERSONALIZED Prevention Strategies based on top risk factors
    explanation += f"## 🛡️ Personalized Prevention Strategies:\n\n"
    explanation += "**Based on YOUR specific risk factors:**\n\n"
    
    # Analyze top risk factors and provide targeted advice
    personalized_prevention = []
    
    for idx, row in feature_importance_df.head(5).iterrows():
        feature = row['feature'].lower()
        importance = row['importance']
        
        try:
            feature_idx = feature_names.index(row['feature'])
            feature_value = instance[feature_idx]
            
            # Personalized recommendations based on actual values
            if 'glucose' in feature and abs(importance) > 0.2:
                if feature_value > 0.5:  # Scaled value indicating high glucose
                    personalized_prevention.append("🎯 **Priority: Control blood sugar** - Your glucose level is elevated. Focus on reducing refined carbohydrates and sugar intake.")
                elif feature_value < -0.5:
                    personalized_prevention.append("✅ **Good: Glucose level is healthy** - Maintain your current dietary habits to keep glucose stable.")
            
            elif 'bmi' in feature and abs(importance) > 0.2:
                if feature_value > 0.5:
                    personalized_prevention.append("🎯 **Priority: Weight management** - Your BMI is elevated. Aim for gradual weight loss (1-2 lbs/week) through diet and exercise.")
                elif feature_value < -0.5:
                    personalized_prevention.append("✅ **Good: Healthy weight** - Continue maintaining your current weight through balanced diet and regular activity.")
            
            elif 'pressure' in feature and abs(importance) > 0.2:
                if feature_value > 0.5:
                    personalized_prevention.append("🎯 **Priority: Blood pressure control** - Your blood pressure is high. Reduce sodium intake (<2300mg/day) and manage stress.")
                elif feature_value < -0.5:
                    personalized_prevention.append("✅ **Good: Blood pressure in range** - Keep up with low-sodium diet and stress management practices.")
            
            elif 'age' in feature and abs(importance) > 0.2:
                if feature_value > 0.5:
                    personalized_prevention.append("⚠️ **Age factor** - As age increases risk, focus on regular health screenings and preventive care every 6-12 months.")
                else:
                    personalized_prevention.append("✅ **Good: Younger age** - Now is the ideal time to establish healthy habits that prevent disease later in life.")
            
            elif 'insulin' in feature and abs(importance) > 0.2:
                if feature_value > 0.5:
                    personalized_prevention.append("🎯 **Priority: Insulin sensitivity** - Your insulin levels suggest resistance. Increase physical activity to 30+ min daily.")
                elif feature_value < -0.5:
                    personalized_prevention.append("✅ **Good: Insulin levels normal** - Continue regular exercise to maintain insulin sensitivity.")
            
            elif 'pregnanc' in feature and abs(importance) > 0.2:
                if feature_value > 0.5:
                    personalized_prevention.append("⚠️ **Pregnancy history** - Multiple pregnancies increase risk. Monitor blood sugar regularly, especially if you had gestational diabetes.")
        except:
            pass
    
    # Add personalized recommendations
    if personalized_prevention:
        for rec in personalized_prevention[:5]:
            explanation += f"- {rec}\n"
        explanation += "\n"
    
    # Add general best practices
    explanation += "**General recommendations for everyone:**\n\n"
    for prevention in knowledge['prevention'][:4]:
        explanation += f"- {prevention}\n"
    explanation += "\n"
    
    # PERSONALIZED Treatment Options
    explanation += f"## 💊 Treatment Recommendations:\n\n"
    if risk_level == "High":
        explanation += "**⚠️ HIGH RISK - Immediate action recommended:**\n\n"
        explanation += "1. **Schedule medical consultation within 1-2 weeks** for proper diagnosis\n"
        explanation += "2. **Start lifestyle modifications immediately** (even before diagnosis)\n"
        explanation += "3. **Begin monitoring** relevant health metrics daily\n\n"
        explanation += "If diagnosed, your treatment plan will likely include:\n\n"
    elif risk_level == "Medium":
        explanation += "**⚠️ MODERATE RISK - Preventive action needed:**\n\n"
        explanation += "1. **Schedule check-up within 1-3 months** for screening\n"
        explanation += "2. **Implement prevention strategies** to reduce risk progression\n"
        explanation += "3. **Monitor symptoms** and track health metrics monthly\n\n"
        explanation += "If diagnosed later, treatment options include:\n\n"
    else:
        explanation += "**✅ LOW RISK - Maintain healthy habits:**\n\n"
        explanation += "1. **Continue healthy lifestyle** to keep risk low\n"
        explanation += "2. **Annual health screenings** for early detection\n"
        explanation += "3. **Stay informed** about risk factors and prevention\n\n"
        explanation += "If diagnosed in the future, treatment options include:\n\n"
    
    for treatment in knowledge['treatment'][:6]:
        explanation += f"- {treatment}\n"
    explanation += "\n"
    
    # Disclaimer
    explanation += "---\n\n"
    explanation += "**⚠️ Important Disclaimer:**\n"
    explanation += "This is a risk prediction based on machine learning analysis and should NOT replace professional medical advice. "
    explanation += "Always consult with qualified healthcare providers for proper diagnosis and treatment. "
    explanation += "Early detection and lifestyle modifications can significantly reduce disease risk.\n"
    
    return explanation
