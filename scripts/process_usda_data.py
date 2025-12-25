"""
Process USDA FoodData Central to create clean nutritional dataset
Author: Sanjay Kumar Chhetri
Date: December 25, 2025

This script:
1. Loads and filters relevant foods from USDA database
2. Extracts key nutritional information
3. Merges with glycemic index data
4. Creates a clean dataset ready for feature engineering
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time

print("=" * 80)
print("PROCESSING USDA FOODDATA CENTRAL")
print("=" * 80)

start_time = time.time()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'

# Ensure output directory exists
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Key nutrient IDs from USDA database
NUTRIENT_MAP = {
    1003: 'protein_g',
    1004: 'fat_g',
    1005: 'total_carbs_g',
    1008: 'energy_kcal',
    1079: 'fiber_g',
    1063: 'sugar_g',
    1258: 'saturated_fat_g',
    1087: 'calcium_mg',
    1089: 'iron_mg'
}

print("\nStep 1: Loading food descriptions...")
print("(This may take a minute for large files)")

# Load foods - filter for foundation and sr_legacy foods (most reliable data)
food_df = pd.read_csv(
    DATA_RAW / 'food.csv',
    usecols=['fdc_id', 'data_type', 'description'],
    low_memory=False
)

print(f"   ✓ Loaded {len(food_df):,} total foods")
print(f"   Food types: {food_df['data_type'].value_counts().to_dict()}")

# Filter for foundation_food and sr_legacy_food (most complete nutritional data)
food_df = food_df[food_df['data_type'].isin(['foundation_food', 'sr_legacy_food'])].copy()
print(f"   ✓ Filtered to {len(food_df):,} foundation/SR legacy foods")

print("\nStep 2: Loading nutritional data...")
print("(This will take 2-3 minutes due to file size)")

# Load nutrients for our filtered foods only
relevant_fdc_ids = set(food_df['fdc_id'].values)

# Read nutrients in chunks to manage memory
nutrients_list = []
chunk_size = 1000000

for chunk in pd.read_csv(DATA_RAW / 'food_nutrient.csv', 
                          usecols=['fdc_id', 'nutrient_id', 'amount'],
                          chunksize=chunk_size,
                          low_memory=False):
    # Filter for relevant foods and nutrients
    chunk = chunk[
        (chunk['fdc_id'].isin(relevant_fdc_ids)) &
        (chunk['nutrient_id'].isin(NUTRIENT_MAP.keys()))
    ]
    nutrients_list.append(chunk)
    print(f"   Processed chunk... {len(nutrients_list)} chunks so far")

nutrient_df = pd.concat(nutrients_list, ignore_index=True)
print(f"   ✓ Loaded {len(nutrient_df):,} relevant nutrient records")

print("\nStep 3: Pivoting nutrients to wide format...")

# Pivot nutrients to columns
nutrient_wide = nutrient_df.pivot_table(
    index='fdc_id',
    columns='nutrient_id',
    values='amount',
    aggfunc='first'  # Take first value if duplicates
).reset_index()

# Rename columns using our mapping
nutrient_wide.columns = ['fdc_id'] + [NUTRIENT_MAP.get(col, f'nutrient_{col}') 
                                       for col in nutrient_wide.columns[1:]]

print(f"   ✓ Created wide format with {len(nutrient_wide)} foods")
print(f"   Columns: {nutrient_wide.columns.tolist()}")

print("\nStep 4: Merging with food descriptions...")

# Merge foods with nutrients
foods_complete = food_df.merge(nutrient_wide, on='fdc_id', how='inner')
print(f"   ✓ Merged dataset: {len(foods_complete):,} foods with complete nutrition data")

# Remove rows with missing critical nutrients
critical_nutrients = ['total_carbs_g', 'protein_g', 'fat_g', 'energy_kcal']
foods_complete = foods_complete.dropna(subset=critical_nutrients)
print(f"   ✓ After removing incomplete records: {len(foods_complete):,} foods")

print("\nStep 5: Loading glycemic index data...")

# Load GI table
gi_df = pd.read_csv(DATA_RAW / 'gi_table.csv')
print(f"   ✓ Loaded {len(gi_df)} foods with GI values")

# Try to match foods - this is approximate matching by name
# For better results, you'd need a comprehensive GI database
foods_complete['food_name_lower'] = foods_complete['description'].str.lower()
gi_df['food_name_lower'] = gi_df['food_name'].str.lower()

# Merge (left join to keep all USDA foods, add GI where available)
foods_with_gi = foods_complete.merge(
    gi_df[['food_name_lower', 'glycemic_index']], 
    on='food_name_lower', 
    how='left'
)

# For foods without GI data, estimate based on carb content and fiber
# This is a simplified heuristic
def estimate_gi(row):
    if pd.notna(row['glycemic_index']):
        return row['glycemic_index']
    
    # Estimate based on net carbs and fiber
    if row['total_carbs_g'] < 5:
        return 15  # Very low carb foods
    
    fiber_ratio = row.get('fiber_g', 0) / row['total_carbs_g'] if row['total_carbs_g'] > 0 else 0
    
    if fiber_ratio > 0.15:
        return 45  # High fiber = lower GI
    elif fiber_ratio > 0.08:
        return 60  # Medium fiber
    else:
        return 70  # Low fiber = higher GI

foods_with_gi['glycemic_index'] = foods_with_gi.apply(estimate_gi, axis=1)

print(f"   ✓ GI values: {(~foods_with_gi['glycemic_index'].isna()).sum()} foods have GI")

print("\nStep 6: Cleaning and finalizing dataset...")

# Select final columns
final_columns = [
    'fdc_id',
    'description',
    'data_type',
    'total_carbs_g',
    'fiber_g',
    'sugar_g',
    'protein_g',
    'fat_g',
    'saturated_fat_g',
    'energy_kcal',
    'glycemic_index'
]

# Keep only columns that exist
final_columns = [col for col in final_columns if col in foods_with_gi.columns]
foods_final = foods_with_gi[final_columns].copy()

# Fill remaining missing values with 0 for optional nutrients
for col in ['fiber_g', 'sugar_g', 'saturated_fat_g']:
    if col in foods_final.columns:
        foods_final[col] = foods_final[col].fillna(0)

# Rename for consistency
foods_final = foods_final.rename(columns={'description': 'food_name'})

# Remove outliers (values that don't make nutritional sense)
foods_final = foods_final[
    (foods_final['total_carbs_g'] >= 0) & (foods_final['total_carbs_g'] <= 100) &
    (foods_final['protein_g'] >= 0) & (foods_final['protein_g'] <= 100) &
    (foods_final['fat_g'] >= 0) & (foods_final['fat_g'] <= 100) &
    (foods_final['energy_kcal'] >= 0) & (foods_final['energy_kcal'] <= 900)
]

print(f"   ✓ Final dataset: {len(foods_final):,} foods")

print("\nStep 7: Saving processed dataset...")

# Save to processed folder
output_file = DATA_PROCESSED / 'usda_foods_with_nutrition.csv'
foods_final.to_csv(output_file, index=False)

elapsed = time.time() - start_time
print(f"   ✓ Saved to: {output_file}")

print("\n" + "=" * 80)
print("PROCESSING COMPLETE!")
print("=" * 80)

print(f"\n📊 Dataset Summary:")
print(f"   • Total foods: {len(foods_final):,}")
print(f"   • Features: {len(foods_final.columns)}")
print(f"   • Processing time: {elapsed:.1f} seconds")

print(f"\n🥗 Nutritional Feature Ranges:")
for col in ['total_carbs_g', 'fiber_g', 'protein_g', 'fat_g', 'energy_kcal']:
    if col in foods_final.columns:
        print(f"   • {col}: {foods_final[col].min():.1f} - {foods_final[col].max():.1f}")

print(f"\n📈 Sample of processed foods:")
print(foods_final.head(10).to_string())

print(f"\n✅ Next steps:")
print(f"   1. Review the data: data/processed/usda_foods_with_nutrition.csv")
print(f"   2. Run feature engineering: python scripts/process_features.py")
print(f"   3. Or use this data in notebooks for EDA")

print("\n" + "=" * 80)
