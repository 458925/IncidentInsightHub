@echo off

:: Azure App Service Deployment Script for Incident Insight Hub

echo Starting deployment for Incident Insight Hub...

:: Verify Python installation
python --version
if %errorlevel% NEQ 0 (
    echo Python is not installed or not in PATH
    exit /b 1
)

:: Install dependencies
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Create necessary directories
if not exist "logs" mkdir logs

:: Deployment completed
echo Deployment completed successfully!
echo Application will start using startup.py

:: End of deployment script 