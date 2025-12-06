---
applyTo: "**"
---

# Mem0 Memory Tools

`spoon_toolkits.memory.mem0` provides async `BaseTool` classes that wrap the Mem0 long-term memory API (https://mem0.ai). Use these tools to store and retrieve persistent agent memory across sessions.

## Environment & Credentials

```bash
export MEM0_API_KEY=your_mem0_api_key
```

- All tools read `MEM0_API_KEY` on initialization and raise `ValueError` if the key is missing or empty.
- The SDK targets the Mem0 cloud service at `https://api.mem0.ai/v1`. For self-hosted deployments, override `base_url` in the `Mem0Client` constructor.

## Tool Catalog

| Tool | Parameters | What it does | Return format |
|------|------------|--------------|---------------|
| `AddMemoryTool` | `messages` (List[dict]), `user_id` (str) | Store conversation history (list of role/content dicts) for a user | Status string (✅ or ❌) |
| `SearchMemoryTool` | `query` (str), `user_id` (str), optional `limit` (int, default 5) | Semantic search for memories related to the query | Status string with matched memories or error |
| `GetAllMemoryTool` | `user_id` (str), optional `limit` (int, default 100) | Retrieve all stored memories for a user | Status string listing memories or error |

All tools return success (`✅`) or failure (`❌`) strings rather than raising exceptions; agents must parse the returned status.

## Usage Patterns

### Store conversation memory

```python
from spoon_toolkits.memory.mem0.mem0_tools import AddMemoryTool

add_tool = AddMemoryTool()
result = await add_tool.execute(
    messages=[
        {"role": "user", "content": "I prefer vanilla over chocolate."},
        {"role": "assistant", "content": "Got it! I'll remember that you like vanilla."},
    ],
    user_id="user_123",
)
if not result.startswith("✅"):
    raise RuntimeError(result)
```

### Search relevant memories

```python
from spoon_toolkits.memory.mem0.mem0_tools import SearchMemoryTool

search_tool = SearchMemoryTool()
results = await search_tool.execute(
    query="What are the user's food preferences?",
    user_id="user_123",
    limit=3,
)
print(results)
```

### Retrieve all memories for a user

```python
from spoon_toolkits.memory.mem0.mem0_tools import GetAllMemoryTool

get_tool = GetAllMemoryTool()
all_memories = await get_tool.execute(user_id="user_123", limit=50)
print(all_memories)
```

## Integration with SpoonOS Chat

When building a conversational agent with persistent memory, combine Mem0 tools with the standard SpoonOS `ChatBot`:

```python
from spoon_ai.chat import ChatBot
from spoon_toolkits.memory.mem0.mem0_tools import AddMemoryTool, SearchMemoryTool

# Initialize chatbot and memory tools
llm = ChatBot(llm_provider="openai", model_name="gpt-4.1")
add_memory = AddMemoryTool()
search_memory = SearchMemoryTool()

# Store conversation after each turn
async def chat_with_memory(user_message: str, user_id: str):
    # 1. Search for relevant memories first
    context = await search_memory.execute(query=user_message, user_id=user_id)

    # 2. Generate response with context
    prompt = f"Context from memory: {context}\n\nUser: {user_message}"
    response = await llm.chat(prompt)

    # 3. Store this conversation turn
    await add_memory.execute(
        messages=[
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response},
        ],
        user_id=user_id,
    )

    return response
```

## Error Handling

- Each tool catches HTTP errors and returns `❌ Error: <description>` strings.
- Agents should use `result.startswith("✅")` to confirm success before parsing the content.
- Mem0 API rate limits and quota errors appear as standard HTTP 429 responses captured in the error message.

## Operational Notes

- The Mem0 API automatically embeds and indexes memories for semantic search; no manual vector setup is needed.
- Memories are scoped per `user_id`. Always use consistent user IDs to maintain proper conversation continuity.
- For high-volume agents, consider batching `AddMemoryTool` calls or implementing local caching to reduce API requests.
- The `messages` parameter in `AddMemoryTool` expects a list of `{"role": ..., "content": ...}` dicts, matching the OpenAI message format.

## Next Steps

- [Toolkit Index](./toolkit-index.instructions.md) - Complete toolkit overview
- [Core Concepts: Long-term Memory](../core-concepts/long-term-memory.instructions.md) - Memory architecture
