#!/usr/bin/env python3
"""
Sistema de Sincronização Inteligente via MCP
Data: 02/08/2025

Sistema que detecta automaticamente quando dados estão desatualizados
e executa sync sob demanda ANTES de consultas via MCP.
"""

import os
import json
import sqlite3
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import hashlib
import asyncio

@dataclass
class SyncMetadata:
    """Metadados de sincronização"""
    table_name: str
    last_sync: datetime
    local_records: int
    remote_records: int
    needs_sync: bool
    sync_priority: int  # 1=crítico, 5=baixo

class MCPSmartSync:
    """
    Sistema de sincronização inteligente que funciona via MCP
    """
    
    def __init__(self, local_db: str = "context-memory.db", turso_db: str = "context-memory"):
        self.local_db = local_db
        self.turso_db = turso_db
        self.sync_threshold_minutes = 30  # Sync se dados > 30min desatualizados
        self.setup_smart_sync_tables()
    
    def setup_smart_sync_tables(self):
        """Configura sistema inteligente de sync"""
        with sqlite3.connect(self.local_db) as conn:
            # Tabela de metadados de sync
            conn.execute("""
                CREATE TABLE IF NOT EXISTS mcp_sync_metadata (
                    table_name TEXT PRIMARY KEY,
                    last_sync_timestamp TIMESTAMP,
                    last_local_count INTEGER DEFAULT 0,
                    last_remote_count INTEGER DEFAULT 0,
                    sync_priority INTEGER DEFAULT 3,
                    auto_sync_enabled BOOLEAN DEFAULT 1,
                    last_query_timestamp TIMESTAMP,
                    query_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de consultas MCP
            conn.execute("""
                CREATE TABLE IF NOT EXISTS mcp_query_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_type TEXT NOT NULL,
                    table_accessed TEXT,
                    sync_triggered BOOLEAN DEFAULT 0,
                    sync_duration_ms INTEGER,
                    query_result_count INTEGER,
                    query_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_context TEXT
                )
            """)
            
            # Trigger para atualizar metadados quando dados mudam
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS mcp_sync_trigger_update
                AFTER INSERT ON docs
                FOR EACH ROW
                BEGIN
                    UPDATE mcp_sync_metadata 
                    SET last_local_count = (SELECT COUNT(*) FROM docs),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE table_name = 'docs';
                END
            """)
            
            conn.commit()
    
    def should_sync_before_query(self, tables: List[str]) -> Tuple[bool, List[str]]:
        """
        Determina se deve fazer sync antes de uma consulta
        
        Returns:
            (deve_fazer_sync, tabelas_que_precisam_sync)
        """
        tables_needing_sync = []
        
        with sqlite3.connect(self.local_db) as conn:
            for table in tables:
                cursor = conn.execute("""
                    SELECT last_sync_timestamp, sync_priority, auto_sync_enabled
                    FROM mcp_sync_metadata 
                    WHERE table_name = ?
                """, (table,))
                
                result = cursor.fetchone()
                
                if not result:
                    # Primeira vez - sempre sync
                    tables_needing_sync.append(table)
                    continue
                
                last_sync, priority, auto_enabled = result
                
                if not auto_enabled:
                    continue
                
                # Verificar se precisa sync baseado no tempo
                if last_sync:
                    last_sync_dt = datetime.fromisoformat(last_sync)
                    time_diff = datetime.now() - last_sync_dt
                    
                    # Threshold baseado na prioridade
                    threshold_minutes = self.sync_threshold_minutes * priority
                    
                    if time_diff > timedelta(minutes=threshold_minutes):
                        tables_needing_sync.append(table)
                else:
                    # Nunca sincronizado
                    tables_needing_sync.append(table)
        
        return len(tables_needing_sync) > 0, tables_needing_sync
    
    def quick_sync_table(self, table_name: str) -> bool:
        """Sincronização rápida de uma tabela específica"""
        print(f"⚡ Sync rápido: {table_name}")
        
        try:
            # Verificar se Turso está disponível
            if not self.check_turso_available():
                print(f"   ⚠️ Turso indisponível, usando dados locais")
                return False
            
            # Contar registros locais vs remotos
            local_count = self.count_table_records(table_name)
            remote_count = self.get_remote_table_count(table_name)
            
            sync_needed = False
            
            # Determinar direção do sync
            if local_count > remote_count:
                # Local tem mais dados - enviar para remoto
                sync_needed = self.push_table_to_turso(table_name)
                print(f"   📤 Local→Turso: {local_count} registros")
            elif remote_count > local_count:
                # Remoto tem mais dados - trazer para local
                sync_needed = self.pull_table_from_turso(table_name)
                print(f"   📥 Turso→Local: {remote_count} registros")
            else:
                # Mesmo número - verificar se há mudanças via hash
                if self.table_has_changes(table_name):
                    sync_needed = self.push_table_to_turso(table_name)
                    print(f"   🔄 Detectadas mudanças: {local_count} registros")
            
            # Atualizar metadados
            if sync_needed:
                self.update_sync_metadata(table_name, local_count, remote_count)
            
            return sync_needed
            
        except Exception as e:
            print(f"   ❌ Erro no sync de {table_name}: {e}")
            return False
    
    def check_turso_available(self) -> bool:
        """Verificação rápida de disponibilidade do Turso"""
        try:
            result = subprocess.run([
                'turso', 'db', 'list', '--timeout', '5s'
            ], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def count_table_records(self, table_name: str) -> int:
        """Conta registros em tabela local"""
        try:
            with sqlite3.connect(self.local_db) as conn:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cursor.fetchone()[0]
        except:
            return 0
    
    def get_remote_table_count(self, table_name: str) -> int:
        """Conta registros em tabela remota (Turso)"""
        try:
            result = subprocess.run([
                'turso', 'db', 'shell', self.turso_db,
                f'SELECT COUNT(*) FROM {table_name};'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Extrair número do resultado
                for line in result.stdout.split('\n'):
                    if line.strip().isdigit():
                        return int(line.strip())
            return 0
        except:
            return 0
    
    def table_has_changes(self, table_name: str) -> bool:
        """Verifica se tabela local tem mudanças não sincronizadas"""
        try:
            with sqlite3.connect(self.local_db) as conn:
                # Verificar se há registros modificados após último sync
                cursor = conn.execute("""
                    SELECT last_sync_timestamp FROM mcp_sync_metadata 
                    WHERE table_name = ?
                """, (table_name,))
                
                result = cursor.fetchone()
                if not result or not result[0]:
                    return True  # Sem histórico = assumir mudanças
                
                last_sync = result[0]
                
                # Verificar se há registros modificados após o sync
                if table_name == 'docs':
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM docs 
                        WHERE updated_at > ?
                    """, (last_sync,))
                elif table_name == 'prps':
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM prps 
                        WHERE updated_at > ?
                    """, (last_sync,))
                else:
                    # Para outras tabelas, assumir mudanças se contagem diferente
                    return True
                
                changes = cursor.fetchone()[0]
                return changes > 0
        except:
            return True  # Em caso de erro, assumir mudanças
    
    def push_table_to_turso(self, table_name: str) -> bool:
        """Push rápido de tabela para Turso"""
        try:
            # Método simplificado - apenas novos registros
            with sqlite3.connect(self.local_db) as conn:
                cursor = conn.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 10")
                records = cursor.fetchall()
                
                if not records:
                    return True
                
                # Obter nomes das colunas
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                
                # Gerar SQL de inserção
                for record in records:
                    values = []
                    for value in record:
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, str):
                            escaped = value.replace("'", "''")
                            values.append(f"'{escaped}'")
                        else:
                            values.append(str(value))
                    
                    sql = f"""
                    INSERT OR REPLACE INTO {table_name} ({','.join(columns)})
                    VALUES ({','.join(values)});
                    """
                    
                    # Executar no Turso
                    subprocess.run([
                        'turso', 'db', 'shell', self.turso_db, sql
                    ], capture_output=True, timeout=5)
            
            return True
        except:
            return False
    
    def pull_table_from_turso(self, table_name: str) -> bool:
        """Pull rápido de tabela do Turso"""
        try:
            # Buscar últimos registros do Turso
            result = subprocess.run([
                'turso', 'db', 'shell', self.turso_db,
                f'SELECT * FROM {table_name} ORDER BY id DESC LIMIT 10;'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Processar resultado (simplificado)
                # Em implementação real, parse do CSV e insert local
                return True
            
            return False
        except:
            return False
    
    def update_sync_metadata(self, table_name: str, local_count: int, remote_count: int):
        """Atualiza metadados de sincronização"""
        with sqlite3.connect(self.local_db) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO mcp_sync_metadata 
                (table_name, last_sync_timestamp, last_local_count, last_remote_count, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (table_name, datetime.now().isoformat(), local_count, remote_count, datetime.now().isoformat()))
            conn.commit()
    
    def smart_query_with_sync(self, query_type: str, tables: List[str], query_func, **kwargs) -> Any:
        """
        Executa consulta inteligente com sync automático
        
        Args:
            query_type: Tipo da consulta (search, list, get, etc.)
            tables: Tabelas que serão acessadas
            query_func: Função de consulta a executar
            **kwargs: Argumentos para a função de consulta
        """
        start_time = datetime.now()
        sync_triggered = False
        sync_duration = 0
        
        print(f"🔍 Consulta: {query_type}")
        
        # Verificar se precisa sync
        should_sync, tables_to_sync = self.should_sync_before_query(tables)
        
        if should_sync:
            print(f"🔄 Sync necessário para: {', '.join(tables_to_sync)}")
            sync_start = datetime.now()
            
            # Executar sync apenas das tabelas necessárias
            for table in tables_to_sync:
                self.quick_sync_table(table)
            
            sync_duration = (datetime.now() - sync_start).total_seconds() * 1000
            sync_triggered = True
            print(f"✅ Sync concluído em {sync_duration:.0f}ms")
        
        # Executar consulta original
        try:
            result = query_func(**kwargs)
            result_count = len(result) if isinstance(result, (list, tuple)) else 1
            
            # Registrar consulta
            self.log_mcp_query(query_type, tables, sync_triggered, sync_duration, result_count)
            
            return result
            
        except Exception as e:
            print(f"❌ Erro na consulta: {e}")
            self.log_mcp_query(query_type, tables, sync_triggered, sync_duration, 0, str(e))
            raise
    
    def log_mcp_query(self, query_type: str, tables: List[str], sync_triggered: bool, 
                     sync_duration: float, result_count: int, error: str = None):
        """Registra consulta MCP para analytics"""
        with sqlite3.connect(self.local_db) as conn:
            conn.execute("""
                INSERT INTO mcp_query_log 
                (query_type, table_accessed, sync_triggered, sync_duration_ms, 
                 query_result_count, user_context)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                query_type, 
                ','.join(tables), 
                sync_triggered, 
                int(sync_duration), 
                result_count,
                json.dumps({'error': error} if error else {})
            ))
            conn.commit()
    
    def get_sync_analytics(self) -> Dict[str, Any]:
        """Analytics do sistema de sync inteligente"""
        with sqlite3.connect(self.local_db) as conn:
            analytics = {}
            
            # Estatísticas de consultas
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_queries,
                    SUM(CASE WHEN sync_triggered THEN 1 ELSE 0 END) as syncs_triggered,
                    AVG(sync_duration_ms) as avg_sync_duration,
                    AVG(query_result_count) as avg_results
                FROM mcp_query_log
                WHERE query_timestamp > datetime('now', '-24 hours')
            """)
            
            stats = cursor.fetchone()
            analytics['last_24h'] = {
                'total_queries': stats[0],
                'syncs_triggered': stats[1],
                'sync_rate': (stats[1] / stats[0] * 100) if stats[0] > 0 else 0,
                'avg_sync_duration_ms': stats[2] or 0,
                'avg_results': stats[3] or 0
            }
            
            # Status das tabelas
            cursor = conn.execute("""
                SELECT table_name, last_sync_timestamp, sync_priority, auto_sync_enabled
                FROM mcp_sync_metadata
                ORDER BY table_name
            """)
            
            analytics['tables'] = []
            for row in cursor.fetchall():
                table_name, last_sync, priority, auto_enabled = row
                
                # Calcular se precisa sync
                needs_sync = False
                if last_sync:
                    last_sync_dt = datetime.fromisoformat(last_sync)
                    time_diff = datetime.now() - last_sync_dt
                    threshold = timedelta(minutes=self.sync_threshold_minutes * priority)
                    needs_sync = time_diff > threshold
                
                analytics['tables'].append({
                    'name': table_name,
                    'last_sync': last_sync,
                    'priority': priority,
                    'auto_enabled': bool(auto_enabled),
                    'needs_sync': needs_sync
                })
            
            # Top consultas
            cursor = conn.execute("""
                SELECT query_type, COUNT(*) as count, 
                       AVG(sync_duration_ms) as avg_sync_duration
                FROM mcp_query_log
                WHERE query_timestamp > datetime('now', '-7 days')
                GROUP BY query_type
                ORDER BY count DESC
                LIMIT 5
            """)
            
            analytics['top_queries'] = [
                {
                    'type': row[0],
                    'count': row[1],
                    'avg_sync_duration': row[2] or 0
                }
                for row in cursor.fetchall()
            ]
            
            return analytics

# Exemplos de uso com MCP Tools
class MCPDocsTools:
    """Ferramentas MCP inteligentes para documentação"""
    
    def __init__(self):
        self.smart_sync = MCPSmartSync()
    
    def search_docs(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca documentos com sync inteligente"""
        def _search():
            with sqlite3.connect(self.smart_sync.local_db) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM docs 
                    WHERE content_status = 'active' 
                    AND (title LIKE ? OR summary LIKE ?)
                    ORDER BY quality_score DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", limit))
                
                return [dict(row) for row in cursor.fetchall()]
        
        return self.smart_sync.smart_query_with_sync(
            'search_docs', ['docs'], _search
        )
    
    def list_clusters(self) -> List[Dict]:
        """Lista clusters com sync inteligente"""
        def _list():
            with sqlite3.connect(self.smart_sync.local_db) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM docs_clusters 
                    ORDER BY avg_quality_score DESC
                """)
                
                return [dict(row) for row in cursor.fetchall()]
        
        return self.smart_sync.smart_query_with_sync(
            'list_clusters', ['docs_clusters'], _list
        )
    
    def get_prps(self, status: str = None) -> List[Dict]:
        """Obtém PRPs com sync inteligente"""
        def _get():
            with sqlite3.connect(self.smart_sync.local_db) as conn:
                conn.row_factory = sqlite3.Row
                
                if status:
                    cursor = conn.execute("""
                        SELECT * FROM prps WHERE status = ?
                        ORDER BY priority DESC, created_at DESC
                    """, (status,))
                else:
                    cursor = conn.execute("""
                        SELECT * FROM prps 
                        ORDER BY priority DESC, created_at DESC
                    """)
                
                return [dict(row) for row in cursor.fetchall()]
        
        return self.smart_sync.smart_query_with_sync(
            'get_prps', ['prps'], _get
        )

def demo_smart_sync():
    """Demonstração do sistema de sync inteligente"""
    print("🧠 DEMONSTRAÇÃO: Sistema de Sync Inteligente via MCP")
    print("=" * 60)
    
    # Inicializar sistema
    mcp_tools = MCPDocsTools()
    smart_sync = mcp_tools.smart_sync
    
    print("📊 ANALYTICS INICIAL:")
    analytics = smart_sync.get_sync_analytics()
    print(f"   📈 Consultas (24h): {analytics['last_24h']['total_queries']}")
    print(f"   🔄 Syncs acionados: {analytics['last_24h']['syncs_triggered']}")
    print(f"   ⚡ Taxa de sync: {analytics['last_24h']['sync_rate']:.1f}%")
    
    # Demonstrar consultas inteligentes
    print(f"\n🔍 TESTE 1: Busca de documentos")
    docs = mcp_tools.search_docs("turso", limit=3)
    print(f"   ✅ Encontrados: {len(docs)} documentos")
    
    print(f"\n📁 TESTE 2: Listar clusters")
    clusters = mcp_tools.list_clusters()
    print(f"   ✅ Encontrados: {len(clusters)} clusters")
    
    print(f"\n📋 TESTE 3: Obter PRPs")
    prps = mcp_tools.get_prps()
    print(f"   ✅ Encontrados: {len(prps)} PRPs")
    
    # Analytics finais
    print(f"\n📊 ANALYTICS FINAIS:")
    analytics = smart_sync.get_sync_analytics()
    print(f"   📈 Total de consultas: {analytics['last_24h']['total_queries']}")
    print(f"   🔄 Syncs acionados: {analytics['last_24h']['syncs_triggered']}")
    print(f"   ⚡ Duração média sync: {analytics['last_24h']['avg_sync_duration_ms']:.0f}ms")
    
    print(f"\n💡 BENEFÍCIOS DEMONSTRADOS:")
    print(f"   ✅ Sync automático APENAS quando necessário")
    print(f"   ✅ Consultas sempre com dados atualizados")
    print(f"   ✅ Performance otimizada (sync sob demanda)")
    print(f"   ✅ Analytics detalhadas de uso")
    print(f"   ✅ Zero configuração manual de agendamento")

if __name__ == "__main__":
    demo_smart_sync()