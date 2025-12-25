@echo off
echo ================================================================================
echo GESTATIONAL DIABETES MEAL RISK PREDICTOR - QUICK START
echo ================================================================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo.

echo Step 2: Installing required packages...
echo This may take a few minutes on first run...
python -m pip install --quiet pandas numpy scikit-learn xgboost matplotlib seaborn streamlit
echo ✓ Packages installed
echo.

echo Step 3: Running complete ML pipeline...
echo This will:
echo   - Generate sample data
echo   - Engineer features
echo   - Train 3 ML models
echo   - Save best model for Streamlit
echo.
python scripts\run_complete_pipeline.py
echo.

if errorlevel 1 (
    echo.
    echo ⚠️ Pipeline encountered some issues. Check the output above.
    echo.
) else (
    echo.
    echo ================================================================================
    echo ✅ SUCCESS! Your project is ready!
    echo ================================================================================
    echo.
    echo 🎯 Next step: Launch the Streamlit app
    echo.
    echo Open a NEW terminal window and run:
    echo   cd app
    echo   python -m streamlit run app.py
    echo.
    echo Then open your browser to: http://localhost:8501
    echo.
)

pause
