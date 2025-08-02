#!/bin/bash

# Script para adicionar MCP Sentry ao Claude Code
# Uso: ./add-to-claude-code.sh

echo "🚀 Adicionando MCP Sentry ao Claude Code"
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

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado. Criando com configurações padrão...${NC}"
    cat > .env << 'EOF'
SENTRY_DSN=https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334
SENTRY_AUTH_TOKEN=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
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0/
EOF
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
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

# Remover servidor existente se houver
echo -e "${BLUE}🔄 Verificando configuração existente...${NC}"
claude mcp remove sentry -s local 2>/dev/null

# Adicionar o servidor MCP
echo -e "${BLUE}📍 Adicionando servidor MCP...${NC}"
claude mcp add sentry ./start.sh

# Verificar se foi adicionado com sucesso
echo ""
echo -e "${BLUE}🔍 Verificando status...${NC}"
claude mcp get sentry

# Mostrar status geral
echo ""
echo -e "${BLUE}📊 Status dos servidores MCP:${NC}"
claude mcp list

echo ""
echo -e "${GREEN}✅ MCP Sentry adicionado com sucesso!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📚 Ferramentas disponíveis:${NC}"
echo "  • sentry_capture_exception - Captura exceções"
echo "  • sentry_capture_message - Envia mensagens"
echo "  • sentry_add_breadcrumb - Adiciona contexto"
echo "  • sentry_set_user - Define usuário"
echo "  • sentry_set_tag - Define tags"
echo "  • sentry_set_context - Contexto customizado"
echo "  • sentry_start_transaction - Performance monitoring"
echo "  • sentry_start_session - Release health"
echo "  • sentry_list_projects - Lista projetos (API)"
echo "  • sentry_list_issues - Lista issues (API)"
echo "  • sentry_create_release - Cria releases (API)"
echo "  • ... e mais 7 ferramentas!"
echo ""
echo -e "${BLUE}💡 Como usar:${NC}"
echo '  No Claude Code, peça: "Use a ferramenta sentry_list_projects"'
echo ""
echo -e "${YELLOW}⚠️  Configuração:${NC}"
echo "  DSN: ${SENTRY_DSN:-Não configurado}"
echo "  Org: ${SENTRY_ORG:-coflow}"
echo "  API: ${SENTRY_API_URL:-https://sentry.io/api/0/}"
echo ""
echo -e "${GREEN}Para remover: ./remove-from-claude-code.sh${NC}"