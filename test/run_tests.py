"""Test runner for marketdata_providers package"""

import sys
import os
import pytest
from pathlib import Path

def main():
    """Run all tests for the marketdata_providers package"""
    
    # Get the test directory path
    test_dir = Path(__file__).parent
    
    # Add the src directory to Python path so we can import the package
    src_dir = test_dir.parent / "src"
    sys.path.insert(0, str(src_dir))
    
    # Test configuration
    pytest_args = [
        str(test_dir),  # Test directory
        "-v",           # Verbose output
        "--tb=short",   # Short traceback format
        "--color=yes",  # Colored output
        "-x",           # Stop on first failure
    ]
    
    print("=" * 60)
    print("RUNNING MARKETDATA PROVIDERS PACKAGE TESTS")
    print("=" * 60)
    print(f"Test directory: {test_dir}")
    print(f"Source directory: {src_dir}")
    print()
    
    # Check if package can be imported
    try:
        import marketdata_providers
        print(f"✅ Successfully imported marketdata_providers")
        print(f"   Package location: {marketdata_providers.__file__}")
    except ImportError as e:
        print(f"❌ Failed to import marketdata_providers: {e}")
        return 1
    
    print()
    print("Running tests...")
    print("-" * 40)
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    print()
    print("-" * 40)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed (exit code: {exit_code})")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
