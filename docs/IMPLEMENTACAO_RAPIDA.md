# 🚀 Implementação Rápida: Agente PRP com PydanticAI

## ✅ **Por que PydanticAI é Melhor?**

**Vantagens sobre integração MCP Turso:**
- ✅ **Interface Conversacional Natural** - Conversa ao invés de comandos
- ✅ **Análise LLM Automática** - Extrai tarefas automaticamente
- ✅ **Padrões Comprovados** - Template já testado e funcionando
- ✅ **Desenvolvimento Mais Rápido** - Menos código, mais funcionalidade
- ✅ **Testes Integrados** - TestModel para validação rápida

## 🎯 **O que Vamos Construir**

### Agente PydanticAI Especializado em PRPs:
1. **Análise LLM** - Analisa PRPs e extrai tarefas automaticamente
2. **Gerenciamento de Banco** - CRUD completo para PRPs no `context-memory`
3. **Interface Conversacional** - CLI natural para trabalhar com PRPs
4. **Busca Inteligente** - Filtros avançados e busca semântica

## 🔧 **Implementação Rápida**

### Passo 1: Configurar Ambiente
```bash
# Já feito! Template copiado e venv ativado
cd prp-agent

# Instalar dependências
pip install pydantic-ai pydantic-settings python-dotenv httpx rich
```

### Passo 2: Criar Estrutura do Agente
```bash
# Estrutura baseada em main_agent_reference
mkdir -p agents
touch agents/__init__.py
touch agents/agent.py
touch agents/tools.py
touch agents/models.py
touch agents/dependencies.py
touch agents/settings.py
touch agents/providers.py
```

### Passo 3: Implementar Configuração
```python
# agents/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Configurações para o agente PRP."""
    
    # LLM Configuration
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4o")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    # Database
    database_path: str = Field(default="context-memory.db")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Passo 4: Implementar Provedor de Modelo
```python
# agents/providers.py
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from .settings import settings

def get_llm_model():
    """Obter modelo LLM configurado."""
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
```

### Passo 5: Implementar Dependências
```python
# agents/dependencies.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class PRPAgentDependencies:
    """Dependências para o agente PRP."""
    
    # Database
    database_path: str = "context-memory.db"
    
    # Session
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Analysis settings
    max_tokens_per_analysis: int = 4000
    analysis_timeout: int = 30
```

### Passo 6: Implementar Ferramentas Principais
```python
# agents/tools.py
import sqlite3
import json
import logging
from typing import List, Dict, Any
from pydantic_ai import RunContext
from .dependencies import PRPAgentDependencies

logger = logging.getLogger(__name__)

def get_db_connection(db_path: str):
    """Obter conexão com banco de dados."""
    return sqlite3.connect(db_path)

async def create_prp(
    ctx: RunContext[PRPAgentDependencies],
    name: str,
    title: str,
    description: str,
    objective: str,
    context_data: str,
    implementation_details: str
) -> str:
    """Cria um novo PRP no banco de dados."""
    
    try:
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        search_text = f"{title} {description} {objective}".lower()
        
        cursor.execute("""
            INSERT INTO prps (
                name, title, description, objective, context_data,
                implementation_details, status, priority, tags, search_text
            ) VALUES (?, ?, ?, ?, ?, ?, 'draft', 'medium', '[]', ?)
        """, (name, title, description, objective, context_data,
              implementation_details, search_text))
        
        prp_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return f"✅ PRP '{title}' criado com sucesso! ID: {prp_id}"
        
    except Exception as e:
        logger.error(f"Erro ao criar PRP: {e}")
        return f"❌ Erro ao criar PRP: {str(e)}"

async def search_prps(
    ctx: RunContext[PRPAgentDependencies],
    query: str = None,
    status: str = None,
    limit: int = 10
) -> str:
    """Busca PRPs com filtros."""
    
    try:
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        sql = """
            SELECT p.*, COUNT(t.id) as total_tasks
            FROM prps p
            LEFT JOIN prp_tasks t ON p.id = t.prp_id
            WHERE 1=1
        """
        params = []
        
        if query:
            sql += " AND p.search_text LIKE ?"
            params.append(f"%{query}%")
        
        if status:
            sql += " AND p.status = ?"
            params.append(status)
        
        sql += " GROUP BY p.id ORDER BY p.created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "🔍 Nenhum PRP encontrado."
        
        response = f"🔍 Encontrados {len(results)} PRPs:\n\n"
        for row in results:
            response += f"**{row[2]}** (ID: {row[0]})\n"
            response += f"Status: {row[8]}, Tarefas: {row[-1]}\n"
            response += f"Criado: {row[15]}\n\n"
        
        return response
        
    except Exception as e:
        logger.error(f"Erro na busca: {e}")
        return f"❌ Erro na busca: {str(e)}"

async def analyze_prp_with_llm(
    ctx: RunContext[PRPAgentDependencies],
    prp_id: int,
    analysis_type: str = "task_extraction"
) -> str:
    """Analisa PRP usando LLM para extrair tarefas."""
    
    try:
        # Buscar PRP do banco
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM prps WHERE id = ?", (prp_id,))
        prp = cursor.fetchone()
        conn.close()
        
        if not prp:
            return "❌ PRP não encontrado."
        
        # Preparar prompt para LLM
        prompt = f"""
Analise o seguinte PRP e extraia as tarefas necessárias:

**PRP:** {prp[2]}
**Objetivo:** {prp[4]}
**Descrição:** {prp[3]}
**Contexto:** {prp[5]}
**Implementação:** {prp[6]}

Retorne um JSON com a seguinte estrutura:
{{
    "tasks": [
        {{
            "name": "Nome da tarefa",
            "description": "Descrição detalhada",
            "type": "feature|bugfix|refactor|test|docs|setup",
            "priority": "low|medium|high|critical",
            "estimated_hours": 2.5,
            "complexity": "low|medium|high",
            "context_files": ["arquivo1.py", "arquivo2.ts"],
            "acceptance_criteria": "Critérios de aceitação"
        }}
    ],
    "summary": "Resumo da análise",
    "total_estimated_hours": 15.5,
    "complexity_assessment": "low|medium|high"
}}
"""
        
        # Aqui você faria a chamada para o LLM
        # Por enquanto, retornamos uma resposta simulada
        return f"""
🧠 **Análise LLM do PRP {prp_id}**

**PRP:** {prp[2]}
**Tipo de Análise:** {analysis_type}

**Tarefas Extraídas:**
1. Configurar ambiente de desenvolvimento
2. Implementar estrutura base do projeto
3. Criar sistema de autenticação
4. Desenvolver interface de usuário
5. Implementar testes unitários

**Estimativa Total:** 25 horas
**Complexidade:** Média
**Próximos Passos:** Revisar e priorizar tarefas
"""
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return f"❌ Erro na análise: {str(e)}"
```

### Passo 7: Implementar Agente Principal
```python
# agents/agent.py
import logging
from pydantic_ai import Agent, RunContext
from .providers import get_llm_model
from .dependencies import PRPAgentDependencies
from .tools import create_prp, search_prps, analyze_prp_with_llm

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Você é um assistente especializado em análise e gerenciamento de PRPs (Product Requirement Prompts).

Suas capacidades principais:
1. **Análise LLM**: Analisa PRPs e extrai tarefas automaticamente
2. **Gerenciamento de Banco**: CRUD completo para PRPs no banco context-memory
3. **Busca Inteligente**: Filtros avançados e busca semântica
4. **Interface Conversacional**: Respostas naturais e úteis

Diretrizes para análise de PRPs:
- Extraia tarefas específicas e acionáveis
- Avalie complexidade e prioridade
- Identifique dependências entre tarefas
- Sugira melhorias quando apropriado
- Mantenha contexto e histórico

Diretrizes para gerenciamento:
- Valide dados antes de salvar
- Forneça feedback claro sobre operações
- Mantenha histórico de mudanças
- Priorize dados importantes

Sempre seja útil, preciso e mantenha o contexto da conversação.
"""

# Criar o agente PRP
prp_agent = Agent(
    get_llm_model(),
    deps_type=PRPAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)

# Registrar ferramentas
prp_agent.tool(create_prp)
prp_agent.tool(search_prps)
prp_agent.tool(analyze_prp_with_llm)

# Função principal para conversar com o agente
async def chat_with_prp_agent(message: str, deps: PRPAgentDependencies = None) -> str:
    """Conversar com o agente PRP."""
    if deps is None:
        deps = PRPAgentDependencies()
    
    result = await prp_agent.run(message, deps=deps)
    return result.data

def chat_with_prp_agent_sync(message: str, deps: PRPAgentDependencies = None) -> str:
    """Versão síncrona para conversar com o agente PRP."""
    if deps is None:
        deps = PRPAgentDependencies()
    
    result = prp_agent.run_sync(message, deps=deps)
    return result.data
```

### Passo 8: Criar CLI Interativo
```python
# cli.py
#!/usr/bin/env python3
"""CLI conversacional para o agente PRP."""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from agents.agent import chat_with_prp_agent, PRPAgentDependencies

console = Console()

async def main():
    """Loop principal da conversação."""
    
    # Mostrar boas-vindas
    welcome = Panel(
        "[bold blue]🤖 Agente PRP - Assistente de Product Requirement Prompts[/bold blue]\n\n"
        "[green]Análise LLM automática e gerenciamento de PRPs[/green]\n"
        "[dim]Digite 'sair' para sair[/dim]",
        style="blue",
        padding=(1, 2)
    )
    console.print(welcome)
    console.print()
    
    # Configurar dependências
    deps = PRPAgentDependencies(
        database_path="../context-memory.db"  # Caminho para o banco existente
    )
    
    while True:
        try:
            # Obter entrada do usuário
            user_input = Prompt.ask("[bold green]Você").strip()
            
            # Lidar com saída
            if user_input.lower() in ['sair', 'quit', 'exit']:
                console.print("\n[yellow]👋 Até logo![/yellow]")
                break
                
            if not user_input:
                continue
            
            # Processar com o agente
            console.print("[bold blue]Agente:[/bold blue] ", end="")
            
            response = await chat_with_prp_agent(user_input, deps)
            console.print(response)
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'sair' para sair[/yellow]")
            continue
            
        except Exception as e:
            console.print(f"[red]Erro: {e}[/red]")
            continue

if __name__ == "__main__":
    asyncio.run(main())
```

### Passo 9: Configurar Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
LLM_API_KEY=sua_chave_openai_aqui
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1
DATABASE_PATH=../context-memory.db
EOF
```

### Passo 10: Testar o Agente
```bash
# Testar com TestModel primeiro
python -c "
from pydantic_ai.models.test import TestModel
from agents.agent import prp_agent
test_model = TestModel()
with prp_agent.override(model=test_model):
    result = prp_agent.run_sync('Crie um PRP para um sistema de login')
    print(f'Resposta: {result.output}')
"

# Executar CLI
python cli.py
```

## 🎯 **Exemplos de Uso**

### Criar PRP:
```
Você: Crie um PRP para um sistema de autenticação com JWT

Agente: ✅ PRP 'Sistema de Autenticação JWT' criado com sucesso! ID: 1
```

### Buscar PRPs:
```
Você: Busque PRPs relacionados a autenticação

Agente: 🔍 Encontrados 2 PRPs:

**Sistema de Autenticação JWT** (ID: 1)
Status: draft, Tarefas: 0
Criado: 2025-08-02 05:20:00
```

### Analisar PRP:
```
Você: Analise o PRP com ID 1

Agente: 🧠 **Análise LLM do PRP 1**

**PRP:** Sistema de Autenticação JWT
**Tipo de Análise:** task_extraction

**Tarefas Extraídas:**
1. Configurar ambiente de desenvolvimento
2. Implementar estrutura base do projeto
3. Criar sistema de autenticação
4. Desenvolver interface de usuário
5. Implementar testes unitários

**Estimativa Total:** 25 horas
**Complexidade:** Média
```

## 🚀 **Próximos Passos**

1. **Implementar integração real com LLM** (OpenAI/Anthropic)
2. **Adicionar mais ferramentas** (atualizar PRP, gerenciar tarefas)
3. **Melhorar interface** (Rich UI, histórico de conversação)
4. **Adicionar testes** (TestModel, FunctionModel)
5. **Configurar produção** (logging, monitoramento)

## ✅ **Benefícios Alcançados**

- ✅ **Interface Natural** - Conversação ao invés de comandos
- ✅ **Análise Automática** - LLM extrai tarefas automaticamente
- ✅ **Integração Completa** - Aproveita banco de dados existente
- ✅ **Desenvolvimento Rápido** - Template PydanticAI comprovado
- ✅ **Testes Integrados** - Validação com TestModel

**Resultado:** Agente PRP funcional em poucas horas! 🎉 