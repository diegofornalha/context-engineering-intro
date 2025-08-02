#!/usr/bin/env python3
"""
Demonstração do Sistema de Documentação em Clusters
Data: 02/08/2025

Script para demonstrar todas as funcionalidades do sistema de gestão
de documentação organizada em clusters com gestão de ciclo de vida.
"""

import sqlite3
import json
from datetime import datetime, date
from typing import List, Dict

class DocsClusterManager:
    """
    Gerenciador de documentação organizada em clusters
    """
    
    def __init__(self, db_path: str = "context-memory.db"):
        self.db_path = db_path
    
    def show_cluster_overview(self):
        """Mostra visão geral dos clusters"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT icon, display_name, active_docs, total_docs, 
                       avg_quality_score, max_docs
                FROM docs_clusters 
                ORDER BY avg_quality_score DESC
            """)
            
            clusters = cursor.fetchall()
            
            print("📊 OVERVIEW DOS CLUSTERS:")
            print("=" * 60)
            for cluster in clusters:
                status = "🟢" if cluster['active_docs'] <= cluster['max_docs'] else "🔴"
                print(f"{status} {cluster['icon']} {cluster['display_name']}")
                print(f"   📄 Documentos: {cluster['active_docs']}/{cluster['total_docs']} (máx: {cluster['max_docs']})")
                print(f"   ⭐ Qualidade média: {cluster['avg_quality_score']:.1f}/10")
                print()
    
    def show_cluster_health(self):
        """Mostra saúde dos clusters"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM v_cluster_health ORDER BY avg_quality_score DESC")
            clusters = cursor.fetchall()
            
            print("🏥 SAÚDE DOS CLUSTERS:")
            print("=" * 60)
            for cluster in clusters:
                health_icon = {
                    'healthy': '🟢',
                    'overcrowded': '🟡', 
                    'low_quality': '🟠',
                    'empty': '🔴'
                }.get(cluster['health_status'], '⚪')
                
                print(f"{health_icon} {cluster['icon']} {cluster['display_name']}")
                print(f"   Status: {cluster['health_status']}")
                print(f"   📋 Recomendação: {cluster['recommendation']}")
                print()
    
    def show_docs_by_cluster(self, cluster_name: str = None):
        """Mostra documentos de um cluster específico ou todos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if cluster_name:
                cursor.execute("""
                    SELECT d.*, dc.display_name as cluster_display_name, dc.icon as cluster_icon
                    FROM docs d
                    JOIN docs_clusters dc ON d.cluster_name = dc.name
                    WHERE d.cluster_name = ? AND d.content_status = 'active'
                    ORDER BY d.cluster_priority, d.quality_score DESC
                """, (cluster_name,))
            else:
                cursor.execute("""
                    SELECT d.*, dc.display_name as cluster_display_name, dc.icon as cluster_icon
                    FROM docs d
                    JOIN docs_clusters dc ON d.cluster_name = dc.name
                    WHERE d.content_status = 'active'
                    ORDER BY dc.avg_quality_score DESC, d.cluster_priority, d.quality_score DESC
                """)
            
            docs = cursor.fetchall()
            
            print(f"📚 DOCUMENTOS {'DO CLUSTER ' + cluster_name if cluster_name else 'POR CLUSTER'}:")
            print("=" * 60)
            
            current_cluster = None
            for doc in docs:
                if doc['cluster_name'] != current_cluster:
                    current_cluster = doc['cluster_name']
                    print(f"\n{doc['cluster_icon']} {doc['cluster_display_name']}:")
                    print("-" * 40)
                
                quality_stars = "⭐" * int(doc['quality_score'] / 2)
                relevance_bars = "📊" * int(doc['relevance_score'] / 2)
                
                print(f"  📄 {doc['title']}")
                print(f"     🎯 Qualidade: {quality_stars} ({doc['quality_score']:.1f}/10)")
                print(f"     📈 Relevância: {relevance_bars} ({doc['relevance_score']:.1f}/10)")
                print(f"     👀 Visualizações: {doc['view_count']} | 👍 Votos úteis: {doc['useful_votes']}")
                print(f"     ⏱️  Leitura: {doc['estimated_read_time']}min | 🏷️  Tipo: {doc['doc_type']}")
                print(f"     📝 {doc['summary'][:80]}...")
                print()
    
    def show_obsolete_management(self):
        """Mostra gestão de documentos obsoletos"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Documentos obsoletos
            cursor.execute("SELECT * FROM v_obsolete_docs")
            obsolete = cursor.fetchall()
            
            print("🗑️  GESTÃO DE DOCUMENTOS OBSOLETOS:")
            print("=" * 60)
            
            if obsolete:
                for doc in obsolete:
                    print(f"❌ {doc['obsolete_title']}")
                    print(f"   ➡️  Substituído por: {doc['superseded_by_title']}")
                    print(f"   📈 Nova qualidade: {doc['new_quality_score']:.1f}/10")
                    print(f"   📅 Obsoleto desde: {doc['obsolete_date']}")
                    print()
            else:
                print("✅ Nenhum documento obsoleto encontrado.")
                print()
            
            # Análise de obsolescência
            cursor.execute("""
                SELECT d.title, oa.obsolescence_score, oa.recommendation, oa.confidence
                FROM docs_obsolescence_analysis oa
                JOIN docs d ON oa.doc_id = d.id
                ORDER BY oa.obsolescence_score DESC
                LIMIT 5
            """)
            analysis = cursor.fetchall()
            
            if analysis:
                print("🔍 ANÁLISE DE OBSOLESCÊNCIA:")
                print("-" * 40)
                for item in analysis:
                    score_bar = "🟥" * int(item['obsolescence_score'] * 5)
                    confidence_bar = "🟦" * int(item['confidence'] * 5)
                    print(f"📄 {item['title']}")
                    print(f"   📊 Score obsolescência: {score_bar} ({item['obsolescence_score']:.2f})")
                    print(f"   🎯 Confiança: {confidence_bar} ({item['confidence']:.2f})")
                    print(f"   💡 Recomendação: {item['recommendation']}")
                    print()
    
    def show_docs_needing_attention(self):
        """Mostra documentos que precisam atenção"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM v_docs_need_attention LIMIT 10")
            docs = cursor.fetchall()
            
            print("⚠️  DOCUMENTOS QUE PRECISAM ATENÇÃO:")
            print("=" * 60)
            
            if docs:
                for doc in docs:
                    reason_icon = {
                        'low_quality': '📉',
                        'low_relevance': '🔻',
                        'needs_validation': '⏰',
                        'user_reported': '🚨'
                    }.get(doc['attention_reason'], '⚠️')
                    
                    print(f"{reason_icon} {doc['title']}")
                    print(f"   📁 Cluster: {doc['cluster_name']}")
                    print(f"   🎯 Qualidade: {doc['quality_score']:.1f} | Relevância: {doc['relevance_score']:.1f}")
                    print(f"   📅 Validado há {doc['days_since_validation']:.0f} dias")
                    print(f"   💭 Motivo: {doc['attention_reason']}")
                    print()
            else:
                print("✅ Todos os documentos estão em boa condição!")
                print()
    
    def show_change_history(self, limit: int = 10):
        """Mostra histórico de mudanças"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT dc.*, d.title
                FROM docs_changes dc
                JOIN docs d ON dc.doc_id = d.id
                ORDER BY dc.created_at DESC
                LIMIT ?
            """, (limit,))
            
            changes = cursor.fetchall()
            
            print(f"📜 HISTÓRICO DE MUDANÇAS (últimas {limit}):")
            print("=" * 60)
            
            for change in changes:
                change_icon = {
                    'created': '✨',
                    'updated': '📝',
                    'superseded': '🔄',
                    'archived': '📦',
                    'quality_update': '⭐'
                }.get(change['change_type'], '📄')
                
                print(f"{change_icon} {change['change_type'].upper()}: {change['title']}")
                print(f"   📅 {change['created_at']} por {change['changed_by']}")
                
                if change['old_content_status'] and change['new_content_status']:
                    print(f"   📊 Status: {change['old_content_status']} → {change['new_content_status']}")
                
                if change['old_quality_score'] and change['new_quality_score']:
                    print(f"   ⭐ Qualidade: {change['old_quality_score']:.1f} → {change['new_quality_score']:.1f}")
                
                if change['change_reason']:
                    print(f"   💭 Motivo: {change['change_reason']}")
                print()
    
    def search_across_clusters(self, query: str, cluster_filter: str = None):
        """Busca através dos clusters"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            sql = """
                SELECT d.*, dc.display_name as cluster_display_name, dc.icon as cluster_icon
                FROM docs d
                JOIN docs_clusters dc ON d.cluster_name = dc.name
                WHERE d.content_status = 'active' 
                  AND (d.title LIKE ? OR d.summary LIKE ? OR d.keywords LIKE ?)
            """
            params = [f"%{query}%", f"%{query}%", f"%{query}%"]
            
            if cluster_filter:
                sql += " AND d.cluster_name = ?"
                params.append(cluster_filter)
            
            sql += " ORDER BY d.quality_score DESC, d.relevance_score DESC"
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            print(f"🔍 BUSCA: '{query}'" + (f" no cluster {cluster_filter}" if cluster_filter else ""))
            print("=" * 60)
            
            if results:
                for doc in results:
                    print(f"{doc['cluster_icon']} {doc['title']}")
                    print(f"   📁 {doc['cluster_display_name']}")
                    print(f"   ⭐ {doc['quality_score']:.1f}/10 | 📈 {doc['relevance_score']:.1f}/10")
                    print(f"   📝 {doc['summary'][:100]}...")
                    print()
            else:
                print("❌ Nenhum resultado encontrado.")
                print()
    
    def get_system_stats(self):
        """Estatísticas gerais do sistema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Contadores básicos
            cursor.execute("SELECT COUNT(*) FROM docs WHERE content_status = 'active'")
            stats['active_docs'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM docs WHERE content_status = 'obsolete'")
            stats['obsolete_docs'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM docs_clusters")
            stats['total_clusters'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM docs_tags")
            stats['total_tags'] = cursor.fetchone()[0]
            
            # Qualidade média
            cursor.execute("SELECT AVG(quality_score) FROM docs WHERE content_status = 'active'")
            stats['avg_quality'] = cursor.fetchone()[0] or 0
            
            # Total de visualizações
            cursor.execute("SELECT SUM(view_count) FROM docs WHERE content_status = 'active'")
            stats['total_views'] = cursor.fetchone()[0] or 0
            
            return stats

def main():
    """Demonstração completa do sistema"""
    print("🚀 DEMONSTRAÇÃO: Sistema de Documentação em Clusters")
    print("Data: 02/08/2025")
    print("=" * 70)
    print()
    
    manager = DocsClusterManager()
    
    # Estatísticas gerais
    stats = manager.get_system_stats()
    print("📊 ESTATÍSTICAS GERAIS:")
    print(f"   📚 Documentos ativos: {stats['active_docs']}")
    print(f"   🗑️  Documentos obsoletos: {stats['obsolete_docs']}")
    print(f"   📁 Clusters organizacionais: {stats['total_clusters']}")
    print(f"   🏷️  Tags disponíveis: {stats['total_tags']}")
    print(f"   ⭐ Qualidade média: {stats['avg_quality']:.1f}/10")
    print(f"   👀 Total de visualizações: {stats['total_views']:,}")
    print()
    
    # Overview dos clusters
    manager.show_cluster_overview()
    
    # Saúde dos clusters
    manager.show_cluster_health()
    
    # Documentos por cluster (exemplo com MCP_CORE)
    manager.show_docs_by_cluster('MCP_CORE')
    
    # Gestão de documentos obsoletos
    manager.show_obsolete_management()
    
    # Documentos que precisam atenção
    manager.show_docs_needing_attention()
    
    # Histórico de mudanças
    manager.show_change_history(5)
    
    # Exemplo de busca
    manager.search_across_clusters('turso')
    
    print("🎉 BENEFÍCIOS DEMONSTRADOS:")
    print("=" * 70)
    print("✅ Organização em clusters temáticos")
    print("✅ Gestão automática de qualidade e relevância")
    print("✅ Identificação de conteúdo obsoleto")
    print("✅ Rastreamento de mudanças e evolução")
    print("✅ Sistema de atenção para manutenção")
    print("✅ Busca inteligente entre clusters")
    print("✅ Analytics em tempo real")
    print("✅ Prevenção de duplicação de conteúdo")
    print()
    
    print("💡 CASOS DE USO:")
    print("✅ Manter documentação sempre atualizada")
    print("✅ Identificar gaps de conhecimento automaticamente") 
    print("✅ Substituir conteúdo obsoleto de forma controlada")
    print("✅ Métricas de qualidade e engagement")
    print("✅ Base estruturada para alimentar IA")
    print("✅ Gestão de conhecimento organizacional")

if __name__ == "__main__":
    main()