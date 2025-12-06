"""Configuration for UserAgent"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for UserAgent"""
    
    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # spoonOS Integration (placeholders)
    SPOON_OS_ENDPOINT: str = os.getenv("SPOON_OS_ENDPOINT", "http://localhost:8000")
    SPOON_OS_API_KEY: str = os.getenv("SPOON_OS_API_KEY", "")
    
    # Agent Settings
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    MAX_ITERATIONS: int = 3
    TEMPERATURE: float = 0.1
    
    # Web3 Settings (for future spoonOS integration)
    ETHEREUM_RPC_URL: str = os.getenv("ETHEREUM_RPC_URL", "")
    POLYGON_RPC_URL: str = os.getenv("POLYGON_RPC_URL", "")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required")
        return True
    
    @classmethod
    def get_env_template(cls) -> str:
        """Get .env file template"""
        return """
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# spoonOS Integration (when ready)
SPOON_OS_ENDPOINT=http://localhost:8000
SPOON_OS_API_KEY=your_spoon_os_api_key

# Web3 RPC URLs (for spoonOS)
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your_infura_key
POLYGON_RPC_URL=https://polygon-mainnet.infura.io/v3/your_infura_key
"""