# Gestational Diabetes Meal Recommender

**Springboard Data Science Capstone Project**

## Project Overview

For pregnant women with gestational diabetes, choosing meals that keep blood sugar in a safe range is difficult and stressful. This project builds a machine learning model that predicts whether a meal is likely to cause a high post-prandial (after-meal) glucose spike based on its nutritional profile.

### Business Problem Statement

Gestational diabetes affects 2-10% of pregnancies in the United States, requiring careful dietary management to prevent complications for both mother and baby. The challenge is that predicting blood glucose response to meals is complex—it depends not just on carbohydrates, but on fiber content, fat, protein, glycemic index, and their interactions.

**Objective:** Build a predictive model that, given a meal's nutritional profile (carbs, fiber, fat, protein, glycemic load, etc.), classifies meals into risk categories for post-prandial glucose spikes.

**Target Users:** Pregnant women with gestational diabetes and their healthcare providers.

**Success Metrics:** 
- Model recall >0.85 for high-risk meals (minimize false negatives)
- Precision >0.70 to avoid excessive false alarms
- Deployable as an easy-to-use web application

## Data Sources

1. **USDA FoodData Central**: Comprehensive nutritional data for thousands of foods
2. **Published Glycemic Index/Load Tables**: Scientific literature on GI/GL values
3. **Private Dataset** (optional): De-identified glucose monitoring data for model calibration

## Features

**Input Features:**
- Macronutrients: total carbs, fiber, sugar, protein, fat, saturated fat
- Energy: calories
- Glycemic metrics: glycemic index, glycemic load
- Derived features: carb quality ratio (fiber/carbs), fat-to-carb ratio
- Meal context: meal type (breakfast/lunch/dinner), whole grains indicator
- Composition flags: contains sugary drink, etc.

**Target Variable:**
- Binary classification: `high_risk` (1 = likely glucose spike >140 mg/dL at 1 hour, 0 = safe)

## Modeling Approach

Three models will be developed and compared:

1. **Logistic Regression** (Baseline)
   - Interpretable coefficients for clinical relevance
   - Fast training and inference

2. **Random Forest Classifier**
   - Captures nonlinear interactions between nutrients
   - Feature importance analysis

3. **XGBoost/LightGBM** (Advanced)
   - State-of-the-art performance
   - Handles complex feature interactions

**Evaluation Metrics:**
- Primary: Recall (sensitivity) for high-risk class
- Secondary: Precision, F1-score, ROC-AUC
- Emphasis on minimizing false negatives (health safety priority)

## Project Structure

```
gestational_diabetes_recommender_project/
├── data/
│   ├── raw/                    # Original data files
│   ├── processed/              # Cleaned and feature-engineered data
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling_baseline_lr_rf_xgb.ipynb
│   └── 04_model_evaluation_and_selection.ipynb
├── src/
│   ├── data_prep.py           # Data loading and cleaning functions
│   ├── features.py            # Feature engineering functions
│   └── train_model.py         # Model training pipeline
├── app/
│   ├── app.py                 # Streamlit web application
│   ├── model.pkl              # Trained model
│   └── preprocessor.pkl       # Feature preprocessor
├── reports/
│   ├── figures/               # Visualizations
│   └── capstone_report.pdf    # Final report
├── README.md
├── requirements.txt
└── .gitignore
```

## Deliverables

1. **Jupyter Notebooks**: Complete data pipeline from raw data to trained models
2. **Python Modules**: Reusable code for data processing and modeling
3. **Streamlit App**: Interactive meal risk predictor
4. **Final Report**: Comprehensive capstone documentation
5. **GitHub Repository**: Version-controlled project with documentation

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda for package management

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gestational_diabetes_recommender_project.git
cd gestational_diabetes_recommender_project

# Install dependencies
pip install -r requirements.txt
```

### Usage

1. **Data Collection**: Download USDA FoodData Central and GI tables (instructions in notebooks)
2. **Run Notebooks**: Execute notebooks in order (01 → 04)
3. **Launch App**: `streamlit run app/app.py`

## Technical Stack

- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Machine Learning**: scikit-learn, XGBoost, LightGBM
- **Model Interpretation**: SHAP
- **Web App**: Streamlit
- **Version Control**: Git/GitHub

## Project Timeline

- **Week 1-2**: Data collection, cleaning, and EDA
- **Week 3**: Feature engineering
- **Week 4-5**: Model development and tuning
- **Week 6**: Model evaluation and selection
- **Week 7**: Streamlit app development
- **Week 8**: Final report and presentation

## Ethical Considerations

- **Medical Disclaimer**: This tool is for educational purposes and should not replace medical advice
- **Privacy**: Any personal health data remains private and de-identified
- **Bias Mitigation**: Model trained on diverse food types and nutritional profiles
- **Transparency**: Predictions include explanations via SHAP values

## Author

Sanja - Springboard Data Science Career Track

## Acknowledgments

- Springboard mentor and community
- USDA for public nutritional data
- Healthcare professionals for domain expertise

## License

This project is for educational purposes as part of a Springboard capstone.

---

*Last Updated: December 25, 2025*
