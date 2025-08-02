#!/bin/bash

# MCP Turso Server - Versão TypeScript para Claude Code
cd "$(dirname "$0")"

# Verificar se existe arquivo .env
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copie .env.example para .env e configure suas variáveis:"
    echo "   cp .env.example .env"
    echo "   # Edite o arquivo .env com suas configurações"
    exit 1
fi

# Carregar variáveis de ambiente do arquivo .env
export $(cat .env | grep -v '^#' | xargs)

# Garantir que o projeto está compilado
if [ ! -d "dist" ]; then
    npm install >/dev/null 2>&1
    npm run build >/dev/null 2>&1
fi

# Iniciar servidor MCP no modo stdio
exec node dist/index.js 