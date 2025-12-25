"""
Model Training Notebook - Simplified Python Script Version
Train Logistic Regression, Random Forest, and XGBoost models
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pickle

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import xgboost as xgb

# Setup
PROJECT_ROOT = Path('.')
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
APP_DIR = PROJECT_ROOT / 'app'

print("=" * 80)
print("MODEL TRAINING PIPELINE")
print("=" * 80)

# Load feature-engineered data
print("\n1. Loading feature-engineered data...")
try:
    df = pd.read_csv(DATA_PROCESSED / 'meals_with_features.csv')
    print(f"   ✓ Loaded {len(df)} meals with {len(df.columns)} features")
except FileNotFoundError:
    print("   ⚠️  Feature-engineered data not found. Running feature engineering first...")
    import sys
    sys.path.append('scripts')
    exec(open('scripts/process_features.py').read())
    df = pd.read_csv(DATA_PROCESSED / 'meals_with_features.csv')

# Prepare features and target
print("\n2. Preparing features and target...")
feature_cols = ['total_carbs_g', 'fiber_g', 'sugar_g', 'protein_g', 'fat_g',
                'saturated_fat_g', 'energy_kcal', 'glycemic_index', 'glycemic_load',
                'carb_quality_ratio', 'fat_to_carb_ratio', 'net_carbs_g',
                'sugar_pct_carbs', 'protein_to_carb_ratio', 'high_sugar',
                'low_fiber', 'high_carb']

X = df[feature_cols]
y = df['high_risk']

print(f"   ✓ Features: {len(feature_cols)}")
print(f"   ✓ Samples: {len(X)}")
print(f"   ✓ Class balance: {y.value_counts().to_dict()}")

# Train-test split
print("\n3. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"   ✓ Training set: {len(X_train)} samples")
print(f"   ✓ Test set: {len(X_test)} samples")

# Scale features
print("\n4. Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("   ✓ Features standardized")

# Model 1: Logistic Regression
print("\n5. Training Logistic Regression (Baseline)...")
lr_model = LogisticRegression(
    random_state=42,
    class_weight='balanced',
    max_iter=1000
)
lr_model.fit(X_train_scaled, y_train)

lr_train_score = lr_model.score(X_train_scaled, y_train)
lr_test_score = lr_model.score(X_test_scaled, y_test)
lr_pred = lr_model.predict(X_test_scaled)
lr_auc = roc_auc_score(y_test, lr_model.predict_proba(X_test_scaled)[:, 1])

print(f"   ✓ Training Accuracy: {lr_train_score:.3f}")
print(f"   ✓ Test Accuracy: {lr_test_score:.3f}")
print(f"   ✓ ROC-AUC: {lr_auc:.3f}")

# Model 2: Random Forest
print("\n6. Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

rf_train_score = rf_model.score(X_train, y_train)
rf_test_score = rf_model.score(X_test, y_test)
rf_pred = rf_model.predict(X_test)
rf_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test)[:, 1])

print(f"   ✓ Training Accuracy: {rf_train_score:.3f}")
print(f"   ✓ Test Accuracy: {rf_test_score:.3f}")
print(f"   ✓ ROC-AUC: {rf_auc:.3f}")

# Model 3: XGBoost
print("\n7. Training XGBoost...")
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    scale_pos_weight=scale_pos_weight,
    eval_metric='logloss'
)
xgb_model.fit(X_train, y_train)

xgb_train_score = xgb_model.score(X_train, y_train)
xgb_test_score = xgb_model.score(X_test, y_test)
xgb_pred = xgb_model.predict(X_test)
xgb_auc = roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1])

print(f"   ✓ Training Accuracy: {xgb_train_score:.3f}")
print(f"   ✓ Test Accuracy: {xgb_test_score:.3f}")
print(f"   ✓ ROC-AUC: {xgb_auc:.3f}")

# Model comparison
print("\n" + "=" * 80)
print("MODEL COMPARISON")
print("=" * 80)
print(f"\n{'Model':<20} {'Train Acc':<12} {'Test Acc':<12} {'ROC-AUC':<12}")
print("-" * 56)
print(f"{'Logistic Regression':<20} {lr_train_score:<12.3f} {lr_test_score:<12.3f} {lr_auc:<12.3f}")
print(f"{'Random Forest':<20} {rf_train_score:<12.3f} {rf_test_score:<12.3f} {rf_auc:<12.3f}")
print(f"{'XGBoost':<20} {xgb_train_score:<12.3f} {xgb_test_score:<12.3f} {xgb_auc:<12.3f}")

# Select best model (by AUC)
models = {
    'Logistic Regression': (lr_model, lr_auc, X_test_scaled),
    'Random Forest': (rf_model, rf_auc, X_test),
    'XGBoost': (xgb_model, xgb_auc, X_test)
}

best_model_name = max(models, key=lambda k: models[k][1])
best_model, best_auc, best_X_test = models[best_model_name]

print(f"\n🏆 Best Model: {best_model_name} (AUC: {best_auc:.3f})")

# Detailed evaluation of best model
print(f"\n" + "=" * 80)
print(f"BEST MODEL EVALUATION: {best_model_name}")
print("=" * 80)

best_pred = best_model.predict(best_X_test)
print("\nClassification Report:")
print(classification_report(y_test, best_pred, target_names=['Low Risk', 'High Risk']))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, best_pred)
print(f"                Predicted")
print(f"                Low  High")
print(f"Actual  Low    {cm[0,0]:4d}  {cm[0,1]:4d}")
print(f"        High   {cm[1,0]:4d}  {cm[1,1]:4d}")

# Save models
print("\n8. Saving models...")
APP_DIR.mkdir(exist_ok=True)

# Save best model and preprocessor
with open(APP_DIR / 'model.pkl', 'wb') as f:
    if best_model_name == 'Logistic Regression':
        pickle.dump({'model': best_model, 'scaler': scaler, 'model_type': 'lr'}, f)
    else:
        pickle.dump({'model': best_model, 'scaler': None, 'model_type': best_model_name.lower().replace(' ', '_')}, f)

with open(APP_DIR / 'feature_names.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)

print(f"   ✓ Saved {best_model_name} to app/model.pkl")
print("   ✓ Saved feature names to app/feature_names.pkl")

# Save all models for comparison
models_dir = PROJECT_ROOT / 'models'
models_dir.mkdir(exist_ok=True)

with open(models_dir / 'logistic_regression.pkl', 'wb') as f:
    pickle.dump({'model': lr_model, 'scaler': scaler}, f)
with open(models_dir / 'random_forest.pkl', 'wb') as f:
    pickle.dump({'model': rf_model, 'scaler': None}, f)
with open(models_dir / 'xgboost.pkl', 'wb') as f:
    pickle.dump({'model': xgb_model, 'scaler': None}, f)

print("   ✓ Saved all models to models/ directory")

print("\n" + "=" * 80)
print("✅ MODEL TRAINING COMPLETE")
print("=" * 80)
print(f"\n🎯 Best Model: {best_model_name}")
print(f"📊 Test Accuracy: {best_model.score(best_X_test, y_test):.3f}")
print(f"📈 ROC-AUC: {best_auc:.3f}")
print("\n📝 Next steps:")
print("   1. Restart Streamlit app to use trained model")
print("   2. Test predictions in the web interface")
print("   3. Create visualizations for final report")
