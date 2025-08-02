# Gerador de Templates - Regras Globais para Context Engineering

Este arquivo contém as regras globais e princípios que se aplicam a TODO trabalho de context engineering, independentemente de qual template ou projeto você está construindo. Essas regras nunca mudam e devem ser seguidas consistentemente.

## 🔄 Princípios Fundamentais de Context Engineering

**IMPORTANTE: Esses princípios se aplicam a TODO trabalho de context engineering:**

### Fluxo de Trabalho do Framework PRP
- **Sempre comece com INITIAL.md** - Defina requisitos antes de gerar PRPs
- **Use o padrão PRP**: INITIAL.md → `/generate-template-prp INITIAL.md` → `/execute-template-prp PRPs/arquivo.md`
- **Siga loops de validação** - Cada PRP deve incluir etapas de validação executáveis
- **Contexto é Rei** - Inclua TODA documentação, exemplos e padrões necessários

### Metodologia de Pesquisa
- **Pesquisa web primeiro** - Sempre faça pesquisa web extensiva antes da implementação
- **Mergulho na documentação** - Estude documentação oficial, melhores práticas e padrões comuns
- **Extração de padrões** - Identifique padrões reutilizáveis e convenções arquiteturais
- **Documentação de armadilhas** - Documente armadilhas comuns e casos extremos

## 📚 Consciência e Contexto do Projeto

- **Use convenções de nomenclatura consistentes** e padrões de estrutura de arquivos
- **Siga padrões estabelecidos de organização de diretórios**
- **Aproveite exemplos extensivamente** - Estude padrões existentes antes de criar novos

## 🧱 Estrutura e Modularidade do Código

- **Nunca crie arquivos com mais de 500 linhas** - Divida em módulos quando se aproximar do limite
- **Organize código em módulos claramente separados** agrupados por funcionalidade ou responsabilidade
- **Use imports claros e consistentes** (prefira imports relativos dentro de pacotes)
- **Siga padrões de codificação estabelecidos** e convenções

## ✅ Gerenciamento de Tarefas

- **Divida tarefas complexas em etapas menores** com critérios claros de conclusão
- **Marque tarefas como concluídas imediatamente** após terminá-las
- **Atualize status da tarefa em tempo real** conforme o trabalho progride

## 📎 Padrões de Documentação

- **Escreva documentação abrangente** para cada componente
- **Inclua exemplos claros de uso** com código funcional
- **Documente todas as armadilhas e casos extremos** para prevenir erros comuns
- **Mantenha referências atualizadas** para documentação externa

## 🔍 Padrões de Pesquisa

- **Pesquisa web é sua melhor amiga** - Use extensivamente para pesquisa tecnológica
- **Estude documentação oficial completamente** antes da implementação
- **Pesquise padrões estabelecidos** e melhores práticas para a tecnologia
- **Documente todas as descobertas abrangentemente** em PRPs e guias de implementação

## 🎯 Padrões de Implementação

- **Siga o fluxo de trabalho PRP religiosamente** - Não pule etapas
- **Sempre valide antes de prosseguir** para a próxima etapa
- **Use padrões existentes como templates** em vez de criar do zero
- **Inclua tratamento de erro abrangente** em todas as implementações

## 🚫 Anti-Padrões para Sempre Evitar

- ❌ Não pule pesquisa - Sempre entenda a tecnologia profundamente primeiro
- ❌ Não crie soluções genéricas - Sempre especialize para o caso de uso específico
- ❌ Não ignore validação - Cada etapa deve incluir verificação
- ❌ Não assuma conhecimento - Documente tudo explicitamente
- ❌ Não pule exemplos - Sempre inclua exemplos de código funcional
- ❌ Não esqueça casos extremos - Inclua tratamento de erro e armadilhas

## 🔧 Padrões de Uso de Ferramentas

- **Use pesquisa web extensivamente** para pesquisa e documentação
- **Siga padrões de comando estabelecidos** para comandos slash
- **Use loops de validação** para garantir qualidade em cada etapa

Essas regras globais se aplicam independentemente de você estar gerando templates, implementando funcionalidades ou fazendo pesquisa. Elas formam a base do trabalho efetivo de context engineering.