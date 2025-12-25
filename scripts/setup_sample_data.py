"""
Quick setup script - creates sample data without interaction
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Create directories
DATA_RAW = Path("data/raw")
DATA_RAW.mkdir(parents=True, exist_ok=True)

print("Creating sample datasets...")

# 1. Create GI Table
gi_data = pd.DataFrame({
    'food_name': [
        'White Rice', 'Brown Rice', 'Quinoa', 'White Bread', 'Whole Wheat Bread',
        'Sweet Potato', 'Potato', 'Banana', 'Apple', 'Orange',
        'Chicken Breast', 'Salmon', 'Tofu', 'Lentils', 'Black Beans',
        'Broccoli', 'Spinach', 'Carrots', 'Soda', 'Orange Juice',
        'Oatmeal', 'Corn Flakes', 'Pasta', 'Yogurt', 'Milk'
    ],
    'glycemic_index': [73, 50, 53, 75, 74, 63, 85, 51, 36, 43, 0, 0, 15, 32, 30, 10, 15, 39, 63, 50, 55, 81, 49, 41, 39],
    'category': ['grains']*5 + ['vegetables']*2 + ['fruits']*3 + ['protein']*5 + ['vegetables']*3 + ['beverages']*2 + ['grains']*3 + ['dairy']*2,
    'gi_category': ['high', 'medium', 'medium', 'high', 'high', 'medium', 'high', 'medium', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'low', 'medium', 'medium', 'medium', 'high', 'low', 'low', 'low']
})

gi_data.to_csv(DATA_RAW / 'gi_table.csv', index=False)
print(f"✓ Created gi_table.csv with {len(gi_data)} foods")

# 2. Create comprehensive sample data
np.random.seed(42)
n_samples = 300

sample_data = pd.DataFrame({
    'food_name': [f'Food_{i}' for i in range(n_samples)],
    'total_carbs_g': np.random.uniform(0, 100, n_samples),
    'fiber_g': np.random.uniform(0, 15, n_samples),
    'sugar_g': np.random.uniform(0, 30, n_samples),
    'protein_g': np.random.uniform(0, 40, n_samples),
    'fat_g': np.random.uniform(0, 30, n_samples),
    'saturated_fat_g': np.random.uniform(0, 10, n_samples),
    'energy_kcal': np.random.uniform(50, 500, n_samples),
    'glycemic_index': np.random.uniform(20, 90, n_samples)
})

sample_data.to_csv(DATA_RAW / 'sample_foods.csv', index=False)
print(f"✓ Created sample_foods.csv with {len(sample_data)} foods")

print("\n✅ Sample data ready! Next steps:")
print("1. Open notebooks/01_data_cleaning_eda.ipynb")
print("2. Run the notebook cells")
print("3. Move to notebook 02 for feature engineering")
