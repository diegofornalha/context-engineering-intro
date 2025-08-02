-- Script Completo de Migração PRP para Turso
-- Data: 02/08/2025
-- Inclui todas as tabelas PRP com dados completos

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
GROUP BY p.id
ORDER BY completion_percentage DESC;

-- =====================================================
-- DADOS COMPLETOS
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
('llm', 'Large Language Models', '#e83e8c', 'ai'),
('ai', 'Inteligência Artificial', '#e83e8c', 'technology'),
('automation', 'Automação de processos', '#20c997', 'process'),
('collaboration', 'Colaboração em tempo real', '#17a2b8', 'feature'),
('realtime', 'Comunicação em tempo real', '#fd7e14', 'technology'),
('analytics', 'Análise de dados', '#6f42c1', 'data'),
('ml', 'Machine Learning', '#dc3545', 'ai'),
('data', 'Processamento de dados', '#28a745', 'data'),
('dashboard', 'Dashboards e visualizações', '#ffc107', 'ui');

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
),
(
    'prp-task-extractor',
    'Extrator Automático de Tarefas de PRPs',
    'Sistema que analisa PRPs e extrai automaticamente tarefas usando IA',
    'Automatizar completamente o processo de extração de tarefas de PRPs',
    '{"files": ["src/extractor.py", "src/models.py"], "libraries": ["openai", "pydantic", "fastapi"], "examples": ["examples/prp_analysis.py"]}',
    '{"framework": "FastAPI", "ai_provider": "OpenAI GPT-4", "database": "PostgreSQL", "queue": "Celery"}',
    '{"tests": "pytest", "linting": "ruff", "validation": "pydantic", "coverage": "90%"}',
    'active',
    'critical',
    '["backend", "ai", "api", "automation"]',
    'extrator automático tarefas PRPs IA OpenAI GPT-4 FastAPI PostgreSQL Celery',
    'system'
),
(
    'prp-collaboration-platform',
    'Plataforma de Colaboração para PRPs',
    'Sistema web para equipes colaborarem na criação e revisão de PRPs',
    'Facilitar a colaboração em tempo real na criação de PRPs',
    '{"files": ["src/components/Editor.tsx", "src/hooks/useCollaboration.ts"], "libraries": ["react", "socket.io", "quill"], "examples": ["examples/collaboration.js"]}',
    '{"framework": "Next.js", "realtime": "Socket.io", "editor": "Quill", "auth": "NextAuth"}',
    '{"tests": "jest", "linting": "eslint", "e2e": "playwright"}',
    'draft',
    'medium',
    '["frontend", "collaboration", "realtime", "ui/ux"]',
    'plataforma colaboração PRPs tempo real Socket.io Quill NextAuth',
    'system'
),
(
    'prp-analytics-dashboard',
    'Dashboard de Analytics para PRPs',
    'Sistema de métricas e analytics para acompanhar performance de PRPs',
    'Fornecer insights sobre eficiência e qualidade dos PRPs',
    '{"files": ["src/analytics.py", "src/metrics.py"], "libraries": ["pandas", "plotly", "scikit-learn"], "examples": ["examples/analytics.ipynb"]}',
    '{"framework": "Streamlit", "analytics": "Plotly", "ml": "scikit-learn", "database": "ClickHouse"}',
    '{"tests": "pytest", "validation": "pandas", "performance": "load testing"}',
    'active',
    'high',
    '["analytics", "ml", "data", "dashboard"]',
    'dashboard analytics PRPs métricas performance Plotly scikit-learn Streamlit',
    'system'
);

-- Inserir todas as tarefas
INSERT OR IGNORE INTO prp_tasks (prp_id, task_name, description, task_type, priority, estimated_hours, status, progress, assigned_to) VALUES
-- Tarefas para mcp-prp-server
(1, 'Configurar projeto base', 'Criar estrutura inicial do projeto MCP com TypeScript', 'setup', 'high', 2.0, 'completed', 100, 'dev'),
(1, 'Implementar autenticação GitHub', 'Configurar OAuth com GitHub para autenticação', 'feature', 'high', 4.0, 'in_progress', 60, 'dev'),
(1, 'Criar endpoint de análise PRP', 'Endpoint que recebe PRP e retorna tarefas extraídas', 'feature', 'critical', 6.0, 'pending', 0, 'dev'),
(1, 'Integrar com LLM Claude', 'Configurar integração com Anthropic Claude para análise', 'feature', 'high', 3.0, 'pending', 0, 'dev'),
(1, 'Implementar cache Redis', 'Adicionar cache para otimizar chamadas ao LLM', 'feature', 'medium', 2.0, 'pending', 0, 'dev'),
(1, 'Criar testes unitários', 'Implementar suite de testes para todas as funcionalidades', 'test', 'medium', 4.0, 'pending', 0, 'qa'),
(1, 'Documentar API', 'Criar documentação completa da API', 'docs', 'low', 2.0, 'pending', 0, 'dev'),

-- Tarefas para turso-prp-dashboard
(2, 'Criar layout base', 'Implementar layout responsivo com Tailwind CSS', 'feature', 'high', 3.0, 'completed', 100, 'frontend'),
(2, 'Componente de lista de PRPs', 'Criar componente para exibir lista de PRPs', 'feature', 'high', 4.0, 'in_progress', 80, 'frontend'),
(2, 'Visualização de tarefas', 'Componente para mostrar tarefas de um PRP', 'feature', 'medium', 3.0, 'pending', 0, 'frontend'),
(2, 'Filtros e busca', 'Implementar filtros por status, prioridade e busca', 'feature', 'medium', 2.0, 'pending', 0, 'frontend'),
(2, 'Integração com Turso', 'Conectar frontend com banco Turso', 'feature', 'critical', 3.0, 'pending', 0, 'backend'),
(2, 'Deploy na Vercel', 'Configurar deploy automático na Vercel', 'setup', 'low', 1.0, 'pending', 0, 'devops'),

-- Tarefas para prp-task-extractor
(4, 'Configurar ambiente FastAPI', 'Criar estrutura base do projeto FastAPI', 'setup', 'high', 2.0, 'completed', 100, 'backend'),
(4, 'Implementar modelo de dados', 'Criar modelos Pydantic para PRPs e tarefas', 'feature', 'high', 3.0, 'in_progress', 70, 'backend'),
(4, 'Integrar OpenAI GPT-4', 'Configurar integração com OpenAI para análise', 'feature', 'critical', 4.0, 'pending', 0, 'ai'),
(4, 'Criar pipeline de processamento', 'Implementar fila de processamento com Celery', 'feature', 'high', 5.0, 'pending', 0, 'backend'),
(4, 'Implementar cache Redis', 'Adicionar cache para otimizar chamadas', 'feature', 'medium', 2.0, 'pending', 0, 'backend'),
(4, 'Criar testes de integração', 'Testes end-to-end para o pipeline completo', 'test', 'medium', 4.0, 'pending', 0, 'qa'),
(4, 'Documentar API', 'Criar documentação Swagger/OpenAPI', 'docs', 'low', 2.0, 'pending', 0, 'dev'),

-- Tarefas para prp-collaboration-platform
(5, 'Configurar Next.js com TypeScript', 'Criar projeto Next.js com configuração TypeScript', 'setup', 'high', 1.0, 'completed', 100, 'frontend'),
(5, 'Implementar editor Quill', 'Integrar editor de texto rico Quill', 'feature', 'high', 3.0, 'in_progress', 50, 'frontend'),
(5, 'Configurar Socket.io', 'Implementar comunicação em tempo real', 'feature', 'critical', 4.0, 'pending', 0, 'frontend'),
(5, 'Implementar autenticação', 'Configurar NextAuth para login', 'feature', 'high', 3.0, 'pending', 0, 'backend'),
(5, 'Criar sistema de versionamento', 'Implementar controle de versão de PRPs', 'feature', 'medium', 4.0, 'pending', 0, 'backend'),
(5, 'Implementar comentários', 'Sistema de comentários em tempo real', 'feature', 'medium', 3.0, 'pending', 0, 'frontend'),
(5, 'Criar testes E2E', 'Testes end-to-end com Playwright', 'test', 'medium', 3.0, 'pending', 0, 'qa'),

-- Tarefas para prp-analytics-dashboard
(6, 'Configurar Streamlit', 'Criar aplicação Streamlit base', 'setup', 'high', 1.0, 'completed', 100, 'data'),
(6, 'Implementar coleta de dados', 'Sistema para coletar métricas de PRPs', 'feature', 'high', 4.0, 'in_progress', 60, 'data'),
(6, 'Criar visualizações Plotly', 'Implementar gráficos e dashboards', 'feature', 'high', 5.0, 'pending', 0, 'data'),
(6, 'Implementar ML para insights', 'Modelos de ML para análise preditiva', 'feature', 'medium', 6.0, 'pending', 0, 'ml'),
(6, 'Configurar ClickHouse', 'Banco de dados para analytics', 'feature', 'critical', 3.0, 'pending', 0, 'backend'),
(6, 'Criar alertas automáticos', 'Sistema de alertas para métricas', 'feature', 'medium', 2.0, 'pending', 0, 'backend'),
(6, 'Implementar exportação', 'Exportar relatórios em PDF/Excel', 'feature', 'low', 2.0, 'pending', 0, 'data');

-- Inserir contexto para todos os PRPs
INSERT OR IGNORE INTO prp_context (prp_id, context_type, name, path, content, importance) VALUES
(1, 'file', 'src/index.ts', 'src/index.ts', 'Arquivo principal do servidor MCP', 'critical'),
(1, 'file', 'src/tools/register-tools.ts', 'src/tools/register-tools.ts', 'Registro de ferramentas MCP', 'high'),
(1, 'library', '@modelcontextprotocol/sdk', NULL, 'SDK oficial do MCP', 'critical'),
(1, 'library', 'zod', NULL, 'Validação de schemas', 'high'),
(2, 'file', 'src/components/PRPList.tsx', 'src/components/PRPList.tsx', 'Componente de lista de PRPs', 'critical'),
(2, 'file', 'src/components/TaskView.tsx', 'src/components/TaskView.tsx', 'Visualização de tarefas', 'high'),
(2, 'library', 'react', NULL, 'Framework React', 'critical'),
(2, 'library', 'tailwindcss', NULL, 'Framework CSS', 'high'),
(4, 'file', 'src/extractor.py', 'src/extractor.py', 'Módulo principal do extrator de tarefas', 'critical'),
(4, 'file', 'src/models.py', 'src/models.py', 'Modelos de dados Pydantic', 'high'),
(4, 'library', 'openai', NULL, 'SDK da OpenAI para GPT-4', 'critical'),
(4, 'library', 'fastapi', NULL, 'Framework web FastAPI', 'critical'),
(5, 'file', 'src/components/Editor.tsx', 'src/components/Editor.tsx', 'Componente do editor colaborativo', 'critical'),
(5, 'file', 'src/hooks/useCollaboration.ts', 'src/hooks/useCollaboration.ts', 'Hook para colaboração em tempo real', 'high'),
(5, 'library', 'socket.io', NULL, 'Biblioteca para comunicação em tempo real', 'critical'),
(5, 'library', 'quill', NULL, 'Editor de texto rico', 'critical'),
(6, 'file', 'src/analytics.py', 'src/analytics.py', 'Módulo principal de analytics', 'critical'),
(6, 'file', 'src/metrics.py', 'src/metrics.py', 'Cálculo de métricas', 'high'),
(6, 'library', 'plotly', NULL, 'Biblioteca de visualizações', 'critical'),
(6, 'library', 'streamlit', NULL, 'Framework para dashboards', 'critical');

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
(3, (SELECT id FROM prp_tags WHERE name = 'ai')),
(4, (SELECT id FROM prp_tags WHERE name = 'backend')),
(4, (SELECT id FROM prp_tags WHERE name = 'ai')),
(4, (SELECT id FROM prp_tags WHERE name = 'api')),
(4, (SELECT id FROM prp_tags WHERE name = 'automation')),
(5, (SELECT id FROM prp_tags WHERE name = 'frontend')),
(5, (SELECT id FROM prp_tags WHERE name = 'collaboration')),
(5, (SELECT id FROM prp_tags WHERE name = 'realtime')),
(5, (SELECT id FROM prp_tags WHERE name = 'ui/ux')),
(6, (SELECT id FROM prp_tags WHERE name = 'analytics')),
(6, (SELECT id FROM prp_tags WHERE name = 'ml')),
(6, (SELECT id FROM prp_tags WHERE name = 'data')),
(6, (SELECT id FROM prp_tags WHERE name = 'dashboard'));

-- Inserir análises LLM de exemplo
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
) VALUES 
(1, 'task_extraction', 'Implementar um servidor MCP que analisa Product Requirement Prompts e extrai tarefas usando LLM', 'Tarefas extraídas: 1. Configurar projeto base, 2. Implementar autenticação, 3. Criar endpoint de análise, 4. Integrar com LLM', '{"tasks": [{"name": "Configurar projeto base", "type": "setup", "priority": "high"}, {"name": "Implementar autenticação", "type": "feature", "priority": "high"}]}',
    'claude-3-sonnet',
    150,
    2500,
    0.95,
    'system'),
(4, 'task_extraction', 'Sistema que analisa PRPs e extrai automaticamente tarefas usando IA', 'Tarefas extraídas: 1. Configurar ambiente, 2. Implementar modelo de dados, 3. Integrar OpenAI, 4. Criar pipeline', '{"tasks": [{"name": "Configurar ambiente", "type": "setup", "priority": "high"}, {"name": "Implementar modelo de dados", "type": "feature", "priority": "high"}]}',
    'gpt-4',
    200,
    3000,
    0.92,
    'system'),
(5, 'complexity_assessment', 'Plataforma web para equipes colaborarem na criação e revisão de PRPs', 'Complexidade: Alta - Requer sincronização em tempo real, controle de versão, e interface colaborativa', '{"complexity": "high", "challenges": ["realtime_sync", "version_control", "ui_complexity"]}',
    'claude-3-sonnet',
    180,
    2200,
    0.88,
    'system'),
(6, 'dependency_analysis', 'Sistema de métricas e analytics para acompanhar performance de PRPs', 'Dependências: Coleta de dados, processamento, visualização, ML para insights', '{"dependencies": ["data_collection", "processing", "visualization", "ml_models"]}',
    'gpt-4',
    160,
    1800,
    0.94,
    'system');