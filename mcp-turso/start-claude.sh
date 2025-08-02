#!/bin/bash

# MCP Turso Server Startup Script para Claude Code
# Versão simplificada para o Claude Code

set -e

# Diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Verificar se node_modules existe
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules não encontrado. Execute 'npm install' primeiro."
    exit 1
fi

# Verificar se dist existe
if [ ! -d "dist" ]; then
    echo "❌ dist não encontrado. Execute 'npm run build' primeiro."
    exit 1
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "❌ .env não encontrado. Configure as variáveis de ambiente primeiro."
    exit 1
fi

# Carregar variáveis de ambiente
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Verificar configurações essenciais
if [ -z "$TURSO_DATABASE_URL" ]; then
    echo "❌ TURSO_DATABASE_URL não configurado"
    exit 1
fi

if [ -z "$TURSO_AUTH_TOKEN" ]; then
    echo "❌ TURSO_AUTH_TOKEN não configurado"
    exit 1
fi

# Iniciar o servidor MCP sem logs verbosos
exec node dist/index.js 