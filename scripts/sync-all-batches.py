#!/usr/bin/env python3
"""
Script para sincronizar todos os batches de documentos
"""

import glob
import re

def extract_inserts_from_file(filepath):
    """Extrai comandos INSERT limpos do arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover comentários no início
    content = re.sub(r'^--.*?\n\n', '', content, flags=re.MULTILINE)
    
    # Dividir por INSERT statements
    pattern = r'(INSERT OR REPLACE INTO docs_organized[\s\S]*?)(?=INSERT OR REPLACE INTO docs_organized|$)'
    inserts = re.findall(pattern, content)
    
    # Limpar cada insert
    cleaned_inserts = []
    for insert in inserts:
        insert = insert.strip()
        # Garantir que termina com ;
        if insert and not insert.endswith(';'):
            insert += ';'
        if insert and 'INSERT OR REPLACE INTO docs_organized' in insert:
            cleaned_inserts.append(insert)
    
    return cleaned_inserts

# Processar todos os batches
batch_files = sorted(glob.glob('/Users/agents/Desktop/context-engineering-intro/docs/sync-batches/batch-*.sql'))

total_inserts = []
for batch_file in batch_files:
    inserts = extract_inserts_from_file(batch_file)
    total_inserts.extend(inserts)
    print(f"📦 {batch_file}: {len(inserts)} inserts extraídos")

print(f"\n✅ Total de inserts: {len(total_inserts)}")

# Salvar todos os inserts em um arquivo único
output_file = '/Users/agents/Desktop/context-engineering-intro/docs/all-inserts-clean.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("-- Todos os inserts de documentos organizados\n\n")
    for i, insert in enumerate(total_inserts, 1):
        f.write(f"-- Documento {i}/{len(total_inserts)}\n")
        f.write(insert)
        f.write("\n\n")

print(f"📝 Arquivo criado: {output_file}")
print("\n🎯 Próximo passo: Executar os inserts usando o MCP Turso")