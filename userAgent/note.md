**UserAgent - Intent-Based Customer Service Layer**

Responsibilities:
- Classify user intents from natural language input
- Route structured intents to appropriate handlers (spoonOS agent)  
- Format responses for user-friendly display
- Manage conversation memory and context
- Handle errors and fallbacks gracefully

Key Components:
- Intent classification system (`intent.py`)
- spoonOS integration interface (`spoonos_integration.py`)  
- Response formatting (`formatter.py`)
- Main agent orchestrator (`agent.py`)

This agent focuses on UNDERSTANDING user needs, not executing Web3 tools directly.
