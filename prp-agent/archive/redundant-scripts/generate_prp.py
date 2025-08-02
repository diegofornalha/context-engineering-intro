#!/usr/bin/env python3
"""
Script que usa o agente real para gerar um PRP
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório archive ao path
sys.path.insert(0, str(Path(__file__).parent / "archive"))

async def generate_prp_with_agent():
    """
    Gera um PRP usando o agente real
    """
    
    print("🤖 GERANDO PRP VIA AGENTE REAL")
    print("=" * 60)
    print()
    
    try:
        # Importar o agente real
        from cursor_turso_integration import CursorTursoIntegration
        
        # Criar instância do agente
        agent = CursorTursoIntegration()
        
        # Definir o PRP a ser gerado
        feature = "Sistema de Gerenciamento de Tarefas"
        context = """
        Preciso de um sistema completo para gerenciar tarefas de projeto.
        O sistema deve incluir:
        - Criação e edição de tarefas
        - Atribuição de responsáveis
        - Controle de status e progresso
        - Dashboard com métricas
        - Notificações automáticas
        - Integração com calendário
        """
        
        print(f"📄 Gerando PRP para: {feature}")
        print(f"📋 Contexto: {context.strip()}")
        print()
        
        # Usar o método do agente para sugerir PRP
        response = await agent.suggest_prp(feature, context)
        
        print("✅ PRP GERADO COM SUCESSO!")
        print("=" * 60)
        print(response)
        
        print("\n" + "=" * 60)
        print("💾 Salvando PRP no banco Turso...")
        
        # Salvar o PRP no banco
        prp_id = await agent.store_prp_suggestion(
            feature=feature,
            context=context,
            prp_content=response
        )
        
        if prp_id > 0:
            print(f"✅ PRP salvo com ID: {prp_id}")
        else:
            print("❌ Erro ao salvar PRP no banco")
        
        print("\n" + "=" * 60)
        print("✅ PRP gerado e salvo com sucesso!")
        print("🤖 Agente real funcionando com MCP Turso")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PRP: {e}")

async def generate_multiple_prps():
    """
    Gera múltiplos PRPs usando o agente real
    """
    
    print("🤖 GERANDO MÚLTIPLOS PRPs VIA AGENTE REAL")
    print("=" * 60)
    print()
    
    try:
        # Importar o agente real
        from cursor_turso_integration import CursorTursoIntegration
        
        # Criar instância do agente
        agent = CursorTursoIntegration()
        
        # Lista de PRPs para gerar
        prps_to_generate = [
            {
                "feature": "Sistema de Autenticação Multi-Fator",
                "context": "Implementar sistema de login seguro com autenticação de dois fatores, suporte a OAuth2 e JWT tokens"
            },
            {
                "feature": "Dashboard de Analytics em Tempo Real",
                "context": "Criar dashboard interativo com métricas em tempo real, gráficos dinâmicos e exportação de relatórios"
            },
            {
                "feature": "API REST com Documentação Automática",
                "context": "Desenvolver API RESTful com documentação OpenAPI automática, testes automatizados e rate limiting"
            },
            {
                "feature": "Sistema de Notificações Push",
                "context": "Implementar sistema de notificações push e email com templates personalizáveis e agendamento"
            }
        ]
        
        generated_count = 0
        
        for i, prp_data in enumerate(prps_to_generate, 1):
            print(f"📄 Gerando PRP {i}: {prp_data['feature']}")
            
            # Gerar PRP
            response = await agent.suggest_prp(prp_data["feature"], prp_data["context"])
            
            print(f"✅ PRP {i} gerado com sucesso!")
            print(f"📋 Resumo: {response[:100]}...")
            
            # Salvar no banco
            prp_id = await agent.store_prp_suggestion(
                feature=prp_data["feature"],
                context=prp_data["context"],
                prp_content=response
            )
            
            if prp_id > 0:
                print(f"💾 PRP {i} salvo com ID: {prp_id}")
                generated_count += 1
            else:
                print(f"❌ Erro ao salvar PRP {i}")
            
            print()
        
        print(f"📊 Total de PRPs gerados: {generated_count}/{len(prps_to_generate)}")
        
        print("\n" + "=" * 60)
        print("✅ Múltiplos PRPs gerados com sucesso!")
        print("🤖 Agente real funcionando com MCP Turso")
        
    except Exception as e:
        print(f"❌ Erro ao gerar múltiplos PRPs: {e}")

async def main():
    """
    Função principal
    """
    
    # Gerar um PRP
    await generate_prp_with_agent()
    print()
    
    # Gerar múltiplos PRPs
    await generate_multiple_prps()

if __name__ == "__main__":
    asyncio.run(main()) 