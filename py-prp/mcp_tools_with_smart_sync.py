#!/usr/bin/env python3
"""
MCP Tools com Sync Inteligente Integrado
Data: 02/08/2025

Ferramentas MCP que automaticamente detectam e sincronizam dados
antes de executar consultas, garantindo sempre dados atualizados.
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from mcp_smart_sync import MCPSmartSync

class SmartMCPTools:
    """
    Ferramentas MCP com sincronização inteligente automática
    """
    
    def __init__(self, local_db: str = "context-memory.db"):
        self.local_db = local_db
        self.smart_sync = MCPSmartSync(local_db)
        self.setup_mcp_tools()
    
    def setup_mcp_tools(self):
        """Configura ferramentas MCP"""
        print("🔧 Configurando MCP Tools com Sync Inteligente...")
    
    # ==============================================
    # DOCUMENTAÇÃO - FERRAMENTAS MCP
    # ==============================================
    
    def mcp_search_docs(self, query: str, category: str = None, 
                       difficulty: str = None, limit: int = 10) -> List[Dict]:
        """
        🔍 MCP Tool: Buscar documentos com sync automático
        
        Args:
            query: Texto a buscar
            category: Filtrar por categoria (mcp, turso, prp, etc.)
            difficulty: Filtrar por dificuldade (easy, medium, hard)
            limit: Número máximo de resultados
        """
        def _search():
            with sqlite3.connect(self.local_db) as conn:
                conn.row_factory = sqlite3.Row
                
                sql = """
                    SELECT id, slug, title, summary, category, difficulty,
                           quality_score, relevance_score, view_count, 
                           estimated_read_time, cluster_name
                    FROM docs 
                    WHERE content_status = 'active'
                    AND (title LIKE ? OR summary LIKE ? OR keywords LIKE ?)
                """
                params = [f"%{query}%", f"%{query}%", f"%{query}%"]
                
                if category:
                    sql += " AND category = ?"
                    params.append(category)
                
                if difficulty:
                    sql += " AND difficulty = ?"
                    params.append(difficulty)
                
                sql += " ORDER BY quality_score DESC, relevance_score DESC LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(sql, params)
                return [dict(row) for row in cursor.fetchall()]
        
        return self.smart_sync.smart_query_with_sync(
            'search_docs', ['docs'], _search
        )
    
    def mcp_get_doc_by_id(self, doc_id: int) -> Optional[Dict]:
        """
        📄 MCP Tool: Obter documento por ID com sync automático
        """
        def _get():
            with sqlite3.connect(self.local_db) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM docs WHERE id = ? AND content_status = 'active'
                """, (doc_id,))
                
                result = cursor.fetchone()
                return dict(result) if result else None
        
        return self.smart_sync.smart_query_with_sync(
            'get_doc_by_id', ['docs'], _get
        )
    
    def mcp_list_clusters(self, include_stats: bool = True) -> List[Dict]:
        """
        📁 MCP Tool: Listar clusters de documentação com sync automático
        """
        def _list():
            with sqlite3.connect(self.local_db) as conn:
                conn.row_factory = sqlite3.Row
                
                if include_stats:
                    cursor = conn.execute("""
                        SELECT * FROM v_active_docs_by_cluster
                        ORDER BY avg_quality DESC
                    """)
                else:
                    cursor = conn.execute("""
                        SELECT name, display_name, description, icon, color
                        FROM docs_clusters
                        ORDER BY display_name
                    """)
                
                return [dict(row) for row in cursor.fetchall()]
        
        tables = ['docs_clusters', 'docs'] if include_stats else ['docs_clusters']
        return self.smart_sync.smart_query_with_sync(
            'list_clusters', tables, _list
        )
    
    def mcp_get_docs_by_cluster(self, cluster_name: str, limit: int = 20) -> List[Dict]:
        """
        📋 MCP Tool: Obter documentos de um cluster específico
        """
        def _get():
            with sqlite3.connect(self.local_db) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT id, title, summary, quality_score, view_count,
                           estimated_read_time, difficulty, doc_type
                    FROM docs 
                    WHERE cluster_name = ? AND content_status = 'active'
                    ORDER BY cluster_priority, quality_score DESC
                    LIMIT ?
                """, (cluster_name, limit))
                
                return [dict(row) for row in cursor.fetchall()]
        
        return self.smart_sync.smart_query_with_sync(
            'get_docs_by_cluster', ['docs'], _get
        )
    
    # ==============================================
    # PRPs - FERRAMENTAS MCP
    # ==============================================
    
    def mcp_search_prps(self, query: str = None, status: str = None, 
                       priority: str = None, limit: int = 10) -> List[Dict]:
        """
        🎯 MCP Tool: Buscar PRPs com sync automático
        """
        def _search():
            with sqlite3.connect(self.local_db) as conn:
                conn.row_factory = sqlite3.Row
                
                sql = "SELECT * FROM prps WHERE 1=1"
                params = []
                
                if query:
                    sql += " AND (name LIKE ? OR title LIKE ? OR description LIKE ?)"
                    params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
                
                if status:
                    sql += " AND status = ?"
                    params.append(status)
                
                if priority:
                    sql += " AND priority = ?"
                    params.append(priority)
                
                sql += " ORDER BY priority DESC, created_at DESC LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(sql, params)
                return [dict(row) for row in cursor.fetchall()]
        
        return self.smart_sync.smart_query_with_sync(
            'search_prps', ['prps'], _search
        )
    
    def mcp_get_prp_with_tasks(self, prp_id: int) -> Optional[Dict]:
        """
        📋 MCP Tool: Obter PRP com suas tarefas
        """
        def _get():
            with sqlite3.connect(self.local_db) as conn:
                conn.row_factory = sqlite3.Row
                
                # Buscar PRP
                cursor = conn.execute("SELECT * FROM prps WHERE id = ?", (prp_id,))
                prp = cursor.fetchone()
                
                if not prp:
                    return None
                
                prp_dict = dict(prp)
                
                # Buscar tarefas
                cursor = conn.execute("""
                    SELECT * FROM prp_tasks 
                    WHERE prp_id = ? 
                    ORDER BY priority DESC, created_at ASC
                """, (prp_id,))
                
                prp_dict['tasks'] = [dict(row) for row in cursor.fetchall()]
                
                # Buscar contexto
                cursor = conn.execute("""
                    SELECT * FROM prp_context 
                    WHERE prp_id = ?
                """, (prp_id,))
                
                prp_dict['context'] = [dict(row) for row in cursor.fetchall()]
                
                return prp_dict
        
        return self.smart_sync.smart_query_with_sync(
            'get_prp_with_tasks', ['prps', 'prp_tasks', 'prp_context'], _get
        )
    
    def mcp_get_prp_analytics(self) -> Dict[str, Any]:
        """
        📊 MCP Tool: Analytics de PRPs com sync automático
        """
        def _analytics():
            with sqlite3.connect(self.local_db) as conn:
                analytics = {}
                
                # Contadores básicos
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_prps,
                        COUNT(CASE WHEN status = 'active' THEN 1 END) as active_prps,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_prps,
                        COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_priority,
                        COUNT(CASE WHEN priority = 'critical' THEN 1 END) as critical_prps
                    FROM prps
                """)
                
                stats = cursor.fetchone()
                analytics['summary'] = {
                    'total_prps': stats[0],
                    'active_prps': stats[1],
                    'completed_prps': stats[2],
                    'high_priority': stats[3],
                    'critical_prps': stats[4]
                }
                
                # PRPs por status
                cursor = conn.execute("""
                    SELECT status, COUNT(*) as count
                    FROM prps
                    GROUP BY status
                    ORDER BY count DESC
                """)
                
                analytics['by_status'] = [
                    {'status': row[0], 'count': row[1]}
                    for row in cursor.fetchall()
                ]
                
                # Tarefas por PRP
                cursor = conn.execute("""
                    SELECT 
                        p.name,
                        COUNT(t.id) as task_count,
                        COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks
                    FROM prps p
                    LEFT JOIN prp_tasks t ON p.id = t.prp_id
                    WHERE p.status = 'active'
                    GROUP BY p.id, p.name
                    ORDER BY task_count DESC
                    LIMIT 5
                """)
                
                analytics['top_prps_by_tasks'] = [
                    {
                        'name': row[0],
                        'total_tasks': row[1],
                        'completed_tasks': row[2],
                        'completion_rate': (row[2] / row[1] * 100) if row[1] > 0 else 0
                    }
                    for row in cursor.fetchall()
                ]
                
                return analytics
        
        return self.smart_sync.smart_query_with_sync(
            'get_prp_analytics', ['prps', 'prp_tasks'], _analytics
        )
    
    # ==============================================
    # SISTEMA - FERRAMENTAS MCP
    # ==============================================
    
    def mcp_get_sync_status(self) -> Dict[str, Any]:
        """
        ⚙️ MCP Tool: Status do sistema de sincronização
        """
        analytics = self.smart_sync.get_sync_analytics()
        
        # Adicionar informações extras
        with sqlite3.connect(self.local_db) as conn:
            # Contagem total de registros
            cursor = conn.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM docs) as docs_count,
                    (SELECT COUNT(*) FROM prps) as prps_count,
                    (SELECT COUNT(*) FROM docs_clusters) as clusters_count,
                    (SELECT COUNT(*) FROM prp_tasks) as tasks_count
            """)
            
            counts = cursor.fetchone()
            analytics['record_counts'] = {
                'docs': counts[0],
                'prps': counts[1],
                'clusters': counts[2],
                'tasks': counts[3]
            }
        
        return analytics
    
    def mcp_health_check(self) -> Dict[str, Any]:
        """
        🏥 MCP Tool: Verificação de saúde do sistema
        """
        health = {
            'status': 'healthy',
            'issues': [],
            'recommendations': [],
            'last_check': datetime.now().isoformat()
        }
        
        with sqlite3.connect(self.local_db) as conn:
            # Verificar documentos que precisam atenção
            cursor = conn.execute("SELECT COUNT(*) FROM v_docs_need_attention")
            docs_needing_attention = cursor.fetchone()[0]
            
            if docs_needing_attention > 0:
                health['issues'].append(f"{docs_needing_attention} documentos precisam atenção")
                health['recommendations'].append("Revisar documentos com baixa qualidade/relevância")
            
            # Verificar PRPs órfãos (sem tarefas)
            cursor = conn.execute("""
                SELECT COUNT(*) FROM prps p
                LEFT JOIN prp_tasks t ON p.id = t.prp_id
                WHERE t.id IS NULL AND p.status = 'active'
            """)
            orphan_prps = cursor.fetchone()[0]
            
            if orphan_prps > 0:
                health['issues'].append(f"{orphan_prps} PRPs ativos sem tarefas")
                health['recommendations'].append("Adicionar tarefas aos PRPs ou revisar status")
            
            # Verificar clusters vazios
            cursor = conn.execute("""
                SELECT COUNT(*) FROM docs_clusters dc
                LEFT JOIN docs d ON dc.name = d.cluster_name AND d.content_status = 'active'
                WHERE d.id IS NULL
            """)
            empty_clusters = cursor.fetchone()[0]
            
            if empty_clusters > 0:
                health['issues'].append(f"{empty_clusters} clusters vazios")
                health['recommendations'].append("Remover clusters vazios ou adicionar documentação")
        
        # Determinar status geral
        if len(health['issues']) == 0:
            health['status'] = 'healthy'
        elif len(health['issues']) <= 2:
            health['status'] = 'warning'
        else:
            health['status'] = 'unhealthy'
        
        return health

def demo_mcp_tools():
    """Demonstração das ferramentas MCP com sync inteligente"""
    print("🛠️ DEMONSTRAÇÃO: MCP Tools com Sync Inteligente")
    print("=" * 60)
    
    tools = SmartMCPTools()
    
    # Teste 1: Buscar documentos
    print("\n🔍 TESTE 1: Buscar documentos sobre 'turso'")
    docs = tools.mcp_search_docs("turso", limit=3)
    print(f"   ✅ Encontrados: {len(docs)} documentos")
    for doc in docs:
        print(f"      📄 {doc['title']} (qualidade: {doc['quality_score']}/10)")
    
    # Teste 2: Listar clusters
    print(f"\n📁 TESTE 2: Listar clusters com estatísticas")
    clusters = tools.mcp_list_clusters()
    print(f"   ✅ Encontrados: {len(clusters)} clusters")
    for cluster in clusters[:3]:
        print(f"      {cluster.get('cluster_icon', '📁')} {cluster.get('cluster_display_name', cluster.get('display_name'))}")
    
    # Teste 3: Analytics de PRPs
    print(f"\n📊 TESTE 3: Analytics de PRPs")
    analytics = tools.mcp_get_prp_analytics()
    print(f"   📋 Total de PRPs: {analytics['summary']['total_prps']}")
    print(f"   ✅ PRPs ativos: {analytics['summary']['active_prps']}")
    print(f"   🎯 Alta prioridade: {analytics['summary']['high_priority']}")
    
    # Teste 4: Health check
    print(f"\n🏥 TESTE 4: Verificação de saúde")
    health = tools.mcp_health_check()
    status_icon = {'healthy': '🟢', 'warning': '🟡', 'unhealthy': '🔴'}.get(health['status'], '⚪')
    print(f"   {status_icon} Status: {health['status']}")
    print(f"   ⚠️  Issues: {len(health['issues'])}")
    print(f"   💡 Recomendações: {len(health['recommendations'])}")
    
    # Teste 5: Status de sync
    print(f"\n⚙️ TESTE 5: Status de sincronização")
    sync_status = tools.mcp_get_sync_status()
    print(f"   📊 Consultas (24h): {sync_status['last_24h']['total_queries']}")
    print(f"   🔄 Taxa de sync: {sync_status['last_24h']['sync_rate']:.1f}%")
    print(f"   📄 Total de docs: {sync_status['record_counts']['docs']}")
    
    print(f"\n🎉 FUNCIONALIDADES DEMONSTRADAS:")
    print(f"   ✅ Sync automático antes de CADA consulta")
    print(f"   ✅ Dados sempre atualizados sem configuração")
    print(f"   ✅ Performance otimizada (sync apenas quando necessário)")
    print(f"   ✅ Analytics detalhadas de uso e sync")
    print(f"   ✅ Health check automático do sistema")
    print(f"   ✅ Zero overhead quando dados estão atualizados")

if __name__ == "__main__":
    demo_mcp_tools()