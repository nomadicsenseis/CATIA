#!/usr/bin/env python3
"""
Test script to verify PBIDataCollector logger fix
"""

import sys
import os
import logging

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_pbi_collector_logger():
    """Test that PBIDataCollector now has a logger attribute"""
    
    print("🧪 TESTING PBI COLLECTOR LOGGER FIX")
    print("=" * 60)
    
    try:
        # Import PBIDataCollector
        from pbi_collector import PBIDataCollector
        
        print("📋 Step 1: Initialize PBIDataCollector")
        collector = PBIDataCollector()
        
        print("✅ PBIDataCollector initialized successfully!")
        
        # Test that logger attribute exists
        print("\n📋 Step 2: Test logger attribute")
        if hasattr(collector, 'logger'):
            print("✅ Logger attribute found!")
            print(f"📊 Logger type: {type(collector.logger)}")
            print(f"📊 Logger name: {collector.logger.name}")
            
            # Test that we can use the logger
            print("\n📋 Step 3: Test logger functionality")
            collector.logger.info("🔧 Testing logger functionality from PBIDataCollector")
            print("✅ Logger works correctly!")
            
            return True
            
        else:
            print("❌ Logger attribute not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing PBIDataCollector: {e}")
        import traceback
        traceback.print_exc()
        return False


def simulate_routes_filtering():
    """Simulate the routes filtering that was causing the error"""
    
    print("\n\n🔍 SIMULATING ROUTES FILTERING")
    print("=" * 60)
    
    try:
        from pbi_collector import PBIDataCollector
        
        print("📋 Step 1: Initialize collector for filtering test")
        collector = PBIDataCollector()
        
        # Test the specific operation that was failing
        print("\n📋 Step 2: Test logger in routes filtering context")
        
        # This should work now - test the logger operations that were failing
        collector.logger.info("🗺️ Filtering NCS using routes dictionary for haul: LH")
        collector.logger.warning("❌ Routes dictionary is empty, falling back to original data")
        collector.logger.info("📊 Found 25 routes for LH")
        
        print("✅ Routes filtering logger operations work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error in routes filtering simulation: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    
    print("🚀 PBI COLLECTOR LOGGER FIX TESTING")
    print("=" * 80)
    
    # Test 1: Basic logger functionality
    test1_success = test_pbi_collector_logger()
    
    # Test 2: Routes filtering simulation
    test2_success = simulate_routes_filtering()
    
    print("\n\n📊 TEST RESULTS")
    print("=" * 60)
    
    if test1_success and test2_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ PBIDataCollector logger fix is working correctly")
        print("✅ The 'PBIDataCollector object has no attribute logger' error should be resolved")
        print()
        print("💡 What was the problem:")
        print("• PBIDataCollector class was missing a logger attribute")
        print("• Routes filtering code was trying to use self.logger")
        print("• This caused: 'PBIDataCollector' object has no attribute 'logger'")
        print()
        print("🔧 What was fixed:")
        print("• Added import logging to pbi_collector.py")
        print("• Added self.logger = logging.getLogger(__name__) in __init__")
        print("• Now all logger operations in PBIDataCollector work correctly")
        
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Need to investigate further")
        
        if not test1_success:
            print("• Basic logger test failed")
        if not test2_success:
            print("• Routes filtering simulation failed")


if __name__ == "__main__":
    main()
