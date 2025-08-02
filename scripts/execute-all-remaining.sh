#!/bin/bash
# Script para executar todos os batches restantes

echo "🚀 Executando sincronização completa dos documentos..."

# Contador de documentos
TOTAL_DOCS=48
ALREADY_INSERTED=7
REMAINING=$((TOTAL_DOCS - ALREADY_INSERTED))

echo "📊 Status atual:"
echo "  - Total de documentos: $TOTAL_DOCS"
echo "  - Já inseridos: $ALREADY_INSERTED" 
echo "  - Restantes: $REMAINING"
echo ""

# Função para executar SQL via Turso CLI
execute_sql() {
    local sql_file=$1
    echo "📝 Executando: $sql_file"
    
    # Executar o arquivo SQL
    turso db shell context-memory < "$sql_file" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Executado com sucesso"
        return 0
    else
        echo "❌ Erro na execução"
        return 1
    fi
}

# Processar cada arquivo SQL do sync original
SQL_FILE="/Users/agents/Desktop/context-engineering-intro/docs/sync-organized-docs.sql"

if [ -f "$SQL_FILE" ]; then
    echo "🔄 Processando arquivo SQL completo..."
    execute_sql "$SQL_FILE"
else
    echo "❌ Arquivo SQL não encontrado: $SQL_FILE"
fi

# Verificar resultado final
echo ""
echo "📊 Verificando resultado final..."
turso db shell context-memory "SELECT COUNT(*) as total FROM docs_organized"

echo ""
echo "📈 Documentos por cluster:"
turso db shell context-memory "SELECT cluster, COUNT(*) as docs FROM docs_organized GROUP BY cluster ORDER BY cluster"