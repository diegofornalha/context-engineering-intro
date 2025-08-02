#!/bin/bash
# Script final para sincronizar todos os documentos restantes

echo "🚀 Sincronização Final de Documentos"
echo "=================================="

# Verificar status atual
echo "📊 Verificando status atual..."
CURRENT_COUNT=$(turso db shell context-memory "SELECT COUNT(*) as total FROM docs_organized" 2>/dev/null | grep -o '[0-9]\+' | tail -1)
echo "✅ Documentos já inseridos: $CURRENT_COUNT"

# Total esperado
TOTAL_EXPECTED=48
REMAINING=$((TOTAL_EXPECTED - CURRENT_COUNT))
echo "📝 Documentos restantes: $REMAINING"

if [ $REMAINING -eq 0 ]; then
    echo "✅ Todos os documentos já foram sincronizados!"
    exit 0
fi

# Executar o arquivo SQL completo
echo ""
echo "🔄 Executando sincronização completa..."
SQL_FILE="/Users/agents/Desktop/context-engineering-intro/docs/sync-organized-docs.sql"

if [ -f "$SQL_FILE" ]; then
    echo "📝 Executando arquivo SQL..."
    turso db shell context-memory < "$SQL_FILE" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Sincronização executada com sucesso!"
    else
        echo "⚠️ Alguns documentos podem já existir (isso é normal)"
    fi
else
    echo "❌ Arquivo SQL não encontrado!"
    exit 1
fi

# Verificar resultado final
echo ""
echo "📊 Verificando resultado final..."
FINAL_COUNT=$(turso db shell context-memory "SELECT COUNT(*) as total FROM docs_organized" 2>/dev/null | grep -o '[0-9]\+' | tail -1)
echo "✅ Total de documentos sincronizados: $FINAL_COUNT"

# Mostrar estatísticas por cluster
echo ""
echo "📈 Documentos por cluster:"
turso db shell context-memory "SELECT cluster, COUNT(*) as docs FROM docs_organized GROUP BY cluster ORDER BY cluster" 2>/dev/null

# Verificar qualidade da sincronização
echo ""
echo "🔍 Verificando integridade..."
turso db shell context-memory "SELECT 
    COUNT(DISTINCT cluster) as clusters,
    COUNT(DISTINCT category) as categories,
    AVG(size) as avg_size,
    COUNT(CASE WHEN size > 0 THEN 1 END) as valid_docs
FROM docs_organized" 2>/dev/null

echo ""
echo "✅ Sincronização concluída!"