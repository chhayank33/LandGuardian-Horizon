#!/usr/bin/env python3
"""
Test API endpoints to verify application is working
"""

import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing HORIZON API Endpoints")
    print("=" * 40)
    
    # Test main page
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("  Main page: OK")
        else:
            print(f"  Main page: ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Main page: ERROR - {e}")
    
    # Test supported states
    try:
        response = requests.get(f"{base_url}/api/search/supported-states", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  Supported states: OK ({len(data.get('states', []))} states)")
        else:
            print(f"  Supported states: ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Supported states: ERROR - {e}")
    
    # Test land search
    try:
        search_data = {
            "state": "bihar",
            "district": "patna",
            "village": "bela",
            "khasra_no": "123"
        }
        response = requests.post(f"{base_url}/api/search/land", 
                               json=search_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  Land search: OK (found {data.get('data', {}).get('total_records', 0)} records)")
        else:
            print(f"  Land search: ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Land search: ERROR - {e}")
    
    # Test smart alerts
    try:
        response = requests.get(f"{base_url}/api/alerts/smart", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  Smart alerts: OK ({len(data.get('alerts', []))} alerts)")
        else:
            print(f"  Smart alerts: ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Smart alerts: ERROR - {e}")
    
    print("\nAPI testing complete!")

if __name__ == '__main__':
    # Wait a moment for server to fully start
    time.sleep(2)
    test_api_endpoints()
