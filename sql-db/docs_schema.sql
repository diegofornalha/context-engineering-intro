-- Schema para Sistema de Documentação no Turso
-- Data: 02/08/2025
-- Objetivo: Migrar documentação .md para banco estruturado

-- =====================================================
-- TABELA PRINCIPAL: DOCUMENTOS
-- =====================================================
CREATE TABLE IF NOT EXISTS docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,              -- Nome do arquivo (sem .md)
    title TEXT NOT NULL,                    -- Título extraído do documento
    content TEXT NOT NULL,                  -- Conteúdo markdown completo
    summary TEXT,                           -- Resumo automático
    
    -- Metadados estruturados
    doc_type TEXT DEFAULT 'guide' CHECK (doc_type IN ('guide', 'config', 'status', 'readme', 'plan', 'reference')),
    category TEXT DEFAULT 'general',        -- categoria principal
    subcategory TEXT,                       -- subcategoria
    difficulty TEXT DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    estimated_read_time INTEGER,            -- tempo estimado de leitura (minutos)
    
    -- Status e ciclo de vida
    status TEXT DEFAULT 'active' CHECK (status IN ('draft', 'active', 'outdated', 'archived')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    is_complete BOOLEAN DEFAULT 1,          -- se o documento está completo
    last_validated DATE,                    -- última vez que foi validado
    
    -- Relacionamentos
    parent_doc_id INTEGER,                  -- documento pai (hierarquia)
    related_docs TEXT,                      -- JSON array de IDs relacionados
    project_id TEXT,                        -- projeto relacionado
    
    -- Controle de versão
    version TEXT DEFAULT '1.0.0',          -- versão semântica
    version_number INTEGER DEFAULT 1,       -- número sequencial
    original_file_path TEXT,               -- caminho original do arquivo
    file_size INTEGER,                     -- tamanho do arquivo original
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    archived_at TIMESTAMP,
    
    -- Autoria e responsabilidade
    created_by TEXT DEFAULT 'system',
    updated_by TEXT,
    reviewer TEXT,                         -- quem revisou por último
    maintainer TEXT,                       -- responsável pela manutenção
    
    -- Indexação e busca
    tags TEXT,                             -- JSON array de tags
    keywords TEXT,                         -- palavras-chave para busca
    search_text TEXT,                      -- texto otimizado para busca
    language TEXT DEFAULT 'pt-br',        -- idioma do documento
    
    -- Métricas e analytics
    view_count INTEGER DEFAULT 0,         -- quantas vezes foi acessado
    last_viewed_at TIMESTAMP,             -- último acesso
    usefulness_score REAL DEFAULT 0.0,    -- score de utilidade (0-5)
    feedback_count INTEGER DEFAULT 0,     -- quantidade de feedbacks
    
    FOREIGN KEY (parent_doc_id) REFERENCES docs(id)
);

-- =====================================================
-- TABELA DE HISTÓRICO DE VERSÕES
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    content TEXT NOT NULL,                 -- conteúdo desta versão
    change_summary TEXT,                   -- resumo das mudanças
    change_type TEXT DEFAULT 'update' CHECK (change_type IN ('create', 'update', 'major_update', 'restructure', 'archive')),
    
    -- Diff e comparação
    lines_added INTEGER DEFAULT 0,
    lines_removed INTEGER DEFAULT 0,
    lines_modified INTEGER DEFAULT 0,
    
    -- Metadados da versão
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    comment TEXT,                          -- comentário sobre a mudança
    
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE TAGS E CATEGORIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    color TEXT DEFAULT '#007bff',          -- cor para UI
    category TEXT DEFAULT 'general',       -- categoria da tag
    usage_count INTEGER DEFAULT 0,        -- quantos docs usam esta tag
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELA DE RELACIONAMENTO DOCS-TAGS
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_tag_relations (
    doc_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    relevance_score REAL DEFAULT 1.0,     -- quão relevante é esta tag (0-1)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (doc_id, tag_id),
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES docs_tags(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELA DE SEÇÕES E ESTRUTURA
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    section_title TEXT NOT NULL,           -- título da seção
    section_content TEXT NOT NULL,         -- conteúdo da seção
    section_order INTEGER NOT NULL,       -- ordem da seção no documento
    section_level INTEGER DEFAULT 1,      -- nível do cabeçalho (1=h1, 2=h2, etc)
    section_type TEXT DEFAULT 'content',  -- tipo de seção (content, code, table, list)
    
    -- Para navegação e índice
    anchor TEXT,                           -- âncora para links diretos
    parent_section_id INTEGER,            -- seção pai (para hierarquia)
    
    -- Metadados da seção
    word_count INTEGER,                    -- contagem de palavras
    estimated_read_time INTEGER,          -- tempo estimado de leitura
    
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_section_id) REFERENCES docs_sections(id)
);

-- =====================================================
-- TABELA DE LINKS E REFERÊNCIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    link_text TEXT NOT NULL,               -- texto do link
    link_url TEXT NOT NULL,                -- URL ou caminho
    link_type TEXT DEFAULT 'internal' CHECK (link_type IN ('internal', 'external', 'file', 'image', 'anchor')),
    
    -- Validação de links
    is_valid BOOLEAN DEFAULT 1,           -- se o link está funcionando
    last_checked TIMESTAMP,               -- última vez que foi verificado
    http_status INTEGER,                   -- status HTTP (para links externos)
    
    -- Contexto
    section_id INTEGER,                    -- seção onde aparece o link
    context TEXT,                          -- contexto ao redor do link
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES docs_sections(id)
);

-- =====================================================
-- TABELA DE FEEDBACK E COMENTÁRIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    feedback_type TEXT DEFAULT 'general' CHECK (feedback_type IN ('general', 'error', 'suggestion', 'clarification', 'rating')),
    
    -- Conteúdo do feedback
    feedback_text TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    is_helpful BOOLEAN,                    -- se o documento foi útil
    
    -- Contexto
    section_id INTEGER,                    -- seção específica (opcional)
    user_context TEXT,                     -- contexto do usuário
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    is_resolved BOOLEAN DEFAULT 0,
    resolved_at TIMESTAMP,
    resolved_by TEXT,
    
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES docs_sections(id)
);

-- =====================================================
-- TABELA DE ESTATÍSTICAS DE USO
-- =====================================================
CREATE TABLE IF NOT EXISTS docs_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('view', 'search', 'download', 'share', 'bookmark')),
    
    -- Dados do evento
    user_agent TEXT,                       -- informações do navegador
    ip_address TEXT,                       -- IP (para analytics)
    session_id TEXT,                       -- sessão do usuário
    
    -- Contexto
    referrer TEXT,                         -- de onde veio
    search_query TEXT,                     -- se veio de busca
    time_spent INTEGER,                    -- tempo gasto no documento (segundos)
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
);

-- =====================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================

-- Índices de busca
CREATE INDEX IF NOT EXISTS idx_docs_search_text ON docs(search_text);
CREATE INDEX IF NOT EXISTS idx_docs_title ON docs(title);
CREATE INDEX IF NOT EXISTS idx_docs_slug ON docs(slug);
CREATE INDEX IF NOT EXISTS idx_docs_content ON docs(content);

-- Índices de filtros
CREATE INDEX IF NOT EXISTS idx_docs_category ON docs(category);
CREATE INDEX IF NOT EXISTS idx_docs_status ON docs(status);
CREATE INDEX IF NOT EXISTS idx_docs_priority ON docs(priority);
CREATE INDEX IF NOT EXISTS idx_docs_doc_type ON docs(doc_type);
CREATE INDEX IF NOT EXISTS idx_docs_project_id ON docs(project_id);

-- Índices temporais
CREATE INDEX IF NOT EXISTS idx_docs_created_at ON docs(created_at);
CREATE INDEX IF NOT EXISTS idx_docs_updated_at ON docs(updated_at);
CREATE INDEX IF NOT EXISTS idx_docs_last_validated ON docs(last_validated);

-- Índices de relacionamentos
CREATE INDEX IF NOT EXISTS idx_docs_versions_doc_id ON docs_versions(doc_id);
CREATE INDEX IF NOT EXISTS idx_docs_sections_doc_id ON docs_sections(doc_id);
CREATE INDEX IF NOT EXISTS idx_docs_links_doc_id ON docs_links(doc_id);
CREATE INDEX IF NOT EXISTS idx_docs_feedback_doc_id ON docs_feedback(doc_id);
CREATE INDEX IF NOT EXISTS idx_docs_analytics_doc_id ON docs_analytics(doc_id);

-- Índices de tags
CREATE INDEX IF NOT EXISTS idx_docs_tags_name ON docs_tags(name);
CREATE INDEX IF NOT EXISTS idx_docs_tag_relations_doc_id ON docs_tag_relations(doc_id);
CREATE INDEX IF NOT EXISTS idx_docs_tag_relations_tag_id ON docs_tag_relations(tag_id);

-- =====================================================
-- TRIGGERS PARA AUTOMAÇÃO
-- =====================================================

-- Trigger para atualizar updated_at automaticamente
CREATE TRIGGER IF NOT EXISTS trigger_docs_updated_at
    AFTER UPDATE ON docs
    FOR EACH ROW
BEGIN
    UPDATE docs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para criar versão automaticamente quando conteúdo muda
CREATE TRIGGER IF NOT EXISTS trigger_docs_version_on_update
    AFTER UPDATE ON docs
    FOR EACH ROW
    WHEN OLD.content != NEW.content
BEGIN
    -- Incrementar número da versão
    UPDATE docs SET version_number = version_number + 1 WHERE id = NEW.id;
    
    -- Criar entrada no histórico
    INSERT INTO docs_versions (doc_id, version_number, content, change_summary, created_by)
    VALUES (NEW.id, NEW.version_number, NEW.content, 'Conteúdo atualizado', NEW.updated_by);
END;

-- Trigger para atualizar contagem de uso de tags
CREATE TRIGGER IF NOT EXISTS trigger_update_tag_usage
    AFTER INSERT ON docs_tag_relations
    FOR EACH ROW
BEGIN
    UPDATE docs_tags SET usage_count = usage_count + 1 WHERE id = NEW.tag_id;
END;

-- =====================================================
-- VIEWS ÚTEIS PARA CONSULTAS
-- =====================================================

-- View de documentos com informações completas
CREATE VIEW IF NOT EXISTS v_docs_complete AS
SELECT 
    d.*,
    GROUP_CONCAT(dt.name) as tag_names,
    GROUP_CONCAT(dt.color) as tag_colors,
    COUNT(dv.id) as version_count,
    COUNT(df.id) as feedback_count,
    AVG(df.rating) as avg_rating
FROM docs d
LEFT JOIN docs_tag_relations dtr ON d.id = dtr.doc_id
LEFT JOIN docs_tags dt ON dtr.tag_id = dt.id
LEFT JOIN docs_versions dv ON d.id = dv.doc_id
LEFT JOIN docs_feedback df ON d.id = df.doc_id
GROUP BY d.id;

-- View de documentos por categoria
CREATE VIEW IF NOT EXISTS v_docs_by_category AS
SELECT 
    category,
    subcategory,
    COUNT(*) as doc_count,
    AVG(usefulness_score) as avg_usefulness,
    SUM(view_count) as total_views
FROM docs
WHERE status = 'active'
GROUP BY category, subcategory
ORDER BY doc_count DESC;

-- View de documentos mais populares
CREATE VIEW IF NOT EXISTS v_docs_popular AS
SELECT 
    d.id,
    d.slug,
    d.title,
    d.category,
    d.view_count,
    d.usefulness_score,
    d.last_viewed_at,
    COUNT(da.id) as recent_views
FROM docs d
LEFT JOIN docs_analytics da ON d.id = da.doc_id 
    AND da.event_type = 'view' 
    AND da.created_at > datetime('now', '-30 days')
WHERE d.status = 'active'
GROUP BY d.id
ORDER BY d.view_count DESC, recent_views DESC;

-- View de documentos desatualizados
CREATE VIEW IF NOT EXISTS v_docs_outdated AS
SELECT 
    d.id,
    d.slug,
    d.title,
    d.last_validated,
    d.updated_at,
    julianday('now') - julianday(d.updated_at) as days_since_update,
    julianday('now') - julianday(d.last_validated) as days_since_validation
FROM docs d
WHERE 
    d.status = 'active' 
    AND (
        d.last_validated < date('now', '-90 days')
        OR d.updated_at < date('now', '-60 days')
    )
ORDER BY days_since_validation DESC;