#!/usr/bin/env python3
"""
Sistema de Sincronização SQLite Local ↔ Turso Remoto
Data: 02/08/2025

Sistema inteligente de sincronização bidirecional entre banco SQLite local
e Turso remoto, com detecção de conflitos e resolução automática.
"""

import os
import json
import sqlite3
import hashlib
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile

@dataclass
class SyncConfig:
    """Configuração do sistema de sincronização"""
    local_db_path: str = "context-memory.db"
    turso_db_name: str = "context-memory"
    turso_org: str = "diegofornalha"
    sync_interval_minutes: int = 5
    conflict_resolution: str = "local_wins"  # local_wins, remote_wins, merge, manual
    enable_auto_sync: bool = True
    backup_before_sync: bool = True
    max_sync_retries: int = 3

@dataclass
class SyncRecord:
    """Registro de sincronização"""
    table_name: str
    record_id: Any
    local_hash: str
    remote_hash: str
    last_sync: datetime
    sync_status: str  # synced, conflict, pending, error

class TursoLocalSync:
    """
    Sistema de sincronização entre SQLite local e Turso remoto
    """
    
    def __init__(self, config: SyncConfig = None):
        self.config = config or SyncConfig()
        self.local_db = self.config.local_db_path
        self.sync_tables = [
            'docs', 'docs_clusters', 'docs_tags', 'docs_tag_relations',
            'docs_changes', 'docs_obsolescence_analysis',
            'prps', 'prp_tasks', 'prp_context', 'prp_tags', 
            'prp_tag_relations', 'prp_history', 'prp_llm_analysis'
        ]
        self.setup_sync_infrastructure()
    
    def setup_sync_infrastructure(self):
        """Configura infraestrutura de sincronização"""
        print("🔧 Configurando infraestrutura de sincronização...")
        
        with sqlite3.connect(self.local_db) as conn:
            # Tabela para controlar sincronização
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_control (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    local_hash TEXT,
                    remote_hash TEXT,
                    last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sync_status TEXT DEFAULT 'pending',
                    sync_direction TEXT DEFAULT 'bidirectional',
                    conflict_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(table_name, record_id)
                )
            """)
            
            # Tabela de logs de sincronização
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_session_id TEXT NOT NULL,
                    table_name TEXT,
                    operation TEXT,
                    records_affected INTEGER DEFAULT 0,
                    success BOOLEAN DEFAULT 1,
                    error_message TEXT,
                    execution_time_ms INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de configurações de sync
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sync_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Trigger para atualizar hashes quando dados mudam
            for table in self.sync_tables:
                if self.table_exists(conn, table):
                    conn.execute(f"""
                        CREATE TRIGGER IF NOT EXISTS sync_trigger_{table}
                        AFTER UPDATE ON {table}
                        FOR EACH ROW
                        BEGIN
                            INSERT OR REPLACE INTO sync_control (table_name, record_id, sync_status)
                            VALUES ('{table}', NEW.id, 'pending');
                        END
                    """)
            
            conn.commit()
    
    def table_exists(self, conn, table_name: str) -> bool:
        """Verifica se tabela existe"""
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    
    def calculate_record_hash(self, table_name: str, record_id: Any, db_path: str = None) -> str:
        """Calcula hash MD5 de um registro específico"""
        db_path = db_path or self.local_db
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
            
            # Buscar dados do registro
            cursor = conn.execute(f"""
                SELECT {','.join(columns)} FROM {table_name} WHERE id = ?
            """, (record_id,))
            
            record = cursor.fetchone()
            if not record:
                return ""
            
            # Criar string representativa do registro
            record_str = '|'.join(str(v) if v is not None else 'NULL' for v in record)
            
            # Calcular hash MD5
            return hashlib.md5(record_str.encode()).hexdigest()
    
    def get_turso_token(self) -> Optional[str]:
        """Obtém token do Turso a partir do ambiente ou CLI"""
        # Tentar variável de ambiente primeiro
        token = os.getenv('TURSO_AUTH_TOKEN')
        if token:
            return token
        
        # Tentar obter do CLI do Turso
        try:
            result = subprocess.run(['turso', 'auth', 'token'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return None
    
    def connect_to_turso(self) -> Optional[str]:
        """Conecta ao Turso e retorna path do banco temporário"""
        try:
            # Verificar se turso CLI está disponível
            result = subprocess.run(['turso', 'db', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print("❌ Turso CLI não disponível ou não autenticado")
                return None
            
            # Obter URL do banco
            result = subprocess.run(['turso', 'db', 'show', self.config.turso_db_name, '--url'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"❌ Banco {self.config.turso_db_name} não encontrado no Turso")
                return None
            
            db_url = result.stdout.strip()
            print(f"🔗 Conectado ao Turso: {db_url}")
            
            # Criar arquivo temporário para dump do Turso
            temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
            temp_file.close()
            
            # Fazer dump do banco Turso
            dump_result = subprocess.run([
                'turso', 'db', 'shell', self.config.turso_db_name,
                '.dump'
            ], capture_output=True, text=True, timeout=30)
            
            if dump_result.returncode == 0:
                # Criar banco SQLite temporário com o dump
                with sqlite3.connect(temp_file.name) as temp_conn:
                    temp_conn.executescript(dump_result.stdout)
                
                return temp_file.name
            
        except Exception as e:
            print(f"❌ Erro ao conectar com Turso: {e}")
        
        return None
    
    def compare_tables(self, local_db: str, remote_db: str, table_name: str) -> Dict[str, List]:
        """Compara tabela entre bancos local e remoto"""
        print(f"🔍 Comparando tabela {table_name}...")
        
        differences = {
            'local_only': [],
            'remote_only': [],
            'conflicts': [],
            'synced': []
        }
        
        # Obter registros de ambos os bancos
        local_records = {}
        remote_records = {}
        
        # Local
        with sqlite3.connect(local_db) as conn:
            if self.table_exists(conn, table_name):
                cursor = conn.execute(f"SELECT id FROM {table_name}")
                for row in cursor.fetchall():
                    record_id = row[0]
                    local_records[record_id] = self.calculate_record_hash(table_name, record_id, local_db)
        
        # Remoto
        with sqlite3.connect(remote_db) as conn:
            if self.table_exists(conn, table_name):
                cursor = conn.execute(f"SELECT id FROM {table_name}")
                for row in cursor.fetchall():
                    record_id = row[0]
                    remote_records[record_id] = self.calculate_record_hash(table_name, record_id, remote_db)
        
        # Comparar
        all_ids = set(local_records.keys()) | set(remote_records.keys())
        
        for record_id in all_ids:
            local_hash = local_records.get(record_id)
            remote_hash = remote_records.get(record_id)
            
            if local_hash and not remote_hash:
                differences['local_only'].append(record_id)
            elif remote_hash and not local_hash:
                differences['remote_only'].append(record_id)
            elif local_hash != remote_hash:
                differences['conflicts'].append(record_id)
            else:
                differences['synced'].append(record_id)
        
        return differences
    
    def sync_record_to_remote(self, table_name: str, record_id: Any) -> bool:
        """Sincroniza um registro específico para o Turso remoto"""
        try:
            # Obter dados do registro local
            with sqlite3.connect(self.local_db) as local_conn:
                cursor = local_conn.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                
                cursor = local_conn.execute(f"""
                    SELECT {','.join(columns)} FROM {table_name} WHERE id = ?
                """, (record_id,))
                
                record = cursor.fetchone()
                if not record:
                    return False
            
            # Preparar comando SQL para Turso
            placeholders = ','.join(['?' for _ in columns])
            insert_sql = f"""
                INSERT OR REPLACE INTO {table_name} ({','.join(columns)})
                VALUES ({placeholders})
            """
            
            # Escapar dados para shell
            escaped_values = []
            for value in record:
                if value is None:
                    escaped_values.append('NULL')
                elif isinstance(value, str):
                    escaped_values.append(f"'{value.replace("'", "''")}'")
                else:
                    escaped_values.append(str(value))
            
            shell_sql = f"""
                INSERT OR REPLACE INTO {table_name} ({','.join(columns)})
                VALUES ({','.join(escaped_values)});
            """
            
            # Executar no Turso
            result = subprocess.run([
                'turso', 'db', 'shell', self.config.turso_db_name,
                shell_sql
            ], capture_output=True, text=True, timeout=30)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Erro ao sincronizar registro {record_id} da tabela {table_name}: {e}")
            return False
    
    def sync_record_from_remote(self, table_name: str, record_id: Any, remote_db: str) -> bool:
        """Sincroniza um registro específico do Turso remoto"""
        try:
            # Obter dados do registro remoto
            with sqlite3.connect(remote_db) as remote_conn:
                cursor = remote_conn.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                
                cursor = remote_conn.execute(f"""
                    SELECT {','.join(columns)} FROM {table_name} WHERE id = ?
                """, (record_id,))
                
                record = cursor.fetchone()
                if not record:
                    return False
            
            # Inserir no banco local
            with sqlite3.connect(self.local_db) as local_conn:
                placeholders = ','.join(['?' for _ in columns])
                local_conn.execute(f"""
                    INSERT OR REPLACE INTO {table_name} ({','.join(columns)})
                    VALUES ({placeholders})
                """, record)
                local_conn.commit()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao sincronizar registro {record_id} da tabela {table_name} do remoto: {e}")
            return False
    
    def perform_sync(self, direction: str = 'bidirectional') -> Dict[str, Any]:
        """Executa sincronização completa"""
        sync_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        sync_results = {
            'session_id': sync_session_id,
            'start_time': datetime.now(),
            'tables_synced': 0,
            'records_synced': 0,
            'conflicts_found': 0,
            'errors': [],
            'success': True
        }
        
        print(f"🔄 Iniciando sincronização (sessão: {sync_session_id})")
        print(f"📍 Direção: {direction}")
        
        # Conectar ao Turso
        remote_db_path = self.connect_to_turso()
        if not remote_db_path:
            sync_results['success'] = False
            sync_results['errors'].append("Não foi possível conectar ao Turso")
            return sync_results
        
        try:
            # Sincronizar cada tabela
            for table_name in self.sync_tables:
                print(f"\n📋 Sincronizando tabela: {table_name}")
                
                # Comparar diferenças
                differences = self.compare_tables(self.local_db, remote_db_path, table_name)
                
                # Relatório de diferenças
                print(f"   📊 Local apenas: {len(differences['local_only'])}")
                print(f"   📊 Remoto apenas: {len(differences['remote_only'])}")
                print(f"   ⚠️  Conflitos: {len(differences['conflicts'])}")
                print(f"   ✅ Sincronizados: {len(differences['synced'])}")
                
                # Processar sincronização baseada na direção
                if direction in ['bidirectional', 'local_to_remote']:
                    # Enviar registros locais para remoto
                    for record_id in differences['local_only']:
                        if self.sync_record_to_remote(table_name, record_id):
                            sync_results['records_synced'] += 1
                            print(f"   ✅ Enviado para remoto: {record_id}")
                        else:
                            sync_results['errors'].append(f"Falha ao enviar {table_name}:{record_id}")
                
                if direction in ['bidirectional', 'remote_to_local']:
                    # Trazer registros remotos para local
                    for record_id in differences['remote_only']:
                        if self.sync_record_from_remote(table_name, record_id, remote_db_path):
                            sync_results['records_synced'] += 1
                            print(f"   ✅ Recebido do remoto: {record_id}")
                        else:
                            sync_results['errors'].append(f"Falha ao receber {table_name}:{record_id}")
                
                # Tratar conflitos
                if differences['conflicts']:
                    sync_results['conflicts_found'] += len(differences['conflicts'])
                    for record_id in differences['conflicts']:
                        resolved = self.resolve_conflict(table_name, record_id, remote_db_path)
                        if resolved:
                            sync_results['records_synced'] += 1
                            print(f"   🔧 Conflito resolvido: {record_id}")
                        else:
                            sync_results['errors'].append(f"Conflito não resolvido {table_name}:{record_id}")
                
                sync_results['tables_synced'] += 1
            
            # Atualizar controle de sincronização
            self.update_sync_control(sync_session_id, sync_results)
            
        finally:
            # Limpar arquivo temporário
            if remote_db_path and os.path.exists(remote_db_path):
                os.unlink(remote_db_path)
        
        sync_results['end_time'] = datetime.now()
        sync_results['duration'] = (sync_results['end_time'] - sync_results['start_time']).total_seconds()
        
        return sync_results
    
    def resolve_conflict(self, table_name: str, record_id: Any, remote_db_path: str) -> bool:
        """Resolve conflito entre versões local e remota"""
        resolution = self.config.conflict_resolution
        
        if resolution == 'local_wins':
            return self.sync_record_to_remote(table_name, record_id)
        elif resolution == 'remote_wins':
            return self.sync_record_from_remote(table_name, record_id, remote_db_path)
        elif resolution == 'merge':
            # Implementar lógica de merge (complexa)
            return self.merge_conflicted_record(table_name, record_id, remote_db_path)
        else:
            # Manual - apenas registrar o conflito
            self.log_manual_conflict(table_name, record_id)
            return False
    
    def merge_conflicted_record(self, table_name: str, record_id: Any, remote_db_path: str) -> bool:
        """Merge inteligente de registros conflitantes"""
        # Para documentação, preferir versão com maior qualidade ou mais recente
        try:
            if table_name == 'docs':
                # Comparar quality_score e updated_at
                with sqlite3.connect(self.local_db) as local_conn:
                    local_cursor = local_conn.execute("""
                        SELECT quality_score, updated_at FROM docs WHERE id = ?
                    """, (record_id,))
                    local_data = local_cursor.fetchone()
                
                with sqlite3.connect(remote_db_path) as remote_conn:
                    remote_cursor = remote_conn.execute("""
                        SELECT quality_score, updated_at FROM docs WHERE id = ?
                    """, (record_id,))
                    remote_data = remote_cursor.fetchone()
                
                if local_data and remote_data:
                    local_quality, local_updated = local_data
                    remote_quality, remote_updated = remote_data
                    
                    # Preferir maior qualidade, se igual, preferir mais recente
                    if local_quality > remote_quality:
                        return self.sync_record_to_remote(table_name, record_id)
                    elif remote_quality > local_quality:
                        return self.sync_record_from_remote(table_name, record_id, remote_db_path)
                    else:
                        # Qualidades iguais, preferir mais recente
                        if local_updated > remote_updated:
                            return self.sync_record_to_remote(table_name, record_id)
                        else:
                            return self.sync_record_from_remote(table_name, record_id, remote_db_path)
            
            # Para outras tabelas, preferir versão local por padrão
            return self.sync_record_to_remote(table_name, record_id)
            
        except Exception as e:
            print(f"❌ Erro no merge: {e}")
            return False
    
    def log_manual_conflict(self, table_name: str, record_id: Any):
        """Registra conflito para resolução manual"""
        with sqlite3.connect(self.local_db) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO sync_control 
                (table_name, record_id, sync_status, conflict_data)
                VALUES (?, ?, 'conflict', ?)
            """, (table_name, record_id, json.dumps({
                'timestamp': datetime.now().isoformat(),
                'requires_manual_resolution': True
            })))
            conn.commit()
    
    def update_sync_control(self, session_id: str, results: Dict):
        """Atualiza controle de sincronização"""
        with sqlite3.connect(self.local_db) as conn:
            conn.execute("""
                INSERT INTO sync_logs 
                (sync_session_id, operation, records_affected, success, execution_time_ms)
                VALUES (?, 'full_sync', ?, ?, ?)
            """, (
                session_id, 
                results['records_synced'],
                results['success'],
                int(results.get('duration', 0) * 1000)
            ))
            conn.commit()
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtém status atual da sincronização"""
        with sqlite3.connect(self.local_db) as conn:
            # Última sincronização
            cursor = conn.execute("""
                SELECT * FROM sync_logs 
                ORDER BY timestamp DESC LIMIT 1
            """)
            last_sync = cursor.fetchone()
            
            # Registros pendentes
            cursor = conn.execute("""
                SELECT table_name, COUNT(*) as pending_count
                FROM sync_control 
                WHERE sync_status = 'pending'
                GROUP BY table_name
            """)
            pending = dict(cursor.fetchall())
            
            # Conflitos manuais
            cursor = conn.execute("""
                SELECT COUNT(*) FROM sync_control 
                WHERE sync_status = 'conflict'
            """)
            conflicts = cursor.fetchone()[0]
            
            return {
                'last_sync': last_sync,
                'pending_records': pending,
                'manual_conflicts': conflicts,
                'turso_connected': self.connect_to_turso() is not None
            }
    
    def auto_sync_daemon(self):
        """Daemon de sincronização automática"""
        print(f"🤖 Iniciando daemon de sync (intervalo: {self.config.sync_interval_minutes}min)")
        
        while self.config.enable_auto_sync:
            try:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Executando sync automático...")
                results = self.perform_sync()
                
                if results['success']:
                    print(f"✅ Sync concluído: {results['records_synced']} registros")
                else:
                    print(f"❌ Sync falhou: {len(results['errors'])} erros")
                
                # Aguardar próximo ciclo
                time.sleep(self.config.sync_interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("\n🛑 Daemon de sync interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro no daemon de sync: {e}")
                time.sleep(60)  # Aguardar 1 minuto antes de tentar novamente

def demo_sync_system():
    """Demonstração do sistema de sincronização"""
    print("🔄 DEMONSTRAÇÃO: Sistema de Sincronização SQLite ↔ Turso")
    print("=" * 60)
    
    # Configurar sistema
    config = SyncConfig(
        sync_interval_minutes=1,  # Para demo
        conflict_resolution='local_wins',
        enable_auto_sync=False
    )
    
    sync_system = TursoLocalSync(config)
    
    # Verificar status inicial
    print("\n📊 STATUS INICIAL:")
    status = sync_system.get_sync_status()
    print(f"   🔗 Turso conectado: {'✅' if status['turso_connected'] else '❌'}")
    print(f"   📋 Registros pendentes: {sum(status['pending_records'].values())}")
    print(f"   ⚠️  Conflitos manuais: {status['manual_conflicts']}")
    
    if status['turso_connected']:
        # Executar sincronização de teste
        print(f"\n🚀 Executando sincronização de teste...")
        results = sync_system.perform_sync('local_to_remote')
        
        print(f"\n📈 RESULTADOS:")
        print(f"   📊 Tabelas sincronizadas: {results['tables_synced']}")
        print(f"   📋 Registros sincronizados: {results['records_synced']}")
        print(f"   ⚠️  Conflitos encontrados: {results['conflicts_found']}")
        print(f"   ⏱️  Duração: {results['duration']:.2f}s")
        print(f"   {'✅ Sucesso' if results['success'] else '❌ Falhou'}")
        
        if results['errors']:
            print(f"\n❌ ERROS ({len(results['errors'])}):")
            for error in results['errors'][:5]:
                print(f"   • {error}")
    else:
        print("\n⚠️  Turso não conectado - funcionalidades limitadas")
        print("   Configure: turso auth login")
    
    print(f"\n💡 FUNCIONALIDADES DISPONÍVEIS:")
    print(f"   🔄 Sync bidirecional automático")
    print(f"   🔍 Detecção inteligente de conflitos")
    print(f"   🔧 Resolução automática de conflitos")
    print(f"   📊 Monitoramento de status em tempo real")
    print(f"   🤖 Daemon de sincronização automática")
    print(f"   📋 Log completo de operações")

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        sync_system = TursoLocalSync()
        
        if command == 'sync':
            direction = sys.argv[2] if len(sys.argv) > 2 else 'bidirectional'
            results = sync_system.perform_sync(direction)
            print(f"Sincronização concluída: {results['records_synced']} registros")
            
        elif command == 'status':
            status = sync_system.get_sync_status()
            print(json.dumps(status, indent=2, default=str))
            
        elif command == 'daemon':
            sync_system.auto_sync_daemon()
            
        else:
            print("Comandos: sync [direction], status, daemon")
    else:
        demo_sync_system()

if __name__ == "__main__":
    main()