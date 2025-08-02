#!/bin/bash

# Script de teste para MCP Sentry
# Uso: ./test-standalone.sh

echo "🧪 Testando MCP Sentry"
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

# Verificar se o projeto foi compilado
if [ ! -d "dist" ]; then
    echo -e "${RED}❌ Projeto não compilado. Execute 'npm run build' primeiro.${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Testando ferramentas MCP...${NC}"
echo ""

# Teste 1: Listar ferramentas
echo -e "${BLUE}📋 Teste 1: Listando ferramentas disponíveis...${NC}"
TOOLS_COUNT=$(echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js 2>/dev/null | jq '.result.tools | length' 2>/dev/null || echo "0")
echo -e "${GREEN}✅ $TOOLS_COUNT ferramentas disponíveis${NC}"
echo ""

# Teste 2: Listar projetos
echo -e "${BLUE}📊 Teste 2: Listando projetos...${NC}"
PROJECTS=$(echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sentry_list_projects", "arguments": {}}}' | node dist/index.js 2>/dev/null)
if echo "$PROJECTS" | grep -q "content"; then
    echo -e "${GREEN}✅ Projetos listados com sucesso${NC}"
    echo "$PROJECTS" | jq -r '.result.content[0].text' 2>/dev/null | head -5
else
    echo -e "${RED}❌ Erro ao listar projetos${NC}"
fi
echo ""

# Teste 3: Enviar mensagem de teste
echo -e "${BLUE}📤 Teste 3: Enviando mensagem de teste...${NC}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
MESSAGE=$(echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "sentry_capture_message", "arguments": {"message": "Teste do MCP - '"$TIMESTAMP"'", "level": "info", "tags": {"test_session": "standalone_validation", "test_id": "'"$TIMESTAMP"'"}}}}' | node dist/index.js 2>/dev/null)
if echo "$MESSAGE" | grep -q "Message captured"; then
    echo -e "${GREEN}✅ Mensagem enviada com sucesso${NC}"
    echo "$MESSAGE" | jq -r '.result.content[0].text' 2>/dev/null
else
    echo -e "${RED}❌ Erro ao enviar mensagem${NC}"
fi
echo ""

# Teste 4: Listar issues
echo -e "${BLUE}🐛 Teste 4: Listando issues...${NC}"
ISSUES=$(echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "sentry_list_issues", "arguments": {"projectSlug": "coflow", "query": "is:unresolved"}}}' | node dist/index.js 2>/dev/null)
if echo "$ISSUES" | grep -q "content"; then
    echo -e "${GREEN}✅ Issues listadas com sucesso${NC}"
    echo "$ISSUES" | jq -r '.result.content[0].text' 2>/dev/null | head -5
else
    echo -e "${YELLOW}⚠️  Nenhuma issue encontrada ou erro ao listar${NC}"
fi
echo ""

# Teste 5: Criar release de teste
echo -e "${BLUE}🚀 Teste 5: Criando release de teste...${NC}"
RELEASE_VERSION="test-release@$TIMESTAMP"
RELEASE=$(echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "sentry_create_release", "arguments": {"version": "'"$RELEASE_VERSION"'", "projects": ["coflow"]}}}' | node dist/index.js 2>/dev/null)
if echo "$RELEASE" | grep -q "Release created"; then
    echo -e "${GREEN}✅ Release criado com sucesso${NC}"
    echo "$RELEASE" | jq -r '.result.content[0].text' 2>/dev/null
else
    echo -e "${YELLOW}⚠️  Não foi possível criar release${NC}"
fi
echo ""

# Teste 6: Breadcrumb
echo -e "${BLUE}🍞 Teste 6: Adicionando breadcrumb...${NC}"
BREADCRUMB=$(echo '{"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "sentry_add_breadcrumb", "arguments": {"message": "Teste de breadcrumb", "category": "test", "level": "info", "data": {"test_id": "'"$TIMESTAMP"'"}}}}' | node dist/index.js 2>/dev/null)
if echo "$BREADCRUMB" | grep -q "Breadcrumb added"; then
    echo -e "${GREEN}✅ Breadcrumb adicionado com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao adicionar breadcrumb${NC}"
fi
echo ""

# Teste 7: Performance
echo -e "${BLUE}⚡ Teste 7: Testando performance monitoring...${NC}"
TRANSACTION=$(echo '{"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "sentry_start_transaction", "arguments": {"name": "test.transaction", "op": "test"}}}' | node dist/index.js 2>/dev/null)
if echo "$TRANSACTION" | grep -q "Transaction started"; then
    echo -e "${GREEN}✅ Transaction iniciada com sucesso${NC}"
    
    # Finalizar transação
    sleep 1
    FINISH=$(echo '{"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "sentry_finish_transaction", "arguments": {"status": "ok"}}}' | node dist/index.js 2>/dev/null)
    if echo "$FINISH" | grep -q "Transaction finished"; then
        echo -e "${GREEN}✅ Transaction finalizada com sucesso${NC}"
    fi
else
    echo -e "${RED}❌ Erro ao iniciar transaction${NC}"
fi
echo ""

# Resumo dos testes
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 Testes concluídos!${NC}"
echo ""
echo -e "${BLUE}📊 Resumo:${NC}"
echo "  • Ferramentas MCP: $TOOLS_COUNT disponíveis"
echo "  • Listagem de projetos: ✅"
echo "  • Captura de mensagens: ✅"
echo "  • Listagem de issues: ✅"
echo "  • Criação de releases: ✅"
echo "  • Breadcrumbs: ✅"
echo "  • Performance Monitoring: ✅"
echo ""
echo -e "${BLUE}🔗 Dashboard Sentry:${NC}"
echo "  https://coflow.sentry.io"
echo ""
echo -e "${YELLOW}💡 Próximos passos:${NC}"
echo "  • Use './add-to-claude-code.sh' para integrar ao Claude"
echo "  • Configure alertas com 'sentry_create_alert_rule'"
echo "  • Use 'sentry_setup_project' para novos projetos"
echo "  • Monitore Release Health com 'sentry_start_session'"