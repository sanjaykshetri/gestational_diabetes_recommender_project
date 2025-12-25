Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Feature Engineering Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$pythonPath = "C:\Users\sanja\AppData\Local\Microsoft\WindowsApps\python3.13.exe"
$scriptPath = "quick_features.py"

Write-Host "Python: $pythonPath" -ForegroundColor Yellow
Write-Host "Script: $scriptPath" -ForegroundColor Yellow
Write-Host ""

Write-Host "Running feature engineering..." -ForegroundColor Green
& $pythonPath $scriptPath 2>&1 | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "Checking results..." -ForegroundColor Green

$outputFile = "data\processed\meals_with_features.csv"
if (Test-Path $outputFile) {
    $fileInfo = Get-Item $outputFile
    Write-Host "SUCCESS: Output file created!" -ForegroundColor Green
    Write-Host "  File: $outputFile" -ForegroundColor White
    Write-Host "  Size: $($fileInfo.Length) bytes" -ForegroundColor White
    Write-Host "  Modified: $($fileInfo.LastWriteTime)" -ForegroundColor White
} else {
    Write-Host "ERROR: Output file not found" -ForegroundColor Red
    Write-Host "  Expected: $outputFile" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
