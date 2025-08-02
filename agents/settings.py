"""
Configurações para o agente PRP.

Este módulo gerencia todas as configurações do agente usando pydantic-settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Configurações para o agente PRP."""
    
    # LLM Configuration
    llm_provider: str = Field(default="openai", description="Provedor LLM (openai, anthropic)")
    llm_api_key: str = Field(..., description="Chave da API do LLM")
    llm_model: str = Field(default="gpt-4o", description="Modelo LLM a ser usado")
    llm_base_url: str = Field(default="https://api.openai.com/v1", description="URL base da API")
    
    # Database Configuration
    database_path: str = Field(default="../context-memory.db", description="Caminho para o banco de dados")
    
    # Agent Configuration
    max_tokens_per_analysis: int = Field(default=4000, description="Máximo de tokens por análise")
    analysis_timeout: int = Field(default=30, description="Timeout para análises em segundos")
    default_session_id: str = Field(default="prp-agent-session", description="ID da sessão padrão")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Nível de logging")
    log_file: str = Field(default="prp_agent.log", description="Arquivo de log")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = "LLM_"

# Instância global das configurações
settings = Settings() 