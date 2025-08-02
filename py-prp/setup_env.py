#!/usr/bin/env python3
"""
Script para configurar o ambiente do agente PRP.
"""

import os
import sys

def create_env_file():
    """Criar arquivo .env com configurações padrão."""
    
    env_content = """# Configurações do Agente PRP
# Copie este arquivo para .env e configure suas chaves

# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=sua_chave_openai_aqui
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1

# Database Configuration
DATABASE_PATH=../context-memory.db

# Agent Configuration
MAX_TOKENS_PER_ANALYSIS=4000
ANALYSIS_TIMEOUT=30
DEFAULT_SESSION_ID=prp-agent-session

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=prp_agent.log
"""
    
    # Verificar se .env já existe
    if os.path.exists('.env'):
        print("⚠️  Arquivo .env já existe!")
        response = input("Deseja sobrescrever? (y/N): ")
        if response.lower() != 'y':
            print("❌ Configuração cancelada.")
            return False
    
    # Criar arquivo .env
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado com sucesso!")
        print("📝 Edite o arquivo .env e configure sua chave da API OpenAI")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def check_dependencies():
    """Verificar se as dependências estão instaladas."""
    
    required_packages = [
        'pydantic-ai',
        'pydantic-settings', 
        'python-dotenv',
        'httpx',
        'rich'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Dependências faltando: {', '.join(missing_packages)}")
        print("📦 Execute: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ Todas as dependências estão instaladas!")
        return True

def check_database():
    """Verificar se o banco de dados existe."""
    
    db_path = "../context-memory.db"
    
    if os.path.exists(db_path):
        print(f"✅ Banco de dados encontrado: {db_path}")
        return True
    else:
        print(f"⚠️  Banco de dados não encontrado: {db_path}")
        print("💡 Execute o script setup_prp_database.py para criar o banco")
        return False

def main():
    """Função principal."""
    
    print("🔧 Configuração do Agente PRP")
    print("=" * 40)
    
    # Verificar dependências
    print("\n1. Verificando dependências...")
    deps_ok = check_dependencies()
    
    # Verificar banco de dados
    print("\n2. Verificando banco de dados...")
    db_ok = check_database()
    
    # Criar arquivo .env
    print("\n3. Configurando arquivo .env...")
    env_ok = create_env_file()
    
    # Resumo
    print("\n" + "=" * 40)
    print("📋 RESUMO DA CONFIGURAÇÃO:")
    print(f"   Dependências: {'✅' if deps_ok else '❌'}")
    print(f"   Banco de dados: {'✅' if db_ok else '⚠️'}")
    print(f"   Arquivo .env: {'✅' if env_ok else '❌'}")
    
    if deps_ok and env_ok:
        print("\n🎉 Configuração concluída!")
        print("\n📝 PRÓXIMOS PASSOS:")
        print("1. Edite o arquivo .env e configure sua chave da API OpenAI")
        print("2. Execute: python cli.py para iniciar o agente")
        print("3. Digite 'ajuda' para ver os comandos disponíveis")
    else:
        print("\n❌ Configuração incompleta!")
        print("Resolva os problemas acima antes de continuar.")

if __name__ == "__main__":
    main() 