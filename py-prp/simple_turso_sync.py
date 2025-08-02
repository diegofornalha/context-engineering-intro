#!/usr/bin/env python3
"""
Sistema Simplificado de Sincronização SQLite ↔ Turso
Data: 02/08/2025

Sistema prático de sincronização entre banco local e Turso,
focado em funcionalidade e facilidade de uso.
"""

import os
import json
import sqlite3
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class SimpleTursoSync:
    """
    Sistema simplificado de sincronização com Turso
    """
    
    def __init__(self, local_db: str = "context-memory.db", turso_db: str = "context-memory"):
        self.local_db = local_db
        self.turso_db = turso_db
        self.setup_sync_tables()
    
    def setup_sync_tables(self):
        """Configura tabelas de controle de sincronização"""
        print("🔧 Configurando sistema de sync...")
        
        with sqlite3.connect(self.local_db) as conn:
            # Tabela de controle de sincronização
            conn.execute("""
                CREATE TABLE IF NOT EXISTS turso_sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_direction TEXT NOT NULL,
                    tables_affected TEXT,
                    records_synced INTEGER DEFAULT 0,
                    success BOOLEAN DEFAULT 1,
                    error_message TEXT,
                    sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de status das tabelas
            conn.execute("""
                CREATE TABLE IF NOT EXISTS turso_sync_status (
                    table_name TEXT PRIMARY KEY,
                    last_sync TIMESTAMP,
                    local_count INTEGER DEFAULT 0,
                    remote_count INTEGER DEFAULT 0,
                    sync_needed BOOLEAN DEFAULT 1
                )
            """)
            
            conn.commit()
    
    def check_turso_connection(self) -> bool:
        """Verifica se consegue conectar ao Turso"""
        try:
            result = subprocess.run([
                'turso', 'db', 'list'
            ], capture_output=True, text=True, timeout=10)
            
            return result.returncode == 0
        except Exception:
            return False
    
    def get_turso_schema(self) -> str:
        """Obtém schema do banco Turso"""
        try:
            result = subprocess.run([
                'turso', 'db', 'shell', self.turso_db,
                '.schema'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return result.stdout
            return ""
        except Exception:
            return ""
    
    def get_local_tables(self) -> List[str]:
        """Lista tabelas do banco local"""
        tables = []
        with sqlite3.connect(self.local_db) as conn:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                AND name NOT LIKE 'turso_sync_%'
                ORDER BY name
            """)
            tables = [row[0] for row in cursor.fetchall()]
        return tables
    
    def count_table_records(self, table_name: str, db_path: str = None) -> int:
        """Conta registros em uma tabela"""
        db_path = db_path or self.local_db
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cursor.fetchone()[0]
        except Exception:
            return 0
    
    def export_table_to_sql(self, table_name: str) -> str:
        """Exporta tabela local para comandos SQL"""
        sql_commands = []
        
        with sqlite3.connect(self.local_db) as conn:
            # Obter schema da tabela
            cursor = conn.execute(f"""
                SELECT sql FROM sqlite_master 
                WHERE type='table' AND name='{table_name}'
            """)
            schema = cursor.fetchone()
            if schema:
                sql_commands.append(f"{schema[0]};")
            
            # Obter dados
            cursor = conn.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            
            for row in cursor.fetchall():
                values = []
                for value in row:
                    if value is None:
                        values.append('NULL')
                    elif isinstance(value, str):
                        # Escapar aspas simples
                        escaped = value.replace("'", "''")
                        values.append(f"'{escaped}'")
                    else:
                        values.append(str(value))
                
                insert_sql = f"""
                INSERT OR REPLACE INTO {table_name} ({','.join(columns)})
                VALUES ({','.join(values)});
                """
                sql_commands.append(insert_sql)
        
        return '\n'.join(sql_commands)
    
    def sync_table_to_turso(self, table_name: str) -> bool:
        """Sincroniza uma tabela específica para o Turso"""
        print(f"📤 Enviando tabela {table_name} para Turso...")
        
        try:
            # Gerar SQL da tabela
            sql_content = self.export_table_to_sql(table_name)
            
            if not sql_content:
                print(f"   ⚠️  Tabela {table_name} vazia ou não encontrada")
                return False
            
            # Criar arquivo temporário com SQL
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
                temp_file.write(sql_content)
                temp_path = temp_file.name
            
            try:
                # Executar SQL no Turso
                with open(temp_path, 'r') as sql_file:
                    result = subprocess.run([
                        'turso', 'db', 'shell', self.turso_db
                    ], stdin=sql_file, capture_output=True, text=True, timeout=60)
                
                success = result.returncode == 0
                
                if success:
                    local_count = self.count_table_records(table_name)
                    print(f"   ✅ {table_name}: {local_count} registros sincronizados")
                else:
                    print(f"   ❌ Erro: {result.stderr}")
                
                return success
                
            finally:
                # Limpar arquivo temporário
                os.unlink(temp_path)
                
        except Exception as e:
            print(f"   ❌ Erro ao sincronizar {table_name}: {e}")
            return False
    
    def sync_all_to_turso(self) -> Dict[str, any]:
        """Sincroniza todas as tabelas para o Turso"""
        start_time = datetime.now()
        
        print("🚀 SINCRONIZAÇÃO: Local → Turso")
        print("=" * 40)
        
        # Verificar conexão
        if not self.check_turso_connection():
            error_msg = "Não foi possível conectar ao Turso. Verifique: turso auth login"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'tables_synced': 0,
                'duration': 0
            }
        
        # Obter tabelas locais
        tables = self.get_local_tables()
        print(f"📋 Encontradas {len(tables)} tabelas para sincronizar")
        print()
        
        # Sincronizar cada tabela
        results = {
            'success': True,
            'tables_synced': 0,
            'total_tables': len(tables),
            'sync_details': {},
            'errors': []
        }
        
        for table_name in tables:
            try:
                local_count = self.count_table_records(table_name)
                
                if local_count == 0:
                    print(f"⏭️  {table_name}: tabela vazia, pulando...")
                    continue
                
                success = self.sync_table_to_turso(table_name)
                
                if success:
                    results['tables_synced'] += 1
                    results['sync_details'][table_name] = {
                        'records': local_count,
                        'status': 'success'
                    }
                else:
                    results['errors'].append(f"Falha ao sincronizar {table_name}")
                    results['sync_details'][table_name] = {
                        'records': local_count,
                        'status': 'error'
                    }
                
            except Exception as e:
                error_msg = f"Erro em {table_name}: {e}"
                results['errors'].append(error_msg)
                print(f"   ❌ {error_msg}")
        
        # Registrar log de sincronização
        duration = (datetime.now() - start_time).total_seconds()
        results['duration'] = duration
        
        self.log_sync_operation('local_to_turso', results)
        
        print()
        print("📊 RESUMO DA SINCRONIZAÇÃO:")
        print(f"   ✅ Tabelas sincronizadas: {results['tables_synced']}/{results['total_tables']}")
        print(f"   ❌ Erros: {len(results['errors'])}")
        print(f"   ⏱️  Duração: {duration:.2f}s")
        
        if results['errors']:
            print(f"\n❌ ERROS ENCONTRADOS:")
            for error in results['errors']:
                print(f"   • {error}")
        
        return results
    
    def pull_from_turso(self) -> Dict[str, any]:
        """Baixa dados do Turso para local"""
        print("🚀 SINCRONIZAÇÃO: Turso → Local")
        print("=" * 40)
        
        if not self.check_turso_connection():
            error_msg = "Não foi possível conectar ao Turso"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
        
        try:
            # Fazer dump completo do Turso
            print("📥 Fazendo download do banco Turso...")
            
            result = subprocess.run([
                'turso', 'db', 'shell', self.turso_db,
                '.dump'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f"Erro ao fazer dump: {result.stderr}"
                }
            
            # Criar backup do banco local
            backup_path = f"{self.local_db}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            subprocess.run(['cp', self.local_db, backup_path])
            print(f"💾 Backup criado: {backup_path}")
            
            # Aplicar dump no banco local
            print("📥 Aplicando dados do Turso no banco local...")
            
            with sqlite3.connect(self.local_db) as conn:
                conn.executescript(result.stdout)
            
            print("✅ Sincronização Turso → Local concluída!")
            
            return {
                'success': True,
                'backup_created': backup_path,
                'tables_updated': 'all'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Erro durante pull: {e}"
            }
    
    def log_sync_operation(self, direction: str, results: Dict):
        """Registra operação de sincronização"""
        with sqlite3.connect(self.local_db) as conn:
            conn.execute("""
                INSERT INTO turso_sync_log 
                (sync_direction, tables_affected, records_synced, success, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (
                direction,
                json.dumps(list(results.get('sync_details', {}).keys())),
                results.get('tables_synced', 0),
                results.get('success', False),
                json.dumps(results.get('errors', []))
            ))
            conn.commit()
    
    def show_sync_status(self):
        """Mostra status atual da sincronização"""
        print("📊 STATUS DE SINCRONIZAÇÃO")
        print("=" * 40)
        
        # Verificar conexão
        turso_connected = self.check_turso_connection()
        print(f"🔗 Conexão Turso: {'✅ Conectado' if turso_connected else '❌ Desconectado'}")
        
        # Tabelas locais
        local_tables = self.get_local_tables()
        print(f"📋 Tabelas locais: {len(local_tables)}")
        
        # Contagem de registros por tabela
        print(f"\n📊 REGISTROS POR TABELA:")
        total_records = 0
        for table in local_tables:
            count = self.count_table_records(table)
            total_records += count
            if count > 0:
                print(f"   📄 {table}: {count:,} registros")
        
        print(f"\n📈 Total de registros: {total_records:,}")
        
        # Histórico de sincronização
        with sqlite3.connect(self.local_db) as conn:
            cursor = conn.execute("""
                SELECT sync_direction, sync_timestamp, tables_affected, records_synced, success
                FROM turso_sync_log 
                ORDER BY sync_timestamp DESC LIMIT 5
            """)
            
            sync_history = cursor.fetchall()
            
            if sync_history:
                print(f"\n📜 HISTÓRICO DE SYNC (últimas 5):")
                for record in sync_history:
                    direction, timestamp, tables, records, success = record
                    status = "✅" if success else "❌"
                    print(f"   {status} {timestamp} | {direction} | {records} registros")
            else:
                print(f"\n📜 Nenhuma sincronização anterior encontrada")
    
    def create_sync_script(self):
        """Cria script para sincronização automática"""
        script_content = f'''#!/bin/bash
# Script de Sincronização Automática
# Gerado em: {datetime.now()}

echo "🔄 Iniciando sincronização automática..."

cd "{os.getcwd()}"

# Sync Local -> Turso
python py-prp/simple_turso_sync.py push

echo "✅ Sincronização concluída!"
'''
        
        script_path = "sync_to_turso.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Tornar executável
        os.chmod(script_path, 0o755)
        
        print(f"📝 Script criado: {script_path}")
        print(f"   Execute: ./{script_path}")

def main():
    """Função principal"""
    import sys
    
    sync = SimpleTursoSync()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'push':
            # Sincronizar local → Turso
            results = sync.sync_all_to_turso()
            exit(0 if results['success'] else 1)
            
        elif command == 'pull':
            # Sincronizar Turso → local
            results = sync.pull_from_turso()
            exit(0 if results['success'] else 1)
            
        elif command == 'status':
            # Mostrar status
            sync.show_sync_status()
            
        elif command == 'create-script':
            # Criar script de automação
            sync.create_sync_script()
            
        else:
            print("Comandos disponíveis:")
            print("  push        - Enviar dados locais para Turso")
            print("  pull        - Baixar dados do Turso")
            print("  status      - Mostrar status de sincronização")
            print("  create-script - Criar script de automação")
    else:
        # Demo interativa
        print("🔄 SISTEMA DE SINCRONIZAÇÃO SQLite ↔ Turso")
        print("=" * 50)
        
        sync.show_sync_status()
        
        print(f"\n💡 COMANDOS DISPONÍVEIS:")
        print(f"   python py-prp/simple_turso_sync.py push")
        print(f"   python py-prp/simple_turso_sync.py pull") 
        print(f"   python py-prp/simple_turso_sync.py status")
        print(f"   python py-prp/simple_turso_sync.py create-script")

if __name__ == "__main__":
    main()