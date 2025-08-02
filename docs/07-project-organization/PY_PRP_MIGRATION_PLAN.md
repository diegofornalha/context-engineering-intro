# 🚀 Plano de Migração: py-prp → prp-agent

## 📊 Análise da Situação

A pasta `/py-prp` contém 45 scripts Python com funcionalidades variadas. Vamos consolidar tudo em `/prp-agent` para ter um único local de desenvolvimento.

## 📋 Categorização dos Scripts

### 1. **Scripts de Integração PRP (MANTER)**
- `prp_mcp_integration.py` - Integração principal PRP+MCP
- `real_mcp_integration.py` - Integração real com MCP
- `setup_prp_database.py` - Setup do banco PRP
- `cli.py` - Interface CLI

**Destino:** `/prp-agent/integrations/`

### 2. **Scripts de Diagnóstico Turso (MANTER)**
- `diagnose_turso_mcp.py`
- `test_turso_token.py`
- `test_new_token.py`
- `organize_turso_configs.py`
- `test_turso_direct.py`

**Destino:** `/prp-agent/diagnostics/`

### 3. **Scripts de Sincronização (CONSOLIDAR)**
- `mcp_smart_sync.py`
- `sync_docs_automatico.py`
- `sync_docs_simples.py`
- `simple_turso_sync.py`
- `turso_local_sync.py`
- + 5 outros scripts similares

**Ação:** Já temos `unified_sync.py`, arquivar os outros

### 4. **Scripts Sentry (MANTER)**
- `setup_sentry_integration.py`
- `sentry_prp_agent_setup.py`
- `sentry_ai_agent_setup.py`
- `prp_agent_sentry_integration.py`
- + outros relacionados

**Destino:** `/prp-agent/monitoring/`

### 5. **Scripts de Demonstração (ARQUIVAR)**
- `memory_demo.py`
- `demonstrate_docs_clusters.py`
- `docs_search_demo.py`
- `release_health_demo.py`

**Destino:** `/prp-agent/examples/demos/`

### 6. **Scripts de Teste (MOVER)**
- `test_memory_system.py`
- `test_multiple_env.py`
- `test_sentry_integration.py`

**Destino:** `/tests/integration/`

### 7. **Scripts de Migração (ARQUIVAR)**
- `migrate_to_turso.py`
- `migrate_memory_system.py`
- `migrate_docs_to_turso.py`
- `migrar_para_uv.py`

**Destino:** `/scripts/archive/migrations/`

## 🎯 Plano de Execução

### Fase 1: Criar Estrutura no prp-agent
```bash
mkdir -p prp-agent/{integrations,diagnostics,monitoring,examples/demos}
mkdir -p tests/integration
mkdir -p scripts/archive/migrations
```

### Fase 2: Mover Scripts Essenciais
```bash
# Integrations
mv py-prp/{prp_mcp_integration.py,real_mcp_integration.py,setup_prp_database.py,cli.py} prp-agent/integrations/

# Diagnostics
mv py-prp/{diagnose_turso_mcp.py,test_turso_*.py,organize_turso_configs.py} prp-agent/diagnostics/

# Monitoring
mv py-prp/*sentry*.py prp-agent/monitoring/

# Tests
mv py-prp/test_*.py tests/integration/
```

### Fase 3: Arquivar Scripts Menos Usados
```bash
# Demos
mv py-prp/*demo*.py prp-agent/examples/demos/

# Migrations
mv py-prp/migrate*.py scripts/archive/migrations/

# Sync scripts (já temos unified)
mv py-prp/*sync*.py scripts/archive/sync-scripts/
```

### Fase 4: Limpar
```bash
# Verificar se sobrou algo importante
ls py-prp/

# Remover pasta vazia
rm -rf py-prp/
```

## ✅ Benefícios

1. **Consolidação**: Um único local para desenvolvimento PRP
2. **Organização**: Scripts categorizados por função
3. **Menos Confusão**: Elimina duplicação py-prp vs prp-agent
4. **Manutenção**: Mais fácil encontrar e manter scripts

## ⚠️ Cuidados

- Atualizar imports após mover arquivos
- Verificar dependências entre scripts
- Testar scripts principais após mudança
- Documentar nova estrutura

---
*Plano criado para consolidar desenvolvimento em prp-agent*