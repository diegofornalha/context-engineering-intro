-- Script de Migração PRP para Turso
-- Gerado em: 02/08/2025
-- Inclui todas as tabelas PRP com dados de exemplo

-- =====================================================
-- TABELA PRINCIPAL: PRPs
-- =====================================================
CREATE TABLE IF NOT EXISTS prps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    objective TEXT NOT NULL,
    justification TEXT,
    
    -- Conteúdo estruturado em JSON
    context_data TEXT NOT NULL,
    implementation_details TEXT NOT NULL,
    validation_gates TEXT,
    
    -- Metadados
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'completed', 'archived')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    complexity TEXT DEFAULT 'medium' CHECK (complexity IN ('low', 'medium', 'high')),
    
    -- Relacionamentos
    parent_prp_id INTEGER,
    related_prps TEXT,
    
    -- Controle de versão
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    
    -- Busca e organização
    tags TEXT,
    search_text TEXT,
    
    FOREIGN KEY (parent_prp_id) REFERENCES prps(id)
);

-- =====================================================
-- TABELA DE TAREFAS EXTRAÍDAS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    description TEXT,
    task_type TEXT DEFAULT 'feature' CHECK (task_type IN ('feature', 'bugfix', 'refactor', 'test', 'docs', 'setup')),
    
    -- Prioridade e estimativa
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    estimated_hours REAL,
    complexity TEXT DEFAULT 'medium' CHECK (complexity IN ('low', 'medium', 'high')),
    
    -- Status e progresso
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'review', 'completed', 'blocked')),
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    
    -- Dependências
    dependencies TEXT,
    blockers TEXT,
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to TEXT,
    completed_at TIMESTAMP,
    
    -- Contexto específico da tarefa
    context_files TEXT,
    acceptance_criteria TEXT,
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE CONTEXTO E ARQUIVOS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    context_type TEXT NOT NULL CHECK (context_type IN ('file', 'directory', 'library', 'api', 'example', 'reference')),
    
    -- Informações do contexto
    name TEXT NOT NULL,
    path TEXT,
    content TEXT,
    version TEXT,
    
    -- Metadados
    importance TEXT DEFAULT 'medium' CHECK (importance IN ('low', 'medium', 'high', 'critical')),
    is_required BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE TAGS E CATEGORIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    color TEXT DEFAULT '#007bff',
    category TEXT DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELA DE RELACIONAMENTO PRP-TAGS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_tag_relations (
    prp_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (prp_id, tag_id),
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES prp_tags(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE HISTÓRICO E VERSIONAMENTO
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('created', 'updated', 'status_changed', 'archived')),
    
    -- Dados da versão
    old_data TEXT,
    new_data TEXT,
    changes_summary TEXT,
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    comment TEXT,
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE ANÁLISES LLM
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_llm_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    analysis_type TEXT NOT NULL CHECK (analysis_type IN ('task_extraction', 'complexity_assessment', 'dependency_analysis', 'validation_check')),
    
    -- Resultado da análise
    input_content TEXT NOT NULL,
    output_content TEXT NOT NULL,
    parsed_data TEXT,
    
    -- Metadados da análise
    model_used TEXT,
    tokens_used INTEGER,
    processing_time_ms INTEGER,
    confidence_score REAL,
    
    -- Status
    status TEXT DEFAULT 'completed' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================

-- Índices para busca rápida
CREATE INDEX IF NOT EXISTS idx_prps_status ON prps(status);
CREATE INDEX IF NOT EXISTS idx_prps_priority ON prps(priority);
CREATE INDEX IF NOT EXISTS idx_prps_created_at ON prps(created_at);
CREATE INDEX IF NOT EXISTS idx_prps_search_text ON prps(search_text);

-- Índices para relacionamentos
CREATE INDEX IF NOT EXISTS idx_prp_tasks_prp_id ON prp_tasks(prp_id);
CREATE INDEX IF NOT EXISTS idx_prp_tasks_status ON prp_tasks(status);
CREATE INDEX IF NOT EXISTS idx_prp_tasks_assigned_to ON prp_tasks(assigned_to);

CREATE INDEX IF NOT EXISTS idx_prp_context_prp_id ON prp_context(prp_id);
CREATE INDEX IF NOT EXISTS idx_prp_context_type ON prp_context(context_type);

CREATE INDEX IF NOT EXISTS idx_prp_history_prp_id ON prp_history(prp_id);
CREATE INDEX IF NOT EXISTS idx_prp_history_version ON prp_history(version);

CREATE INDEX IF NOT EXISTS idx_prp_llm_analysis_prp_id ON prp_llm_analysis(prp_id);
CREATE INDEX IF NOT EXISTS idx_prp_llm_analysis_type ON prp_llm_analysis(analysis_type);

-- =====================================================
-- TRIGGERS PARA AUTOMAÇÃO
-- =====================================================

-- Trigger para atualizar updated_at automaticamente
CREATE TRIGGER IF NOT EXISTS trigger_prps_updated_at
    AFTER UPDATE ON prps
    FOR EACH ROW
BEGIN
    UPDATE prps SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para atualizar updated_at em tarefas
CREATE TRIGGER IF NOT EXISTS trigger_prp_tasks_updated_at
    AFTER UPDATE ON prp_tasks
    FOR EACH ROW
BEGIN
    UPDATE prp_tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- =====================================================
-- VIEWS ÚTEIS
-- =====================================================

-- View para PRPs com contagem de tarefas
CREATE VIEW IF NOT EXISTS v_prps_with_task_count AS
SELECT 
    p.*,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as in_progress_tasks,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending_tasks
FROM prps p
LEFT JOIN prp_tasks t ON p.id = t.prp_id
GROUP BY p.id;

-- View para PRPs com tags
CREATE VIEW IF NOT EXISTS v_prps_with_tags AS
SELECT 
    p.*,
    GROUP_CONCAT(t.name) as tag_names,
    GROUP_CONCAT(t.color) as tag_colors
FROM prps p
LEFT JOIN prp_tag_relations ptr ON p.id = ptr.prp_id
LEFT JOIN prp_tags t ON ptr.tag_id = t.id
GROUP BY p.id;

-- View para análise de progresso
CREATE VIEW IF NOT EXISTS v_prp_progress AS
SELECT 
    p.id,
    p.name,
    p.title,
    p.status as prp_status,
    COUNT(t.id) as total_tasks,
    AVG(t.progress) as avg_task_progress,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
    ROUND(
        (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) * 100.0) / 
        COUNT(t.id), 2
    ) as completion_percentage
FROM prps p
LEFT JOIN prp_tasks t ON p.id = t.prp_id
GROUP BY p.id;

-- =====================================================
-- DADOS INICIAIS
-- =====================================================

-- Inserir tags padrão
INSERT OR IGNORE INTO prp_tags (name, description, color, category) VALUES
('frontend', 'Desenvolvimento frontend', '#007bff', 'technology'),
('backend', 'Desenvolvimento backend', '#28a745', 'technology'),
('database', 'Operações de banco de dados', '#ffc107', 'technology'),
('api', 'Desenvolvimento de APIs', '#17a2b8', 'technology'),
('testing', 'Testes e qualidade', '#6f42c1', 'process'),
('documentation', 'Documentação', '#fd7e14', 'process'),
('security', 'Segurança e autenticação', '#dc3545', 'security'),
('performance', 'Otimização de performance', '#20c997', 'quality'),
('ui/ux', 'Interface e experiência do usuário', '#e83e8c', 'design'),
('devops', 'DevOps e infraestrutura', '#6c757d', 'infrastructure'),
('mcp', 'Model Context Protocol', '#6f42c1', 'technology'),
('llm', 'Large Language Models', '#e83e8c', 'ai');

-- Inserir PRPs de exemplo
INSERT OR IGNORE INTO prps (
    name, 
    title, 
    description, 
    objective,
    context_data,
    implementation_details,
    validation_gates,
    status,
    priority,
    tags,
    search_text,
    created_by
) VALUES 
(
    'mcp-prp-server',
    'Servidor MCP para Análise de PRPs',
    'Implementar um servidor MCP que analisa Product Requirement Prompts e extrai tarefas usando LLM',
    'Criar uma versão simples do taskmaster MCP que analisa PRPs em vez de PRDs',
    '{"files": ["src/index.ts", "src/tools/register-tools.ts"], "libraries": ["@modelcontextprotocol/sdk", "zod"], "examples": ["examples/database-tools.ts"]}',
    '{"architecture": "Cloudflare Workers", "authentication": "GitHub OAuth", "database": "PostgreSQL", "llm": "Anthropic Claude"}',
    '{"tests": "pytest", "linting": "ruff", "type_check": "TypeScript"}',
    'active',
    'high',
    '["backend", "api", "mcp", "llm"]',
    'servidor MCP análise PRPs taskmaster LLM Anthropic Cloudflare Workers GitHub OAuth PostgreSQL',
    'system'
),
(
    'turso-prp-dashboard',
    'Dashboard Web para Visualização de PRPs',
    'Interface web moderna para visualizar e gerenciar PRPs armazenados no Turso',
    'Criar uma interface intuitiva para navegar pelos PRPs e suas tarefas extraídas',
    '{"files": ["src/components/PRPList.tsx", "src/components/TaskView.tsx"], "libraries": ["react", "tailwindcss", "lucide-react"]}',
    '{"framework": "Next.js 14", "styling": "Tailwind CSS", "database": "Turso", "deployment": "Vercel"}',
    '{"tests": "jest", "linting": "eslint", "type_check": "TypeScript"}',
    'active',
    'medium',
    '["frontend", "ui/ux", "database"]',
    'dashboard web visualização PRPs interface moderna Turso Next.js Tailwind',
    'system'
),
(
    'prp-llm-analyzer',
    'Analisador LLM para Extração de Tarefas',
    'Sistema que usa LLMs para analisar PRPs e extrair tarefas automaticamente',
    'Automatizar a extração de tarefas a partir de PRPs usando análise de linguagem natural',
    '{"files": ["src/analyzer.py", "src/prompts.py"], "libraries": ["openai", "anthropic", "pydantic"]}',
    '{"llm_provider": "Anthropic Claude", "framework": "FastAPI", "database": "Turso", "caching": "Redis"}',
    '{"tests": "pytest", "linting": "ruff", "validation": "pydantic"}',
    'draft',
    'high',
    '["backend", "llm", "api", "ai"]',
    'analisador LLM extração tarefas automatização linguagem natural Anthropic Claude FastAPI',
    'system'
);

-- Inserir tarefas para o PRP principal
INSERT OR IGNORE INTO prp_tasks (prp_id, task_name, description, task_type, priority, estimated_hours, status, progress, assigned_to) VALUES
(1, 'Configurar projeto base', 'Criar estrutura inicial do projeto MCP com TypeScript', 'setup', 'high', 2.0, 'completed', 100, 'dev'),
(1, 'Implementar autenticação GitHub', 'Configurar OAuth com GitHub para autenticação', 'feature', 'high', 4.0, 'in_progress', 60, 'dev'),
(1, 'Criar endpoint de análise PRP', 'Endpoint que recebe PRP e retorna tarefas extraídas', 'feature', 'critical', 6.0, 'pending', 0, 'dev'),
(1, 'Integrar com LLM Claude', 'Configurar integração com Anthropic Claude para análise', 'feature', 'high', 3.0, 'pending', 0, 'dev'),
(1, 'Implementar cache Redis', 'Adicionar cache para otimizar chamadas ao LLM', 'feature', 'medium', 2.0, 'pending', 0, 'dev'),
(1, 'Criar testes unitários', 'Implementar suite de testes para todas as funcionalidades', 'test', 'medium', 4.0, 'pending', 0, 'qa'),
(1, 'Documentar API', 'Criar documentação completa da API', 'docs', 'low', 2.0, 'pending', 0, 'dev');

-- Inserir tarefas para o dashboard
INSERT OR IGNORE INTO prp_tasks (prp_id, task_name, description, task_type, priority, estimated_hours, status, progress, assigned_to) VALUES
(2, 'Criar layout base', 'Implementar layout responsivo com Tailwind CSS', 'feature', 'high', 3.0, 'completed', 100, 'frontend'),
(2, 'Componente de lista de PRPs', 'Criar componente para exibir lista de PRPs', 'feature', 'high', 4.0, 'in_progress', 80, 'frontend'),
(2, 'Visualização de tarefas', 'Componente para mostrar tarefas de um PRP', 'feature', 'medium', 3.0, 'pending', 0, 'frontend'),
(2, 'Filtros e busca', 'Implementar filtros por status, prioridade e busca', 'feature', 'medium', 2.0, 'pending', 0, 'frontend'),
(2, 'Integração com Turso', 'Conectar frontend com banco Turso', 'feature', 'critical', 3.0, 'pending', 0, 'backend'),
(2, 'Deploy na Vercel', 'Configurar deploy automático na Vercel', 'setup', 'low', 1.0, 'pending', 0, 'devops');

-- Inserir contexto para os PRPs
INSERT OR IGNORE INTO prp_context (prp_id, context_type, name, path, content, importance) VALUES
(1, 'file', 'src/index.ts', 'src/index.ts', 'Arquivo principal do servidor MCP', 'critical'),
(1, 'file', 'src/tools/register-tools.ts', 'src/tools/register-tools.ts', 'Registro de ferramentas MCP', 'high'),
(1, 'library', '@modelcontextprotocol/sdk', NULL, 'SDK oficial do MCP', 'critical'),
(1, 'library', 'zod', NULL, 'Validação de schemas', 'high'),
(2, 'file', 'src/components/PRPList.tsx', 'src/components/PRPList.tsx', 'Componente de lista de PRPs', 'critical'),
(2, 'file', 'src/components/TaskView.tsx', 'src/components/TaskView.tsx', 'Visualização de tarefas', 'high'),
(2, 'library', 'react', NULL, 'Framework React', 'critical'),
(2, 'library', 'tailwindcss', NULL, 'Framework CSS', 'high');

-- Inserir relacionamentos de tags
INSERT OR IGNORE INTO prp_tag_relations (prp_id, tag_id) VALUES
(1, (SELECT id FROM prp_tags WHERE name = 'backend')),
(1, (SELECT id FROM prp_tags WHERE name = 'api')),
(1, (SELECT id FROM prp_tags WHERE name = 'mcp')),
(1, (SELECT id FROM prp_tags WHERE name = 'llm')),
(2, (SELECT id FROM prp_tags WHERE name = 'frontend')),
(2, (SELECT id FROM prp_tags WHERE name = 'ui/ux')),
(2, (SELECT id FROM prp_tags WHERE name = 'database')),
(3, (SELECT id FROM prp_tags WHERE name = 'backend')),
(3, (SELECT id FROM prp_tags WHERE name = 'llm')),
(3, (SELECT id FROM prp_tags WHERE name = 'api')),
(3, (SELECT id FROM prp_tags WHERE name = 'ai'));

-- Inserir análise LLM de exemplo
INSERT OR IGNORE INTO prp_llm_analysis (
    prp_id, 
    analysis_type, 
    input_content, 
    output_content, 
    parsed_data,
    model_used,
    tokens_used,
    processing_time_ms,
    confidence_score,
    created_by
) VALUES (
    1,
    'task_extraction',
    'Implementar um servidor MCP que analisa Product Requirement Prompts e extrai tarefas usando LLM',
    'Tarefas extraídas: 1. Configurar projeto base, 2. Implementar autenticação, 3. Criar endpoint de análise, 4. Integrar com LLM',
    '{"tasks": [{"name": "Configurar projeto base", "type": "setup", "priority": "high"}, {"name": "Implementar autenticação", "type": "feature", "priority": "high"}]}',
    'claude-3-sonnet',
    150,
    2500,
    0.95,
    'system'
);