#!/usr/bin/env python3
"""
🤖 PRP Agent - FastAPI + Sentry Integration
=============================================

Aplicação principal do PRP Agent com monitoramento Sentry
e integração PydanticAI para processamento de PRPs.

Baseado na documentação oficial do Sentry para FastAPI:
https://docs.sentry.io/platforms/python/integrations/fastapi/
"""

import os
import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from loguru import logger
from typing import Dict, Any

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Sentry ANTES da inicialização do FastAPI
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
    release=os.getenv("SENTRY_RELEASE", "prp-agent@1.0.0"),
    # Capturar dados do usuário (headers, IP, etc.)
    send_default_pii=os.getenv("SEND_DEFAULT_PII", "true").lower() == "true",
    # Taxa de amostragem para performance (0.0 a 1.0)
    traces_sample_rate=float(os.getenv("TRACES_SAMPLE_RATE", "0.1")),
    # Habilitar monitoramento de AI Agents (Beta)
    enable_ai_analytics=os.getenv("ENABLE_AI_MONITORING", "true").lower() == "true",
)

# Inicializar FastAPI
app = FastAPI(
    title=os.getenv("APP_NAME", "PRP Agent"),
    description="AI Agent para processamento de Product Requirement Prompts",
    version=os.getenv("APP_VERSION", "1.0.0"),
    debug=os.getenv("DEBUG", "true").lower() == "true"
)

# Modelos Pydantic
class PRPRequest(BaseModel):
    prompt: str
    context: str = ""
    user_id: str = "anonymous"

class PRPResponse(BaseModel):
    result: str
    status: str
    metadata: Dict[str, Any]

# Middleware para logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📥 Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response: {response.status_code}")
    return response

# Rotas da aplicação
@app.get("/")
async def root():
    """Rota principal com informações do sistema"""
    return {
        "app": "PRP Agent",
        "status": "✅ Online",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "sentry": "🔍 Monitoramento ativo",
        "ai_monitoring": "🤖 Beta habilitado"
    }

@app.get("/health")
async def health_check():
    """Health check para monitoramento"""
    return {"status": "healthy", "timestamp": "2025-01-18T14:34:09.851Z"}

@app.post("/prp/process", response_model=PRPResponse)
async def process_prp(request: PRPRequest):
    """
    Processar Product Requirement Prompt
    
    Esta rota simula o processamento de um PRP usando PydanticAI
    e captura métricas no Sentry para monitoramento de AI Agents.
    """
    try:
        logger.info(f"🔄 Processando PRP para usuário: {request.user_id}")
        
        # Simular processamento de IA (aqui integraria com PydanticAI)
        result = f"PRP processado: {request.prompt[:50]}..."
        
        # Adicionar contexto ao Sentry
        sentry_sdk.set_context("prp_request", {
            "user_id": request.user_id,
            "prompt_length": len(request.prompt),
            "has_context": bool(request.context)
        })
        
        # Log de sucesso
        logger.success(f"✅ PRP processado com sucesso para {request.user_id}")
        
        return PRPResponse(
            result=result,
            status="success",
            metadata={
                "processing_time": "1.2s",
                "ai_model": "pydantic-ai",
                "user_id": request.user_id
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar PRP: {str(e)}")
        # O Sentry capturará automaticamente esta exceção
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/sentry-debug")
async def trigger_error():
    """
    🐛 Rota de teste para verificar integração Sentry
    
    Esta rota gera um erro intencional para testar se o Sentry
    está capturando erros e transações corretamente.
    
    Acesse: http://localhost:8000/sentry-debug
    """
    logger.warning("🚨 Teste de erro do Sentry sendo executado...")
    
    # Adicionar contexto para debugging
    sentry_sdk.set_context("debug_test", {
        "test_type": "division_by_zero",
        "timestamp": "2025-01-18T14:34:09.851Z",
        "user_agent": "sentry-debug-test"
    })
    
    # Erro intencional para teste
    division_by_zero = 1 / 0
    return {"this": "will never be reached"}

# Executar aplicação
if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Iniciando PRP Agent com Sentry...")
    logger.info(f"🔍 Sentry DSN: {os.getenv('SENTRY_DSN', 'Not configured')}")
    logger.info(f"🌍 Environment: {os.getenv('SENTRY_ENVIRONMENT', 'development')}")
    
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "true").lower() == "true"
    )