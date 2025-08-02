#!/usr/bin/env python3
"""
🧪 Teste de Integração Sentry + FastAPI + PRP Agent
====================================================

Script para testar a integração completa do Sentry com
FastAPI e monitoramento de AI Agents.
"""

import asyncio
import httpx
import sentry_sdk
from loguru import logger
from dotenv import load_dotenv
import os

# Carregar configurações
load_dotenv()

async def test_sentry_integration():
    """Testar todas as funcionalidades da integração Sentry"""
    
    base_url = "http://localhost:8000"
    
    logger.info("🧪 Iniciando testes de integração Sentry...")
    
    async with httpx.AsyncClient() as client:
        
        # Teste 1: Health Check
        logger.info("📍 Teste 1: Health Check")
        try:
            response = await client.get(f"{base_url}/health")
            logger.success(f"✅ Health OK: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Health failed: {e}")
        
        # Teste 2: Rota principal
        logger.info("📍 Teste 2: Rota principal")
        try:
            response = await client.get(f"{base_url}/")
            data = response.json()
            logger.success(f"✅ Root OK: {data['status']}")
        except Exception as e:
            logger.error(f"❌ Root failed: {e}")
        
        # Teste 3: Processamento PRP (sucesso)
        logger.info("📍 Teste 3: Processamento PRP")
        try:
            prp_data = {
                "prompt": "Criar sistema de autenticação com JWT",
                "context": "Sistema web FastAPI",
                "user_id": "test_user_123"
            }
            response = await client.post(f"{base_url}/prp/process", json=prp_data)
            data = response.json()
            logger.success(f"✅ PRP processado: {data['status']}")
        except Exception as e:
            logger.error(f"❌ PRP failed: {e}")
        
        # Teste 4: Erro do Sentry (para testar captura)
        logger.info("📍 Teste 4: Teste de erro Sentry")
        try:
            response = await client.get(f"{base_url}/sentry-debug")
            # Esta requisição deve falhar
            logger.warning("🚨 Erro esperado não ocorreu!")
        except Exception as e:
            logger.success("✅ Erro capturado como esperado pelo Sentry")
    
    logger.info("🎉 Testes concluídos! Verifique o Sentry em:")
    logger.info("   https://sentry.io/organizations/coflow/projects/")

def test_sentry_manual():
    """Teste manual do Sentry (sem FastAPI)"""
    
    logger.info("🔧 Testando Sentry SDK diretamente...")
    
    # Configurar Sentry para teste
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        environment="test",
        traces_sample_rate=1.0
    )
    
    # Teste de captura de exceção
    try:
        sentry_sdk.set_context("test_context", {
            "test_type": "manual_sentry_test",
            "framework": "direct_sdk"
        })
        
        raise ValueError("🧪 Teste manual do Sentry SDK")
        
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.success("✅ Exceção enviada para Sentry")
    
    # Teste de mensagem
    sentry_sdk.capture_message("🚀 PRP Agent Sentry integration test", level="info")
    logger.success("✅ Mensagem enviada para Sentry")

if __name__ == "__main__":
    print("🧪 Escolha o tipo de teste:")
    print("1. Teste integração FastAPI (requer app rodando)")
    print("2. Teste manual Sentry SDK")
    
    choice = input("Digite 1 ou 2: ").strip()
    
    if choice == "1":
        print("\n💡 Primeiro inicie o servidor:")
        print("   python main.py")
        print("\nDepois execute este teste novamente.\n")
        asyncio.run(test_sentry_integration())
    elif choice == "2":
        test_sentry_manual()
    else:
        print("❌ Opção inválida")