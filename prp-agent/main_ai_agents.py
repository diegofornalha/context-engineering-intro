import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
import random

# Configure SDK with OpenAI Agents Integration
# Seguindo documentação oficial: https://docs.sentry.io/platforms/python/integrations/openai-agents/
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    # Add data like inputs and responses to/from LLMs and tools;
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    integrations=[
        OpenAIAgentsIntegration(),
    ],
)

app = FastAPI(title="PRP Agent - AI Agents Monitoring")

# Modelos para simular AI Agent
class AgentRequest(BaseModel):
    prompt: str
    agent_type: str = "prp_processor"
    user_id: str = "anonymous"

class AgentResponse(BaseModel):
    result: str
    agent_id: str
    tokens_used: int
    model: str
    tools_used: list
    metadata: Dict[str, Any]

# Simulação de AI Agent para testar Sentry monitoring
class MockAIAgent:
    def __init__(self, name: str, model: str = "gpt-4"):
        self.name = name
        self.model = model
        self.tools = ["text_analyzer", "prp_parser", "context_builder"]
    
    async def process(self, prompt: str, user_id: str) -> Dict[str, Any]:
        """
        Simula processamento de AI Agent
        O Sentry vai capturar automaticamente:
        - Agent information
        - Tools usage
        - Prompts
        - Token usage
        - Model information
        """
        
        # Simular processamento
        await asyncio.sleep(0.5)
        
        # Simular uso de ferramentas
        tools_used = random.sample(self.tools, random.randint(1, 3))
        tokens_used = random.randint(150, 800)
        
        # Simular resposta do agent
        result = f"PRP Agent '{self.name}' processou: {prompt[:100]}..."
        
        return {
            "result": result,
            "agent_id": self.name,
            "model": self.model,
            "tokens_used": tokens_used,
            "tools_used": tools_used,
            "user_id": user_id,
            "processing_time": "0.5s"
        }

# Instância do agente
prp_agent = MockAIAgent("PRP-Processor-v1", "gpt-4-turbo")

@app.get("/")
async def root():
    """Status da aplicação com AI Agents monitoring"""
    return {
        "app": "PRP Agent - AI Monitoring",
        "status": "✅ Online",
        "sentry_ai_agents": "🤖 Active",
        "agent": prp_agent.name,
        "model": prp_agent.model
    }

@app.post("/agent/process", response_model=AgentResponse)
async def process_with_agent(request: AgentRequest):
    """
    Endpoint para processar com AI Agent
    
    O Sentry OpenAI Agents Integration vai capturar automaticamente:
    - Agent interactions
    - Tool usage
    - Prompt data
    - Token consumption
    - Model performance
    """
    try:
        # Adicionar contexto Sentry para AI Agents
        sentry_sdk.set_context("ai_agent", {
            "agent_name": prp_agent.name,
            "agent_type": request.agent_type,
            "user_id": request.user_id,
            "prompt_length": len(request.prompt)
        })
        
        # Processar com AI Agent (Sentry vai monitorar automaticamente)
        result = await prp_agent.process(request.prompt, request.user_id)
        
        return AgentResponse(
            result=result["result"],
            agent_id=result["agent_id"], 
            tokens_used=result["tokens_used"],
            model=result["model"],
            tools_used=result["tools_used"],
            metadata={
                "user_id": result["user_id"],
                "processing_time": result["processing_time"],
                "timestamp": "2025-01-18T14:45:00Z"
            }
        )
        
    except Exception as e:
        # Sentry vai capturar automaticamente erros de AI Agents
        sentry_sdk.capture_exception(e)
        raise

@app.get("/agent/test-tools")
async def test_agent_tools():
    """
    Teste específico para ferramentas do AI Agent
    Gera eventos para Sentry AI Agents monitoring
    """
    try:
        # Simular múltiplos usos de ferramentas
        results = []
        
        for tool in prp_agent.tools:
            # Simular uso de cada ferramenta
            tool_result = {
                "tool": tool,
                "status": "success",
                "execution_time": random.randint(50, 200),
                "tokens": random.randint(20, 100)
            }
            results.append(tool_result)
            
            # Adicionar contexto específico da ferramenta
            sentry_sdk.set_context(f"tool_{tool}", tool_result)
        
        return {
            "agent": prp_agent.name,
            "tools_tested": len(results),
            "results": results,
            "total_tokens": sum(r["tokens"] for r in results)
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

@app.get("/agent/performance")
async def agent_performance_test():
    """
    Teste de performance do AI Agent
    Múltiplas interações para gerar dados no Sentry
    """
    try:
        performance_data = []
        
        # Simular múltiplas interações
        test_prompts = [
            "Analisar requisitos de autenticação",
            "Gerar documentação de API",
            "Revisar código de segurança",
            "Otimizar performance de banco",
            "Criar testes automatizados"
        ]
        
        for i, prompt in enumerate(test_prompts):
            start_time = asyncio.get_event_loop().time()
            
            # Processar com agent
            result = await prp_agent.process(prompt, f"perf_test_user_{i}")
            
            end_time = asyncio.get_event_loop().time()
            processing_time = end_time - start_time
            
            perf_data = {
                "iteration": i + 1,
                "prompt": prompt,
                "tokens": result["tokens_used"],
                "tools": len(result["tools_used"]),
                "time": f"{processing_time:.3f}s"
            }
            performance_data.append(perf_data)
        
        return {
            "agent": prp_agent.name,
            "performance_test": "completed",
            "iterations": len(performance_data),
            "total_tokens": sum(p["tokens"] for p in performance_data),
            "avg_time": f"{sum(float(p['time'][:-1]) for p in performance_data) / len(performance_data):.3f}s",
            "results": performance_data
        }
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

@app.get("/sentry-debug")
async def trigger_error():
    """
    Endpoint de debug para Sentry
    Conforme documentação oficial
    """
    division_by_zero = 1 / 0