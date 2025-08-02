#!/bin/bash

# Script de monitoramento para MCP Sentry Cursor
# Uso: ./monitor.sh

echo "📊 Monitor MCP Sentry (Cursor)"
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

# Carregar configurações
if [ -f "config.env" ]; then
    set -a
    source config.env
    set +a
fi

# Função para exibir estatísticas
show_stats() {
    clear
    echo -e "${BLUE}📊 MCP Sentry Monitor (Cursor) - $(date)${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Verificar status do servidor
    echo -e "${BLUE}🔍 Status do Servidor:${NC}"
    if pgrep -f "node dist/index.js" > /dev/null; then
        echo -e "  ${GREEN}✅ Servidor MCP: Ativo${NC}"
        PID=$(pgrep -f "node dist/index.js")
        echo -e "  ${BLUE}📝 PID: $PID${NC}"
    else
        echo -e "  ${RED}❌ Servidor MCP: Inativo${NC}"
    fi
    
    # Verificar configuração no Cursor
    if [ -f "../.cursor/mcp.json" ]; then
        if grep -q "sentry-mcp-cursor" "../.cursor/mcp.json"; then
            echo -e "  ${GREEN}✅ Configurado no Cursor${NC}"
        else
            echo -e "  ${YELLOW}⚠️  Não configurado no Cursor${NC}"
        fi
    fi
    echo ""
    
    # Estatísticas da organização
    echo -e "${BLUE}📈 Estatísticas (últimas 24h):${NC}"
    STATS=$(echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "sentry_get_organization_stats", "arguments": {"stat": "received", "resolution": "1h", "since": "24h"}}}' | node dist/index.js 2>/dev/null | jq -r '.result.content[0].text' 2>/dev/null || echo "Não disponível")
    echo "  $STATS" | head -5
    echo ""
    
    # Issues não resolvidas
    echo -e "${BLUE}🐛 Issues Não Resolvidas:${NC}"
    ISSUES=$(echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sentry_list_issues", "arguments": {"projectSlug": "coflow", "query": "is:unresolved"}}}' | node dist/index.js 2>/dev/null | jq -r '.result.content[0].text' 2>/dev/null | head -10 || echo "Não disponível")
    echo "  $ISSUES"
    echo ""
    
    # Última release
    echo -e "${BLUE}🚀 Última Release:${NC}"
    RELEASE=$(echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "sentry_list_releases", "arguments": {"projectSlug": "coflow"}}}' | node dist/index.js 2>/dev/null | jq -r '.result.content[0].text' 2>/dev/null | head -5 || echo "Não disponível")
    echo "  $RELEASE"
    echo ""
    
    # Ferramentas disponíveis
    echo -e "${BLUE}🔧 Ferramentas MCP:${NC}"
    TOOLS=$(echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/list", "params": {}}' | node dist/index.js 2>/dev/null | jq -r '.result.tools | length' 2>/dev/null || echo "0")
    echo -e "  Total: ${GREEN}$TOOLS ferramentas disponíveis${NC}"
    echo ""
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}Pressione Ctrl+C para sair | Atualização a cada 30s${NC}"
}

# Loop de monitoramento
while true; do
    show_stats
    sleep 30
done