#!/bin/bash

echo "🔍 Testando MCPs Turso..."
echo "=========================="

# Testar mcp-turso
echo ""
echo "📦 Testando mcp-turso..."
cd mcp-turso

if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
    echo "📊 Configuração atual:"
    echo "   TURSO_DATABASE_URL: $(grep TURSO_DATABASE_URL .env | cut -d'=' -f2)"
    echo "   TURSO_AUTH_TOKEN: $(grep TURSO_AUTH_TOKEN .env | cut -d'=' -f2 | cut -c1-20)..."
else
    echo "❌ Arquivo .env não encontrado"
fi

# Verificar se compila
if npm run build >/dev/null 2>&1; then
    echo "✅ Compilação: OK"
else
    echo "❌ Compilação: FALHOU"
fi

cd ..

# Testar mcp-turso-cloud
echo ""
echo "☁️ Testando mcp-turso-cloud..."
cd mcp-turso-cloud

if [ -f ".env" ]; then
    echo "✅ Arquivo .env encontrado"
    echo "📊 Configuração atual:"
    echo "   TURSO_ORGANIZATION: $(grep TURSO_ORGANIZATION .env | cut -d'=' -f2)"
    echo "   TURSO_API_TOKEN: $(grep TURSO_API_TOKEN .env | cut -d'=' -f2 | cut -c1-20)..."
else
    echo "❌ Arquivo .env não encontrado"
fi

# Verificar se compila
if npm run build >/dev/null 2>&1; then
    echo "✅ Compilação: OK"
else
    echo "❌ Compilação: FALHOU"
fi

cd ..

echo ""
echo "🔧 Comparação de Dependências:"
echo "=============================="

echo ""
echo "📦 mcp-turso:"
cd mcp-turso
echo "   @libsql/client: $(grep '@libsql/client' package.json | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')"
echo "   @modelcontextprotocol/sdk: $(grep '@modelcontextprotocol/sdk' package.json | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')"
cd ..

echo ""
echo "☁️ mcp-turso-cloud:"
cd mcp-turso-cloud
echo "   @libsql/client: $(grep '@libsql/client' package.json | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')"
echo "   @modelcontextprotocol/sdk: $(grep '@modelcontextprotocol/sdk' package.json | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')"
cd ..

echo ""
echo "📋 Resumo:"
echo "=========="
echo "• mcp-turso: Versão simples, problema de autenticação JWT"
echo "• mcp-turso-cloud: Versão avançada, mais funcionalidades"
echo ""
echo "🎯 Recomendação: Usar mcp-turso-cloud para funcionalidades avançadas"
echo "                 Usar mcp-turso para simplicidade (após resolver autenticação)" 