#!/usr/bin/env python3
"""
Script para configurar o banco de dados de PRPs no context-memory
Data: 02/08/2025
"""

import sqlite3
import json
import os
from datetime import datetime

def setup_prp_database():
    """Configura o banco de dados context-memory com as tabelas de PRPs"""
    
    # Conectar ao banco context-memory
    db_path = "context-memory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Configurando banco de dados de PRPs...")
        
        # Ler o schema SQL
        with open('prp_database_schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Executar o schema
        cursor.executescript(schema_sql)
        
        # Verificar se as tabelas foram criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'prp_%'")
        prp_tables = cursor.fetchall()
        
        print(f"✅ Tabelas criadas: {len(prp_tables)}")
        for table in prp_tables:
            print(f"   - {table[0]}")
        
        # Verificar dados iniciais
        cursor.execute("SELECT COUNT(*) FROM prp_tags")
        tag_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prps")
        prp_count = cursor.fetchone()[0]
        
        print(f"✅ Tags padrão inseridas: {tag_count}")
        print(f"✅ PRP de exemplo inserido: {prp_count}")
        
        # Verificar views
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name LIKE 'v_prp_%'")
        views = cursor.fetchall()
        
        print(f"✅ Views criadas: {len(views)}")
        for view in views:
            print(f"   - {view[0]}")
        
        # Testar uma consulta básica
        cursor.execute("""
            SELECT p.name, p.title, p.status, COUNT(t.id) as task_count
            FROM prps p
            LEFT JOIN prp_tasks t ON p.id = t.prp_id
            GROUP BY p.id
        """)
        
        results = cursor.fetchall()
        print(f"✅ Teste de consulta: {len(results)} PRPs encontrados")
        
        for row in results:
            print(f"   - {row[0]}: {row[1]} ({row[2]}) - {row[3]} tarefas")
        
        conn.commit()
        print("✅ Banco de dados de PRPs configurado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao configurar banco de dados: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def test_prp_operations():
    """Testa operações básicas de CRUD para PRPs"""
    
    db_path = "context-memory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n🧪 Testando operações CRUD...")
        
        # 1. Criar um novo PRP
        new_prp = {
            'name': 'test-prp',
            'title': 'PRP de Teste',
            'description': 'PRP para testar as operações',
            'objective': 'Testar funcionalidades do banco de dados',
            'context_data': json.dumps({
                'files': ['test.py'],
                'libraries': ['sqlite3']
            }),
            'implementation_details': json.dumps({
                'language': 'Python',
                'framework': 'SQLite'
            }),
            'validation_gates': json.dumps({
                'tests': 'pytest'
            }),
            'status': 'draft',
            'priority': 'medium',
            'tags': json.dumps(['testing', 'database']),
            'search_text': 'teste PRP banco dados Python SQLite'
        }
        
        cursor.execute("""
            INSERT INTO prps (name, title, description, objective, context_data, 
                             implementation_details, validation_gates, status, priority, tags, search_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_prp['name'], new_prp['title'], new_prp['description'], new_prp['objective'],
            new_prp['context_data'], new_prp['implementation_details'], new_prp['validation_gates'],
            new_prp['status'], new_prp['priority'], new_prp['tags'], new_prp['search_text']
        ))
        
        prp_id = cursor.lastrowid
        print(f"✅ PRP criado com ID: {prp_id}")
        
        # 2. Criar uma tarefa para o PRP
        task_data = {
            'prp_id': prp_id,
            'task_name': 'Implementar schema',
            'description': 'Criar as tabelas do banco de dados',
            'task_type': 'setup',
            'priority': 'high',
            'estimated_hours': 2.0,
            'status': 'pending',
            'context_files': json.dumps(['schema.sql']),
            'acceptance_criteria': 'Todas as tabelas criadas e funcionando'
        }
        
        cursor.execute("""
            INSERT INTO prp_tasks (prp_id, task_name, description, task_type, priority, 
                                  estimated_hours, status, context_files, acceptance_criteria)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_data['prp_id'], task_data['task_name'], task_data['description'],
            task_data['task_type'], task_data['priority'], task_data['estimated_hours'],
            task_data['status'], task_data['context_files'], task_data['acceptance_criteria']
        ))
        
        task_id = cursor.lastrowid
        print(f"✅ Tarefa criada com ID: {task_id}")
        
        # 3. Adicionar contexto
        context_data = {
            'prp_id': prp_id,
            'context_type': 'file',
            'name': 'schema.sql',
            'path': '/path/to/schema.sql',
            'content': 'Schema do banco de dados',
            'version': '1.0',
            'importance': 'high'
        }
        
        cursor.execute("""
            INSERT INTO prp_context (prp_id, context_type, name, path, content, version, importance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            context_data['prp_id'], context_data['context_type'], context_data['name'],
            context_data['path'], context_data['content'], context_data['version'], context_data['importance']
        ))
        
        print("✅ Contexto adicionado")
        
        # 4. Testar view de progresso
        cursor.execute("""
            SELECT name, title, prp_status, total_tasks, completion_percentage
            FROM v_prp_progress
            WHERE id = ?
        """, (prp_id,))
        
        progress = cursor.fetchone()
        print(f"✅ Progresso: {progress[0]} - {progress[1]} ({progress[2]}) - {progress[3]} tarefas - {progress[4]}% completo")
        
        # 5. Limpar dados de teste
        cursor.execute("DELETE FROM prp_context WHERE prp_id = ?", (prp_id,))
        cursor.execute("DELETE FROM prp_tasks WHERE prp_id = ?", (prp_id,))
        cursor.execute("DELETE FROM prps WHERE id = ?", (prp_id,))
        
        print("✅ Dados de teste removidos")
        
        conn.commit()
        print("✅ Testes de operações CRUD concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def show_database_info():
    """Mostra informações sobre o banco de dados de PRPs"""
    
    db_path = "context-memory.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n📊 Informações do Banco de Dados de PRPs:")
        
        # Contagem de registros por tabela
        tables = ['prps', 'prp_tasks', 'prp_context', 'prp_tags', 'prp_history', 'prp_llm_analysis']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} registros")
        
        # PRPs existentes
        cursor.execute("""
            SELECT name, title, status, priority, created_at
            FROM prps
            ORDER BY created_at DESC
        """)
        
        prps = cursor.fetchall()
        print(f"\n📋 PRPs existentes ({len(prps)}):")
        
        for prp in prps:
            print(f"   - {prp[0]}: {prp[1]} ({prp[2]}, {prp[3]}) - {prp[4]}")
        
        # Tags disponíveis
        cursor.execute("""
            SELECT name, category, description
            FROM prp_tags
            ORDER BY category, name
        """)
        
        tags = cursor.fetchall()
        print(f"\n🏷️ Tags disponíveis ({len(tags)}):")
        
        current_category = None
        for tag in tags:
            if tag[1] != current_category:
                current_category = tag[1]
                print(f"   {current_category.upper()}:")
            print(f"     - {tag[0]}: {tag[2]}")
        
    except Exception as e:
        print(f"❌ Erro ao obter informações: {e}")
    finally:
        conn.close()

def main():
    """Função principal"""
    
    print("🚀 CONFIGURAÇÃO DO BANCO DE DADOS DE PRPs")
    print("=" * 50)
    
    # Verificar se o arquivo de schema existe
    if not os.path.exists('prp_database_schema.sql'):
        print("❌ Arquivo prp_database_schema.sql não encontrado!")
        return
    
    try:
        # Configurar o banco de dados
        setup_prp_database()
        
        # Testar operações
        test_prp_operations()
        
        # Mostrar informações
        show_database_info()
        
        print("\n✅ Configuração concluída com sucesso!")
        print("\n📝 Próximos passos:")
        print("   1. Implementar servidor MCP para PRPs")
        print("   2. Criar ferramentas para análise de PRPs")
        print("   3. Integrar com LLM para extração de tarefas")
        print("   4. Implementar interface de usuário")
        
    except Exception as e:
        print(f"❌ Erro durante a configuração: {e}")

if __name__ == "__main__":
    main() 