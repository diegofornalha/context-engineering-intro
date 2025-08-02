#!/bin/bash

# Script de monitoramento para MCP Turso Cloud
# Uso: ./monitor.sh

echo "📊 Monitor MCP Turso Cloud"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Verificar se estamos no diretório correto
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Função para exibir estatísticas
show_stats() {
    clear
    echo -e "${BLUE}📊 MCP Turso Cloud Monitor - $(date)${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Status do servidor MCP
    echo -e "${BLUE}🔍 Status do Servidor MCP:${NC}"
    if pgrep -f "node dist/index.js" > /dev/null; then
        echo -e "  ${GREEN}✅ Servidor MCP: Ativo${NC}"
        PID=$(pgrep -f "node dist/index.js")
        echo -e "  ${BLUE}📝 PID: $PID${NC}"
    else
        echo -e "  ${RED}❌ Servidor MCP: Inativo${NC}"
    fi
    
    # Verificar configuração no Cursor
    echo -e "${BLUE}🔧 Configuração Cursor:${NC}"
    if [ -f "../.cursor/mcp.json" ]; then
        if grep -q "mcp-turso-cloud" "../.cursor/mcp.json"; then
            echo -e "  ${GREEN}✅ Configurado no Cursor${NC}"
        else
            echo -e "  ${YELLOW}⚠️  Não configurado no Cursor${NC}"
        fi
    fi
    echo ""
    
    # Informações do Turso
    echo -e "${BLUE}🗄️  Informações Turso:${NC}"
    echo -e "  ${CYAN}Organização:${NC} ${TURSO_ORGANIZATION:-diegofornalha}"
    echo -e "  ${CYAN}Database:${NC} ${TURSO_DEFAULT_DATABASE:-cursor10x-memory}"
    echo -e "  ${CYAN}URL:${NC} ${TURSO_DATABASE_URL:-libsql://cursor10x-memory-diegofornalha.aws-us-east-1.turso.io}"
    echo ""
    
    # Testar conexão com Turso
    echo -e "${BLUE}🔗 Teste de Conexão:${NC}"
    if [ -f "dist/index.js" ]; then
        # Teste rápido de listagem de ferramentas
        TOOLS=$(echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js 2>/dev/null | jq -r '.result.tools | length' 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✅ Ferramentas disponíveis: $TOOLS${NC}"
    else
        echo -e "  ${RED}❌ Servidor não compilado${NC}"
    fi
    echo ""
    
    # Testar listagem de bancos
    echo -e "${BLUE}📋 Bancos Disponíveis:${NC}"
    if [ -f "dist/index.js" ]; then
        DATABASES=$(echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "list_databases", "arguments": {}}}' | node dist/index.js 2>/dev/null | jq -r '.result.content[0].text' 2>/dev/null | head -5 || echo "Não disponível")
        echo "  $DATABASES"
    else
        echo -e "  ${RED}❌ Servidor não compilado${NC}"
    fi
    echo ""
    
    # Testar listagem de tabelas
    echo -e "${BLUE}📊 Tabelas no Database:${NC}"
    if [ -f "dist/index.js" ]; then
        TABLES=$(echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "list_tables", "arguments": {"database": "cursor10x-memory"}}}' | node dist/index.js 2>/dev/null | jq -r '.result.content[0].text' 2>/dev/null | head -10 || echo "Não disponível")
        echo "  $TABLES"
    else
        echo -e "  ${RED}❌ Servidor não compilado${NC}"
    fi
    echo ""
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}Pressione Ctrl+C para sair | Atualização a cada 30s${NC}"
}

# Loop de monitoramento
while true; do
    show_stats
    sleep 30
done 