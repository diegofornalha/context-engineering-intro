# 🚀 Scripts MCP Turso

Scripts para gerenciamento e sincronização de conhecimento do Turso Agent.

## 📁 Scripts Disponíveis

### 🔄 Sincronização de Conhecimento

#### `sync-turso-knowledge.py`
- **Função**: Sincronização completa de conhecimento via SQLite local
- **Uso**: `python3 sync-turso-knowledge.py`
- **Recursos**:
  - Escaneia arquivos `docs-turso/`
  - Detecta mudanças via hash MD5
  - Atualiza/insere conhecimento no banco
  - Remove registros obsoletos (>30 dias)
  - Valida integridade dos dados

#### `sync-turso-knowledge-mcp.py`
- **Função**: Sincronização via MCP Turso (simulação)
- **Uso**: `python3 sync-turso-knowledge-mcp.py`
- **Recursos**:
  - Usa MCP Turso para operações
  - Simula integração com banco remoto
  - Extrai conhecimento de arquivos
  - Gera relatórios de sync

#### `sync-knowledge-via-mcp.py`
- **Função**: Scan e preparação para MCP Turso
- **Uso**: `python3 sync-knowledge-via-mcp.py`
- **Recursos**:
  - Escaneia arquivos docs-turso
  - Extrai conhecimento estruturado
  - Prepara comandos MCP Turso
  - Gera relatórios de análise

### 🤖 Automação

#### `auto-sync-knowledge.sh`
- **Função**: Script de automação de sincronização
- **Uso**: `./auto-sync-knowledge.sh [comando]`
- **Comandos**:
  - `sync` - Forçar sync agora
  - `auto` - Sync automático (a cada 6h)
  - `status` - Mostrar status do sistema
  - `integrity` - Verificar integridade
  - `cleanup` - Limpar logs antigos

## 🛠️ Configuração

### Pré-requisitos
```bash
# Python 3.8+
python3 --version

# Dependências Python
pip install sqlite3 hashlib glob datetime json

# Permissões de execução
chmod +x *.sh
```

### Estrutura de Arquivos
```
mcp-turso/scripts/
├── README.md                    # Esta documentação
├── sync-turso-knowledge.py      # Sync via SQLite local
├── sync-turso-knowledge-mcp.py  # Sync via MCP (simulação)
├── sync-knowledge-via-mcp.py    # Scan e preparação
└── auto-sync-knowledge.sh       # Automação
```

## 🚀 Uso Rápido

### 1. Scan de Conhecimento
```bash
cd mcp-turso/scripts
python3 sync-knowledge-via-mcp.py
```

### 2. Sincronização Manual
```bash
cd mcp-turso/scripts
python3 sync-turso-knowledge.py
```

### 3. Automação
```bash
cd mcp-turso/scripts
./auto-sync-knowledge.sh auto
```

## 📊 Monitoramento

### Status do Sistema
```bash
./auto-sync-knowledge.sh status
```

### Verificar Integridade
```bash
./auto-sync-knowledge.sh integrity
```

### Logs
```bash
# Ver logs recentes
ls -la ../logs/sync_*.log

# Ver último sync
cat ../logs/last_sync.txt
```

## 🔧 Integração com MCP Turso

### Comandos MCP Disponíveis
```python
# Verificar conhecimento existente
mcp_turso_execute_read_only_query(
    query="SELECT COUNT(*) FROM turso_agent_knowledge",
    database="context-memory"
)

# Inserir novo conhecimento
mcp_turso_execute_query(
    query="INSERT INTO turso_agent_knowledge (...) VALUES (...)",
    database="context-memory"
)

# Verificar obsoletos
mcp_turso_execute_read_only_query(
    query="SELECT * FROM turso_agent_knowledge WHERE updated_at < datetime('now', '-30 days')",
    database="context-memory"
)
```

## 📈 Relatórios

### Relatórios Gerados
- `sync_report_YYYYMMDD_HHMMSS.txt` - Relatório de sincronização
- `../logs/sync_YYYYMMDD_HHMMSS.log` - Log detalhado
- `../logs/last_sync.txt` - Timestamp do último sync

### Exemplo de Relatório
```
🔄 RELATÓRIO DE SINCRONIZAÇÃO VIA MCP
==================================================

📊 RESULTADOS:
• Arquivos escaneados: 7
• Conhecimento extraído: 7
• Registros atualizados: 0
• Novos registros: 0

📝 ARQUIVOS PROCESSADOS:
• docs-turso/RESUMO_FINAL_TURSO_SENTRY.md
• docs-turso/configuration/TURSO_CONFIGURATION_SUMMARY.md
• docs-turso/documentation/GUIA_COMPLETO_TURSO_MCP.md
...

⏰ Timestamp: 2025-08-02 20:11:14
✅ Sincronização concluída!
```

## 🔄 Cronograma de Sincronização

### Automático
- **Frequência**: A cada 6 horas
- **Condição**: Se último sync > 6h atrás
- **Comando**: `./auto-sync-knowledge.sh auto`

### Manual
- **Forçar sync**: `./auto-sync-knowledge.sh sync`
- **Ver status**: `./auto-sync-knowledge.sh status`
- **Limpar logs**: `./auto-sync-knowledge.sh cleanup`

## 🛡️ Segurança

### Validações
- ✅ Verificação de integridade dos dados
- ✅ Detecção de registros duplicados
- ✅ Validação de conteúdo vazio
- ✅ Verificação de tags obrigatórias

### Backup
- ✅ Backup automático antes de sync
- ✅ Logs de todas as operações
- ✅ Rollback em caso de erro

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de Permissão
```bash
chmod +x *.sh
```

#### 2. Python não encontrado
```bash
# Verificar Python
python3 --version

# Instalar dependências
pip install -r requirements.txt
```

#### 3. Banco não encontrado
```bash
# Verificar se o banco existe
ls -la ../context-memory.db

# Criar banco se necessário
touch ../context-memory.db
```

#### 4. Lock file travado
```bash
# Remover lock file
rm -f ../logs/sync.lock
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs em `../logs/`
2. Executar `./auto-sync-knowledge.sh status`
3. Verificar integridade com `./auto-sync-knowledge.sh integrity`

---

**Status**: ✅ Funcional  
**Última atualização**: 2025-08-02  
**Versão**: 1.0.0 