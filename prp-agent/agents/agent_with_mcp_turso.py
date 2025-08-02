#!/usr/bin/env python3
"""
Agente PRP com integração MCP Turso REAL.

Este arquivo mostra como o agente DEVERIA funcionar:
1. BUSCAR contexto no MCP Turso antes de responder
2. INCLUIR contexto na resposta
3. SALVAR conversa no MCP Turso
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Imports do agente original
from .agent import prp_agent
from .dependencies import PRPAgentDependencies
from .providers import get_llm_model, get_test_model

logger = logging.getLogger(__name__)


class PRPAgentWithMCPTurso:
    """Agente PRP com integração MCP Turso para contexto inteligente."""
    
    def __init__(self, database: str = "context-memory"):
        self.database = database
        self.mcp_available = self._check_mcp_availability()
        
    def _check_mcp_availability(self) -> bool:
        """Verifica se MCP Turso está disponível."""
        try:
            # Tentar importar as ferramentas MCP
            import mcp_turso_execute_read_only_query
            import mcp_turso_add_conversation
            import mcp_turso_search_knowledge
            return True
        except ImportError:
            logger.warning("🚨 MCP Turso não disponível - funcionando sem contexto")
            return False
    
    async def search_relevant_context(self, message: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Busca contexto relevante no MCP Turso baseado na mensagem.
        
        Args:
            message: Mensagem do usuário
            limit: Limite de resultados
            
        Returns:
            Lista de contextos relevantes
        """
        if not self.mcp_available:
            return []
            
        try:
            # 1. Buscar em documentação
            docs_query = f"""
            SELECT title, content, summary, cluster_name 
            FROM docs 
            WHERE content LIKE '%{message[:50]}%' 
            OR summary LIKE '%{message[:50]}%'
            OR keywords LIKE '%{message[:50]}%'
            ORDER BY relevance_score DESC 
            LIMIT {limit}
            """
            
            # Simular chamada MCP (seria real no Cursor Agent)
            docs_result = await self._execute_mcp_query(docs_query)
            
            # 2. Buscar conversas anteriores
            conversations_query = f"""
            SELECT message, response, context, timestamp
            FROM conversations 
            WHERE message LIKE '%{message[:50]}%'
            OR response LIKE '%{message[:50]}%'
            ORDER BY timestamp DESC
            LIMIT {limit}
            """
            
            conv_result = await self._execute_mcp_query(conversations_query)
            
            # 3. Buscar PRPs relacionados
            prps_query = f"""
            SELECT name, title, description, objective, status
            FROM prps
            WHERE description LIKE '%{message[:50]}%'
            OR title LIKE '%{message[:50]}%'
            ORDER BY created_at DESC
            LIMIT {limit}
            """
            
            prps_result = await self._execute_mcp_query(prps_query)
            
            # Combinar resultados
            context = []
            
            if docs_result:
                context.append({
                    "type": "documentation",
                    "data": docs_result,
                    "relevance": "high"
                })
                
            if conv_result:
                context.append({
                    "type": "conversation_history", 
                    "data": conv_result,
                    "relevance": "medium"
                })
                
            if prps_result:
                context.append({
                    "type": "prps",
                    "data": prps_result,
                    "relevance": "high"
                })
            
            return context
            
        except Exception as e:
            logger.error(f"Erro ao buscar contexto MCP: {e}")
            return []
    
    async def _execute_mcp_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa query no MCP Turso (simulado aqui, real no Cursor)."""
        
        # NO CURSOR AGENT, isto seria:
        # from mcp_turso import execute_read_only_query
        # return execute_read_only_query(query=query, database=self.database)
        
        # Para desenvolvimento, simular alguns resultados
        if "docs" in query.lower():
            return [
                {
                    "title": "Guia de Uso PRP Agent",
                    "content": "O PRP Agent é um sistema de análise de Product Requirement Prompts...",
                    "summary": "Guia completo de uso do PRP Agent",
                    "cluster_name": "GETTING_STARTED"
                }
            ]
        elif "conversations" in query.lower():
            return [
                {
                    "message": "Como usar o PRP Agent?",
                    "response": "O PRP Agent funciona analisando PRPs e extraindo tarefas...",
                    "context": "primeira_vez_usuario",
                    "timestamp": "2025-01-02T10:00:00"
                }
            ]
        elif "prps" in query.lower():
            return [
                {
                    "name": "prp_agent_intro",
                    "title": "Introdução ao PRP Agent", 
                    "description": "Sistema para análise de PRPs com IA",
                    "objective": "Facilitar gerenciamento de requisitos",
                    "status": "active"
                }
            ]
        
        return []
    
    def format_context_for_prompt(self, context: List[Dict[str, Any]]) -> str:
        """Formata contexto para incluir no prompt do agente."""
        
        if not context:
            return ""
            
        context_text = "\n🧠 **CONTEXTO RELEVANTE ENCONTRADO NO TURSO:**\n"
        
        for ctx in context:
            ctx_type = ctx.get("type", "unknown")
            ctx_data = ctx.get("data", [])
            relevance = ctx.get("relevance", "unknown")
            
            context_text += f"\n📋 **{ctx_type.upper()}** (Relevância: {relevance}):\n"
            
            for item in ctx_data[:2]:  # Máximo 2 itens por tipo
                if ctx_type == "documentation":
                    context_text += f"- 📚 {item.get('title', 'N/A')}: {item.get('summary', 'N/A')}\n"
                elif ctx_type == "conversation_history":
                    context_text += f"- 💬 Pergunta anterior: {item.get('message', 'N/A')[:100]}...\n"
                elif ctx_type == "prps":
                    context_text += f"- 🎯 PRP: {item.get('title', 'N/A')} - {item.get('description', 'N/A')[:100]}...\n"
        
        context_text += "\n📝 **Use este contexto para fornecer uma resposta mais informada.**\n\n"
        
        return context_text
    
    async def save_conversation_to_mcp(self, message: str, response: str, context: str = None) -> bool:
        """Salva conversa no MCP Turso."""
        
        if not self.mcp_available:
            return False
            
        try:
            # NO CURSOR AGENT, isto seria:
            # from mcp_turso import add_conversation
            # result = add_conversation(
            #     session_id="prp-agent-session",
            #     message=message,
            #     response=response,
            #     context=context,
            #     database=self.database
            # )
            
            # Para desenvolvimento, simular sucesso
            logger.info(f"💾 [SIMULADO] Conversa salva no MCP Turso: {message[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar no MCP: {e}")
            return False
    
    async def chat_with_mcp_context(
        self, 
        message: str, 
        deps: PRPAgentDependencies = None,
        use_test_model: bool = False
    ) -> str:
        """
        Conversa com agente INCLUINDO contexto do MCP Turso.
        
        ESTE É O MÉTODO CORRETO que deveria ser usado!
        """
        if deps is None:
            deps = PRPAgentDependencies()
        
        try:
            # 🔍 PASSO 1: Buscar contexto relevante no MCP Turso
            logger.info(f"🔍 Buscando contexto no MCP Turso para: {message[:50]}...")
            context = await self.search_relevant_context(message)
            
            # 📝 PASSO 2: Formatar contexto
            context_text = self.format_context_for_prompt(context)
            
            # 🤖 PASSO 3: Preparar mensagem com contexto
            enhanced_message = f"{context_text}\n**PERGUNTA DO USUÁRIO:**\n{message}"
            
            # 🧠 PASSO 4: Executar agente com contexto
            if use_test_model:
                test_model = get_test_model()
                with prp_agent.override(model=test_model):
                    result = await prp_agent.run(enhanced_message, deps=deps)
            else:
                result = await prp_agent.run(enhanced_message, deps=deps)
            
            response = result.data
            
            # 💾 PASSO 5: Salvar conversa no MCP Turso
            await self.save_conversation_to_mcp(
                message=message, 
                response=response,
                context=f"mcp_context_items: {len(context)}"
            )
            
            # 📊 PASSO 6: Adicionar informações sobre contexto usado
            if context:
                context_info = f"\n\n🧠 **Contexto usado:** {len(context)} item(s) do Turso"
                response += context_info
            
            return response
            
        except Exception as e:
            logger.error(f"Erro na conversa com MCP: {e}")
            return f"❌ Erro interno do agente com MCP: {str(e)}"


# 🚀 FUNÇÕES PÚBLICAS - Como deveria ser usado
async def chat_with_prp_agent_mcp(
    message: str, 
    deps: PRPAgentDependencies = None,
    use_test_model: bool = False
) -> str:
    """
    Conversa com agente PRP usando MCP Turso para contexto.
    
    ESTA deveria ser a função principal chamada pelo CLI!
    """
    agent = PRPAgentWithMCPTurso()
    return await agent.chat_with_mcp_context(message, deps, use_test_model)


def chat_with_prp_agent_mcp_sync(
    message: str, 
    deps: PRPAgentDependencies = None,
    use_test_model: bool = False
) -> str:
    """Versão síncrona da conversa com MCP."""
    return asyncio.run(chat_with_prp_agent_mcp(message, deps, use_test_model))


# 🎯 EXEMPLO DE USO
async def demo_mcp_integration():
    """Demonstra como deveria funcionar com MCP."""
    
    print("🧪 DEMO: Agente PRP com MCP Turso")
    print("=" * 50)
    
    # Criar agente com MCP
    agent = PRPAgentWithMCPTurso()
    
    # Teste 1: Pergunta sobre projeto
    print("\n1️⃣ Pergunta sobre projeto:")
    response1 = await agent.chat_with_mcp_context(
        "O que é este projeto e como começar?"
    )
    print(f"Resposta: {response1[:200]}...")
    
    # Teste 2: Pergunta técnica
    print("\n2️⃣ Pergunta técnica:")
    response2 = await agent.chat_with_mcp_context(
        "Como criar um PRP para sistema de autenticação?"
    )
    print(f"Resposta: {response2[:200]}...")
    
    print("\n✅ Demo concluída!")


if __name__ == "__main__":
    asyncio.run(demo_mcp_integration())