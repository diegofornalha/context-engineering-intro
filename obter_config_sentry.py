#!/usr/bin/env python3
"""
🔧 Script para Obter Configurações do Novo Projeto Sentry
========================================================

Script interativo para ajudar a obter e configurar as credenciais
do novo projeto PRP Agent no Sentry.
"""

import os
import requests
import json
from datetime import datetime

def verificar_organizacao_atual():
    """
    Verifica se a organização 'coflow' ainda está acessível
    """
    print("🔍 Verificando organização atual...")
    
    # Usar token atual para verificar
    token_atual = "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"
    
    headers = {
        "Authorization": f"Bearer {token_atual}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://sentry.io/api/0/organizations/coflow/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            org_data = response.json()
            print(f"✅ Organização: {org_data.get('name', 'coflow')}")
            print(f"✅ Slug: {org_data.get('slug', 'coflow')}")
            return True
        else:
            print(f"⚠️  Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar organização: {e}")
        return False

def listar_projetos_existentes():
    """
    Lista projetos existentes na organização
    """
    print("\n📋 Listando projetos existentes...")
    
    token_atual = "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"
    
    headers = {
        "Authorization": f"Bearer {token_atual}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://sentry.io/api/0/organizations/coflow/projects/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Encontrados {len(projects)} projetos:")
            
            for project in projects:
                print(f"  • {project.get('name')} ({project.get('slug')})")
                if 'prp' in project.get('name', '').lower() or 'agent' in project.get('name', '').lower():
                    print(f"    🎯 Possível projeto PRP Agent: {project.get('slug')}")
                    return project.get('slug'), project.get('name')
            
            return None, None
        else:
            print(f"⚠️  Não foi possível listar projetos: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Erro ao listar projetos: {e}")
        return None, None

def gerar_instrucoes_configuracao():
    """
    Gera instruções passo-a-passo personalizadas
    """
    print("\n" + "="*60)
    print("🎯 INSTRUÇÕES PARA OBTER NOVAS CONFIGURAÇÕES")
    print("="*60)
    
    print("\n1️⃣ CRIAR PROJETO SENTRY:")
    print("   🌐 Acesse: https://sentry.io/organizations/coflow/projects/new/")
    print("   📋 Nome: 'PRP Agent Python Monitoring'")
    print("   🏷️ Slug: 'prp-agent-python-monitoring'")
    print("   🐍 Plataforma: Python")
    print("   🤖 IMPORTANTE: Habilite 'AI Agent Monitoring (Beta)'")
    
    print("\n2️⃣ OBTER NOVO DSN:")
    print("   📄 Na tela de setup, copie o DSN completo")
    print("   📋 Formato: https://NOVA-KEY@o927801.ingest.us.sentry.io/NOVO-ID")
    
    print("\n3️⃣ GERAR NOVO AUTH TOKEN:")
    print("   🔗 Acesse: https://sentry.io/settings/coflow/auth-tokens/")
    print("   ➕ Clique 'Create New Token'")
    print("   📝 Nome: 'PRP Agent Token'")
    print("   ✅ Scopes necessários:")
    print("      • project:read")
    print("      • project:write")
    print("      • event:read")
    print("      • event:write")
    print("      • org:read")
    
    print("\n4️⃣ CONFIGURAR ARQUIVO .env:")
    print("   📁 Edite o arquivo .env.sentry:")
    print("   📝 Substitua:")
    print("      SENTRY_DSN=NOVO-DSN-COPIADO")
    print("      SENTRY_AUTH_TOKEN=NOVO-TOKEN-GERADO")

def testar_configuracao_nova():
    """
    Testa se as novas configurações estão funcionando
    """
    print("\n🧪 TESTE DAS NOVAS CONFIGURAÇÕES")
    print("="*40)
    
    # Verificar se existe arquivo .env.sentry
    if os.path.exists(".env.sentry"):
        print("✅ Arquivo .env.sentry encontrado")
        
        # Ler configurações
        with open(".env.sentry", "r") as f:
            content = f.read()
        
        if "NOVO-DSN-AQUI" in content:
            print("⚠️  DSN ainda não configurado (NOVO-DSN-AQUI)")
        else:
            print("✅ DSN parece configurado")
        
        if "NOVO-TOKEN-AQUI" in content:
            print("⚠️  Token ainda não configurado (NOVO-TOKEN-AQUI)")
        else:
            print("✅ Token parece configurado")
    else:
        print("❌ Arquivo .env.sentry não encontrado")
        print("💡 Execute: cp sentry_config_novo_projeto.env .env.sentry")

def executar_teste_sentry():
    """
    Executa teste básico do Sentry
    """
    print("\n🚀 EXECUTANDO TESTE BÁSICO...")
    
    try:
        # Tentar importar e configurar Sentry
        import sentry_sdk
        
        # Verificar se DSN está configurado
        dsn = os.getenv("SENTRY_DSN")
        if dsn and "NOVO-DSN-AQUI" not in dsn:
            sentry_sdk.init(dsn=dsn, environment="test")
            
            # Enviar evento de teste
            sentry_sdk.capture_message("🧪 Teste de configuração PRP Agent", level="info")
            
            print("✅ Evento de teste enviado!")
            print("📊 Verifique em: https://sentry.io/organizations/coflow/issues/")
        else:
            print("⚠️  DSN não configurado corretamente")
    
    except ImportError:
        print("⚠️  Sentry SDK não instalado")
        print("💡 Execute: pip install sentry-sdk")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

def main():
    """
    Função principal
    """
    print("🔧 CONFIGURAÇÃO SENTRY - NOVO PROJETO PRP AGENT")
    print("="*55)
    
    # 1. Verificar organização atual
    org_ok = verificar_organizacao_atual()
    
    # 2. Listar projetos existentes
    if org_ok:
        project_slug, project_name = listar_projetos_existentes()
        
        if project_slug and 'prp' in project_slug.lower():
            print(f"\n🎯 Projeto PRP Agent encontrado: {project_name}")
            print(f"   Slug: {project_slug}")
            print("   💡 Você pode usar este projeto existente")
        else:
            print("\n⚠️  Projeto PRP Agent não encontrado")
            print("   💡 Será necessário criar novo projeto")
    
    # 3. Gerar instruções
    gerar_instrucoes_configuracao()
    
    # 4. Testar configuração atual
    testar_configuracao_nova()
    
    # 5. Executar teste se possível
    print("\n" + "="*60)
    print("🧪 TESTE FINAL")
    print("="*60)
    
    # Carregar variáveis de ambiente se existir arquivo
    if os.path.exists(".env.sentry"):
        try:
            with open(".env.sentry", "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
        except:
            pass
    
    executar_teste_sentry()
    
    print("\n🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("📖 Consulte o GUIA_AI_AGENT_MONITORING.md para próximos passos")

if __name__ == "__main__":
    main()