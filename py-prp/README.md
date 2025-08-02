# 🔧 py-prp - Scripts de Integração PRP

## 📋 Visão Geral

Coleção de scripts Python para integração de sistemas PRP (Product Requirement Prompts) com bancos de dados e serviços.

## 🎯 Principais Funcionalidades

### 1. **Integração com Turso Database**
- `prp_mcp_integration.py` - Integração PRP com MCP Turso
- `setup_prp_database.py` - Configuração inicial do banco
- `migrate_to_turso.py` - Scripts de migração

### 2. **Sistema de Memória**
- `memory_demo.py` - Demonstração do sistema de memória
- `test_memory_system.py` - Testes de memória persistente
- `migrate_memory_system.py` - Migração de dados de memória

### 3. **Sincronização de Documentos**
- `sync_docs_automatico.py` - Sincronização automática
- `mcp_smart_sync.py` - Sync inteligente com detecção de mudanças
- `reorganizar_clusters_final.py` - Organização em clusters

### 4. **Ferramentas de Diagnóstico**
- `diagnose_turso_mcp.py` - Diagnóstico de problemas MCP
- `test_turso_token.py` - Validação de tokens
- `organize_turso_configs.py` - Organização de configurações

## 🚀 Como Usar

### Instalação de Dependências
```bash
pip install python-dotenv pydantic aiohttp
```

### Exemplo de Uso
```python
from prp_mcp_integration import MCPTursoClient

# Criar cliente
client = MCPTursoClient(database="context-memory")

# Armazenar PRP
await client.store_prp(prp_data)

# Buscar PRPs
prps = await client.search_prps("authentication")
```

## 🔗 Integração com prp-agent

Estes scripts são projetados para trabalhar com agentes criados usando o framework `prp-agent`:

1. Agentes usam estes scripts para persistência
2. Scripts fornecem integração com bancos de dados
3. Sistema completo: Agente + Persistência

## 📁 Estrutura

```
py-prp/
├── Integração/
│   ├── prp_mcp_integration.py
│   ├── real_mcp_integration.py
│   └── setup_prp_database.py
├── Memória/
│   ├── memory_demo.py
│   ├── test_memory_system.py
│   └── migrate_memory_system.py
├── Sincronização/
│   ├── sync_docs_automatico.py
│   ├── mcp_smart_sync.py
│   └── reorganizar_clusters_final.py
└── Diagnóstico/
    ├── diagnose_turso_mcp.py
    ├── test_turso_token.py
    └── organize_turso_configs.py
```

## 🔧 Configuração

Crie um arquivo `.env` com:
```env
TURSO_DATABASE_URL=your-database-url
TURSO_AUTH_TOKEN=your-auth-token
```

## 📚 Documentação Relacionada

- [PRP System Guide](/docs/04-prp-system/)
- [Turso Integration](/docs/03-turso-database/)
- [MCP Integration](/docs/02-mcp-integration/)