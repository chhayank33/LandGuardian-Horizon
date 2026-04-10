#!/usr/bin/env python3
"""
HORIZON Land Guardian Portal - Startup Script
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'flask', 'requests', 'bs4', 'pytesseract',
        'PIL', 'web3', 'cv2', 'numpy', 'pandas',
        'sklearn', 'dotenv', 'cryptography'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  {package}: OK")
        except ImportError:
            print(f"  {package}: MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    print("Checking Tesseract OCR...")
    
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("  Tesseract: OK")
        return True
    except Exception as e:
        print(f"  Tesseract: ERROR - {e}")
        print("Please install Tesseract OCR:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  macOS: brew install tesseract")
        print("  Linux: sudo apt-get install tesseract-ocr")
        return False

def setup_directories():
    """Create necessary directories"""
    print("Setting up directories...")
    
    directories = [
        'uploads', 'models', 'static', 'logs', 'cache', 'temp'
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        print(f"  {directory}: OK")
    
    # Create subdirectories
    subdirs = ['static/uploads', 'static/models']
    for subdir in subdirs:
        dir_path = project_root / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  {subdir}: OK")

def check_environment():
    """Check environment variables"""
    print("Checking environment...")
    
    env_file = project_root / '.env'
    if not env_file.exists():
        print("  .env file: MISSING")
        print("  Creating default .env file...")
        
        default_env = """# Flask Configuration
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# Polygon Testnet Configuration
POLYGON_TESTNET_RPC_URL=https://rpc-mumbai.maticvigil.com
POLYGON_TESTNET_PRIVATE_KEY=
CONTRACT_ADDRESS=

# OCR Configuration
TESSERACT_CMD_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe

# Redis Configuration
REDIS_URL=redis://localhost:6379

# API Keys
GOOGLE_MAPS_API_KEY=
AR_JS_API_KEY=
"""
        
        with open(env_file, 'w') as f:
            f.write(default_env)
        
        print("  .env file: CREATED (please update with your keys)")
    else:
        print("  .env file: OK")

def start_application():
    """Start the Flask application"""
    print("\nStarting HORIZON Land Guardian Portal...")
    print("=" * 50)
    
    try:
        from app import app
        print("Application loaded successfully!")
        print("\nAccess the portal at: http://localhost:5000")
        print("\nFeatures available:")
        print("  - Multi-state land search")
        print("  - OCR deed processing")
        print("  - AR geo-overlay verification")
        print("  - Blockchain query logging")
        print("  - Dispute prediction")
        print("  - Zero-knowledge proofs")
        print("\nPress Ctrl+C to stop the server")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("HORIZON Land Guardian Portal - Startup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Tesseract
    if not check_tesseract():
        print("Warning: Tesseract OCR not found - OCR features will be limited")
    
    # Setup directories
    setup_directories()
    
    # Check environment
    check_environment()
    
    # Start application
    start_application()

if __name__ == '__main__':
    main()
