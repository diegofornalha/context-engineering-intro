#!/bin/bash

# Script rápido para desenvolvimento
# Uso: ./dev.sh

cd "$(dirname "$0")"

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo -e "${BLUE}🚀 Sentry React Demo - Modo Desenvolvimento${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Dashboard: https://coflow.sentry.io"
echo "🔧 Projeto: coflow"
echo "🌐 Local: http://localhost:3000"
echo ""
echo -e "${GREEN}Botões de teste disponíveis:${NC}"
echo "  💥 Break the world - Testa captura de erros"
echo "  📨 Send Test Message - Envia mensagem"
echo "  📊 Test Performance - Monitora performance"
echo "  ⚠️  Abnormal Session - Simula sessão anormal"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar dependências
if [ ! -d "node_modules" ]; then
    npm install
fi

# Iniciar
exec npm start