-- Script para melhorar e adicionar dados às tabelas PRP
-- Data: 02/08/2025

-- =====================================================
-- ADICIONAR MAIS PRPs DE EXEMPLO
-- =====================================================

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

-- =====================================================
-- ADICIONAR TAREFAS PARA OS NOVOS PRPs
-- =====================================================

-- Tarefas para o extrator automático
INSERT OR IGNORE INTO prp_tasks (prp_id, task_name, description, task_type, priority, estimated_hours, status, progress, assigned_to) VALUES
(6, 'Configurar ambiente FastAPI', 'Criar estrutura base do projeto FastAPI', 'setup', 'high', 2.0, 'completed', 100, 'backend'),
(6, 'Implementar modelo de dados', 'Criar modelos Pydantic para PRPs e tarefas', 'feature', 'high', 3.0, 'in_progress', 70, 'backend'),
(6, 'Integrar OpenAI GPT-4', 'Configurar integração com OpenAI para análise', 'feature', 'critical', 4.0, 'pending', 0, 'ai'),
(6, 'Criar pipeline de processamento', 'Implementar fila de processamento com Celery', 'feature', 'high', 5.0, 'pending', 0, 'backend'),
(6, 'Implementar cache Redis', 'Adicionar cache para otimizar chamadas', 'feature', 'medium', 2.0, 'pending', 0, 'backend'),
(6, 'Criar testes de integração', 'Testes end-to-end para o pipeline completo', 'test', 'medium', 4.0, 'pending', 0, 'qa'),
(6, 'Documentar API', 'Criar documentação Swagger/OpenAPI', 'docs', 'low', 2.0, 'pending', 0, 'dev');

-- Tarefas para a plataforma de colaboração
INSERT OR IGNORE INTO prp_tasks (prp_id, task_name, description, task_type, priority, estimated_hours, status, progress, assigned_to) VALUES
(7, 'Configurar Next.js com TypeScript', 'Criar projeto Next.js com configuração TypeScript', 'setup', 'high', 1.0, 'completed', 100, 'frontend'),
(7, 'Implementar editor Quill', 'Integrar editor de texto rico Quill', 'feature', 'high', 3.0, 'in_progress', 50, 'frontend'),
(7, 'Configurar Socket.io', 'Implementar comunicação em tempo real', 'feature', 'critical', 4.0, 'pending', 0, 'frontend'),
(7, 'Implementar autenticação', 'Configurar NextAuth para login', 'feature', 'high', 3.0, 'pending', 0, 'backend'),
(7, 'Criar sistema de versionamento', 'Implementar controle de versão de PRPs', 'feature', 'medium', 4.0, 'pending', 0, 'backend'),
(7, 'Implementar comentários', 'Sistema de comentários em tempo real', 'feature', 'medium', 3.0, 'pending', 0, 'frontend'),
(7, 'Criar testes E2E', 'Testes end-to-end com Playwright', 'test', 'medium', 3.0, 'pending', 0, 'qa');

-- Tarefas para o dashboard de analytics
INSERT OR IGNORE INTO prp_tasks (prp_id, task_name, description, task_type, priority, estimated_hours, status, progress, assigned_to) VALUES
(8, 'Configurar Streamlit', 'Criar aplicação Streamlit base', 'setup', 'high', 1.0, 'completed', 100, 'data'),
(8, 'Implementar coleta de dados', 'Sistema para coletar métricas de PRPs', 'feature', 'high', 4.0, 'in_progress', 60, 'data'),
(8, 'Criar visualizações Plotly', 'Implementar gráficos e dashboards', 'feature', 'high', 5.0, 'pending', 0, 'data'),
(8, 'Implementar ML para insights', 'Modelos de ML para análise preditiva', 'feature', 'medium', 6.0, 'pending', 0, 'ml'),
(8, 'Configurar ClickHouse', 'Banco de dados para analytics', 'feature', 'critical', 3.0, 'pending', 0, 'backend'),
(8, 'Criar alertas automáticos', 'Sistema de alertas para métricas', 'feature', 'medium', 2.0, 'pending', 0, 'backend'),
(8, 'Implementar exportação', 'Exportar relatórios em PDF/Excel', 'feature', 'low', 2.0, 'pending', 0, 'data');

-- =====================================================
-- ADICIONAR NOVAS TAGS
-- =====================================================

INSERT OR IGNORE INTO prp_tags (name, description, color, category) VALUES
('ai', 'Inteligência Artificial', '#e83e8c', 'technology'),
('automation', 'Automação de processos', '#20c997', 'process'),
('collaboration', 'Colaboração em tempo real', '#17a2b8', 'feature'),
('realtime', 'Comunicação em tempo real', '#fd7e14', 'technology'),
('analytics', 'Análise de dados', '#6f42c1', 'data'),
('ml', 'Machine Learning', '#dc3545', 'ai'),
('data', 'Processamento de dados', '#28a745', 'data'),
('dashboard', 'Dashboards e visualizações', '#ffc107', 'ui');

-- =====================================================
-- ADICIONAR RELACIONAMENTOS DE TAGS
-- =====================================================

INSERT OR IGNORE INTO prp_tag_relations (prp_id, tag_id) VALUES
(6, (SELECT id FROM prp_tags WHERE name = 'backend')),
(6, (SELECT id FROM prp_tags WHERE name = 'ai')),
(6, (SELECT id FROM prp_tags WHERE name = 'api')),
(6, (SELECT id FROM prp_tags WHERE name = 'automation')),
(7, (SELECT id FROM prp_tags WHERE name = 'frontend')),
(7, (SELECT id FROM prp_tags WHERE name = 'collaboration')),
(7, (SELECT id FROM prp_tags WHERE name = 'realtime')),
(7, (SELECT id FROM prp_tags WHERE name = 'ui/ux')),
(8, (SELECT id FROM prp_tags WHERE name = 'analytics')),
(8, (SELECT id FROM prp_tags WHERE name = 'ml')),
(8, (SELECT id FROM prp_tags WHERE name = 'data')),
(8, (SELECT id FROM prp_tags WHERE name = 'dashboard'));

-- =====================================================
-- ADICIONAR CONTEXTO PARA OS NOVOS PRPs
-- =====================================================

INSERT OR IGNORE INTO prp_context (prp_id, context_type, name, path, content, importance) VALUES
(6, 'file', 'src/extractor.py', 'src/extractor.py', 'Módulo principal do extrator de tarefas', 'critical'),
(6, 'file', 'src/models.py', 'src/models.py', 'Modelos de dados Pydantic', 'high'),
(6, 'library', 'openai', NULL, 'SDK da OpenAI para GPT-4', 'critical'),
(6, 'library', 'fastapi', NULL, 'Framework web FastAPI', 'critical'),
(7, 'file', 'src/components/Editor.tsx', 'src/components/Editor.tsx', 'Componente do editor colaborativo', 'critical'),
(7, 'file', 'src/hooks/useCollaboration.ts', 'src/hooks/useCollaboration.ts', 'Hook para colaboração em tempo real', 'high'),
(7, 'library', 'socket.io', NULL, 'Biblioteca para comunicação em tempo real', 'critical'),
(7, 'library', 'quill', NULL, 'Editor de texto rico', 'critical'),
(8, 'file', 'src/analytics.py', 'src/analytics.py', 'Módulo principal de analytics', 'critical'),
(8, 'file', 'src/metrics.py', 'src/metrics.py', 'Cálculo de métricas', 'high'),
(8, 'library', 'plotly', NULL, 'Biblioteca de visualizações', 'critical'),
(8, 'library', 'streamlit', NULL, 'Framework para dashboards', 'critical');

-- =====================================================
-- ADICIONAR ANÁLISES LLM DE EXEMPLO
-- =====================================================

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
(6, 'task_extraction', 'Sistema que analisa PRPs e extrai automaticamente tarefas usando IA', 'Tarefas extraídas: 1. Configurar ambiente, 2. Implementar modelo de dados, 3. Integrar OpenAI, 4. Criar pipeline', '{"tasks": [{"name": "Configurar ambiente", "type": "setup", "priority": "high"}, {"name": "Implementar modelo de dados", "type": "feature", "priority": "high"}]}',
    'gpt-4',
    200,
    3000,
    0.92,
    'system'),
(7, 'complexity_assessment', 'Plataforma web para equipes colaborarem na criação e revisão de PRPs', 'Complexidade: Alta - Requer sincronização em tempo real, controle de versão, e interface colaborativa', '{"complexity": "high", "challenges": ["realtime_sync", "version_control", "ui_complexity"]}',
    'claude-3-sonnet',
    180,
    2200,
    0.88,
    'system'),
(8, 'dependency_analysis', 'Sistema de métricas e analytics para acompanhar performance de PRPs', 'Dependências: Coleta de dados, processamento, visualização, ML para insights', '{"dependencies": ["data_collection", "processing", "visualization", "ml_models"]}',
    'gpt-4',
    160,
    1800,
    0.94,
    'system');

-- =====================================================
-- ATUALIZAR VIEWS COM NOVOS DADOS
-- =====================================================

-- Recriar view de progresso para incluir novos dados
DROP VIEW IF EXISTS v_prp_progress;
CREATE VIEW v_prp_progress AS
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