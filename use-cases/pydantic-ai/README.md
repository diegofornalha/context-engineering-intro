# Template Pydantic AI com Engenharia de Contexto

Um template abrangente para construir agentes de IA de nível de produção usando Pydantic AI com melhores práticas de engenharia de contexto, integração de ferramentas, saídas estruturadas e padrões de teste abrangentes.

## 🚀 Início Rápido - Copiar Template

**Comece em 2 minutos:**

```bash
# Clone o repositório de engenharia de contexto
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/pydantic-ai

# 1. Copie este template para seu novo projeto
python copy_template.py /caminho/para/meu-projeto-agente

# 2. Navegue até seu projeto
cd /caminho/para/meu-projeto-agente

# 3. Comece a construir com o fluxo de trabalho PRP
# Preencha PRPs/INITIAL.md com o agente que você deseja criar

# 4. Gere o PRP baseado em seus requisitos detalhados (valide o PRP após gerar!)
/generate-pydantic-ai-prp PRPs/INITIAL.md

# 5. Execute o PRP para criar seu agente Pydantic AI
/execute-pydantic-ai-prp PRPs/generated_prp.md
```

Se você não estiver usando o Claude Code, pode simplesmente dizer ao seu assistente de IA para codificação usar os comandos slash generate-pydantic-ai-prp e execute-pydantic-ai-prp em .claude/commands como prompts.

## 📖 O que é Este Template?

Este template fornece tudo que você precisa para construir agentes Pydantic AI sofisticados usando fluxos de trabalho comprovados de engenharia de contexto. Ele combina:

- **Melhores Práticas do Pydantic AI**: Agentes type-safe com ferramentas, saídas estruturadas e injeção de dependência
- **Fluxos de Trabalho de Engenharia de Contexto**: Metodologia PRP (Product Requirements Prompts) comprovada
- **Exemplos Funcionais**: Implementações completas de agentes para aprender e estender

## 🎯 Fluxo de Trabalho do Framework PRP

Este template usa um fluxo de trabalho de engenharia de contexto em 3 etapas para construir agentes de IA:

### 1. **Definir Requisitos** (`PRPs/INITIAL.md`)
Comece definindo claramente o que seu agente precisa fazer:
```markdown
# Agente de Suporte ao Cliente - Requisitos Iniciais

## Visão Geral
Construir um agente inteligente de suporte ao cliente que possa lidar com consultas, 
acessar dados do cliente e escalar problemas apropriadamente.

## Requisitos Principais
- Conversas multi-turno com contexto e memória
- Autenticação de cliente e acesso à conta
- Consultas de saldo e transações da conta
- Processamento de pagamento e tratamento de reembolso
...
```

### 2. **Gerar Plano de Implementação**
```bash
/generate-pydantic-ai-prp PRPs/INITIAL.md
```
Isso cria um documento abrangente de 'Product Requirements Prompts' que inclui:
- Pesquisa de tecnologia Pydantic AI e melhores práticas
- Design de arquitetura do agente com ferramentas e dependências
- Roteiro de implementação com loops de validação
- Padrões de segurança e considerações de produção

### 3. **Executar Implementação**
```bash
/execute-pydantic-ai-prp PRPs/seu_agente.md
```
Isso implementa o agente completo baseado no PRP, incluindo:
- Criação do agente com configuração adequada do provedor de modelo
- Integração de ferramentas com tratamento de erros e validação
- Modelos de saída estruturada com validação Pydantic
- Testes abrangentes com TestModel e FunctionModel

## 📂 Estrutura do Template

```
pydantic-ai/
├── CLAUDE.md                           # Regras globais de desenvolvimento Pydantic AI
├── copy_template.py                    # Script de implantação do template
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # Geração de PRP para agentes
│   └── execute-pydantic-ai-prp.md      # Execução de PRP para agentes
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # Template base de PRP para agentes
│   └── INITIAL.md                      # Exemplo de requisitos de agente
├── examples/
│   ├── basic_chat_agent/               # Agente conversacional simples
│   │   ├── agent.py                    # Agente com memória e contexto
│   │   └── README.md                   # Guia de uso
│   ├── tool_enabled_agent/             # Agente com ferramentas externas
│   │   ├── agent.py                    # Ferramentas de busca web + calculadora
│   │   └── requirements.txt            # Dependências
│   └── testing_examples/               # Padrões abrangentes de teste
│       ├── test_agent_patterns.py      # Exemplos de TestModel, FunctionModel
│       └── pytest.ini                  # Configuração de teste
└── README.md                           # Este arquivo
```

## 🤖 Exemplos de Agentes Incluídos

### 1. Referência Principal do Agente (`examples/main_agent_reference/`)
**A implementação de referência canônica** mostrando padrões adequados do Pydantic AI:
- Configuração baseada em ambiente com `settings.py` e `providers.py`
- Separação limpa de responsabilidades entre agentes de email e pesquisa
- Estrutura adequada de arquivos para separar prompts, ferramentas, agentes e modelos Pydantic
- Integração de ferramentas com APIs externas (Gmail, Brave Search)

**Arquivos Principais:**
- `settings.py`: Configuração de ambiente com pydantic-settings
- `providers.py`: Abstração do provedor de modelo com `get_llm_model()`
- `research_agent.py`: Agente multi-ferramenta com busca web e integração de email
- `email_agent.py`: Agente especializado para criação de rascunhos do Gmail

### 2. Agente de Chat Básico (`examples/basic_chat_agent/`)
Um agente conversacional simples demonstrando padrões principais:
- **Configuração de modelo baseada em ambiente** (segue main_agent_reference)
- **Saída string por padrão** (sem `result_type` a menos que necessário)
- Prompts do sistema (estáticos e dinâmicos)
- Memória de conversação com injeção de dependência

**Recursos Principais:**
- Respostas em string simples (não saída estruturada)
- Padrão de configuração baseado em settings
- Rastreamento de contexto de conversação
- Implementação limpa e mínima

### 3. Agente com Ferramentas (`examples/tool_enabled_agent/`)
Um agente com capacidades de integração de ferramentas:
- **Configuração baseada em ambiente** (segue main_agent_reference)
- **Saída string por padrão** (sem estrutura desnecessária)
- Ferramentas de busca web e cálculo
- Mecanismos de tratamento de erros e retry

**Recursos Principais:**
- Padrões do decorador `@agent.tool`
- RunContext para injeção de dependência
- Tratamento e recuperação de erros de ferramentas
- Respostas em string simples das ferramentas

### 4. Agente de Saída Estruturada (`examples/structured_output_agent/`)
**NOVO**: Mostra quando usar `result_type` para validação de dados:
- **Configuração baseada em ambiente** (segue main_agent_reference)
- **Saída estruturada com validação Pydantic** (quando especificamente necessário)
- Análise de dados com ferramentas estatísticas
- Geração de relatórios profissionais

**Recursos Principais:**
- Demonstra o uso adequado de `result_type`
- Validação Pydantic para relatórios empresariais
- Ferramentas de análise de dados com estatísticas numéricas
- Documentação clara sobre quando usar saída estruturada vs string

### 5. Exemplos de Teste (`examples/testing_examples/`)
Padrões abrangentes de teste para agentes Pydantic AI:
- TestModel para validação rápida de desenvolvimento
- FunctionModel para teste de comportamento personalizado
- Agent.override() para isolamento de teste
- Fixtures Pytest e testes assíncronos

**Recursos Principais:**
- Testes unitários sem custos de API
- Injeção de dependência mock
- Validação de ferramentas e teste de cenários de erro
- Padrões de teste de integração

## 📚 Recursos Adicionais

- **Documentação Oficial do Pydantic AI**: https://ai.pydantic.dev/
- **Metodologia de Engenharia de Contexto**: Veja o README do repositório principal

## 🆘 Suporte e Contribuições

- **Issues**: Relate problemas com o template ou exemplos
- **Melhorias**: Contribua com exemplos ou padrões adicionais
- **Perguntas**: Pergunte sobre integração Pydantic AI ou engenharia de contexto

Este template faz parte do framework maior de Engenharia de Contexto. Veja o repositório principal para mais templates e metodologias de engenharia de contexto.

---

**Pronto para construir agentes de IA de nível de produção?** Comece com `python copy_template.py meu-projeto-agente` e siga o fluxo de trabalho PRP! 🚀