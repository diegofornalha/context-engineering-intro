#!/usr/bin/env python3
"""
Script para executar inserts em lotes via MCP Turso
"""

import re

def read_all_inserts():
    """Lê todos os inserts do arquivo limpo"""
    with open('/Users/agents/Desktop/context-engineering-intro/docs/all-inserts-clean.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dividir por comentários de documento
    pattern = r'-- Documento \d+/\d+\n(INSERT OR REPLACE INTO docs_organized[\s\S]*?);'
    inserts = re.findall(pattern, content)
    
    return inserts

# Ler todos os inserts
inserts = read_all_inserts()
print(f"📊 Total de inserts encontrados: {len(inserts)}")

# Documentos já inseridos
already_inserted = ['README.md', '08-reference/RESUMO_FINAL_TURSO_SENTRY.md']

# Filtrar inserts para executar
inserts_to_execute = []
for insert in inserts:
    # Verificar se o documento já foi inserido
    file_match = re.search(r"file_path[,\s]+title[,\s]+content[,\s]+summary[,\s]+cluster[,\s]+category[,\s]+file_hash[,\s]+size[,\s]+last_modified[,\s]+metadata\s*\)\s*VALUES\s*\(\s*'([^']+)'", insert)
    if file_match:
        file_path = file_match.group(1)
        if file_path not in already_inserted:
            inserts_to_execute.append((file_path, insert))

print(f"📝 Inserts a executar: {len(inserts_to_execute)}")

# Criar arquivo com os comandos para execução
output_file = '/Users/agents/Desktop/context-engineering-intro/docs/execute-remaining.sql'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("-- Inserts restantes para executar\n\n")
    for i, (file_path, insert) in enumerate(inserts_to_execute[:10], 1):  # Primeiro lote de 10
        f.write(f"-- {i}. {file_path}\n")
        f.write(insert + ";\n\n")

print(f"✅ Arquivo criado com primeiros 10 inserts: {output_file}")
print("\n📋 Primeiros 10 documentos a inserir:")
for i, (file_path, _) in enumerate(inserts_to_execute[:10], 1):
    print(f"  {i}. {file_path}")