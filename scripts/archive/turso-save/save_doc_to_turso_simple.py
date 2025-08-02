#!/usr/bin/env python3
"""
Script simplificado para salvar documento de arquitetura no Turso
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Adicionar caminhos para imports
sys.path.insert(0, str(Path(__file__).parent / "prp-agent"))

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
        # Importar com tratamento de erro
        try:
            from prp_agent.agents.agent_with_mcp_turso import PRPAgentWithMCPTurso
            agent = PRPAgentWithMCPTurso()
        except ImportError as e:
            print(f"❌ Erro de import: {e}")
            print("💡 Verifique se o módulo prp_agent está disponível")
            return False
        
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

async def test_mcp_connection():
    """Testa conexão com MCP"""
    
    print("\n🔍 TESTANDO CONEXÃO MCP")
    print("=" * 40)
    
    try:
        # Verificar se o servidor MCP está rodando
        mcp_dir = Path("mcp-turso-cloud-diegofornalha")
        if not mcp_dir.exists():
            print("❌ Diretório MCP não encontrado")
            return False
        
        # Verificar se package.json existe
        package_json = mcp_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json não encontrado")
            return False
        
        print("✅ Diretório MCP encontrado")
        
        # Verificar se node_modules existe
        node_modules = mcp_dir / "node_modules"
        if not node_modules.exists():
            print("⚠️ node_modules não encontrado")
            print("💡 Execute 'npm install' no diretório mcp-turso-cloud-diegofornalha")
            return False
        
        print("✅ Dependências instaladas")
        
        # Verificar se o servidor está rodando
        import subprocess
        try:
            result = subprocess.run(
                ["lsof", "-i", ":3000"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print("✅ Servidor MCP rodando na porta 3000")
                return True
            else:
                print("❌ Servidor MCP não está rodando")
                print("💡 Execute 'npm start' no diretório mcp-turso-cloud-diegofornalha")
                return False
        except Exception as e:
            print(f"❌ Erro ao verificar servidor: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de conexão: {e}")
        return False

async def main():
    """Função principal"""
    
    print("🚀 SALVANDO DOCUMENTO DE ARQUITETURA NO TURSO")
    print("=" * 80)
    
    # 1. Testar conexão MCP
    mcp_available = await test_mcp_connection()
    
    if not mcp_available:
        print("\n❌ MCP NÃO DISPONÍVEL")
        print("=" * 80)
        print("💡 Para ativar o MCP Turso:")
        print("   1. cd mcp-turso-cloud-diegofornalha")
        print("   2. npm install")
        print("   3. npm start")
        print("   4. Execute este script novamente")
        return
    
    # 2. Salvar documento
    success = await save_architecture_doc_to_turso()
    
    if success:
        print("\n🎉 DOCUMENTO SALVO COM SUCESSO!")
        print("=" * 80)
        print("✅ Arquitetura Flexível documentada")
        print("✅ Documento salvo no Turso")
        print("✅ Integração MCP funcionando")
        print("✅ Sistema pronto para uso")
        
        # 3. Mostrar resumo
        print("\n📊 RESUMO:")
        print("-" * 40)
        print("📄 Documento: docs/arquitetura_flexivel.md")
        print("🗄️ Armazenamento: Turso via MCP")
        print("📋 Tipo: Documentação de Arquitetura")
        print("🏷️ Tags: arquitetura, flexível, agentes, prp, turso, sentry")
        print("📅 Data: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    else:
        print("\n❌ FALHA AO SALVAR DOCUMENTO")
        print("=" * 80)
        print("💡 Verifique:")
        print("   • MCP Turso está rodando")
        print("   • Arquivo docs/arquitetura_flexivel.md existe")
        print("   • Configuração do Turso está correta")

if __name__ == "__main__":
    asyncio.run(main()) 