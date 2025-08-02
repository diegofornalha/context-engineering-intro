#!/usr/bin/env python3
"""
🚨 Configuração do Sentry para PRP Agent
========================================

Configuração completa do Sentry para monitoramento de erros no projeto PRP Agent,
incluindo integração com agentes PydanticAI, MCP Tools e análises LLM.
"""

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

def configure_sentry_for_prp_agent(
    dsn: str,
    environment: str = "development",
    debug: bool = False,
    user_context: Optional[Dict[str, Any]] = None
):
    """
    Configura Sentry especificamente para o projeto PRP Agent
    
    Args:
        dsn: Data Source Name do projeto Sentry
        environment: Ambiente (development, staging, production)
        debug: Habilitar modo debug
        user_context: Contexto do usuário para rastreamento
    """
    
    # Configurar integração com logging
    logging_integration = LoggingIntegration(
        level=logging.INFO,        # Captura logs INFO e acima
        event_level=logging.ERROR  # Envia eventos ERROR e acima
    )
    
    # Configurar Sentry com integrações específicas para PRP Agent
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        debug=debug,
        
        # Integrações específicas
        integrations=[
            logging_integration,
            StdlibIntegration(auto_enabling=True),
            ExcepthookIntegration(always_run=True),
            SqlalchemyIntegration(),  # Para monitorar queries do banco SQLite
        ],
        
        # Performance e traces
        traces_sample_rate=1.0 if environment == "development" else 0.1,
        
        # Release Health
        auto_session_tracking=True,
        
        # Configurações específicas do PRP Agent
        attach_stacktrace=True,
        send_default_pii=False,
        
        # Tags globais para PRP Agent
        before_send=filter_prp_agent_events,
        
        # Configuração de release
        release=f"prp-agent@{get_agent_version()}",
    )
    
    # Configurar contexto específico do PRP Agent
    sentry_sdk.set_tag("project", "prp-agent")
    sentry_sdk.set_tag("component", "pydantic-ai")
    
    # Configurar contexto do usuário se fornecido
    if user_context:
        sentry_sdk.set_user(user_context)
    
    # Configurar contexto do projeto
    sentry_sdk.set_context("prp_agent", {
        "version": get_agent_version(),
        "database_path": "../context-memory.db",
        "supported_llms": ["openai", "anthropic"],
        "mcp_integration": True,
        "setup_time": datetime.now().isoformat()
    })
    
    print(f"✅ Sentry configurado para PRP Agent - Ambiente: {environment}")

def filter_prp_agent_events(event, hint):
    """
    Filtra eventos específicos do PRP Agent antes de enviar para Sentry
    """
    # Ignorar erros de teclado (Ctrl+C)
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, KeyboardInterrupt):
            return None
    
    # Ignorar avisos específicos do PydanticAI (se necessário)
    if event.get('level') == 'warning':
        message = event.get('message', '')
        if 'pydantic' in message.lower() and 'deprecation' in message.lower():
            return None
    
    # Adicionar tags específicas baseadas no erro
    if event.get('exception'):
        for exception in event['exception']['values']:
            module = exception.get('module', '')
            
            # Categorizar erros por componente do PRP Agent
            if 'agents.' in module:
                sentry_sdk.set_tag("component", "agent")
            elif 'tools.' in module:
                sentry_sdk.set_tag("component", "tools")
            elif 'cursor_' in module:
                sentry_sdk.set_tag("component", "cursor-integration")
            elif 'mcp' in module.lower():
                sentry_sdk.set_tag("component", "mcp")
    
    return event

def get_agent_version() -> str:
    """
    Obtém a versão do agente PRP
    """
    try:
        # Tentar ler versão de um arquivo de configuração
        version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                return f.read().strip()
        return "1.0.0"  # Versão padrão
    except:
        return "unknown"

def monitor_prp_agent_operation(operation_name: str, **kwargs):
    """
    Decorator para monitorar operações específicas do PRP Agent
    """
    def decorator(func):
        def wrapper(*args, **func_kwargs):
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("operation", operation_name)
                scope.set_context("operation_details", kwargs)
                
                try:
                    result = func(*args, **func_kwargs)
                    sentry_sdk.add_breadcrumb(
                        message=f"Operation {operation_name} completed successfully",
                        category="prp_agent",
                        level="info"
                    )
                    return result
                except Exception as e:
                    sentry_sdk.add_breadcrumb(
                        message=f"Operation {operation_name} failed: {str(e)}",
                        category="prp_agent",
                        level="error"
                    )
                    sentry_sdk.capture_exception(e)
                    raise
        return wrapper
    return decorator

def monitor_llm_interaction(model: str, prompt_type: str):
    """
    Monitora interações com LLM no contexto do PRP Agent
    """
    sentry_sdk.add_breadcrumb(
        message=f"LLM interaction started",
        category="llm",
        level="info",
        data={
            "model": model,
            "prompt_type": prompt_type,
            "timestamp": datetime.now().isoformat()
        }
    )

def monitor_mcp_call(tool_name: str, params: Dict[str, Any]):
    """
    Monitora chamadas MCP Tools
    """
    sentry_sdk.add_breadcrumb(
        message=f"MCP tool called: {tool_name}",
        category="mcp",
        level="info",
        data={
            "tool_name": tool_name,
            "params_count": len(params),
            "timestamp": datetime.now().isoformat()
        }
    )

def test_sentry_integration():
    """
    Testa a integração do Sentry com o PRP Agent
    """
    print("\n🧪 Testando integração Sentry para PRP Agent...")
    
    # 1. Capturar mensagem específica do projeto
    sentry_sdk.capture_message(
        "PRP Agent iniciado com integração Sentry", 
        level="info"
    )
    print("✅ Mensagem de inicialização enviada")
    
    # 2. Simular contexto de análise LLM
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("component", "llm_analysis")
        scope.set_context("analysis", {
            "prp_id": 123,
            "analysis_type": "task_extraction",
            "model": "gpt-4o"
        })
        
        monitor_llm_interaction("gpt-4o", "task_extraction")
        sentry_sdk.capture_message("Análise LLM concluída", level="info")
    print("✅ Contexto de análise LLM enviado")
    
    # 3. Simular chamada MCP
    monitor_mcp_call("mcp_turso_execute_query", {
        "query": "SELECT * FROM prps",
        "database": "context-memory"
    })
    print("✅ Monitoramento MCP configurado")
    
    # 4. Adicionar contexto do usuário
    sentry_sdk.set_user({
        "id": "prp-developer",
        "username": "dev",
        "agent_session": "prp-session-123"
    })
    print("✅ Contexto de usuário definido")
    
    # 5. Capturar performance de operação
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("operation", "prp_creation")
        
        import time
        start_time = time.time()
        time.sleep(0.1)  # Simular operação
        duration = time.time() - start_time
        
        scope.set_context("performance", {
            "operation": "prp_creation",
            "duration_ms": duration * 1000,
            "status": "success"
        })
        
        sentry_sdk.capture_message(
            f"PRP criado em {duration:.2f}s", 
            level="info"
        )
    print("✅ Monitoramento de performance configurado")

def setup_prp_agent_environment():
    """
    Configura ambiente específico para PRP Agent
    """
    # Configurar contexto do ambiente
    sentry_sdk.set_context("environment", {
        "python_version": os.sys.version,
        "working_directory": os.getcwd(),
        "has_openai_key": bool(os.getenv("LLM_API_KEY")),
        "database_exists": os.path.exists("../context-memory.db"),
        "mcp_servers_available": check_mcp_availability()
    })
    
    # Tags específicas do ambiente
    sentry_sdk.set_tag("python_version", f"{os.sys.version_info.major}.{os.sys.version_info.minor}")
    sentry_sdk.set_tag("has_database", os.path.exists("../context-memory.db"))
    
def check_mcp_availability() -> list:
    """
    Verifica quais servidores MCP estão disponíveis
    """
    available_mcps = []
    
    # Verificar MCP Turso
    try:
        # Simular verificação - em produção usar chamada real
        available_mcps.append("turso")
    except:
        pass
    
    # Verificar MCP Sentry  
    try:
        available_mcps.append("sentry")
    except:
        pass
    
    return available_mcps

def main():
    """
    Função principal - demonstração de uso
    """
    print("🚨 Configuração de Sentry para PRP Agent")
    print("=" * 50)
    
    # IMPORTANTE: Substitua pelo DSN do seu projeto Sentry
    DSN = "https://your-dsn-here@sentry.io/your-project-id"
    
    if DSN == "https://your-dsn-here@sentry.io/your-project-id":
        print("⚠️  AVISO: Configure o DSN do seu projeto Sentry!")
        print("   1. Crie um projeto no Sentry")
        print("   2. Copie o DSN do projeto")
        print("   3. Substitua a variável DSN neste arquivo")
        print("   4. Ou configure via variável de ambiente SENTRY_DSN")
        
        # Tentar obter DSN do ambiente
        DSN = os.getenv("SENTRY_DSN")
        if not DSN:
            print("   5. Configure SENTRY_DSN no arquivo .env")
            return
    
    # Configurar contexto do usuário específico para PRP Agent
    user_context = {
        "id": "prp-agent-user",
        "username": "developer",
        "session_id": f"prp-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    }
    
    # Configurar Sentry
    configure_sentry_for_prp_agent(
        dsn=DSN,
        environment="development",
        debug=True,
        user_context=user_context
    )
    
    # Configurar ambiente
    setup_prp_agent_environment()
    
    # Testar integração
    test_sentry_integration()
    
    print("\n🎉 Configuração de Sentry concluída para PRP Agent!")
    print("📊 Verifique os eventos no dashboard do Sentry")
    print("🔗 https://sentry.io/")

if __name__ == "__main__":
    main()