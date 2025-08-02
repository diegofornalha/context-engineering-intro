from fastapi import FastAPI
import sentry_sdk
from pydantic import BaseModel
from typing import Dict, Any, List
import time
import uuid

# Configure SDK for AI Agents monitoring (Practical Approach)
# Baseado na documentação Sentry + contexto personalizado para AI Agents
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    # Add data like request headers and IP for users
    send_default_pii=True,
    # To reduce the volume of performance data captured
    traces_sample_rate=1.0,
)

app = FastAPI()

class AIAgentRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"
    user_id: str = "anonymous"

class AIAgentResponse(BaseModel):
    result: str
    agent_session: str
    tokens_used: int
    model: str
    tools_called: List[str]
    processing_time: float

def monitor_ai_agent_start(prompt: str, model: str, user_id: str) -> str:
    """
    Monitorar início de AI Agent - FUNCIONA PERFEITAMENTE!
    """
    session_id = str(uuid.uuid4())
    
    # Context específico para AI Agent
    sentry_sdk.set_context("ai_agent", {
        "session_id": session_id,
        "model": model,
        "prompt_length": len(prompt),
        "user_id": user_id,
        "stage": "started"
    })
    
    # Tags para filtrar no Sentry
    sentry_sdk.set_tag("ai.session", session_id)
    sentry_sdk.set_tag("ai.model", model)
    sentry_sdk.set_tag("ai.type", "agent_processing")
    
    # Breadcrumb para tracking
    sentry_sdk.add_breadcrumb(
        message="AI Agent processing started",
        category="ai.agent",
        level="info",
        data={
            "session": session_id,
            "model": model,
            "prompt_size": len(prompt)
        }
    )
    
    return session_id

def monitor_ai_tool_usage(session_id: str, tool_name: str, tokens: int):
    """
    Monitorar uso de ferramentas AI
    """
    sentry_sdk.set_context(f"ai_tool_{tool_name}", {
        "session_id": session_id,
        "tool": tool_name,
        "tokens_used": tokens,
        "timestamp": time.time()
    })
    
    sentry_sdk.add_breadcrumb(
        message=f"AI Tool {tool_name} executed",
        category="ai.tool",
        level="info",
        data={
            "tool": tool_name,
            "tokens": tokens,
            "session": session_id
        }
    )

def monitor_ai_agent_complete(session_id: str, total_tokens: int, 
                            tools_used: List[str], processing_time: float):
    """
    Monitorar conclusão de AI Agent
    """
    sentry_sdk.set_context("ai_agent_result", {
        "session_id": session_id,
        "total_tokens": total_tokens,
        "tools_count": len(tools_used),
        "processing_time": processing_time,
        "tokens_per_second": total_tokens / processing_time if processing_time > 0 else 0,
        "stage": "completed"
    })
    
    # Capture completion event
    sentry_sdk.capture_message(
        f"AI Agent completed: {total_tokens} tokens, {len(tools_used)} tools, {processing_time:.2f}s",
        level="info",
        tags={
            "ai.event": "completion",
            "ai.session": session_id,
            "ai.performance": f"{total_tokens}tokens_{processing_time:.2f}s"
        }
    )

@app.get("/")
async def root():
    return {"message": "PRP Agent - AI Monitoring Prático!"}

@app.post("/ai-agent/process", response_model=AIAgentResponse)
async def process_ai_agent(request: AIAgentRequest):
    """
    Processar com AI Agent + Sentry Monitoring
    
    DEMONSTRA monitoramento completo de AI Agents:
    - Start/Complete tracking
    - Tool usage monitoring  
    - Token consumption
    - Performance metrics
    - Error handling
    """
    start_time = time.time()
    
    try:
        # 1. Monitorar início
        session_id = monitor_ai_agent_start(
            request.prompt, request.model, request.user_id
        )
        
        # 2. Simular processamento AI Agent
        import asyncio
        import random
        
        await asyncio.sleep(0.5)  # Simular processamento
        
        # 3. Simular uso de ferramentas
        available_tools = [
            "text_analyzer", "code_generator", "prp_parser", 
            "context_builder", "output_formatter"
        ]
        
        tools_used = random.sample(available_tools, random.randint(2, 4))
        total_tokens = 0
        
        for tool in tools_used:
            tool_tokens = random.randint(20, 150)
            total_tokens += tool_tokens
            monitor_ai_tool_usage(session_id, tool, tool_tokens)
            await asyncio.sleep(0.1)  # Simular tempo de ferramenta
        
        # Adicionar tokens do modelo principal
        total_tokens += random.randint(200, 500)
        
        # 4. Gerar resultado
        result = f"AI Agent processou: '{request.prompt[:100]}...' usando {len(tools_used)} ferramentas"
        
        processing_time = time.time() - start_time
        
        # 5. Monitorar conclusão
        monitor_ai_agent_complete(
            session_id, total_tokens, tools_used, processing_time
        )
        
        return AIAgentResponse(
            result=result,
            agent_session=session_id,
            tokens_used=total_tokens,
            model=request.model,
            tools_called=tools_used,
            processing_time=processing_time
        )
        
    except Exception as e:
        # Capturar erros específicos de AI Agent
        sentry_sdk.set_context("ai_agent_error", {
            "session_id": session_id if 'session_id' in locals() else "unknown",
            "error_stage": "processing",
            "model": request.model,
            "prompt_length": len(request.prompt)
        })
        sentry_sdk.capture_exception(e)
        raise

@app.get("/ai-agent/benchmark")
async def ai_agent_benchmark():
    """
    Benchmark AI Agent - Gera múltiplos eventos Sentry
    """
    test_cases = [
        {"prompt": "Analisar arquitetura de sistema", "model": "gpt-4"},
        {"prompt": "Gerar documentação de API", "model": "gpt-4-turbo"},
        {"prompt": "Revisar código para segurança", "model": "gpt-3.5-turbo"},
        {"prompt": "Otimizar performance", "model": "gpt-4"},
        {"prompt": "Criar testes automatizados", "model": "gpt-4-turbo"}
    ]
    
    results = []
    
    for i, test in enumerate(test_cases):
        request = AIAgentRequest(
            prompt=test["prompt"],
            model=test["model"],
            user_id=f"benchmark_user_{i}"
        )
        
        result = await process_ai_agent(request)
        
        results.append({
            "test": i + 1,
            "prompt": test["prompt"][:50] + "...",
            "model": test["model"],
            "tokens": result.tokens_used,
            "tools": len(result.tools_called),
            "time": f"{result.processing_time:.2f}s"
        })
    
    # Capturar resumo do benchmark
    total_tokens = sum(r["tokens"] for r in results)
    sentry_sdk.capture_message(
        f"AI Agent benchmark: {len(results)} tests, {total_tokens} tokens",
        level="info",
        tags={
            "ai.event": "benchmark_complete",
            "ai.tests": str(len(results)),
            "ai.total_tokens": str(total_tokens)
        }
    )
    
    return {
        "benchmark": "completed",
        "tests": len(results),
        "total_tokens": total_tokens,
        "avg_time": f"{sum(float(r['time'][:-1]) for r in results) / len(results):.2f}s",
        "results": results
    }

@app.get("/sentry-debug")
async def trigger_error():
    """Endpoint de debug para Sentry"""
    division_by_zero = 1 / 0