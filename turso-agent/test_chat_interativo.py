#!/usr/bin/env python3
"""
Teste do Chat Interativo com o Turso Agent
Vamos perguntar sobre o PRP e ver suas respostas
"""

import sys
import os
from pathlib import Path
import asyncio

# Configurar ambiente de desenvolvimento
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "true"
os.environ["TURSO_API_TOKEN"] = "dev_token_for_testing"
os.environ["TURSO_ORGANIZATION"] = "dev_organization"
os.environ["TURSO_DEFAULT_DATABASE"] = "dev_database"

# Adicionar diretórios ao path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from agents.turso_specialist import TursoSpecialistAgent
from config.turso_settings import TursoSettings
from tools.turso_manager import TursoManager
from tools.mcp_integrator import MCPTursoIntegrator

async def chat_sobre_prp():
    """Chat interativo sobre o PRP"""
    
    print("\n💬 CHAT INTERATIVO COM TURSO AGENT SOBRE PRP")
    print("=" * 60)
    
    # Criar agente
    settings = TursoSettings()
    turso_manager = TursoManager(settings)
    mcp_integrator = MCPTursoIntegrator(settings)
    
    agent = TursoSpecialistAgent(
        turso_manager=turso_manager,
        mcp_integrator=mcp_integrator,
        settings=settings
    )
    
    print("✅ Agente inicializado!")
    print("\n🤖 Vamos conversar sobre o PRP...\n")
    
    # Perguntas sobre o PRP
    perguntas = [
        "O que você acha do PRP ID 6 - Agente Especialista em Turso Database?",
        "Você segue as diretrizes do PRP? Como você implementa elas?",
        "Quais são os principais validation gates do PRP que você utiliza?",
        "Como o PRP ajuda você a ser um especialista melhor?",
        "Você pode me dar exemplos práticos de como usa o PRP no dia a dia?",
        "Qual a importância da integração MCP descrita no PRP?",
        "Como você aplica as best practices de segurança do PRP?",
        "O que você acha mais valioso no PRP ID 6?"
    ]
    
    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n{'='*60}")
        print(f"👤 PERGUNTA {i}: {pergunta}")
        print(f"{'='*60}")
        
        resposta = await agent.chat(pergunta)
        print(f"\n🤖 TURSO AGENT: {resposta}")
        
        # Pequena pausa para facilitar leitura
        await asyncio.sleep(0.5)
    
    # Pergunta final aberta
    print(f"\n{'='*60}")
    print("👤 PERGUNTA FINAL: Você tem algo mais a dizer sobre o PRP ou sobre suas capacidades como especialista?")
    print(f"{'='*60}")
    
    resposta_final = await agent.chat(
        "Você tem algo mais a dizer sobre o PRP ou sobre suas capacidades como especialista?"
    )
    print(f"\n🤖 TURSO AGENT: {resposta_final}")
    
    print("\n" + "="*60)
    print("💡 CONCLUSÃO DO CHAT")
    print("="*60)

if __name__ == "__main__":
    print("🚀 Iniciando chat sobre PRP com o Turso Agent...")
    asyncio.run(chat_sobre_prp())
    print("\n✅ Chat concluído!")