#!/bin/bash
# Script para sincronizar documentos em pequenos batches

echo "🚀 Iniciando sincronização em batches..."

# Função para executar um batch
execute_batch() {
    local batch_file=$1
    echo "📦 Executando: $batch_file"
    
    # Usar o Turso CLI para executar o SQL
    turso db shell context-memory < "$batch_file"
    
    if [ $? -eq 0 ]; then
        echo "✅ Batch executado com sucesso"
    else
        echo "❌ Erro ao executar batch"
        return 1
    fi
}

# Executar cada batch
for i in {01..05}; do
    batch_file="/Users/agents/Desktop/context-engineering-intro/docs/sync-batches/batch-${i}.sql"
    if [ -f "$batch_file" ]; then
        echo -e "\n📊 Processando Batch $i..."
        execute_batch "$batch_file"
        sleep 1  # Pequena pausa entre batches
    fi
done

echo -e "\n✅ Sincronização concluída!"

# Verificar total de documentos
echo -e "\n📊 Verificando total de documentos..."
turso db shell context-memory "SELECT COUNT(*) as total FROM docs_organized"