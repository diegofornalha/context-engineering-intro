#!/usr/bin/env python3
"""
Script para executar sync de documentos em batches usando MCP Turso
"""

import os
import re
import time

def read_batch_file(filepath):
    """Lê arquivo de batch e retorna SQLs"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover comentários e linhas vazias
    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('--')]
    content = '\n'.join(lines)
    
    # Dividir por INSERT statements
    inserts = re.split(r'(?=INSERT OR REPLACE INTO)', content)
    inserts = [i.strip() for i in inserts if i.strip()]
    
    return inserts

def execute_batch(batch_number):
    """Executa um batch de inserts"""
    batch_file = f"/Users/agents/Desktop/context-engineering-intro/docs/sync-batches/batch-{batch_number:02d}.sql"
    
    if not os.path.exists(batch_file):
        return False
    
    print(f"\n📦 Processando Batch {batch_number}...")
    inserts = read_batch_file(batch_file)
    
    # Criar arquivo temporário para cada insert
    for idx, insert in enumerate(inserts, 1):
        temp_file = f"/tmp/turso-insert-{batch_number}-{idx}.sql"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(insert)
        
        print(f"  📝 Executando insert {idx}/{len(inserts)}...")
        os.system(f"turso db shell context-memory < {temp_file}")
        os.remove(temp_file)
        time.sleep(0.1)  # Pequena pausa entre inserts
    
    print(f"✅ Batch {batch_number} concluído ({len(inserts)} documentos)")
    return True

def main():
    print("🚀 Iniciando sincronização de documentos com Turso...")
    
    # Executar batches
    batch_num = 1
    while execute_batch(batch_num):
        batch_num += 1
    
    print(f"\n✅ Sincronização concluída! {batch_num-1} batches processados.")
    
    # Verificar total de documentos
    print("\n📊 Verificando total de documentos...")
    os.system('turso db shell context-memory "SELECT COUNT(*) as total FROM docs_organized"')

if __name__ == "__main__":
    main()