#!/bin/bash

# Azure App Service startup script for Streamlit application
echo "Starting Incident Insight Hub on Azure App Service..."

# Install dependencies
echo "Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Set environment variables for Streamlit
export STREAMLIT_SERVER_PORT=${PORT:-8000}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Create necessary directories
mkdir -p logs

# Start the Streamlit application
echo "Starting Streamlit application on port $STREAMLIT_SERVER_PORT..."
python -m streamlit run app.py \
    --server.port $STREAMLIT_SERVER_PORT \
    --server.address $STREAMLIT_SERVER_ADDRESS \
    --server.headless $STREAMLIT_SERVER_HEADLESS \
    --browser.gatherUsageStats $STREAMLIT_BROWSER_GATHER_USAGE_STATS 