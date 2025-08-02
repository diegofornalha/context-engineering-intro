#!/usr/bin/env python3
"""
🚀 Migração PRP Agent: pip → UV
===============================

Script para migrar o projeto PRP Agent do pip tradicional
para UV (ultra-fast Python package manager).
"""

import os
import subprocess
import sys
from datetime import datetime

def verificar_uv_instalado():
    """Verifica se UV está instalado"""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ UV instalado: {version}")
            return True
        else:
            print("❌ UV não encontrado")
            return False
    except FileNotFoundError:
        print("❌ UV não instalado")
        return False

def instalar_uv():
    """Instala UV se não estiver disponível"""
    print("🚀 Instalando UV...")
    
    try:
        # Instalar UV via pip (ironia, mas funciona)
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'uv'
        ], check=True, capture_output=True, text=True)
        
        print("✅ UV instalado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar UV: {e}")
        print("💡 Tente: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

def backup_arquivos_atuais():
    """Faz backup dos arquivos de dependências atuais"""
    backup_dir = f"backup_pip_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    arquivos = ['requirements.txt']
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            import shutil
            shutil.copy2(arquivo, f"{backup_dir}/{arquivo}")
            print(f"📁 Backup: {arquivo} → {backup_dir}/")
    
    return backup_dir

def criar_pyproject_toml():
    """Cria pyproject.toml otimizado para PRP Agent"""
    pyproject_content = '''[project]
name = "prp-agent"
version = "1.0.0"
description = "PRP Agent - PydanticAI com Sentry AI Monitoring"
authors = [
    {name = "Developer", email = "dev@example.com"}
]
readme = "README.md"
requires-python = ">=3.11"

dependencies = [
    "sentry-sdk[fastapi]>=1.40.0",
    "pydantic-ai>=0.0.1",
    "fastapi>=0.116.0",
    "uvicorn[standard]>=0.35.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.11.0",
    "httpx>=0.25.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
'''
    
    with open("pyproject.toml", "w") as f:
        f.write(pyproject_content)
    
    print("✅ pyproject.toml criado (otimizado para AI)")

def migrar_dependencias():
    """Migra dependências do requirements.txt para UV"""
    print("🔄 Migrando dependências para UV...")
    
    try:
        # Ler requirements.txt atual
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                deps = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
            print(f"📋 Encontradas {len(deps)} dependências:")
            for dep in deps:
                print(f"  • {dep}")
        
        # Inicializar projeto UV
        print("\n🚀 Inicializando projeto UV...")
        subprocess.run(['uv', 'init', '--no-readme'], check=True)
        
        # Adicionar dependências via UV
        if deps:
            print("📦 Adicionando dependências via UV...")
            for dep in deps:
                if dep:  # Ignorar linhas vazias
                    try:
                        result = subprocess.run(['uv', 'add', dep], 
                                               check=True, capture_output=True, text=True)
                        print(f"✅ Adicionado: {dep}")
                    except subprocess.CalledProcessError as e:
                        print(f"⚠️  Problema com {dep}: {e}")
        
        # Instalar dependências de desenvolvimento
        print("\n🛠️ Adicionando ferramentas de desenvolvimento...")
        dev_deps = [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0", 
            "black>=23.0.0",
            "ruff>=0.1.0"
        ]
        
        for dep in dev_deps:
            try:
                subprocess.run(['uv', 'add', '--dev', dep], check=True)
                print(f"✅ Dev tool: {dep}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Problema dev: {dep}")
        
        print("✅ Migração de dependências concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False

def testar_instalacao():
    """Testa se a instalação via UV funcionou"""
    print("\n🧪 Testando instalação UV...")
    
    try:
        # Testar imports principais
        imports_test = [
            "import sentry_sdk",
            "import pydantic_ai", 
            "import fastapi",
            "print('✅ Todos os imports funcionando!')"
        ]
        
        test_code = "; ".join(imports_test)
        
        result = subprocess.run([
            'uv', 'run', 'python', '-c', test_code
        ], capture_output=True, text=True, check=True)
        
        print("✅ Teste de imports: SUCESSO")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Teste falhou: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def gerar_comandos_uv():
    """Gera lista de comandos UV para uso diário"""
    comandos = """
🚀 COMANDOS UV PARA PRP AGENT:
=============================

📦 GERENCIAMENTO DE DEPENDÊNCIAS:
uv add sentry-sdk[fastapi]           # Adicionar dependência
uv add --dev pytest                  # Adicionar dependência de dev
uv remove package-name               # Remover dependência
uv sync                             # Sincronizar ambiente

🏃 EXECUÇÃO:
uv run python script.py             # Executar script
uv run pytest                       # Executar testes
uv run python -m pytest tests/      # Testes específicos
uv run black .                      # Formatar código

🔧 AMBIENTE:
uv venv                             # Criar ambiente virtual
uv pip install -r requirements.txt  # Compatibilidade pip
uv lock                             # Gerar lock file
uv tree                             # Ver árvore de dependências

⚡ PERFORMANCE:
uv add numpy torch                   # Instalar libs pesadas (ultra-rápido)
uv sync --frozen                     # Sync from lock (deployment)
uv cache clean                       # Limpar cache

🎯 ESPECÍFICO PRP AGENT:
uv run python sentry_ai_agent_setup.py    # Testar Sentry
uv run python -m agents.cli               # Executar agente CLI
uv add anthropic openai                    # Adicionar providers LLM
"""
    
    with open("UV_COMANDOS.md", "w") as f:
        f.write(comandos)
    
    print("✅ Guia de comandos UV criado: UV_COMANDOS.md")

def main():
    """Executa migração completa"""
    print("🚀 MIGRAÇÃO PRP AGENT: pip → UV")
    print("=" * 40)
    
    # 1. Verificar UV
    if not verificar_uv_instalado():
        if not instalar_uv():
            print("❌ Não foi possível instalar UV")
            return False
    
    # 2. Backup
    backup_dir = backup_arquivos_atuais()
    print(f"✅ Backup criado: {backup_dir}")
    
    # 3. Criar pyproject.toml
    criar_pyproject_toml()
    
    # 4. Migrar dependências
    if migrar_dependencias():
        print("✅ Dependências migradas!")
    else:
        print("❌ Problema na migração")
        return False
    
    # 5. Testar
    if testar_instalacao():
        print("✅ Instalação testada!")
    else:
        print("⚠️  Problemas no teste")
    
    # 6. Gerar guia
    gerar_comandos_uv()
    
    print("\n🎉 MIGRAÇÃO CONCLUÍDA!")
    print("📋 Próximos passos:")
    print("1. Use 'uv run' ao invés de 'python'")
    print("2. Use 'uv add' ao invés de 'pip install'") 
    print("3. Consulte UV_COMANDOS.md para referência")
    
    return True

if __name__ == "__main__":
    main()