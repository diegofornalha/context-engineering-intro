-- =====================================================
-- MIGRAÇÃO SIMPLIFICADA - Ajustes Incrementais
-- Data: 02/08/2025
-- =====================================================

-- =====================================================
-- 1. ADICIONAR COLUNAS QUE FALTAM
-- =====================================================

-- Adicionar coluna last_sync na tabela docs
ALTER TABLE docs ADD COLUMN last_sync TIMESTAMP;

-- Adicionar coluna priority na tabela docs_clusters (se não existir)
-- Verificar se já existe primeiro
INSERT OR IGNORE INTO docs_clusters (name, display_name, description, icon, color) 
VALUES ('temp', 'temp', 'temp', '📁', '#6B7280');

-- Adicionar priority se não existir
ALTER TABLE docs_clusters ADD COLUMN priority INTEGER DEFAULT 1;

-- Remover linha temporária
DELETE FROM docs_clusters WHERE name = 'temp';

-- =====================================================
-- 2. ATUALIZAR CLUSTERS EXISTENTES
-- =====================================================

-- Garantir que clusters essenciais existem
INSERT OR IGNORE INTO docs_clusters (name, display_name, description, icon, color, priority) VALUES
('guias-essenciais', 'Guias Essenciais', 'Documentação fundamental do projeto', '⭐', '#F59E0B', 1),
('mcp-integracao', 'MCP Integração', 'Documentos sobre integração MCP', '🔗', '#3B82F6', 2),
('turso-database', 'Turso Database', 'Configuração e uso do Turso', '🗄️', '#10B981', 3),
('sync-sistema', 'Sistema de Sync', 'Sincronização inteligente', '🔄', '#8B5CF6', 4),
('desenvolvimento', 'Desenvolvimento', 'Guias de desenvolvimento', '⚡', '#EF4444', 5),
('documentacao', 'Documentação', 'Documentação geral', '📚', '#6366F1', 6),
('obsoletos', 'Obsoletos', 'Documentos antigos/removidos', '🗑️', '#6B7280', 99);

-- Atualizar priority nos clusters existentes
UPDATE docs_clusters SET priority = 1 WHERE name = 'guias-essenciais';
UPDATE docs_clusters SET priority = 2 WHERE name = 'mcp-integracao';
UPDATE docs_clusters SET priority = 3 WHERE name = 'turso-database';
UPDATE docs_clusters SET priority = 4 WHERE name = 'sync-sistema';
UPDATE docs_clusters SET priority = 5 WHERE name = 'desenvolvimento';
UPDATE docs_clusters SET priority = 6 WHERE name = 'documentacao';
UPDATE docs_clusters SET priority = 99 WHERE name = 'obsoletos';

-- =====================================================
-- 3. LIMPEZA DAS TABELAS DESNECESSÁRIAS
-- =====================================================

-- Remover tabelas que você identificou como desnecessárias
DROP TABLE IF EXISTS docs_changes;
DROP TABLE IF EXISTS prp_history;

-- Nota: As outras (docs_obsolescence_analysis, docs_tag_relations, prp_tag_relations) 
-- já foram removidas pelo usuário

-- =====================================================
-- 4. RECRIAR ÍNDICES ESSENCIAIS
-- =====================================================

-- Índices para docs
CREATE INDEX IF NOT EXISTS idx_docs_cluster ON docs(cluster_name);
CREATE INDEX IF NOT EXISTS idx_docs_status ON docs(content_status);
CREATE INDEX IF NOT EXISTS idx_docs_category ON docs(category);
CREATE INDEX IF NOT EXISTS idx_docs_sync ON docs(last_sync);
CREATE INDEX IF NOT EXISTS idx_docs_search ON docs(slug);

-- =====================================================
-- 5. RECRIAR VIEWS ÚTEIS
-- =====================================================

-- View de docs por cluster (simplificada)
DROP VIEW IF EXISTS v_docs_by_cluster;
CREATE VIEW v_docs_by_cluster AS
SELECT 
    d.cluster_name,
    dc.display_name as cluster_display_name,
    dc.icon as cluster_icon,
    COUNT(d.id) as total_docs,
    AVG(d.quality_score) as avg_quality,
    SUM(d.view_count) as total_views,
    MAX(d.updated_at) as last_updated
FROM docs d
LEFT JOIN docs_clusters dc ON d.cluster_name = dc.name
WHERE d.content_status = 'active'
GROUP BY d.cluster_name, dc.display_name, dc.icon
ORDER BY dc.priority, total_docs DESC;

-- View de PRPs com tarefas (simplificada)
DROP VIEW IF EXISTS v_prps_with_tasks;
CREATE VIEW v_prps_with_tasks AS
SELECT 
    p.*,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as in_progress_tasks,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending_tasks,
    ROUND(
        CAST(COUNT(CASE WHEN t.status = 'completed' THEN 1 END) AS FLOAT) * 100.0 / 
        NULLIF(COUNT(t.id), 0), 1
    ) as completion_percentage
FROM prps p
LEFT JOIN prp_tasks t ON p.id = t.prp_id
GROUP BY p.id;

-- =====================================================
-- 6. TRIGGERS SIMPLIFICADOS
-- =====================================================

-- Trigger para atualizar timestamp de docs
DROP TRIGGER IF EXISTS trigger_docs_updated_at;
CREATE TRIGGER trigger_docs_updated_at
    AFTER UPDATE ON docs
    FOR EACH ROW
    BEGIN
        UPDATE docs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- =====================================================
-- 7. LIMPEZA DE DADOS
-- =====================================================

-- Atualizar docs órfãos para cluster de documentação
UPDATE docs SET cluster_name = 'documentacao' WHERE cluster_name IS NULL OR cluster_name = '';

-- Atualizar status de docs
UPDATE docs SET content_status = 'active' WHERE content_status IS NULL OR content_status = '';

-- Marcar docs com nomes obsoletos
UPDATE docs SET 
    cluster_name = 'obsoletos',
    content_status = 'archived'
WHERE (
    LOWER(slug) LIKE '%obsolet%' OR 
    LOWER(slug) LIKE '%deprecat%' OR
    LOWER(slug) LIKE '%antigo%' OR
    LOWER(slug) LIKE '%old%' OR
    LOWER(slug) LIKE '%temp%' OR
    LOWER(title) LIKE '%obsolet%'
) AND content_status != 'archived';

-- =====================================================
-- 8. OTIMIZAÇÕES FINAIS
-- =====================================================

-- Atualizar estatísticas das tabelas
ANALYZE;

-- Vacuum para otimizar espaço
VACUUM;