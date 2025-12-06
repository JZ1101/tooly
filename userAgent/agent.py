"""
UserAgent - AI-Powered Web3 Customer Service Agent
"""

import asyncio
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory

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
        
        # Intent classification prompt with context
        self.intent_prompt = """
You are a Web3 assistant. Analyze the user query and extract:
1. Action: check_balance, get_transactions, estimate_gas, execute_contract, swap_tokens, get_nft_info, or general_chat
2. Parameters: any relevant data (addresses, tokens, amounts, etc.)
3. Confidence: 0.0-1.0 how certain you are

Conversation History:
{history}

Current User Query: {query}

Consider the conversation context when classifying. If the user refers to "that address", "my balance", etc., use context from previous messages.

Respond with JSON only:
{{"action": "action_name", "parameters": {{}}, "confidence": 0.8, "reasoning": "explanation"}}
"""
    
    async def _classify_intent(self, user_input: str, session_id: str = "default") -> Intent:
        """Use AI to understand user intent with conversation context"""
        try:
            # Get conversation history
            memory = self.get_session_memory(session_id)
            history = memory.chat_memory.messages if memory.chat_memory.messages else []
            
            # Format history for context
            history_text = ""
            if history:
                for i in range(0, len(history), 2):
                    if i + 1 < len(history):
                        human_msg = history[i].content if hasattr(history[i], 'content') else str(history[i])
                        ai_msg = history[i+1].content if hasattr(history[i+1], 'content') else str(history[i+1])
                        history_text += f"User: {human_msg}\nAssistant: {ai_msg}\n\n"
            
            if not history_text:
                history_text = "No previous conversation."
            
            prompt = self.intent_prompt.format(query=user_input, history=history_text)
            response = await self.llm.ainvoke(prompt)
            result = json.loads(response.content)
            
            return Intent(
                action=result["action"],
                parameters=result["parameters"],
                confidence=result["confidence"],
                reasoning=result["reasoning"]
            )
        except Exception as e:
            return Intent(
                action="general_chat",
                parameters={},
                confidence=0.0,
                reasoning=f"Classification failed: {str(e)}"
            )
    
    def _setup_memory(self) -> ConversationBufferMemory:
        """Setup conversation memory"""
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    def get_session_memory(self, session_id: str) -> ConversationBufferMemory:
        """Get or create memory for a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = self._setup_memory()
        return self.sessions[session_id]
    
    async def process_query(self, user_input: str, session_id: str = "default") -> str:
        """Main entry point - AI classifies intent and routes to spoonOS"""
        try:
            # Get session memory
            memory = self.get_session_memory(session_id)
            
            # AI classifies the intent with context
            intent = await self._classify_intent(user_input, session_id)
            
            # Route based on intent
            if intent.action == "general_chat" or intent.confidence < 0.3:
                response = await self._handle_general_chat(user_input, session_id)
            else:
                # Send to spoonOS for Web3 actions
                spoonos_response = await self.spoonos.process_intent(intent)
                
                if spoonos_response.success:
                    response = spoonos_response.output
                else:
                    # Handle failed requests with optional follow-up questions
                    response = spoonos_response.output
                    if spoonos_response.follow_up_questions:
                        response += "\n\n" + "\n".join(f"• {q}" for q in spoonos_response.follow_up_questions)
            
            # Update session memory
            self._update_session_memory(session_id, user_input, response)
            return response
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"I encountered an issue processing your request: {str(e)}"
    
    async def _handle_general_chat(self, user_input: str, session_id: str = "default") -> str:
        """Handle general conversation using LLM with context"""
        memory = self.get_session_memory(session_id)
        history = memory.chat_memory.messages if memory.chat_memory.messages else []
        
        # Include conversation context for general chat too
        history_text = ""
        if history:
            for i in range(0, len(history), 2):
                if i + 1 < len(history):
                    human_msg = history[i].content if hasattr(history[i], 'content') else str(history[i])
                    ai_msg = history[i+1].content if hasattr(history[i+1], 'content') else str(history[i+1])
                    history_text += f"User: {human_msg}\nAssistant: {ai_msg}\n\n"
        
        prompt = f"""
You are a helpful Web3 assistant. 

Conversation History:
{history_text if history_text else "No previous conversation."}

Current user message: "{user_input}"

This doesn't seem to be a specific Web3 request. Respond helpfully considering the conversation context. Mention what Web3 actions you can help with:
- Check token balances  
- Get transaction history
- Estimate gas fees
- Execute smart contracts
- Token swaps
- NFT information

Be friendly and educational.
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
    
