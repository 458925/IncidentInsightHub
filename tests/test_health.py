"""
Health check tests for deployment validation
"""
import requests
import time
import sys
import os
from urllib.parse import urljoin


class HealthChecker:
    """Health check utility for validating deployment"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30
        self.retry_count = 5
        self.retry_delay = 10
    
    def wait_for_app_start(self):
        """Wait for the application to start and become responsive"""
        print(f"Waiting for application to start at {self.base_url}...")
        
        for attempt in range(self.retry_count):
            try:
                response = requests.get(self.base_url, timeout=self.timeout)
                if response.status_code == 200:
                    print(f"Application is responsive (attempt {attempt + 1})")
                    return True
                else:
                    print(f"Application returned status {response.status_code} (attempt {attempt + 1})")
            except requests.exceptions.RequestException as e:
                print(f"Connection failed: {e} (attempt {attempt + 1})")
            
            if attempt < self.retry_count - 1:
                print(f"Waiting {self.retry_delay} seconds before next attempt...")
                time.sleep(self.retry_delay)
        
        return False
    
    def check_health(self):
        """Perform comprehensive health checks"""
        print("Starting health checks...")
        
        # Basic connectivity check
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            print(f"✓ Basic connectivity: {response.status_code}")
            
            if response.status_code != 200:
                print(f"✗ Health check failed: HTTP {response.status_code}")
                return False
            
            # Check if it's a Streamlit app
            if "streamlit" in response.text.lower() or "incident insight hub" in response.text.lower():
                print("✓ Streamlit application detected")
            else:
                print("? Could not confirm Streamlit application")
            
            # Check response time
            if response.elapsed.total_seconds() < 10:
                print(f"✓ Response time: {response.elapsed.total_seconds():.2f}s")
            else:
                print(f"⚠ Slow response time: {response.elapsed.total_seconds():.2f}s")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Health check failed: {e}")
            return False
    
    def validate_dependencies(self):
        """Validate that required dependencies are available"""
        print("Validating dependencies...")
        
        try:
            import streamlit
            print(f"✓ Streamlit: {streamlit.__version__}")
        except ImportError:
            print("✗ Streamlit not found")
            return False
        
        try:
            import pandas
            print(f"✓ Pandas: {pandas.__version__}")
        except ImportError:
            print("✗ Pandas not found")
            return False
        
        try:
            import plotly
            print(f"✓ Plotly: {plotly.__version__}")
        except ImportError:
            print("✗ Plotly not found")
            return False
        
        return True
    
    def run_all_checks(self):
        """Run all health checks"""
        print("=" * 50)
        print("INCIDENT INSIGHT HUB - HEALTH CHECK")
        print("=" * 50)
        
        # Dependency check
        deps_ok = self.validate_dependencies()
        
        # Wait for app to start
        app_started = self.wait_for_app_start()
        
        # Health check
        health_ok = False
        if app_started:
            health_ok = self.check_health()
        
        # Summary
        print("\n" + "=" * 50)
        print("HEALTH CHECK SUMMARY")
        print("=" * 50)
        print(f"Dependencies: {'✓ PASS' if deps_ok else '✗ FAIL'}")
        print(f"Application Start: {'✓ PASS' if app_started else '✗ FAIL'}")
        print(f"Health Check: {'✓ PASS' if health_ok else '✗ FAIL'}")
        
        overall_status = deps_ok and app_started and health_ok
        print(f"Overall Status: {'✓ PASS' if overall_status else '✗ FAIL'}")
        
        return overall_status


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Health check for Incident Insight Hub")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL of the application")
    parser.add_argument("--timeout", type=int, default=30,
                       help="Request timeout in seconds")
    parser.add_argument("--retries", type=int, default=5,
                       help="Number of retry attempts")
    
    args = parser.parse_args()
    
    checker = HealthChecker(base_url=args.url)
    checker.timeout = args.timeout
    checker.retry_count = args.retries
    
    success = checker.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 