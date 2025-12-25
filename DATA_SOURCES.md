# Data Sources and Collection Guide

## Required Datasets

### 1. USDA FoodData Central

**Purpose:** Comprehensive nutritional composition data for foods

**Download Instructions:**
1. Visit: https://fdc.nal.usda.gov/download-datasets.html
2. Select: **FoodData Central CSV** (Foundation Foods or SR Legacy)
3. Download the ZIP file (approx. 100-200 MB)
4. Extract the following files to `data/raw/`:
   - `food.csv` - Main food items table
   - `food_nutrient.csv` - Nutrient values for each food
   - `nutrient.csv` - Nutrient definitions

**Key Fields Needed:**
- Food Description
- Carbohydrates (g)
- Fiber (g)
- Sugars (g)
- Protein (g)
- Total Fat (g)
- Saturated Fat (g)
- Energy (kcal)

**Alternative:** Use FoodData Central API
```python
import requests
API_KEY = 'your_api_key'
url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}'
```

---

### 2. Glycemic Index Reference Table

**Purpose:** GI and GL values for foods

**Option A - University of Sydney GI Database**
- Website: https://glycemicindex.com/
- Requires registration for full database
- Most authoritative source

**Option B - Published Research Papers**
- Atkinson et al. (2008): "International Tables of Glycemic Index and Glycemic Load Values"
- Foster-Powell et al. (2002): "International table of glycemic index and glycemic load values"
- Available through PubMed/academic libraries

**Option C - Compiled Tables**
- Create from multiple sources
- Cross-reference with USDA data

**Required Fields:**
- `food_name` - Food item name
- `glycemic_index` - GI value (0-100+)
- `glycemic_load` - GL value (optional, can calculate)
- `category` - Food category (grains, fruits, vegetables, etc.)
- `serving_size_g` - Reference serving size

**Sample GI Table Structure:**
```csv
food_name,glycemic_index,glycemic_load,category,serving_size_g
White Rice,73,29,grains,150
Brown Rice,68,16,grains,150
Apple,36,6,fruits,120
Banana,51,13,fruits,120
```

---

### 3. Optional: Private Glucose Data (CGM/Glucometer)

**Purpose:** Real-world validation of predictions

**Data Collection:**
- Use continuous glucose monitor (CGM) or finger-stick glucometer
- Track for 2-4 weeks
- Record:
  - Date/time
  - Pre-meal glucose (mg/dL)
  - Meal description
  - Portion sizes
  - Post-meal glucose at 1-hour and 2-hour

**Privacy:**
- Keep this data in `data/raw/private_glucose_data.csv`
- Add to `.gitignore` to avoid publishing
- Use only for model calibration/validation
- Report only aggregated results in capstone

**Sample Structure:**
```csv
date,time,pre_meal_glucose,meal_description,carbs_g,fiber_g,glucose_1hr,glucose_2hr
2025-12-25,08:00,95,Oatmeal with berries,45,8,128,105
2025-12-25,12:30,102,Chicken salad with quinoa,35,6,115,98
```

---

## Data Processing Workflow

1. **Download & Extract**
   - USDA data → `data/raw/`
   - GI table → `data/raw/gi_table.csv`

2. **Load in Notebook 01**
   - Read CSV files
   - Inspect structure and quality
   - Initial cleaning

3. **Merge & Engineer Features (Notebook 02)**
   - Join USDA + GI data
   - Calculate derived features
   - Create target labels

4. **Model Training (Notebook 03)**
   - Train/test split
   - Model development
   - Evaluation

---

## Troubleshooting

**Issue:** USDA files too large
- **Solution:** Filter to relevant food categories (grains, fruits, vegetables, proteins)
- Use SQL or chunked reading: `pd.read_csv(file, chunksize=10000)`

**Issue:** Missing GI values
- **Solution:** 
  - Use category-based imputation
  - Research GI for similar foods
  - Flag as missing and handle in modeling

**Issue:** Food name mismatches between datasets
- **Solution:**
  - Fuzzy string matching (`fuzzywuzzy` library)
  - Manual mapping of common foods
  - Standardize naming conventions

---

## Data Citation

Remember to cite data sources in your final report:

**USDA:**
> U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2025. fdc.nal.usda.gov.

**GI Tables:**
> Atkinson, F. S., Foster-Powell, K., & Brand-Miller, J. C. (2008). International tables of glycemic index and glycemic load values: 2008. Diabetes Care, 31(12), 2281-2283.

---

*Last Updated: December 25, 2025*
