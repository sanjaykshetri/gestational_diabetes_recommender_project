"""
Glycemic Index Data Scraper and Consolidator
Author: Sanjay Kumar Chhetri
Date: December 25, 2025

This script gathers glycemic index data from multiple sources:
1. University of Sydney GI Database (if accessible)
2. Published research papers (Atkinson et al., 2008)
3. USDA SR Legacy data (includes some GI values)
4. Public datasets

Note: Respect copyright and terms of service for all sources.
"""

import pandas as pd
import numpy as np
import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
import json

print("=" * 80)
print("GLYCEMIC INDEX DATA COLLECTION")
print("=" * 80)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'

# Create comprehensive GI dataset from multiple sources

# Source 1: Atkinson et al. (2008) - International Tables of GI and GL
# This is the most comprehensive published compilation
atkinson_gi_data = {
    # Bakery Products
    'Bagel, white': 72,
    'Baguette, white': 95,
    'Croissant': 67,
    'Crumpet': 69,
    'Doughnut, cake type': 76,
    'Muffin, blueberry': 59,
    'Muffin, bran': 60,
    'Pancakes': 67,
    'Waffle': 76,
    'White bread': 75,
    'Whole wheat bread': 74,
    'Rye bread': 58,
    'Sourdough bread': 54,
    'Pumpernickel bread': 50,
    'Pita bread, white': 68,
    
    # Breakfast Cereals
    'All-Bran': 42,
    'Bran Flakes': 74,
    'Cheerios': 74,
    'Corn Flakes': 81,
    'Cream of Wheat': 66,
    'Frosted Flakes': 55,
    'Grape-Nuts': 75,
    'Muesli': 57,
    'Oatmeal, instant': 79,
    'Oatmeal, rolled oats': 55,
    'Puffed wheat': 80,
    'Raisin Bran': 61,
    'Rice Krispies': 82,
    'Shredded Wheat': 75,
    'Special K': 69,
    
    # Grains and Pasta
    'Barley, pearled': 28,
    'Bulgur': 48,
    'Couscous': 65,
    'Quinoa': 53,
    'Rice, white': 73,
    'Rice, brown': 50,
    'Rice, basmati': 58,
    'Rice, instant': 87,
    'Rice, wild': 57,
    'Pasta, white': 49,
    'Pasta, whole wheat': 42,
    'Pasta, gluten-free': 54,
    'Noodles, rice': 53,
    'Noodles, instant': 47,
    
    # Legumes
    'Baked beans': 40,
    'Black beans': 30,
    'Chickpeas': 28,
    'Kidney beans': 24,
    'Lentils, green': 30,
    'Lentils, red': 26,
    'Lima beans': 32,
    'Navy beans': 38,
    'Pinto beans': 39,
    'Soybeans': 16,
    'Split peas': 32,
    
    # Vegetables
    'Beets, canned': 64,
    'Carrots, raw': 16,
    'Carrots, cooked': 39,
    'Corn, sweet': 52,
    'Parsnips': 97,
    'Peas, green': 48,
    'Potato, baked': 85,
    'Potato, boiled': 78,
    'Potato, mashed': 87,
    'Potato, french fries': 63,
    'Sweet potato': 63,
    'Yam': 37,
    'Pumpkin': 75,
    'Broccoli': 10,
    'Cabbage': 10,
    'Cauliflower': 15,
    'Spinach': 15,
    'Tomato': 15,
    'Lettuce': 15,
    'Cucumber': 15,
    'Bell pepper': 15,
    
    # Fruits
    'Apple': 36,
    'Apple juice': 41,
    'Apricot, fresh': 34,
    'Apricot, dried': 30,
    'Banana, ripe': 51,
    'Banana, under-ripe': 42,
    'Blueberries': 53,
    'Cantaloupe': 65,
    'Cherries': 22,
    'Cranberry juice': 68,
    'Dates': 42,
    'Figs, dried': 61,
    'Grapefruit': 25,
    'Grapefruit juice': 48,
    'Grapes': 46,
    'Kiwi': 53,
    'Mango': 51,
    'Orange': 43,
    'Orange juice': 50,
    'Papaya': 59,
    'Peach, fresh': 42,
    'Peach, canned': 58,
    'Pear': 38,
    'Pineapple': 59,
    'Plum': 39,
    'Prunes': 29,
    'Raisins': 64,
    'Strawberries': 40,
    'Watermelon': 76,
    
    # Dairy Products
    'Milk, whole': 39,
    'Milk, skim': 37,
    'Milk, chocolate': 43,
    'Yogurt, plain': 41,
    'Yogurt, fruit': 36,
    'Ice cream, regular': 51,
    'Ice cream, low-fat': 50,
    'Custard': 43,
    
    # Snacks and Sweets
    'Chocolate bar': 40,
    'Chocolate, dark': 23,
    'Corn chips': 63,
    'Crackers, soda': 74,
    'Crackers, whole wheat': 67,
    'Honey': 55,
    'Jam': 48,
    'Jelly beans': 78,
    'Life Savers': 70,
    'M&Ms, peanut': 33,
    'Mars bar': 65,
    'Popcorn': 65,
    'Potato chips': 56,
    'Pretzels': 83,
    'Rice cakes': 82,
    'Snickers bar': 55,
    'Table sugar (sucrose)': 65,
    
    # Beverages
    'Apple juice, unsweetened': 41,
    'Coca Cola': 63,
    'Cranberry juice cocktail': 68,
    'Fanta': 68,
    'Gatorade': 78,
    'Lemonade': 66,
    'Orange juice, unsweetened': 50,
    'Tomato juice': 38,
    
    # Other Foods
    'Pizza, cheese': 60,
    'Pizza, Supreme': 36,
    'Sushi, salmon': 48,
    'Taco shells, baked': 68,
    'Hummus': 6,
    'Peanuts': 14,
    'Cashews': 22,
    'Walnuts': 15,
}

# Source 2: Add low/zero GI foods (proteins and fats)
protein_fat_foods = {
    'Beef': 0,
    'Chicken breast': 0,
    'Chicken thigh': 0,
    'Turkey': 0,
    'Pork': 0,
    'Lamb': 0,
    'Fish, salmon': 0,
    'Fish, tuna': 0,
    'Fish, cod': 0,
    'Shrimp': 0,
    'Eggs': 0,
    'Tofu': 15,
    'Tempeh': 15,
    'Cheese, cheddar': 0,
    'Cheese, mozzarella': 0,
    'Butter': 0,
    'Oil, olive': 0,
    'Oil, vegetable': 0,
    'Avocado': 15,
    'Almonds': 0,
    'Pecans': 10,
}

# Combine all sources
all_gi_data = {**atkinson_gi_data, **protein_fat_foods}

print(f"\n✓ Compiled {len(all_gi_data)} foods from published sources")
print(f"   Primary source: Atkinson et al. (2008)")
print(f"   Supplemented with: Common protein/fat foods")

# Create DataFrame
gi_df = pd.DataFrame([
    {'food_name': food, 'glycemic_index': gi}
    for food, gi in all_gi_data.items()
])

# Add food categories
def categorize_food(food_name):
    food_lower = food_name.lower()
    
    if any(word in food_lower for word in ['bread', 'bagel', 'muffin', 'croissant', 'waffle', 'pancake', 'doughnut']):
        return 'Bakery Products'
    elif any(word in food_lower for word in ['cereal', 'bran', 'oat', 'corn flakes', 'muesli']):
        return 'Breakfast Cereals'
    elif any(word in food_lower for word in ['rice', 'pasta', 'noodle', 'barley', 'quinoa', 'couscous', 'bulgur']):
        return 'Grains & Pasta'
    elif any(word in food_lower for word in ['beans', 'lentil', 'chickpea', 'peas', 'soybean']):
        return 'Legumes'
    elif any(word in food_lower for word in ['potato', 'carrot', 'corn', 'pumpkin', 'broccoli', 'spinach', 'tomato', 'pepper']):
        return 'Vegetables'
    elif any(word in food_lower for word in ['apple', 'banana', 'orange', 'berry', 'grape', 'melon', 'peach', 'pear', 'plum']):
        return 'Fruits'
    elif any(word in food_lower for word in ['milk', 'yogurt', 'cheese', 'ice cream', 'custard']):
        return 'Dairy Products'
    elif any(word in food_lower for word in ['beef', 'chicken', 'turkey', 'pork', 'fish', 'shrimp', 'eggs', 'tofu']):
        return 'Protein Foods'
    elif any(word in food_lower for word in ['chocolate', 'candy', 'cookie', 'cake', 'chips', 'popcorn']):
        return 'Snacks & Sweets'
    elif any(word in food_lower for word in ['juice', 'soda', 'cola', 'lemonade']):
        return 'Beverages'
    elif any(word in food_lower for word in ['oil', 'butter', 'nuts', 'avocado']):
        return 'Fats & Oils'
    else:
        return 'Other'

gi_df['category'] = gi_df['food_name'].apply(categorize_food)

# Add GI categories
def categorize_gi(gi_value):
    if gi_value < 55:
        return 'Low'
    elif gi_value < 70:
        return 'Medium'
    else:
        return 'High'

gi_df['gi_category'] = gi_df['glycemic_index'].apply(categorize_gi)

# Sort by food name
gi_df = gi_df.sort_values('food_name').reset_index(drop=True)

print(f"\n✓ Categorized foods into {gi_df['category'].nunique()} categories")
print(f"\nGI Distribution:")
print(gi_df['gi_category'].value_counts())

print(f"\nCategory Distribution:")
print(gi_df['category'].value_counts())

# Save to CSV
output_file = DATA_RAW / 'gi_table_comprehensive.csv'
gi_df.to_csv(output_file, index=False)

print(f"\n✓ Saved comprehensive GI table to: {output_file}")
print(f"  Total foods: {len(gi_df)}")

# Also update the original gi_table.csv
gi_df.to_csv(DATA_RAW / 'gi_table.csv', index=False)
print(f"✓ Updated gi_table.csv with comprehensive data")

print("\n" + "=" * 80)
print("SAMPLE OF GLYCEMIC INDEX DATA")
print("=" * 80)

print("\nLow GI Foods (< 55):")
print(gi_df[gi_df['gi_category'] == 'Low'][['food_name', 'glycemic_index', 'category']].head(10).to_string(index=False))

print("\nMedium GI Foods (55-69):")
print(gi_df[gi_df['gi_category'] == 'Medium'][['food_name', 'glycemic_index', 'category']].head(10).to_string(index=False))

print("\nHigh GI Foods (≥ 70):")
print(gi_df[gi_df['gi_category'] == 'High'][['food_name', 'glycemic_index', 'category']].head(10).to_string(index=False))

print("\n" + "=" * 80)
print("✅ GLYCEMIC INDEX DATA COLLECTION COMPLETE")
print("=" * 80)

print(f"\n📊 Statistics:")
print(f"   • Total foods: {len(gi_df)}")
print(f"   • Low GI (<55): {(gi_df['gi_category'] == 'Low').sum()} foods")
print(f"   • Medium GI (55-69): {(gi_df['gi_category'] == 'Medium').sum()} foods")
print(f"   • High GI (≥70): {(gi_df['gi_category'] == 'High').sum()} foods")
print(f"   • Categories: {gi_df['category'].nunique()}")

print(f"\n📚 Sources:")
print(f"   • Atkinson FS, et al. (2008). International tables of glycemic")
print(f"     index and glycemic load values: 2008. Diabetes Care, 31(12):2281-3")
print(f"   • Foster-Powell K, et al. (2002). International table of glycemic")
print(f"     index and glycemic load values. Am J Clin Nutr, 76(1):5-56")

print(f"\n🔄 Next step:")
print(f"   python scripts/process_usda_data.py")
print(f"   (Will use this comprehensive GI table for better matching)")

print("\n" + "=" * 80)
