from fastapi import FastAPI, Request, HTTPException
import sentry_sdk
from pydantic import BaseModel
from typing import Dict, Any, List
import time
import uuid
import json
import random

# Configure SDK with Release Health
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,
    
    # ✅ RELEASE HEALTH CONFIGURATION
    release="prp-agent@1.0.0",
    environment="production",
    auto_session_tracking=True
)

app = FastAPI(title="PRP Agent - Release Health", version="1.0.0")

class ReleaseHealthRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    agent_name: str = "PRP Assistant"
    user_id: str = "anonymous"

class ReleaseHealthResponse(BaseModel):
    result: str
    session_id: str
    release_version: str
    session_status: str
    processing_time: float
    total_tokens: int
    health_metrics: Dict[str, Any]

@app.middleware("http")
async def release_health_middleware(request: Request, call_next):
    """Middleware for Release Health tracking"""
    start_time = time.time()
    
    # Set release context
    sentry_sdk.set_context("release_health", {
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "request_path": request.url.path,
        "method": request.method
    })
    
    try:
        response = await call_next(request)
        
        # Track successful sessions
        if request.url.path.startswith("/ai-agent/"):
            sentry_sdk.capture_message(
                f"Session completed successfully: {request.url.path}",
                level="info",
                extra={
                    "release": "prp-agent@1.0.0",
                    "session_status": "healthy",
                    "processing_time": time.time() - start_time
                }
            )
        
        return response
        
    except Exception as e:
        # Track crashed sessions
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message(
            f"Session crashed: {request.url.path}",
            level="error",
            extra={
                "release": "prp-agent@1.0.0",
                "session_status": "crashed",
                "error": str(e)
            }
        )
        raise

def ai_agent_with_release_health(agent_name: str, model: str, prompt: str, user_id: str):
    """AI Agent processing with Release Health tracking"""
    session_id = str(uuid.uuid4())
    
    # Start session tracking
    sentry_sdk.start_session(
        distinctId=user_id,
        release="prp-agent@1.0.0",
        environment="production"
    )
    
    # Set session context
    sentry_sdk.set_context("ai_session", {
        "session_id": session_id,
        "agent_name": agent_name,
        "model": model,
        "user_id": user_id,
        "release": "prp-agent@1.0.0"
    })
    
    with sentry_sdk.start_span(
        op="gen_ai.invoke_agent",
        name=f"invoke_agent {agent_name}",
    ) as span:
        
        span.set_data("gen_ai.system", "openai")
        span.set_data("gen_ai.request.model", model)
        span.set_data("gen_ai.operation.name", "invoke_agent")
        span.set_data("gen_ai.agent.name", agent_name)
        span.set_data("release.version", "prp-agent@1.0.0")
        
        start_time = time.time()
        
        with sentry_sdk.start_span(
            op="gen_ai.chat",
            name=f"chat {model}",
        ) as chat_span:
            
            chat_span.set_data("gen_ai.system", "openai")
            chat_span.set_data("gen_ai.request.model", model)
            chat_span.set_data("gen_ai.operation.name", "chat")
            
            # Simulate processing
            time.sleep(random.uniform(0.3, 0.7))
            
            # Simulate tokens
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = random.randint(150, 400)
            total_tokens = int(input_tokens + output_tokens)
            
            processing_time = time.time() - start_time
            
            chat_span.set_data("gen_ai.usage.input_tokens", int(input_tokens))
            chat_span.set_data("gen_ai.usage.output_tokens", output_tokens)
            chat_span.set_data("gen_ai.usage.total_tokens", total_tokens)
            
            response = f"Processed: '{prompt[:100]}...' with Release Health v1.0.0"
            
            # End session as successful
            sentry_sdk.end_session(status="exited")
            
            return {
                "response": response,
                "session_id": session_id,
                "total_tokens": total_tokens,
                "processing_time": processing_time,
                "session_status": "healthy"
            }

@app.get("/")
async def root():
    return {
        "app": "PRP Agent - Release Health",
        "version": "1.0.0",
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "features": ["AI Agents", "Release Health", "Session Tracking"]
    }

@app.post("/ai-agent/release-health", response_model=ReleaseHealthResponse)
async def process_with_release_health(request: ReleaseHealthRequest):
    """AI Agent processing with Release Health monitoring"""
    
    try:
        result = ai_agent_with_release_health(
            agent_name=request.agent_name,
            model=request.model,
            prompt=request.prompt,
            user_id=request.user_id
        )
        
        health_metrics = {
            "release_version": "prp-agent@1.0.0",
            "environment": "production",
            "session_duration": result["processing_time"],
            "tokens_per_second": result["total_tokens"] / result["processing_time"] if result["processing_time"] > 0 else 0,
            "status": "healthy"
        }
        
        return ReleaseHealthResponse(
            result=result["response"],
            session_id=result["session_id"],
            release_version="prp-agent@1.0.0",
            session_status="healthy",
            processing_time=result["processing_time"],
            total_tokens=result["total_tokens"],
            health_metrics=health_metrics
        )
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.end_session(status="crashed")
        raise HTTPException(status_code=500, detail=f"AI Agent processing failed: {str(e)}")

@app.get("/release/health-status")
async def get_health_status():
    """Get current release health status"""
    
    sentry_sdk.capture_message(
        "Release Health status check",
        level="info",
        extra={
            "release": "prp-agent@1.0.0",
            "environment": "production",
            "status": "healthy"
        }
    )
    
    return {
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "status": "healthy",
        "features": {
            "session_tracking": True,
            "crash_detection": True,
            "adoption_metrics": True,
            "auto_session_tracking": True
        },
        "metrics": {
            "crash_free_sessions": "100%",
            "error_rate": "0%",
            "adoption_stage": "adopted"
        }
    }

@app.get("/release/crash-test")
async def crash_test():
    """Test crash detection for Release Health"""
    sentry_sdk.start_session(
        distinctId="crash_test_user",
        release="prp-agent@1.0.0"
    )
    
    try:
        division_by_zero = 1 / 0
    except Exception as e:
        sentry_sdk.end_session(status="crashed")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Intentional crash for Release Health testing")

@app.get("/release/error-test")
async def error_test():
    """Test error tracking for Release Health"""
    sentry_sdk.start_session(
        distinctId="error_test_user",
        release="prp-agent@1.0.0"
    )
    
    try:
        raise ValueError("Intentional error for Release Health testing")
    except ValueError as e:
        sentry_sdk.end_session(status="errored")
        sentry_sdk.capture_exception(e)
        
        return {
            "status": "error_handled",
            "message": "Error tracked in Release Health",
            "release": "prp-agent@1.0.0",
            "session_status": "errored"
        }