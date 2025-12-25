import pandas as pd
import numpy as np
from pathlib import Path

# Paths
DATA_RAW = Path('data/raw')
DATA_PROCESSED = Path('data/processed')

print("="*60)
print("FEATURE ENGINEERING - QUICK RUN")
print("="*60)

# Load data
print("\n1. Loading data...")
df = pd.read_csv(DATA_RAW / 'sample_foods.csv')
print(f"   ✓ Loaded {len(df)} foods with {len(df.columns)} columns")

# Create features
print("\n2. Creating derived features...")
df['glycemic_load'] = (df['glycemic_index'] * df['total_carbs_g']) / 100
df['carb_quality_ratio'] = df['fiber_g'] / df['total_carbs_g'].replace(0, np.nan)
df['carb_quality_ratio'].fillna(0, inplace=True)
df['fat_to_carb_ratio'] = df['fat_g'] / df['total_carbs_g'].replace(0, np.nan)
df['fat_to_carb_ratio'].fillna(0, inplace=True)
df['net_carbs_g'] = df['total_carbs_g'] - df['fiber_g']
df['sugar_pct_carbs'] = (df['sugar_g'] / df['total_carbs_g'].replace(0, np.nan)) * 100
df['sugar_pct_carbs'].fillna(0, inplace=True)
df['protein_to_carb_ratio'] = df['protein_g'] / df['total_carbs_g'].replace(0, np.nan)
df['protein_to_carb_ratio'].fillna(0, inplace=True)
df['high_sugar'] = (df['sugar_g'] > 15).astype(int)
df['low_fiber'] = (df['fiber_g'] < 3).astype(int)
df['high_carb'] = (df['total_carbs_g'] > 45).astype(int)
print(f"   ✓ Created 9 derived features")

# Create risk labels
print("\n3. Creating risk labels...")
df['high_risk'] = (
    ((df['glycemic_index'] > 70) & (df['total_carbs_g'] > 45) & (df['fiber_g'] < 3)) |
    ((df['glycemic_load'] > 20) & (df['carb_quality_ratio'] < 0.1)) |
    ((df['glycemic_index'] > 70) & (df['high_sugar'] == 1))
).astype(int)

print(f"   ✓ High risk: {df['high_risk'].sum()} meals ({df['high_risk'].mean()*100:.1f}%)")
print(f"   ✓ Low risk: {(~df['high_risk'].astype(bool)).sum()} meals ({(1-df['high_risk'].mean())*100:.1f}%)")

# Save
print("\n4. Saving...")
output_file = DATA_PROCESSED / 'meals_with_features.csv'
df.to_csv(output_file, index=False)
print(f"   ✓ Saved to {output_file}")
print(f"   ✓ Total features: {len(df.columns)}")

print("\n" + "="*60)
print("✅ FEATURE ENGINEERING COMPLETE!")
print("="*60)
print(f"\nDataset ready: {len(df)} meals × {len(df.columns)} features")
print("\nNext: python quick_train.py")
