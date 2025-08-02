#!/bin/bash
# 📄 Script para Visualizar Logs do PRP Agent
# ============================================

echo "📄 LOGS DO PRP AGENT"
echo "===================="

if [ ! -f "prp-agent.log" ]; then
    echo "❌ Arquivo de log não encontrado!"
    echo "💡 O servidor precisa estar rodando em background"
    echo "🚀 Execute: ./start.sh e escolha opção 2"
    exit 1
fi

echo "📁 Arquivo: prp-agent.log"
echo "📏 Tamanho: $(du -h prp-agent.log | cut -f1)"
echo ""

# Menu de opções
echo "🎯 O que deseja fazer?"
echo "1) Ver últimas 20 linhas"
echo "2) Ver últimas 50 linhas"
echo "3) Acompanhar logs em tempo real (tail -f)"
echo "4) Ver logs completos"
echo "5) Filtrar erros (ERROR/Exception)"
echo "6) Filtrar requests (GET/POST)"
echo -n "Escolha (1-6): "
read -r option

case $option in
    1)
        echo "📋 Últimas 20 linhas:"
        echo "====================="
        tail -20 prp-agent.log
        ;;
    2)
        echo "📋 Últimas 50 linhas:"
        echo "====================="
        tail -50 prp-agent.log
        ;;
    3)
        echo "🔄 Acompanhando logs em tempo real..."
        echo "💡 Use Ctrl+C para parar"
        echo "=========================="
        tail -f prp-agent.log
        ;;
    4)
        echo "📖 Logs completos:"
        echo "=================="
        cat prp-agent.log
        ;;
    5)
        echo "🚨 Filtrando erros:"
        echo "=================="
        grep -i "error\|exception\|traceback" prp-agent.log
        ;;
    6)
        echo "🌐 Filtrando requests:"
        echo "===================="
        grep -E "GET|POST|PUT|DELETE" prp-agent.log
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac