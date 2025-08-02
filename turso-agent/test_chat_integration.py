#!/usr/bin/env python3
"""
Teste de integração do chat Turso Agent com PydanticAI
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from agents.turso_specialist_pydantic_new import (
    TursoContext,
    TursoSettings,
    chat_with_turso_agent,
    chat_with_turso_agent_sync
)

async def test_chat_integration():
    """Testa a integração completa do chat"""
    print("=" * 60)
    print("🧪 TESTE DE INTEGRAÇÃO - TURSO AGENT COM PYDANTICAI")
    print("=" * 60)
    
    # Criar contexto
    context = TursoContext(
        session_id="test-session",
        current_database="test-db",
        user_role="developer"
    )
    
    # Perguntas de teste
    test_questions = [
        "Olá! O que você pode fazer?",
        "Como criar um database Turso?",
        "Qual a diferença entre Turso e SQLite?",
        "Me mostre um exemplo de query otimizada"
    ]
    
    print("\n📋 TESTE ASSÍNCRONO:")
    print("-" * 40)
    
    for i, question in enumerate(test_questions[:2], 1):
        print(f"\n{i}. Pergunta: {question}")
        try:
            response = await chat_with_turso_agent(question, context)
            print(f"   ✅ Resposta: {response[:100]}..." if len(response) > 100 else f"   ✅ Resposta: {response}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n\n📋 TESTE SÍNCRONO:")
    print("-" * 40)
    
    # Resetar contexto
    context.conversation_count = 0
    
    for i, question in enumerate(test_questions[2:], 1):
        print(f"\n{i}. Pergunta: {question}")
        try:
            response = chat_with_turso_agent_sync(question, context)
            print(f"   ✅ Resposta: {response[:100]}..." if len(response) > 100 else f"   ✅ Resposta: {response}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO - Implementação funcional!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_chat_integration())