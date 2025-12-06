# SpoonOS Agent

SpoonOS是一个工具执行代理,用于执行Web3操作。它接收来自上位agent的命令,调用相应的工具来完成区块链交互、数据查询等任务。

## 特性

- 🎯 **统一工具注册**: 基于枚举的分类系统,工具注册清晰明了
- 🔧 **模块化设计**: 工具按类别组织,易于扩展和维护
- ⚡ **异步执行**: 全异步架构,支持单工具和批量执行
- 🔄 **批处理模式**: 支持串行和并行批量执行
- 🛡️ **完善的错误处理**: 结构化的错误响应和超时保护
- 📊 **健康检查**: 内置健康检查和工具发现功能
- 📝 **详细日志**: 完整的操作日志记录

## 架构

```
spoonOS/
├── agent.py          # 核心代理实现
├── examples.py       # 使用示例
├── config.json       # 配置文件
└── README.md         # 本文件
```

### 核心组件

#### 1. ToolCategory (工具分类)
使用枚举定义10个工具类别:
- `CRYPTO_DATA`: 加密货币数据工具
- `CRYPTO_EVM`: EVM链交互工具
- `CRYPTO_NEO`: Neo区块链工具
- `CRYPTO_SOLANA`: Solana区块链工具
- `CRYPTO_POWERDATA`: PowerData分析工具
- `DATA_PLATFORMS`: 数据平台工具
- `GITHUB`: GitHub集成工具
- `SOCIAL_MEDIA`: 社交媒体工具
- `STORAGE`: 存储工具
- `MEMORY`: 记忆管理工具

#### 2. ToolExecutionResult (执行结果)
标准化的工具执行结果格式:
```python
@dataclass
class ToolExecutionResult:
    success: bool          # 执行是否成功
    tool_name: str        # 工具名称
    category: str         # 工具类别
    data: Any = None      # 返回数据
    error: str = None     # 错误信息
    metadata: dict = None # 元数据
```

#### 3. ToolRegistry (工具注册表)
集中管理所有工具的注册、查询和发现:
- 注册工具: `register_tool(name, tool, category)`
- 获取工具: `get_tool(name)`
- 列出工具: `list_tools(category=None)`
- 统计信息: `get_tool_count()`, `get_categories()`

#### 4. SpoonOSAgent (主代理)
核心执行代理,提供:
- 初始化: `initialize(tool_categories)`
- 单工具执行: `execute_tool(tool_name, parameters, timeout)`
- 批量执行: `execute_batch(commands, parallel)`
- 工具发现: `get_available_tools()`, `get_tool_info(tool_name)`
- 健康检查: `health_check()`

## 快速开始

### 环境配置

```bash
# 必需的环境变量
export BITQUERY_CLIENT_ID="your_client_id"
export BITQUERY_CLIENT_SECRET="your_client_secret"
export RPC_URL="https://eth.llamarpc.com"

# 可选的环境变量
export BITQUERY_API_KEY="your_api_key"
```

### 基本使用

```python
import asyncio
from agent import SpoonOSAgent, ToolCategory

async def main():
    # 创建并初始化代理
    agent = SpoonOSAgent()
    await agent.initialize(tool_categories=[ToolCategory.CRYPTO_DATA])
    
    # 执行单个工具
    result = await agent.execute_tool(
        tool_name="get_token_price",
        parameters={"symbol": "ETH-USDC"}
    )
    
    if result.success:
        print(f"Price: {result.data}")
    else:
        print(f"Error: {result.error}")

asyncio.run(main())
```

### 批量执行

```python
# 串行执行
commands = [
    {"tool_name": "get_token_price", "parameters": {"symbol": "ETH-USDC"}},
    {"tool_name": "get_24h_stats", "parameters": {"symbol": "BTC-USDT"}},
]
results = await agent.execute_batch(commands, parallel=False)

# 并行执行(提高性能)
results = await agent.execute_batch(commands, parallel=True)
```

### 与上位agent交互

```python
# 接收来自上位agent的命令
command = {
    "action": "execute_tool",
    "tool_name": "get_token_price",
    "parameters": {"symbol": "ETH-USDC"},
    "timeout": 30.0,
    "request_id": "req_12345"
}

# 执行命令
result = await agent.execute_tool(
    tool_name=command["tool_name"],
    parameters=command["parameters"],
    timeout=command["timeout"]
)

# 返回响应给上位agent
response = {
    "request_id": command["request_id"],
    "status": "success" if result.success else "error",
    "result": result.to_dict()
}
```

## 已注册工具

### Crypto Data Tools (CRYPTO_DATA)

当前已注册7个加密货币数据工具:

| 工具名称 | 功能描述 |
|---------|---------|
| `get_token_price` | 获取代币实时价格 |
| `get_24h_stats` | 获取24小时统计数据 |
| `get_kline_data` | 获取K线/蜡烛图数据用于技术分析 |
| `price_threshold_alert` | 价格阈值监控和告警 |
| `lp_range_check` | LP头寸范围检查 |
| `sudden_price_increase` | 检测价格突然上涨和潜在机会 |
| `lending_rate_monitor` | 跨平台DeFi借贷利率监控 |

## 扩展新工具

### 添加新工具类别

1. 在 `agent.py` 中添加注册方法:

```python
def _register_crypto_evm_tools(self):
    """注册EVM工具"""
    from spoon_toolkits.crypto.evm import (
        EvmTransferTool,
        EvmErc20TransferTool,
        EvmBalanceTool,
    )
    
    self.registry.register_tool(
        "evm_transfer",
        EvmTransferTool(),
        ToolCategory.CRYPTO_EVM
    )
    self.registry.register_tool(
        "evm_erc20_transfer",
        EvmErc20TransferTool(),
        ToolCategory.CRYPTO_EVM
    )
    # ... 更多工具
```

2. 在 `initialize()` 方法中调用:

```python
async def initialize(self, tool_categories: List[ToolCategory] = None):
    # ... 现有代码 ...
    elif ToolCategory.CRYPTO_EVM in categories:
        self._register_crypto_evm_tools()
```

### 工具实现规范

所有工具必须继承自 `BaseTool` 并实现 `execute()` 方法:

```python
from spoon_ai.tools.base import BaseTool

class MyCustomTool(BaseTool):
    name: str = "my_custom_tool"
    description: str = "工具描述"
    parameters: dict = {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数1"}
        },
        "required": ["param1"]
    }
    
    async def execute(self, **kwargs):
        # 工具实现逻辑
        return result
```

## 配置文件

`config.json` 提供默认配置:

```json
{
  "agent": {
    "name": "SpoonOS-Agent",
    "version": "1.0.0",
    "default_timeout": 30.0,
    "log_level": "INFO"
  },
  "tool_categories": {
    "enabled": ["CRYPTO_DATA"],
    "auto_load": true
  },
  "execution": {
    "parallel_max_workers": 5,
    "retry_attempts": 3,
    "retry_delay": 1.0
  }
}
```

## 示例

查看 `examples.py` 获取完整使用示例:

```bash
python examples.py
```

示例包括:
1. 基本工具执行
2. 批量串行执行
3. 批量并行执行
4. 工具信息查询
5. 错误处理
6. 上位agent命令模拟
7. 价格监控工作流

## 日志

代理使用Python标准日志模块,日志级别为INFO:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

日志输出示例:
```
INFO:SpoonOSAgent:Initializing SpoonOS Agent...
INFO:SpoonOSAgent:Registered 9 tools in category CRYPTO_DATA
INFO:SpoonOSAgent:Agent initialization complete
INFO:SpoonOSAgent:Executing tool: get_token_price
INFO:SpoonOSAgent:Tool get_token_price executed successfully
```

## 错误处理

所有错误都通过 `ToolExecutionResult` 结构化返回:

```python
result = await agent.execute_tool("invalid_tool", {})

if not result.success:
    print(f"Error: {result.error}")
    # Error: Tool 'invalid_tool' not found in registry
```

常见错误类型:
- 工具未找到: `Tool 'xxx' not found in registry`
- 执行超时: `Tool execution timed out after X seconds`
- 参数错误: 工具特定的参数验证错误
- 运行时错误: 捕获的异常信息

## 性能优化

### 并行执行
对于独立的工具调用,使用并行模式可以显著提高性能:

```python
# 串行: 总时间 = time1 + time2 + time3
results = await agent.execute_batch(commands, parallel=False)

# 并行: 总时间 ≈ max(time1, time2, time3)
results = await agent.execute_batch(commands, parallel=True)
```

### 超时设置
为长时间运行的工具设置合适的超时:

```python
result = await agent.execute_tool(
    tool_name="complex_analysis",
    parameters={...},
    timeout=60.0  # 60秒超时
)
```

## 健康检查

```python
health = await agent.health_check()
print(health)
# {
#   "initialized": True,
#   "total_tools": 9,
#   "categories": {
#     "CRYPTO_DATA": 9
#   }
# }
```

## 待实现功能

- [ ] 添加其他工具类别(EVM, Neo, Solana等)
- [ ] 实现工具缓存机制
- [ ] 添加工具执行重试逻辑
- [ ] 实现工具依赖关系管理
- [ ] 添加工具性能监控
- [ ] 实现工具热加载
- [ ] 添加工具版本管理

## License

MIT

## 贡献

欢迎提交PR来添加新的工具或改进现有功能!

## 相关文档

- [Toolkit 文档](../.github/instructions/) - 工具详细说明
- [SpoonAI 框架](https://github.com/XSpoonAi/spoon-core) - 核心框架文档
