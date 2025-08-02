#!/bin/bash

# Script para remover MCP Sentry do Claude Code
# Uso: ./remove-from-claude-code.sh

echo "🗑️  Removendo MCP Sentry do Claude Code"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar se o servidor existe
echo -e "${BLUE}🔍 Verificando configuração atual...${NC}"
claude mcp get sentry 2>/dev/null

if [ $? -eq 0 ]; then
    # Remover de todos os escopos possíveis
    echo -e "${BLUE}🔄 Removendo servidor MCP...${NC}"
    
    # Tentar remover de cada escopo
    claude mcp remove sentry -s local 2>/dev/null
    claude mcp remove sentry -s project 2>/dev/null
    claude mcp remove sentry -s user 2>/dev/null
    
    echo -e "${GREEN}✅ MCP Sentry removido com sucesso!${NC}"
else
    echo -e "${YELLOW}⚠️  MCP Sentry não estava configurado${NC}"
fi

# Mostrar status atual
echo ""
echo -e "${BLUE}📊 Status atual dos servidores MCP:${NC}"
claude mcp list

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Para adicionar novamente: ./add-to-claude-code.sh${NC}"