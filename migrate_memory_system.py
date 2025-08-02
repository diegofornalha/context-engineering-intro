#!/usr/bin/env python3
"""
Script para migrar o sistema de memória do mcp-turso para o mcp-turso-cloud.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any

def read_mcp_turso_data(db_path: str) -> Dict[str, Any]:
    """Lê os dados do banco de dados do mcp-turso."""
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return {"conversations": [], "knowledge": []}
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Verificar se as tabelas existem
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('conversations', 'knowledge_base')")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        data = {"conversations": [], "knowledge": []}
        
        if 'conversations' in existing_tables:
            cursor = conn.execute("""
                SELECT session_id, user_id, message, response, context, timestamp
                FROM conversations
                ORDER BY timestamp DESC
            """)
            data["conversations"] = cursor.fetchall()
        
        if 'knowledge_base' in existing_tables:
            cursor = conn.execute("""
                SELECT topic, content, source, tags, priority, created_at
                FROM knowledge_base
                ORDER BY created_at DESC
            """)
            data["knowledge"] = cursor.fetchall()
        
        return data
        
    finally:
        conn.close()

def generate_migration_script(data: Dict[str, Any], target_database: str) -> str:
    """Gera script SQL para migração dos dados."""
    
    script = f"""
-- Script de Migração do Sistema de Memória
-- Do mcp-turso para mcp-turso-cloud
-- Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
-- Banco de destino: {target_database}

-- Configurar banco de destino
-- Use: setup_memory_tables tool primeiro

-- Migrar conversas
"""
    
    for session_id, user_id, message, response, context, timestamp in data["conversations"]:
        # Escapar aspas simples
        safe_message = message.replace("'", "''") if message else ""
        safe_response = response.replace("'", "''") if response else ""
        safe_context = context.replace("'", "''") if context else ""
        
        script += f"""
-- Migrar conversa: {session_id[:20]}...
INSERT INTO conversations (session_id, user_id, message, response, context, timestamp)
VALUES ('{session_id}', {f"'{user_id}'" if user_id else 'NULL'}, '{safe_message}', {f"'{safe_response}'" if safe_response else 'NULL'}, {f"'{safe_context}'" if safe_context else 'NULL'}, '{timestamp}');
"""
    
    script += "\n-- Migrar conhecimento\n"
    
    for topic, content, source, tags, priority, created_at in data["knowledge"]:
        # Escapar aspas simples
        safe_topic = topic.replace("'", "''") if topic else ""
        safe_content = content.replace("'", "''") if content else ""
        safe_source = source.replace("'", "''") if source else ""
        safe_tags = tags.replace("'", "''") if tags else ""
        
        script += f"""
-- Migrar conhecimento: {safe_topic[:30]}...
INSERT INTO knowledge_base (topic, content, source, tags, priority, created_at)
VALUES ('{safe_topic}', '{safe_content}', {f"'{safe_source}'" if safe_source else 'NULL'}, {f"'{safe_tags}'" if safe_tags else 'NULL'}, {priority or 1}, '{created_at}');
"""
    
    return script

def generate_mcp_commands(data: Dict[str, Any], target_database: str) -> str:
    """Gera comandos MCP para migração."""
    
    commands = f"""
# Comandos MCP para Migração do Sistema de Memória
# Do mcp-turso para mcp-turso-cloud
# Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}

# 1. Configurar tabelas de memória
setup_memory_tables(database="{target_database}")

# 2. Migrar conversas
"""
    
    for session_id, user_id, message, response, context, timestamp in data["conversations"]:
        commands += f"""
add_conversation(
    session_id="{session_id}",
    user_id={f'"{user_id}"' if user_id else 'null'},
    message="{message.replace('"', '\\"') if message else ''}",
    response={f'"{response.replace('"', '\\"')}"' if response else 'null'},
    context={f'"{context.replace('"', '\\"')}"' if context else 'null'},
    database="{target_database}"
)
"""
    
    commands += "\n# 3. Migrar conhecimento\n"
    
    for topic, content, source, tags, priority, created_at in data["knowledge"]:
        commands += f"""
add_knowledge(
    topic="{topic.replace('"', '\\"') if topic else ''}",
    content="{content.replace('"', '\\"') if content else ''}",
    source={f'"{source.replace('"', '\\"')}"' if source else 'null'},
    tags={f'"{tags.replace('"', '\\"')}"' if tags else 'null'},
    database="{target_database}"
)
"""
    
    return commands

def main():
    """Função principal."""
    
    # Caminhos dos bancos de dados
    mcp_turso_db = "../mcp-turso/sentry_errors_documentation.db"  # Banco local do mcp-turso
    target_database = "cursor10x-memory"  # Banco de destino no mcp-turso-cloud
    
    print("🔄 Migrando Sistema de Memória do mcp-turso para mcp-turso-cloud...")
    print("=" * 60)
    
    try:
        # Ler dados do mcp-turso
        print("📖 Lendo dados do mcp-turso...")
        data = read_mcp_turso_data(mcp_turso_db)
        
        print(f"📊 Dados encontrados:")
        print(f"   - Conversas: {len(data['conversations'])}")
        print(f"   - Conhecimento: {len(data['knowledge'])}")
        
        # Gerar scripts de migração
        print("📝 Gerando scripts de migração...")
        
        # Script SQL
        sql_script = generate_migration_script(data, target_database)
        with open("migrate_memory_sql.sql", "w", encoding="utf-8") as f:
            f.write(sql_script)
        
        # Comandos MCP
        mcp_commands = generate_mcp_commands(data, target_database)
        with open("migrate_memory_mcp.txt", "w", encoding="utf-8") as f:
            f.write(mcp_commands)
        
        # Resumo
        summary = f"""
# Resumo da Migração do Sistema de Memória

## Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Dados Migrados
- **Conversas:** {len(data['conversations'])} registros
- **Conhecimento:** {len(data['knowledge'])} registros
- **Banco de Origem:** {mcp_turso_db}
- **Banco de Destino:** {target_database}

## Arquivos Gerados
- `migrate_memory_sql.sql` - Script SQL para migração
- `migrate_memory_mcp.txt` - Comandos MCP para migração

## Próximos Passos
1. Configurar mcp-turso-cloud como MCP principal
2. Executar: setup_memory_tables(database="{target_database}")
3. Executar os comandos em migrate_memory_mcp.txt
4. Verificar migração com: get_conversations(database="{target_database}")
5. Remover mcp-turso após confirmação

## Status
✅ Migração preparada
⚠️ Aguardando execução
"""
        
        with open("MIGRATION_SUMMARY.md", "w", encoding="utf-8") as f:
            f.write(summary)
        
        print("✅ Migração preparada com sucesso!")
        print("📄 Arquivos gerados:")
        print("   - migrate_memory_sql.sql")
        print("   - migrate_memory_mcp.txt")
        print("   - MIGRATION_SUMMARY.md")
        
        print(f"\n🚀 Para executar a migração:")
        print(f"1. Use o mcp-turso-cloud como MCP principal")
        print(f"2. Execute: setup_memory_tables(database='{target_database}')")
        print(f"3. Execute os comandos em migrate_memory_mcp.txt")
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")

if __name__ == "__main__":
    main() 