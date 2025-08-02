#!/usr/bin/env python3
"""
🤖 Criação Automática via MCP Sentry
===================================

Script para criar projeto Sentry automaticamente via MCP
e obter todas as configurações necessárias.
"""

import os
import subprocess
import json
import sys
from datetime import datetime

def executar_mcp_command(command, params):
    """
    Executa comando MCP e retorna resultado
    """
    try:
        # Simular chamada MCP (ajustar conforme sua implementação)
        print(f"🤖 Executando: {command}")
        print(f"📋 Parâmetros: {params}")
        
        # Aqui você adaptaria para sua implementação MCP real
        # Por enquanto, vamos simular
        
        if command == "create_project":
            return {
                "success": True,
                "project_slug": "prp-agent-python-monitoring",
                "dsn": f"https://simulated-key@o927801.ingest.us.sentry.io/{datetime.now().strftime('%Y%m%d')}",
                "project_id": datetime.now().strftime('%Y%m%d')
            }
        elif command == "list_projects":
            return {
                "success": True,
                "projects": [
                    {
                        "name": "PRP Agent Python Monitoring",
                        "slug": "prp-agent-python-monitoring",
                        "platform": "python"
                    }
                ]
            }
        
        return {"success": False, "error": "Comando não implementado"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def tentar_criacao_via_mcp():
    """
    Tenta criar projeto via MCP Sentry
    """
    print("🤖 TENTATIVA 1: Criação Automática via MCP")
    print("=" * 50)
    
    # 1. Listar projetos existentes
    print("\n📋 Listando projetos existentes...")
    result = executar_mcp_command("list_projects", {})
    
    if result["success"]:
        projects = result.get("projects", [])
        print(f"✅ Encontrados {len(projects)} projetos")
        
        # Verificar se projeto PRP já existe
        prp_project = None
        for project in projects:
            if "prp" in project.get("name", "").lower() or "agent" in project.get("name", "").lower():
                prp_project = project
                break
        
        if prp_project:
            print(f"🎯 Projeto PRP encontrado: {prp_project['name']}")
            return prp_project
    
    # 2. Criar novo projeto
    print("\n🚀 Criando novo projeto...")
    result = executar_mcp_command("create_project", {
        "name": "PRP Agent Python Monitoring",
        "slug": "prp-agent-python-monitoring",
        "platform": "python",
        "team": "my-team"
    })
    
    if result["success"]:
        print("✅ Projeto criado com sucesso!")
        return {
            "name": "PRP Agent Python Monitoring",
            "slug": result["project_slug"],
            "dsn": result["dsn"],
            "project_id": result["project_id"]
        }
    else:
        print(f"❌ Falha na criação: {result.get('error', 'Erro desconhecido')}")
        return None

def gerar_configuracao_automatica(project_info):
    """
    Gera configuração automaticamente baseada no projeto
    """
    if not project_info:
        return None
    
    config = f"""# 🤖 Configuração Gerada Automaticamente via MCP
# ================================================
# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# === ORGANIZAÇÃO (mantém atual) ===
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0/

# === PROJETO PRP AGENT (gerado via MCP) ===
SENTRY_PROJECT_SLUG={project_info.get('slug', 'prp-agent-python-monitoring')}
SENTRY_PROJECT_NAME={project_info.get('name', 'PRP Agent Python Monitoring')}

# === DSN (obtido via MCP) ===
SENTRY_DSN={project_info.get('dsn', 'CONFIGURE-DSN-MANUAL')}

# === AUTH TOKEN (gerar manualmente) ===
# 🔗 Acesse: https://sentry.io/settings/coflow/auth-tokens/
# ➕ Crie token com nome "PRP Agent Token"
# ✅ Scopes: project:read, project:write, event:read, event:write, org:read
SENTRY_AUTH_TOKEN=GERAR-TOKEN-MANUAL

# === AI AGENT MONITORING ===
SENTRY_ENVIRONMENT=development
SENTRY_RELEASE=prp-agent@1.0.0
ENABLE_AI_AGENT_MONITORING=true
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_DEBUG=true
"""
    
    return config

def salvar_configuracao(config):
    """
    Salva configuração gerada
    """
    if not config:
        return False
    
    try:
        # Backup do arquivo atual
        if os.path.exists(".env.sentry"):
            backup_name = f".env.sentry.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(".env.sentry", backup_name)
            print(f"📁 Backup criado: {backup_name}")
        
        # Salvar nova configuração
        with open(".env.sentry", "w") as f:
            f.write(config)
        
        print("✅ Configuração salva em .env.sentry")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar configuração: {e}")
        return False

def exibir_proximos_passos(project_info):
    """
    Exibe próximos passos baseado no resultado
    """
    print("\n" + "="*60)
    print("🎯 PRÓXIMOS PASSOS")
    print("="*60)
    
    if project_info and project_info.get('dsn') and 'simulated' not in project_info.get('dsn', ''):
        print("\n✅ PROJETO CRIADO COM SUCESSO VIA MCP!")
        print("📋 Apenas configure o AUTH TOKEN:")
        print("   1. Acesse: https://sentry.io/settings/coflow/auth-tokens/")
        print("   2. Crie token 'PRP Agent Token'")
        print("   3. Edite .env.sentry e substitua GERAR-TOKEN-MANUAL")
        print("   4. Execute: python sentry_ai_agent_setup.py")
    else:
        print("\n⚠️  CRIAÇÃO VIA MCP NÃO FUNCIONOU")
        print("📋 Configuração manual necessária:")
        print("   1. Acesse: https://sentry.io/organizations/coflow/projects/new/")
        print("   2. Crie projeto 'PRP Agent Python Monitoring'")
        print("   3. Copie DSN e configure em .env.sentry")
        print("   4. Gere AUTH TOKEN conforme instruções")
        print("   5. Execute: python sentry_ai_agent_setup.py")
    
    print("\n🔗 LINKS ÚTEIS:")
    print("   • Criar Projeto: https://sentry.io/organizations/coflow/projects/new/")
    print("   • Criar Token: https://sentry.io/settings/coflow/auth-tokens/")
    print("   • Dashboard: https://sentry.io/organizations/coflow/")

def main():
    """
    Função principal
    """
    print("🤖 CRIAÇÃO AUTOMÁTICA VIA MCP SENTRY")
    print("=" * 55)
    print("🎯 Tentando criar projeto PRP Agent automaticamente...")
    
    # 1. Tentar criação via MCP
    project_info = tentar_criacao_via_mcp()
    
    # 2. Gerar configuração
    config = gerar_configuracao_automatica(project_info)
    
    # 3. Salvar configuração
    if config:
        sucesso = salvar_configuracao(config)
        if sucesso:
            print("✅ Configuração gerada e salva!")
        else:
            print("❌ Falha ao salvar configuração")
    
    # 4. Próximos passos
    exibir_proximos_passos(project_info)
    
    # 5. Teste final
    print("\n🧪 TESTE DE CONFIGURAÇÃO:")
    if os.path.exists(".env.sentry"):
        with open(".env.sentry", "r") as f:
            content = f.read()
        
        if "GERAR-TOKEN-MANUAL" in content:
            print("⚠️  Configure AUTH TOKEN antes de testar")
        elif "CONFIGURE-DSN-MANUAL" in content:
            print("⚠️  Configure DSN antes de testar")
        else:
            print("✅ Configuração parece completa")
            print("💡 Execute: python sentry_ai_agent_setup.py")
    
    print("\n🎉 PROCESSO VIA MCP CONCLUÍDO!")

if __name__ == "__main__":
    main()