#!/usr/bin/env python3
"""
Script que cria PRPs reais no banco Turso e depois os lista
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório archive ao path
sys.path.insert(0, str(Path(__file__).parent / "archive"))

async def create_real_prps():
    """
    Cria PRPs reais no banco Turso
    """
    
    print("📝 CRIANDO PRPs REAIS NO BANCO TURSO")
    print("=" * 60)
    print()
    
    try:
        from cursor_turso_integration import CursorTursoIntegration
        
        agent = CursorTursoIntegration()
        
        # Lista de PRPs para criar
        prps_to_create = [
            {
                "feature": "Sistema de Autenticação",
                "context": "Implementar sistema de login seguro com JWT",
                "content": "PRP para sistema de autenticação com múltiplos provedores"
            },
            {
                "feature": "Dashboard de Analytics",
                "context": "Criar dashboard com métricas em tempo real",
                "content": "PRP para dashboard com gráficos interativos"
            },
            {
                "feature": "API REST",
                "context": "Desenvolver API RESTful com documentação OpenAPI",
                "content": "PRP para API com endpoints CRUD completos"
            },
            {
                "feature": "Sistema de Notificações",
                "context": "Implementar sistema de notificações push e email",
                "content": "PRP para sistema de notificações em tempo real"
            }
        ]
        
        created_count = 0
        
        for i, prp_data in enumerate(prps_to_create, 1):
            print(f"📄 Criando PRP {i}: {prp_data['feature']}")
            
            prp_id = await agent.store_prp_suggestion(
                feature=prp_data["feature"],
                context=prp_data["context"],
                prp_content=prp_data["content"]
            )
            
            if prp_id > 0:
                print(f"✅ PRP criado com ID: {prp_id}")
                created_count += 1
            else:
                print(f"❌ Erro ao criar PRP {i}")
            
            print()
        
        print(f"📊 Total de PRPs criados: {created_count}/{len(prps_to_create)}")
        
        # Criar algumas conversas de exemplo
        print("\n💬 Criando conversas de exemplo...")
        
        conversations = [
            {
                "message": "Crie um PRP para sistema de autenticação",
                "response": "PRP criado com sucesso! Sistema de autenticação com JWT implementado.",
                "context": "auth_system.py"
            },
            {
                "message": "Liste todos os PRPs disponíveis",
                "response": "Aqui estão os PRPs disponíveis: Sistema de Autenticação, Dashboard Analytics, API REST, Sistema de Notificações",
                "context": "prp_list.py"
            },
            {
                "message": "Analise o PRP do dashboard",
                "response": "Análise do PRP Dashboard Analytics: Complexidade média, estimativa de 2-3 semanas, requer integração com banco de dados.",
                "context": "dashboard_analysis.py"
            }
        ]
        
        conversation_count = 0
        
        for conv in conversations:
            success = await agent.store_conversation(
                user_message=conv["message"],
                agent_response=conv["response"],
                file_context=conv["context"]
            )
            
            if success:
                conversation_count += 1
                print(f"✅ Conversa criada: {conv['message'][:30]}...")
            else:
                print(f"❌ Erro ao criar conversa")
        
        print(f"📊 Total de conversas criadas: {conversation_count}/{len(conversations)}")
        
        print("\n" + "=" * 60)
        print("✅ Dados reais criados no banco Turso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados reais: {e}")

async def list_real_prps():
    """
    Lista PRPs reais do banco Turso
    """
    
    print("📋 LISTANDO PRPs REAIS DO BANCO TURSO")
    print("=" * 60)
    print()
    
    try:
        from cursor_turso_integration import CursorTursoIntegration
        
        agent = CursorTursoIntegration()
        
        print("📋 Buscando PRPs reais...")
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
            print("📭 Nenhum PRP encontrado no banco real")
        
        print("\n" + "=" * 60)
        print("💬 Buscando conversas reais...")
        
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
            print("📭 Nenhuma conversa encontrada no banco real")
        
        print("\n" + "=" * 60)
        print("✅ Listagem de dados reais concluída!")
        print("💾 Dados reais do banco Turso via MCP")
        
    except Exception as e:
        print(f"❌ Erro ao listar dados reais: {e}")

async def main():
    """
    Função principal
    """
    
    # Primeiro criar dados reais
    await create_real_prps()
    print()
    
    # Depois listar os dados reais
    await list_real_prps()

if __name__ == "__main__":
    asyncio.run(main()) 