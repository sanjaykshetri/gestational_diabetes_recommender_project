import sys
import pandas as pd
import numpy as np
from pathlib import Path

print("Python executable:", sys.executable, flush=True)
print("Python version:", sys.version, flush=True)
print("="*80, flush=True)

try:
    # Paths
    DATA_RAW = Path('data/raw')
    DATA_PROCESSED = Path('data/processed')
    
    print(f"\nChecking paths...", flush=True)
    print(f"  DATA_RAW exists: {DATA_RAW.exists()}", flush=True)
    print(f"  DATA_PROCESSED exists: {DATA_PROCESSED.exists()}", flush=True)
    
    # Load data
    print(f"\nLoading data from: {DATA_RAW / 'sample_foods.csv'}", flush=True)
    df = pd.read_csv(DATA_RAW / 'sample_foods.csv')
    print(f"✓ Loaded {len(df)} foods with {len(df.columns)} columns", flush=True)
    print(f"  Columns: {list(df.columns)}", flush=True)
    
    # Create features
    print(f"\nCreating derived features...", flush=True)
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
    print(f"✓ Created 9 derived features", flush=True)
    
    # Create risk labels
    print(f"\nCreating risk labels...", flush=True)
    df['high_risk'] = (
        ((df['glycemic_index'] > 70) & (df['total_carbs_g'] > 45) & (df['fiber_g'] < 3)) |
        ((df['glycemic_load'] > 20) & (df['carb_quality_ratio'] < 0.1)) |
        ((df['glycemic_index'] > 70) & (df['high_sugar'] == 1))
    ).astype(int)
    
    high_risk_count = df['high_risk'].sum()
    low_risk_count = (~df['high_risk'].astype(bool)).sum()
    print(f"✓ High risk: {high_risk_count} meals ({df['high_risk'].mean()*100:.1f}%)", flush=True)
    print(f"✓ Low risk: {low_risk_count} meals ({(1-df['high_risk'].mean())*100:.1f}%)", flush=True)
    
    # Save
    print(f"\nSaving to CSV...", flush=True)
    output_file = DATA_PROCESSED / 'meals_with_features.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Saved to {output_file}", flush=True)
    print(f"✓ File exists: {output_file.exists()}", flush=True)
    print(f"✓ Total features: {len(df.columns)}", flush=True)
    
    print(f"\n{'='*80}", flush=True)
    print(f"✅ SUCCESS! Feature engineering complete!", flush=True)
    print(f"{'='*80}", flush=True)
    print(f"\nDataset: {len(df)} meals × {len(df.columns)} features", flush=True)
    print(f"\nOutput file: {output_file.absolute()}", flush=True)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}", flush=True)
    print(f"   {str(e)}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
