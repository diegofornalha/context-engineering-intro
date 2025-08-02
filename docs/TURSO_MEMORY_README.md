# 🧠 Sistema de Memória Turso MCP

## 📋 Visão Geral

Este projeto implementa um sistema de memória persistente usando o **Turso Database** (SQLite distribuído) e o **Model Context Protocol (MCP)**. O sistema permite que agentes de IA mantenham memória de longo prazo, incluindo conversas, conhecimento, tarefas e contextos.

## 🏗️ Arquitetura

### Banco de Dados
- **Turso Database**: SQLite distribuído na nuvem
- **URL**: `libsql://context-memory-diegofornalha.aws-us-east-1.turso.io`
- **Região**: AWS US East 1

### Tabelas Principais

#### 1. `conversations` - Histórico de Conversas
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_id TEXT,
    message TEXT NOT NULL,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    context TEXT,
    metadata TEXT
);
```

#### 2. `knowledge_base` - Base de Conhecimento
```sql
CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags TEXT,
    priority INTEGER DEFAULT 1
);
```

#### 3. `tasks` - Gerenciamento de Tarefas
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    priority INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    context TEXT,
    assigned_to TEXT
);
```

#### 4. `contexts` - Contextos de Projeto
```sql
CREATE TABLE contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    data TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    project_id TEXT
);
```

#### 5. `tools_usage` - Log de Uso de Ferramentas
```sql
CREATE TABLE tools_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    input_data TEXT,
    output_data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    success BOOLEAN DEFAULT 1,
    error_message TEXT
);
```

## 🚀 Configuração

### 1. Instalar Turso CLI
```bash
curl -sSfL https://get.tur.so/install.sh | bash
export PATH="$HOME/.turso:$PATH"
```

### 2. Fazer Login
```bash
turso auth login
```

### 3. Configurar Banco de Dados
```bash
# Criar banco de dados
turso db create context-memory --group default

# Obter URL e token
DB_URL=$(turso db show context-memory --url)
DB_TOKEN=$(turso db tokens create context-memory)

# Configurar variáveis de ambiente
export TURSO_DATABASE_URL="$DB_URL"
export TURSO_AUTH_TOKEN="$DB_TOKEN"
```

### 4. Executar Script de Configuração
```bash
chmod +x setup-turso-memory.sh
./setup-turso-memory.sh
```

## 🛠️ Uso

### Via MCP Turso

O MCP Turso fornece as seguintes ferramentas:

#### Ferramentas Básicas
- `turso_list_databases` - Listar bancos de dados
- `turso_execute_query` - Executar consultas SQL
- `turso_list_tables` - Listar tabelas
- `turso_describe_table` - Descrever estrutura de tabela

#### Ferramentas de Memória
- `turso_add_conversation` - Adicionar conversa
- `turso_get_conversations` - Recuperar conversas
- `turso_add_knowledge` - Adicionar conhecimento
- `turso_search_knowledge` - Pesquisar conhecimento

### Via Python

```python
from memory_demo import TursoMemorySystem

# Inicializar sistema
memory = TursoMemorySystem(
    database_url="libsql://context-memory-diegofornalha.aws-us-east-1.turso.io",
    auth_token="seu-token-aqui"
)

# Adicionar conversa
memory.add_conversation(
    session_id="sessao-1",
    message="Olá!",
    response="Olá! Como posso ajudar?",
    user_id="usuario-1"
)

# Pesquisar conhecimento
knowledge = memory.search_knowledge("Python", tags="programming")

# Adicionar tarefa
memory.add_task(
    title="Implementar feature X",
    description="Desenvolver nova funcionalidade",
    priority=1
)
```

## 📊 Demonstração

Execute a demonstração completa:

```bash
python3 memory_demo.py
```

A demonstração inclui:
- ✅ Adição de conversas
- ✅ Recuperação de histórico
- ✅ Gerenciamento de conhecimento
- ✅ Pesquisa na base de conhecimento
- ✅ Criação e listagem de tarefas

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
context-engineering-intro/
├── mcp-turso/                 # Servidor MCP Turso
│   ├── src/index.ts          # Código principal
│   ├── package.json          # Dependências
│   └── start.sh              # Script de inicialização
├── setup-turso-memory.sh     # Script de configuração
├── memory_demo.py            # Demonstração Python
├── .env.turso               # Configurações do Turso
└── TURSO_MEMORY_README.md   # Esta documentação
```

### Compilar MCP Turso
```bash
cd mcp-turso
npm install
npm run build
```

### Executar MCP Turso
```bash
cd mcp-turso
./start.sh
```

## 🎯 Casos de Uso

### 1. Chatbot com Memória
```python
# Manter contexto entre conversas
conversations = memory.get_conversations(session_id="user-123", limit=5)
context = "Histórico: " + "\n".join([c['message'] for c in conversations])
```

### 2. Base de Conhecimento
```python
# Adicionar conhecimento aprendido
memory.add_knowledge(
    topic="Configuração Docker",
    content="Docker é uma plataforma para desenvolvimento...",
    source="documentation",
    tags="docker,devops,containers"
)

# Pesquisar quando necessário
results = memory.search_knowledge("Docker", tags="devops")
```

### 3. Gerenciamento de Projetos
```python
# Criar tarefas
memory.add_task(
    title="Implementar autenticação",
    description="Adicionar sistema de login",
    priority=1,
    context="projeto-web"
)

# Acompanhar progresso
tasks = memory.get_tasks(status="pending")
```

### 4. Log de Ferramentas
```python
# Registrar uso de ferramentas
memory.add_tool_usage(
    tool_name="file_search",
    input_data={"query": "config"},
    output_data={"files": ["config.json"]},
    session_id="sessao-1"
)
```

## 🔒 Segurança

- **Autenticação**: Tokens JWT para acesso ao banco
- **Isolamento**: Cada projeto pode ter seu próprio banco
- **Backup**: Turso fornece backup automático
- **Auditoria**: Log de todas as operações

## 📈 Performance

- **Latência**: < 10ms para consultas simples
- **Escalabilidade**: Distribuído globalmente
- **Concorrência**: Suporte a múltiplas conexões
- **Cache**: Cache automático do Turso

## 🚨 Limitações Atuais

1. **MCP Turso**: Problemas de compatibilidade com Claude Code via stdio
2. **Autenticação**: Necessário configurar tokens manualmente
3. **Conectividade**: Dependência de conexão com internet

## 🔮 Próximos Passos

1. **Resolver compatibilidade MCP**: Migrar para servidor HTTP
2. **Interface Web**: Criar dashboard para visualização
3. **Integração CrewAI**: Adicionar suporte nativo ao CrewAI
4. **Backup automático**: Implementar backup local
5. **Análise avançada**: Adicionar analytics e insights

## 📞 Suporte

Para dúvidas ou problemas:
- Verificar logs do Turso: `turso db logs context-memory`
- Testar conexão: `turso db shell context-memory`
- Consultar documentação: [Turso Docs](https://docs.tur.so)

---

**Status**: ✅ Funcional - Sistema de memória operacional com demonstração completa
**Última atualização**: 2025-08-02
**Versão**: 1.0.0 