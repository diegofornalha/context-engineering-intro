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

# Verificar se o projeto foi compilado
if [ ! -d "dist" ]; then
    echo -e "${BLUE}📦 Compilando projeto...${NC}"
    npm install && npm run build
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erro na compilação${NC}"
        exit 1
    fi
fi

# Criar diretório .cursor se não existir
CURSOR_DIR="../.cursor"
if [ ! -d "$CURSOR_DIR" ]; then
    echo -e "${BLUE}📁 Criando diretório .cursor...${NC}"
    mkdir -p "$CURSOR_DIR"
fi

# Fazer backup do mcp.json se existir
if [ -f "$CURSOR_DIR/mcp.json" ]; then
    echo -e "${BLUE}💾 Fazendo backup do mcp.json existente...${NC}"
    cp "$CURSOR_DIR/mcp.json" "$CURSOR_DIR/mcp.json.backup.$(date +%Y%m%d-%H%M%S)"
fi

# Criar ou atualizar mcp.json
echo -e "${BLUE}📝 Configurando mcp.json...${NC}"

# Se o arquivo existe, precisamos fazer merge
if [ -f "$CURSOR_DIR/mcp.json" ]; then
    # Usar jq para fazer merge mantendo outras configurações
    if command -v jq &> /dev/null; then
        jq '.mcpServers.sentry = {
            "type": "stdio",
            "command": "./sentry-mcp-cursor/start-cursor.sh",
            "args": []
        }' "$CURSOR_DIR/mcp.json" > "$CURSOR_DIR/mcp.json.tmp" && \
        mv "$CURSOR_DIR/mcp.json.tmp" "$CURSOR_DIR/mcp.json"
    else
        # Fallback manual se jq não estiver disponível
        echo -e "${YELLOW}⚠️  jq não encontrado. Criando configuração manual...${NC}"
        cat > "$CURSOR_DIR/mcp.json" << EOF
{
  "mcpServers": {
    "sentry": {
      "type": "stdio",
      "command": "./sentry-mcp-cursor/start-cursor.sh",
      "args": []
    }
  }
}
EOF
    fi
else
    # Criar novo arquivo
    cat > "$CURSOR_DIR/mcp.json" << EOF
{
  "mcpServers": {
    "sentry": {
      "type": "stdio",
      "command": "./sentry-mcp-cursor/start-cursor.sh",
      "args": []
    }
  }
}
EOF
fi

echo -e "${GREEN}✅ Configuração salva em $CURSOR_DIR/mcp.json${NC}"

# Verificar configuração
echo ""
echo -e "${BLUE}📊 Configuração atual:${NC}"
if command -v jq &> /dev/null; then
    jq '.mcpServers.sentry' "$CURSOR_DIR/mcp.json" 2>/dev/null
else
    grep -A3 "sentry" "$CURSOR_DIR/mcp.json"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 MCP Sentry adicionado ao Cursor com sucesso!${NC}"
echo ""
echo -e "${BLUE}📚 Próximos passos:${NC}"
echo "  1. Reinicie o Cursor para carregar o MCP"
echo "  2. Verifique se o MCP aparece no Cursor"
echo "  3. Use as ferramentas com o prefixo mcp__sentry__"
echo ""
echo -e "${BLUE}🧪 Para testar:${NC}"
echo "  ./test-standalone.sh"
echo ""
echo -e "${BLUE}📊 Para monitorar:${NC}"
echo "  ./monitor.sh"
echo ""
echo -e "${YELLOW}💡 Dica: As ferramentas estarão disponíveis como:${NC}"
echo "  • mcp__sentry__sentry_capture_exception"
echo "  • mcp__sentry__sentry_list_projects"
echo "  • mcp__sentry__sentry_create_release"
echo "  • E mais 24 ferramentas..."