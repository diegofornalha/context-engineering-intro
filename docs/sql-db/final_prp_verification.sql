-- Script Final de Verificação PRP para Turso
-- Use este script para verificar se as tabelas PRP estão funcionando corretamente
-- Data: 02/08/2025

-- =====================================================
-- VERIFICAÇÃO DE TABELAS EXISTENTES
-- =====================================================

SELECT '🔍 VERIFICAÇÃO DE TABELAS PRP' as status;

-- Listar todas as tabelas PRP
SELECT name as 'Tabelas PRP Encontradas' 
FROM sqlite_master 
WHERE type='table' AND name LIKE 'prp%' 
ORDER BY name;

-- =====================================================
-- CONTAGEM DE REGISTROS
-- =====================================================

SELECT '📊 CONTAGEM DE REGISTROS' as status;

SELECT 'PRPs' as tabela, COUNT(*) as total FROM prps
UNION ALL
SELECT 'Tarefas' as tabela, COUNT(*) as total FROM prp_tasks
UNION ALL
SELECT 'Tags' as tabela, COUNT(*) as total FROM prp_tags
UNION ALL
SELECT 'Contexto' as tabela, COUNT(*) as total FROM prp_context
UNION ALL
SELECT 'Tag Relations' as tabela, COUNT(*) as total FROM prp_tag_relations
UNION ALL
SELECT 'Histórico' as tabela, COUNT(*) as total FROM prp_history
UNION ALL
SELECT 'Análises LLM' as tabela, COUNT(*) as total FROM prp_llm_analysis
ORDER BY tabela;

-- =====================================================
-- SAMPLE DATA - TOP 3 PRPs
-- =====================================================

SELECT '📋 SAMPLE DATA - TOP 3 PRPs' as status;

SELECT 
    id,
    name,
    title,
    status,
    priority,
    created_at
FROM prps 
ORDER BY priority DESC, created_at DESC 
LIMIT 3;

-- =====================================================
-- VERIFICAÇÃO DE RELACIONAMENTOS
-- =====================================================

SELECT '🔗 VERIFICAÇÃO DE RELACIONAMENTOS' as status;

-- PRPs com suas tarefas
SELECT 
    p.name as prp_name,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as in_progress_tasks,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending_tasks
FROM prps p
LEFT JOIN prp_tasks t ON p.id = t.prp_id
GROUP BY p.id, p.name
ORDER BY total_tasks DESC;

-- =====================================================
-- VERIFICAÇÃO DE TAGS MAIS USADAS
-- =====================================================

SELECT '🏷️ TAGS MAIS UTILIZADAS' as status;

SELECT 
    t.name as tag_name,
    t.description,
    t.color,
    COUNT(ptr.prp_id) as uso_count
FROM prp_tags t
LEFT JOIN prp_tag_relations ptr ON t.id = ptr.tag_id
GROUP BY t.id, t.name, t.description, t.color
ORDER BY uso_count DESC, t.name
LIMIT 10;

-- =====================================================
-- VERIFICAÇÃO DE VIEWS
-- =====================================================

SELECT '👁️ VERIFICAÇÃO DE VIEWS' as status;

-- Testar view de progresso
SELECT 
    name,
    title,
    prp_status,
    total_tasks,
    completed_tasks,
    completion_percentage
FROM v_prp_progress
WHERE total_tasks > 0
ORDER BY completion_percentage DESC;

-- =====================================================
-- ANÁLISES LLM DISPONÍVEIS
-- =====================================================

SELECT '🤖 ANÁLISES LLM DISPONÍVEIS' as status;

SELECT 
    p.name as prp_name,
    a.analysis_type,
    a.model_used,
    a.confidence_score,
    a.created_at
FROM prp_llm_analysis a
JOIN prps p ON a.prp_id = p.id
ORDER BY a.confidence_score DESC, a.created_at DESC;

-- =====================================================
-- VERIFICAÇÃO DE INTEGRIDADE
-- =====================================================

SELECT '✅ VERIFICAÇÃO DE INTEGRIDADE' as status;

-- Verificar se há tarefas órfãs
SELECT 
    'Tarefas Órfãs' as check_type,
    COUNT(*) as count_found
FROM prp_tasks t
LEFT JOIN prps p ON t.prp_id = p.id
WHERE p.id IS NULL

UNION ALL

-- Verificar se há contextos órfãos
SELECT 
    'Contextos Órfãos' as check_type,
    COUNT(*) as count_found
FROM prp_context c
LEFT JOIN prps p ON c.prp_id = p.id
WHERE p.id IS NULL

UNION ALL

-- Verificar se há relações de tags órfãs
SELECT 
    'Tag Relations Órfãs' as check_type,
    COUNT(*) as count_found
FROM prp_tag_relations ptr
LEFT JOIN prps p ON ptr.prp_id = p.id
LEFT JOIN prp_tags t ON ptr.tag_id = t.id
WHERE p.id IS NULL OR t.id IS NULL;

-- =====================================================
-- STATUS FINAL
-- =====================================================

SELECT '🎉 VERIFICAÇÃO CONCLUÍDA' as status;

SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM prps) > 0 
        AND (SELECT COUNT(*) FROM prp_tasks) > 0 
        AND (SELECT COUNT(*) FROM prp_tags) > 0
        THEN '✅ TABELAS PRP FUNCIONANDO CORRETAMENTE!'
        ELSE '❌ PROBLEMA DETECTADO NAS TABELAS PRP'
    END as resultado_final;