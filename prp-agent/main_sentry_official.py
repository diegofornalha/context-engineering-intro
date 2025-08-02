import sentry_sdk
from fastapi import FastAPI
from pydantic import BaseModel
import json
import time
import uuid
from typing import Dict, Any, List

# Configure SDK seguindo documentação oficial
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,  # Include LLM inputs/outputs
)

app = FastAPI(title="PRP Agent - Sentry AI Agents Official Standards")

# Models seguindo padrão oficial
class AgentRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    agent_name: str = "PRP Assistant"
    temperature: float = 0.1
    max_tokens: int = 1000
    user_id: str = "anonymous"

class AgentResponse(BaseModel):
    result: str
    agent_session: str
    total_tokens: int
    input_tokens: int
    output_tokens: int
    tools_executed: List[str]
    processing_time: float

# Implementação seguindo Manual Instrumentation Oficial
class SentryAIAgent:
    def __init__(self, name: str, model_provider: str = "openai", model: str = "gpt-4o-mini"):
        self.name = name
        self.model_provider = model_provider
        self.model = model
        self.available_tools = [
            {
                "name": "text_analyzer", 
                "description": "Analyzes text content and extracts insights",
                "type": "function"
            },
            {
                "name": "code_generator",
                "description": "Generates code based on requirements",
                "type": "function"
            },
            {
                "name": "prp_parser",
                "description": "Parses Product Requirement Prompts",
                "type": "function"
            },
            {
                "name": "context_builder",
                "description": "Builds context for AI processing",
                "type": "function"
            }
        ]
    
    async def invoke_agent(self, prompt: str, temperature: float = 0.1, max_tokens: int = 1000, user_id: str = "anonymous"):
        """
        Invoke Agent Span - Seguindo documentação oficial Sentry
        https://docs.sentry.io/platforms/python/tracing/instrumentation/custom-instrumentation/
        """
        session_id = str(uuid.uuid4())
        
        # INVOKE AGENT SPAN - Padrão Oficial Sentry
        with sentry_sdk.start_span(
            op="gen_ai.invoke_agent",
            name=f"invoke_agent {self.name}",
        ) as agent_span:
            
            # Common Span Attributes (REQUIRED)
            agent_span.set_data("gen_ai.system", self.model_provider)
            agent_span.set_data("gen_ai.request.model", self.model)
            agent_span.set_data("gen_ai.operation.name", "invoke_agent")
            agent_span.set_data("gen_ai.agent.name", self.name)
            
            # Agent-specific attributes (OPTIONAL)
            agent_span.set_data("gen_ai.request.temperature", temperature)
            agent_span.set_data("gen_ai.request.max_tokens", max_tokens)
            agent_span.set_data("gen_ai.request.available_tools", json.dumps(self.available_tools))
            
            # Messages format: [{"role": "", "content": ""}]
            messages = [
                {"role": "system", "content": f"You are {self.name}, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
            agent_span.set_data("gen_ai.request.messages", json.dumps(messages))
            
            start_time = time.time()
            
            # Simular processamento do agent
            result = await self._process_with_llm(prompt, temperature, max_tokens, session_id)
            
            processing_time = time.time() - start_time
            
            # Response data
            agent_span.set_data("gen_ai.response.text", json.dumps([result["response"]]))
            if result["tool_calls"]:
                agent_span.set_data("gen_ai.response.tool_calls", json.dumps(result["tool_calls"]))
            
            # Usage tokens
            agent_span.set_data("gen_ai.usage.input_tokens", result["input_tokens"])
            agent_span.set_data("gen_ai.usage.output_tokens", result["output_tokens"])
            agent_span.set_data("gen_ai.usage.total_tokens", result["total_tokens"])
            
            return {
                "session_id": session_id,
                "result": result["response"],
                "tools_executed": result["tools_executed"],
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"],
                "processing_time": processing_time
            }
    
    async def _process_with_llm(self, prompt: str, temperature: float, max_tokens: int, session_id: str):
        """
        AI Client Span - Seguindo documentação oficial Sentry
        """
        import asyncio
        import random
        
        # AI CLIENT SPAN - Padrão Oficial Sentry
        with sentry_sdk.start_span(
            op="gen_ai.chat",
            name=f"chat {self.model}",
        ) as chat_span:
            
            # Common Span Attributes (REQUIRED)
            chat_span.set_data("gen_ai.system", self.model_provider)
            chat_span.set_data("gen_ai.request.model", self.model)
            chat_span.set_data("gen_ai.operation.name", "chat")
            
            # Request parameters
            messages = [
                {"role": "system", "content": f"You are {self.name}."},
                {"role": "user", "content": prompt}
            ]
            chat_span.set_data("gen_ai.request.messages", json.dumps(messages))
            chat_span.set_data("gen_ai.request.temperature", temperature)
            chat_span.set_data("gen_ai.request.max_tokens", max_tokens)
            
            # Simular processamento LLM
            await asyncio.sleep(0.5)
            
            # Simular resposta e uso de tokens
            input_tokens = len(prompt.split()) * 1.3  # Aproximação
            output_tokens = random.randint(150, 400)
            total_tokens = int(input_tokens + output_tokens)
            
            # Simular tool calls se necessário
            should_use_tools = random.choice([True, False])
            tool_calls = []
            tools_executed = []
            
            if should_use_tools:
                selected_tools = random.sample(self.available_tools, random.randint(1, 3))
                
                for tool in selected_tools:
                    # Executar ferramenta
                    tool_result = await self._execute_tool(tool, prompt, session_id)
                    tools_executed.append(tool["name"])
                    
                    tool_calls.append({
                        "name": tool["name"],
                        "type": "function_call",
                        "arguments": json.dumps({"input": prompt[:100]})
                    })
            
            response = f"Processed: '{prompt[:100]}...' using {len(tools_executed)} tools"
            
            # Response data
            chat_span.set_data("gen_ai.response.text", json.dumps([response]))
            if tool_calls:
                chat_span.set_data("gen_ai.response.tool_calls", json.dumps(tool_calls))
            
            # Usage data
            chat_span.set_data("gen_ai.usage.input_tokens", int(input_tokens))
            chat_span.set_data("gen_ai.usage.output_tokens", output_tokens)
            chat_span.set_data("gen_ai.usage.total_tokens", total_tokens)
            
            return {
                "response": response,
                "tool_calls": tool_calls,
                "tools_executed": tools_executed,
                "input_tokens": int(input_tokens),
                "output_tokens": output_tokens,
                "total_tokens": total_tokens
            }
    
    async def _execute_tool(self, tool: Dict, prompt: str, session_id: str):
        """
        Execute Tool Span - Seguindo documentação oficial Sentry
        """
        import asyncio
        import random
        
        # EXECUTE TOOL SPAN - Padrão Oficial Sentry
        with sentry_sdk.start_span(
            op="gen_ai.execute_tool",
            name=f"execute_tool {tool['name']}",
        ) as tool_span:
            
            # Common attributes
            tool_span.set_data("gen_ai.system", self.model_provider)
            tool_span.set_data("gen_ai.request.model", self.model)
            
            # Tool-specific attributes
            tool_span.set_data("gen_ai.tool.name", tool["name"])
            tool_span.set_data("gen_ai.tool.description", tool["description"])
            tool_span.set_data("gen_ai.tool.type", tool["type"])
            
            # Tool input
            tool_input = {"prompt": prompt[:100], "session_id": session_id}
            tool_span.set_data("gen_ai.tool.input", json.dumps(tool_input))
            
            # Simular execução da ferramenta
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Simular output da ferramenta
            tool_output = f"{tool['name']} processed input successfully"
            tool_span.set_data("gen_ai.tool.output", tool_output)
            
            return tool_output

# Instância do agent seguindo padrões oficiais
sentry_agent = SentryAIAgent(
    name="PRP Assistant",
    model_provider="openai", 
    model="gpt-4o-mini"
)

@app.get("/")
async def root():
    return {
        "app": "PRP Agent - Sentry Official Standards",
        "agent": sentry_agent.name,
        "model": sentry_agent.model,
        "standards": "Official Sentry AI Agents Manual Instrumentation"
    }

@app.post("/ai-agent/official", response_model=AgentResponse)
async def process_official_ai_agent(request: AgentRequest):
    """
    Processamento AI Agent seguindo 100% os padrões oficiais Sentry
    
    Implementa todos os spans oficiais:
    - gen_ai.invoke_agent (Agent invocation)
    - gen_ai.chat (LLM interaction) 
    - gen_ai.execute_tool (Tool execution)
    
    Com todos os atributos obrigatórios e opcionais da documentação oficial.
    """
    try:
        result = await sentry_agent.invoke_agent(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            user_id=request.user_id
        )
        
        return AgentResponse(
            result=result["result"],
            agent_session=result["session_id"],
            total_tokens=result["total_tokens"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            tools_executed=result["tools_executed"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise

@app.get("/ai-agent/benchmark-official")
async def benchmark_official_standards():
    """
    Benchmark seguindo padrões oficiais Sentry AI Agents
    Gera múltiplos spans de todos os tipos oficiais
    """
    test_cases = [
        {"prompt": "Analyze system architecture", "model": "gpt-4o-mini", "agent": "Architecture Agent"},
        {"prompt": "Generate API documentation", "model": "gpt-4-turbo", "agent": "Documentation Agent"},
        {"prompt": "Review code security", "model": "gpt-4", "agent": "Security Agent"},
        {"prompt": "Optimize database queries", "model": "gpt-4o-mini", "agent": "Performance Agent"},
        {"prompt": "Create automated tests", "model": "gpt-4-turbo", "agent": "Testing Agent"}
    ]
    
    results = []
    
    for i, test in enumerate(test_cases):
        # Criar agent específico para cada teste
        test_agent = SentryAIAgent(
            name=test["agent"],
            model_provider="openai",
            model=test["model"]
        )
        
        result = await test_agent.invoke_agent(
            prompt=test["prompt"],
            user_id=f"benchmark_user_{i}"
        )
        
        results.append({
            "test": i + 1,
            "agent": test["agent"],
            "model": test["model"],
            "session_id": result["session_id"],
            "tokens": result["total_tokens"],
            "tools": len(result["tools_executed"]),
            "time": f"{result['processing_time']:.2f}s"
        })
    
    # Capture benchmark completion
    sentry_sdk.capture_message(
        f"AI Agents Official Standards Benchmark: {len(results)} agents tested",
        level="info"
    )
    
    return {
        "benchmark": "Official Sentry AI Agents Standards",
        "agents_tested": len(results),
        "total_tokens": sum(r["tokens"] for r in results),
        "avg_time": f"{sum(float(r['time'][:-1]) for r in results) / len(results):.2f}s",
        "results": results
    }

@app.get("/sentry-debug")
async def trigger_error():
    """Debug endpoint para teste Sentry"""
    division_by_zero = 1 / 0