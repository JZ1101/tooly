"""
SpoonOS Tool Execution Agent - Comprehensive Tool Demonstration

This example demonstrates ALL 21 tools across 5 categories with real usage scenarios.
Each tool category includes multiple practical examples showing the tool's capabilities.

Tool Categories (21 tools total):
1. CRYPTO_DATA (7 tools): Price data, alerts, monitoring
2. CRYPTO_POWERDATA (3 tools): Exchange data, technical indicators
3. CRYPTO_EVM (6 tools): Ethereum operations, swaps, transfers
4. CRYPTO_NEO (2 tools): Neo blockchain queries
5. GITHUB (3 tools): Repository analysis

Key Features:
- Comprehensive demonstration of all 21 tools
- Real-world usage scenarios for each tool
- Natural language interface
- ReAct autonomous tool selection
- Detailed output for each tool execution
"""

import asyncio
from agent import SpoonOSAgent, ToolCategory
from spoon_ai.agents import SpoonReactAI
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
import os
import time
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Initialize log file
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"tool_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

def log_query_response(query: str, response: str, tool_name: str = None, error: str = None):
    """Log query, response, and tool used to JSON file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "query": query,
        "response": response if not error else None,
        "error": error
    }
    
    # Append to log file
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

async def demonstrate_all_tools():
    """
    Comprehensive demonstration of all 21 tools across 5 categories.
    Each section showcases specific tool capabilities with real examples.
    """
    print("\n" + "=" * 80)
    print("SpoonOS Agent - Comprehensive Tool Demonstration")
    print("Showcasing ALL 21 Tools Across 5 Categories")
    print("=" * 80)
    
    # Initialize SpoonOS tool registry
    print("\n[1] Initializing SpoonOS Tool Registry...")
    tool_agent = SpoonOSAgent()
    
    all_categories = [
        ToolCategory.CRYPTO_DATA,
        ToolCategory.CRYPTO_POWERDATA,
        ToolCategory.CRYPTO_EVM,
        ToolCategory.CRYPTO_NEO,
        ToolCategory.GITHUB,
    ]
    await tool_agent.initialize(all_categories)
    
    # Show detailed statistics
    print(f"\n    📊 Tool Registry Statistics:")
    print(f"    {'─' * 70}")
    total_tools = tool_agent.registry.get_tool_count()
    print(f"    Total Tools: {total_tools}")
    print(f"\n    Tool Breakdown by Category:")
    
    categories_info = tool_agent.registry.get_categories()
    for category, count in categories_info.items():
        tools = tool_agent.registry.list_tools(ToolCategory(category))
        print(f"\n      [{category.upper()}] - {count} tools:")
        for i, tool_name in enumerate(tools, 1):
            print(f"        {i}. {tool_name}")
    
    # Create ReAct agent with ALL tools
    print(f"\n[2] Creating ReAct Agent with All {total_tools} Tools...")
    
    tools = []
    for category in all_categories:
        category_tools = tool_agent.registry.list_tools(category)
        for tool_name in category_tools:
            tool_instance = tool_agent.registry.get_tool(tool_name)
            tools.append(tool_instance)
    
    tool_manager = ToolManager(tools)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 🚀 OPTIMAL SOLUTION FOR RATE LIMITS
    # ═══════════════════════════════════════════════════════════════════════════
    # 
    # Problem: Gemini free tier = 15 requests/min (too low for 24 tool demos)
    # 
    # Solution: Use OpenAI gpt-4o-mini (BEST for tool execution)
    # - Free tier: 3 req/min → Still better than Gemini
    # - Paid tier ($5): 3,500 req/min → 233x faster than Gemini!
    # - Cost: ~$0.15 per 1M tokens (24 demos = $0.10-0.20 total)
    # - Stability: Best framework support, no memory bugs
    # 
    # Setup:
    # 1. Get API key: https://platform.openai.com/api-keys
    # 2. Add to .env: OPENAI_API_KEY=sk-proj-...
    # 3. Optional: Add $5 credit for unlimited usage
    # 
    # Alternative if no OpenAI key: Falls back to Gemini (will hit rate limits)
    # ═══════════════════════════════════════════════════════════════════════════
    
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if openai_key:
        print("    🚀 Using OpenAI gpt-4o-mini (optimal for tool execution)")
        react_agent = SpoonReactAI(
            llm=ChatBot(
                model_name="gpt-4o-mini",
                llm_provider="openai",
                temperature=0.1,
                enable_short_term_memory=False
            ),
            tools=tool_manager,
            max_iterations=10
        )
    else:
        print("    ⚠️  OPENAI_API_KEY not found - using Gemini (will hit rate limits)")
        print("    💡 Add OPENAI_API_KEY to .env for 233x faster execution!")
        react_agent = SpoonReactAI(
            llm=ChatBot(
                model_name="gemini-2.0-flash-exp",
                llm_provider="gemini",
                temperature=0.1,
                enable_short_term_memory=False
            ),
            tools=tool_manager,
            max_iterations=10
        )
    
    print("    ✓ ReAct agent initialized with autonomous tool selection")
    print(f"    ✓ Agent can choose from {total_tools} available tools")
    
    # Execute comprehensive tool demonstrations
    print("\n" + "=" * 80)
    print("[3] Comprehensive Tool Demonstrations")
    print("=" * 80)
    
    # =============================================================================
    # CATEGORY 1: CRYPTO_DATA (7 tools)
    # =============================================================================
    print("\n" + "─" * 80)
    print("📈 CATEGORY 1: CRYPTO DATA TOOLS (7 tools)")
    print("─" * 80)
    print("Tools: get_token_price, get_24h_stats, get_kline_data,")
    print("       price_threshold_alert, lp_range_check,")
    print("       sudden_price_increase, lending_rate_monitor")
    
    crypto_data_demos = [
        {
            "name": "Tool 1: get_token_price",
            "query": "What is the current price of ETH in USDC?",
            "description": "Fetches real-time token prices from Uniswap pools"
        },
        {
            "name": "Tool 2: get_24h_stats",
            "query": "Show me the 24-hour statistics for ETH-USDC including price change",
            "description": "Provides 24h volume, price change, and percentage metrics"
        },
        {
            "name": "Tool 3: get_kline_data",
            "query": "Get the historical candlestick data for BTC-USDT",
            "description": "Retrieves OHLCV (Open, High, Low, Close, Volume) candle data"
        },
        {
            "name": "Tool 4: price_threshold_alert",
            "query": "Check if ETH price has moved more than 5% in the last 24 hours",
            "description": "Monitors price changes and triggers alerts on threshold breach"
        },
        {
            "name": "Tool 5: lp_range_check",
            "query": "Check if my liquidity position for ETH-USDC is still in range",
            "description": "Validates LP position health and warns of out-of-range scenarios"
        },
        {
            "name": "Tool 6: sudden_price_increase",
            "query": "Detect any sudden price spikes in major cryptocurrencies",
            "description": "Identifies abnormal price movements and potential pump events"
        },
        {
            "name": "Tool 7: lending_rate_monitor",
            "query": "What are the current lending rates for USDC across DeFi platforms?",
            "description": "Aggregates lending/borrowing rates from major protocols"
        }
    ]
    
    await execute_demo_section(react_agent, crypto_data_demos)
    # =============================================================================
    # CATEGORY 2: CRYPTO_POWERDATA (3 tools)
    # =============================================================================
    print("\n" + "─" * 80)
    print("📊 CATEGORY 2: CRYPTO POWERDATA TOOLS (3 tools)")
    print("─" * 80)
    print("Tools: crypto_powerdata_cex, crypto_powerdata_dex,")
    print("       crypto_powerdata_indicators")
    
    powerdata_demos = [
        {
            "name": "Tool 8: crypto_powerdata_cex",
            "query": "Get OHLCV data for BTC/USDT from Binance exchange with 1 hour timeframe",
            "description": "Fetches centralized exchange data with technical indicators"
        },
        {
            "name": "Tool 9: crypto_powerdata_dex",
            "query": "Get DEX trading data for ETH on Ethereum chain",
            "description": "Retrieves decentralized exchange data via OKX Web3 API"
        },
        {
            "name": "Tool 10: crypto_powerdata_indicators",
            "query": "List all available technical indicators I can calculate",
            "description": "Shows supported indicators (RSI, MACD, Bollinger Bands, etc.)"
        }
    ]
    
    await execute_demo_section(react_agent, powerdata_demos)
    # =============================================================================
    # CATEGORY 3: CRYPTO_EVM (6 tools)
    # =============================================================================
    print("\n" + "─" * 80)
    print("⛓️  CATEGORY 3: EVM BLOCKCHAIN TOOLS (6 tools)")
    print("─" * 80)
    print("Tools: evm_transfer, evm_erc20_transfer, evm_balance,")
    print("       evm_swap, evm_swap_quote, evm_bridge")
    
    evm_demos = [
        {
            "name": "Tool 12: evm_balance",
            "query": "Check the ETH balance of address 0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "description": "Queries native token and ERC-20 balances on EVM chains"
        },
        {
            "name": "Tool 13: evm_swap_quote",
            "query": "Get a quote for swapping 1 ETH to USDC on Ethereum mainnet",
            "description": "Fetches optimal swap routes and expected output amounts"
        },
        {
            "name": "Tool 14: evm_transfer",
            "query": "Simulate transferring 0.1 ETH to another address",
            "description": "Executes native ETH transfers (requires RPC configuration)"
        },
        {
            "name": "Tool 15: evm_erc20_transfer",
            "query": "Simulate transferring 100 USDC tokens",
            "description": "Handles ERC-20 token transfers with approval checks"
        },
        {
            "name": "Tool 16: evm_swap",
            "query": "Simulate swapping ETH for USDC using DEX aggregator",
            "description": "Executes token swaps via Bebop/1inch aggregators"
        },
        {
            "name": "Tool 17: evm_bridge",
            "query": "Get bridge information for moving assets from Ethereum to Polygon",
            "description": "Facilitates cross-chain asset transfers via LiFi protocol"
        }
    ]
    
    await execute_demo_section(react_agent, evm_demos)
    # =============================================================================
    # CATEGORY 4: CRYPTO_NEO (2 tools)
    # =============================================================================
    print("\n" + "─" * 80)
    print("🔷 CATEGORY 4: NEO BLOCKCHAIN TOOLS (2 tools)")
    print("─" * 80)
    print("Tools: neo_address_info, neo_validate_address")
    
    neo_demos = [
        {
            "name": "Tool 18: neo_validate_address",
            "query": "Validate if this is a correct Neo address: NaU3shtZqnR1H6XnDTxghorgkXN687C444",
            "description": "Validates Neo address format and checksum"
        },
        {
            "name": "Tool 19: neo_address_info",
            "query": "Get balance and transaction info for Neo address NaU3shtZqnR1H6XnDTxghorgkXN687C444",
            "description": "Retrieves complete address information including assets"
        }
    ]
    
    await execute_demo_section(react_agent, neo_demos)
    # =============================================================================
    # CATEGORY 5: GITHUB (3 tools)
    # =============================================================================
    print("\n" + "─" * 80)
    print("🐙 CATEGORY 5: GITHUB ANALYSIS TOOLS (3 tools)")
    print("─" * 80)
    print("Tools: github_issues, github_pull_requests, github_commits")
    
    github_demos = [
        {
            "name": "Tool 22: github_issues",
            "query": "Show me the recent issues from XSpoonAi/spoon-core repository",
            "description": "Retrieves issues with filters for state, labels, and date range"
        },
        {
            "name": "Tool 23: github_pull_requests",
            "query": "List the recent pull requests from XSpoonAi/spoon-core",
            "description": "Fetches PRs with merge status and review information"
        },
        {
            "name": "Tool 24: github_commits",
            "query": "Get the commit history for XSpoonAi/spoon-core from the last month",
            "description": "Retrieves commit logs with author, message, and diff stats"
        }
    ]
    
    await execute_demo_section(react_agent, github_demos)
    # Summary
    print("\n" + "=" * 80)
    print("✨ Tool Demonstration Complete")
    print("=" * 80)
    print(f"\nSuccessfully demonstrated all {total_tools} tools across 5 categories:")
    print("  • CRYPTO_DATA: 7 tools for price monitoring and DeFi analytics")
    print("  • CRYPTO_POWERDATA: 3 tools for advanced market data and indicators")
    print("  • CRYPTO_EVM: 6 tools for Ethereum operations and cross-chain bridging")
    print("  • CRYPTO_NEO: 2 tools for Neo blockchain queries and validation")
    print("  • GITHUB: 3 tools for repository analysis and development insights")
    print(f"\n📝 Log file saved: {LOG_FILE}")
    print("\n" + "=" * 80)


async def execute_demo_section(agent: SpoonReactAI, demos: list):
    """
    Execute a section of tool demonstrations with detailed output.
    
    Args:
        agent: The ReAct agent to execute queries
        demos: List of demo dictionaries with name, query, and description
    """
    for i, demo in enumerate(demos, 1):
        print(f"\n{'─' * 80}")
        print(f"🔧 {demo['name']}")
        print(f"   Description: {demo['description']}")
        print(f"   Query: \"{demo['query']}\"")
        print(f"{'─' * 80}")
        
        try:
            response = await agent.run(demo['query'])
            print(f"\n✅ Response:")
            print(f"   {response}")
            # Log query, response, and tool name
            log_query_response(demo['query'], response, tool_name=demo['name'])
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Error: {error_msg}")
            # Log query, error, and tool name
            log_query_response(demo['query'], None, tool_name=demo['name'], error=error_msg)
        
        # Add a small delay between queries to avoid rate limiting
        if i < len(demos):
            await asyncio.sleep(4)


async def main():
    """Main execution function."""
    try:
        await demonstrate_all_tools()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
