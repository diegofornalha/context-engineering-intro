
-- Script de Migração para Turso
-- Gerado em: 02/08/2025 04:27
-- Total de registros: 10 erros, 2 projetos, 2 problemas MCP

-- Criar tabelas no Turso
CREATE TABLE IF NOT EXISTS sentry_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    error_title TEXT NOT NULL,
    error_level TEXT NOT NULL,
    event_count INTEGER DEFAULT 1,
    status TEXT DEFAULT 'unresolved',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sentry_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT UNIQUE NOT NULL,
    issue_count INTEGER DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mcp_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mcp_name TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME NULL
);

-- Inserir projetos
INSERT OR REPLACE INTO sentry_projects (project_name, issue_count, last_updated) VALUES ('coflow', 10, '2025-08-02 04:27:24.375556');
INSERT OR REPLACE INTO sentry_projects (project_name, issue_count, last_updated) VALUES ('mcp-test-project', 0, '2025-08-02 04:27:24.378609');

-- Inserir erros do Sentry
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Error: This is your first error!', 'error', 1, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Session will end abnormally', 'warning', 2, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Error: Teste de captura de exceção via MCP Sentry', 'warning', 2, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Teste do MCP - 20250802-020905', 'info', 1, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Teste do MCP Sentry funcionando perfeitamente no Cursor Agent! 🎉', 'info', 1, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Teste do MCP Standalone - Sat Aug 2 00:59:45 -03 2025', 'info', 3, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Teste de validação do MCP Sentry - Credenciais funcionando perfeitamente!', 'info', 1, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Teste finalizado com sucesso - MCP Sentry funcionando corretamente', 'info', 1, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Teste inicial do MCP Sentry no Claude Code', 'info', 1, 'unresolved', '2025-08-02 07:27:24');
INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('coflow', 'Test message from React app', 'info', 1, 'unresolved', '2025-08-02 07:27:24');

-- Inserir problemas de MCP
INSERT INTO mcp_issues (mcp_name, issue_type, description, status, created_at) VALUES ('Turso', 'authentication', 'Erro de autenticação JWT: ''could not parse jwt id'' - Impossibilidade de acessar bancos de dados', 'open', '2025-08-02 07:27:24');
INSERT INTO mcp_issues (mcp_name, issue_type, description, status, created_at) VALUES ('Sentry', 'cleanup_needed', 'Muitos testes antigos no sistema de produção - Necessário limpeza', 'open', '2025-08-02 07:27:24');
