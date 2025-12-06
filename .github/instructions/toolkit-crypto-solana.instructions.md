---
applyTo: "**"
---

# Solana Tools

`spoon_toolkits.crypto.solana` provides Python-based Solana blockchain tools built on top of `solana-py`, offering native SOL transfers, SPL token operations, and Jupiter-powered token swaps.

## Environment & Dependencies

```bash
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
export SOLANA_PRIVATE_KEY=your_base58_or_base64_private_key
export HELIUS_API_KEY=your_helius_key   # Optional
export BIRDEYE_API_KEY=your_birdeye_key # Optional
```

The keypair loader accepts both base58 (phantom export) and base64 strings, and you can override any parameter per call via the tool arguments.

## Tool Catalog

### Transfer Tools

#### SolanaTransferTool

Transfer SOL or SPL tokens to another address.

**Parameters:**
- `recipient` (str, required) - Destination Solana address
- `amount` (str/number, required) - Amount in human-readable units
- `token_address` (str, optional) - SPL token mint address; omit for SOL
- `rpc_url` (str, optional) - RPC endpoint override
- `private_key` (str, optional) - Sender private key override

**Example:**
```python
from spoon_toolkits.crypto.solana import SolanaTransferTool

transfer_tool = SolanaTransferTool()
result = await transfer_tool.execute(
    recipient="9jW8FPr6BSSsemWPV22UUCzSqkVdTp6HTyPqeqyuBbCa",
    amount="0.1"
)
```

**Features:**
- Automatic ATA (Associated Token Account) creation for recipients
- Transfers execute immediately after submission

### Swap Tools

#### SolanaSwapTool

Execute token swaps using Jupiter aggregator with intelligent token resolution.

**Parameters:**
- `input_token` (str, required) - Input token (symbol/mint/address)
- `output_token` (str, required) - Output token (symbol/mint/address)
- `amount` (str/number, required) - Amount to swap
- `slippage_bps` (int, optional) - Slippage tolerance in basis points (default: dynamic)
- `priority_level` (str, optional) - Transaction priority: `low`, `medium`, `high`, `veryHigh` (default)
- `rpc_url` (str, optional) - RPC endpoint override
- `private_key` (str, optional) - Wallet private key override

**Priority Fee Levels:**

| Level | Max Lamports | Use Case |
|-------|-------------|----------|
| `low` | 50 | Non-urgent swaps |
| `medium` | 200 | Normal operations |
| `high` | 1,000 | Time-sensitive |
| `veryHigh` | 4,000,000 | MEV protection (default) |

**Example:**
```python
from spoon_toolkits.crypto.solana import SolanaSwapTool

swap_tool = SolanaSwapTool()
result = await swap_tool.execute(
    input_token="SOL",
    output_token="USDC",
    amount="1.0",
    slippage_bps=50,
    priority_level="high"
)
```

### Wallet Tools

#### SolanaWalletInfoTool

Query comprehensive wallet information including SOL balance and SPL token holdings.

**Parameters:**
- `address` (str, optional) - Wallet address; defaults to configured wallet
- `include_tokens` (bool, optional) - Include SPL token balances (default: True)
- `token_limit` (int, optional) - Max tokens to return (default: 20)
- `rpc_url` (str, optional) - RPC endpoint override

**Example:**
```python
from spoon_toolkits.crypto.solana import SolanaWalletInfoTool

wallet_tool = SolanaWalletInfoTool()
result = await wallet_tool.execute()
print(f"SOL Balance: {result.output['sol_balance']}")
```

**Features:**
- Wallet cache scheduler for efficient repeated reads
- Optional price data when Birdeye API key is present
- Portfolio cache for swap helper's token resolution

## Service Helpers

### Validation

```python
from spoon_toolkits.crypto.solana import (
    validate_solana_address,
    validate_private_key,
    is_native_sol
)

is_valid = validate_solana_address("9jW8FPr6BSSsemWPV22UUCzSqkVdTp6HTyPqeqyuBbCa")
is_valid = validate_private_key("5j7s...")
is_sol = is_native_sol("So11111111111111111111111111111111111111112")
```

### Conversion

```python
from spoon_toolkits.crypto.solana import (
    lamports_to_sol,
    sol_to_lamports,
    format_token_amount,
    parse_token_amount
)

lamports = sol_to_lamports(1.5)
sol = lamports_to_sol(1500000000)
ui_amount = format_token_amount(150230000, decimals=6)
raw_amount = parse_token_amount(150.23, decimals=6)
```

### Address Utilities

```python
from spoon_toolkits.crypto.solana import (
    get_associated_token_address,
    truncate_address,
    detect_pubkeys_from_string
)

ata = get_associated_token_address(token_mint="EPjFW...", owner="9jW8F...")
short = truncate_address("9jW8FPr6BSSsemWPV22UUCzSqkVdTp6HTyPqeqyuBbCa")
pubkeys = detect_pubkeys_from_string("Send 1 SOL to 9jW8F...")
```

## Wallet Cache Scheduler

Background service that keeps wallet data fresh:

```python
from spoon_toolkits.crypto.solana import get_wallet_cache_scheduler

scheduler = get_wallet_cache_scheduler()

await scheduler.ensure_running(
    rpc_url="https://api.mainnet-beta.solana.com",
    wallet_address="9jW8F...",
    include_tokens=True
)

cached = await scheduler.get_cached(
    rpc_url="https://api.mainnet-beta.solana.com",
    wallet_address="9jW8F..."
)
```

## Operational Notes

- Fund the signer via Solana faucets for testnet development
- Keep `SOLANA_PRIVATE_KEY` secure; use environment variables
- Monitor RPC rate limits for production deployments
- Configure priority fees based on network congestion

## Next Steps

- [Data Platforms: Chainbase](./toolkit-data-platforms-chainbase.instructions.md) - Blockchain data provider
- [Data Platforms: Desearch](./toolkit-data-platforms-desearch.instructions.md) - Search and discovery tools
