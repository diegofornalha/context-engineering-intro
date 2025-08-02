#!/bin/bash

# Script para testar MCP Sentry no formato Cursor
echo "🧪 Testando MCP Sentry para Cursor..."
echo ""

cd "$(dirname "$0")"

# Testar com requisição tools/list
echo "📋 Testando listagem de ferramentas..."
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | ./start-cursor.sh 2>/dev/null | jq '.result.tools | length'

echo ""
echo "✅ Se você viu o número 27, o servidor está funcionando!"
echo "   (27 ferramentas Sentry disponíveis)"
echo ""
echo "📝 Configuração do Cursor em: ../.cursor/mcp.json"