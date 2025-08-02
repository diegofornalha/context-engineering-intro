"""
Provedores de modelo LLM para o agente PRP.

Este módulo gerencia a configuração e criação de modelos LLM.
"""

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.models.anthropic import AnthropicModel
from .settings import settings
import logging

logger = logging.getLogger(__name__)

def get_llm_model():
    """Obter modelo LLM configurado baseado nas configurações."""
    
    try:
        if settings.llm_provider.lower() == "openai":
            provider = OpenAIProvider(
                base_url=settings.llm_base_url,
                api_key=settings.llm_api_key
            )
            model = OpenAIModel(settings.llm_model, provider=provider)
            logger.info(f"Modelo OpenAI configurado: {settings.llm_model}")
            return model
            
        elif settings.llm_provider.lower() == "anthropic":
            provider = AnthropicProvider(
                api_key=settings.llm_api_key
            )
            model = AnthropicModel(settings.llm_model, provider=provider)
            logger.info(f"Modelo Anthropic configurado: {settings.llm_model}")
            return model
            
        else:
            raise ValueError(f"Provedor LLM não suportado: {settings.llm_provider}")
            
    except Exception as e:
        logger.error(f"Erro ao configurar modelo LLM: {e}")
        raise

def get_test_model():
    """Obter modelo de teste para desenvolvimento."""
    from pydantic_ai.models.test import TestModel
    logger.info("Usando modelo de teste para desenvolvimento")
    return TestModel()

def get_function_model():
    """Obter modelo de função para validação."""
    from pydantic_ai.models.function import FunctionModel
    logger.info("Usando modelo de função para validação")
    return FunctionModel() 