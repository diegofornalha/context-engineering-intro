#!/usr/bin/env python3
"""
Script que usa a API do servidor PRP Agent para listar PRPs
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional

class PRPAgentAPI:
    """
    Cliente para API do PRP Agent
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    async def list_prps(self) -> List[Dict[str, Any]]:
        """
        Lista PRPs via API
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                # Tentar endpoint específico para PRPs
                async with session.get(f"{self.base_url}/prps") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"❌ Erro ao listar PRPs: {response.status}")
                        return []
                        
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return []
    
    async def list_conversations(self) -> List[Dict[str, Any]]:
        """
        Lista conversas via API
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                # Tentar endpoint específico para conversas
                async with session.get(f"{self.base_url}/conversations") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"❌ Erro ao listar conversas: {response.status}")
                        return []
                        
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return []
    
    async def get_server_info(self) -> Dict[str, Any]:
        """
        Obtém informações do servidor
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"Status {response.status}"}
                        
        except Exception as e:
            return {"error": str(e)}
    
    async def test_sentry_debug(self) -> Dict[str, Any]:
        """
        Testa endpoint de debug do Sentry
        """
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/sentry-debug") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"Status {response.status}"}
                        
        except Exception as e:
            return {"error": str(e)}
    
    def format_prp_list(self, prps: List[Dict[str, Any]]) -> str:
        """
        Formata lista de PRPs para exibição
        """
        
        if not prps:
            return "📭 Nenhum PRP encontrado via API"
        
        output = "📋 PRPs VIA API DO SERVIDOR\n"
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
            return "📭 Nenhuma conversa encontrada via API"
        
        output = "💬 CONVERSAS VIA API DO SERVIDOR\n"
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
    
    print("🌐 CONECTANDO AO SERVIDOR PRP AGENT")
    print("=" * 60)
    print()
    
    api = PRPAgentAPI()
    
    # Testar conexão com servidor
    print("🔍 Testando conexão com servidor...")
    server_info = await api.get_server_info()
    
    if "error" in server_info:
        print(f"❌ Erro ao conectar: {server_info['error']}")
        print("💡 Verifique se o servidor está rodando em http://localhost:8000")
        return
    else:
        print("✅ Servidor conectado!")
        print(f"📊 Info: {server_info}")
        print()
    
    # Testar Sentry
    print("🐛 Testando Sentry...")
    sentry_info = await api.test_sentry_debug()
    if "error" not in sentry_info:
        print("✅ Sentry funcionando!")
    else:
        print(f"⚠️ Sentry: {sentry_info['error']}")
    print()
    
    # Listar PRPs
    print("📋 Buscando PRPs via API...")
    prps = await api.list_prps()
    print(api.format_prp_list(prps))
    
    print("\n" + "=" * 60 + "\n")
    
    # Listar conversas
    print("💬 Buscando conversas via API...")
    conversations = await api.list_conversations()
    print(api.format_conversation_list(conversations))
    
    print("\n" + "=" * 60)
    print("✅ Listagem via API concluída!")
    print("🌐 Servidor PRP Agent funcionando corretamente")

if __name__ == "__main__":
    asyncio.run(main()) 