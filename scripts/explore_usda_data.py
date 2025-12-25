"""
Quick exploration of USDA FoodData Central files
Author: Sanjay Kumar Chhetri
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 80)
print("EXPLORING USDA FOODDATA CENTRAL")
print("=" * 80)

# Paths
DATA_RAW = Path(__file__).parent.parent / 'data' / 'raw'

print("\n1. Loading food.csv (sample)...")
# Load first 10000 rows to explore structure
food_df = pd.read_csv(DATA_RAW / 'food.csv', nrows=10000, low_memory=False)

print(f"\nColumns in food.csv:")
print(food_df.columns.tolist())
print(f"\nShape (first 10k rows): {food_df.shape}")
print(f"\nData types:\n{food_df.dtypes}")
print(f"\nFirst 3 rows:\n{food_df.head(3)}")
print(f"\nFood categories:\n{food_df['data_type'].value_counts()}")

print("\n" + "=" * 80)
print("\n2. Loading food_nutrient.csv (sample)...")
# Load sample to explore structure
nutrient_df = pd.read_csv(DATA_RAW / 'food_nutrient.csv', nrows=10000, low_memory=False)

print(f"\nColumns in food_nutrient.csv:")
print(nutrient_df.columns.tolist())
print(f"\nShape (first 10k rows): {nutrient_df.shape}")
print(f"\nFirst 3 rows:\n{nutrient_df.head(3)}")
print(f"\nUnique nutrients (sample): {nutrient_df['nutrient_id'].nunique()}")

print("\n" + "=" * 80)
print("\n3. Key Nutrient IDs to Extract:")
print("""
Common nutrient_id mappings from USDA:
- 1003: Protein (g)
- 1004: Total lipid (fat) (g)
- 1005: Carbohydrate, by difference (g)
- 1008: Energy (kcal)
- 1079: Fiber, total dietary (g)
- 1063: Sugars, total including NLEA (g)
- 1258: Fatty acids, total saturated (g)
- 1087: Calcium (mg)
- 1089: Iron (mg)

We'll need to map these when processing!
""")

print("\n" + "=" * 80)
print("\n✓ Exploration complete!")
print("\nNext step: Run process_usda_data.py to create working dataset")
