"""
Master Pipeline Script
Runs the complete ML pipeline from data processing to model deployment
"""

import subprocess
import sys
from pathlib import Path

print("=" * 80)
print("GESTATIONAL DIABETES PREDICTOR - COMPLETE PIPELINE")
print("=" * 80)

PROJECT_ROOT = Path(__file__).parent.parent

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*80}")
    print(f"STEP: {description}")
    print(f"{'='*80}\n")
    
    script_path = PROJECT_ROOT / 'scripts' / script_name
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# Step 1: Setup Data
print("\n🔄 Starting complete pipeline...")
success = True

if run_script('setup_sample_data.py', '1. Setting up sample data'):
    print("✅ Sample data ready")
else:
    print("⚠️ Sample data setup had issues, continuing...")

# Step 2: Feature Engineering
if run_script('process_features.py', '2. Feature engineering'):
    print("✅ Features engineered successfully")
else:
    print("❌ Feature engineering failed")
    success = False

# Step 3: Model Training
if success and run_script('train_models.py', '3. Training ML models'):
    print("✅ Models trained successfully")
else:
    print("❌ Model training failed")
    success = False

# Final Summary
print("\n" + "=" * 80)
if success:
    print("✅ PIPELINE COMPLETE!")
    print("=" * 80)
    print("\n🎉 All steps completed successfully!")
    print("\n📊 What's been created:")
    print("   • Feature-engineered dataset")
    print("   • 3 trained ML models (LR, RF, XGBoost)")
    print("   • Best model saved to app/model.pkl")
    print("\n🚀 Next steps:")
    print("   1. Restart Streamlit app: cd app && python -m streamlit run app.py")
    print("   2. Test predictions in the web interface")
    print("   3. Review model performance in terminal output")
    print("\n💻 Streamlit app will use the trained model automatically!")
else:
    print("❌ PIPELINE INCOMPLETE")
    print("=" * 80)
    print("\n⚠️  Some steps failed. Please check the error messages above.")
    print("\nYou can run individual scripts manually:")
    print("   python scripts/process_features.py")
    print("   python scripts/train_models.py")

print("\n" + "=" * 80)
