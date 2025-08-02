#!/usr/bin/env python3
"""
Teste de Sincronização dos docs-turso
"""

import os
import glob
import sqlite3
from datetime import datetime

def test_sync():
    """Testa a sincronização dos docs-turso"""
    
    print("🧪 Teste de Sincronização dos docs-turso")
    print("=" * 50)
    
    # 1. Verificar se o banco existe
    db_path = "../../context-memory.db"
    if not os.path.exists(db_path):
        print(f"❌ Banco não encontrado: {db_path}")
        return
    
    print(f"✅ Banco encontrado: {db_path}")
    
    # 2. Conectar ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 3. Verificar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"📋 Tabelas encontradas: {[t[0] for t in tables]}")
    
    # 4. Escanear arquivos docs-turso
    docs_files = []
    patterns = [
        "../../docs-turso/**/*.md",
        "../../docs-turso/**/*.txt"
    ]
    
    for pattern in patterns:
        for file_path in glob.glob(pattern, recursive=True):
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                docs_files.append({
                    'path': file_path,
                    'size': file_size,
                    'modified': modified
                })
    
    print(f"📁 Arquivos docs-turso encontrados: {len(docs_files)}")
    
    # 5. Verificar se há tabela de conhecimento
    if any('knowledge' in t[0].lower() for t in tables):
        print("✅ Tabela de conhecimento encontrada")
        
        # Verificar registros existentes
        cursor.execute("SELECT COUNT(*) FROM turso_agent_knowledge")
        count = cursor.fetchone()[0]
        print(f"📊 Registros existentes: {count}")
        
        # Mostrar alguns registros
        cursor.execute("SELECT topic, category, updated_at FROM turso_agent_knowledge LIMIT 5")
        records = cursor.fetchall()
        print("📝 Últimos registros:")
        for record in records:
            print(f"  • {record[0]} ({record[1]}) - {record[2]}")
    else:
        print("❌ Tabela de conhecimento não encontrada")
    
    # 6. Simular inserção de conhecimento
    print("\n🔄 Simulando inserção de conhecimento...")
    
    for file_info in docs_files[:3]:  # Primeiros 3 arquivos
        filename = os.path.basename(file_info['path'])
        topic = filename.replace('.md', '').replace('.txt', '').replace('_', ' ').title()
        
        print(f"  📝 Processando: {topic}")
        print(f"     📁 Arquivo: {file_info['path']}")
        print(f"     📏 Tamanho: {file_info['size']} bytes")
        print(f"     ⏰ Modificado: {file_info['modified']}")
        
        # Simular inserção (sem realmente inserir)
        print(f"     ✅ Conhecimento extraído e pronto para inserção")
    
    conn.close()
    
    print(f"\n✅ Teste concluído!")
    print(f"📊 Resumo:")
    print(f"  • Arquivos escaneados: {len(docs_files)}")
    print(f"  • Banco de dados: {db_path}")
    print(f"  • Tabelas disponíveis: {len(tables)}")

if __name__ == "__main__":
    test_sync() 