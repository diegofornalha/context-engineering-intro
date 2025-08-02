#!/bin/bash

# Script de inicialização para Cursor MCP
# Uso: ./start.sh

# Carregar configurações do config.env se existir
if [ -f "config.env" ]; then
    source config.env
fi

# Verificar se o projeto foi compilado
if [ ! -d "dist" ]; then
    echo "Compilando projeto..." >&2
    npm run build
fi

# Iniciar o servidor MCP
node dist/index.js