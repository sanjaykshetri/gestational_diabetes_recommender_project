"""
Script to help download and prepare data for the project
"""

import requests
import pandas as pd
from pathlib import Path
import zipfile
import io

# Project paths
DATA_RAW = Path("data/raw")
DATA_RAW.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("GESTATIONAL DIABETES MEAL PREDICTOR - DATA DOWNLOAD HELPER")
print("=" * 80)

# ============================================================================
# Option 1: Create a sample GI table
# ============================================================================

def create_sample_gi_table():
    """Create a sample glycemic index reference table"""
    
    sample_gi_data = pd.DataFrame({
        'food_name': [
            # Grains
            'White Rice', 'Brown Rice', 'Basmati Rice', 'Wild Rice',
            'White Bread', 'Whole Wheat Bread', 'Sourdough Bread', 'Rye Bread',
            'Pasta (white)', 'Pasta (whole wheat)', 'Quinoa', 'Couscous',
            'Corn Flakes', 'Oatmeal', 'Bran Flakes', 'Muesli',
            
            # Fruits
            'Apple', 'Banana', 'Orange', 'Grapes', 'Watermelon', 'Strawberries',
            'Mango', 'Pineapple', 'Peach', 'Pear', 'Cherries', 'Grapefruit',
            
            # Vegetables
            'Potato (baked)', 'Sweet Potato', 'Carrots (raw)', 'Carrots (cooked)',
            'Broccoli', 'Spinach', 'Tomato', 'Lettuce', 'Corn', 'Peas',
            
            # Legumes
            'Lentils', 'Chickpeas', 'Black Beans', 'Kidney Beans', 'Soybeans',
            
            # Dairy
            'Milk (whole)', 'Milk (skim)', 'Yogurt (plain)', 'Ice Cream',
            
            # Snacks/Beverages
            'Soda', 'Orange Juice', 'Apple Juice', 'Pretzels', 'Potato Chips',
            'Chocolate', 'Honey', 'Table Sugar',
            
            # Proteins
            'Chicken Breast', 'Salmon', 'Beef', 'Tofu', 'Eggs'
        ],
        'glycemic_index': [
            # Grains
            73, 50, 58, 45, 75, 74, 52, 50,
            49, 42, 53, 65, 81, 55, 74, 57,
            
            # Fruits
            36, 51, 43, 46, 76, 41, 51, 59, 42, 38, 22, 25,
            
            # Vegetables
            85, 63, 16, 39, 10, 15, 15, 10, 52, 51,
            
            # Legumes
            32, 28, 30, 24, 16,
            
            # Dairy
            39, 37, 41, 51,
            
            # Snacks/Beverages
            63, 50, 44, 83, 51, 40, 61, 65,
            
            # Proteins
            0, 0, 0, 15, 0
        ],
        'category': [
            # Grains
            'grains', 'grains', 'grains', 'grains', 'grains', 'grains', 'grains', 'grains',
            'grains', 'grains', 'grains', 'grains', 'grains', 'grains', 'grains', 'grains',
            
            # Fruits
            'fruits', 'fruits', 'fruits', 'fruits', 'fruits', 'fruits',
            'fruits', 'fruits', 'fruits', 'fruits', 'fruits', 'fruits',
            
            # Vegetables
            'vegetables', 'vegetables', 'vegetables', 'vegetables',
            'vegetables', 'vegetables', 'vegetables', 'vegetables', 'vegetables', 'vegetables',
            
            # Legumes
            'legumes', 'legumes', 'legumes', 'legumes', 'legumes',
            
            # Dairy
            'dairy', 'dairy', 'dairy', 'dairy',
            
            # Snacks/Beverages
            'beverages', 'beverages', 'beverages', 'snacks', 'snacks',
            'snacks', 'sweeteners', 'sweeteners',
            
            # Proteins
            'protein', 'protein', 'protein', 'protein', 'protein'
        ],
        'serving_size_g': [150] * 57
    })
    
    # Categorize GI
    def categorize_gi(gi):
        if gi < 55:
            return 'low'
        elif gi < 70:
            return 'medium'
        else:
            return 'high'
    
    sample_gi_data['gi_category'] = sample_gi_data['glycemic_index'].apply(categorize_gi)
    
    # Save
    output_path = DATA_RAW / 'gi_table.csv'
    sample_gi_data.to_csv(output_path, index=False)
    print(f"\n✓ Created sample GI table: {output_path}")
    print(f"  - {len(sample_gi_data)} foods")
    print(f"  - {sample_gi_data['category'].nunique()} categories")
    
    return sample_gi_data

# ============================================================================
# Option 2: USDA FoodData Central Download Instructions
# ============================================================================

def print_usda_instructions():
    """Print instructions for downloading USDA data"""
    
    print("\n" + "=" * 80)
    print("USDA FOODDATA CENTRAL DOWNLOAD INSTRUCTIONS")
    print("=" * 80)
    
    print("""
📥 **Manual Download (Recommended):**

1. Visit: https://fdc.nal.usda.gov/download-datasets.html

2. Download one of these datasets:
   • Foundation Foods (smaller, curated)
   • SR Legacy (larger, comprehensive)

3. Extract these files to data/raw/:
   • food.csv
   • food_nutrient.csv  
   • nutrient.csv

4. Files are large (100-500 MB), but most comprehensive

---

🔑 **API Access (Alternative):**

1. Get free API key: https://api.data.gov/signup/
2. Use Python requests to fetch data programmatically
3. See example code in notebooks/01_data_cleaning_eda.ipynb

---

📊 **What You'll Get:**

• 350,000+ food items
• Complete nutritional profiles
• Carbs, fiber, sugar, protein, fat, calories, and more
• Official USDA data used by nutrition apps

---

⏱️ **Processing Time:**

• Download: 5-10 minutes
• Load in Python: 1-2 minutes
• Initial filtering: 2-3 minutes

---

💡 **Alternative:** For quick start, use the sample data generated by
   the EDA notebook. Real USDA data recommended for final models.
    """)

# ============================================================================
# Option 3: Create sample comprehensive dataset
# ============================================================================

def create_comprehensive_sample_data():
    """Create a more comprehensive sample dataset for immediate use"""
    
    print("\n" + "=" * 80)
    print("CREATING COMPREHENSIVE SAMPLE DATASET")
    print("=" * 80)
    
    # Create realistic sample data
    np.random.seed(42)
    
    foods = []
    for _ in range(500):
        carbs = np.random.uniform(0, 100)
        gi = np.random.uniform(20, 90)
        
        food = {
            'food_name': f'Food_{np.random.randint(1000, 9999)}',
            'total_carbs_g': carbs,
            'fiber_g': np.random.uniform(0, min(carbs * 0.3, 15)),
            'sugar_g': np.random.uniform(0, min(carbs * 0.5, 30)),
            'protein_g': np.random.uniform(0, 40),
            'fat_g': np.random.uniform(0, 30),
            'saturated_fat_g': np.random.uniform(0, 10),
            'energy_kcal': np.random.uniform(50, 500),
            'glycemic_index': gi
        }
        foods.append(food)
    
    df = pd.DataFrame(foods)
    
    output_path = DATA_RAW / 'sample_comprehensive_foods.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Created comprehensive sample dataset: {output_path}")
    print(f"  - {len(df)} food items")
    print(f"  - Ready for feature engineering")
    
    return df

# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    import numpy as np
    
    print("\n🍽️ What would you like to do?\n")
    print("1. Create sample GI reference table")
    print("2. View USDA download instructions")
    print("3. Create comprehensive sample dataset (for testing)")
    print("4. All of the above")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice in ['1', '4']:
            gi_data = create_sample_gi_table()
        
        if choice in ['2', '4']:
            print_usda_instructions()
        
        if choice in ['3', '4']:
            sample_data = create_comprehensive_sample_data()
        
        print("\n" + "=" * 80)
        print("✓ DATA PREPARATION COMPLETE")
        print("=" * 80)
        print("\n📝 Next Steps:")
        print("1. Review files in data/raw/")
        print("2. Open notebooks/01_data_cleaning_eda.ipynb")
        print("3. Run the EDA notebook")
        print("4. Proceed to feature engineering (Notebook 02)")
        
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
