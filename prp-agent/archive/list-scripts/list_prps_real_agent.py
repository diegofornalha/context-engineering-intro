#!/usr/bin/env python3
"""
Script que usa o agente real para listar PRPs do banco Turso
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório archive ao path
sys.path.insert(0, str(Path(__file__).parent / "archive"))

async def list_prps_with_real_agent():
    """
    Lista PRPs usando o agente real que já está funcionando
    """
    
    print("🤖 USANDO AGENTE REAL PARA LISTAR PRPs")
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
            print("📋 PRPs ENCONTRADOS VIA AGENTE REAL:")
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
        
        print("\n" + "=" * 60)
        print("💬 Buscando conversas via agente real...")
        
        # Usar o método do agente para listar conversas
        conversations = await agent.get_conversation_history(limit=10)
        
        if conversations:
            print("💬 CONVERSAS ENCONTRADAS VIA AGENTE REAL:")
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
        
        print("\n" + "=" * 60)
        print("✅ Listagem via agente real concluída!")
        print("🤖 Agente real funcionando com MCP Turso")
        
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

async def create_sample_data():
    """
    Cria dados de exemplo usando o agente real
    """
    
    print("📝 CRIANDO DADOS DE EXEMPLO VIA AGENTE REAL")
    print("=" * 60)
    print()
    
    try:
        from cursor_turso_integration import CursorTursoIntegration
        
        agent = CursorTursoIntegration()
        
        # Criar PRP de exemplo
        print("📄 Criando PRP de exemplo...")
        prp_id = await agent.store_prp_suggestion(
            feature="Funcionalidade de Exemplo Real",
            context="Contexto de teste para demonstrar funcionalidade real",
            prp_content="PRP de exemplo criado via agente real"
        )
        
        if prp_id > 0:
            print(f"✅ PRP de exemplo criado com ID: {prp_id}")
        else:
            print("❌ Erro ao criar PRP de exemplo")
        
        # Armazenar conversa de exemplo
        print("💬 Armazenando conversa de exemplo...")
        success = await agent.store_conversation(
            user_message="Liste os PRPs disponíveis",
            agent_response="Aqui estão os PRPs disponíveis via agente real...",
            file_context="list_prps_real_agent.py"
        )
        
        if success:
            print("✅ Conversa de exemplo armazenada com sucesso!")
        else:
            print("❌ Erro ao armazenar conversa de exemplo")
        
        print("\n" + "=" * 60)
        print("✅ Dados de exemplo criados via agente real!")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")

async def main():
    """
    Função principal
    """
    
    # Primeiro criar dados de exemplo
    await create_sample_data()
    print()
    
    # Depois listar os dados
    await list_prps_with_real_agent()

if __name__ == "__main__":
    asyncio.run(main()) 