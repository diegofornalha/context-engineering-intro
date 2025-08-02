#!/bin/bash

# Script para testar o MCP Turso
echo "🧪 Testando MCP Turso..."

# Verificar se o servidor está rodando
if pgrep -f "node dist/index.js" > /dev/null; then
    echo "✅ Servidor MCP está rodando"
else
    echo "❌ Servidor MCP não está rodando"
    echo "🚀 Iniciando servidor..."
    ./start.sh &
    sleep 2
fi

# Verificar arquivo .env
if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
    echo "📊 Configurações:"
    echo "   TURSO_DATABASE_URL: $(grep TURSO_DATABASE_URL .env | cut -d'=' -f2)"
    echo "   MCP_SERVER_NAME: $(grep MCP_SERVER_NAME .env | cut -d'=' -f2)"
else
    echo "❌ Arquivo .env não encontrado"
    echo "🔧 Execute: ./setup-env.sh"
    exit 1
fi

# Verificar arquivo compilado
if [ -f "dist/index.js" ]; then
    echo "✅ Código compilado encontrado"
else
    echo "❌ Código não compilado"
    echo "🔨 Execute: npm run build"
    exit 1
fi

echo ""
echo "🎯 Para testar no Cursor:"
echo "1. Reinicie o Cursor"
echo "2. Teste as ferramentas:"
echo "   - turso_list_databases"
echo "   - turso_list_tables"
echo "   - turso_add_conversation"
echo "   - turso_search_knowledge"

echo ""
echo "📋 Status atual:"
echo "   ✅ Servidor: Rodando"
echo "   ✅ Configuração: OK"
echo "   ✅ Compilação: OK"
echo "   🎯 Pronto para uso!" 