#!/usr/bin/env python3
"""
Script final que usa o agente real para listar PRPs do banco Turso
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório archive ao path
sys.path.insert(0, str(Path(__file__).parent / "archive"))

async def list_prps_final():
    """
    Lista PRPs usando o agente real que já está funcionando
    """
    
    print("🤖 LISTANDO PRPs VIA AGENTE REAL - MCP TURSO")
    print("=" * 60)
    print()
    
    try:
        # Importar o agente real
        from cursor_turso_integration import CursorTursoIntegration
        
        # Criar instância do agente
        agent = CursorTursoIntegration()
        
        print("📋 Buscando PRPs via agente real...")
        
        # Usar o método do agente para listar PRPs
        prps = await agent.get_prp_suggestions(limit=20)
        
        if prps:
            print(f"📋 PRPs ENCONTRADOS: {len(prps)}")
            print("=" * 60)
            print()
            
            for i, prp in enumerate(prps, 1):
                print(f"{i}. 📄 **{prp.get('name', 'N/A')}**")
                print(f"   • Título: {prp.get('title', 'N/A')}")
                print(f"   • Descrição: {prp.get('description', 'N/A')}")
                print(f"   • Status: {prp.get('status', 'N/A')}")
                print(f"   • Prioridade: {prp.get('priority', 'N/A')}")
                print(f"   • Criado: {prp.get('created_at', 'N/A')}")
                print(f"   • Tags: {prp.get('tags', 'N/A')}")
                print()
        else:
            print("📭 Nenhum PRP encontrado via agente real")
            print("💡 O banco de dados Turso está vazio")
            print("💡 Use o agente para criar PRPs primeiro")
        
        print("\n" + "=" * 60)
        print("💬 Buscando conversas via agente real...")
        
        # Usar o método do agente para listar conversas
        conversations = await agent.get_conversation_history(limit=10)
        
        if conversations:
            print(f"💬 CONVERSAS ENCONTRADAS: {len(conversations)}")
            print("=" * 60)
            print()
            
            for i, conv in enumerate(conversations, 1):
                print(f"{i}. 💬 **{conv.get('session_id', 'N/A')}**")
                print(f"   • Usuário: {conv.get('user_message', 'N/A')[:50]}...")
                print(f"   • Agente: {conv.get('agent_response', 'N/A')[:50]}...")
                print(f"   • Arquivo: {conv.get('file_context', 'N/A')}")
                print(f"   • Timestamp: {conv.get('timestamp', 'N/A')}")
                print()
        else:
            print("📭 Nenhuma conversa encontrada via agente real")
            print("💡 O banco de dados Turso está vazio")
            print("💡 Use o agente para criar conversas primeiro")
        
        print("\n" + "=" * 60)
        print("✅ Listagem via agente real concluída!")
        print("🤖 Agente real funcionando com MCP Turso")
        print("💾 Banco de dados: context-memory")
        print("🔧 Status: Conectado e funcionando")
        
    except Exception as e:
        print(f"❌ Erro ao usar agente real: {e}")
        print("🔧 Verificando se o agente está disponível...")
        
        # Verificar se o arquivo existe
        agent_file = Path("archive/cursor_turso_integration.py")
        if agent_file.exists():
            print("✅ Arquivo do agente encontrado")
            print("📄 Conteúdo do arquivo:")
            with open(agent_file, 'r') as f:
                print(f.read()[:500] + "...")
        else:
            print("❌ Arquivo do agente não encontrado")

async def main():
    """
    Função principal
    """
    await list_prps_final()

if __name__ == "__main__":
    asyncio.run(main()) 