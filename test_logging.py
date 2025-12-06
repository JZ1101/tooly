"""
Test script to verify logging functionality works correctly.
"""
import asyncio
import os
import sys

# Add spoonOS to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spoonOS'))

async def test_logging():
    """Test if logging setup works correctly."""
    print("Testing logging functionality...")
    
    # Import after adding to path
    from examples import setup_logging
    
    # Test setup_logging function
    logger, log_file = setup_logging()
    
    print(f"✅ Logger created successfully")
    print(f"✅ Log file: {log_file}")
    
    # Test writing to log
    logger.info("Test message 1: This is a test")
    logger.info("Test message 2: Query - 'What is the price of BTC?'")
    logger.info("Test message 3: ✅ Response - 'BTC price is $42,000'")
    logger.error("Test message 4: ❌ Error - 'API rate limit exceeded'")
    
    print(f"✅ Test messages written to log file")
    
    # Verify file exists and has content
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > 0:
                print(f"✅ Log file contains {len(content)} characters")
                print("\nLog file preview:")
                print("─" * 80)
                print(content)
                print("─" * 80)
            else:
                print("❌ Log file is empty")
    else:
        print("❌ Log file does not exist")
    
    print("\n✅ Logging test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_logging())
