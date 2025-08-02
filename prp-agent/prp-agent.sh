#!/bin/bash
# 🤖 PRP Agent - Script de Gerenciamento Principal
# ================================================

echo "🤖 PRP AGENT - GERENCIAMENTO"
echo "============================"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Erro: Execute este script do diretório prp-agent/"
    exit 1
fi

# Menu principal
show_menu() {
    echo "🎯 O que deseja fazer?"
    echo ""
    echo "📊 MONITORAMENTO:"
    echo "  1) 📈 Status do servidor"
    echo "  2) 📄 Ver logs"
    echo "  3) 🧪 Executar testes"
    echo ""
    echo "🔧 CONTROLE:"
    echo "  4) 🚀 Iniciar servidor"
    echo "  5) 🛑 Parar servidor"  
    echo "  6) 🔄 Reiniciar servidor"
    echo ""
    echo "🔗 ACESSO RÁPIDO:"
    echo "  7) 🌐 Abrir no navegador"
    echo "  8) 🐛 Testar Sentry debug"
    echo ""
    echo "  9) ❓ Ajuda"
    echo "  0) 🚪 Sair"
    echo ""
    echo -n "Digite sua escolha (0-9): "
}

# Função para abrir no navegador (macOS)
open_browser() {
    if command -v open > /dev/null; then
        echo "🌐 Abrindo http://localhost:8000 no navegador..."
        open http://localhost:8000
    else
        echo "🔗 Acesse: http://localhost:8000"
    fi
}

# Função de ajuda
show_help() {
    echo ""
    echo "📖 AJUDA - PRP AGENT"
    echo "===================="
    echo ""
    echo "🚀 SCRIPTS DISPONÍVEIS:"
    echo "  ./start.sh    - Iniciar servidor (foreground/background)"
    echo "  ./stop.sh     - Parar servidor"
    echo "  ./restart.sh  - Reiniciar servidor"
    echo "  ./status.sh   - Ver status completo"
    echo "  ./logs.sh     - Ver/acompanhar logs"
    echo "  ./test.sh     - Executar bateria de testes"
    echo ""
    echo "🌐 ENDPOINTS PRINCIPAIS:"
    echo "  http://localhost:8000/           - Status da aplicação"
    echo "  http://localhost:8000/sentry-debug - Teste de erro (Sentry)"
    echo ""
    echo "🔍 SENTRY MONITORING:"
    echo "  Dashboard: https://sentry.io/organizations/coflow/projects/"
    echo "  Busque por: ZeroDivisionError, performance transactions"
    echo ""
    echo "📁 ARQUIVOS IMPORTANTES:"
    echo "  main.py       - Aplicação FastAPI + Sentry"
    echo "  .env          - Configuração Sentry DSN"
    echo "  pyproject.toml - Dependências UV"
    echo "  .venv/        - Ambiente virtual UV"
    echo ""
    echo "🆘 SOLUÇÃO DE PROBLEMAS:"
    echo "  • Servidor não inicia: Verifique se porta 8000 está livre"
    echo "  • Imports falhando: Execute 'source .venv/bin/activate'"
    echo "  • Sentry não funciona: Verifique DSN no arquivo .env"
    echo ""
}

# Loop principal
while true; do
    show_menu
    read -r choice
    echo ""
    
    case $choice in
        1)
            echo "📊 Executando verificação de status..."
            ./status.sh
            ;;
        2)
            echo "📄 Abrindo visualizador de logs..."
            ./logs.sh
            ;;
        3)
            echo "🧪 Executando bateria de testes..."
            ./test.sh
            ;;
        4)
            echo "🚀 Iniciando servidor..."
            ./start.sh
            ;;
        5)
            echo "🛑 Parando servidor..."
            ./stop.sh
            ;;
        6)
            echo "🔄 Reiniciando servidor..."
            ./restart.sh
            ;;
        7)
            open_browser
            ;;
        8)
            echo "🐛 Testando endpoint Sentry debug..."
            if curl -s http://localhost:8000/ > /dev/null; then
                echo "🔗 Executando: curl http://localhost:8000/sentry-debug"
                curl -v http://localhost:8000/sentry-debug
                echo ""
                echo "✅ Erro enviado para Sentry! Verifique o dashboard."
            else
                echo "❌ Servidor não está rodando. Execute opção 4 primeiro."
            fi
            ;;
        9)
            show_help
            ;;
        0)
            echo "👋 Saindo do gerenciador PRP Agent..."
            echo "💡 Use ./prp-agent.sh para voltar a este menu"
            exit 0
            ;;
        *)
            echo "❌ Opção inválida! Digite um número de 0 a 9."
            ;;
    esac
    
    echo ""
    echo "⏸️  Pressione Enter para continuar..."
    read
    echo ""
done