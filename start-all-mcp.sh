#!/bin/bash

# Script para iniciar todos os servidores MCP
echo "🚀 Iniciando todos os servidores MCP..."

# Função para verificar se um processo está rodando
check_process() {
    local process_name=$1
    if pgrep -f "$process_name" > /dev/null; then
        echo "✅ $process_name já está rodando"
        return 0
    else
        echo "❌ $process_name não está rodando"
        return 1
    fi
}

# Função para verificar se um servidor MCP está rodando
check_mcp_server() {
    local server_type=$1
    if pgrep -f "node.*dist/index.js" > /dev/null; then
        echo "✅ $server_type MCP está rodando"
        return 0
    else
        echo "❌ $server_type MCP não está rodando"
        return 1
    fi
}

# Função para iniciar um servidor
start_server() {
    local server_name=$1
    local script_path=$2
    local process_name=$3
    
    echo "🔧 Iniciando $server_name..."
    
    if [ -f "$script_path" ]; then
        cd "$(dirname "$script_path")"
        chmod +x "$(basename "$script_path")"
        "./$(basename "$script_path")" &
        sleep 2
        
        if check_process "$process_name"; then
            echo "✅ $server_name iniciado com sucesso!"
        else
            echo "❌ Falha ao iniciar $server_name"
        fi
    else
        echo "❌ Script não encontrado: $script_path"
    fi
}

# Verificar status atual
echo "📊 Status atual dos servidores:"
check_mcp_server "Sentry" || echo "   Sentry: Inativo"
check_mcp_server "Turso" || echo "   Turso: Inativo"

echo ""

# Iniciar Sentry MCP
start_server "Sentry MCP" "./mcp-sentry/start-mcp.sh" "node.*sentry"

echo ""

# Iniciar Turso MCP  
start_server "Turso MCP" "./mcp-turso/dist/index.js" "node.*turso"

echo ""

# Status final
echo "📋 Status final:"
check_mcp_server "Sentry" || echo "   Sentry: ❌ Inativo"
check_mcp_server "Turso" || echo "   Turso: ❌ Inativo"

echo ""
echo "🎯 Próximos passos:"
echo "1. Reinicie o Cursor se necessário"
echo "2. Teste as ferramentas:"
echo "   - Sentry: sentry_list_projects, sentry_capture_message"
echo "   - Turso: turso_list_databases, turso_execute_query"
echo ""
echo "✅ Script concluído!" 