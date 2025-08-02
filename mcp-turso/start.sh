#!/bin/bash

# MCP Turso Server - Versão TypeScript para Claude Code
cd "$(dirname "$0")"

# Configurar variáveis de ambiente para o banco de memória
export TURSO_DATABASE_URL="libsql://context-memory-diegofornalha.aws-us-east-1.turso.io"
export TURSO_ORGANIZATION="diegofornalha"
export TURSO_DEFAULT_DATABASE="context-memory"
export TURSO_AUTH_TOKEN="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTQxMTc5NjIsImlkIjoiOTUwY2ExMGUtN2EzMi00ODgwLTkyYjgtOTNkMTdmZTZjZTBkIiwicmlkIjoiZWU2YTJlNmYtMDViYy00NWIzLWEyOTgtN2Q0NzE3NTE0YjRiIn0.rnD-GZ4nA8dOvorMQ6GwM2yKSNT4KcKwwAzjdgzqK1ZUMoCOe_c23CusgnsBNr3m6WzejPMiy0HlrrMUfqZBCA"

# Garantir que o projeto está compilado
if [ ! -d "dist" ]; then
    npm install >/dev/null 2>&1
    npm run build >/dev/null 2>&1
fi

# Iniciar servidor MCP no modo stdio
exec node dist/index.js 