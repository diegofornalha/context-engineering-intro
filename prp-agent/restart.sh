#!/bin/bash
# 🔄 Script para Reiniciar o PRP Agent
# ====================================

echo "🔄 Reiniciando PRP Agent..."

# Parar se estiver rodando
if [ -f "prp-agent.pid" ] || [ ! -z "$(lsof -ti:8000)" ]; then
    echo "🛑 Parando processo atual..."
    ./stop.sh
    echo "⏳ Aguardando 2 segundos..."
    sleep 2
fi

# Iniciar novamente
echo "🚀 Iniciando novamente..."
./start.sh