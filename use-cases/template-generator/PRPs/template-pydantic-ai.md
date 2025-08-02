---
name: "PRP de Gerador de Template PydanticAI"
description: "Gerar template abrangente de context engineering para desenvolvimento de agentes PydanticAI com ferramentas, memória e saídas estruturadas"
---

## Propósito

Gerar um pacote completo de template de context engineering para **PydanticAI** que permite aos desenvolvedores construir rapidamente agentes de IA inteligentes com integração de ferramentas, manipulação de conversas e validação de dados estruturados usando o framework PydanticAI.

## Princípios Fundamentais

1. **Especialização PydanticAI**: Integração profunda com padrões PydanticAI para criação de agentes, ferramentas e saídas estruturadas
2. **Geração de Pacote Completo**: Criar ecossistema completo de template com exemplos funcionais e validação
3. **Segurança de Tipos Primeiro**: Aproveitar o design type-safe do PydanticAI e validação Pydantic em todo o código
4. **Pronto para Produção**: Incluir segurança, teste e melhores práticas para implantações em produção
5. **Integração de Context Engineering**: Aplicar fluxos de trabalho comprovados de context engineering ao desenvolvimento de agentes de IA

---

## Objetivo

Gerar um pacote completo de template de context engineering para **PydanticAI** que inclui:

- Guia de implementação CLAUDE.md específico do PydanticAI com padrões de agentes
- Comandos especializados de geração e execução de PRP para agentes de IA
- Template base PRP específico do domínio com padrões de arquitetura de agentes
- Exemplos funcionais abrangentes (agentes de chat, integração de ferramentas, fluxos de trabalho multi-etapa)
- Loops de validação específicos do PydanticAI e padrões de teste

## Por que

- **Aceleração do Desenvolvimento de IA**: Habilitar desenvolvimento rápido de agentes PydanticAI de nível de produção
- **Consistência de Padrões**: Manter padrões estabelecidos de arquitetura de agentes de IA e melhores práticas
- **Garantia de Qualidade**: Garantir teste abrangente para comportamento de agentes, ferramentas e saídas
- **Captura de Conhecimento**: Documentar padrões específicos do PydanticAI, armadilhas e estratégias de integração
- **Framework de IA Escalável**: Criar templates reutilizáveis para vários casos de uso de agentes de IA

## O que

### Componentes do Pacote de Template

**Estrutura Completa de Diretório:**
```
use-cases/pydantic-ai/
├── CLAUDE.md                           # Guia de implementação PydanticAI
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # Geração de PRP de agente
│   └── execute-pydantic-ai-prp.md      # Execução de PRP de agente  
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # Template base PRP PydanticAI
│   ├── ai_docs/                        # Documentação PydanticAI
│   └── INITIAL.md                      # Solicitação de funcionalidade de agente de exemplo
├── examples/
│   ├── basic_chat_agent/               # Agente de chat simples com memória
│   ├── tool_enabled_agent/             # Ferramentas de busca web + calculadora
│   ├── workflow_agent/                 # Processamento de fluxo de trabalho multi-etapa
│   ├── structured_output_agent/        # Modelos Pydantic customizados
│   └── testing_examples/               # Padrões de teste de agentes
├── copy_template.py                    # Script de implantação do template
└── README.md                           # Guia de uso abrangente
```

**Integração PydanticAI:**
- Criação de agentes com múltiplos provedores de modelo (OpenAI, Anthropic, Gemini)
- Padrões de integração de ferramentas e registro de funções
- Memória de conversa e gerenciamento de contexto usando dependências
- Validação de saída estruturada com modelos Pydantic
- Padrões de teste usando TestModel e FunctionModel
- Padrões de segurança para gerenciamento de chaves de API e validação de entrada

**Adaptação de Context Engineering:**
- Processos de pesquisa específicos do PydanticAI e referências de documentação
- Loops de validação apropriados para agentes e estratégias de teste
- Planos de implementação especializados para framework de IA
- Integração com princípios base de context engineering para desenvolvimento de IA

### Critérios de Sucesso

- [ ] Estrutura completa do pacote de template PydanticAI gerada
- [ ] Todos os arquivos necessários presentes com conteúdo específico do PydanticAI
- [ ] Padrões de agentes representam com precisão as melhores práticas PydanticAI
- [ ] Princípios de context engineering adaptados para desenvolvimento de agentes de IA
- [ ] Loops de validação apropriados para teste de agentes de IA e ferramentas
- [ ] Template imediatamente utilizável para criar projetos PydanticAI
- [ ] Integração com framework base de context engineering mantida
- [ ] Exemplos abrangentes e documentação de teste incluídos

## Todo o Contexto Necessário

### Documentação & Referências (PESQUISADAS)

```yaml
# IMPORTANTE - use o servidor MCP Archon para obter mais documentação Pydantic AI!
- mcp: Archon
  why: Documentação oficial Pydantic AI pronta para consulta RAG
  content: Toda documentação Pydantic AI
# DOCUMENTAÇÃO CORE PYDANTIC AI - Entendimento essencial do framework
- url: https://ai.pydantic.dev/
  why: Documentação oficial PydanticAI com conceitos core e início
  content: Criação de agentes, provedores de modelo, segurança de tipos, injeção de dependência

- url: https://ai.pydantic.dev/agents/
  why: Arquitetura abrangente de agentes, prompts de sistema, ferramentas, saídas estruturadas
  content: Componentes de agentes, métodos de execução, opções de configuração

- url: https://ai.pydantic.dev/models/
  why: Configuração de provedores de modelo, gerenciamento de chaves de API, modelos de fallback
  content: Padrões de integração OpenAI, Anthropic, Gemini e autenticação

- url: https://ai.pydantic.dev/tools/
  why: Registro de ferramentas de função, uso de contexto, retornos ricos, ferramentas dinâmicas
  content: Decoradores de ferramentas, validação de parâmetros, padrões de documentação

- url: https://ai.pydantic.dev/testing/
  why: Estratégias de teste, TestModel, FunctionModel, padrões pytest
  content: Teste unitário, validação de comportamento de agentes, uso de modelo mock

- url: https://ai.pydantic.dev/examples/
  why: Exemplos funcionais para vários casos de uso PydanticAI
  content: Apps de chat, sistemas RAG, geração SQL, integração FastAPI

# FUNDAÇÃO DE CONTEXT ENGINEERING - Framework base para adaptar
- file: ../../../README.md
  why: Princípios core de context engineering e fluxo de trabalho para adaptar para agentes de IA

- file: ../../../.claude/commands/generate-prp.md
  why: Padrões base de geração de PRP para especializar para desenvolvimento PydanticAI

- file: ../../../.claude/commands/execute-prp.md  
  why: Padrões base de execução de PRP para adaptar para validação de agentes de IA

- file: ../../../PRPs/templates/prp_base.md
  why: Estrutura base de template PRP para especializar para domínio PydanticAI

# EXEMPLO DE SERVIDOR MCP - Implementação de referência
- file: ../mcp-server/CLAUDE.md
  why: Exemplo de padrões de guia de implementação específico do domínio
  
- file: ../mcp-server/.claude/commands/prp-mcp-create.md
  why: Exemplo de estrutura de comando especializado de geração de PRP
```

### Análise do Framework PydanticAI (DA PESQUISA)

```typescript
// Padrões de Arquitetura PydanticAI (da documentação oficial)
interface PydanticAIPatterns {
  // Padrões core de agentes
  agent_creation: {
    model_providers: ["openai:gpt-4o", "anthropic:claude-3-sonnet", "google:gemini-1.5-flash"];
    configuration: ["system_prompt", "deps_type", "output_type", "instructions"];
    execution_methods: ["run()", "run_sync()", "run_stream()", "iter()"];
  };
  
  // Padrões de sistema de ferramentas
  tool_system: {
    registration: ["@agent.tool", "@agent.tool_plain", "tools=[]"];
    context_access: ["RunContext[DepsType]", "ctx.deps", "dependency_injection"];
    return_types: ["str", "ToolReturn", "structured_data", "rich_content"];
    validation: ["parameter_schemas", "docstring_extraction", "type_hints"];
  };
  
  // Teste e validação
  testing_patterns: {
    unit_testing: ["TestModel", "FunctionModel", "Agent.override()"];
    validation: ["capture_run_messages()", "pytest_fixtures", "mock_dependencies"];
    evals: ["model_performance", "agent_behavior", "production_monitoring"];
  };
  
  // Considerações de produção
  security: {
    api_keys: ["environment_variables", "secure_storage", "key_rotation"];
    input_validation: ["pydantic_models", "parameter_validation", "sanitization"];
    monitoring: ["logfire_integration", "usage_tracking", "error_handling"];
  };
}
```

### Análise do Fluxo de Trabalho de Desenvolvimento (DA PESQUISA)

```yaml
# Padrões de Desenvolvimento PydanticAI (pesquisados da documentação e exemplos)
project_structure:
  basic_pattern: |
    my_agent/
    ├── agent.py          # Definição principal do agente
    ├── tools.py          # Funções de ferramentas
    ├── models.py         # Modelos de saída Pydantic
    ├── dependencies.py   # Dependências de contexto
    └── tests/
        ├── test_agent.py
        └── test_tools.py

  advanced_pattern: |
    agents_project/
    ├── agents/
    │   ├── __init__.py
    │   ├── chat_agent.py
    │   └── workflow_agent.py
    ├── tools/
    │   ├── __init__.py
    │   ├── web_search.py
    │   └── calculator.py
    ├── models/
    │   ├── __init__.py
    │   └── outputs.py
    ├── dependencies/
    │   ├── __init__.py
    │   └── database.py
    ├── tests/
    └── examples/

package_management:
  installation: "pip install pydantic-ai"
  optional_deps: "pip install 'pydantic-ai[examples]'"
  dev_deps: "pip install pytest pytest-asyncio inline-snapshot dirty-equals"

testing_workflow:
  unit_tests: "pytest tests/ -v"
  agent_testing: "Use TestModel for fast validation"
  integration_tests: "Use real models with rate limiting"
  evals: "Run performance benchmarks separately"

environment_setup:
  api_keys: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
  development: "Set ALLOW_MODEL_REQUESTS=False for testing"
  production: "Configure proper logging and monitoring"
```

### Segurança e Melhores Práticas (DA PESQUISA)

```typescript
// Padrões de segurança específicos do PydanticAI (da pesquisa)
interface PydanticAISecurity {
  // Gerenciamento de chaves de API
  api_security: {
    storage: "environment_variables_only";
    access_control: "minimal_required_permissions";
    monitoring: "usage_tracking_and_alerts";
  };
  
  // Validação e sanitização de entrada
  input_security: {
    validation: "pydantic_models_for_all_inputs";
    sanitization: "escape_user_content";
    rate_limiting: "prevent_abuse_patterns";
    content_filtering: "block_malicious_prompts";
  };
  
  // Prevenção de injeção de prompt
  prompt_security: {
    system_prompts: "clear_instruction_boundaries";
    user_input: "validate_and_sanitize";
    tool_calls: "parameter_validation";
    output_filtering: "structured_response_validation";
  };
  
  // Considerações de produção
  production_security: {
    monitoring: "logfire_integration_recommended";
    error_handling: "no_sensitive_data_in_logs";
    dependency_injection: "secure_context_management";
    testing: "security_focused_unit_tests";
  };
}
```

### Armadilhas Comuns e Casos Extremos (DA PESQUISA)

```yaml
# Armadilhas específicas do PydanticAI descobertas através da pesquisa
agent_gotchas:
  model_limits:
    issue: "Diferentes modelos têm diferentes limites de token e capacidades"
    solution: "Use FallbackModel for automatic model switching"
    validation: "Test with multiple model providers"
  
  async_patterns:
    issue: "Misturar chamadas de agente sync e async pode causar problemas"
    solution: "Padrões consistentes async/await em todo o código"
    validation: "Test both sync and async execution paths"
  
  dependency_injection:
    issue: "Grafos de dependência complexos podem ser difíceis de debugar"
    solution: "Mantenha dependências simples e bem tipadas"
    validation: "Unit test dependencies in isolation"

tool_integration_gotchas:
  parameter_validation:
    issue: "Ferramentas podem receber tipos de parâmetros inesperados"
    solution: "Use strict Pydantic models for tool parameters"
    validation: "Test tools with invalid inputs"
  
  context_management:
    issue: "Estado do RunContext pode se tornar inconsistente"
    solution: "Projete ferramentas stateless quando possível"
    validation: "Test context isolation between runs"
  
  error_handling:
    issue: "Erros de ferramentas podem crashar execuções inteiras de agentes"
    solution: "Implemente mecanismos de retry e degradação graciosa"
    validation: "Test error scenarios and recovery"

testing_gotchas:
  model_costs:
    issue: "Teste de modelo real pode ser caro"
    solution: "Use TestModel and FunctionModel for development"
    validation: "Separate unit tests from expensive eval runs"
  
  async_testing:
    issue: "Teste de agente async requer configuração especial"
    solution: "Use pytest-asyncio and proper fixtures"
    validation: "Test both sync and async code paths"
  
  deterministic_behavior:
    issue: "Respostas de IA são inerentemente não-determinísticas"
    solution: "Focus on testing tool calls and structured outputs"
    validation: "Use inline-snapshot for complex assertions"
```

## Plano de Implementação

### Fase de Pesquisa Tecnológica (CONCLUÍDA)

**Análise Abrangente do PydanticAI Concluída:**

✅ **Análise do Framework Core:** 
- Arquitetura PydanticAI, padrões de criação de agentes, integração de provedores de modelo
- Convenções de estrutura de projeto da documentação oficial e exemplos
- Sistema de injeção de dependência e princípios de design type-safe
- Fluxo de trabalho de desenvolvimento com padrões async/sync e suporte a streaming

✅ **Investigação do Sistema de Ferramentas:**
- Padrões de registro de ferramentas de função (@agent.tool vs @agent.tool_plain)
- Gerenciamento de contexto com RunContext e injeção de dependência
- Validação de parâmetros, extração de docstring e geração de schema
- Tipos de retorno ricos e suporte a conteúdo multi-modal

✅ **Análise do Framework de Teste:**
- TestModel e FunctionModel para teste unitário sem chamadas de API
- Padrões Agent.override() para isolamento de teste
- Integração Pytest com teste async e fixtures
- Estratégias de avaliação para performance de modelo vs teste unitário

✅ **Padrões de Segurança e Produção:**
- Gerenciamento de chaves de API com variáveis de ambiente e armazenamento seguro
- Validação de entrada usando modelos Pydantic e schemas de parâmetros
- Limitação de taxa, monitoramento e integração Logfire
- Vulnerabilidades de segurança comuns e estratégias de prevenção

### Geração do Pacote de Template

Criar template completo de context engineering PydanticAI baseado nas descobertas da pesquisa:

```yaml
Tarefa de Geração 1 - Criar Estrutura de Diretório do Template PydanticAI:
  CRIAR estrutura completa de diretório de caso de uso:
    - use-cases/pydantic-ai/
    - .claude/commands/ com comandos slash específicos do PydanticAI
    - PRPs/templates/ com template base focado em agentes
    - examples/ com implementações funcionais de agentes
    - Todos os subdiretórios por requisitos do pacote de template

Tarefa de Geração 2 - Gerar CLAUDE.md Específico do PydanticAI:
  CRIAR arquivo de regras globais PydanticAI incluindo:
    - Padrões de criação de agentes PydanticAI e integração de ferramentas
    - Configuração de provedores de modelo e gerenciamento de chaves de API
    - Padrões de arquitetura de agentes (chat, workflow, habilitado para ferramentas)
    - Estratégias de teste com TestModel/FunctionModel
    - Melhores práticas de segurança para agentes de IA e integração de ferramentas
    - Armadilhas comuns: padrões async, gerenciamento de contexto, limites de modelo

Tarefa de Geração 3 - Criar Comandos PRP PydanticAI:
  GERAR comandos slash específicos do domínio:
    - generate-pydantic-ai-prp.md com padrões de pesquisa de agentes
    - execute-pydantic-ai-prp.md com loops de validação de agentes de IA
    - Incluir referências de documentação PydanticAI e estratégias de pesquisa
    - Critérios de sucesso específicos de agentes e requisitos de teste

Tarefa de Geração 4 - Desenvolver Template Base PRP PydanticAI:
  CRIAR template especializado prp_pydantic_ai_base.md:
    - Pré-preenchido com padrões de arquitetura de agentes da pesquisa
    - Critérios de sucesso específicos do PydanticAI e portões de validação
    - Referências de documentação oficial e guias de provedores de modelo
    - Padrões de teste de agentes com TestModel e estratégias de validação

Tarefa de Geração 5 - Criar Exemplos PydanticAI Funcionais:
  GERAR agentes de exemplo abrangentes:
    - basic_chat_agent: Conversa simples com memória
    - tool_enabled_agent: Integração de busca web e calculadora
    - workflow_agent: Processamento de tarefas multi-etapa
    - structured_output_agent: Modelos Pydantic customizados
    - testing_examples: Testes unitários e padrões de validação
    - Incluir arquivos de configuração e configuração de ambiente

Tarefa de Geração 6 - Criar Script de Cópia do Template:
  CRIAR script Python para implantação do template:
    - copy_template.py com interface de linha de comando
    - Copia estrutura completa do template PydanticAI para localização alvo
    - Lida com todos os arquivos: CLAUDE.md, comandos, PRPs, exemplos, etc.
    - Tratamento de erro e feedback de sucesso com próximos passos

Tarefa de Geração 7 - Gerar README Abrangente:
  CRIAR README.md específico do PydanticAI:
    - Descrição clara: "Template de Context Engineering PydanticAI"
    - Uso do script de cópia do template (proeminentemente no topo)
    - Fluxo de trabalho do framework PRP para desenvolvimento de agentes de IA
    - Estrutura do template com explicações específicas do PydanticAI
    - Guia de início rápido com exemplos de criação de agentes
    - Visão geral de exemplos funcionais e padrões de teste
```

### Detalhes de Especialização PydanticAI

```typescript
// Especialização de template para PydanticAI
const pydantic_ai_specialization = {
  agent_patterns: [
    "chat_agent_with_memory",
    "tool_integrated_agent", 
    "workflow_processing_agent",
    "structured_output_agent"
  ],
  
  validation: [
    "agent_behavior_testing",
    "tool_function_validation", 
    "output_schema_verification",
    "model_provider_compatibility"
  ],
  
  examples: [
    "basic_conversation_agent",
    "web_search_calculator_tools",
    "multi_step_workflow_processing",
    "custom_pydantic_output_models",
    "comprehensive_testing_suite"
  ],
  
  gotchas: [
    "async_sync_mixing_issues",
    "model_token_limits",
    "dependency_injection_complexity",
    "tool_error_handling_failures",
    "context_state_management"
  ],
  
  security: [
    "api_key_environment_management",
    "input_validation_pydantic_models",
    "prompt_injection_prevention",
    "rate_limiting_implementation",
    "secure_tool_parameter_handling"
  ]
};
```

### Pontos de Integração

```yaml
FRAMEWORK_DE_CONTEXT_ENGINEERING:
  - base_workflow: Herdar geração/execução de PRP, adaptar para desenvolvimento de agentes de IA
  - validation_principles: Estender com teste específico de IA (comportamento de agente, validação de ferramentas)
  - documentation_standards: Manter consistência enquanto especializa para PydanticAI

INTEGRAÇÃO_PYDANTIC_AI:
  - agent_architecture: Incluir padrões de agentes de chat, habilitados para ferramentas e workflow
  - model_providers: Suportar padrões de configuração OpenAI, Anthropic, Gemini
  - testing_framework: Usar TestModel/FunctionModel para validação de desenvolvimento
  - production_patterns: Incluir segurança, monitoramento e considerações de implantação

ESTRUTURA_DE_TEMPLATE:
  - directory_organization: Seguir padrões de template de caso de uso com exemplos específicos de IA
  - file_naming: generate-pydantic-ai-prp.md, prp_pydantic_ai_base.md
  - content_format: Markdown com exemplos de código de agentes e configuração
  - command_patterns: Estender comandos slash para fluxos de trabalho de desenvolvimento de agentes de IA
```

## Loop de Validação

### Nível 1: Validação de Estrutura do Template PydanticAI

```bash
# Verificar estrutura completa do pacote de template PydanticAI
find use-cases/pydantic-ai -type f | sort
ls -la use-cases/pydantic-ai/.claude/commands/
ls -la use-cases/pydantic-ai/PRPs/templates/
ls -la use-cases/pydantic-ai/examples/

# Verificar script de cópia e exemplos de agentes
test -f use-cases/pydantic-ai/copy_template.py
ls use-cases/pydantic-ai/examples/*/agent.py 2>/dev/null | wc -l  # Deve ter arquivos de agente
python use-cases/pydantic-ai/copy_template.py --help 2>/dev/null || echo "Script de cópia precisa de ajuda"

# Esperado: Todos os arquivos necessários incluindo exemplos funcionais de agentes
# Se ausente: Gerar componentes ausentes com padrões PydanticAI
```

### Nível 2: Validação de Qualidade de Conteúdo PydanticAI

```bash
# Verificar precisão de conteúdo específico do PydanticAI
grep -r "from pydantic_ai import Agent" use-cases/pydantic-ai/examples/
grep -r "@agent.tool" use-cases/pydantic-ai/examples/
grep -r "TestModel\|FunctionModel" use-cases/pydantic-ai/

# Verificar padrões PydanticAI e evitar conteúdo genérico
grep -r "TODO\|PLACEHOLDER" use-cases/pydantic-ai/
grep -r "openai:gpt-4o\|anthropic:" use-cases/pydantic-ai/
grep -r "RunContext\|deps_type" use-cases/pydantic-ai/

# Esperado: Código PydanticAI real, sem placeholders, padrões de agentes presentes
# Se problemas: Adicionar padrões específicos do PydanticAI e exemplos adequados
```

### Nível 3: Validação Funcional PydanticAI

```bash
# Testar funcionalidade do template PydanticAI
cd use-cases/pydantic-ai

# Testar geração de PRP com foco em agentes
/generate-pydantic-ai-prp INITIAL.md
ls PRPs/*.md | grep -v templates | head -1  # Deve gerar PRP de agente

# Verificar se exemplos de agentes podem ser analisados (verificação de sintaxe)
python -m py_compile examples/basic_chat_agent/agent.py 2>/dev/null && echo "Sintaxe do agente básico OK"
python -m py_compile examples/tool_enabled_agent/agent.py 2>/dev/null && echo "Sintaxe do agente de ferramentas OK"

# Esperado: Geração de PRP funciona, exemplos de agentes têm sintaxe válida
# Se falhando: Debugar padrões de comando PydanticAI e corrigir código de agentes
```

### Nível 4: Teste de Integração PydanticAI

```bash
# Verificar se especialização PydanticAI mantém compatibilidade com framework base
diff -r ../../.claude/commands/ .claude/commands/ | head -10
grep -r "Context is King" . | wc -l  # Deve herdar princípios base
grep -r "pydantic.ai.dev\|PydanticAI" . | wc -l  # Deve ter especializações

# Testar se exemplos de agentes têm dependências adequadas
grep -r "pydantic_ai" examples/ | wc -l  # Deve importar PydanticAI
grep -r "pytest" examples/testing_examples/ | wc -l  # Deve ter testes

# Esperado: Especialização adequada, padrões de agentes funcionais, teste incluído
# Se problemas: Ajustar para manter compatibilidade enquanto adiciona recursos PydanticAI
```

## Checklist Final de Validação

### Completude do Pacote de Template PydanticAI

- [ ] Estrutura completa de diretório: `tree use-cases/pydantic-ai`
- [ ] Arquivos específicos do PydanticAI: CLAUDE.md com padrões de agentes, comandos especializados
- [ ] Script de cópia presente: `copy_template.py` com funcionalidade adequada do PydanticAI
- [ ] README abrangente: Inclui fluxo de trabalho de desenvolvimento de agentes e instruções de cópia
- [ ] Exemplos de agentes funcionais: Todos os exemplos usam padrões de código PydanticAI reais
- [ ] Padrões de teste incluídos: Exemplos TestModel/FunctionModel e validação
- [ ] Documentação completa: Padrões específicos do PydanticAI e armadilhas documentadas

### Qualidade e Usabilidade para PydanticAI

- [ ] Sem conteúdo placeholder: `grep -r "TODO\|PLACEHOLDER"` retorna vazio
- [ ] Especialização PydanticAI: Padrões de agentes, ferramentas, teste adequadamente documentados
- [ ] Loops de validação funcionam: Todos os comandos executáveis com funcionalidade específica de agentes
- [ ] Integração de framework: Funciona com context engineering base para desenvolvimento de IA
- [ ] Pronto para desenvolvimento de IA: Desenvolvedores podem criar agentes PydanticAI imediatamente

### Integração do Framework PydanticAI

- [ ] Herda princípios base: Fluxo de trabalho de context engineering preservado para agentes de IA
- [ ] Especialização adequada de IA: Padrões PydanticAI, segurança, teste incluídos
- [ ] Compatibilidade de comandos: Comandos slash funcionam para fluxos de trabalho de desenvolvimento de agentes
- [ ] Consistência de documentação: Segue padrões enquanto especializa para desenvolvimento de IA
- [ ] Estrutura mantível: Fácil de atualizar conforme o framework PydanticAI evolui

---

## Anti-Padrões para Evitar

### Geração de Template PydanticAI

- ❌ Não crie templates genéricos de IA - pesquise especificidades do PydanticAI completamente
- ❌ Não pule pesquisa de arquitetura de agentes - entenda ferramentas, memória, validação
- ❌ Não use código placeholder de agentes - inclua exemplos PydanticAI reais e funcionais
- ❌ Não ignore padrões de teste - TestModel/FunctionModel são críticos para IA

### Qualidade de Conteúdo PydanticAI

- ❌ Não assuma padrões de IA - documente armadilhas específicas do PydanticAI explicitamente
- ❌ Não pule pesquisa de segurança - chaves de API, validação de entrada, injeção de prompt críticos
- ❌ Não ignore provedores de modelo - inclua padrões OpenAI, Anthropic, Gemini
- ❌ Não esqueça padrões async - PydanticAI tem considerações específicas async/sync

### Integração do Framework PydanticAI

- ❌ Não quebre context engineering - mantenha fluxo de trabalho PRP para desenvolvimento de IA
- ❌ Não duplique funcionalidade base - estenda e especialize apropriadamente
- ❌ Não ignore validação específica de IA - teste de comportamento de agente é requisito único
- ❌ Não pule exemplos reais - inclua agentes funcionais com ferramentas e validação

**PONTUAÇÃO DE CONFIANÇA: 9/10** - Pesquisa abrangente do PydanticAI concluída, padrões de framework entendidos, pronto para gerar template especializado de context engineering para desenvolvimento de agentes de IA.