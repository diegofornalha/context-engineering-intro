#!/bin/bash

echo "🔍 DIAGNÓSTICO DO MCP TURSO CLOUD"
echo "=================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "📁 Verificando arquivos:"
echo "  ✅ start-claude.sh existe: $([ -f "start-claude.sh" ] && echo "SIM" || echo "NÃO")"
echo "  ✅ dist/index.js existe: $([ -f "dist/index.js" ] && echo "SIM" || echo "NÃO")"
echo "  ✅ package.json existe: $([ -f "package.json" ] && echo "SIM" || echo "NÃO")"

echo ""
echo "🔧 Testando script de inicialização:"
echo "  Executando: ./start-claude.sh"
echo ""

# Testar o script de inicialização
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | ./start-claude.sh 2>&1 | head -20

echo ""
echo "🌐 Verificando configuração Turso:"
echo "  Organização: ${TURSO_ORGANIZATION:-diegofornalha}"
echo "  Database: ${TURSO_DEFAULT_DATABASE:-cursor10x-memory}"
echo "  URL: ${TURSO_DATABASE_URL:-libsql://cursor10x-memory-diegofornalha.aws-us-east-1.turso.io}"

echo ""
echo "📋 Configuração MCP atual:"
echo "  Arquivo: .cursor/mcp.json"
echo "  Comando: ./mcp-turso-cloud/start-claude.sh"

echo ""
echo "🔍 Verificando dependências:"
if command -v node &> /dev/null; then
    echo "  ✅ Node.js: $(node --version)"
else
    echo "  ❌ Node.js: NÃO INSTALADO"
fi

if command -v npm &> /dev/null; then
    echo "  ✅ npm: $(npm --version)"
else
    echo "  ❌ npm: NÃO INSTALADO"
fi

if command -v jq &> /dev/null; then
    echo "  ✅ jq: $(jq --version)"
else
    echo "  ❌ jq: NÃO INSTALADO"
fi

echo ""
echo "📦 Verificando node_modules:"
if [ -d "node_modules" ]; then
    echo "  ✅ node_modules: Presente"
else
    echo "  ❌ node_modules: Ausente (execute: npm install)"
fi

echo ""
echo "🚀 PRÓXIMOS PASSOS:"
echo "  1. Se houver erros, execute: npm install && npm run build"
echo "  2. Feche COMPLETAMENTE o Cursor"
echo "  3. Abra o Cursor novamente"
echo "  4. Verifique se o Turso MCP mostra as 9 ferramentas"
echo "  5. Execute: ./test.sh para testes completos"
echo "  6. Execute: ./monitor.sh para monitoramento" 