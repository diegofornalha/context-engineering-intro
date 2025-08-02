import sentry_sdk
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
import asyncio
import random
import time
import uuid

# Configure SDK for AI Agents monitoring (Custom Implementation)
# Baseado na documentação oficial Sentry, adaptado para monitoramento customizado de AI Agents
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    # Add data like inputs and responses to/from LLMs and tools
    send_default_pii=True,
    # Tags para identificar AI Agent events
    tags={
        "app.type": "ai_agent",
        "agent.framework": "prp_custom",
        "monitoring.type": "ai_agents"
    }
)

app = FastAPI(title="PRP Agent - AI Agents Custom Monitoring")

# Modelos para AI Agent
class AgentRequest(BaseModel):
    prompt: str
    agent_type: str = "prp_processor"
    user_id: str = "anonymous"
    temperature: float = 0.7

class ToolCall(BaseModel):
    name: str
    input: Dict[str, Any]
    output: str
    execution_time: float
    tokens_used: int

class AgentResponse(BaseModel):
    result: str
    agent_id: str
    total_tokens: int
    model: str
    tools_used: List[ToolCall]
    metadata: Dict[str, Any]

# AI Agent Simulator para gerar eventos Sentry realistas
class AIAgentMonitor:
    def __init__(self, name: str, model: str = "gpt-4-turbo"):
        self.name = name
        self.model = model
        self.available_tools = [
            "text_analyzer", "prp_parser", "context_builder", 
            "code_generator", "documentation_writer", "test_creator"
        ]
    
    def _capture_agent_start(self, prompt: str, user_id: str) -> str:
        """Captura início de processamento do AI Agent no Sentry"""
        session_id = str(uuid.uuid4())
        
        # Set agent context
        sentry_sdk.set_context("ai_agent", {
            "agent_name": self.name,
            "agent_id": session_id,
            "model": self.model,
            "prompt_length": len(prompt),
            "user_id": user_id,
            "status": "processing"
        })
        
        # Set tags específicas para AI
        sentry_sdk.set_tag("agent.name", self.name)
        sentry_sdk.set_tag("agent.model", self.model)
        sentry_sdk.set_tag("agent.session", session_id)
        
        # Capturar mensagem de início
        sentry_sdk.capture_message(
            f"AI Agent {self.name} started processing",
            level="info",
            tags={
                "event.type": "agent_start",
                "agent.session": session_id
            }
        )
        
        return session_id
    
    def _capture_tool_usage(self, session_id: str, tool_name: str, 
                          input_data: Dict, output: str, 
                          execution_time: float, tokens: int):
        """Captura uso de ferramentas no Sentry"""
        
        # Context específico da ferramenta
        sentry_sdk.set_context(f"tool_{tool_name}", {
            "tool_name": tool_name,
            "session_id": session_id,
            "execution_time": execution_time,
            "tokens_used": tokens,
            "input_size": len(str(input_data)),
            "output_size": len(output)
        })
        
        # Breadcrumb para tracking de ferramentas
        sentry_sdk.add_breadcrumb(
            message=f"Tool {tool_name} executed",
            category="ai.tool",
            level="info",
            data={
                "tool": tool_name,
                "tokens": tokens,
                "time": execution_time,
                "session": session_id
            }
        )
    
    def _capture_agent_complete(self, session_id: str, total_tokens: int, 
                              tools_count: int, total_time: float):
        """Captura conclusão do AI Agent no Sentry"""
        
        # Update agent context with results
        sentry_sdk.set_context("ai_agent_result", {
            "session_id": session_id,
            "total_tokens": total_tokens,
            "tools_used": tools_count,
            "total_processing_time": total_time,
            "status": "completed"
        })
        
        # Performance metrics
        sentry_sdk.set_context("ai_performance", {
            "tokens_per_second": total_tokens / total_time if total_time > 0 else 0,
            "avg_tool_time": total_time / tools_count if tools_count > 0 else 0,
            "efficiency_score": min(100, (total_tokens / total_time) * 10) if total_time > 0 else 0
        })
        
        # Capture completion message
        sentry_sdk.capture_message(
            f"AI Agent {self.name} completed processing",
            level="info",
            tags={
                "event.type": "agent_complete",
                "agent.session": session_id,
                "performance.tokens": str(total_tokens),
                "performance.time": f"{total_time:.2f}s"
            }
        )
    
    async def process(self, prompt: str, user_id: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Processa prompt com AI Agent e captura todos os eventos no Sentry
        """
        start_time = time.time()
        
        # 1. Iniciar monitoramento
        session_id = self._capture_agent_start(prompt, user_id)
        
        try:
            # 2. Simular processamento inicial
            await asyncio.sleep(0.3)
            
            # 3. Simular uso de ferramentas
            tools_used = []
            selected_tools = random.sample(self.available_tools, random.randint(2, 4))
            
            for tool_name in selected_tools:
                tool_start = time.time()
                
                # Simular input/output da ferramenta
                tool_input = {
                    "prompt_segment": prompt[:100],
                    "temperature": temperature,
                    "context": f"Processing with {tool_name}"
                }
                
                # Simular processamento da ferramenta
                await asyncio.sleep(random.uniform(0.1, 0.4))
                
                tool_output = f"{tool_name} processed: {prompt[:50]}... -> Generated output"
                tokens_used = random.randint(15, 80)
                execution_time = time.time() - tool_start
                
                # Capturar no Sentry
                self._capture_tool_usage(
                    session_id, tool_name, tool_input, 
                    tool_output, execution_time, tokens_used
                )
                
                # Adicionar aos resultados
                tools_used.append(ToolCall(
                    name=tool_name,
                    input=tool_input,
                    output=tool_output,
                    execution_time=execution_time,
                    tokens_used=tokens_used
                ))
            
            # 4. Simular resposta final
            await asyncio.sleep(0.2)
            
            total_time = time.time() - start_time
            total_tokens = sum(tool.tokens_used for tool in tools_used) + random.randint(100, 300)
            
            result = f"PRP Agent '{self.name}' processou com sucesso: {prompt[:100]}..."
            
            # 5. Capturar conclusão
            self._capture_agent_complete(
                session_id, total_tokens, len(tools_used), total_time
            )
            
            return {
                "result": result,
                "agent_id": self.name,
                "session_id": session_id,
                "model": self.model,
                "total_tokens": total_tokens,
                "tools_used": tools_used,
                "processing_time": total_time,
                "user_id": user_id
            }
            
        except Exception as e:
            # Capturar erros específicos de AI Agent
            sentry_sdk.set_context("ai_agent_error", {
                "session_id": session_id,
                "error_stage": "processing",
                "prompt_length": len(prompt)
            })
            sentry_sdk.capture_exception(e)
            raise

# Instância do agente
prp_agent = AIAgentMonitor("PRP-Agent-v1", "gpt-4-turbo")

@app.get("/")
async def root():
    """Status da aplicação AI Agents"""
    sentry_sdk.capture_message("PRP Agent status check", level="info")
    
    return {
        "app": "PRP Agent - AI Monitoring",
        "status": "✅ Online",
        "sentry_monitoring": "🤖 AI Agents Custom",
        "agent": prp_agent.name,
        "model": prp_agent.model,
        "tools_available": len(prp_agent.available_tools)
    }

@app.post("/ai-agent/process", response_model=AgentResponse)
async def process_with_ai_agent(request: AgentRequest):
    """
    Processar com AI Agent + Full Sentry Monitoring
    
    Captura no Sentry:
    - Agent start/complete events
    - Tool usage tracking  
    - Performance metrics
    - Token consumption
    - Error handling
    """
    try:
        # Processar com monitoramento completo
        result = await prp_agent.process(
            request.prompt, request.user_id, request.temperature
        )
        
        return AgentResponse(
            result=result["result"],
            agent_id=result["agent_id"],
            total_tokens=result["total_tokens"],
            model=result["model"],
            tools_used=result["tools_used"],
            metadata={
                "session_id": result["session_id"],
                "processing_time": f"{result['processing_time']:.2f}s",
                "user_id": result["user_id"],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        )
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

@app.get("/ai-agent/benchmark")
async def ai_agent_benchmark():
    """
    Benchmark de AI Agent para gerar múltiplos eventos Sentry
    """
    benchmark_prompts = [
        "Analisar arquitetura de microserviços",
        "Gerar documentação de API REST", 
        "Revisar código para segurança",
        "Otimizar queries de banco de dados",
        "Criar testes automatizados E2E"
    ]
    
    results = []
    
    for i, prompt in enumerate(benchmark_prompts):
        result = await prp_agent.process(
            prompt, f"benchmark_user_{i}", temperature=0.5
        )
        
        results.append({
            "prompt": prompt,
            "session_id": result["session_id"],
            "tokens": result["total_tokens"],
            "tools": len(result["tools_used"]),
            "time": f"{result['processing_time']:.2f}s"
        })
    
    # Capturar resumo do benchmark
    sentry_sdk.capture_message(
        f"AI Agent benchmark completed: {len(results)} sessions",
        level="info",
        tags={
            "event.type": "benchmark_complete",
            "benchmark.sessions": str(len(results)),
            "benchmark.total_tokens": str(sum(r["tokens"] for r in results))
        }
    )
    
    return {
        "benchmark": "completed",
        "agent": prp_agent.name,
        "sessions": len(results),
        "total_tokens": sum(r["tokens"] for r in results),
        "avg_time": f"{sum(float(r['time'][:-1]) for r in results) / len(results):.2f}s",
        "results": results
    }

@app.get("/sentry-debug")
async def trigger_error():
    """Debug endpoint para Sentry"""
    division_by_zero = 1 / 0