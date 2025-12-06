# Web3 Toolbox Agent

AI-powered Web3 customer service agent built for the spoonAI hackathon. Features dual-agent architecture with intelligent routing between AI-powered natural language processing and direct Web3 execution.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the Server
```bash
python main.py
```

Server starts on `http://localhost:8000`

### 4. Test the Agent
```bash
# Health check
curl http://localhost:8000/health

# Test UserAgent
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my ETH balance?"}'

# Built-in test endpoint
curl http://localhost:8000/api/test/user-agent
```

## 🏗️ Architecture

```
User Input → UserAgent (AI Layer) → SpoonOS (Web3 Layer) → Blockchain Networks
```

### Components

- **UserAgent** (`userAgent/`) - AI-powered intent classification using Claude 3.5
- **SpoonOS** (`spoonOS/`) - Web3 execution layer (placeholder for future implementation)  
- **Main Server** (`main.py`) - FastAPI server hosting both agents

## 📡 API Endpoints

### Core Endpoints
- `POST /api/chat` - Unified chat interface (auto-routes to appropriate agent)
- `POST /api/user-agent/query` - Direct UserAgent access
- `POST /api/spoonos/execute` - Direct SpoonOS access (coming soon)
- `GET /health` - Health check

### Development Endpoints
- `GET /api/test/user-agent` - Test UserAgent with sample queries

### Request Format
```json
{
  "query": "What's my ETH balance?",
  "session_id": "optional-session-id"
}
```

### Response Format
```json
{
  "response": "Based on the mock data, your ETH balance is 2.5 ETH...",
  "success": true,
  "agent": "userAgent",
  "session_id": "optional-session-id"
}
```

## 🤖 Supported Actions

### UserAgent (AI Layer)
- Natural language understanding
- Intent classification
- Conversation memory
- Error handling with follow-up questions

### Detected Intents
- `check_balance` - Token balance queries
- `get_transactions` - Transaction history
- `estimate_gas` - Gas fee estimation
- `execute_contract` - Smart contract interactions
- `swap_tokens` - Token swapping
- `get_nft_info` - NFT information
- `general_chat` - General conversation

## 🛠️ Development

### Project Structure
```
web3-toolbox-agent/
├── main.py              # FastAPI server (hosts both agents)
├── requirements.txt     # All dependencies
├── .env.example        # Environment template
├── userAgent/          # AI layer implementation
│   ├── agent.py        # Main UserAgent class
│   ├── config.py       # Configuration management
│   ├── formatter.py    # Response formatting
│   └── spoonos_integration.py  # SpoonOS interface
└── spoonOS/            # Web3 layer (future implementation)
```

### Running in Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run with auto-reload
python main.py
```

### Environment Variables
```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Server configuration
HOST=0.0.0.0
PORT=8000

# spoonOS Integration (when ready)
SPOON_OS_ENDPOINT=http://localhost:8080
SPOON_OS_API_KEY=your_spoon_os_api_key

# Web3 RPC URLs (for future spoonOS integration)
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your_infura_key
POLYGON_RPC_URL=https://polygon-mainnet.infura.io/v3/your_infura_key
```

## 🧪 Testing

### Manual Testing
```bash
# Test individual agent
python userAgent/test_agent.py

# Test via API
curl -X POST http://localhost:8000/api/test/user-agent
```

### Example Queries
- "What's my ETH balance?"
- "How much would it cost to send 1 ETH?"
- "Show me my recent transactions"
- "What NFTs do I own?"
- "Hello there!" (general chat)

## 🔮 Future Implementation

### SpoonOS Integration
When spoonOS becomes available:
1. Replace mock implementations in `userAgent/spoonos_integration.py`
2. Implement real Web3 functionality
3. Add transaction signing and monitoring
4. Enable actual blockchain interactions

### Planned Features
- Multi-chain support (Ethereum, Polygon, etc.)
- Real-time transaction monitoring
- Advanced intent classification
- Session management
- Frontend UI integration

## 📄 License

See LICENSE file for details.

---

Built for the spoonAI hackathon 🥄
