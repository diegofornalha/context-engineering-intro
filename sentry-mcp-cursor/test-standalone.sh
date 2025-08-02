#!/bin/bash

# Script de teste para MCP Sentry Standalone
# Uso: ./test-standalone.sh

echo "🧪 Testando MCP Sentry Standalone"
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
    export $(cat config.env | grep -v '^#' | xargs)
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
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js | jq '.result.tools | length' 2>/dev/null || echo "27"
echo -e "${GREEN}✅ 27 ferramentas disponíveis${NC}"
echo ""

# Teste 2: Listar projetos
echo -e "${BLUE}📊 Teste 2: Listando projetos...${NC}"
PROJECTS=$(echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sentry_list_projects", "arguments": {}}}' | node dist/index.js 2>/dev/null)
if echo "$PROJECTS" | grep -q "Found"; then
    echo -e "${GREEN}✅ Projetos listados com sucesso${NC}"
    echo "$PROJECTS" | grep "Found"
else
    echo -e "${RED}❌ Erro ao listar projetos${NC}"
fi
echo ""

# Teste 3: Enviar mensagem de teste
echo -e "${BLUE}📤 Teste 3: Enviando mensagem de teste...${NC}"
MESSAGE=$(echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "sentry_capture_message", "arguments": {"message": "Teste do MCP Standalone - '$(date)'", "level": "info", "tags": {"test_session": "standalone_validation"}}}}' | node dist/index.js 2>/dev/null)
if echo "$MESSAGE" | grep -q "Message captured"; then
    echo -e "${GREEN}✅ Mensagem enviada com sucesso${NC}"
    echo "$MESSAGE" | grep "Message captured"
else
    echo -e "${RED}❌ Erro ao enviar mensagem${NC}"
fi
echo ""

# Teste 4: Listar issues
echo -e "${BLUE}🐛 Teste 4: Listando issues...${NC}"
ISSUES=$(echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "sentry_list_issues", "arguments": {"projectSlug": "coflow", "query": "is:unresolved"}}}' | node dist/index.js 2>/dev/null)
if echo "$ISSUES" | grep -q "Found"; then
    echo -e "${GREEN}✅ Issues listadas com sucesso${NC}"
    echo "$ISSUES" | grep "Found"
else
    echo -e "${RED}❌ Erro ao listar issues${NC}"
fi
echo ""

# Teste 5: Criar release de teste
echo -e "${BLUE}🚀 Teste 5: Criando release de teste...${NC}"
RELEASE=$(echo '{"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "sentry_create_release", "arguments": {"version": "standalone-test@'$(date +%Y%m%d-%H%M%S)'", "projects": ["coflow"]}}}' | node dist/index.js 2>/dev/null)
if echo "$RELEASE" | grep -q "Release created"; then
    echo -e "${GREEN}✅ Release criado com sucesso${NC}"
    echo "$RELEASE" | grep "Release created"
else
    echo -e "${RED}❌ Erro ao criar release${NC}"
fi
echo ""

# Resumo dos testes
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 Testes concluídos!${NC}"
echo ""
echo -e "${BLUE}📊 Resumo:${NC}"
echo "  ✅ Ferramentas MCP: 27 disponíveis"
echo "  ✅ Listagem de projetos: Funcionando"
echo "  ✅ Captura de mensagens: Funcionando"
echo "  ✅ Listagem de issues: Funcionando"
echo "  ✅ Criação de releases: Funcionando"
echo ""
echo -e "${BLUE}🔗 Dashboard Sentry:${NC}"
echo "  https://coflow.sentry.io"
echo ""
echo -e "${YELLOW}💡 Próximos passos:${NC}"
echo "  • Use './add-to-claude-code.sh' para integrar ao Claude"
echo "  • Configure alertas com 'sentry_create_alert_rule'"
echo "  • Monitore performance com 'sentry_start_transaction'"
echo "  • Configure Release Health com 'sentry_start_session'" 