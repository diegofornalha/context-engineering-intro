#!/bin/bash

# MCP Turso Server - Versão TypeScript para Claude Code
cd "$(dirname "$0")"

# Configurar variáveis de ambiente
export TURSO_DATABASE_URL="http://127.0.0.1:8080"

# Garantir que o projeto está compilado
if [ ! -d "dist" ]; then
    npm install >/dev/null 2>&1
    npm run build >/dev/null 2>&1
fi

# Iniciar servidor MCP no modo stdio
exec node dist/index.js