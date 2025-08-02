#!/usr/bin/env python3
"""
🔗 Integração Sentry com Agentes PRP
===================================

Integração específica do Sentry com os agentes PydanticAI do projeto PRP,
incluindo monitoramento de operações LLM, MCP Tools e análises de PRPs.
"""

import sentry_sdk
import asyncio
import functools
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import traceback
import json

class PRPAgentSentryIntegration:
    """
    Classe para integração específica do Sentry com agentes PRP
    """
    
    def __init__(self, dsn: str, environment: str = "development"):
        """
        Inicializa a integração Sentry para PRP Agent
        
        Args:
            dsn: Sentry DSN
            environment: Ambiente de execução
        """
        self.dsn = dsn
        self.environment = environment
        self.setup_sentry()
    
    def setup_sentry(self):
        """Configura Sentry com configurações específicas do PRP Agent"""
        from sentry_prp_agent_setup import configure_sentry_for_prp_agent
        
        configure_sentry_for_prp_agent(
            dsn=self.dsn,
            environment=self.environment,
            debug=True if self.environment == "development" else False
        )
    
    def monitor_agent_operation(self, operation_name: str, **context):
        """
        Decorator para monitorar operações de agentes PRP
        
        Args:
            operation_name: Nome da operação sendo monitorada
            **context: Contexto adicional para a operação
        """
        def decorator(func):
            if asyncio.iscoroutinefunction(func):
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    with sentry_sdk.configure_scope() as scope:
                        scope.set_tag("agent_operation", operation_name)
                        scope.set_context("operation_context", context)
                        
                        start_time = datetime.now()
                        
                        try:
                            result = await func(*args, **kwargs)
                            
                            # Registrar sucesso
                            duration = (datetime.now() - start_time).total_seconds()
                            self._log_operation_success(operation_name, duration, context)
                            
                            return result
                        except Exception as e:
                            # Registrar erro
                            duration = (datetime.now() - start_time).total_seconds()
                            self._log_operation_error(operation_name, e, duration, context)
                            raise
                return async_wrapper
            else:
                @functools.wraps(func)
                def sync_wrapper(*args, **kwargs):
                    with sentry_sdk.configure_scope() as scope:
                        scope.set_tag("agent_operation", operation_name)
                        scope.set_context("operation_context", context)
                        
                        start_time = datetime.now()
                        
                        try:
                            result = func(*args, **kwargs)
                            
                            # Registrar sucesso
                            duration = (datetime.now() - start_time).total_seconds()
                            self._log_operation_success(operation_name, duration, context)
                            
                            return result
                        except Exception as e:
                            # Registrar erro
                            duration = (datetime.now() - start_time).total_seconds()
                            self._log_operation_error(operation_name, e, duration, context)
                            raise
                return sync_wrapper
        return decorator
    
    def monitor_llm_call(self, model: str, prompt_type: str, tokens_used: Optional[int] = None):
        """
        Monitora chamadas para LLM
        
        Args:
            model: Modelo LLM usado
            prompt_type: Tipo de prompt (system, user, analysis, etc.)
            tokens_used: Número de tokens utilizados
        """
        sentry_sdk.add_breadcrumb(
            message=f"LLM call: {model}",
            category="llm",
            level="info",
            data={
                "model": model,
                "prompt_type": prompt_type,
                "tokens_used": tokens_used,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def monitor_mcp_tool_call(self, tool_name: str, params: Dict[str, Any], success: bool = True):
        """
        Monitora chamadas para ferramentas MCP
        
        Args:
            tool_name: Nome da ferramenta MCP
            params: Parâmetros passados para a ferramenta
            success: Se a chamada foi bem-sucedida
        """
        sentry_sdk.add_breadcrumb(
            message=f"MCP tool call: {tool_name}",
            category="mcp",
            level="info" if success else "error",
            data={
                "tool_name": tool_name,
                "params_keys": list(params.keys()) if params else [],
                "success": success,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def monitor_prp_operation(self, prp_id: Optional[int], operation: str, details: Dict[str, Any]):
        """
        Monitora operações específicas de PRPs
        
        Args:
            prp_id: ID do PRP (se aplicável)
            operation: Tipo de operação (create, update, analyze, etc.)
            details: Detalhes da operação
        """
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("prp_operation", operation)
            scope.set_context("prp_details", {
                "prp_id": prp_id,
                "operation": operation,
                **details
            })
            
            sentry_sdk.add_breadcrumb(
                message=f"PRP operation: {operation}",
                category="prp",
                level="info",
                data={
                    "prp_id": prp_id,
                    "operation": operation,
                    "timestamp": datetime.now().isoformat()
                }
            )
    
    def monitor_database_operation(self, query_type: str, table: str, success: bool = True):
        """
        Monitora operações de banco de dados
        
        Args:
            query_type: Tipo de query (SELECT, INSERT, UPDATE, DELETE)
            table: Tabela afetada
            success: Se a operação foi bem-sucedida
        """
        sentry_sdk.add_breadcrumb(
            message=f"Database operation: {query_type} on {table}",
            category="database",
            level="info" if success else "error",
            data={
                "query_type": query_type,
                "table": table,
                "success": success,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def set_user_context(self, session_id: str, user_id: Optional[str] = None):
        """
        Define contexto do usuário para a sessão
        
        Args:
            session_id: ID da sessão
            user_id: ID do usuário (opcional)
        """
        sentry_sdk.set_user({
            "id": user_id or f"session-{session_id}",
            "session_id": session_id,
            "agent_type": "prp-agent"
        })
    
    def capture_prp_analysis_result(self, prp_id: int, analysis_type: str, result: Dict[str, Any]):
        """
        Captura resultado de análise de PRP para métricas
        
        Args:
            prp_id: ID do PRP analisado
            analysis_type: Tipo de análise realizada
            result: Resultado da análise
        """
        sentry_sdk.capture_message(
            f"PRP analysis completed: {analysis_type}",
            level="info",
            extras={
                "prp_id": prp_id,
                "analysis_type": analysis_type,
                "result_summary": self._summarize_analysis_result(result),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def capture_agent_performance_metrics(self, agent_name: str, metrics: Dict[str, Any]):
        """
        Captura métricas de performance do agente
        
        Args:
            agent_name: Nome do agente
            metrics: Métricas coletadas
        """
        with sentry_sdk.configure_scope() as scope:
            scope.set_context("performance_metrics", {
                "agent_name": agent_name,
                **metrics
            })
            
            sentry_sdk.capture_message(
                f"Agent performance metrics: {agent_name}",
                level="info"
            )
    
    def _log_operation_success(self, operation_name: str, duration: float, context: Dict[str, Any]):
        """Registra sucesso de operação"""
        sentry_sdk.add_breadcrumb(
            message=f"Operation {operation_name} completed successfully",
            category="operation",
            level="info",
            data={
                "duration_seconds": duration,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _log_operation_error(self, operation_name: str, error: Exception, duration: float, context: Dict[str, Any]):
        """Registra erro de operação"""
        sentry_sdk.add_breadcrumb(
            message=f"Operation {operation_name} failed",
            category="operation",
            level="error",
            data={
                "error": str(error),
                "duration_seconds": duration,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Capturar a exceção
        sentry_sdk.capture_exception(error)
    
    def _summarize_analysis_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Cria resumo do resultado de análise para evitar dados sensíveis"""
        return {
            "keys": list(result.keys()),
            "data_types": {k: type(v).__name__ for k, v in result.items()},
            "size": len(str(result))
        }

# Exemplo de uso com os agentes existentes
class SentryEnhancedPRPAgent:
    """
    Wrapper para agentes PRP com monitoramento Sentry integrado
    """
    
    def __init__(self, sentry_dsn: str, environment: str = "development"):
        self.sentry = PRPAgentSentryIntegration(sentry_dsn, environment)
    
    @property
    def monitor_agent_operation(self):
        """Decorator para monitorar operações de agente"""
        return self.sentry.monitor_agent_operation
    
    def setup_session(self, session_id: str, user_id: Optional[str] = None):
        """Configura sessão com contexto Sentry"""
        self.sentry.set_user_context(session_id, user_id)
    
    async def chat_with_monitoring(self, message: str, **kwargs):
        """
        Chat com monitoramento Sentry integrado
        """
        # Importar função de chat existente
        from agents.agent import chat_with_prp_agent
        
        # Monitorar a operação
        self.sentry.monitor_llm_call("gpt-4o", "chat", None)
        
        try:
            result = await chat_with_prp_agent(message, **kwargs)
            
            # Registrar sucesso
            self.sentry.monitor_prp_operation(
                prp_id=None,
                operation="chat",
                details={"message_length": len(message)}
            )
            
            return result
        except Exception as e:
            # Registrar erro
            sentry_sdk.capture_exception(e)
            raise
    
    async def create_prp_with_monitoring(self, name: str, title: str, **kwargs):
        """
        Criação de PRP com monitoramento Sentry
        """
        from agents.tools import create_prp
        
        try:
            # Monitorar operação
            self.sentry.monitor_prp_operation(
                prp_id=None,
                operation="create",
                details={"name": name, "title": title}
            )
            
            # Executar criação
            result = await create_prp(None, name, title, **kwargs)
            
            # Registrar sucesso
            self.sentry.monitor_database_operation("INSERT", "prps", True)
            
            return result
        except Exception as e:
            # Registrar erro
            self.sentry.monitor_database_operation("INSERT", "prps", False)
            sentry_sdk.capture_exception(e)
            raise

def demo_sentry_integration():
    """
    Demonstração da integração Sentry com PRP Agent
    """
    print("🚨 Demo: Integração Sentry com PRP Agent")
    print("=" * 45)
    
    # Configurar DSN (substitua pelo seu)
    SENTRY_DSN = "https://your-dsn@sentry.io/project-id"
    
    if SENTRY_DSN == "https://your-dsn@sentry.io/project-id":
        print("⚠️  Configure o SENTRY_DSN primeiro!")
        return
    
    # Criar agente com monitoramento
    agent = SentryEnhancedPRPAgent(SENTRY_DSN, "development")
    
    # Configurar sessão
    agent.setup_session("demo-session-123", "developer")
    
    print("✅ Agente PRP com monitoramento Sentry criado")
    print("📊 Verifique os eventos no dashboard do Sentry")

if __name__ == "__main__":
    demo_sentry_integration()