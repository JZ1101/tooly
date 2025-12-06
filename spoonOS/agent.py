"""
SpoonOS Tool Execution Agent

A specialized agent designed to execute Web3 and crypto operations based on
instructions from upper-level agents. This agent focuses on tool orchestration,
execution, and standardized response formatting.

Architecture:
    - Clean separation of tool registration and execution
    - Unified tool management interface
    - Structured error handling and logging
    - Extensible tool category system
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    """Tool categories for organization."""
    CRYPTO_DATA = "crypto_data"
    CRYPTO_POWERDATA = "crypto_powerdata"
    CRYPTO_EVM = "crypto_evm"
    CRYPTO_NEO = "crypto_neo"
    GITHUB = "github"


@dataclass
class ToolExecutionResult:
    """Standardized result format for tool execution."""
    success: bool
    tool_name: str
    category: str
    data: Any = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization."""
        return {
            "success": self.success,
            "tool_name": self.tool_name,
            "category": self.category,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata or {}
        }


class ToolRegistry:
    """
    Centralized tool registry for managing and accessing tools.
    
    Provides a clean interface for:
    - Registering tools by category
    - Looking up tools by name
    - Listing available tools
    - Managing tool lifecycle
    """

    def __init__(self):
        self._tools: Dict[str, Any] = {}
        self._categories: Dict[ToolCategory, List[str]] = {
            category: [] for category in ToolCategory
        }
        logger.info("Tool registry initialized")

    def register_tool(
        self,
        tool_name: str,
        tool_instance: Any,
        category: ToolCategory
    ) -> None:
        """
        Register a tool with the registry.
        
        Args:
            tool_name: Unique identifier for the tool
            tool_instance: The actual tool instance
            category: Tool category for organization
        """
        if tool_name in self._tools:
            logger.warning(f"Tool '{tool_name}' already registered, overwriting")
        
        self._tools[tool_name] = tool_instance
        if tool_name not in self._categories[category]:
            self._categories[category].append(tool_name)
        
        logger.info(f"Registered tool: {tool_name} in category: {category.value}")

    def get_tool(self, tool_name: str) -> Optional[Any]:
        """Get a tool instance by name."""
        return self._tools.get(tool_name)

    def list_tools(self, category: Optional[ToolCategory] = None) -> List[str]:
        """
        List all registered tools, optionally filtered by category.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of tool names
        """
        if category:
            return self._categories.get(category, [])
        return list(self._tools.keys())

    def get_tool_count(self) -> int:
        """Get total number of registered tools."""
        return len(self._tools)

    def get_categories(self) -> Dict[str, int]:
        """Get tool count by category."""
        return {
            cat.value: len(tools)
            for cat, tools in self._categories.items()
            if tools
        }


class SpoonOSAgent:
    """
    SpoonOS Tool Execution Agent
    
    Receives commands from upper-level agents and executes the requested
    tools with proper error handling and result formatting.
    
    Key Features:
    - Unified tool registration interface
    - Async tool execution with timeout support
    - Structured error handling
    - Comprehensive logging
    - Easy to extend with new tool categories
    """

    def __init__(self):
        self.registry = ToolRegistry()
        self._initialized = False
        logger.info("SpoonOS Agent created")

    async def initialize(self, tool_categories: Optional[List[ToolCategory]] = None) -> None:
        """
        Initialize the agent and register tools.
        
        Args:
            tool_categories: List of categories to initialize. If None, initializes all.
        """
        if self._initialized:
            logger.warning("Agent already initialized")
            return

        categories_to_init = tool_categories or [ToolCategory.CRYPTO_DATA]
        
        logger.info(f"Initializing agent with categories: {[c.value for c in categories_to_init]}")
        
        for category in categories_to_init:
            await self._register_category_tools(category)
        
        self._initialized = True
        logger.info(
            f"Agent initialized successfully. "
            f"Total tools: {self.registry.get_tool_count()}"
        )

    async def _register_category_tools(self, category: ToolCategory) -> None:
        """
        Register all tools for a specific category.
        
        Args:
            category: The tool category to register
        """
        try:
            if category == ToolCategory.CRYPTO_DATA:
                await self._register_crypto_data_tools()
            elif category == ToolCategory.CRYPTO_POWERDATA:
                await self._register_crypto_powerdata_tools()
            elif category == ToolCategory.CRYPTO_EVM:
                await self._register_crypto_evm_tools()
            elif category == ToolCategory.CRYPTO_NEO:
                await self._register_crypto_neo_tools()
            elif category == ToolCategory.GITHUB:
                await self._register_github_tools()
            else:
                logger.warning(f"Category {category.value} not yet implemented")
        except Exception as e:
            logger.error(f"Failed to register {category.value} tools: {str(e)}")
            raise

    async def _register_crypto_data_tools(self) -> None:
        """Register crypto data tools from spoon_toolkits."""
        try:
            from spoon_toolkits.crypto.crypto_data_tools import (
                GetTokenPriceTool,
                Get24hStatsTool,
                GetKlineDataTool,
                PriceThresholdAlertTool,
                LpRangeCheckTool,
                LendingRateMonitorTool,
                SuddenPriceIncreaseTool,
            )

            # Price tools
            self.registry.register_tool(
                "get_token_price",
                GetTokenPriceTool(),
                ToolCategory.CRYPTO_DATA
            )
            self.registry.register_tool(
                "get_24h_stats",
                Get24hStatsTool(),
                ToolCategory.CRYPTO_DATA
            )
            self.registry.register_tool(
                "get_kline_data",
                GetKlineDataTool(),
                ToolCategory.CRYPTO_DATA
            )

            # Alert tools
            self.registry.register_tool(
                "price_threshold_alert",
                PriceThresholdAlertTool(),
                ToolCategory.CRYPTO_DATA
            )
            self.registry.register_tool(
                "lp_range_check",
                LpRangeCheckTool(),
                ToolCategory.CRYPTO_DATA
            )
            self.registry.register_tool(
                "sudden_price_increase",
                SuddenPriceIncreaseTool(),
                ToolCategory.CRYPTO_DATA
            )

            # DeFi tools
            self.registry.register_tool(
                "lending_rate_monitor",
                LendingRateMonitorTool(),
                ToolCategory.CRYPTO_DATA
            )

            logger.info("Successfully registered 7 crypto data tools")

        except ImportError as e:
            logger.error(f"Failed to import crypto data tools: {str(e)}")
            logger.info("Make sure spoon_toolkits is installed: pip install spoon-toolkits")
            raise
    
    async def _register_crypto_powerdata_tools(self) -> None:
        """Register crypto PowerData tools for advanced market analysis."""
        try:
            from spoon_toolkits.crypto.crypto_powerdata.tools import (
                CryptoPowerDataCEXTool, CryptoPowerDataDEXTool,
                CryptoPowerDataIndicatorsTool
            )
            
            self.registry.register_tool("crypto_powerdata_cex", CryptoPowerDataCEXTool(), ToolCategory.CRYPTO_POWERDATA)
            self.registry.register_tool("crypto_powerdata_dex", CryptoPowerDataDEXTool(), ToolCategory.CRYPTO_POWERDATA)
            self.registry.register_tool("crypto_powerdata_indicators", CryptoPowerDataIndicatorsTool(), ToolCategory.CRYPTO_POWERDATA)
            
            logger.info("Successfully registered 3 crypto PowerData tools")
        except ImportError as e:
            logger.warning(f"Crypto PowerData tools not available: {e}")
    
    async def _register_crypto_evm_tools(self) -> None:
        """Register EVM blockchain tools."""
        try:
            from spoon_toolkits.crypto.evm import (
                EvmTransferTool, EvmErc20TransferTool, EvmBalanceTool,
                EvmSwapTool, EvmSwapQuoteTool, EvmBridgeTool
            )
            
            self.registry.register_tool("evm_transfer", EvmTransferTool(), ToolCategory.CRYPTO_EVM)
            self.registry.register_tool("evm_erc20_transfer", EvmErc20TransferTool(), ToolCategory.CRYPTO_EVM)
            self.registry.register_tool("evm_balance", EvmBalanceTool(), ToolCategory.CRYPTO_EVM)
            self.registry.register_tool("evm_swap", EvmSwapTool(), ToolCategory.CRYPTO_EVM)
            self.registry.register_tool("evm_swap_quote", EvmSwapQuoteTool(), ToolCategory.CRYPTO_EVM)
            self.registry.register_tool("evm_bridge", EvmBridgeTool(), ToolCategory.CRYPTO_EVM)
            
            logger.info("Successfully registered 6 EVM tools")
        except ImportError as e:
            logger.warning(f"EVM tools not available: {e}")
    
    async def _register_crypto_neo_tools(self) -> None:
        """Register Neo blockchain tools (sample selection)."""
        try:
            from spoon_toolkits.crypto.neo.address_tools import GetAddressInfoTool, ValidateAddressTool
            
            self.registry.register_tool("neo_address_info", GetAddressInfoTool(), ToolCategory.CRYPTO_NEO)
            self.registry.register_tool("neo_validate_address", ValidateAddressTool(), ToolCategory.CRYPTO_NEO)
            
            logger.info("Successfully registered 2 Neo tools")
        except ImportError as e:
            logger.warning(f"Neo tools not available: {e}")
    
    async def _register_github_tools(self) -> None:
        """Register GitHub analysis tools."""
        try:
            from spoon_toolkits.github.github_analysis_tool import (
                GetGitHubIssuesTool, GetGitHubPullRequestsTool, GetGitHubCommitsTool
            )
            
            self.registry.register_tool("github_issues", GetGitHubIssuesTool(), ToolCategory.GITHUB)
            self.registry.register_tool("github_pull_requests", GetGitHubPullRequestsTool(), ToolCategory.GITHUB)
            self.registry.register_tool("github_commits", GetGitHubCommitsTool(), ToolCategory.GITHUB)
            
            logger.info("Successfully registered 3 GitHub tools")
        except ImportError as e:
            logger.warning(f"GitHub tools not available: {e}")

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = 30.0
    ) -> ToolExecutionResult:
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters
            timeout: Execution timeout in seconds
            
        Returns:
            ToolExecutionResult with execution details
        """
        if not self._initialized:
            return ToolExecutionResult(
                success=False,
                tool_name=tool_name,
                category="unknown",
                error="Agent not initialized. Call initialize() first."
            )

        tool = self.registry.get_tool(tool_name)
        if not tool:
            available_tools = self.registry.list_tools()
            return ToolExecutionResult(
                success=False,
                tool_name=tool_name,
                category="unknown",
                error=f"Tool '{tool_name}' not found. Available tools: {available_tools}"
            )

        # Determine tool category
        category = "unknown"
        for cat in ToolCategory:
            if tool_name in self.registry.list_tools(cat):
                category = cat.value
                break

        logger.info(f"Executing tool: {tool_name} with parameters: {parameters}")

        try:
            # Execute tool with timeout
            result = await asyncio.wait_for(
                tool.execute(**(parameters or {})),
                timeout=timeout
            )

            # Handle different result formats
            if hasattr(result, 'output'):
                # BaseTool ToolResult format
                return ToolExecutionResult(
                    success=not hasattr(result, 'error') or result.error is None,
                    tool_name=tool_name,
                    category=category,
                    data=result.output if hasattr(result, 'output') else result,
                    error=result.error if hasattr(result, 'error') else None
                )
            else:
                # Direct result format
                return ToolExecutionResult(
                    success=True,
                    tool_name=tool_name,
                    category=category,
                    data=result
                )

        except asyncio.TimeoutError:
            error_msg = f"Tool execution timed out after {timeout} seconds"
            logger.error(f"{tool_name}: {error_msg}")
            return ToolExecutionResult(
                success=False,
                tool_name=tool_name,
                category=category,
                error=error_msg
            )

        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            logger.error(f"{tool_name}: {error_msg}", exc_info=True)
            return ToolExecutionResult(
                success=False,
                tool_name=tool_name,
                category=category,
                error=error_msg
            )

    async def execute_batch(
        self,
        commands: List[Dict[str, Any]],
        parallel: bool = False
    ) -> List[ToolExecutionResult]:
        """
        Execute multiple tool commands.
        
        Args:
            commands: List of command dicts with 'tool_name' and 'parameters'
            parallel: Whether to execute commands in parallel
            
        Returns:
            List of ToolExecutionResult
        """
        if parallel:
            tasks = [
                self.execute_tool(
                    cmd.get("tool_name"),
                    cmd.get("parameters"),
                    cmd.get("timeout", 30.0)
                )
                for cmd in commands
            ]
            return await asyncio.gather(*tasks, return_exceptions=True)
        else:
            results = []
            for cmd in commands:
                result = await self.execute_tool(
                    cmd.get("tool_name"),
                    cmd.get("parameters"),
                    cmd.get("timeout", 30.0)
                )
                results.append(result)
            return results

    def get_available_tools(self) -> Dict[str, List[str]]:
        """Get all available tools organized by category."""
        return {
            category.value: self.registry.list_tools(category)
            for category in ToolCategory
            if self.registry.list_tools(category)
        }

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dictionary with tool information or None if not found
        """
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return None

        # Find category
        category = "unknown"
        for cat in ToolCategory:
            if tool_name in self.registry.list_tools(cat):
                category = cat.value
                break

        return {
            "name": tool_name,
            "category": category,
            "description": getattr(tool, "description", "No description available"),
            "parameters": getattr(tool, "parameters", {}),
        }

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the agent.
        
        Returns:
            Dictionary with health status information
        """
        return {
            "initialized": self._initialized,
            "total_tools": self.registry.get_tool_count(),
            "tools_by_category": self.registry.get_categories(),
            "status": "healthy" if self._initialized else "not_initialized"
        }
