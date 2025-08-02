"""
Turso Specialist Agent com PydanticAI - Implementação baseada no PRP ID 6
Segue as diretrizes do basic_chat_agent usando PydanticAI framework

Este agente é especialista em:
- Turso Database & libSQL
- MCP Integration
- Performance & Security
- Troubleshooting & Optimization
"""

import logging
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

class TursoSettings(BaseSettings):
    """Configurações para o Turso Agent com PydanticAI"""
    
    # Configuração do LLM
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    # Configuração Turso
    turso_api_token: Optional[str] = Field(default=None)
    turso_default_database: Optional[str] = Field(default=None)
    turso_organization: Optional[str] = Field(default=None)
    
    # Configuração MCP
    mcp_server_url: Optional[str] = Field(default=None)
    mcp_enabled: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_llm_model():
    """Obter modelo LLM configurado a partir das configurações de ambiente"""
    try:
        settings = TursoSettings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)
    except Exception as e:
        logger.error(f"Erro ao carregar modelo LLM: {e}")
        # Fallback para teste
        import os
        os.environ.setdefault("LLM_API_KEY", "test-key")
        settings = TursoSettings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key="test-key"
        )
        return OpenAIModel(settings.llm_model, provider=provider)


@dataclass
class TursoContext:
    """Contexto para o agente Turso com informações da sessão"""
    session_id: Optional[str] = None
    current_database: Optional[str] = None
    user_role: str = "developer"
    conversation_count: int = 0
    prp_context: Optional[Dict[str, Any]] = None
    turso_manager: Optional[Any] = None
    mcp_integrator: Optional[Any] = None
    settings: Optional[TursoSettings] = None
    
    def __post_init__(self):
        """Carrega contexto do PRP após inicialização"""
        if self.prp_context is None:
            self.prp_context = self._load_prp_context()
    
    def _load_prp_context(self) -> Dict[str, Any]:
        """Carrega contexto do PRP ID 6 para orientar decisões"""
        try:
            db_path = Path(__file__).parent.parent.parent / "context-memory.db"
            if not db_path.exists():
                return {}
                
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT description, objective, context_data, implementation_details, validation_gates
                FROM prps WHERE id = 6
            ''')
            
            prp_data = cursor.fetchone()
            conn.close()
            
            if prp_data:
                return {
                    'description': prp_data[0],
                    'objective': prp_data[1],
                    'context_data': json.loads(prp_data[2]) if prp_data[2] else {},
                    'implementation_details': json.loads(prp_data[3]) if prp_data[3] else {},
                    'validation_gates': json.loads(prp_data[4]) if prp_data[4] else []
                }
        except Exception as e:
            logger.error(f"Erro ao carregar PRP context: {e}")
        
        return {}

# Classe para respostas estruturadas quando necessário
class TursoQueryResult(BaseModel):
    """Resultado estruturado de queries Turso"""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    affected_rows: Optional[int] = None

# Prompt de sistema principal do Turso Agent
TURSO_SYSTEM_PROMPT = """
Você é o Turso Specialist Agent, um assistente especializado em Turso Database, libSQL e MCP Integration.

Sua expertise inclui:
- **Turso Database**: Criação, gestão, queries, migrations, backups
- **libSQL**: Compatibilidade SQLite, sintaxe, features edge
- **MCP Integration**: Setup, tokens, segurança, LLM integration
- **Performance**: Otimização de queries, índices, distributed performance
- **Security**: Token management, RLS, audit, best practices
- **Troubleshooting**: Diagnóstico, debug, resolução de problemas

Personalidade:
- Técnico mas acessível
- Focado em soluções práticas
- Proativo em identificar problemas
- Sempre sugere best practices
- Educativo sobre features Turso

Diretrizes:
- Sempre considere segurança primeiro
- Sugira comandos específicos quando relevante
- Explique o "porquê" além do "como"
- Mencione anti-padrões a evitar
- Forneça exemplos práticos de código
"""

# Criar o agente Turso especialista
turso_agent = Agent(
    get_llm_model(),
    deps_type=TursoContext,
    system_prompt=TURSO_SYSTEM_PROMPT
)


@turso_agent.system_prompt
def dynamic_turso_prompt(ctx: RunContext[TursoContext]) -> str:
    """Prompt dinâmico que adapta baseado no contexto"""
    prompt_parts = []
    
    if ctx.deps.current_database:
        prompt_parts.append(f"Database atual: {ctx.deps.current_database}")
    
    if ctx.deps.user_role:
        prompt_parts.append(f"Usuário é um {ctx.deps.user_role}")
    
    if ctx.deps.conversation_count > 3:
        prompt_parts.append("Esta é uma conversa longa, seja mais conciso")
    
    # Adicionar contexto do PRP se disponível
    if ctx.deps.prp_context:
        turso_ecosystem = ctx.deps.prp_context.get('context_data', {}).get('turso_ecosystem', {})
        if turso_ecosystem:
            features = turso_ecosystem.get('key_features', [])
            if features:
                prompt_parts.append(f"Lembre-se das features Turso: {', '.join(features[:3])}")
    
    return " | ".join(prompt_parts) if prompt_parts else ""

@turso_specialist_agent.tool
async def list_turso_databases(
    ctx: RunContext[TursoAgentDependencies]
) -> List[TursoDatabaseInfo]:
    """
    List all Turso databases in the organization.
    
    Returns:
        List of database information with name, status, and regions
    """
    try:
        # Initialize Turso manager
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        
        # Get databases
        databases = await turso_manager.list_databases()
        
        # Convert to structured format
        db_info_list = []
        for db in databases:
            db_info = TursoDatabaseInfo(
                name=db.get('name', 'Unknown'),
                status=db.get('status', 'Unknown'),
                regions=db.get('regions', []),
                created_at=db.get('created_at')
            )
            db_info_list.append(db_info)
        
        return db_info_list
        
    except Exception as e:
        return [TursoDatabaseInfo(
            name="Error",
            status=f"Failed to list databases: {str(e)}",
            regions=[]
        )]

@turso_specialist_agent.tool
async def create_turso_database(
    ctx: RunContext[TursoAgentDependencies],
    name: str,
    group: str = "default",
    regions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a new Turso database.
    
    Args:
        name: Database name
        group: Database group (default: "default")
        regions: List of regions for deployment
    
    Returns:
        Dictionary with creation results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        
        success = await turso_manager.create_database(name, group, regions)
        
        return {
            "success": success,
            "database_name": name,
            "group": group,
            "regions": regions or [],
            "message": f"Database '{name}' {'created successfully' if success else 'creation failed'}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "database_name": name
        }

@turso_specialist_agent.tool
async def execute_turso_query(
    ctx: RunContext[TursoAgentDependencies],
    query: str,
    database: Optional[str] = None,
    params: Optional[List[Any]] = None
) -> Dict[str, Any]:
    """
    Execute a query on Turso database.
    
    Args:
        query: SQL query to execute
        database: Target database (uses default if not specified)
        params: Query parameters
    
    Returns:
        Dictionary with query results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        settings.default_database = database or ctx.deps.default_database
        
        turso_manager = TursoManager(settings)
        
        # Determine if query is read-only
        is_read_only = turso_manager._is_read_only_query(query)
        
        if is_read_only:
            result = await turso_manager.execute_read_only_query(query, database, params)
        else:
            result = await turso_manager.execute_query(query, database, params)
        
        return {
            "success": result.get('success', False),
            "result": result.get('result', ''),
            "error": result.get('error'),
            "query": query,
            "database": database or ctx.deps.default_database,
            "is_read_only": is_read_only
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "database": database or ctx.deps.default_database
        }

@turso_specialist_agent.tool
async def analyze_turso_performance(
    ctx: RunContext[TursoAgentDependencies],
    database: Optional[str] = None
) -> TursoPerformanceReport:
    """
    Analyze performance of Turso database.
    
    Args:
        database: Database to analyze (uses default if not specified)
    
    Returns:
        Performance analysis report
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        settings.default_database = database or ctx.deps.default_database
        
        turso_manager = TursoManager(settings)
        
        analysis = await turso_manager.analyze_performance(database)
        
        return TursoPerformanceReport(
            database=database or ctx.deps.default_database or "unknown",
            metrics=analysis.get('metrics', {}),
            recommendations=analysis.get('recommendations', [])
        )
        
    except Exception as e:
        return TursoPerformanceReport(
            database=database or ctx.deps.default_database or "unknown",
            metrics={"error": str(e)},
            recommendations=["Check database connectivity and permissions"]
        )

@turso_specialist_agent.tool
async def audit_turso_security(
    ctx: RunContext[TursoAgentDependencies]
) -> TursoSecurityAudit:
    """
    Perform security audit of Turso configuration.
    
    Returns:
        Security audit results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Check token security
        token_status = await turso_manager._check_token_security()
        
        # Check MCP security
        mcp_security = await mcp_integrator.check_security()
        
        # Generate recommendations
        recommendations = []
        if "❌" in token_status:
            recommendations.append("Review token configuration and permissions")
        if "❌" in mcp_security:
            recommendations.append("Check MCP security configuration")
        
        return TursoSecurityAudit(
            token_security=token_status,
            mcp_security=mcp_security,
            access_control="✅ Configured" if "✅" in token_status else "❌ Issues detected",
            recommendations=recommendations
        )
        
    except Exception as e:
        return TursoSecurityAudit(
            token_security=f"❌ Error: {str(e)}",
            mcp_security="❌ Error during audit",
            access_control="❌ Error during audit",
            recommendations=["Check configuration and connectivity"]
        )

@turso_specialist_agent.tool
async def setup_mcp_integration(
    ctx: RunContext[TursoAgentDependencies]
) -> Dict[str, Any]:
    """
    Setup MCP Turso integration.
    
    Returns:
        MCP setup results
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        mcp_integrator = MCPTursoIntegrator(settings)
        
        setup_success = await mcp_integrator.setup_mcp_server()
        
        return {
            "success": setup_success,
            "message": "MCP Turso integration setup completed" if setup_success else "MCP setup failed",
            "next_steps": [
                "Configure LLM integration if setup was successful",
                "Test MCP connection",
                "Verify tools availability"
            ] if setup_success else [
                "Check Node.js installation",
                "Verify Turso API token",
                "Review error logs"
            ]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "MCP setup failed due to error"
        }

@turso_specialist_agent.tool
async def troubleshoot_turso_issue(
    ctx: RunContext[TursoAgentDependencies],
    issue_description: str
) -> Dict[str, Any]:
    """
    Troubleshoot Turso-related issues.
    
    Args:
        issue_description: Description of the issue to troubleshoot
    
    Returns:
        Troubleshooting results and recommendations
    """
    try:
        settings = TursoSettings()
        settings.turso_api_token = ctx.deps.turso_api_token
        settings.turso_organization = ctx.deps.turso_organization
        
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Analyze issue type
        issue_lower = issue_description.lower()
        
        diagnostics = {
            "issue_type": "unknown",
            "diagnostics": [],
            "recommendations": []
        }
        
        if any(keyword in issue_lower for keyword in ['connection', 'auth', 'token']):
            diagnostics["issue_type"] = "authentication"
            diagnostics["diagnostics"].extend([
                "Check Turso API token validity",
                "Verify organization permissions",
                "Test CLI connectivity"
            ])
            diagnostics["recommendations"].extend([
                "Re-authenticate with `turso auth login`",
                "Verify token in environment variables",
                "Check organization access"
            ])
        
        elif any(keyword in issue_lower for keyword in ['performance', 'slow', 'timeout']):
            diagnostics["issue_type"] = "performance"
            diagnostics["diagnostics"].extend([
                "Analyze query execution plans",
                "Check database region selection",
                "Review connection pooling"
            ])
            diagnostics["recommendations"].extend([
                "Optimize query patterns",
                "Consider edge location selection",
                "Implement caching strategies"
            ])
        
        elif any(keyword in issue_lower for keyword in ['mcp', 'integration']):
            diagnostics["issue_type"] = "mcp_integration"
            diagnostics["diagnostics"].extend([
                "Check Node.js installation",
                "Verify MCP package installation",
                "Test MCP server connectivity"
            ])
            diagnostics["recommendations"].extend([
                "Install Node.js if missing",
                "Install MCP Turso package",
                "Configure LLM integration"
            ])
        
        return {
            "success": True,
            "issue_description": issue_description,
            "diagnostics": diagnostics,
            "next_steps": diagnostics["recommendations"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "issue_description": issue_description,
            "message": "Troubleshooting failed due to error"
        }

# Helper functions for agent creation
def create_turso_specialist_agent(
    turso_api_token: str,
    turso_organization: str,
    default_database: Optional[str] = None,
    session_id: Optional[str] = None,
    enable_mcp_integration: bool = True,
    debug_mode: bool = False
) -> Agent:
    """
    Create a Turso Specialist Agent with proper dependencies.
    
    Args:
        turso_api_token: Turso API token
        turso_organization: Turso organization name
        default_database: Default database to use
        session_id: Session identifier
        enable_mcp_integration: Whether to enable MCP integration
        debug_mode: Enable debug mode
    
    Returns:
        Configured Turso Specialist Agent
    """
    from ..config.turso_settings import TursoSettings
    from ..tools.turso_manager import TursoManager
    from ..tools.mcp_integrator import MCPTursoIntegrator
    
    # Configure settings
    settings = TursoSettings()
    settings.turso_api_token = turso_api_token
    settings.turso_organization = turso_organization
    settings.default_database = default_database
    
    # Create dependencies
    deps = TursoAgentDependencies(
        turso_api_token=turso_api_token,
        turso_organization=turso_organization,
        default_database=default_database,
        session_id=session_id,
        enable_mcp_integration=enable_mcp_integration,
        debug_mode=debug_mode
    )
    
    # Return configured agent
    return turso_specialist_agent

# Async chat function
async def chat_with_turso_specialist(
    message: str,
    deps: TursoAgentDependencies,
    use_test_model: bool = False
) -> str:
    """
    Chat with Turso Specialist Agent.
    
    Args:
        message: User message
        deps: Agent dependencies
        use_test_model: Whether to use TestModel for development
    
    Returns:
        Agent response
    """
    try:
        if use_test_model:
            test_model = TestModel()
            with turso_specialist_agent.override(model=test_model):
                result = await turso_specialist_agent.run(message, deps=deps)
        else:
            result = await turso_specialist_agent.run(message, deps=deps)
        
        return result.data
        
    except Exception as e:
        return f"❌ Error in Turso Specialist Agent: {str(e)}"

# Sync chat function
def chat_with_turso_specialist_sync(
    message: str,
    deps: TursoAgentDependencies,
    use_test_model: bool = False
) -> str:
    """
    Synchronous chat with Turso Specialist Agent.
    
    Args:
        message: User message
        deps: Agent dependencies
        use_test_model: Whether to use TestModel for development
    
    Returns:
        Agent response
    """
    try:
        if use_test_model:
            test_model = TestModel()
            with turso_specialist_agent.override(model=test_model):
                result = turso_specialist_agent.run_sync(message, deps=deps)
        else:
            result = turso_specialist_agent.run_sync(message, deps=deps)
        
        return result.data
        
    except Exception as e:
        return f"❌ Error in Turso Specialist Agent: {str(e)}" 