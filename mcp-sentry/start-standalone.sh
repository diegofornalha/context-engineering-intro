#!/bin/bash

# Script de inicialização para MCP Sentry Standalone
# Uso: ./start-standalone.sh

echo "🚀 Iniciando MCP Sentry Standalone"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar se estamos no diretório correto
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Carregar configurações do arquivo config.env
if [ -f "config.env" ]; then
    echo -e "${BLUE}📋 Carregando configurações do config.env...${NC}"
    set -a
    source config.env
    set +a
    echo -e "${GREEN}✅ Configurações carregadas${NC}"
else
    echo -e "${YELLOW}⚠️  Arquivo config.env não encontrado. Usando configurações padrão...${NC}"
fi

# Verificar se o projeto foi compilado
if [ ! -d "dist" ]; then
    echo -e "${BLUE}📦 Compilando projeto...${NC}"
    npm install && npm run build
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erro na compilação. Verifique o código.${NC}"
        exit 1
    fi
fi

# Verificar se as variáveis de ambiente estão configuradas
if [ -z "$SENTRY_DSN" ]; then
    echo -e "${RED}❌ SENTRY_DSN não configurado${NC}"
    exit 1
fi

if [ -z "$SENTRY_AUTH_TOKEN" ]; then
    echo -e "${RED}❌ SENTRY_AUTH_TOKEN não configurado${NC}"
    exit 1
fi

if [ -z "$SENTRY_ORG" ]; then
    echo -e "${RED}❌ SENTRY_ORG não configurado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Todas as configurações estão válidas${NC}"
echo ""
echo -e "${BLUE}📊 Configurações atuais:${NC}"
echo "  DSN: ${SENTRY_DSN}"
echo "  Org: ${SENTRY_ORG}"
echo "  API: ${SENTRY_API_URL:-https://sentry.io/api/0/}"
echo "  Release: ${SENTRY_RELEASE:-mcp-sentry@1.0.0}"
echo "  Environment: ${SENTRY_ENVIRONMENT:-production}"
echo ""

# Testar conexão com Sentry
echo -e "${BLUE}🔍 Testando conexão com Sentry...${NC}"
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Conexão com Sentry estabelecida${NC}"
else
    echo -e "${RED}❌ Erro na conexão com Sentry${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 MCP Sentry Standalone iniciado com sucesso!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📚 Como usar:${NC}"
echo "  • Para testar: ./test-standalone.sh"
echo "  • Para adicionar ao Claude: ./add-to-claude-code.sh"
echo "  • Para ver logs: tail -f sentry-mcp.log"
echo ""
echo -e "${BLUE}🔗 Dashboard:${NC}"
echo "  https://coflow.sentry.io"
echo ""
echo -e "${YELLOW}💡 Dica: Use 'source config.env' para carregar as configurações no terminal${NC}"

# Iniciar servidor
exec node dist/index.js