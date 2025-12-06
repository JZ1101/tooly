"""
Real SpoonOS Integration Layer - Production Implementation
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Add spoonOS directory to path for imports
spoon_os_path = Path(__file__).parent.parent / "spoonOS"
sys.path.insert(0, str(spoon_os_path))

try:
    from agent import SpoonOSAgent, ToolCategory, ToolExecutionResult
    SPOONOS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ SpoonOS import failed: {e}")
    SPOONOS_AVAILABLE = False

@dataclass
class Intent:
    """User intent with extracted parameters"""
    action: str
    parameters: Dict[str, Any]
    confidence: float
    reasoning: str

@dataclass
class SpoonOSRequest:
    """Request format for spoonOS agent"""
    action: str
    parameters: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@dataclass 
class SpoonOSResponse:
    """Simple response from spoonOS"""
    success: bool
    output: str
    follow_up_questions: Optional[list] = None

class SpoonOSIntegration:
    """
    Production SpoonOS Integration Layer
    
    Connects UserAgent intent classification with real SpoonOS tool execution.
    Supports 21+ Web3 tools across 5 categories.
    """
    
    def __init__(self, spoon_os_endpoint: str = "http://localhost:8000"):
        self.endpoint = spoon_os_endpoint
        self.agent = None
        self.is_connected = False
        self._tool_mappings = self._init_tool_mappings()
        
    async def initialize(self):
        """Initialize the SpoonOS agent with all tool categories"""
        if not SPOONOS_AVAILABLE:
            print("⚠️ SpoonOS not available, using fallback responses")
            return False
            
        try:
            self.agent = SpoonOSAgent()
            
            # Initialize all available tool categories
            categories = [
                ToolCategory.CRYPTO_DATA,
                ToolCategory.CRYPTO_EVM, 
                ToolCategory.CRYPTO_NEO,
                ToolCategory.GITHUB,
                ToolCategory.CRYPTO_POWERDATA
            ]
            
            await self.agent.initialize(categories)
            self.is_connected = True
            
            # Get actual tool count for reporting
            tool_count = self.agent.registry.get_tool_count()
            print(f"✅ SpoonOS agent initialized with {tool_count} tools")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize SpoonOS agent: {e}")
            self.is_connected = False
            return False
    
    def _init_tool_mappings(self) -> Dict[str, str]:
        """Map UserAgent intents to SpoonOS tool names"""
        return {
            # Balance and transaction queries
            "check_balance": "evm_balance",
            "get_balance": "evm_balance",
            "get_transactions": "get_24h_stats",  # Use stats for transaction-like data
            
            # Price and market data
            "get_token_price": "get_token_price",
            "get_price": "get_token_price",
            "price_info": "get_token_price",
            
            # OHLCV/Kline data - route to appropriate tool based on exchange
            "get_ohlcv": "crypto_powerdata_cex",  # CEX data for exchange queries
            "get_kline": "get_kline_data",        # DEX data for on-chain queries
            "get_candles": "crypto_powerdata_cex",
            "get_kline_data": "get_kline_data",
            
            # Gas estimation
            "estimate_gas": "evm_swap_quote",  # Quote includes gas estimates
            "gas_estimate": "evm_swap_quote",
            
            # Token swapping
            "swap_tokens": "evm_swap",
            "token_swap": "evm_swap",
            "execute_swap": "evm_swap",
            
            # Contract interaction
            "execute_contract": "evm_transfer",  # Generic contract execution
            "contract_call": "evm_transfer",
            
            # NFT information
            "get_nft_info": "get_24h_stats",  # Use stats as proxy for NFT data
            "nft_info": "get_24h_stats",
            
            # General queries fall back to price data
            "general_info": "get_token_price",
            "market_data": "get_kline_data"
        }
    
    async def send_intent(self, intent: Intent) -> SpoonOSResponse:
        """
        Send structured intent to SpoonOS agent for execution
        
        Args:
            intent: Classified user intent with parameters
            
        Returns:
            SpoonOSResponse with results from SpoonOS tools
        """
        if not self.is_connected or not self.agent:
            # Fallback to mock responses if SpoonOS unavailable
            return await self._fallback_response(intent)
        
        try:
            # Map intent action to SpoonOS tool
            tool_name = self._map_intent_to_tool(intent.action)
            
            # Prepare parameters for SpoonOS tool
            tool_params = self._prepare_tool_parameters(intent, tool_name)
            
            # Execute tool via SpoonOS agent
            result = await self.agent.execute_tool(
                tool_name=tool_name,
                parameters=tool_params,
                timeout=30.0
            )
            
            return self._format_spoonos_result(result, intent)
            
        except Exception as e:
            print(f"❌ SpoonOS execution error: {e}")
            return SpoonOSResponse(
                success=False,
                output=f"Tool execution failed: {str(e)}",
                follow_up_questions=["Would you like me to try a different approach?"]
            )
    
    def _map_intent_to_tool(self, action: str) -> str:
        """Map user intent to actual SpoonOS tool name"""
        tool_name = self._tool_mappings.get(action)
        if not tool_name:
            # Improved fallback logic based on action type
            if 'balance' in action.lower():
                tool_name = "evm_balance"
            elif 'price' in action.lower():
                tool_name = "get_token_price"
            else:
                tool_name = "get_token_price"  # Default fallback
        print(f"🔧 Mapping intent '{action}' → tool '{tool_name}'")
        return tool_name
    
    def _prepare_tool_parameters(self, intent: Intent, tool_name: str) -> Dict[str, Any]:
        """Minimal parameter preparation - let SpoonOS tools handle their own defaults"""
        params = intent.parameters.copy()
        
        # Only handle basic parameter name mapping, let tools handle validation
        if tool_name == "evm_balance":
            # Only provide address if we have one
            if 'wallet_address' in params:
                params['address'] = params.pop('wallet_address')
            # Remove parameters that don't belong to this tool
            params.pop('token', None)
            params.pop('symbol', None)
            
        elif tool_name == "get_token_price":
            # Convert single token to proper trading pair format
            if 'token' in params and 'symbol' not in params:
                token = params.pop('token').upper()
                # Convert single token to trading pair
                if token in ['ETH', 'ETHEREUM']:
                    params['symbol'] = 'ETH-USDC'
                elif token in ['BTC', 'BITCOIN']:
                    params['symbol'] = 'BTC-USDT'
                else:
                    params['symbol'] = f'{token}-USDC'  # Default to USDC pair
            elif 'symbol' in params and '-' not in params['symbol']:
                # Fix symbol if it's just a single token
                token = params['symbol'].upper()
                if token in ['ETH', 'ETHEREUM']:
                    params['symbol'] = 'ETH-USDC'
                elif token in ['BTC', 'BITCOIN']:
                    params['symbol'] = 'BTC-USDT'
                else:
                    params['symbol'] = f'{token}-USDC'
            # Remove parameters that don't belong to this tool
            params.pop('address', None)
            params.pop('vs_currency', None)
            params.pop('wallet_address', None)
            
        elif tool_name == "get_kline_data":
            # Handle OHLCV/kline data parameters
            if 'symbol' in params:
                # Fix symbol format for kline data (remove exchange prefix if present)
                symbol = params['symbol']
                if '/' in symbol:
                    symbol = symbol.replace('/', '-')
                params['symbol'] = symbol
            
            # Map common parameter names
            if 'interval' in params:
                params['timeframe'] = params.pop('interval')
            elif 'timeframe' not in params:
                params['timeframe'] = '1h'  # Default timeframe
                
            # Remove parameters that don't belong
            params.pop('exchange', None)
            params.pop('address', None)
        
        # For other tools, pass parameters as-is and let them handle defaults
        return params
    
    def _format_spoonos_result(self, result: ToolExecutionResult, intent: Intent) -> SpoonOSResponse:
        """Format SpoonOS tool result for UserAgent consumption"""
        if result.success:
            # Format successful result based on intent type
            output = self._format_success_output(result, intent.action)
            
            return SpoonOSResponse(
                success=True,
                output=output,
                follow_up_questions=self._generate_follow_up_questions(intent.action, result)
            )
        else:
            return SpoonOSResponse(
                success=False,
                output=f"❌ {result.error or 'Unknown error occurred'}",
                follow_up_questions=["Would you like to try with different parameters?"]
            )
    
    def _format_success_output(self, result: ToolExecutionResult, action: str) -> str:
        """Format successful tool result into user-friendly output"""
        data = result.data
        
        if action in ["check_balance", "get_balance"]:
            if isinstance(data, dict) and 'balance' in str(data):
                return f"💰 Wallet Balance: {data}"
            return f"💰 Balance information: {data}"
        
        elif action in ["get_token_price", "price_info"]:
            if isinstance(data, dict):
                return f"💲 Token Price: {data}"
            return f"💲 Current price: {data}"
        
        elif action in ["swap_tokens", "token_swap"]:
            return f"🔄 Swap Result: {data}"
        
        elif action in ["estimate_gas", "gas_estimate"]:
            return f"⛽ Gas Estimate: {data}"
        
        elif action == "get_transactions":
            return f"📋 Transaction Data: {data}"
        
        else:
            return f"✅ {result.tool_name} Result: {data}"
    
    def _generate_follow_up_questions(self, action: str, result: ToolExecutionResult) -> Optional[list]:
        """Generate contextual follow-up questions"""
        if action in ["check_balance"]:
            return [
                "Would you like to see your transaction history?",
                "Do you want to check other token balances?"
            ]
        elif action in ["get_token_price"]:
            return [
                "Would you like to see the 24h price chart?",
                "Do you want to check other token prices?"
            ]
        elif action in ["estimate_gas"]:
            return [
                "Would you like me to execute this transaction?",
                "Do you want to see alternative routes?"
            ]
        return None
    
    async def _fallback_response(self, intent: Intent) -> SpoonOSResponse:
        """Fallback response when SpoonOS is unavailable"""
        action = intent.action
        params = intent.parameters
        
        fallback_responses = {
            "check_balance": f"💰 Mock Balance: 2.5 ETH (~$6,250) for address {params.get('address', 'your wallet')}",
            "get_token_price": f"💲 Mock Price: ETH/USDC = $2,500.00 (+2.5% 24h)",
            "estimate_gas": "⛽ Mock Gas: ~21,000 units ($3.50 USD)",
            "swap_tokens": f"🔄 Mock Swap: Would swap {params.get('amount', 1)} {params.get('from_token', 'ETH')} → {params.get('to_token', 'USDC')}",
            "get_transactions": "📋 Mock Transactions: Latest 5 transactions would be shown here",
            "execute_contract": "📄 Mock Contract: Contract interaction would be executed",
            "get_nft_info": "🖼️ Mock NFT: NFT collection info would be displayed"
        }
        
        output = fallback_responses.get(action, f"🤖 Mock response for: {action}")
        output += "\n\n⚠️ Note: This is a fallback response. Real SpoonOS integration unavailable."
        
        return SpoonOSResponse(
            success=True,
            output=output,
            follow_up_questions=["Would you like to try another Web3 operation?"]
        )
    
    def health_check(self) -> bool:
        """Check if SpoonOS agent is available and healthy"""
        if not self.is_connected or not self.agent:
            return False
        
        try:
            # Use SpoonOS built-in health check
            health_data = asyncio.run(self.agent.health_check())
            return health_data.get("initialized", False)
        except:
            return False
    
    def get_available_tools(self) -> list:
        """Get list of available tools from SpoonOS"""
        if not self.is_connected or not self.agent:
            return ["fallback_responses"]
        
        try:
            tools_by_category = self.agent.get_available_tools()
            all_tools = []
            for category, tools in tools_by_category.items():
                all_tools.extend(tools)
            return all_tools
        except:
            return ["error_getting_tools"]
    
    async def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool"""
        if not self.is_connected or not self.agent:
            return None
        
        return self.agent.get_tool_info(tool_name)

# Integration interface for easy future replacement
class SpoonOSInterface:
    """
    Abstract interface for spoonOS integration
    Allows easy swapping of implementation when spoonOS is ready
    """
    
    def __init__(self):
        # Use placeholder implementation for now
        self.implementation = SpoonOSIntegration()
    
    async def process_intent(self, intent: Intent) -> SpoonOSResponse:
        """Process user intent through spoonOS"""
        return await self.implementation.send_intent(intent)
    
    def is_available(self) -> bool:
        """Check if spoonOS is available"""
        return self.implementation.health_check()
    
    def get_capabilities(self) -> list:
        """Get spoonOS capabilities"""
        return self.implementation.get_available_tools()

# Factory function for easy configuration
def create_spoonos_integration(endpoint: str = None) -> SpoonOSInterface:
    """
    Factory function to create spoonOS integration
    
    Args:
        endpoint: spoonOS endpoint URL (optional)
        
    Returns:
        SpoonOSInterface instance
    """
    if endpoint:
        integration = SpoonOSIntegration(endpoint)
        interface = SpoonOSInterface()
        interface.implementation = integration
        return interface
    
    return SpoonOSInterface()