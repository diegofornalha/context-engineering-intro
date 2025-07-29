# PydanticAI Context Engineering - Regras Globais para Desenvolvimento de Agentes de IA

Este arquivo contém as regras e princípios globais que se aplicam a TODO o trabalho de desenvolvimento de agentes PydanticAI. Estas regras são especializadas para construir agentes de IA de nível de produção com ferramentas, memória e saídas estruturadas.

## 🔄 Princípios Fundamentais do PydanticAI

**IMPORTANTE: Estes princípios se aplicam a TODO desenvolvimento de agentes PydanticAI:**

### Fluxo de Trabalho de Desenvolvimento de Agentes
- **Sempre comece com INITIAL.md** - Defina requisitos do agente antes de gerar PRPs
- **Use o padrão PRP**: INITIAL.md → `/generate-pydantic-ai-prp INITIAL.md` → `/execute-pydantic-ai-prp PRPs/filename.md`
- **Siga loops de validação** - Cada PRP deve incluir teste de agente com TestModel/FunctionModel
- **Contexto é Rei** - Inclua TODOS os padrões, exemplos e documentação PydanticAI necessários

### Metodologia de Pesquisa para Agentes de IA
- **Pesquise extensivamente na web** - Sempre pesquise padrões e melhores práticas PydanticAI
- **Estude documentação oficial** - ai.pydantic.dev é a fonte autoritativa
- **Extração de padrões** - Identifique arquiteturas de agentes reutilizáveis e padrões de ferramentas
- **Documentação de armadilhas** - Documente padrões assíncronos, limites de modelo e problemas de gerenciamento de contexto

## 📚 Consciência do Projeto & Contexto

- **Use um ambiente virtual** para executar todo código e testes. Se não houver um no codebase quando necessário, crie um
- **Use convenções de nomenclatura PydanticAI consistentes** e padrões de estrutura de agentes
- **Siga padrões estabelecidos de organização de diretório de agentes** (agent.py, tools.py, models.py)
- **Aproveite exemplos PydanticAI extensivamente** - Estude padrões existentes antes de criar novos agentes

## 🧱 Estrutura de Agente & Modularidade

- **Nunca crie arquivos com mais de 500 linhas** - Divida em módulos quando se aproximar do limite
- **Organize código de agente em módulos claramente separados** agrupados por responsabilidade:
  - `agent.py` - Definição principal do agente e lógica de execução
  - `tools.py` - Funções de ferramentas usadas pelo agente
  - `models.py` - Modelos de saída Pydantic e classes de dependência
  - `dependencies.py` - Dependências de contexto e integrações de serviços externos
- **Use imports claros e consistentes** - Importe do pacote pydantic_ai apropriadamente
- **Use python-dotenv e load_dotenv()** para variáveis de ambiente - Siga o padrão examples/main_agent_reference/settings.py
- **Nunca codifique informações sensíveis** - Sempre use arquivos .env para chaves de API e configuração

## 🤖 Padrões de Desenvolvimento PydanticAI

### Padrões de Criação de Agentes
- **Use design agnóstico de modelo** - Suporte múltiplos provedores (OpenAI, Anthropic, Gemini)
- **Implemente injeção de dependência** - Use deps_type para serviços externos e contexto
- **Defina saídas estruturadas** - Use modelos Pydantic para validação de resultados
- **Inclua prompts de sistema abrangentes** - Tanto instruções estáticas quanto dinâmicas

### Padrões de Integração de Ferramentas
- **Use decorador @agent.tool** para ferramentas com consciência de contexto com RunContext[DepsType]
- **Use decorador @agent.tool_plain** para ferramentas simples sem dependências de contexto
- **Implemente validação adequada de parâmetros** - Use modelos Pydantic para parâmetros de ferramentas
- **Lide com erros de ferramentas graciosamente** - Implemente mecanismos de retry e recuperação de erro

### Configuração de Variáveis de Ambiente com python-dotenv
```python
# Use python-dotenv e pydantic-settings para gerenciamento adequado de configuração
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

class Settings(BaseSettings):
    """Configurações da aplicação com suporte a variáveis de ambiente."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Configuração LLM
    llm_provider: str = Field(default="openai", description="Provedor LLM")
    llm_api_key: str = Field(..., description="Chave de API para o provedor LLM")
    llm_model: str = Field(default="gpt-4", description="Nome do modelo a usar")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1", 
        description="URL base para a API LLM"
    )

def load_settings() -> Settings:
    """Carrega configurações com tratamento adequado de erro e carregamento de ambiente."""
    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()
    
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Falha ao carregar configurações: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nCertifique-se de definir LLM_API_KEY no seu arquivo .env"
        raise ValueError(error_msg) from e

def get_llm_model():
    """Obtém modelo LLM configurado com carregamento adequado de ambiente."""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url, 
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
```

### Padrões de Teste para Agentes de IA
- **Use TestModel para desenvolvimento** - Validação rápida sem chamadas de API
- **Use FunctionModel para comportamento customizado** - Controle respostas do agente em testes
- **Use Agent.override() para teste** - Substitua modelos em contextos de teste
- **Teste padrões síncronos e assíncronos** - Garanta compatibilidade com diferentes modos de execução
- **Teste validação de ferramentas** - Verifique schemas de parâmetros de ferramentas e tratamento de erros

## ✅ Gerenciamento de Tarefas para Desenvolvimento de IA

- **Divida desenvolvimento de agente em etapas claras** com critérios específicos de conclusão
- **Marque tarefas como completas imediatamente** após finalizar implementações de agentes
- **Atualize status da tarefa em tempo real** conforme o desenvolvimento do agente progride
- **Teste comportamento do agente** antes de marcar tarefas de implementação como completas

## 📎 Padrões de Codificação PydanticAI

### Arquitetura de Agente
```python
# Siga padrões main_agent_reference - sem result_type a menos que saída estruturada seja necessária
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from .settings import load_settings

@dataclass
class AgentDependencies:
    """Dependências para execução do agente"""
    api_key: str
    session_id: str = None

# Carrega configurações com tratamento adequado de dotenv
settings = load_settings()

# Agente simples com saída de string (padrão)
agent = Agent(
    get_llm_model(),  # Usa load_settings() internamente
    deps_type=AgentDependencies,
    system_prompt="Você é um assistente útil..."
)

@agent.tool
async def example_tool(
    ctx: RunContext[AgentDependencies], 
    query: str
) -> str:
    """Ferramenta com acesso adequado ao contexto"""
    return await external_api_call(ctx.deps.api_key, query)
```

### Melhores Práticas de Segurança
- **Gerenciamento de chave de API** - Use python-dotenv com arquivos .env, nunca comite chaves no controle de versão
- **Carregamento de variáveis de ambiente** - Sempre use load_dotenv() seguindo examples/main_agent_reference/settings.py
- **Validação de entrada** - Use modelos Pydantic para todos os parâmetros de ferramentas
- **Limitação de taxa** - Implemente throttling adequado de requisições para APIs externas
- **Prevenção de injeção de prompt** - Valide e sanitize entradas do usuário
- **Tratamento de erro** - Nunca exponha informações sensíveis em mensagens de erro

### Armadilhas Comuns do PydanticAI
- **Problemas de mistura async/sync** - Seja consistente com padrões async/await em todo o código
- **Limites de token do modelo** - Diferentes modelos têm diferentes limites de contexto, planeje adequadamente
- **Complexidade de injeção de dependência** - Mantenha grafos de dependência simples e bem tipados
- **Falhas no tratamento de erro de ferramentas** - Sempre implemente mecanismos adequados de retry e fallback
- **Gerenciamento de estado de contexto** - Projete ferramentas stateless quando possível para confiabilidade

## 🔍 Padrões de Pesquisa para Agentes de IA

- **Use servidor Archon MCP** - Aproveite documentação PydanticAI disponível via RAG
- **Estude exemplos oficiais** - ai.pydantic.dev/examples tem implementações funcionais
- **Pesquise capacidades de modelo** - Entenda recursos e limitações específicos do provedor
- **Documente padrões de integração** - Inclua exemplos de integração de serviços externos

## 🎯 Padrões de Implementação para Agentes de IA

- **Siga o fluxo de trabalho PRP religiosamente** - Não pule etapas de validação de agente
- **Sempre teste com TestModel primeiro** - Valide lógica do agente antes de usar modelos reais
- **Use padrões de agente existentes** em vez de criar do zero
- **Inclua tratamento abrangente de erro** para falhas de ferramentas e erros de modelo
- **Teste padrões de streaming** ao implementar interações de agente em tempo real

## 🚫 Anti-Padrões para Sempre Evitar

- ❌ Não pule teste de agente - Sempre use TestModel/FunctionModel para validação
- ❌ Não codifique strings de modelo - Use configuração baseada em ambiente como main_agent_reference
- ❌ Não use result_type a menos que saída estruturada seja especificamente necessária - padrão para string
- ❌ Não ignore padrões assíncronos - PydanticAI tem considerações específicas async/sync
- ❌ Não crie grafos de dependência complexos - Mantenha dependências simples e testáveis
- ❌ Não esqueça tratamento de erro de ferramentas - Implemente retry adequado e degradação graciosa
- ❌ Não pule validação de entrada - Use modelos Pydantic para todas as entradas externas

## 🔧 Padrões de Uso de Ferramentas para Desenvolvimento de IA

- **Use pesquisa web extensivamente** para pesquisa e documentação PydanticAI
- **Siga padrões de comando PydanticAI** para comandos slash e fluxos de trabalho de agentes
- **Use loops de validação de agente** para garantir qualidade em cada etapa de desenvolvimento
- **Teste com múltiplos provedores de modelo** para garantir compatibilidade do agente

## 🧪 Teste & Confiabilidade para Agentes de IA

- **Sempre crie testes abrangentes de agente** para ferramentas, saídas e tratamento de erro
- **Teste comportamento do agente com TestModel** antes de usar provedores de modelo reais
- **Inclua teste de casos extremos** para falhas de ferramentas e problemas de provedor de modelo
- **Teste saídas estruturadas e não estruturadas** para garantir flexibilidade do agente
- **Valide injeção de dependência** funciona corretamente em ambientes de teste

Estas regras globais se aplicam especificamente ao desenvolvimento de agentes PydanticAI e garantem aplicações de IA prontas para produção com tratamento adequado de erro, teste e práticas de segurança.