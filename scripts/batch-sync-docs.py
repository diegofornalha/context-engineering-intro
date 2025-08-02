#!/usr/bin/env python3
"""
Script para executar sync de documentos em batches
"""

import re
import time

def extract_inserts(sql_file):
    """Extrai comandos INSERT do arquivo SQL"""
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para encontrar comandos INSERT completos
    pattern = r'INSERT OR REPLACE INTO docs_organized.*?(?=INSERT OR REPLACE INTO docs_organized|$)'
    inserts = re.findall(pattern, content, re.DOTALL)
    
    # Limpar e retornar apenas INSERTs válidos
    cleaned_inserts = []
    for insert in inserts:
        insert = insert.strip()
        if insert and not insert.endswith(';'):
            insert += ';'
        if insert:
            cleaned_inserts.append(insert)
    
    return cleaned_inserts

def create_batch_files(inserts, batch_size=10):
    """Cria arquivos de batch para execução"""
    batches = []
    for i in range(0, len(inserts), batch_size):
        batch = inserts[i:i+batch_size]
        batches.append(batch)
    
    # Salvar batches
    for idx, batch in enumerate(batches, 1):
        filename = f"/Users/agents/Desktop/context-engineering-intro/docs/sync-batches/batch-{idx:02d}.sql"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"-- Batch {idx} - {len(batch)} documentos\n\n")
            for insert in batch:
                f.write(insert + "\n\n")
        print(f"✅ Criado: {filename} ({len(batch)} documentos)")
    
    return len(batches)

def main():
    # Arquivo SQL original
    sql_file = "/Users/agents/Desktop/context-engineering-intro/docs/sync-organized-docs.sql"
    
    print("📊 Processando arquivo SQL...")
    inserts = extract_inserts(sql_file)
    print(f"📝 Total de INSERTs encontrados: {len(inserts)}")
    
    # Pular o primeiro INSERT (README.md já inserido)
    remaining_inserts = inserts[1:]
    print(f"📋 INSERTs restantes para processar: {len(remaining_inserts)}")
    
    # Criar diretório para batches
    import os
    os.makedirs("/Users/agents/Desktop/context-engineering-intro/docs/sync-batches", exist_ok=True)
    
    # Criar arquivos de batch
    num_batches = create_batch_files(remaining_inserts, batch_size=10)
    
    print(f"\n✅ {num_batches} arquivos de batch criados!")
    print("\n🚀 Execute cada batch usando:")
    print("mcp__turso__execute_query com o conteúdo de cada arquivo batch")

if __name__ == "__main__":
    main()