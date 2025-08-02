#!/bin/bash

# MCP Sentry Server
# Uso: ./start.sh

cd "$(dirname "$0")"

# Carregar variáveis de ambiente do .env se existir
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Compilar se necessário
if [ ! -d "dist" ]; then
    npm run build || exit 1
fi

# Iniciar servidor
exec node dist/index.js "$@"