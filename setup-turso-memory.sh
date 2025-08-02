#!/bin/bash

# Script para configurar Turso MCP e criar estrutura de memória
echo "🔧 Configurando Turso MCP para memória..."

# Verificar se o Turso CLI está instalado
if ! command -v turso &> /dev/null; then
    echo "❌ Turso CLI não encontrado. Instalando..."
    curl -sSfL https://get.tur.so/install.sh | bash
    export PATH="$HOME/.turso:$PATH"
fi

# Verificar se está logado
if ! turso auth whoami &> /dev/null; then
    echo "🔐 Fazendo login no Turso..."
    turso auth login
fi

# Criar banco de dados para memória
echo "🗄️ Criando banco de dados para memória..."
turso db create context-memory --group default

# Obter URL e token do banco
echo "🔑 Obtendo credenciais do banco..."
DB_URL=$(turso db show context-memory --url)
DB_TOKEN=$(turso db tokens create context-memory)

echo "📝 Configurando variáveis de ambiente..."
echo "TURSO_DATABASE_URL=$DB_URL" > .env.turso
echo "TURSO_AUTH_TOKEN=$DB_TOKEN" >> .env.turso

# Criar estrutura de tabelas
echo "🏗️ Criando estrutura de tabelas..."
turso db shell context-memory << 'EOF'
-- Tabela de conversas
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_id TEXT,
    message TEXT NOT NULL,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    context TEXT,
    metadata TEXT
);

-- Tabela de base de conhecimento
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags TEXT,
    priority INTEGER DEFAULT 1
);

-- Tabela de tarefas
CREATE TABLE IF NOT EXISTS tasks (
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

-- Tabela de contextos
CREATE TABLE IF NOT EXISTS contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    data TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    project_id TEXT
);

-- Tabela de uso de ferramentas
CREATE TABLE IF NOT EXISTS tools_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    input_data TEXT,
    output_data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    success BOOLEAN DEFAULT 1,
    error_message TEXT
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_knowledge_topic ON knowledge_base(topic);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_contexts_name ON contexts(name);
CREATE INDEX IF NOT EXISTS idx_tools_timestamp ON tools_usage(timestamp);

-- Inserir dados de exemplo
INSERT OR IGNORE INTO knowledge_base (topic, content, source, tags) VALUES 
('MCP Turso', 'Model Context Protocol para Turso - banco de dados SQLite distribuído', 'documentation', 'mcp,turso,database'),
('Context Engineering', 'Técnicas para engenharia de contexto em sistemas de IA', 'research', 'ai,context,engineering'),
('Memory Systems', 'Sistemas de memória para agentes de IA e assistentes', 'research', 'memory,ai,agents');

INSERT OR IGNORE INTO contexts (name, description, data, project_id) VALUES 
('default', 'Contexto padrão do projeto', '{"project": "context-engineering-intro", "version": "1.0.0"}', 'context-engineering-intro');

EOF

echo "✅ Estrutura de memória criada com sucesso!"
echo "📊 Banco de dados: $DB_URL"
echo "🔑 Token salvo em: .env.turso"
echo ""
echo "Para usar no MCP Turso, configure as variáveis de ambiente:"
echo "export TURSO_DATABASE_URL=\"$DB_URL\""
echo "export TURSO_AUTH_TOKEN=\"$DB_TOKEN\"" 