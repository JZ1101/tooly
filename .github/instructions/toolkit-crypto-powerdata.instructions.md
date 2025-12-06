---
applyTo: "**"
---

# Crypto PowerData Tools

`spoon_toolkits.crypto.crypto_powerdata` fuses CCXT-powered CEX feeds, OKX Web3 DEX data, TA-Lib/enhanced indicators, and an MCP server that can stream results over stdio or SSE. Use it when agents need richer analytics than simple price lookups.

## Environment & Settings

```bash
export OKX_API_KEY=...
export OKX_SECRET_KEY=...
export OKX_API_PASSPHRASE=...
export OKX_PROJECT_ID=...
export OKX_BASE_URL=https://web3.okx.com/api/v5/   # optional override

# Optional overrides (defaults shown)
export RATE_LIMIT_REQUESTS_PER_SECOND=10
export MAX_RETRIES=3
export RETRY_DELAY=1.0
export TIMEOUT_SECONDS=30
```

`data_provider.Settings` ingests these variables (plus indicator defaults such as SMA/EMA periods). Missing OKX keys raise immediately before any HTTP call, so configure them centrally—either via environment or by passing `env_vars` into the MCP helpers.

## What's Inside the Toolkit

| Component | File(s) | Purpose |
|-----------|---------|---------|
| `CryptoPowerDataCEXTool` | `tools.py` | Pull OHLCV candles from 100+ CCXT exchanges and pipe them through the enhanced indicator stack. |
| `CryptoPowerDataDEXTool` | `tools.py` | Hit OKX Web3 DEX APIs for on-chain pairs specified by `chain_index` + token address. |
| `CryptoPowerDataPriceTool` | `tools.py` | Lightweight spot price snapshot (CEX or DEX) without fetching an entire candle set. |
| `CryptoPowerDataIndicatorsTool` | `tools.py` | Enumerate every indicator name/parameter accepted by the enhanced TA registry (TA-Lib + custom extras). |
| `Settings`, `OKXDEXClient`, `TechnicalAnalysis` | `data_provider.py` | Central place for rate limiting, retries, authenticated OKX calls, and TA-Lib helpers. |
| MCP server runners | `server.py`, `dual_transport_server.py` | Start stdio or HTTP/SSE transports so UI agents can subscribe to continuous feeds. |
| Analytics core | `main.py`, `enhanced_indicators.py`, `talib_registry.py` | Parse indicator configs, register TA functions, and expose them via FastMCP tools. |

All tools inherit `CryptoPowerDataBaseTool`, which lazily initializes global settings and reuses throttled clients; you rarely need to micromanage sessions yourself.

## Indicator Configuration

- Accepts either JSON strings (most MCP clients) or native dicts. Double-encoded JSON like `"\"{\\\"ema\\\": ...}\""` is auto-decoded.
- Mix-and-match multiple parameters per indicator: `{"ema": [{"timeperiod": 12}, {"timeperiod": 26}], "macd": [{"fastperiod": 12, "slowperiod": 26, "signalperiod": 9}]}`
- Enhanced registry supports 150+ TA-Lib functions plus custom composites (VWAP, BB width/position, Aroon oscillators, etc.).
- Validation errors bubble back as descriptive `ToolResult.error` messages so you can surface them directly to users.

## Usage Patterns

### CEX candles + indicators

```python
from spoon_toolkits.crypto.crypto_powerdata import CryptoPowerDataCEXTool

tool = CryptoPowerDataCEXTool()
result = await tool.execute(
    exchange="binance",
    symbol="BTC/USDT",
    timeframe="1h",
    limit=200,
    indicators_config='{"ema": [{"timeperiod": 12}, {"timeperiod": 26}], "rsi": [{"timeperiod": 14}]}',
)
```

### DEX price lookup

```python
from spoon_toolkits.crypto.crypto_powerdata import CryptoPowerDataDEXTool

dex_tool = CryptoPowerDataDEXTool()
result = await dex_tool.execute(
    chain_index="1",
    token_address="0xA0b86a33E6441e88C5F2712C3E9b74E39E9f6E5a",
)
```

## Best Practices

- Configure OKX credentials centrally via environment variables
- Use indicator validation to catch configuration errors early
- Leverage rate limiting and retry logic for production deployments
- Monitor MCP server health when using streaming transports

## Next Steps

- [Crypto Data Tools](./toolkit-crypto-data-tools.instructions.md) - Additional cryptocurrency data tools
- [EVM Tools](./toolkit-crypto-evm.instructions.md) - Ethereum and EVM chain interactions
