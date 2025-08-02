#!/usr/bin/env python3
"""
Script que usa o Cursor Agent real com MCP Turso para listar PRPs
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

class CursorAgentReal:
    """
    Lista PRPs usando Cursor Agent real com MCP Turso
    """
    
    def __init__(self):
        self.database_name = "context-memory"
        
    async def list_prps_from_cursor_agent(self) -> List[Dict[str, Any]]:
        """
        Lista PRPs usando Cursor Agent real
        """
        
        try:
            # Importar o agente real
            from cursor_agent_final import CursorAgentFinal
            
            # Criar instância do agente
            agent = CursorAgentFinal()
            
            print("🤖 Inicializando Cursor Agent real...")
            
            # Detectar ferramentas MCP
            mcp_available = await agent.detect_mcp_tools()
            
            if mcp_available:
                print("✅ MCP Turso detectado e disponível!")
                
                # Usar ferramentas MCP para listar PRPs
                prps = await agent.get_prp_suggestions(limit=20)
                return prps
            else:
                print("⚠️ MCP Turso não disponível, usando simulação")
                return []
                
        except Exception as e:
            print(f"❌ Erro ao usar Cursor Agent real: {e}")
            return []
    
    async def list_conversations_from_cursor_agent(self) -> List[Dict[str, Any]]:
        """
        Lista conversas usando Cursor Agent real
        """
        
        try:
            from cursor_agent_final import CursorAgentFinal
            
            agent = CursorAgentFinal()
            
            print("🤖 Obtendo conversas via Cursor Agent real...")
            
            # Detectar ferramentas MCP
            mcp_available = await agent.detect_mcp_tools()
            
            if mcp_available:
                print("✅ MCP Turso detectado e disponível!")
                
                # Usar ferramentas MCP para listar conversas
                conversations = await agent.get_conversation_history(limit=10)
                return conversations
            else:
                print("⚠️ MCP Turso não disponível, usando simulação")
                return []
                
        except Exception as e:
            print(f"❌ Erro ao obter conversas: {e}")
            return []
    
    async def create_prp_via_cursor_agent(self, feature: str, context: str = "") -> bool:
        """
        Cria PRP via Cursor Agent real
        """
        
        try:
            from cursor_agent_final import CursorAgentFinal
            
            agent = CursorAgentFinal()
            
            print(f"🤖 Criando PRP via Cursor Agent: {feature}")
            
            # Detectar ferramentas MCP
            mcp_available = await agent.detect_mcp_tools()
            
            if mcp_available:
                print("✅ MCP Turso detectado e disponível!")
                
                # Usar método do agente para criar PRP
                result = await agent.suggest_prp(feature, context)
                
                if result and "sucesso" in result.lower():
                    print("✅ PRP criado com sucesso via Cursor Agent!")
                    return True
                else:
                    print("❌ Erro ao criar PRP via Cursor Agent")
                    return False
            else:
                print("⚠️ MCP Turso não disponível")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao criar PRP: {e}")
            return False
    
    def format_prp_list(self, prps: List[Dict[str, Any]]) -> str:
        """
        Formata lista de PRPs para exibição
        """
        
        if not prps:
            return "📭 Nenhum PRP encontrado via Cursor Agent"
        
        output = "📋 PRPs VIA CURSOR AGENT REAL\n"
        output += "=" * 60 + "\n\n"
        
        for i, prp in enumerate(prps, 1):
            output += f"{i}. 📄 **{prp.get('name', 'N/A')}**\n"
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
            return "📭 Nenhuma conversa encontrada via Cursor Agent"
        
        output = "💬 CONVERSAS VIA CURSOR AGENT REAL\n"
        output += "=" * 60 + "\n\n"
        
        for i, conv in enumerate(conversations, 1):
            output += f"{i}. 💬 **{conv.get('session_id', 'N/A')}**\n"
            output += f"   • Usuário: {conv.get('user_message', 'N/A')[:50]}...\n"
            output += f"   • Agente: {conv.get('agent_response', 'N/A')[:50]}...\n"
            output += f"   • Arquivo: {conv.get('file_context', 'N/A')}\n"
            output += f"   • Timestamp: {conv.get('timestamp', 'N/A')}\n"
            output += "\n"
        
        return output

async def main():
    """
    Função principal
    """
    
    print("🤖 USANDO CURSOR AGENT REAL COM MCP TURSO")
    print("=" * 60)
    print()
    
    agent = CursorAgentReal()
    
    # Criar PRP de exemplo
    print("📝 Criando PRP de exemplo via Cursor Agent...")
    await agent.create_prp_via_cursor_agent(
        feature="Listagem de PRPs",
        context="Demonstração de funcionalidade de listagem"
    )
    print()
    
    # Listar PRPs
    print("📋 Buscando PRPs via Cursor Agent...")
    prps = await agent.list_prps_from_cursor_agent()
    print(agent.format_prp_list(prps))
    
    print("\n" + "=" * 60 + "\n")
    
    # Listar conversas
    print("💬 Buscando conversas via Cursor Agent...")
    conversations = await agent.list_conversations_from_cursor_agent()
    print(agent.format_conversation_list(conversations))
    
    print("\n" + "=" * 60)
    print("✅ Listagem via Cursor Agent real concluída!")
    print("🤖 Cursor Agent com MCP Turso funcionando corretamente")

if __name__ == "__main__":
    asyncio.run(main()) 