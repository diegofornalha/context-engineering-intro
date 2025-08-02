#!/usr/bin/env python3
"""
Script para inserir os documentos restantes de forma eficiente
"""

import glob
import re

# Documentos já inseridos
already_inserted = [
    'README.md',
    '08-reference/RESUMO_FINAL_TURSO_SENTRY.md',
    '08-reference/README.md',
    '04-prp-system/README.md',
    '01-getting-started/README.md',
    'archive/README.md',
    '05-sentry-monitoring/README.md'
]

def extract_file_paths_from_batch(batch_file):
    """Extrai caminhos de arquivo de um batch SQL"""
    with open(batch_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Procurar por file_path nos VALUES
    pattern = r"VALUES\s*\(\s*'([^']+\.md)'"
    matches = re.findall(pattern, content)
    return matches

# Listar todos os arquivos de batch
batch_files = sorted(glob.glob('/Users/agents/Desktop/context-engineering-intro/docs/sync-batches/batch-*.sql'))

# Coletar todos os arquivos para inserir
files_to_insert = []
for batch_file in batch_files:
    file_paths = extract_file_paths_from_batch(batch_file)
    for fp in file_paths:
        if fp not in already_inserted and fp not in files_to_insert:
            files_to_insert.append(fp)

print(f"📊 Total de documentos já inseridos: {len(already_inserted)}")
print(f"📝 Documentos restantes para inserir: {len(files_to_insert)}")

# Agrupar em batches de 10
batch_size = 10
batches = []
for i in range(0, len(files_to_insert), batch_size):
    batch = files_to_insert[i:i+batch_size]
    batches.append(batch)

print(f"\n🎯 Organizado em {len(batches)} batches de até {batch_size} documentos cada")

# Salvar lista de arquivos para referência
with open('/Users/agents/Desktop/context-engineering-intro/docs/remaining-files.txt', 'w') as f:
    f.write("Arquivos restantes para inserir:\n\n")
    for i, batch in enumerate(batches, 1):
        f.write(f"Batch {i} ({len(batch)} arquivos):\n")
        for fp in batch:
            f.write(f"  - {fp}\n")
        f.write("\n")

print(f"\n✅ Lista salva em: remaining-files.txt")
print("\n📋 Próximos batches:")
for i, batch in enumerate(batches[:3], 1):
    print(f"\nBatch {i}:")
    for fp in batch[:5]:
        print(f"  - {fp}")