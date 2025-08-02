#!/usr/bin/env python3
"""
Script de teste para verificar se a migração foi bem-sucedida.
"""

import sys

def test_imports():
    """Testar se todos os imports funcionam."""
    print("🧪 Testando imports...")
    
    try:
        from agents.agent import prp_agent, chat_with_prp_agent_sync, PRPAgentDependencies
        print("✅ Import agent.py OK")
    except Exception as e:
        print(f"❌ Erro em agent.py: {e}")
        return False
    
    try:
        from agents.tools import create_prp, search_prps, analyze_prp_with_llm
        print("✅ Import tools.py OK")
    except Exception as e:
        print(f"❌ Erro em tools.py: {e}")
        return False
    
    try:
        from agents.settings import settings
        print("✅ Import settings.py OK")
    except Exception as e:
        print(f"❌ Erro em settings.py: {e}")
        return False
    
    try:
        from agents.providers import get_llm_model, get_test_model
        print("✅ Import providers.py OK")
    except Exception as e:
        print(f"❌ Erro em providers.py: {e}")
        return False
    
    try:
        from agents.dependencies import PRPAgentDependencies
        print("✅ Import dependencies.py OK")
    except Exception as e:
        print(f"❌ Erro em dependencies.py: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Testar funcionalidade básica."""
    print("\n🧪 Testando funcionalidade básica...")
    
    try:
        from agents.agent import chat_with_prp_agent_sync, PRPAgentDependencies
        
        # Criar dependências
        deps = PRPAgentDependencies()
        print("✅ Dependências criadas")
        
        # Testar com modelo de teste
        response = chat_with_prp_agent_sync(
            "Olá! Este é um teste de migração.",
            deps,
            use_test_model=True
        )
        print("✅ Chat funcionando com modelo de teste")
        print(f"   Resposta: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na funcionalidade: {e}")
        return False

def main():
    """Executar todos os testes."""
    print("=" * 60)
    print("🚀 TESTE DE MIGRAÇÃO DO DIRETÓRIO AGENTS")
    print("=" * 60)
    
    # Testar imports
    imports_ok = test_imports()
    
    # Testar funcionalidade
    functionality_ok = test_basic_functionality()
    
    # Resultado final
    print("\n" + "=" * 60)
    if imports_ok and functionality_ok:
        print("✅ MIGRAÇÃO BEM-SUCEDIDA!")
        print("   Todos os testes passaram.")
    else:
        print("❌ PROBLEMAS NA MIGRAÇÃO!")
        print("   Verifique os erros acima.")
    print("=" * 60)
    
    return 0 if (imports_ok and functionality_ok) else 1

if __name__ == "__main__":
    sys.exit(main())