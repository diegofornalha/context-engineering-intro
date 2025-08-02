#!/bin/bash

# Script wrapper para Cursor MCP
# Garante que as variáveis de ambiente sejam carregadas corretamente

# Definir variáveis de ambiente diretamente
export SENTRY_DSN="https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334"
export SENTRY_AUTH_TOKEN="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"
export SENTRY_ORG="coflow"
export SENTRY_API_URL="https://sentry.io/api/0"

# Mudar para o diretório do script
cd "$(dirname "$0")"

# Verificar se o projeto foi compilado
if [ ! -d "dist" ]; then
    echo "Compilando projeto..." >&2
    npm run build
fi

# Iniciar o servidor MCP
exec node dist/index.js 