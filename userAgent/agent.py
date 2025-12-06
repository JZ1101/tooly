"""
UserAgent - AI-Powered Web3 Customer Service Agent
"""

import asyncio
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from langchain_anthropic import ChatAnthropic
# Simple conversation memory implementation
class SimpleConversationMemory:
    def __init__(self):
        self.messages = []
    
    def save_context(self, inputs, outputs):
        self.messages.append({"input": inputs.get("input", ""), "output": outputs.get("output", "")})
    
    @property 
    def chat_memory(self):
        return self
    
    def clear(self):
        self.messages = []

try:
    from .spoonos_integration import SpoonOSInterface, create_spoonos_integration, Intent
    from .formatter import ResponseFormatter
except ImportError:
    from spoonos_integration import SpoonOSInterface, create_spoonos_integration, Intent
    from formatter import ResponseFormatter

class UserAgent:
    """AI-powered Web3 customer service agent"""
    
    def __init__(self, anthropic_api_key: str, spoonos_endpoint: str = None):
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            anthropic_api_key=anthropic_api_key,
            temperature=0.1
        )
        self.spoonos = create_spoonos_integration(spoonos_endpoint)
        self.formatter = ResponseFormatter()
        self.sessions = {}  # Store session memories
        self._spoonos_initialized = False
    
    async def initialize_spoonos(self):
        """Initialize SpoonOS integration with real tools"""
        if not self._spoonos_initialized:
            try:
                success = await self.spoonos.implementation.initialize()
                if success:
                    self._spoonos_initialized = True
                    print("✅ UserAgent: SpoonOS integration initialized successfully")
                else:
                    print("⚠️ UserAgent: SpoonOS integration failed, using fallback responses")
            except Exception as e:
                print(f"❌ UserAgent: SpoonOS initialization error: {e}")
        
        # UserAgent is now a simple filter/router - no complex intent classification needed
    
    def _setup_memory(self) -> SimpleConversationMemory:
        """Setup conversation memory"""
        return SimpleConversationMemory()
    
    def get_session_memory(self, session_id: str) -> SimpleConversationMemory:
        """Get or create memory for a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = self._setup_memory()
        return self.sessions[session_id]
    
    async def process_query(self, user_input: str, session_id: str = "default") -> str:
        """Simple filter - extract Web3 query and send to SpoonOS ReAct agent"""
        try:
            # Ensure SpoonOS is initialized
            await self.initialize_spoonos()
            
            # Simple Web3 keyword detection
            web3_keywords = ['eth', 'btc', 'token', 'price', 'balance', 'swap', 'gas', 'wallet', 'address', 'crypto', 'defi', 'nft', 'blockchain', 'transaction', 'ohlcv', 'kline', 'candles', 'chart', 'binance', 'usdt', 'usdc', 'uniswap', 'contract', 'transfer']
            is_web3_query = any(keyword in user_input.lower() for keyword in web3_keywords)
            
            if is_web3_query:
                # Extract the important Web3 part and send directly to SpoonOS
                clean_query = await self._extract_web3_query(user_input, session_id)
                response = await self._send_to_spoonos_react(clean_query)
            else:
                # Non-Web3 query - handle with general chat
                response = await self._handle_general_chat(user_input, session_id)
            
            # Update session memory
            self._update_session_memory(session_id, user_input, response)
            return response
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"I encountered an issue processing your request: {str(e)}"
    
    async def _extract_web3_query(self, user_input: str, session_id: str = "default") -> str:
        """Simple extraction of Web3-relevant parts from noisy input"""
        # Get conversation context
        memory = self.get_session_memory(session_id)
        history = memory.messages
        
        context = ""
        if history:
            for msg in history[-2:]:  # Last 2 exchanges for context
                context += f"Previous: {msg['input']} → {msg['output']}\n"
        
        prompt = f"""Extract the Web3/crypto question from this user input. Remove irrelevant noise and keep only the essential Web3 query.

{f"Context: {context}" if context else ""}

User input: "{user_input}"

Return only the clean Web3 question (no explanations):"""

        try:
            response = await self.llm.ainvoke(prompt)
            return response.content.strip()
        except:
            return user_input  # Fallback to original if extraction fails

    async def _send_to_spoonos_react(self, query: str) -> str:
        """Send clean query directly to SpoonOS ReAct agent (like examples.py)"""
        try:
            # Import SpoonOS ReAct components
            from spoonOS.agent import SpoonOSAgent, ToolCategory
            try:
                from spoon_ai.agents import SpoonReactAI
                from spoon_ai.chat import ChatBot
                from spoon_ai.tools import ToolManager
                import os
                
                # Create ReAct agent with all SpoonOS tools (same as examples.py)
                if not hasattr(self, '_react_agent'):
                    # Initialize SpoonOS agent with all tools
                    tool_agent = SpoonOSAgent()
                    categories = [ToolCategory.CRYPTO_DATA, ToolCategory.CRYPTO_EVM, 
                                ToolCategory.CRYPTO_NEO, ToolCategory.GITHUB, 
                                ToolCategory.CRYPTO_POWERDATA]
                    await tool_agent.initialize(categories)
                    
                    # Get all tool instances
                    tools = []
                    for category in categories:
                        category_tools = tool_agent.registry.list_tools(category)
                        for tool_name in category_tools:
                            tool_instance = tool_agent.registry.get_tool(tool_name)
                            tools.append(tool_instance)
                    
                    tool_manager = ToolManager(tools)
                    
                    # Create ReAct agent (same as examples.py logic)
                    openai_key = os.getenv("OPENAI_API_KEY")
                    if openai_key:
                        self._react_agent = SpoonReactAI(
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
                        # Fallback to current approach if no OpenAI key
                        return await self._fallback_to_current_approach(query)
                
                # Run query through ReAct agent
                raw_result = await self._react_agent.run(query)
                # Format the result for better user experience
                formatted_result = await self._format_spoonos_result(str(raw_result), query)
                return formatted_result
                
            except ImportError:
                # spoon_ai not available, fallback
                return await self._fallback_to_current_approach(query)
                
        except Exception as e:
            print(f"❌ ReAct agent error: {e}")
            return await self._fallback_to_current_approach(query)

    async def _format_spoonos_result(self, raw_result: str, original_query: str) -> str:
        """Format raw SpoonOS result into clean, user-friendly response"""
        try:
            # Simple formatting prompt to clean up raw output
            format_prompt = f"""Transform this raw Web3 tool output into a clean, user-friendly response.

Original user question: "{original_query}"
Raw tool output: {raw_result}

Make it:
- Clear and concise
- Remove technical jargon where possible
- Keep important numbers/data but format nicely
- Add appropriate emojis for better readability
- If it's an error, explain it simply

Return only the formatted response:"""

            response = await self.llm.ainvoke(format_prompt)
            return response.content.strip()
            
        except Exception as e:
            print(f"⚠️ Formatting failed: {e}")
            # Fallback: basic cleanup of raw result
            return self._basic_format_cleanup(raw_result)
    
    def _basic_format_cleanup(self, raw_result: str) -> str:
        """Basic cleanup of raw result if AI formatting fails"""
        result = str(raw_result)
        
        # Remove excessive technical details
        if "ToolResult" in result:
            # Extract just the meaningful part
            try:
                import re
                # Look for JSON-like data
                json_match = re.search(r'\{.*\}', result)
                if json_match:
                    result = json_match.group()
            except:
                pass
        
        # Add basic formatting
        if "price" in result.lower():
            result = f"💲 {result}"
        elif "balance" in result.lower():
            result = f"💰 {result}"
        elif "error" in result.lower():
            result = f"❌ {result}"
        else:
            result = f"✅ {result}"
            
        return result

    async def _fallback_to_current_approach(self, query: str) -> str:
        """Fallback to current SpoonOS integration if ReAct unavailable"""
        # Use existing SpoonOS integration as backup
        intent = Intent(action="general_web3", parameters={"query": query}, confidence=1.0, reasoning="Direct query")
        spoonos_response = await self.spoonos.process_intent(intent)
        
        if spoonos_response.success:
            return spoonos_response.output
        else:
            return f"❌ {spoonos_response.output}"

    async def _handle_general_chat(self, user_input: str, session_id: str = "default") -> str:
        """Handle general conversation using LLM with context"""
        memory = self.get_session_memory(session_id)
        history = memory.messages
        
        # Include conversation context for general chat too
        history_text = ""
        if history:
            for msg in history[-3:]:  # Last 3 exchanges for context
                history_text += f"User: {msg['input']}\nAssistant: {msg['output']}\n\n"
        
        prompt = f"""
You are a helpful Web3 assistant powered by SpoonOS with access to 21+ real Web3 tools.

Conversation History:
{history_text if history_text else "No previous conversation."}

Current user message: "{user_input}"

This appears to be a general question. Respond helpfully and guide users toward specific Web3 actions I can perform:

**Real Web3 capabilities powered by SpoonOS:**
- **Price Data**: "What's the current price of ETH?" 
- **Balance Checks**: "Check my ETH balance at [address]"
- **Transaction Data**: "Show my recent transactions"
- **Gas Estimates**: "Estimate gas for this transaction"
- **Token Swaps**: "Swap 1 ETH for USDC"
- **Smart Contracts**: "Execute this contract function"
- **NFT Information**: "Get info about this NFT collection"
- **DeFi Analytics**: "Check lending rates for USDC"

Ask me specific Web3 questions and I'll use real blockchain data through SpoonOS!
"""
        response = await self.llm.ainvoke(prompt)
        return response.content
    
    def _update_session_memory(self, session_id: str, user_input: str, response: str) -> None:
        """Update conversation memory for a specific session"""
        try:
            memory = self.get_session_memory(session_id)
            memory.save_context(
                inputs={'input': user_input},
                outputs={'output': response}
            )
        except Exception as e:
            # Memory update is not critical, continue without it
            pass
    
