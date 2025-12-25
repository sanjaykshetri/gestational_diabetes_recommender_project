@echo off
echo ========================================
echo Running Feature Engineering Pipeline
echo ========================================
echo.

cd /d "%~dp0"
echo Current directory: %CD%
echo.

echo Running feature engineering...
C:\Users\sanja\AppData\Local\Microsoft\WindowsApps\python3.13.exe quick_features.py
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Feature engineering completed
) else (
    echo ERROR: Feature engineering failed with code %ERRORLEVEL%
)
echo.

echo Checking output file...
if exist "data\processed\meals_with_features.csv" (
    echo SUCCESS: meals_with_features.csv created
    for %%A in ("data\processed\meals_with_features.csv") do echo File size: %%~zA bytes
) else (
    echo ERROR: meals_with_features.csv not found
)
echo.

echo ========================================
echo Press any key to close...
pause >nul
