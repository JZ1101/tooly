"""
Simple test for AI-powered UserAgent
"""

import asyncio
import os
from dotenv import load_dotenv
from agent import UserAgent

# Load environment variables from .env file
load_dotenv()

async def test_agent():
    """Test the AI agent with sample queries"""
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Set ANTHROPIC_API_KEY to test with AI")
        return
    
    agent = UserAgent(api_key)
    
    test_queries = [
        "What's my ETH balance for 0x123...?",
        "Show me recent transactions",
        "How much gas for a transfer?", 
        "Swap 100 ETH for USDC",
        "Hello, how are you?",
        "Check my balance"  # Missing address - should ask follow-up
    ]
    
    print("🤖 Testing AI UserAgent...\n")
    
    for query in test_queries:
        print(f"❓ User: {query}")
        try:
            response = await agent.process_query(query)
            print(f"🤖 Agent: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_agent())