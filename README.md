# Web3 Toolbox Agent

AI-powered Web3 customer service agent built for the spoonAI hackathon. Features dual-agent architecture with intelligent routing between AI-powered natural language processing and Web3 tool execution.

## 🎮 Try It Now - Interactive Demo

**Want to see all 21 Web3 tools in action?** Run our comprehensive demo:

### Option 1: Using uv (Recommended)
```bash
git clone <repository-url>
cd web3-toolbox-agent
uv sync
uv run python spoonOS/examples.py
```

### Option 2: Using Python + pip
```bash
git clone <repository-url>
cd web3-toolbox-agent
pip install -r requirements.txt
python spoonOS/examples.py
```

**What you'll see:**
- 🔧 21 real Web3 tools across 5 categories
- 💰 Live price data, balance checks, token swaps
- 📊 OHLCV data from exchanges like Binance
- ⛓️ EVM operations, gas estimates, bridging
- 🐙 GitHub repository analysis
- 🔷 Neo blockchain operations

The demo runs autonomous queries showing each tool's capabilities with real blockchain data!

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone <repository-url>
cd web3-toolbox-agent

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add required API keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# Optional: OPENAI_API_KEY for better performance
# Optional: Web3 RPC URLs for real blockchain data
```

### 3. Start Everything
```bash
# Start the integrated server (hosts both frontend and APIs)
uv run main.py
# Or: python main.py

# Server starts on http://localhost:8000
# Frontend: http://localhost:8000/
# Playground: http://localhost:8000/playground.html
# API: http://localhost:8000/api/chat
```

### 4. Test the Integration
```bash
# Health check
curl http://localhost:8000/health

# Test natural language queries
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the current ETH price?"}'

# Run comprehensive integration test
uv run test_integration.py

# Run complete workflow demo
uv run demo_workflow.py
```

## 🏗️ Architecture

```
Frontend (UI/) ↔ FastAPI Server (main.py) ↔ UserAgent (AI) ↔ SpoonOS (Web3 Tools)
```

### Dual-Agent System

**UserAgent** - AI-powered natural language processing
- Claude 3.5 for intent classification 
- Conversation memory and context awareness
- Session management across requests
- Graceful fallbacks and error handling

**SpoonOS** - Web3 tool execution middleware  
- 21+ Web3 tools across 5 categories
- Real blockchain interactions (when configured)
- Standardized tool execution interface
- Comprehensive error handling and logging

## 📁 Project Structure & Scripts

```
web3-toolbox-agent/
├── main.py                    # 🚀 Main FastAPI server - start here
├── pyproject.toml             # 📦 Project dependencies and config
├── .env.example              # 🔑 Environment variables template
├── demo_workflow.py          # 🎮 Complete system demo
├── test_integration.py       # 🧪 Integration testing suite
│
├── userAgent/                # 🤖 AI Layer (Langchain + Claude)
│   ├── agent.py              # Core UserAgent implementation
│   ├── config.py             # Configuration management
│   ├── spoonos_integration.py # SpoonOS integration layer
│   ├── formatter.py          # Response formatting utilities
│   └── test_agent.py         # Individual agent testing
│
├── spoonOS/                  # 🔧 Web3 Tools Layer
│   ├── agent.py              # SpoonOS tool execution agent
│   ├── config.json           # Tool configuration settings
│   ├── examples.py           # Tool usage examples
│   └── README.md             # SpoonOS documentation
│
└── UI/                       # 🌐 Frontend Interface
    ├── index.html            # Landing page
    ├── playground.html       # Interactive chat interface
    ├── playground.js         # Frontend logic and API calls
    └── styles.css            # Apple HIG-compliant styling
```

### Script Functions

| Script | Purpose | Usage |
|--------|---------|--------|
| **main.py** | 🚀 Main server | `uv run main.py` - Starts everything |
| **demo_workflow.py** | 🎮 Complete demo | `uv run demo_workflow.py` - Shows full workflow |
| **test_integration.py** | 🧪 Integration test | `uv run test_integration.py` - Tests all components |
| **userAgent/test_agent.py** | 🤖 Agent test | `cd userAgent && uv run test_agent.py` |
| **spoonOS/examples.py** | 🔧 Tool examples | `cd spoonOS && uv run examples.py` |

## 🌐 Frontend Integration

### Accessing the UI
- **Landing Page**: `http://localhost:8000/` - Project overview and info
- **Interactive Playground**: `http://localhost:8000/playground.html` - Chat interface
- **API Endpoint**: `http://localhost:8000/api/chat` - Direct API access

### UI Features
- ✅ Apple HIG-compliant dark theme design
- ✅ Real-time chat interface with API integration  
- ✅ Accessibility-focused (ARIA labels, skip links)
- ✅ Example queries and quick actions
- ✅ Session persistence and error handling
- ✅ Responsive design for all devices

## 📡 API Endpoints

### Production Endpoints
- `POST /api/chat` - **Unified chat interface** (recommended)
- `POST /api/user-agent/query` - Direct UserAgent access
- `POST /api/spoonos/execute` - Direct SpoonOS access (placeholder)
- `GET /health` - System health and agent status

### Frontend Assets
- `GET /` - Landing page (index.html)
- `GET /playground.html` - Interactive chat interface
- `GET /styles.css`, `/playground.js` - Static assets

### Request/Response Format
```json
// Request
{
  "query": "What's my ETH balance for 0x123...?",
  "session_id": "optional-session-id"  // Auto-generated if not provided
}

// Response  
{
  "response": "💰 Balance: 2.5 ETH (~$6,250)",
  "success": true,
  "agent": "userAgent", 
  "session_id": "session-1234"
}
```

## 🛠️ Available Web3 Tools

### CRYPTO_DATA (7 tools)
Price monitoring and DeFi analytics
- `get_token_price` - Real-time token prices
- `get_24h_stats` - 24h trading statistics  
- `get_kline_data` - Candlestick/OHLCV data
- `price_threshold_alert` - Price monitoring alerts
- `lp_range_check` - Liquidity position validation
- `sudden_price_increase` - Pump detection
- `lending_rate_monitor` - DeFi lending rates

### CRYPTO_EVM (6 tools)  
Ethereum and EVM chain operations
- `evm_balance` - Token balance queries
- `evm_transfer` - Native ETH transfers
- `evm_erc20_transfer` - ERC-20 token transfers
- `evm_swap` - Token swapping via DEX aggregators
- `evm_swap_quote` - Swap quotes and gas estimates
- `evm_bridge` - Cross-chain asset bridging

### Additional Categories
- **CRYPTO_NEO** (2 tools) - Neo blockchain operations
- **GITHUB** (3 tools) - Repository analysis and insights  
- **CRYPTO_POWERDATA** (3 tools) - Advanced market analysis

## 🧪 Testing & Development

### Quick Testing Commands
```bash
# Test everything end-to-end
uv run demo_workflow.py

# Test individual components
uv run test_integration.py

# Test UserAgent only
cd userAgent && uv run test_agent.py

# Test SpoonOS tools
cd spoonOS && uv run examples.py

# Test via API (server must be running)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Check balance for 0x742d35Cc6634C0532925a3b844Bc454e4438f44e"}'
```

### Development Workflow
```bash
# 1. Start development server with auto-reload
uv run main.py

# 2. Test changes
uv run test_integration.py

# 3. Frontend development: Edit UI/ files, server serves them automatically

# 4. Validate configuration  
python -c "from userAgent.config import Config; Config.validate()"
```

## ⚙️ Environment Configuration

### Required Environment Variables
```bash
# AI/LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...        # Required for UserAgent
OPENAI_API_KEY=sk-proj-...          # Optional, improves performance

# Server Configuration  
HOST=0.0.0.0                        # Server bind address
PORT=8000                           # Server port

# Web3 Configuration (for real blockchain data)
RPC_URL=https://eth.llamarpc.com     # Ethereum RPC endpoint
BITQUERY_CLIENT_ID=your_id           # Bitquery API credentials
BITQUERY_CLIENT_SECRET=your_secret

# SpoonOS Integration
SPOON_OS_ENDPOINT=http://localhost:8080
```

### Example .env File
```bash
# Copy from .env.example and customize
cp .env.example .env

# Minimal setup - just add your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Enhanced setup - add OpenAI for better performance  
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-proj-your-key-here

# Production setup - add Web3 endpoints for real data
ANTHROPIC_API_KEY=sk-ant-your-key-here
RPC_URL=https://mainnet.infura.io/v3/your-infura-key
BITQUERY_CLIENT_ID=your_bitquery_id
BITQUERY_CLIENT_SECRET=your_bitquery_secret
```

## 🎯 Example Queries

### Balance & Transaction Queries
- "What's my ETH balance?"
- "Check wallet 0x742d35Cc...balance" 
- "Show me recent transactions"
- "What tokens do I own?"

### Price & Market Data
- "What's the current ETH price?"
- "Show me BTC price chart" 
- "Monitor USDC lending rates"
- "Alert me if ETH drops below $2000"

### Gas & Swaps
- "How much gas to send 1 ETH?"
- "Estimate swap cost for ETH→USDC"
- "Execute 100 USDC → ETH swap"
- "Best route for token swap?"

### General Web3
- "Explain how gas fees work"
- "What are liquidity pools?"
- "Help me understand DeFi"

## 🔮 Production Deployment

### Making It Production Ready
1. **Install Real Tools**: `uv add spoon-toolkits` 
2. **Configure Web3 RPCs**: Add RPC URLs to .env
3. **Add API Keys**: Bitquery, Infura, etc.
4. **Deploy Frontend**: Host UI/ on CDN or web server
5. **Scale Server**: Use proper WSGI server (Gunicorn, etc.)

### Docker Deployment (Future)
```bash
# Build container
docker build -t web3-toolbox-agent .

# Run with environment
docker run -p 8000:8000 --env-file .env web3-toolbox-agent
```

## 📄 License

See LICENSE file for details.

---

🥄 **Built for the spoonAI hackathon** - Demonstrating the power of dual-agent architecture for Web3 interactions.
