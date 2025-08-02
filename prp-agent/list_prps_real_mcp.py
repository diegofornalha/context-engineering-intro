#!/usr/bin/env python3
"""
Script para listar PRPs usando MCP Turso real
"""

import asyncio
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTursoPRPList:
    """
    Lista PRPs usando MCP Turso real
    """
    
    def __init__(self):
        self.database_name = "context-memory"
        
    async def call_real_mcp_turso(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chama MCP Turso real via subprocess
        """
        
        try:
            # Comando para chamar MCP Turso
            cmd = [
                "npx", "@modelcontextprotocol/server-cli", "run",
                "mcp-turso-cloud-diegofornalha",
                "--database", self.database_name,
                "--tool", tool_name,
                "--params", json.dumps(params)
            ]
            
            print(f"🔌 Chamando MCP Turso real: {tool_name}")
            
            # Executar comando
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"❌ Erro MCP: {result.stderr}")
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            print(f"❌ Erro ao chamar MCP: {e}")
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
            
            result = await self.call_real_mcp_turso("mcp_turso_execute_read_only_query", {
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
            
            result = await self.call_real_mcp_turso("mcp_turso_execute_read_only_query", {
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
    Função principal para listar PRPs do Turso real
    """
    
    print("🔍 LISTANDO PRPs DO BANCO DE DADOS TURSO REAL")
    print("=" * 60)
    print()
    
    lister = RealTursoPRPList()
    
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
    print("✅ Listagem concluída!")
    print("💾 Dados obtidos do banco Turso real via MCP")

if __name__ == "__main__":
    asyncio.run(main()) 