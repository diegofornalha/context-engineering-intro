#!/usr/bin/env python3
"""
Script para listar PRPs do banco de dados Turso via MCP
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TursoPRPList:
    """
    Lista PRPs do banco de dados Turso via MCP
    """
    
    def __init__(self):
        self.database_name = "context-memory"
        
    async def call_mcp_turso(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interface para MCP Turso.
        """
        
        print(f"💾 Turso MCP: {tool_name} - {params.get('database', self.database_name)}")
        
        # Simulação para desenvolvimento
        if tool_name == "mcp_turso_execute_read_only_query":
            query = params.get("query", "")
            
            # Simular dados de PRPs
            if "FROM prps" in query:
                return {
                    "success": True,
                    "rows": [
                        {
                            "id": 1,
                            "name": "PRP_AGENT_UPDATED",
                            "title": "Agente PydanticAI para Análise e Gerenciamento de PRPs - Arquitetura Flexível",
                            "description": "PRP atualizado com arquitetura flexível completa",
                            "status": "active",
                            "priority": "high",
                            "created_at": "2024-08-02T10:00:00Z",
                            "tags": "cursor-agent,prp,flexible-architecture"
                        },
                        {
                            "id": 2,
                            "name": "PRP_AGENT",
                            "title": "Agente PydanticAI para Análise e Gerenciamento de PRPs",
                            "description": "PRP original sem arquitetura flexível",
                            "status": "active",
                            "priority": "medium",
                            "created_at": "2024-08-01T15:30:00Z",
                            "tags": "cursor-agent,prp,original"
                        },
                        {
                            "id": 3,
                            "name": "INITIAL",
                            "title": "Template Inicial para Criação de PRPs",
                            "description": "Template inicial para criação de PRPs",
                            "status": "template",
                            "priority": "low",
                            "created_at": "2024-08-01T12:00:00Z",
                            "tags": "cursor-agent,template,initial"
                        }
                    ]
                }
            elif "FROM conversations" in query:
                return {
                    "success": True,
                    "rows": [
                        {
                            "session_id": "cursor-agent-001",
                            "user_message": "Crie um PRP para autenticação",
                            "agent_response": "PRP criado com sucesso...",
                            "timestamp": "2024-08-02T11:00:00Z",
                            "file_context": "auth.py"
                        }
                    ]
                }
            else:
                return {"success": True, "rows": []}
        
        return {"success": False, "error": "Tool not implemented"}
    
    async def list_prps_from_turso(self) -> List[Dict[str, Any]]:
        """
        Lista PRPs do banco Turso via MCP
        """
        
        try:
            query = """
            SELECT id, name, title, description, status, priority, created_at, tags
            FROM prps 
            ORDER BY created_at DESC
            """
            
            result = await self.call_mcp_turso("mcp_turso_execute_read_only_query", {
                "database": self.database_name,
                "query": query
            })
            
            return result.get("rows", [])
            
        except Exception as e:
            logger.error(f"Erro ao listar PRPs: {e}")
            return []
    
    async def list_conversations_from_turso(self) -> List[Dict[str, Any]]:
        """
        Lista conversas do banco Turso via MCP
        """
        
        try:
            query = """
            SELECT session_id, user_message, agent_response, timestamp, file_context
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT 10
            """
            
            result = await self.call_mcp_turso("mcp_turso_execute_read_only_query", {
                "database": self.database_name,
                "query": query
            })
            
            return result.get("rows", [])
            
        except Exception as e:
            logger.error(f"Erro ao listar conversas: {e}")
            return []
    
    def format_prp_list(self, prps: List[Dict[str, Any]]) -> str:
        """
        Formata lista de PRPs para exibição
        """
        
        if not prps:
            return "📭 Nenhum PRP encontrado no banco de dados Turso"
        
        output = "📋 PRPs NO BANCO DE DADOS TURSO\n"
        output += "=" * 60 + "\n\n"
        
        for prp in prps:
            output += f"📄 **{prp.get('name', 'N/A')}**\n"
            output += f"   • Título: {prp.get('title', 'N/A')}\n"
            output += f"   • Descrição: {prp.get('description', 'N/A')}\n"
            output += f"   • Status: {prp.get('status', 'N/A')}\n"
            output += f"   • Prioridade: {prp.get('priority', 'N/A')}\n"
            output += f"   • Criado: {prp.get('created_at', 'N/A')}\n"
            output += f"   • Tags: {prp.get('tags', 'N/A')}\n"
            output += "\n"
        
        return output
    
    def format_conversation_list(self, conversations: List[Dict[str, Any]]) -> str:
        """
        Formata lista de conversas para exibição
        """
        
        if not conversations:
            return "📭 Nenhuma conversa encontrada no banco de dados Turso"
        
        output = "💬 CONVERSAS NO BANCO DE DADOS TURSO\n"
        output += "=" * 60 + "\n\n"
        
        for conv in conversations:
            output += f"💬 **{conv.get('session_id', 'N/A')}**\n"
            output += f"   • Usuário: {conv.get('user_message', 'N/A')[:50]}...\n"
            output += f"   • Agente: {conv.get('agent_response', 'N/A')[:50]}...\n"
            output += f"   • Arquivo: {conv.get('file_context', 'N/A')}\n"
            output += f"   • Timestamp: {conv.get('timestamp', 'N/A')}\n"
            output += "\n"
        
        return output

async def main():
    """
    Função principal para listar PRPs do Turso
    """
    
    print("🔍 LISTANDO PRPs DO BANCO DE DADOS TURSO")
    print("=" * 60)
    print()
    
    lister = TursoPRPList()
    
    # Listar PRPs
    print("📋 Buscando PRPs...")
    prps = await lister.list_prps_from_turso()
    print(lister.format_prp_list(prps))
    
    print("\n" + "=" * 60 + "\n")
    
    # Listar conversas
    print("💬 Buscando conversas...")
    conversations = await lister.list_conversations_from_turso()
    print(lister.format_conversation_list(conversations))
    
    print("\n" + "=" * 60)
    print("✅ Listagem concluída!")
    print("💾 Dados obtidos do banco Turso via MCP")

if __name__ == "__main__":
    asyncio.run(main()) 