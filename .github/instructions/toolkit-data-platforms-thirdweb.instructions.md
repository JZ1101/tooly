---
applyTo: "**"
---

# Thirdweb Data Platform

`spoon_toolkits.data_platforms.third_web` wraps the Thirdweb Insight REST API in async `BaseTool` classes so Spoon agents can fetch contract events, multichain transfers, transactions, and block data without crafting HTTP requests by hand.

## Environment & Configuration

```bash
export THIRDWEB_CLIENT_ID=your_client_id
```

- Tools fall into two credential styles:
  1. `GetContractEventsFromThirdwebInsight`, `GetBlocksFromThirdwebInsight`, and `GetWalletTransactionsFromThirdwebInsight` require a `client_id` argument on every call.
  2. `GetMultichainTransfersFromThirdwebInsight`, `GetTransactionsTool`, `GetContractTransactionsTool`, and `GetContractTransactionsBySignatureTool` exclusively read `THIRDWEB_CLIENT_ID`.
- Requests use a 100-second timeout where implemented; a few helpers currently omit the timeout parameter.
- Each tool catches exceptions and returns either a formatted status string (prefixed with ✅/❌) or a dict like `{"error": "..."}`—errors do not raise.

## Package Layout

| Module | Purpose |
|--------|---------|
| `third_web_tools.py` | Houses every `BaseTool` plus lightweight async test helpers. Some `execute` methods return human-readable strings instead of raw JSON. |

## Tooling Highlights

### Events and Transfers

- `GetContractEventsFromThirdwebInsight` - fetch decoded events for a contract + signature with paging metadata. Returns a status string.
- `GetMultichainTransfersFromThirdwebInsight` - scan recent transfers for a list of chain IDs. Returns raw Insight JSON dict.

### Transactions and Blocks

- `GetTransactionsTool` - consolidate recent transactions across multiple chains. Returns raw JSON dict.
- `GetContractTransactionsTool` - view activity for a single contract. Returns raw JSON dict.
- `GetContractTransactionsBySignatureTool` - narrow contract activity down to a specific function signature. Returns raw JSON dict.
- `GetBlocksFromThirdwebInsight` - stream the latest blocks per chain. Returns formatted status string.
- `GetWalletTransactionsFromThirdwebInsight` - list wallet transactions across multiple chains. Returns status string.

## Usage Examples

### Fetch contract events

```python
from spoon_toolkits.data_platforms.third_web.third_web_tools import GetContractEventsFromThirdwebInsight

tool = GetContractEventsFromThirdwebInsight()
result = await tool.execute(
    client_id="your-client-id",
    chain_id=1,
    contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7",
    event_signature="Transfer(address,address,uint256)",
    limit=5,
)
if result.startswith("❌"):
    raise RuntimeError(result)
```

### Aggregate transfers across chains

```python
from spoon_toolkits.data_platforms.third_web.third_web_tools import GetMultichainTransfersFromThirdwebInsight

tool = GetMultichainTransfersFromThirdwebInsight()
transfers = await tool.execute(chains=[1, 137, 8453], limit=10)
print(transfers["data"][0])
```

### Inspect wallet transactions

```python
from spoon_toolkits.data_platforms.third_web.third_web_tools import GetWalletTransactionsFromThirdwebInsight

wallet_tool = GetWalletTransactionsFromThirdwebInsight()
history = await wallet_tool.execute(
    client_id="your-client-id",
    wallet_address="0xabc...",
    chains=[1, 137],
    limit=10,
    sort_by="block_timestamp",
    sort_order="desc",
)
```

## Operational Notes

- Set `THIRDWEB_CLIENT_ID` in your runtime environment for env-driven tools, and pass `client_id` for helpers that require it.
- HTTP errors are caught and reported in the returned string/dict instead of raising.
- Test helpers at the bottom of `third_web_tools.py` offer quick sanity checks.
- Insight endpoints enforce per-client rate limits; stagger large batch pulls.

## Next Steps

- [GitHub Analysis Tools](./toolkit-github-analysis.instructions.md) - Repository analysis
- [GitHub Provider](./toolkit-github-provider.instructions.md) - Low-level GraphQL client
