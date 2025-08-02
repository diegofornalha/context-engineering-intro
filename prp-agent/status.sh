#!/bin/bash
# 📊 Script de Status do PRP Agent
# ================================

echo "📊 STATUS DO PRP AGENT"
echo "======================"

# Verificar PID file
if [ -f "prp-agent.pid" ]; then
    PID=$(cat prp-agent.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Status: RODANDO"
        echo "📋 PID: $PID"
        echo "⏰ Uptime: $(ps -o etime= -p $PID | tr -d ' ')"
        echo "💾 Memória: $(ps -o rss= -p $PID | tr -d ' ')KB"
    else
        echo "❌ Status: PARADO (PID file órfão)"
        rm -f prp-agent.pid
    fi
else
    PID=$(lsof -ti:8000)
    if [ ! -z "$PID" ]; then
        echo "⚠️  Status: RODANDO (sem PID file)"
        echo "📋 PID: $PID"
    else
        echo "❌ Status: PARADO"
    fi
fi

# Verificar porta
echo ""
echo "🌐 CONECTIVIDADE"
echo "================="
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Servidor: RESPONDENDO"
    echo "🔗 URL: http://localhost:8000"
    
    # Testar endpoint debug
    if curl -s http://localhost:8000/sentry-debug > /dev/null 2>&1; then
        echo "🐛 Debug: DISPONÍVEL (http://localhost:8000/sentry-debug)"
    fi
else
    echo "❌ Servidor: NÃO RESPONDENDO"
fi

# Verificar logs
echo ""
echo "📄 LOGS"
echo "======="
if [ -f "prp-agent.log" ]; then
    echo "📁 Arquivo: prp-agent.log"
    echo "📏 Tamanho: $(du -h prp-agent.log | cut -f1)"
    echo "🕐 Última modificação: $(stat -f "%Sm" prp-agent.log)"
    echo ""
    echo "📋 Últimas 5 linhas:"
    tail -5 prp-agent.log
else
    echo "ℹ️  Nenhum arquivo de log encontrado"
fi

# Verificar ambiente
echo ""
echo "🔧 AMBIENTE"
echo "==========="
if [ -d ".venv" ]; then
    echo "✅ UV Environment: DISPONÍVEL"
else
    echo "❌ UV Environment: NÃO ENCONTRADO"
fi

if [ -f ".env" ]; then
    echo "✅ Configuração: .env DISPONÍVEL"
else
    echo "❌ Configuração: .env NÃO ENCONTRADO"
fi

if [ -f "main.py" ]; then
    echo "✅ Aplicação: main.py DISPONÍVEL"
else
    echo "❌ Aplicação: main.py NÃO ENCONTRADO"
fi