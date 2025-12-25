@echo off
cd /d "%~dp0"

echo ==================================================
echo Running Feature Engineering + Model Training
echo ==================================================
echo.

python quick_features.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR in feature engineering
    pause
    exit /b 1
)

python quick_train.py  
if %ERRORLEVEL% NEQ 0 (
    echo ERROR in model training
    pause
    exit /b 1
)

echo.
echo ==================================================
echo SUCCESS! Pipeline complete
echo ==================================================
pause
