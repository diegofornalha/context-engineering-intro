---
name: "PRP Base do Gerador de Template"
description: "Meta-template para gerar templates de context engineering para domínios de tecnologia específicos e casos de uso"
---

## Propósito

Template otimizado para agentes de IA gerarem pacotes completos de template de context engineering para domínios de tecnologia específicos (frameworks de IA, stacks frontend, tecnologias backend, etc.) com especialização abrangente de domínio e validação.

## Princípios Fundamentais

1. **Meta-Context Engineering**: Aplicar princípios de context engineering para gerar templates específicos de domínio
2. **Especialização Tecnológica**: Integração profunda com padrões e convenções do framework alvo
3. **Geração de Pacote Completo**: Criar ecossistemas completos de template, não apenas arquivos individuais
4. **Dirigido por Validação**: Incluir loops abrangentes de teste e validação apropriados para o domínio
5. **Usabilidade Primeiro**: Gerar templates que são imediatamente utilizáveis por desenvolvedores

---

## Objetivo

Gerar um pacote completo de template de context engineering para **[TECNOLOGIA_ALVO]** que inclui:

- Guia de implementação CLAUDE.md específico do domínio
- Comandos especializados de geração e execução de PRP
- Template base PRP apropriado para a tecnologia
- Exemplos e documentação abrangentes
- Loops de validação específicos do domínio e critérios de sucesso

## Por que

- **Aceleração de Desenvolvedores**: Habilitar aplicação rápida de context engineering para qualquer tecnologia
- **Consistência de Padrões**: Manter princípios de context engineering em todos os domínios
- **Garantia de Qualidade**: Garantir validação e teste abrangentes para cada tecnologia
- **Captura de Conhecimento**: Documentar melhores práticas e padrões para tecnologias específicas
- **Framework Escalável**: Criar templates reutilizáveis que evoluem com mudanças tecnológicas

## O que

### Componentes do Pacote de Template

**Estrutura Completa de Diretório:**
```
use-cases/{technology-name}/
├── CLAUDE.md                      # Guia de implementação do domínio
├── .claude/commands/
│   ├── generate-{technology}-prp.md  # Geração de PRP do domínio
│   └── execute-{technology}-prp.md   # Execução de PRP do domínio  
├── PRPs/
│   ├── templates/
│   │   └── prp_{technology}_base.md  # Template base PRP do domínio
│   ├── ai_docs/                      # Documentação do domínio (opcional)
│   └── INITIAL.md                    # Solicitação de funcionalidade de exemplo
├── examples/                         # Exemplos de código do domínio
├── copy_template.py                  # Script de implantação do template
└── README.md                         # Guia de uso abrangente
```

**Integração Tecnológica:**
- Ferramentas e comandos específicos do framework
- Padrões arquiteturais e convenções
- Integração do fluxo de trabalho de desenvolvimento
- Abordagens de teste e validação
- Considerações de segurança e performance

**Adaptação de Context Engineering:**
- Processos de pesquisa específicos do domínio
- Loops de validação apropriados para a tecnologia
- Planos de implementação especializados para framework
- Integração com princípios base de context engineering

### Critérios de Sucesso

- [ ] Estrutura completa do pacote de template gerada
- [ ] Todos os arquivos necessários presentes e formatados adequadamente
- [ ] Conteúdo específico do domínio representa com precisão padrões da tecnologia
- [ ] Princípios de context engineering adaptados adequadamente para a tecnologia
- [ ] Loops de validação apropriados e executáveis para o framework
- [ ] Template imediatamente utilizável para criar projetos no domínio
- [ ] Integração com framework base de context engineering mantida
- [ ] Documentação e exemplos abrangentes incluídos

## Todo o Contexto Necessário

### Documentação & Referências (DEVE LER)

```yaml
# FUNDAÇÃO DE CONTEXT ENGINEERING - Entender o framework base
- file: ../../../README.md
  why: Princípios core de context engineering e fluxo de trabalho para adaptar

- file: ../../../.claude/commands/generate-prp.md
  why: Padrões base de geração de PRP para especializar para domínio

- file: ../../../.claude/commands/execute-prp.md  
  why: Padrões base de execução de PRP para adaptar para tecnologia

- file: ../../../PRPs/templates/prp_base.md
  why: Estrutura base de template PRP para especializar para domínio

# EXEMPLO DE SERVIDOR MCP - Implementação de referência de especialização de domínio
- file: ../mcp-server/CLAUDE.md
  why: Exemplo de padrões de guia de implementação específico do domínio

- file: ../mcp-server/.claude/commands/prp-mcp-create.md
  why: Exemplo de comando especializado de geração de PRP

- file: ../mcp-server/PRPs/templates/prp_mcp_base.md
  why: Exemplo de template base PRP especializado para domínio

# PESQUISA DE TECNOLOGIA ALVO - Adicionar documentação específica do domínio
- url: [DOCUMENTAÇÃO_OFICIAL_FRAMEWORK]
  why: Conceitos core do framework, APIs e padrões arquiteturais

- url: [GUIA_MELHORES_PRÁTICAS]
  why: Padrões e convenções estabelecidas para a tecnologia

- url: [CONSIDERAÇÕES_DE_SEGURANÇA]
  why: Melhores práticas de segurança e vulnerabilidades comuns

- url: [FRAMEWORKS_DE_TESTE]
  why: Abordagens de teste e padrões de validação para a tecnologia

- url: [PADRÕES_DE_IMPLANTAÇÃO]
  why: Considerações de implantação em produção e monitoramento
```

### Estrutura Atual de Context Engineering

```bash
# Estrutura base do framework para estender
context-engineering-intro/
├── README.md                    # Princípios core para adaptar
├── .claude/commands/            # Comandos base para especializar
├── PRPs/templates/prp_base.md   # Template base para estender
├── CLAUDE.md                    # Regras base para herdar
└── use-cases/
    ├── mcp-server/              # Exemplo de especialização de referência
    └── template-generator/      # Este sistema meta-template
```

### Requisitos de Análise de Tecnologia Alvo

```typescript
// Áreas de pesquisa para especialização tecnológica
interface TechnologyAnalysis {
  // Padrões core do framework
  architecture: {
    project_structure: string[];
    configuration_files: string[];
    dependency_management: string;
    module_organization: string[];
  };
  
  // Fluxo de trabalho de desenvolvimento
  development: {
    package_manager: string;
    dev_server_commands: string[];
    build_process: string[];
    testing_frameworks: string[];
  };
  
  // Melhores práticas
  patterns: {
    code_organization: string[];
    state_management: string[];
    error_handling: string[];
    performance_optimization: string[];
  };
  
  // Pontos de integração
  ecosystem: {
    common_libraries: string[];
    deployment_platforms: string[];
    monitoring_tools: string[];
    CI_CD_patterns: string[];
  };
}
```

### Padrões Conhecidos de Geração de Template

```typescript
// CRÍTICO: Geração de template deve seguir estes padrões

// 1. SEMPRE herdar de princípios base de context engineering
const basePatterns = {
  prp_workflow: "INITIAL.md → generate-prp → execute-prp",
  validation_loops: "syntax → unit → integration → deployment",
  context_richness: "documentation + examples + patterns + gotchas"
};

// 2. SEMPRE especializar para a tecnologia alvo
const specialization = {
  tooling: "Substituir comandos genéricos por específicos do framework",
  patterns: "Incluir convenções arquiteturais do framework",
  validation: "Usar teste e linting apropriados para a tecnologia",
  examples: "Fornecer exemplos de código reais e funcionais para o domínio"
};

// 3. SEMPRE manter usabilidade e completude
const quality_gates = {
  immediate_usability: "Template funciona out of the box",
  comprehensive_docs: "Todos os padrões e armadilhas documentados",
  working_examples: "Exemplos compilam e executam com sucesso",
  validation_loops: "Todos os comandos de validação são executáveis"
};

// 4. Armadilhas comuns para evitar
const anti_patterns = {
  generic_content: "Não usar texto placeholder - pesquisar padrões reais",
  incomplete_research: "Não pular documentação específica da tecnologia",
  broken_examples: "Não incluir exemplos de código não funcionais",
  missing_validation: "Não pular padrões de teste apropriados para o domínio"
};
```

## Plano de Implementação

### Fase de Pesquisa Tecnológica

**CRÍTICO: Pesquisar extensivamente na web antes de qualquer geração de template. Isso é essencial para o sucesso.**

Conduzir análise abrangente da tecnologia alvo usando pesquisa na web:

```yaml
Tarefa de Pesquisa 1 - Análise Core do Framework (PESQUISA WEB REQUERIDA):
  PESQUISAR NA WEB e ESTUDAR documentação oficial completamente:
    - Arquitetura do framework e padrões de design  
    - Convenções de estrutura de projeto e melhores práticas
    - Padrões de arquivo de configuração e abordagens de gerenciamento
    - Gerenciamento de pacote/dependência para a tecnologia
    - Guias de início e procedimentos de configuração

Tarefa de Pesquisa 2 - Análise do Fluxo de Trabalho de Desenvolvimento (PESQUISA WEB REQUERIDA):
  PESQUISAR NA WEB e ANALISAR padrões de desenvolvimento:
    - Configuração de desenvolvimento local e ferramentas
    - Processos de build e etapas de compilação
    - Frameworks de teste comumente usados com esta tecnologia
    - Ferramentas de debug e ambientes de desenvolvimento
    - Comandos CLI e fluxos de trabalho de gerenciamento de pacotes

Tarefa de Pesquisa 3 - Investigação de Melhores Práticas (PESQUISA WEB REQUERIDA):
  PESQUISAR NA WEB e PESQUISAR padrões estabelecidos:
    - Organização de código e convenções de estrutura de arquivo
    - Melhores práticas de segurança específicas para esta tecnologia
    - Armadilhas comuns, pitfalls e casos extremos
    - Padrões de tratamento de erro e estratégias
    - Considerações de performance e técnicas de otimização

Tarefa de Pesquisa 4 - Planejamento da Estrutura do Pacote de Template:
  PLANEJAR como criar template de context engineering para esta tecnologia:
    - Como adaptar framework PRP para esta tecnologia específica
    - Quais regras CLAUDE.md específicas do domínio são necessárias
    - Quais loops de validação são apropriados para este framework
    - Quais exemplos e documentação devem ser incluídos
```

### Geração do Pacote de Template

Criar pacote completo de template de context engineering baseado nas descobertas da pesquisa na web:

```yaml
Tarefa de Geração 1 - Criar Estrutura de Diretório do Template:
  CRIAR estrutura completa de diretório de caso de uso:
    - use-cases/{technology-name}/
    - .claude/commands/ subdiretório  
    - PRPs/templates/ subdiretório
    - examples/ subdiretório
    - Todos os outros subdiretórios necessários por requisitos do pacote de template

Tarefa de Geração 2 - Gerar CLAUDE.md Específico do Domínio:
  CRIAR arquivo de regras globais específico da tecnologia:
    - Comandos de ferramentas e gerenciamento de pacotes específicos da tecnologia
    - Padrões arquiteturais e convenções do framework da pesquisa na web
    - Procedimentos de fluxo de trabalho de desenvolvimento específicos para esta tecnologia
    - Segurança e melhores práticas descobertas através da pesquisa
    - Armadilhas comuns e pontos de integração encontrados na documentação

Tarefa de Geração 3 - Criar Comandos PRP Especializados do Template:
  GERAR comandos slash específicos do domínio:
    - generate-{technology}-prp.md com padrões de pesquisa da tecnologia
    - execute-{technology}-prp.md com loops de validação do framework
    - Comandos devem referenciar padrões específicos da tecnologia da pesquisa
    - Incluir estratégias de pesquisa na web específicas para este domínio tecnológico

Tarefa de Geração 4 - Desenvolver Template Base PRP Específico do Domínio:
  CRIAR template especializado prp_{technology}_base.md:
    - Pré-preenchido com contexto da tecnologia da pesquisa na web
    - Critérios de sucesso específicos da tecnologia e portões de validação
    - Referências de documentação do framework encontradas através da pesquisa
    - Padrões de implementação apropriados para o domínio e loops de validação

Tarefa de Geração 5 - Criar Exemplos e Template INITIAL.md:
  GERAR conteúdo abrangente do pacote de template:
    - INITIAL.md de exemplo mostrando como solicitar funcionalidades para esta tecnologia
    - Exemplos de código funcionais relevantes para a tecnologia (da pesquisa)
    - Templates de arquivo de configuração e padrões

Tarefa de Geração 6 - Criar Script de Cópia do Template:
  CRIAR script Python para implantação do template:
    - Script copy_template.py que aceita argumento de diretório alvo
    - Copia estrutura completa de diretório do template para localização especificada
    - Inclui todos os arquivos: CLAUDE.md, comandos, PRPs, exemplos, etc.
    - Lida com criação de diretório e cópia de arquivos com tratamento de erro
    - Interface simples de linha de comando para uso fácil

Tarefa de Geração 7 - Gerar README Abrangente:
  CRIAR README.md abrangente mas conciso:
    - Descrição clara do que este template é para e seu propósito
    - Explicação do fluxo de trabalho do framework PRP (processo de 3 etapas)
    - Instruções de uso do script de cópia do template (colocadas proeminentemente perto do topo)
    - Guia de início rápido com exemplos concretos
    - Visão geral da estrutura do template mostrando todos os arquivos gerados
    - Exemplos de uso específicos para este domínio tecnológico
```

### Detalhes de Implementação para Script de Cópia e README

**Requisitos do Script de Cópia (copy_template.py):**
```python
# Funcionalidade essencial do script de cópia:
# 1. Aceitar diretório alvo como argumento de linha de comando
# 2. Copiar estrutura completa de diretório do template para localização alvo
# 3. Incluir TODOS os arquivos: CLAUDE.md, .claude/, PRPs/, examples/, README.md
# 4. Lidar com criação de diretório e tratamento de erro
# 5. Fornecer feedback claro de sucesso com próximos passos
# 6. Uso simples: python copy_template.py /path/to/target
```

**Requisitos da Estrutura README:**
```markdown
# Deve incluir estas seções nesta ordem:
# 1. Título e breve descrição do propósito do template
# 2. 🚀 Início Rápido - Copiar Template Primeiro (proeminentemente no topo)
# 3. 📋 Fluxo de Trabalho do Framework PRP (explicação do processo de 3 etapas)
# 4. 📁 Estrutura do Template (árvore de diretório com explicações)
# 5. 🎯 O Que Você Pode Construir (exemplos específicos da tecnologia)
# 6. 📚 Recursos Principais (capacidades do framework)
# 7. 🔍 Exemplos Incluídos (exemplos funcionais fornecidos)
# 8. 📖 Referências de Documentação (fontes de pesquisa)
# 9. 🚫 Armadilhas Comuns (pitfalls específicos da tecnologia)

# Uso do script de cópia deve ser destacado proeminentemente perto do topo
# Fluxo de trabalho PRP deve mostrar claramente as 3 etapas com comandos reais
# Tudo deve ser específico da tecnologia, não genérico
```

### Detalhes de Especialização de Domínio

```typescript
// Padrões de especialização de template para domínios específicos

// Para Frameworks de IA/ML (Pydantic AI, CrewAI, etc.)
const ai_specialization = {
  patterns: ["agent_architecture", "tool_integration", "model_configuration"],
  validation: ["model_response_testing", "agent_behavior_validation"],
  examples: ["basic_agent", "multi_agent_system", "tool_integration"],
  gotchas: ["token_limits", "model_compatibility", "async_patterns"]
};

// Para Frameworks Frontend (React, Vue, Svelte, etc.)
const frontend_specialization = {
  patterns: ["component_architecture", "state_management", "routing"],
  validation: ["component_testing", "e2e_testing", "accessibility"],
  examples: ["basic_app", "state_integration", "api_consumption"],
  gotchas: ["bundle_size", "ssr_considerations", "performance"]
};

// Para Frameworks Backend (FastAPI, Express, Django, etc.)
const backend_specialization = {
  patterns: ["api_design", "database_integration", "authentication"],
  validation: ["api_testing", "database_testing", "security_testing"],
  examples: ["rest_api", "auth_system", "database_models"],
  gotchas: ["security_vulnerabilities", "performance_bottlenecks", "scalability"]
};

// Para Frameworks de Banco de Dados/Dados (SQLModel, Prisma, etc.)
const data_specialization = {
  patterns: ["schema_design", "migration_management", "query_optimization"],
  validation: ["schema_testing", "migration_testing", "query_performance"],
  examples: ["basic_models", "relationships", "complex_queries"],
  gotchas: ["migration_conflicts", "n+1_queries", "index_optimization"]
};
```

### Pontos de Integração

```yaml
FRAMEWORK_DE_CONTEXT_ENGINEERING:
  - base_workflow: Herdar padrões core de geração e execução de PRP do framework base
  - validation_principles: Estender validação base com verificações específicas do domínio para a tecnologia
  - documentation_standards: Manter consistência com padrões de documentação base de context engineering

INTEGRAÇÃO_TECNOLÓGICA:
  - package_management: Incluir gerenciadores de pacote e ferramentas específicos do framework
  - development_tools: Incluir ferramentas de desenvolvimento e teste específicas da tecnologia
  - framework_patterns: Usar padrões arquiteturais e de código apropriados para a tecnologia
  - validation_approaches: Incluir métodos de teste e validação específicos do framework

ESTRUTURA_DE_TEMPLATE:
  - directory_structure: Seguir padrões estabelecidos de template de caso de uso do framework base
  - file_naming: Manter convenções de nomenclatura consistentes (generate-{tech}-prp.md, etc.)
  - content_format: Usar formatos estabelecidos de markdown e documentação
  - command_patterns: Estender funcionalidade base de comando slash para a tecnologia específica
```

## Loop de Validação

### Nível 1: Validação de Estrutura do Template

```bash
# CRÍTICO: Verificar estrutura completa do pacote de template
find use-cases/{technology-name} -type f | sort
ls -la use-cases/{technology-name}/.claude/commands/
ls -la use-cases/{technology-name}/PRPs/templates/

# Verificar se script de cópia existe e é funcional
test -f use-cases/{technology-name}/copy_template.py
python use-cases/{technology-name}/copy_template.py --help 2>/dev/null || echo "Script de cópia precisa de opção help"

# Esperado: Todos os arquivos necessários presentes incluindo copy_template.py
# Se ausente: Gerar arquivos ausentes seguindo padrões estabelecidos
```

### Nível 2: Validação de Qualidade de Conteúdo

```bash
# Verificar precisão de conteúdo específico do domínio
grep -r "TODO\|PLACEHOLDER\|{domain}" use-cases/{technology-name}/
grep -r "{technology}" use-cases/{technology-name}/ | wc -l

# Verificar padrões específicos da tecnologia
grep -r "framework-specific-pattern" use-cases/{technology-name}/
grep -r "validation" use-cases/{technology-name}/.claude/commands/

# Esperado: Sem conteúdo placeholder, padrões de tecnologia presentes
# Se problemas: Pesquisar e adicionar conteúdo específico do domínio adequado
```

### Nível 3: Validação Funcional

```bash
# Testar funcionalidade do template
cd use-cases/{technology-name}

# Testar comando de geração de PRP
/generate-prp INITIAL.md
ls PRPs/*.md | grep -v templates

# Testar completude do template
grep -r "Context is King" . | wc -l  # Deve herdar princípios
grep -r "{technology-specific}" . | wc -l  # Deve ter especializações

# Esperado: Geração de PRP funciona, conteúdo é especializado
# Se falhando: Debugar padrões de comando e estrutura do template
```

### Nível 4: Teste de Integração

```bash
# Verificar integração com framework base de context engineering
diff -r ../../.claude/commands/ .claude/commands/ | head -20
diff ../../CLAUDE.md CLAUDE.md | head -20

# Testar se template produz resultados funcionais
cd examples/
# Executar quaisquer comandos de validação de exemplo específicos para a tecnologia

# Esperado: Especialização adequada sem quebrar padrões base
# Se problemas: Ajustar especialização para manter compatibilidade
```

## Checklist Final de Validação

### Completude do Pacote de Template

- [ ] Estrutura completa de diretório: `tree use-cases/{technology-name}`
- [ ] Todos os arquivos necessários presentes: CLAUDE.md, comandos, PRP base, exemplos
- [ ] Script de cópia presente: `copy_template.py` com funcionalidade adequada
- [ ] README abrangente: Inclui instruções de script de cópia e fluxo de trabalho PRP
- [ ] Conteúdo específico do domínio: Padrões de tecnologia representados com precisão
- [ ] Exemplos funcionais: Todos os exemplos compilam/executam com sucesso
- [ ] Documentação completa: README e instruções de uso claras

### Qualidade e Usabilidade

- [ ] Sem conteúdo placeholder: `grep -r "TODO\|PLACEHOLDER"`
- [ ] Especialização tecnológica: Padrões de framework adequadamente documentados
- [ ] Loops de validação funcionam: Todos os comandos executáveis e funcionais
- [ ] Integração mantida: Funciona com framework base de context engineering
- [ ] Pronto para uso: Desenvolvedor pode imediatamente começar a usar template

### Integração de Framework

- [ ] Herda princípios base: Fluxo de trabalho de context engineering preservado
- [ ] Especialização adequada: Padrões específicos da tecnologia incluídos
- [ ] Compatibilidade de comandos: Comandos slash funcionam como esperado
- [ ] Consistência de documentação: Segue padrões estabelecidos de documentação
- [ ] Estrutura mantível: Fácil de atualizar conforme tecnologia evolui

---

## Anti-Padrões para Evitar

### Geração de Template

- ❌ Não crie templates genéricos - sempre pesquise e especialize profundamente
- ❌ Não pule pesquisa tecnológica abrangente - entenda frameworks completamente
- ❌ Não use conteúdo placeholder - sempre inclua informação real e pesquisada
- ❌ Não ignore loops de validação - inclua teste abrangente para a tecnologia

### Qualidade de Conteúdo

- ❌ Não assuma conhecimento - documente tudo explicitamente para o domínio
- ❌ Não pule casos extremos - inclua armadilhas comuns e tratamento de erro
- ❌ Não ignore segurança - sempre inclua considerações de segurança para a tecnologia
- ❌ Não esqueça manutenção - garanta que templates possam evoluir com mudanças tecnológicas

### Integração de Framework

- ❌ Não quebre padrões base - mantenha compatibilidade com princípios de context engineering
- ❌ Não duplique esforço - reutilize e estenda componentes do framework base
- ❌ Não ignore consistência - siga convenções estabelecidas de nomenclatura e estrutura
- ❌ Não pule validação - garanta que templates realmente funcionem antes da conclusão