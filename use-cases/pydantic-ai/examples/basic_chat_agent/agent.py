"""
Agente de Chat Básico com Memória e Contexto

Um agente conversacional simples que demonstra os padrões principais do PydanticAI:
- Configuração de modelo baseada em ambiente
- Prompts de sistema para personalidade e comportamento
- Manipulação básica de conversação com memória
- Saída de string (padrão, não precisa de result_type)
"""

import logging
from dataclasses import dataclass
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configurações para o agente de chat."""
    
    # Configuração do LLM
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_llm_model() -> OpenAIModel:
    """Obter modelo LLM configurado a partir das configurações de ambiente."""
    try:
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)
    except Exception:
        # Para testes sem variáveis de ambiente
        import os
        os.environ.setdefault("LLM_API_KEY", "test-key")
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key="test-key"
        )
        return OpenAIModel(settings.llm_model, provider=provider)


@dataclass
class ConversationContext:
    """Contexto simples para gerenciamento de estado da conversação."""
    user_name: Optional[str] = None
    conversation_count: int = 0
    preferred_language: str = "English"
    session_id: Optional[str] = None


SYSTEM_PROMPT = """
Você é um assistente de IA amigável e prestativo.

Sua personalidade:
- Caloroso e acessível
- Conhecedor mas humilde
- Paciente e compreensivo
- Encorajador e solidário

Diretrizes:
- Mantenha as respostas conversacionais e naturais
- Seja útil sem ser esmagador
- Faça perguntas de acompanhamento quando apropriado
- Lembre-se do contexto da conversação
- Adapte seu tom para atender às necessidades do usuário
"""


# Criar o agente de chat básico - nota: sem result_type, padrão é string
chat_agent = Agent(
    get_llm_model(),
    deps_type=ConversationContext,
    system_prompt=SYSTEM_PROMPT
)


@chat_agent.system_prompt
def dynamic_context_prompt(ctx) -> str:
    """Prompt de sistema dinâmico que inclui contexto da conversação."""
    prompt_parts = []
    
    if ctx.deps.user_name:
        prompt_parts.append(f"O nome do usuário é {ctx.deps.user_name}.")
    
    if ctx.deps.conversation_count > 0:
        prompt_parts.append(f"Esta é a mensagem #{ctx.deps.conversation_count + 1} em sua conversação.")
    
    if ctx.deps.preferred_language != "English":
        prompt_parts.append(f"O usuário prefere se comunicar em {ctx.deps.preferred_language}.")
    
    return " ".join(prompt_parts) if prompt_parts else ""


async def chat_with_agent(message: str, context: Optional[ConversationContext] = None) -> str:
    """
    Função principal para conversar com o agente.
    
    Args:
        message: Mensagem do usuário para o agente
        context: Contexto opcional da conversação para memória
    
    Returns:
        Resposta em string do agente
    """
    if context is None:
        context = ConversationContext()
    
    # Incrementar contador de conversação
    context.conversation_count += 1
    
    # Executar o agente com a mensagem e contexto
    result = await chat_agent.run(message, deps=context)
    
    return result.data


def chat_with_agent_sync(message: str, context: Optional[ConversationContext] = None) -> str:
    """
    Versão síncrona de chat_with_agent para casos de uso simples.
    
    Args:
        message: Mensagem do usuário para o agente
        context: Contexto opcional da conversação para memória
    
    Returns:
        Resposta em string do agente
    """
    if context is None:
        context = ConversationContext()
    
    # Incrementar contador de conversação
    context.conversation_count += 1
    
    # Executar o agente sincronamente
    result = chat_agent.run_sync(message, deps=context)
    
    return result.data


# Exemplo de uso e demonstração
if __name__ == "__main__":
    import asyncio
    
    async def demo_conversation():
        """Demonstrar o agente de chat básico com uma conversação simples."""
        print("=== Demonstração do Agente de Chat Básico ===\n")
        
        # Criar contexto da conversação
        context = ConversationContext(
            user_name="Alex",
            preferred_language="English"
        )
        
        # Conversação de exemplo
        messages = [
            "Olá! Meu nome é Alex, prazer em conhecê-lo.",
            "Você pode me ajudar a entender o que é PydanticAI?",
            "Isso é interessante! O que o torna diferente de outros frameworks de IA?",
            "Obrigado pela explicação. Você pode recomendar alguns bons recursos para aprender mais?"
        ]
        
        for message in messages:
            print(f"Usuário: {message}")
            
            response = await chat_with_agent(message, context)
            
            print(f"Agente: {response}")
            print("-" * 50)
    
    # Executar a demonstração
    asyncio.run(demo_conversation())