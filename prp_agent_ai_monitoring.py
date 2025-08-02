#!/usr/bin/env python3
"""
🔗 Integração PRP Agent com Sentry AI Agent Monitoring
====================================================

Integração específica dos agentes PydanticAI do PRP com o 
Sentry AI Agent Monitoring (Beta) para rastreamento completo
de workflows de IA.
"""

import sentry_sdk
import asyncio
import functools
import time
import uuid
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from sentry_ai_agent_setup import (
    start_ai_agent_run, 
    track_llm_call, 
    track_tool_execution,
    track_agent_decision,
    end_ai_agent_run
)

class PRPAgentAIMonitoring:
    """
    Classe para integração completa do PRP Agent com Sentry AI Agent Monitoring
    """
    
    def __init__(self, dsn: str, environment: str = "development", agent_name: str = "prp-agent"):
        """
        Inicializa monitoramento de AI Agent para PRP
        
        Args:
            dsn: Sentry DSN
            environment: Ambiente de execução
            agent_name: Nome do agente para rastreamento
        """
        self.dsn = dsn
        self.environment = environment
        self.agent_name = agent_name
        self.current_run_id = None
        self.setup_ai_agent_monitoring()
    
    def setup_ai_agent_monitoring(self):
        """Configura Sentry AI Agent Monitoring"""
        from sentry_ai_agent_setup import configure_sentry_ai_agent_monitoring
        
        configure_sentry_ai_agent_monitoring(
            dsn=self.dsn,
            environment=self.environment,
            debug=True if self.environment == "development" else False,
            agent_name=self.agent_name
        )
    
    def monitor_agent_conversation(self, conversation_id: Optional[str] = None):
        """
        Decorator para monitorar conversas completas do agente
        
        Args:
            conversation_id: ID da conversa (opcional)
        """
        def decorator(func):
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    # Gerar ID único para este run
                    run_id = conversation_id or f"conv-{uuid.uuid4().hex[:8]}"
                    self.current_run_id = run_id
                    
                    # Extrair input do usuário
                    user_input = args[0] if args else kwargs.get('message', 'No input')
                    
                    # Iniciar monitoramento do workflow
                    start_ai_agent_run(self.agent_name, run_id, user_input)
                    
                    start_time = time.time()
                    
                    try:
                        # Executar função do agente
                        result = await func(*args, **kwargs)
                        
                        # Sucesso - finalizar monitoramento
                        duration = time.time() - start_time
                        output_length = len(str(result)) if result else 0
                        
                        end_ai_agent_run(run_id, True, output_length)
                        
                        # Capturar métricas de performance
                        self._capture_performance_metrics(duration, output_length, True)
                        
                        return result
                        
                    except Exception as e:
                        # Erro - finalizar com falha
                        duration = time.time() - start_time
                        end_ai_agent_run(run_id, False, error=str(e))
                        
                        # Capturar erro específico
                        sentry_sdk.capture_exception(e)
                        self._capture_performance_metrics(duration, 0, False)
                        
                        raise
                    finally:
                        self.current_run_id = None
                
                return async_wrapper
            else:
                @functools.wraps(func)
                def sync_wrapper(*args, **kwargs):
                    # Implementação similar para funções síncronas
                    run_id = conversation_id or f"conv-{uuid.uuid4().hex[:8]}"
                    self.current_run_id = run_id
                    
                    user_input = args[0] if args else kwargs.get('message', 'No input')
                    start_ai_agent_run(self.agent_name, run_id, user_input)
                    
                    start_time = time.time()
                    
                    try:
                        result = func(*args, **kwargs)
                        duration = time.time() - start_time
                        output_length = len(str(result)) if result else 0
                        
                        end_ai_agent_run(run_id, True, output_length)
                        self._capture_performance_metrics(duration, output_length, True)
                        
                        return result
                    except Exception as e:
                        duration = time.time() - start_time
                        end_ai_agent_run(run_id, False, error=str(e))
                        sentry_sdk.capture_exception(e)
                        self._capture_performance_metrics(duration, 0, False)
                        raise
                    finally:
                        self.current_run_id = None
                
                return sync_wrapper
        return decorator
    
    def track_llm_interaction(self, model: str, prompt_type: str, tokens_used: Optional[int] = None, cost: Optional[float] = None):
        """
        Rastreia interações com LLM durante o workflow
        """
        track_llm_call(model, prompt_type, tokens_used, cost)
        
        # Contexto adicional para esta chamada LLM
        with sentry_sdk.configure_scope() as scope:
            scope.set_context("current_llm_call", {
                "model": model,
                "prompt_type": prompt_type,
                "run_id": self.current_run_id,
                "timestamp": datetime.now().isoformat()
            })
    
    def track_mcp_tool_call(self, tool_name: str, params: Dict[str, Any], duration: float, success: bool):
        """
        Rastreia chamadas para ferramentas MCP
        """
        track_tool_execution(tool_name, params, duration, success)
        
        # Contexto específico para MCP
        sentry_sdk.add_breadcrumb(
            message=f"MCP tool call: {tool_name}",
            category="mcp_tool",
            level="info" if success else "error",
            data={
                "tool_name": tool_name,
                "mcp_type": "turso" if "turso" in tool_name.lower() else "other",
                "params_keys": list(params.keys()),
                "success": success,
                "duration_ms": duration * 1000,
                "run_id": self.current_run_id
            }
        )
    
    def track_prp_operation(self, operation_type: str, prp_data: Dict[str, Any], success: bool):
        """
        Rastreia operações específicas de PRPs
        """
        track_agent_decision(
            decision_type=f"prp_{operation_type}",
            reasoning=f"Executing PRP operation: {operation_type}",
            confidence=0.9
        )
        
        # Contexto específico para PRPs
        with sentry_sdk.configure_scope() as scope:
            scope.set_context("prp_operation", {
                "operation": operation_type,
                "prp_id": prp_data.get("id"),
                "prp_name": prp_data.get("name"),
                "success": success,
                "run_id": self.current_run_id
            })
    
    def track_database_query(self, query_type: str, table: str, duration: float, success: bool):
        """
        Rastreia queries de banco de dados
        """
        track_tool_execution(
            tool_name=f"database_{query_type.lower()}",
            params={"table": table, "type": query_type},
            duration=duration,
            success=success
        )
    
    def _capture_performance_metrics(self, duration: float, output_length: int, success: bool):
        """
        Captura métricas de performance do agente
        """
        sentry_sdk.capture_message(
            f"Agent performance metrics",
            level="info",
            extras={
                "agent_name": self.agent_name,
                "duration_seconds": duration,
                "output_length": output_length,
                "success": success,
                "run_id": self.current_run_id,
                "performance_category": "fast" if duration < 5 else "slow",
                "timestamp": datetime.now().isoformat()
            }
        )

# Wrapper para agentes PRP existentes
class AIMonitoredPRPAgent:
    """
    Wrapper para agentes PRP existentes com AI Monitoring integrado
    """
    
    def __init__(self, sentry_dsn: str, environment: str = "development"):
        self.ai_monitoring = PRPAgentAIMonitoring(sentry_dsn, environment)
    
    @property
    def monitor_conversation(self):
        """Decorator para monitorar conversas"""
        return self.ai_monitoring.monitor_agent_conversation
    
    async def chat_with_ai_monitoring(self, message: str, **kwargs):
        """
        Chat com AI Agent Monitoring completo
        """
        # Importar função de chat existente
        try:
            from agents.agent import chat_with_prp_agent
        except ImportError:
            print("⚠️  Função chat_with_prp_agent não encontrada")
            return "Erro: Agente não configurado"
        
        # Aplicar monitoramento
        @self.ai_monitoring.monitor_agent_conversation()
        async def monitored_chat(msg):
            # Rastrear início da interação LLM
            self.ai_monitoring.track_llm_interaction("gpt-4o", "user_message")
            
            # Executar chat
            result = await chat_with_prp_agent(msg, **kwargs)
            
            # Rastrear finalização
            self.ai_monitoring.track_llm_interaction("gpt-4o", "assistant_response")
            
            return result
        
        return await monitored_chat(message)
    
    async def create_prp_with_ai_monitoring(self, name: str, title: str, **kwargs):
        """
        Criação de PRP com AI Monitoring
        """
        try:
            from agents.tools import create_prp
        except ImportError:
            print("⚠️  Função create_prp não encontrada")
            return "Erro: Ferramenta não configurada"
        
        start_time = time.time()
        
        try:
            # Rastrear operação PRP
            self.ai_monitoring.track_prp_operation("create", {"name": name, "title": title}, True)
            
            # Executar criação
            result = await create_prp(None, name, title, **kwargs)
            
            # Rastrear database operation
            duration = time.time() - start_time
            self.ai_monitoring.track_database_query("INSERT", "prps", duration, True)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.ai_monitoring.track_database_query("INSERT", "prps", duration, False)
            raise

def demo_ai_agent_monitoring():
    """
    Demonstração do AI Agent Monitoring com PRP Agent
    """
    print("🤖 Demo: Sentry AI Agent Monitoring + PRP Agent")
    print("=" * 50)
    
    # Configurar DSN
    SENTRY_DSN = os.getenv("SENTRY_DSN", "https://your-dsn@sentry.io/project-id")
    
    if "your-dsn" in SENTRY_DSN:
        print("⚠️  Configure SENTRY_DSN primeiro!")
        print("   1. Crie projeto no Sentry")
        print("   2. Habilite 'AI Agent Monitoring' (Beta)")
        print("   3. Configure DSN: export SENTRY_DSN='seu-dsn'")
        return
    
    # Criar agente com AI Monitoring
    ai_agent = AIMonitoredPRPAgent(SENTRY_DSN, "development")
    
    print("✅ PRP Agent com AI Agent Monitoring criado")
    print("🔗 Acesse: https://sentry.io/ → AI Agents")
    print("📊 Visualize workflows completos dos agentes")

if __name__ == "__main__":
    import os
    demo_ai_agent_monitoring()