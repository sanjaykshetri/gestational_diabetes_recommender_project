# Problem Statement: Gestational Diabetes Meal Risk Predictor

**Author:** Sanjay Kumar Chhetri  
**Springboard Data Science Capstone Project**

## 1. Problem Identification

### Background and Context

Gestational diabetes mellitus (GDM) affects between 2-10% of pregnancies annually in the United States, with rates increasing globally. Women diagnosed with GDM must carefully manage their blood glucose levels throughout pregnancy to prevent serious complications including preeclampsia, cesarean delivery, macrosomia (large birth weight), and increased long-term diabetes risk for both mother and child.

The cornerstone of GDM management is dietary control. However, predicting how a specific meal will affect post-prandial (after-meal) blood glucose is remarkably complex. Blood sugar response depends not only on carbohydrate quantity but also on:

- **Fiber content** (slows glucose absorption)
- **Fat and protein** (modify glycemic response)
- **Glycemic index** (rate of carbohydrate digestion)
- **Meal timing** and composition interactions
- Individual metabolic variations

Most current dietary guidance for GDM patients is generic and rule-based ("limit carbs to 45g per meal," "avoid white rice and sugary drinks"). While these rules help, they don't account for the nuanced interactions between nutrients. This leads to:

1. **Decision fatigue**: Women must constantly calculate, worry, and second-guess meal choices
2. **Unnecessary restrictions**: Some safe meals may be avoided due to overly conservative guidelines
3. **Unexpected spikes**: Seemingly "safe" meals can still cause dangerous glucose elevations
4. **Stress and anxiety**: The uncertainty compounds the already-stressful experience of managing a high-risk pregnancy

### The Opportunity

With the advent of continuous glucose monitors (CGMs) and comprehensive nutritional databases, we now have access to:

- Rich meal-level nutritional data (USDA FoodData Central, glycemic index databases)
- Real-world glucose response patterns from CGM devices
- Machine learning techniques that can model complex, nonlinear relationships

This creates an opportunity to build a **data-driven meal risk predictor** that provides personalized, probabilistic guidance rather than rigid rules.

### Business/Clinical Objective

**Develop a machine learning classification model that predicts whether a meal will cause a high post-prandial glucose spike (>140 mg/dL at 1 hour) for pregnant women with gestational diabetes, based on the meal's nutritional profile.**

The model will power a simple, accessible web application that:
- Allows users to input or select meals
- Returns a risk category (Low / Medium / High)
- Explains which nutritional factors drive the risk
- Suggests modifications to reduce glucose impact

### Target Audience

**Primary users:**
- Pregnant women diagnosed with gestational diabetes
- Partners and family members helping with meal planning

**Secondary users:**
- Registered dietitians and certified diabetes educators
- Endocrinologists and obstetricians managing GDM patients
- Digital health companies building pregnancy/diabetes management platforms

### Value Proposition

**For patients:**
- Reduced anxiety through clearer, data-backed meal guidance
- Empowerment to make informed food choices
- Better glucose control leading to healthier pregnancy outcomes
- Time saved on meal planning and worry

**For healthcare providers:**
- Scalable tool to support patient education
- Data-driven complement to clinical guidelines
- Reduced patient calls/messages about meal choices

**For healthcare systems:**
- Potential reduction in GDM complications (costly NICU stays, cesarean deliveries)
- Improved patient satisfaction and engagement
- Foundation for telehealth and remote monitoring integration

## 2. Success Criteria

### Model Performance Metrics

Given the health-critical nature of this application, we prioritize **minimizing false negatives** (failing to warn about a risky meal). Our primary metrics are:

1. **Recall (Sensitivity) ≥ 0.85** for the high-risk class
   - We want to catch at least 85% of meals that would cause dangerous glucose spikes
   - Missing a risky meal is more harmful than over-warning

2. **Precision ≥ 0.70** for the high-risk class
   - Balance against false alarms to avoid decision fatigue
   - Still maintain practical usability

3. **F1-Score ≥ 0.75**
   - Harmonic mean ensuring balanced performance

4. **ROC-AUC ≥ 0.80**
   - Overall discriminatory ability across thresholds

### Business/Clinical Success Criteria

**Phase 1 (Capstone MVP):**
- ✅ Functional predictive model meeting performance thresholds
- ✅ Deployed Streamlit web application accessible via URL
- ✅ Model interpretability via SHAP or feature importance
- ✅ Comprehensive documentation and reproducible code

**Phase 2 (Post-Capstone, Real-World Validation):**
- User testing with 10-20 women with GDM
- Qualitative feedback on usability and trust
- Comparison to actual glucose readings (if CGM data available)
- Iteration based on user needs

**Long-Term Vision:**
- Integration with meal-tracking apps (MyFitnessPal, etc.)
- Mobile app version
- Personalization based on individual glucose patterns
- Clinical validation study and potential FDA clearance as clinical decision support

## 3. Constraints and Assumptions

### Constraints

1. **Data limitations:**
   - No large, publicly available dataset linking specific meals to glucose responses in GDM
   - Must synthesize training data from nutritional databases + glycemic research
   - Private/personal data (if used) must remain de-identified

2. **Regulatory:**
   - Cannot make medical claims without FDA clearance
   - Must include clear disclaimers ("educational purposes only, not medical advice")

3. **Computational:**
   - Model must be lightweight enough to run in a free Streamlit deployment
   - Inference time <2 seconds for good user experience

4. **Timeline:**
   - 8-week Springboard capstone timeline
   - Must balance sophistication with deliverability

### Assumptions

1. **Generalizability:**
   - Nutritional principles (GI, fiber effect, etc.) from general population research apply reasonably to GDM
   - Synthetic labels based on established glycemic science can train an initial useful model

2. **User behavior:**
   - Users can accurately identify meals or input nutritional information
   - Users will follow tool guidance in context with medical advice (not as replacement)

3. **Technical:**
   - USDA FoodData and GI tables are sufficiently accurate
   - Binary classification (high-risk vs. safe) is clinically meaningful
   - Feature engineering can capture key nutrient interactions

## 4. Out of Scope (For This Capstone)

- Personalized predictions based on individual patient history
- Mobile app development
- Real-time CGM integration
- Recipe database or meal planning features
- Multi-class classification (low/medium/high risk)
- International food databases beyond USDA
- Clinical validation study
- Medication or insulin dosing recommendations

---

## Next Steps

1. **Data Collection:**
   - Download USDA FoodData Central
   - Compile glycemic index/load tables from literature
   - (Optional) Collect small private dataset for validation

2. **Exploratory Data Analysis:**
   - Understand distributions of nutritional features
   - Identify correlations and patterns
   - Define labeling strategy for synthetic target variable

3. **Feature Engineering:**
   - Compute derived features (glycemic load, ratios)
   - Handle missing values
   - Create meal-level aggregations

4. **Modeling:**
   - Baseline: Logistic Regression
   - Advanced: Random Forest, XGBoost
   - Hyperparameter tuning and cross-validation
   - Model selection based on recall/precision trade-off

5. **Deployment:**
   - Save trained model and preprocessor
   - Build Streamlit app with prediction + explanation interface
   - Deploy to Streamlit Community Cloud

6. **Documentation:**
   - Complete Jupyter notebooks with narrative
   - Final capstone report
   - GitHub README with screenshots and instructions

---

*Document Version: 1.0*  
*Last Updated: December 25, 2025*  
*Project: Gestational Diabetes Meal Risk Predictor*  
*Author: Sanja*
