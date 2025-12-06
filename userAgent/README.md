# UserAgent - Web3 Customer Service

Simple LangChain agent that routes user queries to spoonOS tools.

## Quick Start

```python
from userAgent.agent import UserAgent

# Initialize agent
agent = UserAgent(anthropic_api_key="your-key")

# Process user query
response = agent.process_query("What's my ETH balance?")
print(response)
```

## Structure

- `agent.py` - Main agent with LangChain integration
- `router.py` - Routes queries to appropriate tools  
- `formatter.py` - Formats responses for users
- `test_agent.py` - Test script with examples

## Placeholders

All spoonOS connections are placeholder functions. Replace these when spoonOS is ready:

```python
# In agent.py - replace these with real spoonOS calls:
_placeholder_check_balance()
_placeholder_get_tx_history() 
_placeholder_estimate_gas()
_placeholder_execute_contract()
```

## Testing

```bash
cd userAgent
python test_agent.py
```

Works with mock data even without API key.