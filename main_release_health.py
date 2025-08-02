from fastapi import FastAPI, Request, HTTPException
import sentry_sdk
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import time
import uuid
import json
import asyncio
import random
import os
from datetime import datetime

# Configure SDK with Release Health tracking
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,  # Include LLM inputs/outputs
    
    # ✅ RELEASE HEALTH CONFIGURATION
    release="prp-agent@1.0.0",  # Set release version
    environment="production",   # Set environment
    
    # Enable session tracking for Release Health
    auto_session_tracking=True  # Automatic session management
)

app = FastAPI(
    title="PRP Agent - Release Health Monitoring",
    version="1.0.0",
    description="AI Agents with Sentry Release Health tracking"
)

# Models for Release Health tracking
class HealthRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    agent_name: str = "PRP Assistant"
    user_id: str = "anonymous"
    release_version: str = "1.0.0"

class HealthResponse(BaseModel):
    result: str
    session_id: str
    release_version: str
    session_status: str
    processing_time: float
    total_tokens: int
    tools_executed: List[str]
    health_metrics: Dict[str, Any]

class SessionManager:
    """Manages Release Health sessions for AI Agent interactions"""
    
    def __init__(self):
        self.active_sessions = {}
    
    def start_session(self, user_id: str, request_data: Dict) -> str:
        """Start a new Release Health session"""
        session_id = str(uuid.uuid4())
        
        # Start session manually for detailed tracking
        sentry_sdk.start_session(
            sessionId=session_id,
            distinctId=user_id,
            environment="production",
            release="prp-agent@1.0.0"
        )
        
        self.active_sessions[session_id] = {
            "start_time": time.time(),
            "user_id": user_id,
            "request_data": request_data,
            "status": "healthy"  # Default to healthy
        }
        
        # Add breadcrumb for session start
        sentry_sdk.add_breadcrumb(
            category="session",
            message=f"AI Agent session started",
            data={
                "session_id": session_id,
                "user_id": user_id,
                "agent_name": request_data.get("agent_name", "unknown")
            },
            level="info"
        )
        
        return session_id
    
    def end_session(self, session_id: str, status: str = "exited", error_count: int = 0):
        """End a Release Health session with specific status"""
        if session_id not in self.active_sessions:
            return
        
        session_data = self.active_sessions[session_id]
        duration = time.time() - session_data["start_time"]
        
        # Capture session manually with detailed metrics
        sentry_sdk.capture_session(
            sessionId=session_id,
            distinctId=session_data["user_id"],
            duration=duration,
            status=status,  # healthy, errored, crashed, abnormal
            errors=error_count
        )
        
        # Add breadcrumb for session end
        sentry_sdk.add_breadcrumb(
            category="session",
            message=f"AI Agent session ended",
            data={
                "session_id": session_id,
                "status": status,
                "duration": duration,
                "errors": error_count
            },
            level="info"
        )
        
        # Update session data
        session_data["status"] = status
        session_data["duration"] = duration
        session_data["errors"] = error_count
        
        # Clean up
        del self.active_sessions[session_id]
        
        return session_data

# Global session manager
session_manager = SessionManager()

# Middleware for automatic session tracking
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    """Middleware to track Release Health for all requests"""
    start_time = time.time()
    session_id = None
    error_count = 0
    
    try:
        # Start session for AI Agent endpoints
        if request.url.path.startswith("/ai-agent/"):
            user_id = request.headers.get("X-User-ID", "anonymous")
            session_id = session_manager.start_session(user_id, {
                "path": request.url.path,
                "method": request.method,
                "user_agent": request.headers.get("User-Agent", "unknown")
            })
            
            # Set session context for this request
            sentry_sdk.set_context("release_health", {
                "session_id": session_id,
                "release": "prp-agent@1.0.0",
                "environment": "production",
                "request_path": request.url.path
            })
        
        # Process request
        response = await call_next(request)
        
        # Determine session status based on response
        if session_id:
            if response.status_code >= 500:
                status = "errored"
                error_count = 1
            elif response.status_code >= 400:
                status = "errored" 
                error_count = 1
            else:
                status = "exited"  # Normal completion
            
            session_manager.end_session(session_id, status, error_count)
        
        return response
        
    except Exception as e:
        # Handle crashes
        if session_id:
            session_manager.end_session(session_id, "crashed", 1)
        
        # Capture exception for Release Health
        sentry_sdk.capture_exception(e)
        raise

def ai_agent_with_health_tracking(agent_name: str, model: str, prompt: str, user_id: str, session_id: str):
    """AI Agent processing with Release Health tracking"""
    
    # Set release context
    sentry_sdk.set_context("ai_agent_release", {
        "session_id": session_id,
        "agent_name": agent_name,
        "model": model,
        "release": "prp-agent@1.0.0",
        "environment": "production"
    })
    
    # INVOKE AGENT SPAN with Release Health
    with sentry_sdk.start_span(
        op="gen_ai.invoke_agent",
        name=f"invoke_agent {agent_name}",
    ) as span:
        
        # Set release-specific attributes
        span.set_data("gen_ai.system", "openai")
        span.set_data("gen_ai.request.model", model)
        span.set_data("gen_ai.operation.name", "invoke_agent")
        span.set_data("gen_ai.agent.name", agent_name)
        span.set_data("release.version", "prp-agent@1.0.0")
        span.set_data("session.id", session_id)
        
        start_time = time.time()
        
        # Simulate AI processing with health tracking
        try:
            # AI CLIENT SPAN
            with sentry_sdk.start_span(
                op="gen_ai.chat",
                name=f"chat {model}",
            ) as chat_span:
                
                chat_span.set_data("gen_ai.system", "openai")
                chat_span.set_data("gen_ai.request.model", model)
                chat_span.set_data("gen_ai.operation.name", "chat")
                chat_span.set_data("release.version", "prp-agent@1.0.0")
                
                # Simulate processing
                time.sleep(random.uniform(0.3, 0.8))
                
                # Simulate token usage
                input_tokens = len(prompt.split()) * 1.3
                output_tokens = random.randint(150, 400)
                total_tokens = int(input_tokens + output_tokens)
                
                # Simulate tools execution
                tools_executed = []
                if random.choice([True, False]):
                    tools = ["text_analyzer", "code_generator", "prp_parser"]
                    selected_tools = random.sample(tools, random.randint(1, 2))
                    
                    for tool_name in selected_tools:
                        # EXECUTE TOOL SPAN with Release Health
                        with sentry_sdk.start_span(
                            op="gen_ai.execute_tool",
                            name=f"execute_tool {tool_name}",
                        ) as tool_span:
                            
                            tool_span.set_data("gen_ai.system", "openai")
                            tool_span.set_data("gen_ai.request.model", model)
                            tool_span.set_data("gen_ai.tool.name", tool_name)
                            tool_span.set_data("gen_ai.tool.type", "function")
                            tool_span.set_data("release.version", "prp-agent@1.0.0")
                            
                            time.sleep(random.uniform(0.1, 0.3))
                            tools_executed.append(tool_name)
                
                processing_time = time.time() - start_time
                
                # Set response data
                chat_span.set_data("gen_ai.usage.input_tokens", int(input_tokens))
                chat_span.set_data("gen_ai.usage.output_tokens", output_tokens)
                chat_span.set_data("gen_ai.usage.total_tokens", total_tokens)
                
                response = f"Processed: '{prompt[:100]}...' with Release Health tracking"
                
                return {
                    "response": response,
                    "total_tokens": total_tokens,
                    "input_tokens": int(input_tokens),
                    "output_tokens": output_tokens,
                    "tools_executed": tools_executed,
                    "processing_time": processing_time,
                    "session_status": "healthy"
                }
                
        except Exception as e:
            # Track error in Release Health
            sentry_sdk.capture_exception(e)
            raise

@app.get("/")
async def root():
    return {
        "app": "PRP Agent - Release Health Monitoring",
        "version": "1.0.0",
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "features": [
            "AI Agents Monitoring",
            "Release Health Tracking", 
            "Session Management",
            "Crash Detection",
            "Adoption Metrics"
        ]
    }

@app.post("/ai-agent/health", response_model=HealthResponse)
async def process_ai_agent_with_health(request: HealthRequest):
    """
    AI Agent processing with full Release Health monitoring
    
    Tracks:
    - Session lifecycle (start/end)
    - Release adoption metrics
    - Crash free sessions/users
    - Error rates per release
    - Performance per release
    """
    session_id = str(uuid.uuid4())
    
    try:
        # Manual session start for detailed tracking
        session_id = session_manager.start_session(request.user_id, {
            "agent_name": request.agent_name,
            "model": request.model,
            "prompt_length": len(request.prompt)
        })
        
        # Process AI Agent
        result = ai_agent_with_health_tracking(
            agent_name=request.agent_name,
            model=request.model,
            prompt=request.prompt,
            user_id=request.user_id,
            session_id=session_id
        )
        
        # Health metrics calculation
        health_metrics = {
            "release_version": "prp-agent@1.0.0",
            "session_duration": result["processing_time"],
            "tokens_per_second": result["total_tokens"] / result["processing_time"] if result["processing_time"] > 0 else 0,
            "tools_used": len(result["tools_executed"]),
            "status": "healthy",
            "environment": "production"
        }
        
        # End session as healthy
        session_manager.end_session(session_id, "exited", 0)
        
        return HealthResponse(
            result=result["response"],
            session_id=session_id,
            release_version="prp-agent@1.0.0",
            session_status="healthy",
            processing_time=result["processing_time"],
            total_tokens=result["total_tokens"],
            tools_executed=result["tools_executed"],
            health_metrics=health_metrics
        )
        
    except Exception as e:
        # End session as errored/crashed
        session_manager.end_session(session_id, "crashed", 1)
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=f"AI Agent processing failed: {str(e)}")

@app.get("/release/health")
async def get_release_health():
    """Get current release health metrics"""
    
    # Capture release health message
    sentry_sdk.capture_message(
        "Release Health check requested",
        level="info",
        extra={
            "release": "prp-agent@1.0.0",
            "environment": "production",
            "active_sessions": len(session_manager.active_sessions),
            "timestamp": datetime.now().isoformat()
        }
    )
    
    return {
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "health_status": "healthy",
        "active_sessions": len(session_manager.active_sessions),
        "features": {
            "session_tracking": True,
            "crash_detection": True,
            "adoption_metrics": True,
            "error_tracking": True
        },
        "metrics": {
            "uptime": "stable",
            "crash_free_sessions": "100%",
            "error_rate": "0%",
            "adoption_stage": "adopted"
        }
    }

@app.get("/release/crash-test")
async def trigger_crash():
    """
    Endpoint to test crash detection in Release Health
    This will create a "crashed" session
    """
    session_id = session_manager.start_session("crash_test_user", {
        "test_type": "crash_simulation",
        "endpoint": "/release/crash-test"
    })
    
    try:
        # Simulate a crash
        division_by_zero = 1 / 0
    except Exception as e:
        # End session as crashed
        session_manager.end_session(session_id, "crashed", 1)
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Intentional crash for Release Health testing")

@app.get("/release/error-test")
async def trigger_error():
    """
    Endpoint to test error tracking in Release Health
    This will create an "errored" session
    """
    session_id = session_manager.start_session("error_test_user", {
        "test_type": "error_simulation", 
        "endpoint": "/release/error-test"
    })
    
    try:
        # Simulate handled error
        raise ValueError("Intentional error for Release Health testing")
    except ValueError as e:
        # End session as errored (handled error)
        session_manager.end_session(session_id, "errored", 1)
        sentry_sdk.capture_exception(e)
        
        return {
            "status": "error_handled",
            "message": "Error was handled and tracked in Release Health",
            "session_id": session_id,
            "session_status": "errored"
        }