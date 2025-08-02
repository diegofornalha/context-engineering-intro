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
    
    # Language Configuration
    default_language: str = Field(default="pt-br", description="Idioma padrão para criação de PRPs")
    language_name: str = Field(default="Português do Brasil", description="Nome do idioma padrão")
    use_default_language: bool = Field(default=True, description="Usar idioma padrão automaticamente")
    
    # Sentry Configuration (Optional)
    sentry_dsn: str = Field(default="", description="Sentry DSN")
    sentry_auth_token: str = Field(default="", description="Sentry Auth Token")
    sentry_org: str = Field(default="", description="Sentry Organization")
    sentry_api_url: str = Field(default="", description="Sentry API URL")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Nível de logging")
    log_file: str = Field(default="prp_agent.log", description="Arquivo de log")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "allow"  # Permitir campos extras
    }

# Instância global das configurações
settings = Settings() 