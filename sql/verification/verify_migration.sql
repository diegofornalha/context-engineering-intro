
-- Queries para verificar a migração

-- Verificar total de registros
SELECT 'sentry_errors' as table_name, COUNT(*) as total FROM sentry_errors
UNION ALL
SELECT 'sentry_projects' as table_name, COUNT(*) as total FROM sentry_projects
UNION ALL
SELECT 'mcp_issues' as table_name, COUNT(*) as total FROM mcp_issues;

-- Verificar erros críticos
SELECT project_name, error_title, error_level, event_count 
FROM sentry_errors 
WHERE error_level = 'error';

-- Verificar problemas de MCP abertos
SELECT mcp_name, issue_type, description 
FROM mcp_issues 
WHERE status = 'open';

-- Estatísticas por projeto
SELECT 
    project_name,
    COUNT(*) as total_issues,
    SUM(CASE WHEN error_level = 'error' THEN 1 ELSE 0 END) as critical_errors,
    SUM(CASE WHEN error_level = 'warning' THEN 1 ELSE 0 END) as warnings,
    SUM(CASE WHEN error_level = 'info' THEN 1 ELSE 0 END) as info_messages
FROM sentry_errors 
GROUP BY project_name;
