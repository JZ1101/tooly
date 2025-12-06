---
applyTo: "**"
---

# Desearch Data Platform

`spoon_toolkits.data_platforms.desearch` wraps the official DeSearch SDK in async helpers, builtin Spoon tools, and FastMCP servers so agents can query real-time web, social, and academic sources without writing raw HTTP logic.

## Environment & Configuration

```bash
export DESEARCH_API_KEY=your_actual_key            # required
export DESEARCH_BASE_URL=https://api.desearch.ai   # optional (not currently consumed)
export DESEARCH_TIMEOUT=30                         # optional (read but not yet wired into SDK calls)
```

- `env.py` loads `.env` via `python-dotenv`, so store the variables beside the process that imports the package.
- `DESEARCH_BASE_URL`/`DESEARCH_TIMEOUT` are parsed for future use but the current helpers always talk to the SDK defaults; changing these env vars today has no effect without modifying the code.
- The helpers enforce `limit >= 10`, mirroring the SDK requirements.

## Package Layout

| Module | Purpose |
|--------|---------|
| `__init__.py` | Mounts `ai_search` and `web_search` FastMCP sub-servers and re-exports helper coroutines plus `mcp_server`. |
| `ai_search_official.py` | Async tools for AI/meta search, Reddit/Twitter feeds, and academic datasets. Decorated with `@mcp.tool()`. |
| `web_search_official.py` | Web search plus Twitter post/link lookups using the official SDK. |
| `builtin_tools.py` | `BaseTool` wrappers (`DesearchAISearchTool`, etc.) for spoon-core usage without MCP. |
| `cache.py` | `time_cache` decorator that memoizes tool responses for ~5 minutes. |
| `example.py`, `test_integration.py`, `README.md` | Usage demos, live API smoke tests, and quick-start. |

## Tooling Highlights

### AI and Social Search

- `search_ai_data(query, platforms, limit)` aggregates results from web, Reddit, Wikipedia, YouTube, Twitter, ArXiv, and HackerNews.
- `search_social_media(query, platform, limit)` targets Twitter or Reddit directly.
- `search_academic(query, platform, limit)` narrows to ArXiv or Wikipedia research corpora.

### Web and Twitter Search

- `search_web(query, num_results, start)` calls `basic_web_search` and returns snippet-rich results.
- `search_twitter_posts(query, limit, sort)` pulls live tweets with sort control (Top, Latest, etc.).
- `search_twitter_links(query, limit)` surfaces URLs that are trending on Twitter.

### Builtin Tools and Caching

- `DesearchAISearchTool`, `DesearchWebSearchTool`, `DesearchAcademicSearchTool`, and `DesearchTwitterSearchTool` validate API keys up front and expose JSON schemas for planners.
- `time_cache` decorates every MCP tool, preventing duplicate outbound calls during iterative planning loops.

## Usage Examples

### Mount the FastMCP server

```python
from spoon_toolkits.data_platforms.desearch import mcp_server

agent_config = {
    "tools": [mcp_server],
}
```

### Call async helpers directly

```python
from spoon_toolkits.data_platforms.desearch import (
    search_ai_data,
    search_web,
)

async def summarize(topic: str):
    ai = await search_ai_data(query=f"{topic} 2024", platforms="web,reddit,wikipedia", limit=12)
    web = await search_web(query=topic, num_results=5)
    return {"ai": ai, "web": web}
```

### Use builtin tools

```python
from spoon_toolkits.data_platforms.desearch.builtin_tools import DesearchAISearchTool

tool = DesearchAISearchTool()
response = await tool.execute(query="Solana MEV research", platforms="web,reddit", limit=10)

if not response.get("success"):
    raise RuntimeError(response.get("error"))

print(response["data"]["results"].keys())
```

## FastMCP Server Mode

```bash
python -m spoon_toolkits.data_platforms.desearch
# or in code:
from spoon_toolkits.data_platforms.desearch import mcp_server
mcp_server.run(transport="sse", host="0.0.0.0", port=8000, path="/sse")
```

## Operational Notes

- Use `test_integration.py` before shipping: it validates your API key and SDK wiring.
- Responses are dictionaries (e.g., `{"query": ..., "results": ..., "count": ...}`); check for `"error"` keys when handling failures.
- `DESEARCH_TIMEOUT` is parsed but currently unused; adjust it only after wiring the value into helper functions.
- Remove cached entries by restarting the process if you need uncached data while debugging.
- Rate limits come from the DeSearch API; stagger large batches or broaden queries.

## Next Steps

- [Thirdweb Platform](./toolkit-data-platforms-thirdweb.instructions.md) - Thirdweb Insight API
- [GitHub Tools](./toolkit-github-analysis.instructions.md) - Repository analysis
