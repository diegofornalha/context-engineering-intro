#!/bin/bash

# Script para resolver problemas de autenticação do Turso MCP
# Data: 02/08/2025

echo "🔧 Iniciando diagnóstico e correção do Turso MCP..."
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# 1. Verificar se o Turso CLI está instalado
print_status $BLUE "1. Verificando instalação do Turso CLI..."
if command -v turso &> /dev/null; then
    print_status $GREEN "✅ Turso CLI encontrado"
    turso_version=$(turso --version)
    print_status $BLUE "   Versão: $turso_version"
else
    print_status $RED "❌ Turso CLI não encontrado"
    print_status $YELLOW "   Instalando Turso CLI..."
    brew install tursodatabase/tap/turso
    if [ $? -eq 0 ]; then
        print_status $GREEN "✅ Turso CLI instalado com sucesso"
    else
        print_status $RED "❌ Falha na instalação do Turso CLI"
        exit 1
    fi
fi

echo ""

# 2. Verificar status atual da autenticação
print_status $BLUE "2. Verificando status da autenticação..."
auth_status=$(turso auth status 2>&1)
if [[ $auth_status == *"You are logged in"* ]]; then
    print_status $GREEN "✅ Usuário autenticado"
    echo "   $auth_status"
else
    print_status $YELLOW "⚠️  Usuário não autenticado ou problema detectado"
    echo "   $auth_status"
fi

echo ""

# 3. Verificar tokens existentes
print_status $BLUE "3. Verificando tokens existentes..."
tokens_output=$(turso db tokens list 2>&1)
if [[ $tokens_output == *"No tokens found"* ]] || [[ $tokens_output == *"error"* ]]; then
    print_status $YELLOW "⚠️  Nenhum token encontrado ou erro na listagem"
    echo "   $tokens_output"
else
    print_status $GREEN "✅ Tokens encontrados"
    echo "   $tokens_output"
fi

echo ""

# 4. Verificar bancos de dados
print_status $BLUE "4. Verificando bancos de dados..."
db_output=$(turso db list 2>&1)
if [[ $db_output == *"error"* ]] || [[ $db_output == *"could not parse jwt"* ]]; then
    print_status $RED "❌ Erro ao listar bancos de dados"
    echo "   $db_output"
    echo ""
    print_status $YELLOW "🔧 Tentando reautenticação..."
    
    # 5. Tentar reautenticação
    print_status $BLUE "5. Fazendo logout..."
    turso auth logout
    
    print_status $BLUE "6. Fazendo login..."
    turso auth login
    
    print_status $BLUE "7. Verificando status após reautenticação..."
    new_auth_status=$(turso auth status 2>&1)
    if [[ $new_auth_status == *"You are logged in"* ]]; then
        print_status $GREEN "✅ Reautenticação bem-sucedida"
        echo "   $new_auth_status"
        
        print_status $BLUE "8. Testando listagem de bancos novamente..."
        new_db_output=$(turso db list 2>&1)
        if [[ $new_db_output != *"error"* ]] && [[ $new_db_output != *"could not parse jwt"* ]]; then
            print_status $GREEN "✅ Listagem de bancos funcionando"
            echo "   $new_db_output"
        else
            print_status $RED "❌ Problema persiste após reautenticação"
            echo "   $new_db_output"
        fi
    else
        print_status $RED "❌ Falha na reautenticação"
        echo "   $new_auth_status"
    fi
else
    print_status $GREEN "✅ Listagem de bancos funcionando"
    echo "   $db_output"
fi

echo ""

# 6. Verificar variáveis de ambiente
print_status $BLUE "9. Verificando variáveis de ambiente..."
if [ -n "$TURSO_AUTH_TOKEN" ]; then
    print_status $GREEN "✅ TURSO_AUTH_TOKEN configurado"
    echo "   Token: ${TURSO_AUTH_TOKEN:0:20}..."
else
    print_status $YELLOW "⚠️  TURSO_AUTH_TOKEN não configurado"
fi

if [ -n "$TURSO_DB_URL" ]; then
    print_status $GREEN "✅ TURSO_DB_URL configurado"
    echo "   URL: $TURSO_DB_URL"
else
    print_status $YELLOW "⚠️  TURSO_DB_URL não configurado"
fi

echo ""

# 7. Tentar regenerar tokens se necessário
print_status $BLUE "10. Tentando regenerar tokens..."
regenerate_output=$(turso db tokens create --all 2>&1)
if [[ $regenerate_output == *"error"* ]] || [[ $regenerate_output == *"could not parse jwt"* ]]; then
    print_status $RED "❌ Falha ao regenerar tokens"
    echo "   $regenerate_output"
else
    print_status $GREEN "✅ Tokens regenerados com sucesso"
    echo "   $regenerate_output"
fi

echo ""

# 8. Teste final
print_status $BLUE "11. Teste final de conectividade..."
final_test=$(turso db list 2>&1)
if [[ $final_test != *"error"* ]] && [[ $final_test != *"could not parse jwt"* ]]; then
    print_status $GREEN "🎉 PROBLEMA RESOLVIDO! Turso MCP deve estar funcionando"
    echo "   $final_test"
else
    print_status $RED "❌ PROBLEMA PERSISTE. Verificar manualmente:"
    echo "   $final_test"
    echo ""
    print_status $YELLOW "📋 Próximos passos manuais:"
    echo "   1. Verificar credenciais no site do Turso"
    echo "   2. Reinstalar CLI: brew uninstall turso && brew install tursodatabase/tap/turso"
    echo "   3. Verificar configuração do MCP Turso"
    echo "   4. Contatar suporte do Turso se necessário"
fi

echo ""
print_status $BLUE "=================================================="
print_status $BLUE "Diagnóstico concluído!" 