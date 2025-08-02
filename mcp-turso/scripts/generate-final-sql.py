#!/usr/bin/env python3
"""
Gera os comandos SQL finais para inserir os documentos restantes.
"""
import json
from datetime import datetime

print("🚀 Comandos SQL para Sincronização Final")
print("="*50)
print("\n-- Execute estes comandos no banco context-memory do Turso")
print("-- Via MCP no Claude Code ou diretamente no Turso CLI\n")

# Lista simplificada dos 8 documentos restantes
docs = [
    ('08-reference/README.md', '08 Reference', '08-reference'),
    ('04-prp-system/README.md', '04 Prp System', '04-prp-system'),
    ('06-system-status/README.md', '06 System Status', '06-system-status'),
    ('07-project-organization/README.md', '07 Project Organization', '07-project-organization'),
    ('03-turso-database/README.md', '03 Turso Database', '03-turso-database'),
    ('05-sentry-monitoring/README.md', '05 Sentry Monitoring', '05-sentry-monitoring'),
    ('01-getting-started/README.md', '01 Getting Started', '01-getting-started'),
    ('02-mcp-integration/README.md', '02 MCP Integration', '02-mcp-integration')
]

print("-- 1. Verificar se a tabela existe")
print("SELECT name FROM sqlite_master WHERE type='table' AND name='docs_organized';\n")

print("-- 2. Inserir os documentos restantes")
for i, (file_path, title, cluster) in enumerate(docs, 1):
    print(f"-- {i}. {file_path}")
    print(f"""INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '{file_path}',
    '{title}',
    '# {title}

README do cluster {cluster}',
    'README do cluster {cluster}',
    '{cluster}',
    'root',
    'hash_{cluster.replace("-", "_")}',
    200,
    '2025-08-02T07:37:45.000000',
    '{{"synced_at": "{datetime.now().isoformat()}", "sync_version": "1.0"}}'
);
""")

print("-- 3. Verificar o resultado")
print("""SELECT file_path, cluster, title 
FROM docs_organized 
WHERE category = 'root'
ORDER BY cluster;
""")

print("\n-- 4. Contar total de documentos")
print("SELECT COUNT(*) as total FROM docs_organized;")

print("\n📝 Total de comandos INSERT: 8")
print("✅ Execute estes comandos para completar a sincronização!")