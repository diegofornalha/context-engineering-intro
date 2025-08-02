"""
Turso Settings - Configurações especializadas para Turso Agent
Implementa todas as configurações necessárias para o agente especialista
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from dotenv import load_dotenv

@dataclass
class TursoSettings:
    """
    Configurações completas para Turso Agent
    
    Implementa padrões de segurança e configuração baseados no PRP ID 6:
    - Two-level authentication system
    - Secure token management  
    - Environment-based configuration
    - Development/Production separation
    """
    
    # Turso Core Configuration
    turso_api_token: Optional[str] = None
    turso_organization: Optional[str] = None
    default_database: Optional[str] = None
    
    # Database Configuration
    database_tokens: Dict[str, str] = field(default_factory=dict)
    database_urls: Dict[str, str] = field(default_factory=dict)
    
    # MCP Integration
    mcp_server_port: int = 3000
    mcp_server_host: str = "localhost"
    mcp_package_name: str = "@diegofornalha/mcp-turso-cloud"
    
    # Security Settings
    token_cache_ttl: int = 3600  # 1 hour
    max_token_age: int = 86400   # 24 hours
    enable_audit_logging: bool = True
    
    # Performance Settings
    connection_pool_size: int = 10
    query_timeout: int = 30
    max_retries: int = 3
    
    # Development Settings
    debug_mode: bool = False
    log_level: str = "INFO"
    environment: str = "development"
    
    def __post_init__(self):
        """Carrega configurações do ambiente"""
        self.load_from_environment()
        self.validate_configuration()
    
    def load_from_environment(self):
        """Carrega configurações de variáveis de ambiente e arquivos .env"""
        
        # Carregar arquivos .env em ordem de prioridade
        env_files = [
            Path(".env.local"),
            Path(".env"),
            Path("../.env.turso"),
            Path("../.env")
        ]
        
        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file)
                print(f"📄 Loaded env file: {env_file}")
        
        # Turso Core
        self.turso_api_token = os.getenv("TURSO_API_TOKEN")
        self.turso_organization = os.getenv("TURSO_ORGANIZATION") 
        self.default_database = os.getenv("TURSO_DEFAULT_DATABASE")
        
        # Database específicos
        self._load_database_configs()
        
        # MCP Settings
        self.mcp_server_port = int(os.getenv("MCP_SERVER_PORT", "3000"))
        self.mcp_server_host = os.getenv("MCP_SERVER_HOST", "localhost")
        
        # Environment
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug_mode = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Security
        self.enable_audit_logging = os.getenv("ENABLE_AUDIT_LOGGING", "true").lower() == "true"
        
    def _load_database_configs(self):
        """Carrega configurações de databases específicos"""
        
        # Carregar tokens de databases específicos
        for key, value in os.environ.items():
            if key.startswith("TURSO_DB_TOKEN_"):
                db_name = key.replace("TURSO_DB_TOKEN_", "").lower()
                self.database_tokens[db_name] = value
            elif key.startswith("TURSO_DB_URL_"):
                db_name = key.replace("TURSO_DB_URL_", "").lower()
                self.database_urls[db_name] = value
    
    def validate_configuration(self):
        """Valida configurações essenciais"""
        
        errors = []
        warnings = []
        
        # Validar configurações críticas
        if not self.turso_api_token:
            errors.append("TURSO_API_TOKEN não configurado")
        
        if not self.turso_organization:
            warnings.append("TURSO_ORGANIZATION não especificada")
        
        # Validar formato do token
        if self.turso_api_token:
            if not self._is_valid_token_format(self.turso_api_token):
                warnings.append("Formato do TURSO_API_TOKEN pode estar incorreto")
        
        # Validar configurações de database
        if not self.default_database and not self.database_tokens:
            warnings.append("Nenhum database configurado")
        
        # Reportar problemas
        if errors:
            error_msg = "\n".join([f"❌ {error}" for error in errors])
            raise ValueError(f"Configuração inválida:\n{error_msg}")
        
        if warnings:
            warning_msg = "\n".join([f"⚠️ {warning}" for warning in warnings])
            print(f"Avisos de configuração:\n{warning_msg}")
    
    def _is_valid_token_format(self, token: str) -> bool:
        """Valida formato básico do token Turso"""
        # Tokens Turso geralmente começam com algum prefixo específico
        if len(token) < 10:
            return False
        
        # Verificar se não é token de formato antigo (EdDSA)
        if token.startswith("eyJ") and "EdDSA" in token:
            return False  # Formato antigo não suportado
        
        return True
    
    def get_database_token(self, database_name: str) -> Optional[str]:
        """Obtém token para database específico"""
        return self.database_tokens.get(database_name.lower())
    
    def get_database_url(self, database_name: str) -> Optional[str]:
        """Obtém URL para database específico"""
        return self.database_urls.get(database_name.lower())
    
    def add_database_config(self, database_name: str, token: str, url: str):
        """Adiciona configuração para novo database"""
        db_name = database_name.lower()
        self.database_tokens[db_name] = token
        self.database_urls[db_name] = url
    
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento"""
        return self.environment.lower() == "development"
    
    def get_connection_string(self, database_name: str) -> Optional[str]:
        """Gera connection string completa para database"""
        url = self.get_database_url(database_name)
        token = self.get_database_token(database_name)
        
        if url and token:
            return f"{url}?authToken={token}"
        
        return None
    
    def export_mcp_config(self) -> Dict:
        """Exporta configuração para MCP server"""
        return {
            "organizationToken": self.turso_api_token,
            "defaultDatabase": self.default_database,
            "databaseTokens": self.database_tokens,
            "serverConfig": {
                "host": self.mcp_server_host,
                "port": self.mcp_server_port
            },
            "security": {
                "enableAuditLogging": self.enable_audit_logging,
                "tokenCacheTTL": self.token_cache_ttl
            }
        }
    
    def get_turso_cli_config(self) -> Dict:
        """Exporta configuração para Turso CLI"""
        return {
            "api_token": self.turso_api_token,
            "organization": self.turso_organization,
            "default_database": self.default_database
        }
    
    def summary(self) -> str:
        """Retorna resumo das configurações"""
        
        summary = "🔧 **TURSO AGENT CONFIGURATION SUMMARY:**\n\n"
        
        # Status geral
        summary += "**📊 Status Geral:**\n"
        summary += f"   🌍 Environment: {self.environment}\n"
        summary += f"   🔍 Debug Mode: {self.debug_mode}\n"
        summary += f"   📝 Log Level: {self.log_level}\n\n"
        
        # Configuração Turso
        summary += "**🗄️ Turso Configuration:**\n"
        summary += f"   🔑 API Token: {'✅ Configurado' if self.turso_api_token else '❌ Não configurado'}\n"
        summary += f"   🏢 Organization: {self.turso_organization or 'Não especificada'}\n"
        summary += f"   📊 Default DB: {self.default_database or 'Não definido'}\n"
        summary += f"   💾 Databases: {len(self.database_tokens)} configurados\n\n"
        
        # MCP Configuration
        summary += "**🔌 MCP Configuration:**\n"
        summary += f"   🌐 Server: {self.mcp_server_host}:{self.mcp_server_port}\n"
        summary += f"   📦 Package: {self.mcp_package_name}\n\n"
        
        # Security
        summary += "**🛡️ Security Settings:**\n"
        summary += f"   📋 Audit Logging: {'✅ Enabled' if self.enable_audit_logging else '❌ Disabled'}\n"
        summary += f"   ⏰ Token Cache TTL: {self.token_cache_ttl}s\n"
        summary += f"   🔄 Max Token Age: {self.max_token_age}s\n\n"
        
        # Performance
        summary += "**⚡ Performance Settings:**\n"
        summary += f"   🔗 Connection Pool: {self.connection_pool_size}\n"
        summary += f"   ⏱️ Query Timeout: {self.query_timeout}s\n"
        summary += f"   🔄 Max Retries: {self.max_retries}\n"
        
        return summary