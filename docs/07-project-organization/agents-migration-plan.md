# 📋 Plano de Migração: /agents → /prp-agent/agents

## 📊 Análise da Situação Atual

### 🔍 Descobertas:

1. **Duplicação Parcial**: Existem 2 diretórios `agents`:
   - `/agents` (raiz do projeto)
   - `/prp-agent/agents` (dentro do prp-agent)

2. **Arquivos Diferentes**:
   - `settings.py`: Versão em `/agents` tem configurações de idioma e Sentry
   - `tools.py`: Versões têm diferenças não especificadas
   - Outros arquivos (agent.py, dependencies.py, providers.py) são idênticos

3. **Imports Problemáticos**:
   - **config/config_idioma.py** importa de `agents.settings`
   - **turso-agent/** tem múltiplos imports de `agents.turso_specialist`
   - Arquivos em **prp-agent/** importam de `agents.*`

## 🚨 Problema Principal

O arquivo `agents.turso_specialist` não existe em nenhum dos diretórios agents, indicando que há outra estrutura ou está faltando.

## ✅ Plano de Migração

### Fase 1: Preparação
1. ✅ Analisar estrutura atual
2. ✅ Verificar duplicações
3. ✅ Identificar imports
4. ⏳ Fazer backup completo

### Fase 2: Consolidação
1. **Mesclar configurações**:
   - Adicionar configs de idioma e Sentry ao `/prp-agent/agents/settings.py`
   - Analisar diferenças em `tools.py` e mesclar funcionalidades

2. **Resolver turso_specialist**:
   - Localizar onde está o módulo `turso_specialist`
   - Decidir se deve ficar em `/prp-agent/agents` ou `/turso-agent`

### Fase 3: Atualização de Imports
1. **Atualizar imports diretos**:
   ```python
   # De:
   from agents.settings import settings
   # Para:
   from prp_agent.agents.settings import settings
   ```

2. **Adicionar __init__.py adequados**:
   - Garantir que `/prp-agent/__init__.py` existe
   - Configurar imports relativos corretamente

### Fase 4: Validação
1. Executar testes existentes
2. Testar funcionalidades principais:
   - CLI do PRP Agent
   - Servidor MCP
   - Integração com Turso

### Fase 5: Limpeza
1. Remover `/agents` da raiz
2. Atualizar documentação
3. Atualizar .gitignore se necessário

## ⚠️ Riscos e Mitigações

### Risco 1: Quebrar funcionalidades em produção
**Mitigação**: Fazer backup completo e testar em ambiente isolado

### Risco 2: Imports circulares
**Mitigação**: Revisar estrutura de imports antes de mover

### Risco 3: Perda de configurações
**Mitigação**: Mesclar cuidadosamente settings.py mantendo todas as configs

## 📝 Comandos de Execução

```bash
# 1. Backup
cp -r /Users/agents/Desktop/context-engineering-intro/agents /Users/agents/Desktop/context-engineering-intro/agents.backup

# 2. Mesclar settings.py
# (manual - requer análise das diferenças)

# 3. Atualizar imports
# Usar sed ou ferramenta similar para substituir em massa

# 4. Remover diretório antigo
rm -rf /Users/agents/Desktop/context-engineering-intro/agents

# 5. Testar
cd /Users/agents/Desktop/context-engineering-intro/prp-agent
python cli.py
```

## 🎯 Resultado Esperado

- Um único diretório `/prp-agent/agents` com todas as funcionalidades
- Todos os imports apontando para o local correto
- Nenhuma funcionalidade quebrada
- Estrutura mais organizada e mantível