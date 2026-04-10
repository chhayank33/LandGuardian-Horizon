#!/usr/bin/env python3
"""
Simple test to debug application startup issues
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    
    try:
        from app import app
        print("  Flask app: OK")
        return True
    except Exception as e:
        print(f"  Flask app: ERROR - {e}")
        return False

def test_modules():
    """Test individual modules"""
    print("Testing modules...")
    
    modules = [
        'modules.bhulekh_integration',
        'modules.ocr_processor', 
        'modules.blockchain_service',
        'modules.dispute_predictor',
        'modules.ar_service',
        'modules.multi_state_search',
        'modules.zero_knowledge_proofs'
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  {module}: OK")
        except Exception as e:
            print(f"  {module}: ERROR - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Main test function"""
    print("HORIZON - Application Debug Test")
    print("=" * 40)
    
    # Test modules
    if not test_modules():
        print("\nModule imports failed - fixing issues...")
        return False
    
    # Test app
    if not test_imports():
        print("\nApp import failed - fixing issues...")
        return False
    
    print("\nAll tests passed!")
    return True

if __name__ == '__main__':
    main()
