#!/usr/bin/env python3
"""
🐍 Configuração do Sentry para Projeto Python
================================================================

Este script demonstra como configurar Sentry em um projeto Python
usando as melhores práticas de monitoramento de erros.

Baseado na documentação oficial e integração com MCP Sentry.
"""

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
import logging
import sys

def configure_sentry(dsn: str, environment: str = "development", debug: bool = False):
    """
    Configura o Sentry SDK para Python
    
    Args:
        dsn: Data Source Name do projeto Sentry
        environment: Ambiente (development, staging, production)
        debug: Habilitar modo debug
    """
    
    # Configurar integração com logging
    logging_integration = LoggingIntegration(
        level=logging.INFO,        # Captura logs level INFO e acima
        event_level=logging.ERROR  # Envia eventos level ERROR e acima
    )
    
    # Configurar Sentry
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        debug=debug,
        
        # Integrações
        integrations=[
            logging_integration,
            StdlibIntegration(auto_enabling=True),
            ExcepthookIntegration(always_run=True),
        ],
        
        # Performance
        traces_sample_rate=1.0 if environment == "development" else 0.1,
        
        # Release Health
        auto_session_tracking=True,
        
        # Configurações de captura
        attach_stacktrace=True,
        send_default_pii=False,  # Não enviar informações pessoais
        
        # Filtros
        before_send=filter_events,
    )
    
    print(f"✅ Sentry configurado para ambiente: {environment}")

def filter_events(event, hint):
    """
    Filtra eventos antes de enviar para o Sentry
    """
    # Ignorar erros de teclado (Ctrl+C)
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, KeyboardInterrupt):
            return None
    
    return event

def test_sentry_integration():
    """
    Testa a integração com Sentry
    """
    print("\n🧪 Testando integração com Sentry...")
    
    # 1. Capturar mensagem de info
    sentry_sdk.capture_message("Projeto Python configurado com Sentry", level="info")
    print("✅ Mensagem de info enviada")
    
    # 2. Capturar warning
    logging.warning("Este é um warning de teste")
    print("✅ Warning enviado")
    
    # 3. Adicionar contexto de usuário
    sentry_sdk.set_user({
        "id": "python-developer",
        "username": "dev",
        "email": "dev@example.com"
    })
    print("✅ Contexto de usuário definido")
    
    # 4. Adicionar tag personalizada
    sentry_sdk.set_tag("project_type", "python")
    sentry_sdk.set_tag("framework", "fastapi")
    print("✅ Tags personalizadas adicionadas")
    
    # 5. Capturar exceção (comentado para não gerar erro real)
    # try:
    #     raise ValueError("Erro de teste para demonstração")
    # except Exception as e:
    #     sentry_sdk.capture_exception(e)
    #     print("✅ Exceção capturada")

def main():
    """
    Função principal - demonstração de uso
    """
    print("🐍 Configuração de Projeto Python com Sentry")
    print("=" * 50)
    
    # IMPORTANTE: Substitua pelo DSN do seu projeto
    DSN = "https://your-dsn-here@sentry.io/your-project-id"
    
    if DSN == "https://your-dsn-here@sentry.io/your-project-id":
        print("⚠️  AVISO: Configure o DSN do seu projeto Sentry!")
        print("   1. Crie um projeto no Sentry")
        print("   2. Copie o DSN do projeto")
        print("   3. Substitua a variável DSN neste arquivo")
        return
    
    # Configurar Sentry
    configure_sentry(
        dsn=DSN,
        environment="development",
        debug=True
    )
    
    # Testar integração
    test_sentry_integration()
    
    print("\n🎉 Configuração concluída!")
    print("📊 Verifique os eventos no dashboard do Sentry")

if __name__ == "__main__":
    main()