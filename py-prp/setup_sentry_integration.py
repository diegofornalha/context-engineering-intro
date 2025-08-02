#!/usr/bin/env python3
"""
🚨 Setup Automático: Sentry + PRP Agent
======================================

Script para configurar automaticamente a integração do Sentry
com todos os componentes do projeto PRP Agent.
"""

import os
import sys
import shutil
from pathlib import Path

def setup_sentry_integration():
    """
    Configura integração completa do Sentry com PRP Agent
    """
    print("🚨 Setup: Integração Sentry + PRP Agent")
    print("=" * 50)
    
    # 1. Verificar estrutura do projeto
    print("\n1️⃣ Verificando estrutura do projeto...")
    
    required_dirs = ["agents", "examples", "PRPs"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Diretórios faltando: {missing_dirs}")
        print("   Execute este script no diretório prp-agent/")
        return False
    
    print("✅ Estrutura do projeto validada")
    
    # 2. Verificar arquivos Sentry necessários
    print("\n2️⃣ Verificando arquivos de configuração Sentry...")
    
    required_files = [
        "sentry_prp_agent_setup.py",
        "prp_agent_sentry_integration.py", 
        "prp_agent_env_sentry.example",
        "GUIA_SENTRY_PRP_AGENT.md"
    ]
    
    missing_files = []
    for file_name in required_files:
        if not os.path.exists(file_name):
            missing_files.append(file_name)
        else:
            print(f"✅ Encontrado: {file_name}")
    
    if missing_files:
        print(f"⚠️  Arquivos faltando: {missing_files}")
        print("   Os arquivos foram criados no diretório correto?")
    
    # 3. Atualizar requirements.txt
    print("\n3️⃣ Atualizando requirements.txt...")
    
    sentry_requirement = "sentry-sdk[fastapi]==1.40.0"
    
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        if "sentry-sdk" not in content:
            with open("requirements.txt", "a") as f:
                f.write(f"\n# Sentry monitoring\n{sentry_requirement}\n")
            print("✅ Sentry adicionado ao requirements.txt")
        else:
            print("✅ Sentry já presente no requirements.txt")
    else:
        with open("requirements.txt", "w") as f:
            f.write(f"# PRP Agent dependencies\n{sentry_requirement}\n")
        print("✅ requirements.txt criado com Sentry")
    
    # 4. Atualizar agents/settings.py
    print("\n4️⃣ Atualizando configurações do agente...")
    
    settings_file = "agents/settings.py"
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            content = f.read()
        
        # Verificar se já tem configuração Sentry
        if "sentry_dsn" not in content.lower():
            # Adicionar campos Sentry
            sentry_config = '''
    # Sentry Configuration
    sentry_dsn: str = Field(default="", description="Sentry DSN para monitoramento")
    sentry_environment: str = Field(default="development", description="Ambiente Sentry")
    enable_sentry_monitoring: bool = Field(default=True, description="Habilitar monitoramento Sentry")
'''
            
            # Inserir antes da class Config
            if "class Config:" in content:
                content = content.replace("class Config:", sentry_config + "\n    class Config:")
                
                with open(settings_file, "w") as f:
                    f.write(content)
                print("✅ Configurações Sentry adicionadas a settings.py")
            else:
                print("⚠️  Estrutura de settings.py não reconhecida")
        else:
            print("✅ Configurações Sentry já presentes")
    else:
        print("⚠️  Arquivo settings.py não encontrado")
    
    # 5. Criar arquivo de configuração .env
    print("\n5️⃣ Configurando arquivo .env...")
    
    if not os.path.exists(".env.sentry"):
        if os.path.exists("prp_agent_env_sentry.example"):
            shutil.copy2("prp_agent_env_sentry.example", ".env.sentry")
            print("✅ Arquivo .env.sentry criado")
            print("   ⚠️  Configure seu SENTRY_DSN em .env.sentry")
        else:
            print("⚠️  Arquivo de exemplo não encontrado")
    else:
        print("✅ Arquivo .env.sentry já existe")
    
    # 6. Verificar se venv existe
    print("\n6️⃣ Verificando ambiente virtual...")
    
    if os.path.exists("venv/bin/activate"):
        print("✅ Ambiente virtual encontrado")
        print("💡 Para instalar Sentry, execute:")
        print("   source venv/bin/activate")
        print("   pip install sentry-sdk[fastapi]==1.40.0")
    else:
        print("⚠️  Ambiente virtual não encontrado")
        print("💡 Crie um ambiente virtual:")
        print("   python -m venv venv")
        print("   source venv/bin/activate") 
        print("   pip install -r requirements.txt")
    
    # 7. Criar script de exemplo de uso
    print("\n7️⃣ Criando exemplo de uso...")
    
    example_content = '''#!/usr/bin/env python3
"""
Exemplo de uso do PRP Agent com monitoramento Sentry
"""

import asyncio
import os
from sentry_prp_agent_setup import configure_sentry_for_prp_agent

async def demo_with_sentry():
    """Demo do PRP Agent com Sentry"""
    
    # Configurar Sentry (substitua pelo seu DSN)
    sentry_dsn = os.getenv("SENTRY_DSN", "https://your-dsn@sentry.io/project")
    
    if "your-dsn" in sentry_dsn:
        print("⚠️  Configure SENTRY_DSN no arquivo .env.sentry")
        print("   1. Crie um projeto no Sentry")
        print("   2. Copie o DSN")
        print("   3. Configure em .env.sentry")
        return
    
    # Configurar Sentry
    configure_sentry_for_prp_agent(sentry_dsn, "development")
    
    print("🚨 PRP Agent com Sentry ativo!")
    print("📊 Verifique eventos em https://sentry.io/")
    
    # Capturar evento de teste
    import sentry_sdk
    sentry_sdk.capture_message("PRP Agent com Sentry funcionando!", level="info")
    
    print("✅ Evento de teste enviado para Sentry")

if __name__ == "__main__":
    asyncio.run(demo_with_sentry())
'''
    
    with open("exemplo_sentry.py", "w") as f:
        f.write(example_content)
    print("✅ Exemplo criado: exemplo_sentry.py")
    
    return True

def create_sentry_project_guide():
    """
    Cria guia para criar projeto no Sentry
    """
    guide_content = '''# 🚨 Como Criar Projeto Sentry para PRP Agent

## 1. Acesse o Sentry
- Vá para https://sentry.io/
- Faça login ou crie uma conta

## 2. Criar Novo Projeto
1. Clique em "Create Project"
2. Escolha "Python" como plataforma
3. Nome do projeto: "PRP Agent Python Monitoring"
4. Clique em "Create Project"

## 3. Configurar DSN
1. Copie o DSN exibido (formato: https://xxx@sentry.io/xxx)
2. Cole no arquivo .env.sentry:
   ```
   SENTRY_DSN=https://seu-dsn-aqui@sentry.io/projeto-id
   ```

## 4. Testar Integração
```bash
# Configure o DSN primeiro
export SENTRY_DSN="seu-dsn-aqui"

# Execute o exemplo
python exemplo_sentry.py
```

✅ Pronto! Seu PRP Agent agora tem monitoramento profissional.
'''
    
    with open("SENTRY_PROJECT_GUIDE.md", "w") as f:
        f.write(guide_content)
    print("✅ Guia criado: SENTRY_PROJECT_GUIDE.md")

def main():
    """Função principal"""
    
    # Verificar se está no diretório correto
    if not os.path.exists("agents") or not os.path.exists("PRPs"):
        print("❌ Execute este script no diretório prp-agent/")
        print("   Estrutura esperada: prp-agent/agents/, prp-agent/PRPs/")
        sys.exit(1)
    
    # Executar setup
    success = setup_sentry_integration()
    
    if success:
        # Criar guia adicional
        create_sentry_project_guide()
        
        print("\n🎉 Setup concluído!")
        print("=" * 50)
        print("📋 Próximos passos:")
        print("1. Configure SENTRY_DSN em .env.sentry")
        print("2. Ative o ambiente virtual: source venv/bin/activate")
        print("3. Instale dependências: pip install sentry-sdk[fastapi]==1.40.0")
        print("4. Execute o exemplo: python exemplo_sentry.py")
        print("5. Verifique eventos em https://sentry.io/")
        print("\n📖 Leia o GUIA_SENTRY_PRP_AGENT.md para detalhes completos")
    else:
        print("\n❌ Setup falhado. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()