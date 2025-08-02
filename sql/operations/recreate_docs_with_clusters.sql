-- Recriar Sistema de Documentação com Dados Demonstrativos
-- Data: 02/08/2025
-- Objetivo: Popular tabelas com dados organizados em clusters para demonstrar utilidade

-- =====================================================
-- 1. LIMPAR E RECRIAR ESTRUTURA
-- =====================================================

-- Limpar tabelas existentes
DROP TABLE IF EXISTS docs_analytics;
DROP TABLE IF EXISTS docs_feedback;
DROP TABLE IF EXISTS docs_links;
DROP TABLE IF EXISTS docs_sections;
DROP TABLE IF EXISTS docs_tag_relations;
DROP TABLE IF EXISTS docs_tags;
DROP TABLE IF EXISTS docs_versions;
DROP TABLE IF EXISTS docs;

-- =====================================================
-- 2. RECRIAR TABELAS COM SCHEMA OTIMIZADO
-- =====================================================

-- Tabela principal de documentos
CREATE TABLE docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    
    -- Organização em clusters
    cluster_name TEXT NOT NULL,           -- Nome do cluster (ex: "MCP_CORE", "TURSO_CONFIG")
    cluster_priority INTEGER DEFAULT 5,   -- Prioridade dentro do cluster (1=alta, 10=baixa)
    supersedes_doc_id INTEGER,           -- ID do documento que este substitui
    
    -- Classificação de conteúdo
    doc_type TEXT DEFAULT 'guide' CHECK (doc_type IN ('guide', 'config', 'status', 'readme', 'reference', 'obsolete')),
    category TEXT NOT NULL,
    difficulty TEXT DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    estimated_read_time INTEGER DEFAULT 5,
    
    -- Gestão de ciclo de vida
    content_status TEXT DEFAULT 'active' CHECK (content_status IN ('draft', 'active', 'outdated', 'obsolete', 'archived')),
    quality_score REAL DEFAULT 5.0,      -- Score de qualidade (1-10)
    relevance_score REAL DEFAULT 5.0,    -- Score de relevância atual (1-10)
    last_validated DATE,
    validation_needed BOOLEAN DEFAULT 0,
    
    -- Metadados de uso
    view_count INTEGER DEFAULT 0,
    useful_votes INTEGER DEFAULT 0,
    needs_update_votes INTEGER DEFAULT 0,
    
    -- Controle temporal
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    content_date DATE,                    -- Data do conteúdo (pode ser diferente da criação)
    expiry_date DATE,                     -- Data de expiração estimada
    
    -- Relacionamentos
    tags TEXT,                            -- JSON array de tags
    keywords TEXT,                        -- Palavras-chave para busca
    related_docs TEXT,                    -- JSON array de IDs relacionados
    
    FOREIGN KEY (supersedes_doc_id) REFERENCES docs(id)
);

-- Tabela de clusters de conteúdo
CREATE TABLE docs_clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    description TEXT,
    color TEXT DEFAULT '#007bff',
    icon TEXT DEFAULT '📁',
    
    -- Configuração do cluster
    max_docs INTEGER DEFAULT 10,          -- Máximo de docs ativos por cluster
    auto_archive BOOLEAN DEFAULT 1,       -- Auto-arquivar docs obsoletos
    retention_days INTEGER DEFAULT 90,    -- Dias para manter docs obsoletos
    
    -- Estatísticas
    active_docs INTEGER DEFAULT 0,
    total_docs INTEGER DEFAULT 0,
    avg_quality_score REAL DEFAULT 0.0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de tags estruturadas
CREATE TABLE docs_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT DEFAULT 'general',
    color TEXT DEFAULT '#6c757d',
    description TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de relacionamentos docs-tags
CREATE TABLE docs_tag_relations (
    doc_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    relevance_score REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (doc_id, tag_id),
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES docs_tags(id) ON DELETE CASCADE
);

-- Tabela de histórico de mudanças
CREATE TABLE docs_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    change_type TEXT NOT NULL CHECK (change_type IN ('created', 'updated', 'superseded', 'archived', 'quality_update')),
    old_content_status TEXT,
    new_content_status TEXT,
    old_quality_score REAL,
    new_quality_score REAL,
    change_reason TEXT,
    changed_by TEXT DEFAULT 'system',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
);

-- Tabela de análise de obsolescência
CREATE TABLE docs_obsolescence_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER NOT NULL,
    analysis_date DATE DEFAULT CURRENT_DATE,
    
    -- Fatores de obsolescência
    age_factor REAL DEFAULT 0.0,          -- Fator baseado na idade (0-1)
    usage_factor REAL DEFAULT 0.0,        -- Fator baseado no uso (0-1)
    relevance_factor REAL DEFAULT 0.0,    -- Fator de relevância (0-1)
    technical_factor REAL DEFAULT 0.0,    -- Fator técnico (versões, APIs) (0-1)
    
    -- Score final e recomendação
    obsolescence_score REAL DEFAULT 0.0,  -- Score final (0-1, 1=muito obsoleto)
    recommendation TEXT,                   -- Recomendação (keep, update, supersede, archive)
    confidence REAL DEFAULT 0.0,          -- Confiança na recomendação (0-1)
    
    -- Análise automática
    auto_generated BOOLEAN DEFAULT 1,
    analysis_notes TEXT,
    
    FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
);

-- =====================================================
-- 3. ÍNDICES PARA PERFORMANCE
-- =====================================================

CREATE INDEX idx_docs_cluster ON docs(cluster_name);
CREATE INDEX idx_docs_status ON docs(content_status);
CREATE INDEX idx_docs_category ON docs(category);
CREATE INDEX idx_docs_quality ON docs(quality_score);
CREATE INDEX idx_docs_relevance ON docs(relevance_score);
CREATE INDEX idx_docs_supersedes ON docs(supersedes_doc_id);
CREATE INDEX idx_docs_updated_at ON docs(updated_at);

CREATE INDEX idx_clusters_name ON docs_clusters(name);
CREATE INDEX idx_tags_name ON docs_tags(name);
CREATE INDEX idx_changes_doc_id ON docs_changes(doc_id);
CREATE INDEX idx_obsolescence_doc_id ON docs_obsolescence_analysis(doc_id);

-- =====================================================
-- 4. TRIGGERS PARA AUTOMAÇÃO
-- =====================================================

-- Trigger para atualizar updated_at
CREATE TRIGGER trigger_docs_updated_at
    AFTER UPDATE ON docs
    FOR EACH ROW
BEGIN
    UPDATE docs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para registrar mudanças
CREATE TRIGGER trigger_docs_log_changes
    AFTER UPDATE ON docs
    FOR EACH ROW
    WHEN OLD.content_status != NEW.content_status OR OLD.quality_score != NEW.quality_score
BEGIN
    INSERT INTO docs_changes (doc_id, change_type, old_content_status, new_content_status, 
                             old_quality_score, new_quality_score, change_reason)
    VALUES (NEW.id, 'updated', OLD.content_status, NEW.content_status,
            OLD.quality_score, NEW.quality_score, 'Automatic update');
END;

-- Trigger para atualizar estatísticas do cluster
CREATE TRIGGER trigger_update_cluster_stats
    AFTER UPDATE ON docs
    FOR EACH ROW
BEGIN
    UPDATE docs_clusters SET 
        active_docs = (SELECT COUNT(*) FROM docs WHERE cluster_name = NEW.cluster_name AND content_status = 'active'),
        total_docs = (SELECT COUNT(*) FROM docs WHERE cluster_name = NEW.cluster_name),
        avg_quality_score = (SELECT AVG(quality_score) FROM docs WHERE cluster_name = NEW.cluster_name AND content_status = 'active'),
        updated_at = CURRENT_TIMESTAMP
    WHERE name = NEW.cluster_name;
END;

-- =====================================================
-- 5. VIEWS ÚTEIS PARA ANÁLISE
-- =====================================================

-- View de documentos ativos por cluster
CREATE VIEW v_active_docs_by_cluster AS
SELECT 
    d.cluster_name,
    dc.display_name as cluster_display_name,
    dc.icon as cluster_icon,
    COUNT(*) as active_docs,
    AVG(d.quality_score) as avg_quality,
    AVG(d.relevance_score) as avg_relevance,
    SUM(d.view_count) as total_views
FROM docs d
JOIN docs_clusters dc ON d.cluster_name = dc.name
WHERE d.content_status = 'active'
GROUP BY d.cluster_name, dc.display_name, dc.icon
ORDER BY avg_quality DESC;

-- View de documentos que precisam atenção
CREATE VIEW v_docs_need_attention AS
SELECT 
    d.id,
    d.slug,
    d.title,
    d.cluster_name,
    d.content_status,
    d.quality_score,
    d.relevance_score,
    d.last_validated,
    julianday('now') - julianday(d.last_validated) as days_since_validation,
    d.needs_update_votes,
    CASE 
        WHEN d.quality_score < 4.0 THEN 'low_quality'
        WHEN d.relevance_score < 4.0 THEN 'low_relevance'
        WHEN julianday('now') - julianday(d.last_validated) > 90 THEN 'needs_validation'
        WHEN d.needs_update_votes > 2 THEN 'user_reported'
        ELSE 'unknown'
    END as attention_reason
FROM docs d
WHERE d.content_status = 'active'
  AND (d.quality_score < 4.0 
       OR d.relevance_score < 4.0 
       OR julianday('now') - julianday(d.last_validated) > 90
       OR d.needs_update_votes > 2)
ORDER BY d.quality_score ASC, d.relevance_score ASC;

-- View de documentos obsoletos e supersedidos
CREATE VIEW v_obsolete_docs AS
SELECT 
    old_doc.id as obsolete_doc_id,
    old_doc.title as obsolete_title,
    old_doc.cluster_name,
    old_doc.content_status,
    new_doc.id as superseded_by_id,
    new_doc.title as superseded_by_title,
    new_doc.quality_score as new_quality_score,
    old_doc.updated_at as obsolete_date
FROM docs old_doc
LEFT JOIN docs new_doc ON old_doc.id = new_doc.supersedes_doc_id
WHERE old_doc.content_status IN ('outdated', 'obsolete')
ORDER BY old_doc.updated_at DESC;

-- View de análise de clusters
CREATE VIEW v_cluster_health AS
SELECT 
    dc.name,
    dc.display_name,
    dc.icon,
    dc.active_docs,
    dc.total_docs,
    dc.avg_quality_score,
    dc.max_docs,
    CASE 
        WHEN dc.active_docs > dc.max_docs THEN 'overcrowded'
        WHEN dc.avg_quality_score < 4.0 THEN 'low_quality'
        WHEN dc.active_docs = 0 THEN 'empty'
        ELSE 'healthy'
    END as health_status,
    CASE 
        WHEN dc.active_docs > dc.max_docs THEN 'Consider archiving older docs'
        WHEN dc.avg_quality_score < 4.0 THEN 'Review and improve doc quality'
        WHEN dc.active_docs = 0 THEN 'Add documentation to this cluster'
        ELSE 'Cluster is in good condition'
    END as recommendation
FROM docs_clusters dc
ORDER BY dc.avg_quality_score DESC;

-- =====================================================
-- 6. POPULAR COM DADOS DEMONSTRATIVOS
-- =====================================================

-- Criar clusters organizacionais
INSERT INTO docs_clusters (name, display_name, description, color, icon, max_docs) VALUES
('MCP_CORE', 'MCP Core', 'Documentação central do MCP (Model Context Protocol)', '#007bff', '🔌', 8),
('MCP_INTEGRATION', 'MCP Integração', 'Guias de integração e configuração MCP', '#28a745', '🔗', 6),
('TURSO_CONFIG', 'Turso Configuração', 'Configuração e setup do Turso Database', '#17a2b8', '🗄️', 5),
('TURSO_USAGE', 'Turso Uso', 'Guias de uso e operação do Turso', '#20c997', '⚡', 4),
('PRP_SYSTEM', 'Sistema PRP', 'Product Requirement Prompts e gestão', '#fd7e14', '📋', 6),
('PROJECT_MGMT', 'Gestão de Projeto', 'Organização e estrutura do projeto', '#6f42c1', '📁', 4),
('ERRORS_TRACKING', 'Tracking de Erros', 'Documentação de erros e soluções', '#dc3545', '🚨', 3),
('GUIDES_FINAL', 'Guias Finais', 'Documentação consolidada e definitiva', '#ffc107', '🎯', 5);

-- Criar tags estruturadas
INSERT INTO docs_tags (name, category, color, description) VALUES
('mcp', 'technology', '#007bff', 'Model Context Protocol'),
('turso', 'technology', '#17a2b8', 'Turso Database SQLite'),
('prp', 'methodology', '#fd7e14', 'Product Requirement Prompts'),
('config', 'type', '#28a745', 'Documentação de configuração'),
('guide', 'type', '#6c757d', 'Guias e tutoriais'),
('integration', 'type', '#20c997', 'Integração entre sistemas'),
('status', 'type', '#ffc107', 'Relatórios de status'),
('final', 'stage', '#198754', 'Documentação finalizada'),
('python', 'technology', '#3776ab', 'Linguagem Python'),
('typescript', 'technology', '#3178c6', 'Linguagem TypeScript'),
('sql', 'technology', '#336791', 'Structured Query Language'),
('api', 'type', '#ff6b35', 'Application Programming Interface'),
('cursor', 'tool', '#0066cc', 'Cursor IDE'),
('sentry', 'technology', '#362d59', 'Sentry Error Tracking'),
('obsolete', 'status', '#dc3545', 'Conteúdo obsoleto');

-- Popular com documentos organizados em clusters
INSERT INTO docs (slug, title, content, summary, cluster_name, cluster_priority, doc_type, category, 
                 difficulty, estimated_read_time, content_status, quality_score, relevance_score, 
                 last_validated, tags, keywords, content_date) VALUES

-- CLUSTER: MCP_CORE (Documentação central do MCP)
('mcp-overview', 'MCP Overview - Visão Geral do Protocolo', 
'# MCP Overview
Model Context Protocol (MCP) é um protocolo para comunicação entre LLMs e ferramentas externas...', 
'Visão geral do Model Context Protocol, suas funcionalidades e casos de uso principais.',
'MCP_CORE', 1, 'reference', 'mcp', 'medium', 8, 'active', 9.0, 9.5, '2025-08-02',
'["mcp", "protocol", "reference"]', 'mcp, protocol, llm, communication', '2025-08-02'),

('mcp-architecture', 'Arquitetura MCP - Como Funciona', 
'# Arquitetura MCP
O MCP funciona através de um sistema de cliente-servidor onde...', 
'Explicação detalhada da arquitetura do MCP, componentes e fluxo de comunicação.',
'MCP_CORE', 2, 'reference', 'mcp', 'hard', 12, 'active', 8.5, 9.0, '2025-08-02',
'["mcp", "architecture", "technical"]', 'architecture, client, server, communication', '2025-08-02'),

('mcp-best-practices', 'MCP Best Practices - Melhores Práticas', 
'# MCP Best Practices
Para implementar MCP de forma eficiente, siga estas práticas...', 
'Guia de melhores práticas para implementação e uso do MCP em projetos.',
'MCP_CORE', 3, 'guide', 'mcp', 'medium', 6, 'active', 8.0, 8.5, '2025-08-02',
'["mcp", "best-practices", "guide"]', 'practices, implementation, guidelines', '2025-08-02'),

-- CLUSTER: MCP_INTEGRATION (Guias de integração MCP)
('mcp-cursor-integration', 'Integração MCP com Cursor IDE', 
'# Integração MCP Cursor
Para integrar MCP com Cursor IDE, configure o arquivo mcp_servers.json...', 
'Guia completo para configurar e usar MCP dentro do Cursor IDE.',
'MCP_INTEGRATION', 1, 'guide', 'integration', 'hard', 10, 'active', 9.5, 9.0, '2025-08-02',
'["mcp", "cursor", "integration", "guide"]', 'cursor, ide, configuration, setup', '2025-08-02'),

('mcp-python-client', 'Cliente MCP em Python', 
'# Cliente MCP Python
Implementação de cliente MCP usando Python para automação...', 
'Como criar e usar um cliente MCP em Python para automação de tarefas.',
'MCP_INTEGRATION', 2, 'guide', 'programming', 'hard', 8, 'active', 8.5, 8.0, '2025-08-02',
'["mcp", "python", "client", "automation"]', 'python, client, automation, programming', '2025-08-02'),

-- CLUSTER: TURSO_CONFIG (Configuração Turso)
('turso-setup-guide', 'Guia de Setup do Turso Database', 
'# Setup Turso
Para configurar o Turso Database, primeiro instale o CLI...', 
'Guia completo de instalação e configuração inicial do Turso Database.',
'TURSO_CONFIG', 1, 'guide', 'database', 'medium', 7, 'active', 9.0, 9.5, '2025-08-02',
'["turso", "setup", "database", "config"]', 'turso, database, setup, configuration', '2025-08-02'),

('turso-auth-tokens', 'Gerenciamento de Tokens Turso', 
'# Tokens Turso
O Turso usa tokens JWT para autenticação. Configure assim...', 
'Como gerar, configurar e gerenciar tokens de autenticação do Turso.',
'TURSO_CONFIG', 2, 'guide', 'security', 'medium', 5, 'active', 8.5, 9.0, '2025-08-02',
'["turso", "auth", "tokens", "security"]', 'authentication, tokens, security, jwt', '2025-08-02'),

-- CLUSTER: TURSO_USAGE (Uso do Turso)
('turso-mcp-integration', 'Integração Turso + MCP', 
'# Turso MCP
A integração entre Turso e MCP permite persistência de dados...', 
'Como integrar Turso Database com MCP para persistência de dados.',
'TURSO_USAGE', 1, 'guide', 'integration', 'hard', 9, 'active', 9.5, 9.0, '2025-08-02',
'["turso", "mcp", "integration", "database"]', 'integration, persistence, database, mcp', '2025-08-02'),

-- CLUSTER: PRP_SYSTEM (Sistema PRP)
('prp-methodology', 'Metodologia PRP - Product Requirement Prompts', 
'# Metodologia PRP
PRPs são uma metodologia para estruturar requisitos de produto...', 
'Introdução completa à metodologia PRP e como aplicar em projetos.',
'PRP_SYSTEM', 1, 'reference', 'methodology', 'medium', 8, 'active', 9.0, 9.5, '2025-08-02',
'["prp", "methodology", "requirements"]', 'requirements, methodology, product, planning', '2025-08-02'),

('prp-agent-usage', 'Usando o Agente PRP', 
'# Agente PRP
O agente PRP automatiza a criação e gestão de requisitos...', 
'Como usar o agente PRP para automatizar gestão de requisitos de produto.',
'PRP_SYSTEM', 2, 'guide', 'automation', 'medium', 6, 'active', 8.5, 8.5, '2025-08-02',
'["prp", "agent", "automation", "ai"]', 'agent, automation, requirements, ai', '2025-08-02'),

-- CLUSTER: PROJECT_MGMT (Gestão de Projeto)
('project-structure', 'Estrutura de Organização do Projeto', 
'# Estrutura do Projeto
O projeto está organizado seguindo melhores práticas...', 
'Documentação da estrutura organizacional e padrões do projeto.',
'PROJECT_MGMT', 1, 'reference', 'organization', 'easy', 4, 'active', 8.0, 8.0, '2025-08-02',
'["organization", "structure", "standards"]', 'organization, structure, standards, files', '2025-08-02'),

-- CLUSTER: ERRORS_TRACKING (Tracking de Erros)
('sentry-mcp-errors', 'Documentação de Erros MCP Sentry', 
'# Erros MCP Sentry
Documentação automática dos erros encontrados no MCP Sentry...', 
'Catalogação e análise de erros do sistema MCP Sentry com soluções.',
'ERRORS_TRACKING', 1, 'status', 'troubleshooting', 'medium', 5, 'active', 7.5, 7.0, '2025-08-02',
'["sentry", "errors", "troubleshooting"]', 'errors, troubleshooting, sentry, debugging', '2025-08-02'),

-- CLUSTER: GUIDES_FINAL (Guias Finais)
('final-integration-guide', 'Guia Final - Integração Completa', 
'# Integração Final
Guia definitivo para integração completa do sistema...', 
'Documentação final consolidando toda a integração do sistema.',
'GUIDES_FINAL', 1, 'guide', 'final', 'hard', 15, 'active', 9.5, 9.5, '2025-08-02',
'["final", "integration", "complete", "guide"]', 'final, integration, complete, definitive', '2025-08-02'),

-- DOCUMENTOS OBSOLETOS PARA DEMONSTRAR GESTÃO DE CICLO DE VIDA
('old-mcp-config', 'Configuração MCP Antiga (OBSOLETO)', 
'# Configuração MCP Antiga
Esta configuração não funciona mais devido a mudanças na API...', 
'Configuração obsoleta do MCP que foi substituída por versão mais nova.',
'MCP_INTEGRATION', 9, 'obsolete', 'config', 'medium', 4, 'obsolete', 3.0, 2.0, '2025-07-15',
'["mcp", "config", "obsolete"]', 'obsolete, old, deprecated', '2025-07-15'),

('deprecated-turso-setup', 'Setup Turso Depreciado', 
'# Setup Turso Antigo
Este método de setup foi depreciado...', 
'Método antigo de configuração do Turso que não deve mais ser usado.',
'TURSO_CONFIG', 8, 'obsolete', 'setup', 'easy', 3, 'obsolete', 2.5, 1.5, '2025-07-20',
'["turso", "setup", "deprecated", "obsolete"]', 'deprecated, obsolete, old, turso', '2025-07-20');

-- Criar relacionamentos de supersedência
UPDATE docs SET supersedes_doc_id = (SELECT id FROM docs WHERE slug = 'old-mcp-config') 
WHERE slug = 'mcp-cursor-integration';

UPDATE docs SET supersedes_doc_id = (SELECT id FROM docs WHERE slug = 'deprecated-turso-setup') 
WHERE slug = 'turso-setup-guide';

-- Criar relacionamentos docs-tags
INSERT INTO docs_tag_relations (doc_id, tag_id, relevance_score)
SELECT d.id, t.id, 0.9
FROM docs d, docs_tags t
WHERE json_extract(d.tags, '$[0]') = t.name OR json_extract(d.tags, '$[1]') = t.name OR json_extract(d.tags, '$[2]') = t.name;

-- Adicionar análises de obsolescência para documentos antigos
INSERT INTO docs_obsolescence_analysis (doc_id, age_factor, usage_factor, relevance_factor, 
                                       technical_factor, obsolescence_score, recommendation, confidence, analysis_notes)
SELECT 
    d.id,
    0.8,  -- Idade alta
    0.1,  -- Baixo uso
    0.2,  -- Baixa relevância
    0.9,  -- Tecnicamente obsoleto
    0.75, -- Score alto de obsolescência
    'archive', -- Recomendação
    0.9,  -- Alta confiança
    'Documento substituído por versão mais atual'
FROM docs d
WHERE d.content_status = 'obsolete';

-- Adicionar algumas mudanças no histórico para demonstrar rastreamento
INSERT INTO docs_changes (doc_id, change_type, old_content_status, new_content_status, 
                         old_quality_score, new_quality_score, change_reason, changed_by)
SELECT 
    id, 'created', NULL, 'active', NULL, quality_score, 'Initial creation', 'migration_system'
FROM docs WHERE content_status = 'active';

INSERT INTO docs_changes (doc_id, change_type, old_content_status, new_content_status, 
                         old_quality_score, new_quality_score, change_reason, changed_by)
SELECT 
    id, 'superseded', 'active', 'obsolete', 8.0, quality_score, 'Superseded by newer version', 'system'
FROM docs WHERE content_status = 'obsolete';

-- Atualizar estatísticas dos clusters
UPDATE docs_clusters SET 
    active_docs = (SELECT COUNT(*) FROM docs WHERE cluster_name = docs_clusters.name AND content_status = 'active'),
    total_docs = (SELECT COUNT(*) FROM docs WHERE cluster_name = docs_clusters.name),
    avg_quality_score = (SELECT AVG(quality_score) FROM docs WHERE cluster_name = docs_clusters.name AND content_status = 'active'),
    updated_at = CURRENT_TIMESTAMP;

-- Simular algumas visualizações e votos
UPDATE docs SET 
    view_count = CASE 
        WHEN quality_score > 9.0 THEN 150 + (id * 10)
        WHEN quality_score > 8.0 THEN 100 + (id * 8)
        WHEN quality_score > 7.0 THEN 50 + (id * 5)
        ELSE 20 + (id * 2)
    END,
    useful_votes = CASE 
        WHEN quality_score > 9.0 THEN 15 + (id * 2)
        WHEN quality_score > 8.0 THEN 10 + id
        ELSE 5 + (id / 2)
    END
WHERE content_status = 'active';

-- =====================================================
-- 7. FINALIZAÇÃO
-- =====================================================

-- Analisar e mostrar estatísticas finais
SELECT 'CLUSTERS CRIADOS:' as section;
SELECT printf('%s %s: %d docs ativos (qualidade média: %.1f)', 
              icon, display_name, active_docs, avg_quality_score) as cluster_info
FROM docs_clusters ORDER BY avg_quality_score DESC;

SELECT '' as separator;
SELECT 'DOCUMENTOS POR STATUS:' as section;
SELECT content_status, COUNT(*) as count, AVG(quality_score) as avg_quality
FROM docs GROUP BY content_status;

SELECT '' as separator;
SELECT 'TAGS MAIS USADAS:' as section;
SELECT name, usage_count FROM docs_tags ORDER BY usage_count DESC LIMIT 5;

SELECT '' as separator;
SELECT 'DOCUMENTOS QUE PRECISAM ATENÇÃO:' as section;
SELECT title, attention_reason, quality_score FROM v_docs_need_attention LIMIT 3;