#!/usr/bin/env python3
"""
🤖 Sentry AI Agent Monitoring para PRP Agent
===========================================

Configuração específica do Sentry AI Agent Monitoring (Beta)
para monitoramento avançado de agentes PydanticAI e workflows de IA.
"""

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import json

def configure_sentry_ai_agent_monitoring(
    dsn: str,
    environment: str = "development",
    debug: bool = False,
    agent_name: str = "prp-agent"
):
    """
    Configura Sentry AI Agent Monitoring especificamente para PRP Agent
    
    Args:
        dsn: Sentry DSN do projeto
        environment: Ambiente (development, staging, production)
        debug: Habilitar modo debug
        agent_name: Nome do agente para rastreamento
    """
    
    # Configurar integração com logging otimizada para AI Agents
    logging_integration = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    
    # Configurar Sentry com foco em AI Agent Monitoring
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        debug=debug,
        
        # Integrações essenciais para AI Agents
        integrations=[
            logging_integration,
            StdlibIntegration(auto_enabling=True),
            ExcepthookIntegration(always_run=True),
        ],
        
        # Performance tracking para AI workflows
        traces_sample_rate=1.0 if environment == "development" else 0.2,
        
        # AI Agent específico: Session tracking para workflows
        auto_session_tracking=True,
        session_mode="request",  # Track cada run do agente como sessão
        
        # Configurações específicas para AI Agent Monitoring
        attach_stacktrace=True,
        send_default_pii=False,
        max_breadcrumbs=50,  # Mais breadcrumbs para workflows complexos
        
        # Release tracking para agentes
        release=f"{agent_name}@{get_agent_version()}",
        
        # Filtrar eventos antes de enviar
        before_send=filter_ai_agent_events,
    )
    
    # Configurar contexto específico para AI Agent
    sentry_sdk.set_tag("agent_type", "pydantic_ai")
    sentry_sdk.set_tag("agent_name", agent_name)
    sentry_sdk.set_tag("monitoring_type", "ai_agent")
    
    # Context específico para AI Agent Monitoring
    sentry_sdk.set_context("ai_agent", {
        "name": agent_name,
        "version": get_agent_version(),
        "framework": "pydantic_ai",
        "llm_providers": ["openai", "anthropic"],
        "tools": ["mcp_turso", "mcp_sentry", "prp_analysis"],
        "workflow_type": "conversational_analysis",
        "setup_time": datetime.now().isoformat()
    })
    
    print(f"🤖 Sentry AI Agent Monitoring configurado para {agent_name}")
    print(f"📊 Ambiente: {environment}")
    print(f"🔗 Acesse: https://sentry.io/ → AI Agents")

def filter_ai_agent_events(event, hint):
    """
    Filtro específico para eventos de AI Agent Monitoring
    """
    # Ignorar interrupções de teclado
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, KeyboardInterrupt):
            return None
    
    # Enriquecer eventos com contexto de AI Agent
    if event.get('exception'):
        for exception in event['exception']['values']:
            module = exception.get('module', '')
            
            # Categorizar por componente do AI Agent
            if 'agents.' in module:
                sentry_sdk.set_tag("ai_component", "agent_core")
                sentry_sdk.set_tag("workflow_stage", "agent_execution")
            elif 'tools.' in module:
                sentry_sdk.set_tag("ai_component", "tool_execution")
                sentry_sdk.set_tag("workflow_stage", "tool_call")
            elif 'pydantic_ai' in module.lower():
                sentry_sdk.set_tag("ai_component", "pydantic_ai_framework")
                sentry_sdk.set_tag("workflow_stage", "framework")
            elif any(x in module.lower() for x in ['openai', 'anthropic', 'llm']):
                sentry_sdk.set_tag("ai_component", "llm_provider")
                sentry_sdk.set_tag("workflow_stage", "model_interaction")
    
    # Adicionar contexto do workflow de IA
    event.setdefault('extra', {}).update({
        'ai_monitoring': True,
        'agent_framework': 'pydantic_ai',
        'monitoring_version': '1.0.0'
    })
    
    return event

def get_agent_version() -> str:
    """Obtém versão do agente PRP"""
    try:
        version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                return f.read().strip()
        return "1.0.0"
    except:
        return "unknown"

def start_ai_agent_run(agent_name: str, run_id: str, user_input: str):
    """
    Inicia uma nova execução do AI Agent para monitoramento
    
    Args:
        agent_name: Nome do agente
        run_id: ID único da execução
        user_input: Input do usuário
    """
    # Iniciar nova sessão para este run do agente
    sentry_sdk.start_session(
        session_mode="request",
        distinctId=run_id,
        release=f"{agent_name}@{get_agent_version()}"
    )
    
    # Configurar contexto específico deste run
    sentry_sdk.set_context("agent_run", {
        "run_id": run_id,
        "agent_name": agent_name,
        "user_input_length": len(user_input),
        "start_time": datetime.now().isoformat(),
        "workflow_type": "prp_analysis"
    })
    
    # Breadcrumb para início do workflow
    sentry_sdk.add_breadcrumb(
        message=f"AI Agent run started: {agent_name}",
        category="ai_agent",
        level="info",
        data={
            "run_id": run_id,
            "agent_name": agent_name,
            "input_chars": len(user_input)
        }
    )

def track_llm_call(model: str, prompt_type: str, tokens_used: Optional[int] = None, cost: Optional[float] = None):
    """
    Rastreia chamadas para LLM no contexto de AI Agent Monitoring
    """
    sentry_sdk.add_breadcrumb(
        message=f"LLM call: {model}",
        category="llm_interaction",
        level="info",
        data={
            "model": model,
            "prompt_type": prompt_type,
            "tokens_used": tokens_used,
            "estimated_cost": cost,
            "timestamp": datetime.now().isoformat(),
            "workflow_stage": "model_interaction"
        }
    )
    
    # Capturar métricas específicas para AI Agents
    with sentry_sdk.configure_scope() as scope:
        scope.set_context("llm_call", {
            "model": model,
            "prompt_type": prompt_type,
            "tokens": tokens_used,
            "cost": cost
        })

def track_tool_execution(tool_name: str, params: Dict[str, Any], duration: float, success: bool):
    """
    Rastreia execução de ferramentas no workflow do AI Agent
    """
    sentry_sdk.add_breadcrumb(
        message=f"Tool execution: {tool_name}",
        category="tool_execution",
        level="info" if success else "error",
        data={
            "tool_name": tool_name,
            "params_count": len(params),
            "duration_ms": duration * 1000,
            "success": success,
            "workflow_stage": "tool_call",
            "timestamp": datetime.now().isoformat()
        }
    )

def track_agent_decision(decision_type: str, reasoning: str, confidence: Optional[float] = None):
    """
    Rastreia decisões do agente durante o workflow
    """
    sentry_sdk.add_breadcrumb(
        message=f"Agent decision: {decision_type}",
        category="agent_reasoning",
        level="info",
        data={
            "decision_type": decision_type,
            "reasoning": reasoning[:200] + "..." if len(reasoning) > 200 else reasoning,
            "confidence": confidence,
            "workflow_stage": "agent_reasoning",
            "timestamp": datetime.now().isoformat()
        }
    )

def end_ai_agent_run(run_id: str, success: bool, output_length: Optional[int] = None, error: Optional[str] = None):
    """
    Finaliza execução do AI Agent
    """
    # Breadcrumb final do workflow
    sentry_sdk.add_breadcrumb(
        message=f"AI Agent run completed: {'success' if success else 'failed'}",
        category="ai_agent",
        level="info" if success else "error",
        data={
            "run_id": run_id,
            "success": success,
            "output_length": output_length,
            "error": error[:100] if error else None,
            "end_time": datetime.now().isoformat()
        }
    )
    
    # Finalizar sessão
    sentry_sdk.end_session(status="ok" if success else "errored")
    
    # Capturar métricas finais
    if success:
        sentry_sdk.capture_message(
            f"AI Agent run completed successfully",
            level="info",
            extras={
                "run_id": run_id,
                "output_length": output_length,
                "workflow_type": "prp_analysis"
            }
        )

def test_ai_agent_monitoring():
    """
    Testa o monitoramento de AI Agent com workflow simulado
    """
    print("\n🤖 Testando Sentry AI Agent Monitoring...")
    
    # 1. Simular início de run do agente
    run_id = f"test-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    start_ai_agent_run("prp-agent", run_id, "Crie um PRP para sistema de cache Redis")
    print("✅ Workflow de AI Agent iniciado")
    
    # 2. Simular chamada LLM
    track_llm_call("gpt-4o", "system_prompt", tokens_used=150, cost=0.003)
    print("✅ Chamada LLM rastreada")
    
    # 3. Simular execução de ferramenta
    import time
    start_time = time.time()
    time.sleep(0.1)  # Simular tempo de execução
    track_tool_execution("create_prp", {"name": "cache-redis", "priority": "high"}, time.time() - start_time, True)
    print("✅ Execução de ferramenta rastreada")
    
    # 4. Simular decisão do agente
    track_agent_decision("prp_creation", "Identificada necessidade de cache para melhorar performance", confidence=0.95)
    print("✅ Decisão do agente rastreada")
    
    # 5. Finalizar run
    end_ai_agent_run(run_id, True, output_length=500)
    print("✅ Workflow de AI Agent finalizado")
    
    print("\n🎯 Workflow completo rastreado no Sentry AI Agent Monitoring!")

def main():
    """
    Função principal - configuração para AI Agent Monitoring
    """
    print("🤖 Sentry AI Agent Monitoring para PRP Agent")
    print("=" * 55)
    
    # DSN do projeto (substitua pelo seu)
    DSN = os.getenv("SENTRY_DSN", "https://your-dsn-here@sentry.io/your-project-id")
    
    if DSN == "https://your-dsn-here@sentry.io/your-project-id":
        print("⚠️  CONFIGURE O DSN DO SEU PROJETO SENTRY!")
        print("   1. Crie um projeto no Sentry")
        print("   2. Habilite 'AI Agent Monitoring' (Beta)")
        print("   3. Copie o DSN do projeto")
        print("   4. Configure SENTRY_DSN no arquivo .env")
        
        DSN = os.getenv("SENTRY_DSN")
        if not DSN:
            print("   5. Execute: export SENTRY_DSN='seu-dsn-aqui'")
            return
    
    # Configurar AI Agent Monitoring
    configure_sentry_ai_agent_monitoring(
        dsn=DSN,
        environment="development",
        debug=True,
        agent_name="prp-agent"
    )
    
    # Testar monitoramento
    test_ai_agent_monitoring()
    
    print("\n🎉 Sentry AI Agent Monitoring configurado!")
    print("🔗 Acesse: https://sentry.io/ → AI Agents")
    print("📊 Visualize workflows, tool calls e performance dos agentes")

if __name__ == "__main__":
    main()