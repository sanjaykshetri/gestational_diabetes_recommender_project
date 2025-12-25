import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("Note: XGBoost not installed. Install with: pip install xgboost")

print("="*60)
print("MODEL TRAINING - QUICK RUN")
print("="*60)

# Load data
print("\n1. Loading feature-engineered data...")
df = pd.read_csv('data/processed/meals_with_features.csv')
print(f"   ✓ Loaded {len(df)} meals with {len(df.columns)} features")

# Prepare data
print("\n2. Preparing features and target...")
feature_cols = ['total_carbs_g', 'fiber_g', 'sugar_g', 'protein_g', 'fat_g',
                'saturated_fat_g', 'energy_kcal', 'glycemic_index', 'glycemic_load',
                'carb_quality_ratio', 'fat_to_carb_ratio', 'net_carbs_g',
                'sugar_pct_carbs', 'protein_to_carb_ratio', 'high_sugar',
                'low_fiber', 'high_carb']

X = df[feature_cols]
y = df['high_risk']
print(f"   ✓ Features: {len(feature_cols)}")
print(f"   ✓ Target balance: {(y==0).sum()} low risk, {(y==1).sum()} high risk")

# Split
print("\n3. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"   ✓ Train: {len(X_train)}, Test: {len(X_test)}")

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {}

print("\n4. Training Logistic Regression...")
lr = LogisticRegression(random_state=42, class_weight='balanced', max_iter=1000)
lr.fit(X_train_scaled, y_train)
lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test_scaled)[:, 1])
models['Logistic Regression'] = (lr, lr_auc, scaler, X_test_scaled)
print(f"   ✓ ROC-AUC: {lr_auc:.3f}")

print("\n5. Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced', n_jobs=-1)
rf.fit(X_train, y_train)
rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
models['Random Forest'] = (rf, rf_auc, None, X_test)
print(f"   ✓ ROC-AUC: {rf_auc:.3f}")

if HAS_XGB:
    print("\n6. Training XGBoost...")
    xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=6, random_state=42, eval_metric='logloss')
    xgb_model.fit(X_train, y_train)
    xgb_auc = roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1])
    models['XGBoost'] = (xgb_model, xgb_auc, None, X_test)
    print(f"   ✓ ROC-AUC: {xgb_auc:.3f}")

# Select best
print("\n7. Comparing models...")
best_name = max(models, key=lambda k: models[k][1])
best_model, best_auc, best_scaler, best_X_test = models[best_name]
print(f"   🏆 Best: {best_name} (AUC: {best_auc:.3f})")

# Save
print("\n8. Saving model...")
Path('app').mkdir(exist_ok=True)
with open('app/model.pkl', 'wb') as f:
    pickle.dump({'model': best_model, 'scaler': best_scaler, 'features': feature_cols}, f)
print(f"   ✓ Saved to app/model.pkl")

# Report
print("\n" + "="*60)
print("MODEL EVALUATION")
print("="*60)
y_pred = best_model.predict(best_X_test)
print("\n" + classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))

print("="*60)
print("✅ TRAINING COMPLETE!")
print("="*60)
print(f"\nBest Model: {best_name}")
print(f"ROC-AUC: {best_auc:.3f}")
print(f"\nModel saved to: app/model.pkl")
print("\nNext: Restart Streamlit app to use trained model")
