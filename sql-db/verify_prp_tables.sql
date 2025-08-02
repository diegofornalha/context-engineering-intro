-- Script para verificar status das tabelas PRP
-- Data: 02/08/2025

-- =====================================================
-- VERIFICAÇÃO GERAL DAS TABELAS
-- =====================================================

-- Contar registros em cada tabela
SELECT 'PRPs' as tabela, COUNT(*) as total FROM prps
UNION ALL
SELECT 'Tarefas' as tabela, COUNT(*) as total FROM prp_tasks
UNION ALL
SELECT 'Tags' as tabela, COUNT(*) as total FROM prp_tags
UNION ALL
SELECT 'Contexto' as tabela, COUNT(*) as total FROM prp_context
UNION ALL
SELECT 'Histórico' as tabela, COUNT(*) as total FROM prp_history
UNION ALL
SELECT 'Análises LLM' as tabela, COUNT(*) as total FROM prp_llm_analysis;

-- =====================================================
-- PRPs COM DETALHES
-- =====================================================

SELECT 
    id,
    name,
    title,
    status,
    priority,
    complexity,
    created_at,
    updated_at
FROM prps
ORDER BY id;

-- =====================================================
-- TAREFAS POR PRP
-- =====================================================

SELECT 
    p.name as prp_name,
    t.task_name,
    t.status,
    t.progress,
    t.priority,
    t.assigned_to,
    t.estimated_hours
FROM prp_tasks t
JOIN prps p ON t.prp_id = p.id
ORDER BY p.id, t.id;

-- =====================================================
-- TAGS E RELACIONAMENTOS
-- =====================================================

SELECT 
    t.name as tag_name,
    t.description,
    t.color,
    COUNT(ptr.prp_id) as prps_associados
FROM prp_tags t
LEFT JOIN prp_tag_relations ptr ON t.id = ptr.tag_id
GROUP BY t.id
ORDER BY prps_associados DESC, t.name;

-- =====================================================
-- PROGRESSO GERAL
-- =====================================================

SELECT 
    p.name,
    p.title,
    p.status as prp_status,
    COUNT(t.id) as total_tasks,
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
-- ANÁLISES LLM
-- =====================================================

SELECT 
    p.name as prp_name,
    a.analysis_type,
    a.model_used,
    a.confidence_score,
    a.created_at
FROM prp_llm_analysis a
JOIN prps p ON a.prp_id = p.id
ORDER BY a.created_at DESC;

-- =====================================================
-- CONTEXTO DOS PRPs
-- =====================================================

SELECT 
    p.name as prp_name,
    c.context_type,
    c.name as context_name,
    c.importance
FROM prp_context c
JOIN prps p ON c.prp_id = p.id
ORDER BY p.id, c.importance DESC;