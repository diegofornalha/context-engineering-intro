-- Schema para armazenamento de PRPs (Product Requirement Prompts)
-- Banco: context-memory
-- Data: 02/08/2025

-- =====================================================
-- TABELA PRINCIPAL: PRPs
-- =====================================================
CREATE TABLE IF NOT EXISTS prps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,                    -- Nome único do PRP
    title TEXT NOT NULL,                          -- Título descritivo
    description TEXT,                             -- Descrição geral
    objective TEXT NOT NULL,                      -- Objetivo principal
    justification TEXT,                           -- Por que é necessário
    
    -- Conteúdo estruturado em JSON
    context_data TEXT NOT NULL,                   -- JSON com contexto (arquivos, versões, exemplos)
    implementation_details TEXT NOT NULL,         -- JSON com detalhes de implementação
    validation_gates TEXT,                        -- JSON com portões de validação
    
    -- Metadados
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'completed', 'archived')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    complexity TEXT DEFAULT 'medium' CHECK (complexity IN ('low', 'medium', 'high')),
    
    -- Relacionamentos
    parent_prp_id INTEGER,                        -- PRP pai (para dependências)
    related_prps TEXT,                            -- JSON array de IDs relacionados
    
    -- Controle de versão
    version INTEGER DEFAULT 1,                    -- Versão atual
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,                              -- Usuário que criou
    updated_by TEXT,                              -- Usuário que atualizou
    
    -- Busca e organização
    tags TEXT,                                    -- JSON array de tags
    search_text TEXT,                             -- Texto para busca full-text
    
    FOREIGN KEY (parent_prp_id) REFERENCES prps(id)
);

-- =====================================================
-- TABELA DE TAREFAS EXTRAÍDAS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,                      -- PRP pai
    task_name TEXT NOT NULL,                      -- Nome da tarefa
    description TEXT,                             -- Descrição detalhada
    task_type TEXT DEFAULT 'feature' CHECK (task_type IN ('feature', 'bugfix', 'refactor', 'test', 'docs', 'setup')),
    
    -- Prioridade e estimativa
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    estimated_hours REAL,                         -- Estimativa em horas
    complexity TEXT DEFAULT 'medium' CHECK (complexity IN ('low', 'medium', 'high')),
    
    -- Status e progresso
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'review', 'completed', 'blocked')),
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    
    -- Dependências
    dependencies TEXT,                            -- JSON array de IDs de tarefas dependentes
    blockers TEXT,                                -- JSON array de IDs de tarefas bloqueadoras
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to TEXT,                             -- Usuário responsável
    completed_at TIMESTAMP,
    
    -- Contexto específico da tarefa
    context_files TEXT,                           -- JSON array de arquivos relacionados
    acceptance_criteria TEXT,                     -- Critérios de aceitação
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE CONTEXTO E ARQUIVOS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,                      -- PRP relacionado
    context_type TEXT NOT NULL CHECK (context_type IN ('file', 'directory', 'library', 'api', 'example', 'reference')),
    
    -- Informações do contexto
    name TEXT NOT NULL,                           -- Nome do arquivo/biblioteca/etc
    path TEXT,                                    -- Caminho completo (se aplicável)
    content TEXT,                                 -- Conteúdo ou descrição
    version TEXT,                                 -- Versão (se aplicável)
    
    -- Metadados
    importance TEXT DEFAULT 'medium' CHECK (importance IN ('low', 'medium', 'high', 'critical')),
    is_required BOOLEAN DEFAULT 1,                -- Se é obrigatório para o PRP
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE TAGS E CATEGORIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,                    -- Nome da tag
    description TEXT,                             -- Descrição da tag
    color TEXT DEFAULT '#007bff',                 -- Cor para UI
    category TEXT DEFAULT 'general',              -- Categoria da tag
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
    prp_id INTEGER NOT NULL,                      -- PRP relacionado
    version INTEGER NOT NULL,                     -- Número da versão
    action TEXT NOT NULL CHECK (action IN ('created', 'updated', 'status_changed', 'archived')),
    
    -- Dados da versão
    old_data TEXT,                                -- JSON com dados anteriores
    new_data TEXT,                                -- JSON com dados novos
    changes_summary TEXT,                         -- Resumo das mudanças
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,                              -- Usuário que fez a mudança
    comment TEXT,                                 -- Comentário sobre a mudança
    
    FOREIGN KEY (prp_id) REFERENCES prps(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE ANÁLISES LLM
-- =====================================================
CREATE TABLE IF NOT EXISTS prp_llm_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,                      -- PRP analisado
    analysis_type TEXT NOT NULL CHECK (analysis_type IN ('task_extraction', 'complexity_assessment', 'dependency_analysis', 'validation_check')),
    
    -- Resultado da análise
    input_content TEXT NOT NULL,                  -- Conteúdo enviado para o LLM
    output_content TEXT NOT NULL,                 -- Resposta do LLM
    parsed_data TEXT,                             -- JSON com dados estruturados extraídos
    
    -- Metadados da análise
    model_used TEXT,                              -- Modelo LLM usado
    tokens_used INTEGER,                          -- Tokens consumidos
    processing_time_ms INTEGER,                   -- Tempo de processamento
    confidence_score REAL,                        -- Score de confiança (0-1)
    
    -- Status
    status TEXT DEFAULT 'completed' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,                           -- Mensagem de erro (se falhou)
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,                              -- Usuário que solicitou a análise
    
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

-- Trigger para registrar histórico automaticamente
CREATE TRIGGER IF NOT EXISTS trigger_prps_history
    AFTER UPDATE ON prps
    FOR EACH ROW
BEGIN
    INSERT INTO prp_history (prp_id, version, action, old_data, new_data, changes_summary)
    VALUES (
        NEW.id,
        NEW.version,
        'updated',
        json_object(
            'title', OLD.title,
            'status', OLD.status,
            'priority', OLD.priority,
            'description', OLD.description
        ),
        json_object(
            'title', NEW.title,
            'status', NEW.status,
            'priority', NEW.priority,
            'description', NEW.description
        ),
        'PRP updated'
    );
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
('devops', 'DevOps e infraestrutura', '#6c757d', 'infrastructure');

-- Inserir PRP de exemplo
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
    search_text
) VALUES (
    'mcp-prp-server',
    'Servidor MCP para Análise de PRPs',
    'Implementar um servidor MCP que analisa Product Requirement Prompts e extrai tarefas usando LLM',
    'Criar uma versão simples do taskmaster MCP que analisa PRPs em vez de PRDs',
    '{"files": ["src/index.ts", "src/tools/register-tools.ts"], "libraries": ["@modelcontextprotocol/sdk", "zod"], "examples": ["examples/database-tools.ts"]}',
    '{"architecture": "Cloudflare Workers", "authentication": "GitHub OAuth", "database": "PostgreSQL", "llm": "Anthropic Claude"}',
    '{"tests": "pytest", "linting": "ruff", "type_check": "TypeScript"}',
    'active',
    'high',
    '["backend", "api", "mcp"]',
    'servidor MCP análise PRPs taskmaster LLM Anthropic Cloudflare Workers GitHub OAuth PostgreSQL'
); 