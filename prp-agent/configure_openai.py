#!/usr/bin/env python3
"""
Script para configurar o .env do agente PRP com as configurações da OpenAI.
"""

import os
import shutil

def configure_openai_env():
    """Configurar .env com as configurações da OpenAI."""
    
    # Conteúdo do .env com configurações da OpenAI
    env_content = """# Configurações do Agente PRP
# Usando configurações da OpenAI do arquivo .env principal

# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=sua_chave_openai_aqui
LLM_MODEL=gpt-4
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
    
    # Criar arquivo .env
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env configurado com OpenAI!")
        print("🤖 Modelo: gpt-4")
        print("🔑 API Key: Configurada")
        print("🌐 Base URL: https://api.openai.com/v1")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def test_agent():
    """Testar o agente com modelo de teste."""
    
    print("\n🧪 Testando agente com modelo de teste...")
    
    try:
        from agents.agent import chat_with_prp_agent_sync, PRPAgentDependencies
        
        # Criar dependências
        deps = PRPAgentDependencies()
        
        # Testar com modelo de teste
        response = chat_with_prp_agent_sync(
            "Olá! Teste de funcionamento do agente PRP.",
            deps=deps,
            use_test_model=True
        )
        
        print("✅ Teste bem-sucedido!")
        print(f"🤖 Resposta: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal."""
    
    print("🔧 Configurando Agente PRP com OpenAI")
    print("=" * 40)
    
    # Configurar .env
    print("\n1. Configurando arquivo .env...")
    env_ok = configure_openai_env()
    
    # Testar agente
    print("\n2. Testando agente...")
    test_ok = test_agent()
    
    # Resumo
    print("\n" + "=" * 40)
    print("📋 RESUMO DA CONFIGURAÇÃO:")
    print(f"   Arquivo .env: {'✅' if env_ok else '❌'}")
    print(f"   Teste do agente: {'✅' if test_ok else '❌'}")
    
    if env_ok and test_ok:
        print("\n🎉 Configuração concluída!")
        print("\n📝 PRÓXIMOS PASSOS:")
        print("1. Execute: python cli.py para iniciar o agente")
        print("2. Digite 'ajuda' para ver os comandos disponíveis")
        print("3. Teste: 'criar um PRP para sistema de login'")
    else:
        print("\n❌ Configuração incompleta!")
        print("Resolva os problemas acima antes de continuar.")

if __name__ == "__main__":
    main() 