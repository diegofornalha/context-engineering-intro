#!/bin/bash

# MCP Sentry Server para Cursor
# Baseado no start-mcp.sh que funciona no Claude Code

cd "$(dirname "$0")"

# Configurar variáveis de ambiente
export SENTRY_DSN="https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334"
export SENTRY_AUTH_TOKEN="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"
export SENTRY_ORG="coflow"
export SENTRY_API_URL="https://sentry.io/api/0/"

# Garantir que o projeto está compilado
if [ ! -d "dist" ]; then
    npm install >/dev/null 2>&1
    npm run build >/dev/null 2>&1
fi

# Iniciar servidor MCP no modo stdio
exec node dist/index.js