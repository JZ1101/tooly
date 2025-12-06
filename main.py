"""
Web3 Toolbox Agent - Main FastAPI Server
Hosts both UserAgent and SpoonOS agents
"""

import asyncio
import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager

# Import agents
from userAgent.agent import UserAgent
from userAgent.config import Config

# Global agent instances
user_agent_instance = None
spoonos_agent_instance = None  # For future implementation

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup"""
    global user_agent_instance
    
    # Initialize UserAgent
    config = Config()
    if config.ANTHROPIC_API_KEY:
        user_agent_instance = UserAgent(
            anthropic_api_key=config.ANTHROPIC_API_KEY,
            spoonos_endpoint=config.SPOON_OS_ENDPOINT
        )
        print("✅ UserAgent initialized")
    else:
        print("⚠️  UserAgent not initialized - missing ANTHROPIC_API_KEY")
    
    # TODO: Initialize SpoonOS agent when ready
    # spoonos_agent_instance = SpoonOSAgent(...)
    
    yield
    
    # Cleanup (if needed)
    pass

app = FastAPI(
    title="Web3 Toolbox Agent",
    description="AI-powered Web3 customer service with dual agent architecture",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class UserQuery(BaseModel):
    query: str
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    response: str
    success: bool
    agent: str
    session_id: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": {
            "userAgent": user_agent_instance is not None,
            "spoonOS": spoonos_agent_instance is not None
        }
    }

# UserAgent endpoints
@app.post("/api/user-agent/query", response_model=AgentResponse)
async def query_user_agent(request: UserQuery):
    """Process queries through the UserAgent (AI layer)"""
    if not user_agent_instance:
        raise HTTPException(
            status_code=503, 
            detail="UserAgent not available - check ANTHROPIC_API_KEY configuration"
        )
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session-{int(time.time()) % 10000}"
        
        response = await user_agent_instance.process_query(request.query, session_id)
        return AgentResponse(
            response=response,
            success=True,
            agent="userAgent",
            session_id=session_id
        )
    except Exception as e:
        return AgentResponse(
            response=f"Error processing query: {str(e)}",
            success=False,
            agent="userAgent",
            session_id=request.session_id
        )

# SpoonOS endpoints (placeholder for future implementation)
@app.post("/api/spoonos/execute", response_model=AgentResponse)
async def execute_spoonos_command(request: UserQuery):
    """Direct SpoonOS execution (future implementation)"""
    # TODO: Implement when SpoonOS agent is ready
    return AgentResponse(
        response="SpoonOS agent not yet implemented",
        success=False,
        agent="spoonOS",
        session_id=request.session_id
    )

# Unified endpoint that routes to appropriate agent
@app.post("/api/chat", response_model=AgentResponse)
async def unified_chat(request: UserQuery):
    """Unified chat endpoint - routes to UserAgent by default, SpoonOS for direct commands"""
    
    # Simple routing logic - expand as needed
    if request.query.strip().lower().startswith('/spoonos'):
        # Direct SpoonOS command
        return await execute_spoonos_command(request)
    else:
        # Default to UserAgent
        return await query_user_agent(request)

# Development/testing endpoints
@app.get("/api/test/user-agent")
async def test_user_agent():
    """Test UserAgent with sample queries"""
    if not user_agent_instance:
        return {"error": "UserAgent not available"}
    
    test_queries = [
        "What's my ETH balance?",
        "How much gas would a transfer cost?",
        "Show my transaction history",
        "Hello there!"
    ]
    
    results = []
    test_session_id = f"test-session-{int(time.time())}"
    
    for query in test_queries:
        try:
            response = await user_agent_instance.process_query(query, test_session_id)
            results.append({"query": query, "response": response, "success": True})
        except Exception as e:
            results.append({"query": query, "error": str(e), "success": False})
    
    return {"test_results": results, "session_id": test_session_id}

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Web3 Toolbox Agent on {host}:{port}")
    print("📡 UserAgent endpoint: /api/user-agent/query")
    print("🔧 SpoonOS endpoint: /api/spoonos/execute (coming soon)")
    print("💬 Unified chat: /api/chat")
    print("🏥 Health check: /health")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=["userAgent", "spoonOS"]
    )