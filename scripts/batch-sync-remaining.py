#!/usr/bin/env python3
"""
Script para processar inserts restantes de forma eficiente
"""

import os
import glob

# Lista de arquivos já inseridos
already_inserted = [
    'README.md',
    '08-reference/RESUMO_FINAL_TURSO_SENTRY.md'
]

# Ler todos os arquivos de batch
batch_files = sorted(glob.glob('/Users/agents/Desktop/context-engineering-intro/docs/sync-batches/batch-*.sql'))

print(f"📊 Processando {len(batch_files)} arquivos de batch...")
print(f"📝 Documentos já inseridos: {len(already_inserted)}")

# Processar cada batch
for batch_file in batch_files:
    with open(batch_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar quantos INSERTs tem no arquivo
    insert_count = content.count('INSERT OR REPLACE INTO docs_organized')
    print(f"\n📦 {os.path.basename(batch_file)}: {insert_count} documentos")
    
    # Verificar quais documentos estão no batch
    lines = content.split('\n')
    for line in lines:
        if 'file_path' in line and "'" in line:
            # Extrair o nome do arquivo
            parts = line.split("'")
            if len(parts) >= 2:
                file_path = parts[1]
                if file_path not in already_inserted and file_path.endswith('.md'):
                    print(f"  - {file_path}")

print(f"\n✅ Total de documentos para inserir: {48 - len(already_inserted)}")