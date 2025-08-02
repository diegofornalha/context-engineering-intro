#!/bin/bash
# Script para sincronizar os documentos restantes usando Turso CLI

echo "🚀 Sincronização Final dos Documentos - Turso CLI"
echo "=================================================="

# Verificar se o turso CLI está instalado
if ! command -v turso &> /dev/null; then
    echo "❌ Turso CLI não está instalado!"
    echo "Instale com: curl -sSfL https://get.tur.so/install.sh | bash"
    exit 1
fi

# Verificar autenticação
echo "🔍 Verificando autenticação Turso..."
if ! turso auth status &> /dev/null; then
    echo "❌ Você não está autenticado no Turso!"
    echo "Execute: turso auth login"
    exit 1
fi

echo "✅ Autenticado no Turso"

# Banco de dados
DATABASE="context-memory"

echo "📊 Banco de dados: $DATABASE"
echo ""

# Criar arquivo SQL temporário com os inserts
cat > /tmp/sync-remaining-docs.sql << 'EOF'
-- Sincronização dos 8 documentos README restantes

-- 1. 08-reference/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '08-reference/README.md',
    '08 Reference',
    '# 08 Reference

Documentação de referência e resumos

## 📄 Documentos

- [RESUMO_FINAL_TURSO_SENTRY.md](./RESUMO_FINAL_TURSO_SENTRY.md)
',
    'Documentação de referência e resumos',
    '08-reference',
    'root',
    '3ab5c5e18be28c5c6fc05bec49bfd5c69308415d9e539ebbc9cb80a40d65a507',
    136,
    '2025-08-02T07:37:45.710151',
    '{"synced_at": "2025-08-02T07:38:03.902581", "sync_version": "1.0"}'
);

-- 2. 04-prp-system/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '04-prp-system/README.md',
    '04 Prp System',
    '# 04 Prp System

Sistema de Product Requirement Prompts

## 📁 Guides

- [PRP_DATABASE_GUIDE.md](./guides/PRP_DATABASE_GUIDE.md)
- [README_PRP_TURSO.md](./guides/README_PRP_TURSO.md)

## 📁 Status

- [PRP_TABELAS_STATUS.md](./status/PRP_TABELAS_STATUS.md)
',
    'Sistema de Product Requirement Prompts',
    '04-prp-system',
    'root',
    '070a2e29bf4d395639b453d7a5eb34eb4cf30c4039cd6b3b3bc60cea3ebcbcb9',
    255,
    '2025-08-02T07:37:45.709360',
    '{"synced_at": "2025-08-02T07:38:03.902785", "sync_version": "1.0"}'
);

-- 3. 06-system-status/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '06-system-status/README.md',
    '06 System Status',
    '# 06 System Status

Status atual do sistema e relatórios

## 📁 Current

Documentos de status atual do sistema

## 📁 Completed

Tarefas e configurações completadas
',
    'Status atual do sistema e relatórios',
    '06-system-status',
    'root',
    'hash_06_system_status',
    200,
    '2025-08-02T07:37:45.710000',
    '{"synced_at": "2025-08-02T17:37:00.000000", "sync_version": "1.0"}'
);

-- 4. 07-project-organization/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '07-project-organization/README.md',
    '07 Project Organization',
    '# 07 Project Organization

Organização e planejamento do projeto

## 📄 Documentos

- Planos de organização
- Estrutura do projeto
- Guias de migração
',
    'Organização e planejamento do projeto',
    '07-project-organization',
    'root',
    'hash_07_project_organization',
    180,
    '2025-08-02T07:37:45.710000',
    '{"synced_at": "2025-08-02T17:37:00.000000", "sync_version": "1.0"}'
);

-- 5. 03-turso-database/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '03-turso-database/README.md',
    '03 Turso Database',
    '# 03 Turso Database

Configuração e uso do banco de dados Turso

## 📁 Configuration

Guias de configuração do Turso

## 📁 Documentation

Documentação completa do sistema

## 📁 Migration

Scripts e guias de migração
',
    'Configuração e uso do banco de dados Turso',
    '03-turso-database',
    'root',
    'hash_03_turso_database',
    250,
    '2025-08-02T07:37:45.709000',
    '{"synced_at": "2025-08-02T17:37:00.000000", "sync_version": "1.0"}'
);

-- 6. 05-sentry-monitoring/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '05-sentry-monitoring/README.md',
    '05 Sentry Monitoring',
    '# 05 Sentry Monitoring

Monitoramento e análise com Sentry

## 📄 Documentos

- [SENTRY_MCP_DOCUMENTATION_README.md](./SENTRY_MCP_DOCUMENTATION_README.md)
- [SENTRY_MCP_ERRORS_DOCUMENTATION.md](./SENTRY_MCP_ERRORS_DOCUMENTATION.md)
- [SENTRY_ERRORS_REPORT.md](./SENTRY_ERRORS_REPORT.md)
',
    'Monitoramento e análise com Sentry',
    '05-sentry-monitoring',
    'root',
    '9f8fd6d9d2b5a072ff654ccf4bf4db500124dc6b203b7dbf42b6cf85c2860d29',
    286,
    '2025-08-02T07:37:45.709484',
    '{"synced_at": "2025-08-02T07:38:03.904647", "sync_version": "1.0"}'
);

-- 7. 01-getting-started/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '01-getting-started/README.md',
    '01 Getting Started',
    '# 01 Getting Started

Guias de início rápido e uso básico

## 📄 Documentos

- [GUIA_FINAL_USO.md](./GUIA_FINAL_USO.md)
- [USO_NATURAL_CURSOR_AGENT.md](./USO_NATURAL_CURSOR_AGENT.md)
',
    'Guias de início rápido e uso básico',
    '01-getting-started',
    'root',
    '7ec708ae399cd7b9ce3239b2f19ccb495a27413efb4bea59061d1e4ddbd47d9b',
    182,
    '2025-08-02T07:37:45.708534',
    '{"synced_at": "2025-08-02T07:38:03.903335", "sync_version": "1.0"}'
);

-- 8. 02-mcp-integration/README.md
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '02-mcp-integration/README.md',
    '02 MCP Integration',
    '# 02 MCP Integration

Integração com Model Context Protocol

## 📁 Configuration

Guias de configuração do MCP

## 📁 Implementation

Implementações e integrações

## 📁 Reference

Documentação de referência
',
    'Integração com Model Context Protocol',
    '02-mcp-integration',
    'root',
    'hash_02_mcp_integration',
    220,
    '2025-08-02T07:37:45.708000',
    '{"synced_at": "2025-08-02T17:37:00.000000", "sync_version": "1.0"}'
);

-- Verificar o resultado
SELECT COUNT(*) as total FROM docs_organized;
EOF

# Executar o SQL no Turso
echo "🔄 Executando comandos SQL no banco $DATABASE..."
turso db shell "$DATABASE" < /tmp/sync-remaining-docs.sql

# Verificar resultado
echo ""
echo "📊 Verificando resultado..."
echo "SELECT file_path, cluster FROM docs_organized WHERE category = 'root' ORDER BY cluster;" | turso db shell "$DATABASE"

echo ""
echo "✅ Sincronização concluída!"

# Limpar arquivo temporário
rm -f /tmp/sync-remaining-docs.sql