#!/usr/bin/env python3
"""
Script que usa o Cursor Agent com MCP Turso real para listar PRPs
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealCursorTursoList:
    """
    Lista PRPs usando Cursor Agent com MCP Turso real
    """
    
    def __init__(self):
        self.database_name = "context-memory"
        
    async def call_mcp_turso_real(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chama MCP Turso real via Cursor Agent
        """
        
        try:
            # Importar o agente real
            from cursor_turso_integration import CursorTursoIntegration
            
            # Criar instância do agente
            agent = CursorTursoIntegration()
            
            print(f"🔌 Chamando MCP Turso real via Cursor Agent: {tool_name}")
            
            # Usar o método do agente para chamar MCP
            result = await agent.call_mcp_turso(tool_name, params)
            
            return result
                
        except Exception as e:
            print(f"❌ Erro ao chamar MCP via Cursor Agent: {e}")
            return {"success": False, "error": str(e)}
    
    async def list_prps_from_real_turso(self) -> List[Dict[str, Any]]:
        """
        Lista PRPs do banco Turso real via MCP
        """
        
        try:
            query = """
            SELECT id, name, title, description, status, priority, created_at, tags
            FROM prps 
            ORDER BY created_at DESC
            """
            
            result = await self.call_mcp_turso_real("mcp_turso_execute_read_only_query", {
                "database": self.database_name,
                "query": query
            })
            
            if result.get("success"):
                return result.get("rows", [])
            else:
                print(f"❌ Erro ao listar PRPs: {result.get('error')}")
                return []
            
        except Exception as e:
            logger.error(f"Erro ao listar PRPs: {e}")
            return []
    
    async def list_conversations_from_real_turso(self) -> List[Dict[str, Any]]:
        """
        Lista conversas do banco Turso real via MCP
        """
        
        try:
            query = """
            SELECT session_id, user_message, agent_response, timestamp, file_context
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT 10
            """
            
            result = await self.call_mcp_turso_real("mcp_turso_execute_read_only_query", {
                "database": self.database_name,
                "query": query
            })
            
            if result.get("success"):
                return result.get("rows", [])
            else:
                print(f"❌ Erro ao listar conversas: {result.get('error')}")
                return []
            
        except Exception as e:
            logger.error(f"Erro ao listar conversas: {e}")
            return []
    
    async def create_sample_prp(self) -> bool:
        """
        Cria um PRP de exemplo no banco real
        """
        
        try:
            query = """
            INSERT INTO prps (name, title, description, status, priority, created_at, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            params = [
                "PRP_EXAMPLE_REAL",
                "PRP de Exemplo Real",
                "PRP criado via Cursor Agent com MCP Turso real",
                "active",
                "high",
                "2024-08-02T15:30:00Z",
                "cursor-agent,real,mcp-turso"
            ]
            
            result = await self.call_mcp_turso_real("mcp_turso_execute_query", {
                "database": self.database_name,
                "query": query,
                "params": params
            })
            
            if result.get("success"):
                print("✅ PRP de exemplo criado com sucesso!")
                return True
            else:
                print(f"❌ Erro ao criar PRP: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao criar PRP: {e}")
            return False
    
    def format_prp_list(self, prps: List[Dict[str, Any]]) -> str:
        """
        Formata lista de PRPs para exibição
        """
        
        if not prps:
            return "📭 Nenhum PRP encontrado no banco de dados Turso real"
        
        output = "📋 PRPs NO BANCO DE DADOS TURSO REAL\n"
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
            return "📭 Nenhuma conversa encontrada no banco de dados Turso real"
        
        output = "💬 CONVERSAS NO BANCO DE DADOS TURSO REAL\n"
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
    Função principal para listar PRPs do Turso real via Cursor Agent
    """
    
    print("🔍 LISTANDO PRPs VIA CURSOR AGENT COM MCP TURSO REAL")
    print("=" * 60)
    print()
    
    lister = RealCursorTursoList()
    
    # Criar PRP de exemplo primeiro
    print("📝 Criando PRP de exemplo no banco real...")
    await lister.create_sample_prp()
    print()
    
    # Listar PRPs
    print("📋 Buscando PRPs do banco real...")
    prps = await lister.list_prps_from_real_turso()
    print(lister.format_prp_list(prps))
    
    print("\n" + "=" * 60 + "\n")
    
    # Listar conversas
    print("💬 Buscando conversas do banco real...")
    conversations = await lister.list_conversations_from_real_turso()
    print(lister.format_conversation_list(conversations))
    
    print("\n" + "=" * 60)
    print("✅ Listagem via Cursor Agent concluída!")
    print("💾 Dados obtidos do banco Turso real via MCP")

if __name__ == "__main__":
    asyncio.run(main()) 