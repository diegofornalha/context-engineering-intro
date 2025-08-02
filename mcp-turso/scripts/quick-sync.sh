#!/bin/bash
# Script de execução rápida para sincronização

echo "🔄 Executando sincronização rápida..."

# Executar scan
python3 sync-knowledge-via-mcp.py

# Executar integrador
python3 integrate-with-mcp.py

echo "✅ Sincronização rápida concluída!"
