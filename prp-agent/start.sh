#!/bin/bash
# 🚀 Script de Inicialização do PRP Agent com Sentry
# ===================================================

echo "🚀 Iniciando PRP Agent com Sentry + FastAPI..."

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Erro: main.py não encontrado!"
    echo "💡 Execute este script do diretório prp-agent/"
    exit 1
fi

# Verificar se o ambiente UV existe
if [ ! -d ".venv" ]; then
    echo "❌ Erro: Ambiente UV (.venv) não encontrado!"
    echo "💡 Execute: uv init && uv add sentry-sdk[fastapi] fastapi uvicorn"
    exit 1
fi

# Ativar ambiente UV
echo "📦 Ativando ambiente UV..."
source .venv/bin/activate

# Verificar se há processo rodando na porta 8000
PID=$(lsof -ti:8000)
if [ ! -z "$PID" ]; then
    echo "⚠️  Processo já rodando na porta 8000 (PID: $PID)"
    echo "❓ Deseja parar e reiniciar? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🛑 Parando processo anterior..."
        kill $PID
        sleep 2
    else
        echo "❌ Cancelado. Use ./stop.sh para parar o processo atual."
        exit 1
    fi
fi

# Verificar configuração Sentry
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando configuração básica..."
    echo "SENTRY_DSN=https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832" > .env
fi

# Escolher modo de execução
echo ""
echo "🎯 Como deseja executar?"
echo "1) Foreground (logs visíveis, Ctrl+C para parar)"
echo "2) Background (daemon, use ./stop.sh para parar)"
echo -n "Escolha (1 ou 2): "
read -r mode

case $mode in
    1)
        echo "🖥️  Executando em foreground..."
        echo "💡 Use Ctrl+C para parar"
        echo "🌐 Acesse: http://localhost:8000"
        echo "🐛 Debug: http://localhost:8000/sentry-debug"
        echo ""
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    2)
        echo "🔄 Executando em background..."
        nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > prp-agent.log 2>&1 &
        PID=$!
        echo $PID > prp-agent.pid
        
        echo "✅ PRP Agent iniciado!"
        echo "📋 PID: $PID"
        echo "📄 Logs: tail -f prp-agent.log"
        echo "🌐 URL: http://localhost:8000"
        echo "🐛 Debug: http://localhost:8000/sentry-debug"
        echo "🛑 Parar: ./stop.sh"
        
        # Aguardar inicialização
        echo "⏳ Aguardando inicialização..."
        sleep 3
        
        # Testar se está respondendo
        if curl -s http://localhost:8000/ > /dev/null; then
            echo "🎉 Servidor online e respondendo!"
        else
            echo "❌ Servidor pode não ter iniciado corretamente"
            echo "📄 Verifique os logs: tail -f prp-agent.log"
        fi
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac