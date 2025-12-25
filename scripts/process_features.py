"""
Feature Engineering Script
Processes sample data and creates feature-engineered dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path('.')
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'

print("=" * 80)
print("FEATURE ENGINEERING PIPELINE")
print("=" * 80)

# Load data
print("\n1. Loading sample data...")
df = pd.read_csv(DATA_RAW / 'sample_foods.csv')
print(f"   ✓ Loaded {len(df)} food items")
print(f"   ✓ Base features: {len(df.columns)}")

# Calculate derived features
print("\n2. Creating derived features...")

# Glycemic load
df['glycemic_load'] = (df['glycemic_index'] * df['total_carbs_g']) / 100

# Carb quality ratio
df['carb_quality_ratio'] = df['fiber_g'] / df['total_carbs_g'].replace(0, np.nan)
df['carb_quality_ratio'].fillna(0, inplace=True)

# Fat to carb ratio
df['fat_to_carb_ratio'] = df['fat_g'] / df['total_carbs_g'].replace(0, np.nan)
df['fat_to_carb_ratio'].fillna(0, inplace=True)

# Net carbs
df['net_carbs_g'] = df['total_carbs_g'] - df['fiber_g']

# Sugar percentage
df['sugar_pct_carbs'] = (df['sugar_g'] / df['total_carbs_g'].replace(0, np.nan)) * 100
df['sugar_pct_carbs'].fillna(0, inplace=True)

# Protein to carb ratio
df['protein_to_carb_ratio'] = df['protein_g'] / df['total_carbs_g'].replace(0, np.nan)
df['protein_to_carb_ratio'].fillna(0, inplace=True)

# Binary flags
df['high_sugar'] = (df['sugar_g'] > 15).astype(int)
df['low_fiber'] = (df['fiber_g'] < 3).astype(int)
df['high_carb'] = (df['total_carbs_g'] > 45).astype(int)

print("   ✓ Created 9 derived features")

# Create risk labels
print("\n3. Creating synthetic risk labels...")

def create_risk_label(row):
    """Create binary risk label based on nutritional criteria"""
    condition1 = (row['glycemic_index'] > 70) & (row['total_carbs_g'] > 45) & (row['fiber_g'] < 3)
    condition2 = (row['glycemic_load'] > 20) & (row['carb_quality_ratio'] < 0.1)
    condition3 = (row['glycemic_index'] > 70) & (row['high_sugar'] == 1)
    return 1 if (condition1 or condition2 or condition3) else 0

df['high_risk'] = df.apply(create_risk_label, axis=1)

high_risk_count = df['high_risk'].sum()
high_risk_pct = df['high_risk'].mean() * 100

print(f"   ✓ High risk meals: {high_risk_count} ({high_risk_pct:.1f}%)")
print(f"   ✓ Low risk meals: {len(df) - high_risk_count} ({100-high_risk_pct:.1f}%)")

# Save processed data
print("\n4. Saving feature-engineered dataset...")
output_file = DATA_PROCESSED / 'meals_with_features.csv'
df.to_csv(output_file, index=False)

print(f"   ✓ Saved to: {output_file}")
print(f"   ✓ Total features: {len(df.columns)}")

# Summary statistics
print("\n" + "=" * 80)
print("DATASET SUMMARY")
print("=" * 80)
print(f"\nShape: {df.shape[0]} meals × {df.shape[1]} features")
print(f"\nFeature List:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print(f"\nTarget Distribution:")
print(f"  Low Risk (0):  {(df['high_risk']==0).sum():3d} meals ({(df['high_risk']==0).mean()*100:5.1f}%)")
print(f"  High Risk (1): {(df['high_risk']==1).sum():3d} meals ({(df['high_risk']==1).mean()*100:5.1f}%)")

print("\n" + "=" * 80)
print("✅ FEATURE ENGINEERING COMPLETE")
print("=" * 80)
print("\n📝 Next step: Model training (Notebook 03)")
