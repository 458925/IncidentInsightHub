#!/usr/bin/env python3
"""
Azure App Service startup script for Incident Insight Hub
"""
import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main startup function for Azure App Service"""
    try:
        # Get the port from environment variable (set by Azure)
        port = os.environ.get('PORT', '8000')
        
        logger.info(f"Starting Incident Insight Hub on port {port}")
        
        # Set Streamlit configuration
        os.environ['STREAMLIT_SERVER_PORT'] = port
        os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Build the streamlit command
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', port,
            '--server.address', '0.0.0.0',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ]
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        
        # Start the Streamlit application
        subprocess.run(cmd, check=True)
        
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 