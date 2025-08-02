#!/usr/bin/env python3
"""
Script para salvar documento de arquitetura no Turso
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys

async def save_architecture_doc_to_turso():
    """Salva o documento de arquitetura no Turso"""
    
    print("📄 SALVANDO DOCUMENTO DE ARQUITETURA NO TURSO")
    print("=" * 60)
    
    # 1. Ler o documento
    doc_path = Path("docs/arquitetura_flexivel.md")
    
    if not doc_path.exists():
        print(f"❌ Erro: Arquivo {doc_path} não encontrado")
        return False
    
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Documento lido: {len(content)} caracteres")
        
    except Exception as e:
        print(f"❌ Erro ao ler documento: {e}")
        return False
    
    # 2. Preparar dados para Turso
    doc_data = {
        "title": "Arquitetura Flexível - Sistema de Agentes Inteligentes",
        "type": "architecture_documentation",
        "content": content,
        "metadata": {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "author": "Sistema de Agentes",
            "tags": ["arquitetura", "flexível", "agentes", "prp", "turso", "sentry"],
            "status": "active",
            "priority": "high"
        },
        "sections": {
            "core_components": ["PRP Agent", "Turso", "Sentry"],
            "optional_components": ["CrewAI", "A2A"],
            "scenarios": ["Sistema Mínimo", "Com Memória", "Com Monitoramento", "Sistema Completo"]
        }
    }
    
    print("📊 Dados preparados para Turso")
    
    # 3. Salvar no Turso via MCP
    try:
        # Usar o script de integração MCP existente
        from prp_agent.agents.agent_with_mcp_turso import PRPAgentWithMCPTurso
        
        agent = PRPAgentWithMCPTurso()
        
        # Verificar se MCP está disponível
        if not agent._check_mcp_availability():
            print("❌ MCP Turso não está disponível")
            print("💡 Dica: Execute 'npm start' no diretório mcp-turso-cloud-diegofornalha")
            return False
        
        # Salvar documento
        success = await agent.save_conversation_to_mcp(
            message="Documento de Arquitetura Flexível",
            response=json.dumps(doc_data, indent=2),
            context="Documentação técnica da arquitetura do sistema"
        )
        
        if success:
            print("✅ Documento salvo no Turso com sucesso!")
            
            # 4. Buscar e mostrar o documento salvo
            print("\n🔍 VERIFICANDO DOCUMENTO SALVO:")
            print("-" * 40)
            
            # Buscar documentos relacionados
            search_results = await agent.search_relevant_context(
                "arquitetura flexível sistema agentes",
                limit=3
            )
            
            if search_results:
                print(f"📋 Encontrados {len(search_results)} documentos relacionados:")
                for i, result in enumerate(search_results, 1):
                    print(f"   {i}. {result.get('title', 'Sem título')}")
                    print(f"      Tipo: {result.get('type', 'N/A')}")
                    print(f"      Data: {result.get('created_at', 'N/A')}")
                    print()
            else:
                print("📋 Nenhum documento relacionado encontrado")
            
            return True
        else:
            print("❌ Falha ao salvar documento no Turso")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao salvar no Turso: {e}")
        return False

async def demonstrate_turso_integration():
    """Demonstra integração com Turso"""
    
    print("\n🎯 DEMONSTRAÇÃO DE INTEGRAÇÃO TURSO")
    print("=" * 60)
    
    try:
        from prp_agent.agents.agent_with_mcp_turso import PRPAgentWithMCPTurso
        
        agent = PRPAgentWithMCPTurso()
        
        # Verificar disponibilidade
        print("🔍 Verificando disponibilidade do MCP Turso...")
        if agent._check_mcp_availability():
            print("✅ MCP Turso disponível")
        else:
            print("❌ MCP Turso não disponível")
            return
        
        # Testar busca
        print("\n🔍 Testando busca no Turso...")
        results = await agent.search_relevant_context(
            "arquitetura sistema",
            limit=2
        )
        
        if results:
            print(f"✅ Encontrados {len(results)} resultados")
            for result in results:
                print(f"   • {result.get('title', 'Sem título')}")
        else:
            print("📋 Nenhum resultado encontrado")
        
        # Testar salvamento
        print("\n💾 Testando salvamento no Turso...")
        test_data = {
            "title": "Teste de Integração Turso",
            "content": "Este é um teste de integração com o Turso",
            "timestamp": datetime.now().isoformat()
        }
        
        success = await agent.save_conversation_to_mcp(
            message="Teste de integração",
            response=json.dumps(test_data),
            context="Teste de funcionalidade"
        )
        
        if success:
            print("✅ Teste de salvamento bem-sucedido")
        else:
            print("❌ Falha no teste de salvamento")
            
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")

async def main():
    """Função principal"""
    
    print("🚀 SALVANDO DOCUMENTO DE ARQUITETURA NO TURSO")
    print("=" * 80)
    
    # 1. Salvar documento principal
    success = await save_architecture_doc_to_turso()
    
    if success:
        print("\n🎉 DOCUMENTO SALVO COM SUCESSO!")
        print("=" * 80)
        print("✅ Arquitetura Flexível documentada")
        print("✅ Documento salvo no Turso")
        print("✅ Integração MCP funcionando")
        print("✅ Sistema pronto para uso")
        
        # 2. Demonstração adicional
        await demonstrate_turso_integration()
        
    else:
        print("\n❌ FALHA AO SALVAR DOCUMENTO")
        print("=" * 80)
        print("💡 Verifique:")
        print("   • MCP Turso está rodando")
        print("   • Arquivo docs/arquitetura_flexivel.md existe")
        print("   • Configuração do Turso está correta")

if __name__ == "__main__":
    asyncio.run(main()) 