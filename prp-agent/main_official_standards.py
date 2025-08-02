from fastapi import FastAPI
import sentry_sdk
from pydantic import BaseModel
from typing import Dict, Any, List
import time
import uuid
import json
import asyncio
import random

# Configure SDK seguindo documentação oficial Sentry AI Agents + Release Health
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,  # Include LLM inputs/outputs conforme documentação
    
    # ✅ RELEASE HEALTH CONFIGURATION
    release="prp-agent@1.0.0",  # Set release version for tracking
    environment="production",   # Set environment for Release Health
    auto_session_tracking=True  # Enable automatic session tracking
)

app = FastAPI()

class OfficialAgentRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    agent_name: str = "PRP Assistant"
    temperature: float = 0.1
    max_tokens: int = 1000
    user_id: str = "anonymous"

class OfficialAgentResponse(BaseModel):
    result: str
    agent_session: str
    total_tokens: int
    input_tokens: int
    output_tokens: int
    tools_executed: List[str]
    processing_time: float

# Implementação seguindo EXATAMENTE os padrões oficiais Sentry
def invoke_agent_official(agent_name: str, model: str, prompt: str, temperature: float, max_tokens: int, user_id: str):
    """
    INVOKE AGENT SPAN - Seguindo documentação oficial Sentry
    
    The spans op MUST be "gen_ai.invoke_agent".
    The span name SHOULD be "invoke_agent {gen_ai.agent.name}".
    """
    session_id = str(uuid.uuid4())
    
    # INVOKE AGENT SPAN - Padrão oficial
    with sentry_sdk.start_span(
        op="gen_ai.invoke_agent",  # MUST be "gen_ai.invoke_agent"
        name=f"invoke_agent {agent_name}",  # SHOULD be "invoke_agent {agent_name}"
    ) as span:
        
        # Common Span Attributes - REQUIRED
        span.set_data("gen_ai.system", "openai")  # REQUIRED
        span.set_data("gen_ai.request.model", model)  # REQUIRED
        span.set_data("gen_ai.operation.name", "invoke_agent")  # MUST be "invoke_agent"
        span.set_data("gen_ai.agent.name", agent_name)  # SHOULD be set
        
        # Optional attributes
        span.set_data("gen_ai.request.temperature", temperature)
        span.set_data("gen_ai.request.max_tokens", max_tokens)
        
        # Available tools
        available_tools = [
            {"name": "text_analyzer", "description": "Analyzes text content"},
            {"name": "code_generator", "description": "Generates code"},
            {"name": "prp_parser", "description": "Parses Product Requirements"}
        ]
        span.set_data("gen_ai.request.available_tools", json.dumps(available_tools))
        
        # Messages format: [{"role": "", "content": ""}]
        messages = [
            {"role": "system", "content": f"You are {agent_name}, a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        span.set_data("gen_ai.request.messages", json.dumps(messages))
        
        # Processar com LLM
        start_time = time.time()
        llm_result = ai_client_official(model, messages, temperature, max_tokens, session_id)
        processing_time = time.time() - start_time
        
        # Response data
        span.set_data("gen_ai.response.text", json.dumps([llm_result["response"]]))
        if llm_result["tool_calls"]:
            span.set_data("gen_ai.response.tool_calls", json.dumps(llm_result["tool_calls"]))
        
        # Token usage
        span.set_data("gen_ai.usage.input_tokens", llm_result["input_tokens"])
        span.set_data("gen_ai.usage.output_tokens", llm_result["output_tokens"])
        span.set_data("gen_ai.usage.total_tokens", llm_result["total_tokens"])
        
        return {
            "session_id": session_id,
            "result": llm_result["response"],
            "tools_executed": llm_result["tools_executed"],
            "input_tokens": llm_result["input_tokens"],
            "output_tokens": llm_result["output_tokens"],
            "total_tokens": llm_result["total_tokens"],
            "processing_time": processing_time
        }

def ai_client_official(model: str, messages: List[Dict], temperature: float, max_tokens: int, session_id: str):
    """
    AI CLIENT SPAN - Seguindo documentação oficial Sentry
    
    The span op MUST be "gen_ai.{gen_ai.operation.name}". (e.g. "gen_ai.chat")
    The span name SHOULD be {gen_ai.operation.name} {gen_ai.request.model}". (e.g. "chat gpt-4o-mini")
    """
    
    # AI CLIENT SPAN - Padrão oficial
    with sentry_sdk.start_span(
        op="gen_ai.chat",  # MUST be "gen_ai.chat"
        name=f"chat {model}",  # SHOULD be "chat {model}"
    ) as span:
        
        # Common Span Attributes - REQUIRED
        span.set_data("gen_ai.system", "openai")  # REQUIRED
        span.set_data("gen_ai.request.model", model)  # REQUIRED
        span.set_data("gen_ai.operation.name", "chat")  # operation name
        
        # Request data
        span.set_data("gen_ai.request.messages", json.dumps(messages))
        span.set_data("gen_ai.request.temperature", temperature)
        span.set_data("gen_ai.request.max_tokens", max_tokens)
        
        # Simular processamento LLM
        time.sleep(0.5)
        
        # Simular tokens
        prompt_text = " ".join([msg["content"] for msg in messages])
        input_tokens = int(len(prompt_text.split()) * 1.3)
        output_tokens = random.randint(150, 400)
        total_tokens = input_tokens + output_tokens
        
        # Simular resposta
        response = f"Processed: '{messages[-1]['content'][:100]}...' with advanced AI analysis"
        
        # Simular tool calls
        should_use_tools = random.choice([True, False])
        tool_calls = []
        tools_executed = []
        
        if should_use_tools:
            tools = ["text_analyzer", "code_generator", "prp_parser"]
            selected_tools = random.sample(tools, random.randint(1, 2))
            
            for tool_name in selected_tools:
                # Execute tool seguindo padrão oficial
                tool_result = execute_tool_official(tool_name, messages[-1]["content"], model, session_id)
                tools_executed.append(tool_name)
                
                tool_calls.append({
                    "name": tool_name,
                    "type": "function_call",
                    "arguments": json.dumps({"input": messages[-1]["content"][:100]})
                })
        
        # Response data
        span.set_data("gen_ai.response.text", json.dumps([response]))
        if tool_calls:
            span.set_data("gen_ai.response.tool_calls", json.dumps(tool_calls))
        
        # Token usage
        span.set_data("gen_ai.usage.input_tokens", input_tokens)
        span.set_data("gen_ai.usage.output_tokens", output_tokens)
        span.set_data("gen_ai.usage.total_tokens", total_tokens)
        
        return {
            "response": response,
            "tool_calls": tool_calls,
            "tools_executed": tools_executed,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        }

def execute_tool_official(tool_name: str, input_text: str, model: str, session_id: str):
    """
    EXECUTE TOOL SPAN - Seguindo documentação oficial Sentry
    
    The span op MUST be "gen_ai.execute_tool".
    The span name SHOULD be "execute_tool {gen_ai.tool.name}".
    """
    
    # EXECUTE TOOL SPAN - Padrão oficial
    with sentry_sdk.start_span(
        op="gen_ai.execute_tool",  # MUST be "gen_ai.execute_tool"
        name=f"execute_tool {tool_name}",  # SHOULD be "execute_tool {tool_name}"
    ) as span:
        
        # Common attributes
        span.set_data("gen_ai.system", "openai")
        span.set_data("gen_ai.request.model", model)
        
        # Tool-specific attributes
        span.set_data("gen_ai.tool.name", tool_name)
        
        # Tool descriptions
        descriptions = {
            "text_analyzer": "Analyzes text content and extracts insights",
            "code_generator": "Generates code based on requirements", 
            "prp_parser": "Parses Product Requirement Prompts"
        }
        span.set_data("gen_ai.tool.description", descriptions.get(tool_name, "AI Tool"))
        span.set_data("gen_ai.tool.type", "function")
        
        # Tool input/output
        tool_input = {"text": input_text[:100], "session_id": session_id}
        span.set_data("gen_ai.tool.input", json.dumps(tool_input))
        
        # Simular execução
        time.sleep(random.uniform(0.1, 0.3))
        
        tool_output = f"{tool_name} processed: {input_text[:50]}... -> Analysis complete"
        span.set_data("gen_ai.tool.output", tool_output)
        
        return tool_output

@app.get("/")
async def root():
    return {
        "app": "PRP Agent - Official Sentry AI Standards + Release Health", 
        "version": "1.0.0",
        "release": "prp-agent@1.0.0",
        "environment": "production",
        "status": "🎯 100% Official Implementation + Release Health",
        "spans": ["gen_ai.invoke_agent", "gen_ai.chat", "gen_ai.execute_tool"],
        "features": ["AI Agents Monitoring", "Release Health", "Session Tracking", "Crash Detection"],
        "standards": "https://docs.sentry.io/platforms/python/tracing/instrumentation/custom-instrumentation/"
    }

@app.post("/ai-agent/official-standards", response_model=OfficialAgentResponse)
async def process_official_standards(request: OfficialAgentRequest):
    """
    Processamento AI Agent seguindo 100% os padrões oficiais Sentry
    
    Implementa TODOS os spans oficiais:
    ✅ gen_ai.invoke_agent (Agent invocation)
    ✅ gen_ai.chat (LLM interaction)
    ✅ gen_ai.execute_tool (Tool execution)
    
    Com TODOS os atributos obrigatórios da documentação oficial.
    """
    try:
        result = invoke_agent_official(
            agent_name=request.agent_name,
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            user_id=request.user_id
        )
        
        return OfficialAgentResponse(
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

@app.get("/ai-agent/benchmark-standards")
async def benchmark_official_standards():
    """
    Benchmark seguindo padrões oficiais Sentry AI Agents
    Gera múltiplos spans seguindo documentação oficial
    """
    test_cases = [
        {"prompt": "Implement JWT authentication system", "model": "gpt-4o-mini", "agent": "Security Engineer"},
        {"prompt": "Design RESTful API architecture", "model": "gpt-4-turbo", "agent": "API Architect"},
        {"prompt": "Optimize database performance", "model": "gpt-4", "agent": "Database Specialist"},
        {"prompt": "Create automated testing suite", "model": "gpt-4o-mini", "agent": "QA Engineer"},
        {"prompt": "Implement CI/CD pipeline", "model": "gpt-4-turbo", "agent": "DevOps Engineer"}
    ]
    
    results = []
    
    for i, test in enumerate(test_cases):
        result = invoke_agent_official(
            agent_name=test["agent"],
            model=test["model"],
            prompt=test["prompt"],
            temperature=0.1,
            max_tokens=1000,
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
    
    # Capture benchmark completion seguindo padrões
    sentry_sdk.capture_message(
        f"Official Sentry AI Standards Benchmark: {len(results)} agents, {sum(r['tokens'] for r in results)} tokens",
        level="info"
    )
    
    return {
        "benchmark": "✅ Official Sentry AI Agents Standards",
        "implementation": "100% Official Documentation Compliance",
        "agents_tested": len(results),
        "total_tokens": sum(r["tokens"] for r in results),
        "avg_time": f"{sum(float(r['time'][:-1]) for r in results) / len(results):.2f}s",
        "spans_generated": ["gen_ai.invoke_agent", "gen_ai.chat", "gen_ai.execute_tool"],
        "results": results
    }

@app.get("/sentry-debug")
async def trigger_error():
    """Debug endpoint oficial"""
    division_by_zero = 1 / 0