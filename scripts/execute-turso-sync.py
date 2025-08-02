#!/usr/bin/env python3
"""
Executa a sincronização dos documentos no Turso
Divide o SQL em partes menores para evitar timeouts
"""

import re
from pathlib import Path

def split_sql_file(sql_file_path):
    """Divide o arquivo SQL em comandos individuais"""
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Separar por comandos SQL
    commands = []
    
    # 1. Comandos CREATE TABLE/INDEX
    create_commands = re.findall(r'CREATE\s+(?:TABLE|INDEX)[^;]+;', content, re.IGNORECASE | re.DOTALL)
    commands.extend(create_commands)
    
    # 2. Comandos INSERT/UPDATE
    insert_commands = re.findall(r'INSERT\s+INTO\s+docs[^;]+;', content, re.IGNORECASE | re.DOTALL)
    
    return create_commands, insert_commands

def save_sql_parts(create_commands, insert_commands):
    """Salva comandos SQL em arquivos separados"""
    output_dir = Path("/Users/agents/Desktop/context-engineering-intro/docs/sync-parts")
    output_dir.mkdir(exist_ok=True)
    
    # Salvar comandos CREATE
    with open(output_dir / "01-create-tables.sql", 'w', encoding='utf-8') as f:
        f.write("-- Criar estrutura das tabelas\n\n")
        for cmd in create_commands:
            f.write(cmd + "\n\n")
    
    # Salvar comandos INSERT em lotes
    batch_size = 10
    for i in range(0, len(insert_commands), batch_size):
        batch = insert_commands[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        
        with open(output_dir / f"02-insert-batch-{batch_num:02d}.sql", 'w', encoding='utf-8') as f:
            f.write(f"-- Batch {batch_num} de documentos\n\n")
            for cmd in batch:
                f.write(cmd + "\n\n")
    
    return output_dir, len(insert_commands)

def create_execution_script(output_dir, total_docs):
    """Cria script para executar no Claude Code"""
    script_content = f'''# Instruções para Sincronização com Turso

## 📊 Resumo
- Total de documentos: {total_docs}
- Arquivos SQL gerados: {len(list(output_dir.glob("*.sql")))}

## 🚀 Execute no Claude Code:

### 1. Criar estrutura das tabelas:
```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/01-create-tables.sql no banco context-memory
```

### 2. Inserir documentos (execute cada batch):
'''
    
    for sql_file in sorted(output_dir.glob("02-insert-batch-*.sql")):
        script_content += f'''
```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/{sql_file.name} no banco context-memory
```
'''
    
    script_content += '''

## ✅ Verificar sincronização:
```
Use mcp__turso__execute_read_only_query com a query "SELECT COUNT(*) as total, cluster, COUNT(DISTINCT category) as categories FROM docs GROUP BY cluster ORDER BY cluster" no banco context-memory
```
'''
    
    with open(output_dir / "EXECUTE-SYNC.md", 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📝 Instruções salvas em: {output_dir}/EXECUTE-SYNC.md")

if __name__ == "__main__":
    sql_file = Path("/Users/agents/Desktop/context-engineering-intro/docs/sync-to-turso.sql")
    
    print("🔄 Dividindo arquivo SQL em partes...")
    create_commands, insert_commands = split_sql_file(sql_file)
    
    print(f"📊 Encontrados:")
    print(f"  - Comandos CREATE: {len(create_commands)}")
    print(f"  - Comandos INSERT: {len(insert_commands)}")
    
    output_dir, total_docs = save_sql_parts(create_commands, insert_commands)
    
    print(f"\n✅ Arquivos SQL salvos em: {output_dir}")
    
    create_execution_script(output_dir, total_docs)
    
    print("\n🎯 Próximo passo: Siga as instruções em EXECUTE-SYNC.md")