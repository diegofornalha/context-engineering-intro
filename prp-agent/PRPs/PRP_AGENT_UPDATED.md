---
name: "Agente PydanticAI para Análise e Gerenciamento de PRPs - Arquitetura Flexível"
description: "Agente inteligente com arquitetura flexível para analisar Product Requirement Prompts, extrair tarefas com LLM e gerenciar banco de dados de PRPs"
---

## Propósito

Construir um agente PydanticAI especializado em **análise e gerenciamento de PRPs** (Product Requirement Prompts) com **arquitetura flexível** que utiliza LLM para extrair tarefas automaticamente e fornece interface conversacional natural para gerenciar o banco de dados `context-memory`.

## 🎯 Arquitetura Flexível - Padrões Descobertos

### ✅ Core Obrigatório
- **PRP Agent**: Sempre presente - Metodologia principal
- **Turso**: Opcional - Sistema de memória (quando necessário)
- **Sentry**: Opcional - Sistema de monitoramento (quando necessário)

### 🔄 Componentes Opcionais
- **CrewAI**: Opcional - Framework de orquestração
- **A2A**: Opcional - Interoperabilidade entre agentes

### 📋 PRP - Metodologia (Sempre presente)
- Análise de requisitos
- Engenharia de contexto
- Prompts estruturados

## Princípios Fundamentais

1. **Análise LLM Inteligente**: Usar LLM para analisar PRPs e extrair tarefas estruturadas
2. **Gerenciamento de Banco de Dados**: CRUD completo para PRPs no banco `context-memory`
3. **Interface Conversacional**: CLI natural para interagir com PRPs
4. **Busca e Filtros Avançados**: Capacidades de busca inteligente
5. **Integração com Sistema Existente**: Aproveitar banco de dados já configurado
6. **Arquitetura Flexível**: Componentes modulares e opcionais

## ⚠️ Diretrizes de Implementação: Mantenha Foco

**IMPORTANTE**: Mantenha o agente focado e prático. Não construa complexidade desnecessária.

### O que NÃO fazer:
- ❌ **Não criar dezenas de ferramentas** - Apenas as essenciais para PRPs
- ❌ **Não complicar dependências** - Mantenha injeção de dependência simples
- ❌ **Não adicionar abstrações desnecessárias** - Siga padrões main_agent_reference
- ❌ **Não construir workflows complexos** a menos que especificamente necessário
- ❌ **Não adicionar saída estruturada** a menos que validação seja necessária
- ❌ **Não forçar componentes opcionais** - Turso e Sentry são opcionais

### O que FAZER:
- ✅ **Comece simples** - Agente mínimo viável que atenda aos requisitos
- ✅ **Adicione ferramentas incrementalmente** - Implemente apenas o que o agente precisa
- ✅ **Siga main_agent_reference** - Use padrões comprovados, não reinvente
- ✅ **Use saída string por padrão** - Apenas adicione result_type quando validação for necessária
- ✅ **Teste cedo e frequentemente** - Use TestModel para validar conforme constrói
- ✅ **Implemente arquitetura flexível** - Componentes opcionais configuráveis

### Pergunta Chave:
**"Este agente realmente precisa desta funcionalidade para cumprir seu propósito principal?"**

Se a resposta for não, não construa. Mantenha simples, focado e funcional.

---

## Objetivo

Construir um agente PydanticAI especializado com **arquitetura flexível** que:

1. **Analisa PRPs com LLM**: Extrai tarefas, avalia complexidade e gera insights
2. **Gerencia Banco de Dados**: CRUD completo para PRPs no banco `context-memory`
3. **Fornece Interface Conversacional**: CLI natural para trabalhar com PRPs
4. **Realiza Busca Inteligente**: Filtros avançados e busca semântica
5. **Integra com Sistema Existente**: Aproveita infraestrutura já configurada
6. **Suporta Componentes Opcionais**: Turso (memória) e Sentry (monitoramento)

## Por que

- **Automação Inteligente**: LLM analisa PRPs e extrai tarefas automaticamente
- **Interface Natural**: Conversação natural ao invés de comandos complexos
- **Reutilização de Infraestrutura**: Aproveita banco de dados já configurado
- **Produtividade**: Acelera processo de análise e gerenciamento de PRPs
- **Consistência**: Padrões uniformes para todos os PRPs
- **Flexibilidade**: Componentes opcionais conforme necessidade

## O que

### Classificação do Tipo de Agente
- [x] **Agente com Ferramentas**: Agente com capacidades de integração de ferramentas externas
- [x] **Agente de Workflow**: Processamento multi-etapas e orquestração
- [ ] **Agente de Saída Estruturada**: Validação complexa de dados e formatação

### Requisitos do Provedor de Modelo
- [x] **OpenAI**: `openai:gpt-4o` ou `openai:gpt-4o-mini`
- [x] **Anthropic**: `anthropic:claude-3-5-sonnet-20241022`
- [x] **Estratégia de Fallback**: Suporte múltiplo de provedores com failover automático

### Integrações Externas
- [x] **Conexões de Banco de Dados**: SQLite (context-memory.db)
- [x] **Integrações de API REST**: LLM APIs (OpenAI, Anthropic)
- [x] **Operações de Sistema de Arquivos**: Leitura/escrita de arquivos PRP
- [x] **Fontes de Dados em Tempo Real**: Banco de dados SQLite
- [x] **Turso (Opcional)**: Sistema de memória via MCP
- [x] **Sentry (Opcional)**: Sistema de monitoramento via MCP

### Critérios de Sucesso
- [ ] Agente analisa PRPs com LLM e extrai tarefas automaticamente
- [ ] Todas as ferramentas funcionam corretamente com tratamento adequado de erros
- [ ] Interface conversacional natural e intuitiva
- [ ] Cobertura abrangente de testes com TestModel e FunctionModel
- [ ] Medidas de segurança implementadas (chaves de API, validação de entrada)
- [ ] Performance atende aos requisitos (tempo de resposta, throughput)
- [ ] Arquitetura flexível implementada (componentes opcionais)
- [ ] Integração opcional com Turso e Sentry funcionando

## Todo o Contexto Necessário

### Documentação PydanticAI & Pesquisa

```yaml
# Servidores MCP
- mcp: Archon
  query: "PydanticAI agent creation model providers tools dependencies"
  why: Entendimento do framework e padrões mais recentes

# DOCUMENTAÇÃO PYDANTIC AI ESSENCIAL - Deve ser pesquisada
- url: https://ai.pydantic.dev/
  why: Documentação oficial PydanticAI com guia de início
  content: Criação de agentes, provedores de modelo, padrões de injeção de dependência

- url: https://ai.pydantic.dev/agents/
  why: Padrões abrangentes de arquitetura e configuração de agentes
  content: Prompts do sistema, tipos de saída, métodos de execução, composição de agentes

- url: https://ai.pydantic.dev/tools/
  why: Padrões de integração de ferramentas e registro de funções
  content: Decoradores @agent.tool, uso de RunContext, validação de parâmetros

- url: https://ai.pydantic.dev/testing/
  why: Estratégias de teste específicas para agentes PydanticAI
  content: TestModel, FunctionModel, Agent.override(), padrões pytest

- url: https://ai.pydantic.dev/models/
  why: Configuração de provedor de modelo e autenticação
  content: Setup OpenAI, Anthropic, Gemini, gerenciamento de chave de API, modelos de fallback

# Exemplos pré-construídos
- path: examples/
  why: Implementações de referência para agentes Pydantic AI
  content: Vários exemplos Pydantic AI já construídos para referência incluindo como configurar modelos e provedores

- path: examples/cli.py
  why: Mostra interação real com agentes Pydantic AI
  content: CLI conversacional com streaming, visibilidade de chamadas de ferramentas e manipulação de conversação - demonstra como usuários realmente interagem com agentes
```

### Pesquisa de Arquitetura de Agente

```yaml
# Padrões de Arquitetura PydanticAI (seguir main_agent_reference)
agent_structure:
  configuration:
    - settings.py: Configuração baseada em ambiente com pydantic-settings
    - providers.py: Abstração de provedor de modelo com get_llm_model()
    - Variáveis de ambiente para chaves de API e seleção de modelo
    - Nunca codificar strings de modelo como "openai:gpt-4o"
  
  agent_definition:
    - Padrão para saída string (sem result_type a menos que saída estruturada seja necessária)
    - Usar get_llm_model() de providers.py para configuração de modelo
    - Prompts do sistema como constantes string ou funções
    - Dependências dataclass para serviços externos
  
  tool_integration:
    - @agent.tool para ferramentas com consciência de contexto com RunContext[DepsType]
    - Funções de ferramenta como funções puras que podem ser chamadas independentemente
    - Tratamento adequado de erros e logging em implementações de ferramentas
    - Injeção de dependência através de RunContext.deps
  
  testing_strategy:
    - TestModel para validação rápida de desenvolvimento
    - FunctionModel para teste de comportamento customizado
    - Agent.override() para isolamento de teste
    - Teste abrangente de ferramentas com mocks

# ARQUITETURA FLEXÍVEL - NOVA DESCOBERTA
flexible_architecture:
  core_components:
    - PRP Agent: Sempre presente - Metodologia principal
    - Turso: Opcional - Sistema de memória
    - Sentry: Opcional - Sistema de monitoramento
  
  optional_components:
    - CrewAI: Opcional - Framework de orquestração
    - A2A: Opcional - Interoperabilidade entre agentes
  
  configuration_patterns:
    - Componentes opcionais configuráveis via variáveis de ambiente
    - Detecção automática de disponibilidade de componentes
    - Fallback gracioso quando componentes opcionais não estão disponíveis
    - Logging adequado para componentes ativos/inativos
```

### Considerações de Segurança e Produção

```yaml
# Padrões de Segurança PydanticAI (pesquisa necessária)
security_requirements:
  api_management:
    environment_variables: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    secure_storage: "Nunca commitar chaves de API no controle de versão"
    rotation_strategy: "Planejar rotação e gerenciamento de chaves"
  
  input_validation:
    sanitization: "Validar todas as entradas do usuário com modelos Pydantic"
    prompt_injection: "Implementar estratégias de prevenção de injeção de prompt"
    rate_limiting: "Prevenir abuso com throttling adequado"
  
  output_security:
    data_filtering: "Garantir que nenhum dado sensível nas respostas do agente"
    content_validation: "Validar estrutura e conteúdo da saída"
    logging_safety: "Logging seguro sem expor segredos"

# ARQUITETURA FLEXÍVEL - SEGURANÇA
flexible_security:
  component_isolation:
    - Componentes opcionais não devem comprometer segurança do core
    - Validação independente para cada componente
    - Logging separado para componentes opcionais
  
  configuration_security:
    - Variáveis de ambiente para ativação de componentes
    - Validação de configuração de componentes opcionais
    - Fallback seguro quando componentes falham
```

### Armadilhas Comuns PydanticAI (pesquisar e documentar)

```yaml
# Armadilhas específicas do agente para pesquisar e abordar
implementation_gotchas:
  async_patterns:
    issue: "Misturar chamadas sync e async de agente inconsistentemente"
    research: "Melhores práticas async/await PydanticAI"
    solution: "[A ser documentado baseado na pesquisa]"
  
  model_limits:
    issue: "Diferentes modelos têm capacidades e limites de token diferentes"
    research: "Comparação de provedores de modelo e capacidades"
    solution: "[A ser documentado baseado na pesquisa]"
  
  dependency_complexity:
    issue: "Grafos de dependência complexos podem ser difíceis de debugar"
    research: "Melhores práticas de injeção de dependência em PydanticAI"
    solution: "[A ser documentado baseado na pesquisa]"
  
  tool_error_handling:
    issue: "Falhas de ferramentas podem quebrar execuções inteiras do agente"
    research: "Padrões de tratamento de erro e retry para ferramentas"
    solution: "[A ser documentado baseado na pesquisa]"

# ARQUITETURA FLEXÍVEL - ARMADILHAS
flexible_gotchas:
  component_dependencies:
    issue: "Componentes opcionais podem criar dependências não esperadas"
    research: "Padrões de desacoplamento para componentes opcionais"
    solution: "[A ser documentado baseado na pesquisa]"
  
  configuration_complexity:
    issue: "Múltiplas configurações podem tornar o sistema complexo"
    research: "Padrões de configuração simplificada para componentes opcionais"
    solution: "[A ser documentado baseado na pesquisa]"
  
  testing_flexibility:
    issue: "Testar todas as combinações de componentes pode ser desafiador"
    research: "Estratégias de teste para arquitetura flexível"
    solution: "[A ser documentado baseado na pesquisa]"
```

## Plano de Implementação

### Fase de Pesquisa de Tecnologia

**PESQUISA NECESSÁRIA - Complete antes da implementação:**

✅ **Deep Dive do Framework PydanticAI:**
- [ ] Padrões de criação de agentes e melhores práticas
- [ ] Configuração de provedor de modelo e estratégias de fallback
- [ ] Padrões de integração de ferramentas (@agent.tool vs @agent.tool_plain)
- [ ] Sistema de injeção de dependência e type safety
- [ ] Estratégias de teste com TestModel e FunctionModel

✅ **Investigação de Arquitetura de Agente:**
- [ ] Convenções de estrutura de projeto (agent.py, tools.py, models.py, dependencies.py)
- [ ] Design de prompt do sistema (estático vs dinâmico)
- [ ] Validação de saída estruturada com modelos Pydantic
- [ ] Padrões async/sync e suporte a streaming
- [ ] Mecanismos de tratamento de erro e retry

✅ **Padrões de Segurança e Produção:**
- [ ] Gerenciamento de chave de API e configuração segura
- [ ] Validação de entrada e prevenção de injeção de prompt
- [ ] Estratégias de rate limiting e monitoramento
- [ ] Logging e observabilidade padrões
- [ ] Considerações de implantação e escalabilidade

✅ **Arquitetura Flexível - NOVA PESQUISA:**
- [ ] Padrões de componentes opcionais em PydanticAI
- [ ] Configuração dinâmica de componentes
- [ ] Integração MCP para Turso e Sentry
- [ ] Estratégias de fallback para componentes opcionais
- [ ] Testes para arquitetura flexível

### Plano de Implementação do Agente

```yaml
Tarefa de Implementação 1 - Configuração da Arquitetura do Agente (Seguir main_agent_reference):
  CRIAR estrutura do projeto do agente:
    - settings.py: Configuração baseada em ambiente com pydantic-settings
    - providers.py: Abstração de provedor de modelo com get_llm_model()
    - agent.py: Definição principal do agente (saída string padrão)
    - tools.py: Funções de ferramentas com decoradores adequados
    - dependencies.py: Integrações de serviços externos (dataclasses)
    - tests/: Suite de testes abrangente
    - components/: Componentes opcionais (Turso, Sentry)

Tarefa de Implementação 2 - Desenvolvimento do Agente Principal:
  IMPLEMENTAR agent.py seguindo padrões main_agent_reference:
    - Usar get_llm_model() de providers.py para configuração de modelo
    - Prompt do sistema como constante string ou função
    - Injeção de dependência com dataclass
    - SEM result_type a menos que saída estruturada seja especificamente necessária
    - Tratamento de erro e logging

Tarefa de Implementação 3 - Integração de Ferramentas:
  DESENVOLVER tools.py:
    - Funções de ferramentas com decoradores @agent.tool
    - Integração RunContext[DepsType] para acesso a dependências
    - Validação de parâmetros com type hints adequados
    - Mecanismos de tratamento de erro e retry
    - Documentação de ferramentas e geração de schema

Tarefa de Implementação 4 - Modelos de Dados e Dependências:
  CRIAR models.py e dependencies.py:
    - Modelos Pydantic para saídas estruturadas
    - Classes de dependência para serviços externos
    - Modelos de validação de entrada para ferramentas
    - Validadores customizados e constraints

Tarefa de Implementação 5 - Componentes Opcionais (NOVA):
  IMPLEMENTAR arquitetura flexível:
    - Componente Turso (memória) - opcional
    - Componente Sentry (monitoramento) - opcional
    - Configuração via variáveis de ambiente
    - Detecção automática de disponibilidade
    - Fallback gracioso quando não disponível

Tarefa de Implementação 6 - Testes Abrangentes:
  IMPLEMENTAR suite de testes:
    - TestModel para validação rápida de desenvolvimento
    - FunctionModel para comportamento customizado
    - Agent.override() para isolamento
    - Testes de integração com provedores reais
    - Validação de ferramentas e teste de cenários de erro
    - Testes para componentes opcionais

Tarefa de Implementação 7 - Segurança e Configuração:
  CONFIGURAR padrões de segurança:
    - Gerenciamento de variáveis de ambiente para chaves de API
    - Sanitização e validação de entrada
    - Implementação de rate limiting
    - Logging seguro e monitoramento
    - Configuração de implantação de produção
    - Segurança para componentes opcionais
```

## Ferramentas Específicas do Agente PRP

### 1. **Ferramentas de Análise LLM**

```python
@agent.tool
async def analyze_prp_with_llm(
    ctx: RunContext[AgentDependencies],
    prp_content: str,
    analysis_type: str = "task_extraction"
) -> str:
    """
    Analisa um PRP usando LLM para extrair tarefas e insights.
    
    Args:
        prp_content: Conteúdo do PRP para análise
        analysis_type: Tipo de análise (task_extraction, complexity_assessment, etc.)
    
    Returns:
        Análise estruturada do PRP
    """
    # Implementação com chamada para LLM
    pass

@agent.tool
async def extract_tasks_from_prp(
    ctx: RunContext[AgentDependencies],
    prp_id: int
) -> str:
    """
    Extrai tarefas de um PRP existente no banco de dados.
    
    Args:
        prp_id: ID do PRP no banco de dados
    
    Returns:
        Lista de tarefas extraídas
    """
    # Buscar PRP do banco e analisar com LLM
    pass
```

### 2. **Ferramentas de Gerenciamento de Banco de Dados**

```python
@agent.tool
async def create_prp(
    ctx: RunContext[AgentDependencies],
    name: str,
    title: str,
    description: str,
    objective: str,
    context_data: str,
    implementation_details: str
) -> str:
    """
    Cria um novo PRP no banco de dados.
    
    Args:
        name: Nome único do PRP
        title: Título descritivo
        description: Descrição geral
        objective: Objetivo principal
        context_data: JSON com contexto
        implementation_details: JSON com detalhes de implementação
    
    Returns:
        Confirmação de criação com ID
    """
    # Inserir no banco context-memory
    pass

@agent.tool
async def search_prps(
    ctx: RunContext[AgentDependencies],
    query: str = None,
    status: str = None,
    priority: str = None,
    limit: int = 10
) -> str:
    """
    Busca PRPs com filtros avançados.
    
    Args:
        query: Termo de busca
        status: Filtro por status
        priority: Filtro por prioridade
        limit: Limite de resultados
    
    Returns:
        Lista de PRPs encontrados
    """
    # Buscar no banco context-memory
    pass

@agent.tool
async def get_prp_details(
    ctx: RunContext[AgentDependencies],
    prp_id: int
) -> str:
    """
    Obtém detalhes completos de um PRP.
    
    Args:
        prp_id: ID do PRP
    
    Returns:
        Detalhes completos do PRP
    """
    # Buscar PRP e tarefas relacionadas
    pass
```

### 3. **Ferramentas de Componentes Opcionais (NOVAS)**

```python
@agent.tool
async def save_to_turso_memory(
    ctx: RunContext[AgentDependencies],
    data: str,
    data_type: str = "conversation"
) -> str:
    """
    Salva dados no Turso (componente opcional).
    
    Args:
        data: Dados para salvar
        data_type: Tipo de dados (conversation, analysis, etc.)
    
    Returns:
        Confirmação de salvamento
    """
    # Verificar se Turso está disponível
    if not ctx.deps.turso_available:
        return "Turso não disponível - dados não salvos"
    
    # Salvar no Turso via MCP
    pass

@agent.tool
async def track_with_sentry(
    ctx: RunContext[AgentDependencies],
    event_type: str,
    event_data: str
) -> str:
    """
    Rastreia evento no Sentry (componente opcional).
    
    Args:
        event_type: Tipo de evento
        event_data: Dados do evento
    
    Returns:
        Confirmação de rastreamento
    """
    # Verificar se Sentry está disponível
    if not ctx.deps.sentry_available:
        return "Sentry não disponível - evento não rastreado"
    
    # Rastrear no Sentry via MCP
    pass
```

## Dependências do Agente

```python
@dataclass
class PRPAgentDependencies:
    """Dependências para o agente PRP com arquitetura flexível."""
    
    # Configuração LLM
    llm_api_key: str
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    
    # Banco de dados
    database_path: str = "context-memory.db"
    
    # Configuração do agente
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Configurações de análise
    max_tokens_per_analysis: int = 4000
    analysis_timeout: int = 30
    
    # ARQUITETURA FLEXÍVEL - NOVAS CONFIGURAÇÕES
    turso_available: bool = False
    sentry_available: bool = False
    crewai_available: bool = False
    a2a_available: bool = False
    
    # Configurações de componentes opcionais
    turso_api_token: Optional[str] = None
    sentry_dsn: Optional[str] = None
    
    def __post_init__(self):
        """Inicialização pós-criação com detecção automática."""
        # Detectar componentes opcionais
        self.turso_available = self._detect_turso_availability()
        self.sentry_available = self._detect_sentry_availability()
    
    def _detect_turso_availability(self) -> bool:
        """Detecta se Turso está disponível."""
        # Verificar MCP Turso
        pass
    
    def _detect_sentry_availability(self) -> bool:
        """Detecta se Sentry está disponível."""
        # Verificar MCP Sentry
        pass
```

## Prompt do Sistema

```python
SYSTEM_PROMPT = """
Você é um assistente especializado em análise e gerenciamento de PRPs (Product Requirement Prompts) com arquitetura flexível.

Suas capacidades principais:
1. **Análise LLM**: Analisa PRPs e extrai tarefas automaticamente
2. **Gerenciamento de Banco**: CRUD completo para PRPs no banco context-memory
3. **Busca Inteligente**: Filtros avançados e busca semântica
4. **Interface Conversacional**: Respostas naturais e úteis
5. **Componentes Opcionais**: Turso (memória) e Sentry (monitoramento) quando disponíveis

ARQUITETURA FLEXÍVEL:
- PRP Agent: Sempre presente (metodologia principal)
- Turso: Opcional (sistema de memória)
- Sentry: Opcional (sistema de monitoramento)
- CrewAI: Opcional (framework de orquestração)
- A2A: Opcional (interoperabilidade entre agentes)

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

Diretrizes para componentes opcionais:
- Use Turso quando disponível para persistência
- Use Sentry quando disponível para monitoramento
- Funcione graciosamente quando componentes não estão disponíveis
- Informe usuário sobre status dos componentes

Sempre seja útil, preciso e mantenha o contexto da conversação.
"""
```

## Loop de Validação

### Nível 1: Validação da Estrutura do Agente

```bash
# Verificar estrutura completa do projeto do agente
find prp_agent_project -name "*.py" | sort
test -f prp_agent_project/agent.py && echo "Definição do agente presente"
test -f prp_agent_project/tools.py && echo "Módulo de ferramentas presente"
test -f prp_agent_project/models.py && echo "Módulo de modelos presente"
test -f prp_agent_project/dependencies.py && echo "Módulo de dependências presente"
test -f prp_agent_project/components/ && echo "Componentes opcionais presente"

# Verificar imports PydanticAI adequados
grep -q "from pydantic_ai import Agent" prp_agent_project/agent.py
grep -q "@agent.tool" prp_agent_project/tools.py
grep -q "from pydantic import BaseModel" prp_agent_project/models.py

# Verificar arquitetura flexível
grep -q "turso_available" prp_agent_project/dependencies.py
grep -q "sentry_available" prp_agent_project/dependencies.py

# Esperado: Todos os arquivos necessários com padrões PydanticAI corretos
# Se faltando: Gerar componentes ausentes com padrões corretos
```

### Nível 2: Validação de Funcionalidade do Agente

```bash
# Testar se o agente pode ser importado e instanciado
python -c "
from prp_agent_project.agent import agent
print('Agente criado com sucesso')
print(f'Modelo: {agent.model}')
print(f'Ferramentas: {len(agent.tools)}')
"

# Testar com TestModel para validação
python -c "
from pydantic_ai.models.test import TestModel
from prp_agent_project.agent import agent
test_model = TestModel()
with agent.override(model=test_model):
    result = agent.run_sync('Analise este PRP: Criar um sistema de login')
    print(f'Resposta do agente: {result.output}')
"

# Testar componentes opcionais
python -c "
from prp_agent_project.dependencies import PRPAgentDependencies
deps = PRPAgentDependencies(llm_api_key='test')
print(f'Turso disponível: {deps.turso_available}')
print(f'Sentry disponível: {deps.sentry_available}')
"

# Esperado: Instanciação do agente funciona, ferramentas registradas, validação TestModel passa
# Se falhando: Debugar configuração do agente e registro de ferramentas
```

### Nível 3: Validação de Testes Abrangentes

```bash
# Executar suite de testes completa
cd prp_agent_project
python -m pytest tests/ -v

# Testar comportamento específico do agente
python -m pytest tests/test_agent.py::test_agent_response -v
python -m pytest tests/test_tools.py::test_tool_validation -v
python -m pytest tests/test_models.py::test_output_validation -v
python -m pytest tests/test_components.py::test_optional_components -v

# Esperado: Todos os testes passam, cobertura abrangente alcançada
# Se falhando: Corrigir implementação baseado em falhas de teste
```

### Nível 4: Validação de Prontidão para Produção

```bash
# Verificar padrões de segurança
grep -r "API_KEY" prp_agent_project/ | grep -v ".py:" # Não deve expor chaves
test -f prp_agent_project/.env.example && echo "Template de ambiente presente"

# Verificar tratamento de erro
grep -r "try:" prp_agent_project/ | wc -l  # Deve ter tratamento de erro
grep -r "except" prp_agent_project/ | wc -l  # Deve ter tratamento de exceção

# Verificar configuração de logging
grep -r "logging\|logger" prp_agent_project/ | wc -l  # Deve ter logging

# Verificar arquitetura flexível
grep -r "turso_available\|sentry_available" prp_agent_project/ | wc -l  # Deve ter componentes opcionais

# Esperado: Medidas de segurança em vigor, tratamento de erro abrangente, logging configurado
# Se problemas: Implementar padrões de segurança e produção ausentes
```

## Checklist Final de Validação

### Completude da Implementação do Agente

- [ ] Estrutura completa do projeto do agente: `agent.py`, `tools.py`, `models.py`, `dependencies.py`
- [ ] Instanciação do agente com configuração adequada do provedor de modelo
- [ ] Registro de ferramentas com decoradores @agent.tool e integração RunContext
- [ ] Saídas estruturadas com validação de modelo Pydantic
- [ ] Injeção de dependência adequadamente configurada e testada
- [ ] Suite de testes abrangente com TestModel e FunctionModel
- [ ] **ARQUITETURA FLEXÍVEL**: Componentes opcionais implementados
- [ ] **ARQUITETURA FLEXÍVEL**: Detecção automática de disponibilidade
- [ ] **ARQUITETURA FLEXÍVEL**: Fallback gracioso para componentes não disponíveis

### Melhores Práticas PydanticAI

- [ ] Type safety em todo o código com type hints e validação adequados
- [ ] Padrões de segurança implementados (chaves de API, validação de entrada, rate limiting)
- [ ] Mecanismos de tratamento de erro e retry para operação robusta
- [ ] Padrões async/sync consistentes e apropriados
- [ ] Documentação e comentários de código para manutenibilidade
- [ ] **ARQUITETURA FLEXÍVEL**: Configuração via variáveis de ambiente
- [ ] **ARQUITETURA FLEXÍVEL**: Logging adequado para componentes opcionais

### Prontidão para Produção

- [ ] Configuração de ambiente com arquivos .env e validação
- [ ] Setup de logging e monitoramento para observabilidade
- [ ] Otimização de performance e gerenciamento de recursos
- [ ] Prontidão para implantação com gerenciamento adequado de configuração
- [ ] Estratégias de manutenção e atualização documentadas
- [ ] **ARQUITETURA FLEXÍVEL**: Deploy com componentes opcionais
- [ ] **ARQUITETURA FLEXÍVEL**: Monitoramento de componentes opcionais

---

## Anti-Padrões para Evitar

### Desenvolvimento de Agente PydanticAI

- ❌ Não pule validação TestModel - sempre teste com TestModel durante desenvolvimento
- ❌ Não codifique chaves de API - use variáveis de ambiente para todas as credenciais
- ❌ Não ignore padrões async - PydanticAI tem requisitos específicos async/sync
- ❌ Não crie cadeias de ferramentas complexas - mantenha ferramentas focadas e composáveis
- ❌ Não pule tratamento de erro - implemente mecanismos abrangentes de retry e fallback
- ❌ **Não force componentes opcionais** - Turso e Sentry são opcionais

### Arquitetura de Agente

- ❌ Não misture tipos de agente - separe claramente padrões de chat, ferramentas, workflow e saída estruturada
- ❌ Não ignore injeção de dependência - use gerenciamento adequado de dependências type-safe
- ❌ Não pule validação de saída - sempre use modelos Pydantic para respostas estruturadas
- ❌ Não esqueça documentação de ferramentas - garanta que todas as ferramentas tenham descrições e schemas adequados
- ❌ **Não ignore arquitetura flexível** - implemente componentes opcionais corretamente

### Segurança e Produção

- ❌ Não exponha dados sensíveis - valide todas as saídas e logs para segurança
- ❌ Não pule validação de entrada - sanitize e valide todas as entradas do usuário
- ❌ Não ignore rate limiting - implemente throttling adequado para serviços externos
- ❌ Não implante sem monitoramento - inclua observabilidade adequada desde o início
- ❌ **Não force componentes opcionais** - funcione graciosamente sem Turso/Sentry

**STATUS DA PESQUISA: [A SER COMPLETADO]** - Complete pesquisa abrangente PydanticAI e arquitetura flexível antes do início da implementação. 