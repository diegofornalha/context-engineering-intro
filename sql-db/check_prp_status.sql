-- Script para verificar status final das tabelas PRP
-- Data: 02/08/2025

-- =====================================================
-- RESUMO GERAL
-- =====================================================

SELECT '=== RESUMO DAS TABELAS PRP ===' as info;
SELECT '';

-- Contar registros em cada tabela
SELECT 'Tabela' as tipo, 'Total' as contagem, 'Descrição' as descricao
UNION ALL
SELECT 'PRPs', COUNT(*), 'Product Requirement Prompts' FROM prps
UNION ALL
SELECT 'Tarefas', COUNT(*), 'Tarefas extraídas dos PRPs' FROM prp_tasks
UNION ALL
SELECT 'Tags', COUNT(*), 'Tags para categorização' FROM prp_tags
UNION ALL
SELECT 'Contexto', COUNT(*), 'Arquivos e contexto dos PRPs' FROM prp_context
UNION ALL
SELECT 'Análises LLM', COUNT(*), 'Análises realizadas por LLMs' FROM prp_llm_analysis
UNION ALL
SELECT 'Histórico', COUNT(*), 'Histórico de mudanças' FROM prp_history;

SELECT '';

-- =====================================================
-- PRPs COM DETALHES
-- =====================================================

SELECT '=== PRPs CADASTRADOS ===' as info;
SELECT '';

SELECT 
    id,
    name,
    title,
    status,
    priority,
    complexity,
    created_at
FROM prps
ORDER BY id;

SELECT '';

-- =====================================================
-- PROGRESSO DOS PRPs
-- =====================================================

SELECT '=== PROGRESSO DOS PRPs ===' as info;
SELECT '';

SELECT 
    p.name as prp_name,
    p.title,
    p.status as prp_status,
    COUNT(t.id) as total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN t.status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_tasks,
    SUM(CASE WHEN t.status = 'pending' THEN 1 ELSE 0 END) as pending_tasks,
    ROUND(
        (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) * 100.0) / 
        COUNT(t.id), 2
    ) as completion_percentage
FROM prps p
LEFT JOIN prp_tasks t ON p.id = t.prp_id
GROUP BY p.id
ORDER BY completion_percentage DESC;

SELECT '';

-- =====================================================
-- TAREFAS POR STATUS
-- =====================================================

SELECT '=== TAREFAS POR STATUS ===' as info;
SELECT '';

SELECT 
    t.status,
    COUNT(*) as total,
    ROUND(AVG(t.progress), 1) as avg_progress,
    ROUND(AVG(t.estimated_hours), 1) as avg_hours
FROM prp_tasks t
GROUP BY t.status
ORDER BY total DESC;

SELECT '';

-- =====================================================
-- TAGS MAIS UTILIZADAS
-- =====================================================

SELECT '=== TAGS MAIS UTILIZADAS ===' as info;
SELECT '';

SELECT 
    t.name as tag_name,
    t.description,
    t.color,
    COUNT(ptr.prp_id) as prps_associados
FROM prp_tags t
LEFT JOIN prp_tag_relations ptr ON t.id = ptr.tag_id
GROUP BY t.id
ORDER BY prps_associados DESC, t.name;

SELECT '';

-- =====================================================
-- ANÁLISES LLM
-- =====================================================

SELECT '=== ANÁLISES LLM REALIZADAS ===' as info;
SELECT '';

SELECT 
    p.name as prp_name,
    a.analysis_type,
    a.model_used,
    a.confidence_score,
    a.tokens_used,
    a.processing_time_ms,
    a.created_at
FROM prp_llm_analysis a
JOIN prps p ON a.prp_id = p.id
ORDER BY a.created_at DESC;

SELECT '';

-- =====================================================
-- CONTEXTO DOS PRPs
-- =====================================================

SELECT '=== CONTEXTO DOS PRPs ===' as info;
SELECT '';

SELECT 
    p.name as prp_name,
    c.context_type,
    c.name as context_name,
    c.importance,
    c.path
FROM prp_context c
JOIN prps p ON c.prp_id = p.id
ORDER BY p.id, c.importance DESC;

SELECT '';

-- =====================================================
-- ESTATÍSTICAS FINAIS
-- =====================================================

SELECT '=== ESTATÍSTICAS FINAIS ===' as info;
SELECT '';

SELECT 
    'Total de PRPs' as metric,
    COUNT(*) as value
FROM prps
UNION ALL
SELECT 
    'PRPs Ativos',
    COUNT(*)
FROM prps
WHERE status = 'active'
UNION ALL
SELECT 
    'Total de Tarefas',
    COUNT(*)
FROM prp_tasks
UNION ALL
SELECT 
    'Tarefas Concluídas',
    COUNT(*)
FROM prp_tasks
WHERE status = 'completed'
UNION ALL
SELECT 
    'Tarefas em Progresso',
    COUNT(*)
FROM prp_tasks
WHERE status = 'in_progress'
UNION ALL
SELECT 
    'Total de Tags',
    COUNT(*)
FROM prp_tags
UNION ALL
SELECT 
    'Análises LLM',
    COUNT(*)
FROM prp_llm_analysis
UNION ALL
SELECT 
    'Horas Estimadas',
    ROUND(SUM(estimated_hours), 1)
FROM prp_tasks
WHERE estimated_hours IS NOT NULL;

SELECT '';

SELECT '=== PRONTO PARA MIGRAÇÃO PARA TURSO ===' as info;
SELECT 'Todas as tabelas PRP estão criadas e populadas com dados de exemplo!';