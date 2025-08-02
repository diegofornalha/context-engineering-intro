#!/bin/bash
# Script para executar sincronização via MCP Turso

echo "🚀 Executando sincronização de documentos com Turso..."

# Usar o Claude Code para executar via MCP
cat << 'EOF'
Use a ferramenta mcp__turso__execute_query para executar o script SQL em sync-to-turso.sql no banco context-memory.
Leia o arquivo docs/sync-to-turso.sql e execute todas as queries.
EOF
