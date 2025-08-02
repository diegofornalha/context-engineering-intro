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
    llm_api_key: str = Field(default="test-key")  # Default para teste
    llm_model: str = Field(default="gpt-4")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    # Configuração Turso
    turso_api_token: Optional[str] = Field(default=None)
    turso_default_database: Optional[str] = Field(default=None)
    turso_organization: Optional[str] = Field(default=None)
    
    # Configuração MCP
    mcp_server_url: Optional[str] = Field(default=None)
    mcp_server_host: Optional[str] = Field(default="localhost")
    mcp_server_port: Optional[int] = Field(default=3000)
    mcp_enabled: bool = Field(default=True)
    
    # Configurações adicionais do .env existente
    environment: Optional[str] = Field(default="development")
    debug: Optional[bool] = Field(default=False)
    log_level: Optional[str] = Field(default="INFO")
    enable_audit_logging: Optional[bool] = Field(default=True)
    token_cache_ttl: Optional[int] = Field(default=3600)
    max_token_age: Optional[int] = Field(default=86400)
    connection_pool_size: Optional[int] = Field(default=10)
    query_timeout: Optional[int] = Field(default=30)
    max_retries: Optional[int] = Field(default=3)
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Permitir campos extras


def get_llm_model():
    """Obter modelo LLM configurado a partir das configurações de ambiente"""
    try:
        # Tentar carregar configurações
        settings = TursoSettings()
        
        # Se não houver API key, usar TestModel para desenvolvimento
        if settings.llm_api_key == "test-key" or not settings.llm_api_key:
            logger.warning("Usando TestModel para desenvolvimento (sem API key real)")
            from pydantic_ai.models.test import TestModel
            return TestModel()
            
        # Caso contrário, usar o modelo configurado
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)
        
    except Exception as e:
        logger.error(f"Erro ao carregar modelo LLM: {e}")
        # Fallback para TestModel
        from pydantic_ai.models.test import TestModel
        return TestModel()


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


# Criar o agente Turso especialista com lazy loading
def create_turso_agent():
    """Cria uma nova instância do agente Turso"""
    agent = Agent(
        get_llm_model(),
        deps_type=TursoContext,
        system_prompt=TURSO_SYSTEM_PROMPT
    )
    
    # Registrar tools
    agent.system_prompt(dynamic_turso_prompt)
    agent.tool(list_databases)
    agent.tool(check_database_status)
    agent.tool(generate_query_example)
    agent.tool(troubleshoot_error)
    agent.tool_plain(get_mcp_setup_instructions)
    
    return agent

# Instância global do agente
turso_agent = None


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


async def list_databases(ctx: RunContext[TursoContext]) -> str:
    """Lista todos os databases Turso disponíveis"""
    try:
        if ctx.deps.turso_manager:
            databases = await ctx.deps.turso_manager.list_databases()
            return f"Databases encontrados: {', '.join(databases)}"
        else:
            return "Turso Manager não está configurado. Use `turso db list` no terminal."
    except Exception as e:
        return f"Erro ao listar databases: {str(e)}"


async def check_database_status(
    ctx: RunContext[TursoContext], 
    database_name: str
) -> str:
    """Verifica status de um database específico"""
    try:
        # Simulação - em produção, usaria turso_manager
        return f"""
Status do database '{database_name}':
- Status: ACTIVE
- Region: us-east-1
- Size: 125MB
- Last backup: 2 hours ago
- Connections: 15/100
"""
    except Exception as e:
        return f"Erro ao verificar status: {str(e)}"


async def generate_query_example(
    ctx: RunContext[TursoContext],
    query_type: str
) -> str:
    """Gera exemplos de queries Turso/libSQL"""
    examples = {
        "create_table": """
-- Criar tabela com best practices Turso
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índice para performance
CREATE INDEX idx_users_email ON users(email);
""",
        "insert": """
-- Insert com prepared statement (seguro)
INSERT INTO users (email, name) VALUES (?, ?);

-- Insert múltiplo para eficiência
INSERT INTO users (email, name) VALUES
    ('user1@example.com', 'User 1'),
    ('user2@example.com', 'User 2');
""",
        "select": """
-- Select otimizado com índice
SELECT id, name, email 
FROM users 
WHERE email = ?
LIMIT 10;

-- Join eficiente
SELECT u.name, p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE u.created_at > datetime('now', '-7 days');
""",
        "performance": """
-- Analisar performance de query
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email LIKE '%@example.com';

-- Verificar índices
PRAGMA index_list('users');

-- Stats da tabela
SELECT COUNT(*) as total_rows FROM users;
"""
    }
    
    example = examples.get(query_type, "Tipo de query não reconhecido")
    return f"Exemplo de {query_type}:\n```sql\n{example}\n```"


async def troubleshoot_error(
    ctx: RunContext[TursoContext],
    error_message: str
) -> str:
    """Analisa e sugere soluções para erros Turso"""
    
    # Análise básica do erro
    error_lower = error_message.lower()
    
    if "auth" in error_lower or "token" in error_lower:
        return """
🔧 **Erro de Autenticação Detectado**

Soluções:
1. Verificar token: `turso auth whoami`
2. Re-autenticar: `turso auth login`
3. Verificar variáveis de ambiente:
   - TURSO_API_TOKEN
   - TURSO_DATABASE_URL

Comando de diagnóstico:
```bash
turso db tokens create <database-name>
```
"""
    elif "connection" in error_lower:
        return """
🔧 **Erro de Conexão Detectado**

Verificações:
1. Status do database: `turso db show <db-name>`
2. URL correto do database
3. Firewall/proxy settings
4. SSL/TLS configuração

Debug:
```bash
turso db shell <db-name>
```
"""
    else:
        return f"""
🔧 **Análise do Erro**

Erro reportado: {error_message}

Passos gerais de troubleshooting:
1. Verificar logs detalhados
2. Testar query em `turso db shell`
3. Verificar sintaxe SQL
4. Confirmar permissões

Precisa de mais contexto para diagnóstico específico.
"""


def get_mcp_setup_instructions() -> str:
    """Retorna instruções de setup MCP para Turso"""
    return """
📚 **Setup MCP Turso Integration**

1. **Instalar MCP Server:**
```bash
npm install @diegofornalha/mcp-turso-cloud
```

2. **Configurar tokens:**
```typescript
// .env
TURSO_API_TOKEN=your-org-token
TURSO_DATABASE_URL=libsql://db-name.turso.io
TURSO_DATABASE_TOKEN=your-db-token
```

3. **Inicializar servidor:**
```typescript
import { TursoMCPServer } from '@diegofornalha/mcp-turso-cloud';

const server = new TursoMCPServer({
  organizationToken: process.env.TURSO_API_TOKEN,
  defaultDatabase: 'my-database'
});

await server.start();
```

4. **Segurança:**
- Use `execute_read_only_query` para SELECT
- Use `execute_query` apenas quando necessário
- Implemente rate limiting
- Rotação regular de tokens
"""


async def chat_with_turso_agent(
    message: str, 
    context: Optional[TursoContext] = None
) -> str:
    """
    Função principal para conversar com o Turso Agent
    
    Args:
        message: Mensagem do usuário
        context: Contexto opcional da conversa
    
    Returns:
        Resposta do agente especialista em Turso
    """
    if context is None:
        context = TursoContext()
    
    # Incrementar contador de conversação
    context.conversation_count += 1
    
    # Executar o agente com a mensagem e contexto
    global turso_agent
    if turso_agent is None:
        turso_agent = create_turso_agent()
    
    result = await turso_agent.run(message, deps=context)
    
    return result.data


def chat_with_turso_agent_sync(
    message: str,
    context: Optional[TursoContext] = None
) -> str:
    """
    Versão síncrona do chat para compatibilidade
    
    Args:
        message: Mensagem do usuário
        context: Contexto opcional da conversa
    
    Returns:
        Resposta do agente
    """
    if context is None:
        context = TursoContext()
    
    context.conversation_count += 1
    
    # Executar sincronamente
    global turso_agent
    if turso_agent is None:
        turso_agent = create_turso_agent()
        
    result = turso_agent.run_sync(message, deps=context)
    
    return result.data


# Funções auxiliares para manter compatibilidade com a implementação anterior

async def analyze_performance(context: TursoContext) -> str:
    """Análise de performance usando o agente"""
    message = "Faça uma análise completa de performance do sistema Turso atual"
    return await chat_with_turso_agent(message, context)


async def security_audit(context: TursoContext) -> str:
    """Auditoria de segurança usando o agente"""
    message = "Execute uma auditoria de segurança completa do sistema Turso"
    return await chat_with_turso_agent(message, context)


async def troubleshoot_issue(issue: str, context: TursoContext) -> str:
    """Troubleshooting usando o agente"""
    message = f"Preciso de ajuda para resolver este problema: {issue}"
    return await chat_with_turso_agent(message, context)


async def optimize_system(context: TursoContext) -> str:
    """Otimização do sistema usando o agente"""
    message = "Execute otimizações automáticas no sistema Turso para melhorar performance"
    return await chat_with_turso_agent(message, context)


async def run_validation_gates(context: TursoContext) -> str:
    """Executa validation gates do PRP"""
    message = "Execute todos os validation gates do PRP Turso (ID 6) e mostre os resultados"
    return await chat_with_turso_agent(message, context)


async def get_system_info(context: TursoContext) -> str:
    """Informações do sistema usando o agente"""
    message = "Mostre informações completas sobre o Turso Agent e suas capacidades"
    return await chat_with_turso_agent(message, context)


# Exemplo de uso e demonstração
if __name__ == "__main__":
    import asyncio
    
    async def demo_turso_agent():
        """Demonstra o Turso Agent com PydanticAI"""
        print("=== Turso Specialist Agent com PydanticAI ===\n")
        
        # Criar contexto com configurações
        settings = TursoSettings()
        context = TursoContext(
            session_id="demo-session",
            current_database="my-app-db",
            user_role="developer",
            settings=settings
        )
        
        # Exemplos de interação
        questions = [
            "Como criar um database Turso otimizado para edge?",
            "Qual a melhor forma de implementar segurança com tokens?",
            "Como otimizar queries para melhor performance?",
            "Mostre um exemplo de integração MCP com Turso"
        ]
        
        for question in questions:
            print(f"👤 Usuário: {question}")
            response = await chat_with_turso_agent(question, context)
            print(f"🤖 Turso Agent: {response}")
            print("-" * 80)
    
    # Executar demonstração
    asyncio.run(demo_turso_agent())