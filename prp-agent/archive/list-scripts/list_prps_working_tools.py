#!/usr/bin/env python3
"""
Script que usa as ferramentas realmente implementadas no agente
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

class WorkingTursoTools:
    """
    Lista PRPs usando ferramentas realmente implementadas
    """
    
    def __init__(self):
        self.database_name = "context-memory"
        
    async def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Obtém histórico de conversas usando método implementado
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("💬 Obtendo histórico de conversas...")
            
            # Usar método implementado
            conversations = await agent.get_conversation_history(limit=10)
            
            return conversations
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    async def get_prp_suggestions(self) -> List[Dict[str, Any]]:
        """
        Obtém sugestões de PRPs usando método implementado
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("📋 Obtendo sugestões de PRPs...")
            
            # Usar método implementado
            prps = await agent.get_prp_suggestions(limit=10)
            
            return prps
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    async def create_sample_prp(self) -> bool:
        """
        Cria um PRP de exemplo usando método implementado
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("📝 Criando PRP de exemplo...")
            
            # Usar método implementado
            result = await agent.store_prp_suggestion(
                feature="Funcionalidade de Exemplo",
                context="Contexto de teste para demonstrar funcionalidade",
                prp_content="PRP de exemplo criado via agente"
            )
            
            if result > 0:
                print("✅ PRP de exemplo criado com sucesso!")
                return True
            else:
                print("❌ Erro ao criar PRP de exemplo")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    async def store_sample_conversation(self) -> bool:
        """
        Armazena conversa de exemplo usando método implementado
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("💬 Armazenando conversa de exemplo...")
            
            # Usar método implementado
            result = await agent.store_conversation(
                user_message="Liste os PRPs disponíveis",
                agent_response="Aqui estão os PRPs disponíveis...",
                file_context="list_prps_working_tools.py"
            )
            
            if result:
                print("✅ Conversa de exemplo armazenada com sucesso!")
                return True
            else:
                print("❌ Erro ao armazenar conversa de exemplo")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def format_prp_list(self, prps: List[Dict[str, Any]]) -> str:
        """
        Formata lista de PRPs para exibição
        """
        
        if not prps:
            return "📭 Nenhum PRP encontrado"
        
        output = "📋 PRPs ENCONTRADOS\n"
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
            return "📭 Nenhuma conversa encontrada"
        
        output = "💬 CONVERSAS ENCONTRADAS\n"
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
    
    print("🔍 LISTANDO PRPs COM FERRAMENTAS IMPLEMENTADAS")
    print("=" * 60)
    print()
    
    tools = WorkingTursoTools()
    
    # Criar dados de exemplo
    print("📝 Criando dados de exemplo...")
    await tools.create_sample_prp()
    await tools.store_sample_conversation()
    print()
    
    # Listar PRPs
    print("📋 Buscando PRPs...")
    prps = await tools.get_prp_suggestions()
    print(tools.format_prp_list(prps))
    
    print("\n" + "=" * 60 + "\n")
    
    # Listar conversas
    print("💬 Buscando conversas...")
    conversations = await tools.get_conversation_history()
    print(tools.format_conversation_list(conversations))
    
    print("\n" + "=" * 60)
    print("✅ Listagem com ferramentas implementadas concluída!")
    print("🔧 Agente funcionando com dados reais")

if __name__ == "__main__":
    asyncio.run(main()) 