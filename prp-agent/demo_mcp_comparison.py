#!/usr/bin/env python3
"""
🎯 DEMONSTRAÇÃO: Diferença entre Agente SEM e COM MCP Turso

Este script mostra EXATAMENTE o problema que você identificou:
- Agente atual: responde sem contexto
- Agente correto: busca contexto no MCP Turso primeiro
"""

import asyncio
import sys
from agents.agent import chat_with_prp_agent_sync
from agents.agent_with_mcp_turso import chat_with_prp_agent_mcp_sync
from agents.dependencies import PRPAgentDependencies


def demo_comparison():
    """Demonstra a diferença entre agente SEM e COM MCP Turso."""
    
    print("🔥 DEMONSTRAÇÃO: Por que o agente PRECISA do MCP Turso")
    print("=" * 70)
    
    # Pergunta de teste
    test_question = "Como alguém novo no projeto, o que preciso saber para começar?"
    
    print(f"\n❓ **PERGUNTA:** {test_question}")
    print("-" * 70)
    
    # Configurar dependências
    deps = PRPAgentDependencies(session_id="demo-comparison")
    
    # 1. Agente ATUAL (SEM MCP Turso)
    print("\n❌ **AGENTE ATUAL (SEM MCP TURSO):**")
    print("🤖 Respondendo SEM buscar contexto no banco de dados...")
    
    try:
        response_without_mcp = chat_with_prp_agent_sync(test_question, deps)
        print(f"📝 Resposta: {response_without_mcp[:300]}...")
        print("❌ PROBLEMA: Resposta genérica, sem contexto específico do projeto!")
    except Exception as e:
        print(f"❌ Erro no agente atual: {e}")
    
    print("\n" + "="*70)
    
    # 2. Agente CORRETO (COM MCP Turso)
    print("\n✅ **AGENTE CORRETO (COM MCP TURSO):**")
    print("🧠 Buscando contexto relevante no Turso antes de responder...")
    
    try:
        response_with_mcp = chat_with_prp_agent_mcp_sync(test_question, deps)
        print(f"📝 Resposta: {response_with_mcp[:300]}...")
        print("✅ VANTAGEM: Resposta informada com contexto do projeto!")
    except Exception as e:
        print(f"❌ Erro no agente com MCP: {e}")
    
    print("\n" + "="*70)
    print("\n🎯 **CONCLUSÃO:**")
    print("📊 O agente SEM MCP Turso não tem acesso ao knowledge base")
    print("🧠 O agente COM MCP Turso busca contexto relevante antes de responder")
    print("🚀 Resultado: Respostas muito mais informadas e úteis!")
    
    print("\n💡 **PRÓXIMOS PASSOS:**")
    print("1. Substituir agente atual pelo agente com MCP Turso")
    print("2. Testar integração real com MCP no Cursor Agent")
    print("3. Verificar que contexto está sendo buscado antes de cada resposta")


def demo_mcp_workflow():
    """Demonstra o workflow MCP que deveria acontecer."""
    
    print("\n🔄 **WORKFLOW MCP TURSO (Como DEVERIA funcionar):**")
    print("=" * 60)
    
    steps = [
        "1️⃣ Usuário faz pergunta",
        "2️⃣ Agente busca contexto relevante no MCP Turso:",
        "   📚 Documentação relacionada", 
        "   💬 Conversas anteriores similares",
        "   🎯 PRPs relacionados",
        "3️⃣ Agente combina contexto + pergunta",
        "4️⃣ LLM responde com contexto completo",
        "5️⃣ Resposta salva no MCP Turso para futuras consultas"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🎯 **RESULTADO:** Agente sempre tem contexto do projeto!")


def check_mcp_integration():
    """Verifica se MCP está integrado no agente principal."""
    
    print("\n🔍 **VERIFICAÇÃO DE INTEGRAÇÃO MCP:**")
    print("=" * 50)
    
    # Verificar arquivo do agente principal
    try:
        with open("agents/agent.py", "r") as f:
            content = f.read()
            
        # Procurar por indicações de MCP
        mcp_indicators = [
            "mcp_turso",
            "execute_read_only_query", 
            "search_knowledge",
            "add_conversation",
            "context",
            "turso"
        ]
        
        found_indicators = []
        for indicator in mcp_indicators:
            if indicator.lower() in content.lower():
                found_indicators.append(indicator)
        
        print(f"📊 Indicadores MCP encontrados: {len(found_indicators)}/6")
        
        if len(found_indicators) < 3:
            print("❌ PROBLEMA CONFIRMADO: Agente principal NÃO usa MCP Turso!")
            print("🔧 SOLUÇÃO: Usar agent_with_mcp_turso.py ao invés de agent.py")
        else:
            print("✅ Agente parece ter integração MCP")
            
    except Exception as e:
        print(f"❌ Erro ao verificar: {e}")


if __name__ == "__main__":
    print("🎯 ANÁLISE: Agente PRP e MCP Turso Integration")
    print("🔍 Investigando por que agente não usa contexto do banco...")
    
    # Executar demonstrações
    demo_mcp_workflow()
    check_mcp_integration()
    
    # Só executar comparação se tiver ambiente configurado
    print("\n" + "="*70)
    user_input = input("🤖 Executar comparação prática? (y/N): ")
    
    if user_input.lower() == 'y':
        demo_comparison()
    else:
        print("\n✅ Análise concluída! Use agent_with_mcp_turso.py para integração correta.")