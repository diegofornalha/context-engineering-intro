#!/bin/bash

# MCP Sentry Server
# Uso: ./start.sh

cd "$(dirname "$0")"

# Carregar variáveis de ambiente do config.env ou .env
if [ -f config.env ]; then
    set -a
    source config.env
    set +a
elif [ -f .env ]; then
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