#!/bin/bash

# Script para adicionar MCP Sentry ao Cursor
# Uso: ./add-to-cursor.sh

echo "🚀 Adicionando MCP Sentry ao Cursor"
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
    echo -e "${BLUE}📝 Criando arquivo .env...${NC}"
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

# Criar diretório .cursor se não existir
CURSOR_DIR="../.cursor"
if [ ! -d "$CURSOR_DIR" ]; then
    echo -e "${BLUE}📁 Criando diretório .cursor...${NC}"
    mkdir -p "$CURSOR_DIR"
fi

# Criar ou atualizar arquivo mcp.json
MCP_CONFIG="$CURSOR_DIR/mcp.json"
if [ ! -f "$MCP_CONFIG" ]; then
    echo -e "${BLUE}📄 Criando configuração MCP para Cursor...${NC}"
    cat > "$MCP_CONFIG" << 'EOF'
{
  "mcpServers": {
    "sentry": {
      "type": "stdio",
      "command": "./mcp-sentry/start-cursor.sh",
      "args": []
    }
  }
}
EOF
else
    echo -e "${YELLOW}⚠️  Configuração MCP já existe. Atualize manualmente se necessário.${NC}"
fi

echo ""
echo -e "${GREEN}✅ MCP Sentry configurado para o Cursor!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📚 Ferramentas disponíveis no Cursor:${NC}"
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
echo "  • ... e mais 16 ferramentas!"
echo ""
echo -e "${BLUE}💡 Como usar:${NC}"
echo "  1. Reinicie o Cursor"
echo '  2. Use: "Use the sentry tool to list projects"'
echo ""
echo -e "${YELLOW}📍 Localização da configuração:${NC}"
echo "  ${CURSOR_DIR}/mcp.json"
echo ""
echo -e "${GREEN}Para remover: rm ${CURSOR_DIR}/mcp.json${NC}"