from fastapi import FastAPI, HTTPException
import sentry_sdk
from pydantic import BaseModel
import time
import uuid
import random

# ✅ RELEASE HEALTH CONFIGURATION COMPLETA
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,
    
    # RELEASE HEALTH - Configuração oficial
    release="prp-agent@1.0.0",     # Release version tracking
    environment="production",      # Environment for Release Health
    auto_session_tracking=True     # Automatic session management
)

app = FastAPI(
    title="PRP Agent - Release Health Demo",
    version="1.0.0"
)

class ReleaseHealthDemo(BaseModel):
    user_id: str = "demo_user"
    action: str = "process_ai_agent"

@app.get("/")
async def root():
    return {
        "app": "PRP Agent - Release Health Demo",
        "version": "1.0.0", 
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "features": [
            "✅ Auto Session Tracking",
            "✅ Crash Detection", 
            "✅ Error Tracking",
            "✅ Adoption Metrics",
            "✅ Performance Monitoring"
        ],
        "session_modes": [
            "Server-mode (each request = session)",
            "Automatic session management",
            "Crash-free sessions tracking"
        ]
    }

@app.get("/release/health")
async def release_health_status():
    """
    Release Health Status - Demonstração completa
    
    Retorna métricas de saúde da release prp-agent@1.0.0
    conforme documentação oficial Sentry Release Health
    """
    
    # Capture message for Release Health tracking
    sentry_sdk.capture_message(
        "Release Health status requested",
        level="info", 
        extra={
            "release": "prp-agent@1.0.0",
            "environment": "production",
            "feature": "release_health_demo"
        }
    )
    
    return {
        "release_info": {
            "version": "prp-agent@1.0.0",
            "environment": "production",
            "status": "healthy"
        },
        "session_tracking": {
            "mode": "server-mode/request-mode",
            "auto_tracking": True,
            "session_per_request": True
        },
        "health_metrics": {
            "crash_free_sessions": "100%",
            "crash_free_users": "100%", 
            "error_rate": "0%",
            "adoption_stage": "adopted"
        },
        "session_status_types": {
            "healthy": "Session ended normally, no errors",
            "errored": "Session had handled errors",
            "crashed": "Session ended with unhandled error", 
            "abnormal": "Session timed out or was forced to quit"
        },
        "features_active": [
            "Auto session tracking",
            "Crash detection",
            "Release adoption metrics",
            "Error rate monitoring"
        ]
    }

@app.post("/demo/healthy-session")
async def demo_healthy_session(request: ReleaseHealthDemo):
    """
    Demo: Session saudável (Healthy)
    
    Demonstra uma sessão que termina normalmente sem erros.
    """
    session_id = str(uuid.uuid4())
    
    # Manual session start for detailed tracking
    sentry_sdk.start_session(
        distinctId=request.user_id,
        release="prp-agent@1.0.0",
        environment="production"
    )
    
    # Simulate successful AI Agent processing
    start_time = time.time()
    time.sleep(random.uniform(0.2, 0.5))  # Simulate processing
    processing_time = time.time() - start_time
    
    # Successful completion - end session as "exited" (healthy)
    sentry_sdk.end_session(status="exited")
    
    sentry_sdk.capture_message(
        f"Healthy session completed: {session_id}",
        level="info",
        extra={
            "session_id": session_id,
            "user_id": request.user_id,
            "processing_time": processing_time,
            "session_status": "healthy"
        }
    )
    
    return {
        "session_id": session_id,
        "status": "healthy",
        "result": "Session completed successfully",
        "processing_time": processing_time,
        "release": "prp-agent@1.0.0",
        "impact_on_release_health": "Contributes to crash-free sessions percentage"
    }

@app.post("/demo/errored-session")  
async def demo_errored_session(request: ReleaseHealthDemo):
    """
    Demo: Session com erro (Errored)
    
    Demonstra uma sessão que teve erros tratados mas não crashed.
    """
    session_id = str(uuid.uuid4())
    
    sentry_sdk.start_session(
        distinctId=request.user_id,
        release="prp-agent@1.0.0",
        environment="production"
    )
    
    try:
        # Simulate handled error
        if random.choice([True, False]):
            raise ValueError("Simulated handled error for Release Health demo")
    except ValueError as e:
        # End session as errored (handled error)
        sentry_sdk.end_session(status="errored")
        sentry_sdk.capture_exception(e)
        
        return {
            "session_id": session_id,
            "status": "errored",
            "result": "Session completed with handled errors",
            "error": str(e),
            "release": "prp-agent@1.0.0",
            "impact_on_release_health": "Counted as errored session (not crashed)"
        }

@app.post("/demo/crashed-session")
async def demo_crashed_session(request: ReleaseHealthDemo):
    """
    Demo: Session crashed (Crashed)
    
    Demonstra uma sessão que terminou com erro não tratado.
    ⚠️ Impacta negativamente as métricas de Release Health.
    """
    session_id = str(uuid.uuid4())
    
    sentry_sdk.start_session(
        distinctId=request.user_id,
        release="prp-agent@1.0.0",
        environment="production"
    )
    
    try:
        # Simulate a crash
        division_by_zero = 1 / 0
    except Exception as e:
        # End session as crashed
        sentry_sdk.end_session(status="crashed")
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=500, 
            detail={
                "session_id": session_id,
                "status": "crashed",
                "error": "Division by zero - unhandled crash",
                "release": "prp-agent@1.0.0",
                "impact_on_release_health": "⚠️ Reduces crash-free sessions percentage"
            }
        )

@app.get("/demo/adoption-metrics")
async def demo_adoption_metrics():
    """
    Demo: Release Adoption Metrics
    
    Simula métricas de adoção de release conforme documentação.
    """
    
    sentry_sdk.capture_message(
        "Release adoption metrics requested",
        level="info",
        extra={
            "release": "prp-agent@1.0.0",
            "environment": "production",
            "metrics_type": "adoption"
        }
    )
    
    return {
        "release": "prp-agent@1.0.0",
        "adoption_metrics": {
            "session_adoption": "85%",
            "user_adoption": "75%", 
            "adoption_stage": "Adopted",
            "last_24h_sessions": 1250,
            "last_24h_users": 320
        },
        "adoption_stages": {
            "adopted": "Release seen in 10%+ of sessions",
            "low_adoption": "Release seen in <10% of sessions",
            "replaced": "Previously adopted but now below threshold"
        },
        "comparison": {
            "previous_release": "prp-agent@0.9.0",
            "adoption_trend": "⬆️ Increasing",
            "sessions_growth": "+15%"
        }
    }

@app.get("/demo/session-summary")
async def demo_session_summary():
    """
    Demo: Resumo completo de sessions para Release Health
    """
    
    return {
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "session_summary": {
            "total_sessions_today": 1250,
            "healthy_sessions": 1200,
            "errored_sessions": 45, 
            "crashed_sessions": 5,
            "abnormal_sessions": 0
        },
        "health_percentages": {
            "crash_free_sessions": "99.6%",
            "error_free_sessions": "96.0%",
            "healthy_sessions": "96.0%"
        },
        "user_metrics": {
            "total_users_today": 320,
            "crash_free_users": "99.7%",
            "users_with_errors": 15,
            "users_with_crashes": 1
        },
        "performance": {
            "avg_session_duration": "0.45s",
            "p95_session_duration": "0.8s",
            "requests_per_second": 14.5
        }
    }