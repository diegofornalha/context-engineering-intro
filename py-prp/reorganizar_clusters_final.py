#!/usr/bin/env python3
"""
Reorganização Final de Clusters - Informações Atualizadas
Data: 02/08/2025

Organiza todos os documentos em clusters bem definidos e atualizados,
removendo obsoletos e mantendo apenas informações relevantes.
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Tuple

class ClusterOrganizer:
    """Organizador inteligente de clusters"""
    
    def __init__(self, db_path: str = "context-memory.db"):
        self.db_path = db_path
        self.setup_final_clusters()
    
    def setup_final_clusters(self):
        """Define clusters finais bem organizados"""
        self.final_clusters = {
            # Clusters principais atualizados
            'SISTEMA_FINAL': {
                'display_name': 'Sistema Final',
                'description': 'Documentação do sistema final implementado',
                'icon': '🎯',
                'keywords': ['final', 'sistema', 'implementado', 'completo', 'funcionando'],
                'priority': 1
            },
            'SYNC_INTELIGENTE': {
                'display_name': 'Sync Inteligente',
                'description': 'Sistema de sincronização inteligente via MCP',
                'icon': '🔄',
                'keywords': ['sync', 'inteligente', 'mcp', 'automatico', 'smart'],
                'priority': 2
            },
            'TURSO_DATABASE': {
                'display_name': 'Turso Database',
                'description': 'Configuração e uso do Turso Database',
                'icon': '🗄️',
                'keywords': ['turso', 'database', 'config', 'setup', 'sql'],
                'priority': 3
            },
            'MCP_INTEGRACAO': {
                'display_name': 'MCP Integração',
                'description': 'Integração com Model Context Protocol',
                'icon': '🔗',
                'keywords': ['mcp', 'integration', 'protocol', 'model', 'context'],
                'priority': 4
            },
            'PROJETO_VIVO': {
                'display_name': 'Projeto Vivo',
                'description': 'Sistema adaptativo e evolutivo',
                'icon': '🌱',
                'keywords': ['vivo', 'adaptativo', 'evolutivo', 'organico'],
                'priority': 5
            },
            'GUIAS_ESSENCIAIS': {
                'display_name': 'Guias Essenciais',
                'description': 'Guias fundamentais e essenciais',
                'icon': '⭐',
                'keywords': ['guia', 'essencial', 'fundamental', 'importante'],
                'priority': 6
            },
            'IMPLEMENTACAO': {
                'display_name': 'Implementação',
                'description': 'Documentos de implementação e desenvolvimento',
                'icon': '⚡',
                'keywords': ['implementacao', 'desenvolvimento', 'rapida', 'codigo'],
                'priority': 7
            },
            'CONFIGURACAO': {
                'display_name': 'Configuração',
                'description': 'Configurações de ambiente e setup',
                'icon': '🔧',
                'keywords': ['config', 'setup', 'env', 'ambiente', 'cursor'],
                'priority': 8
            },
            'MONITORAMENTO': {
                'display_name': 'Monitoramento',
                'description': 'Sentry, logs e monitoramento de erros',
                'icon': '📊',
                'keywords': ['sentry', 'monitor', 'error', 'log', 'tracking'],
                'priority': 9
            },
            'OBSOLETOS': {
                'display_name': 'Obsoletos',
                'description': 'Documentos obsoletos ou desatualizados',
                'icon': '🗑️',
                'keywords': ['obsoleto', 'old', 'deprecated', 'antigo'],
                'priority': 99
            }
        }
    
    def classify_document_intelligent(self, title: str, content: str, current_cluster: str) -> str:
        """Classifica documento de forma inteligente baseado no conteúdo"""
        title_lower = title.lower()
        content_lower = content.lower()[:2000]  # Primeiros 2000 chars
        
        # Pontuação por cluster
        scores = {}
        
        for cluster_name, cluster_info in self.final_clusters.items():
            score = 0
            keywords = cluster_info['keywords']
            
            # Pontuação baseada em palavras-chave no título (peso maior)
            for keyword in keywords:
                if keyword in title_lower:
                    score += 10
                if keyword in content_lower:
                    score += 3
            
            # Bonificação para clusters específicos baseado em padrões
            if cluster_name == 'SISTEMA_FINAL':
                if any(word in title_lower for word in ['final', 'simplificado', 'funcionando']):
                    score += 20
                if 'implementado' in content_lower and 'sucesso' in content_lower:
                    score += 15
            
            elif cluster_name == 'SYNC_INTELIGENTE':
                if 'sync' in title_lower and 'inteligente' in title_lower:
                    score += 25
                if 'mcp' in title_lower and 'smart' in content_lower:
                    score += 15
            
            elif cluster_name == 'PROJETO_VIVO':
                if 'vivo' in title_lower or 'adaptativo' in title_lower:
                    score += 25
                if 'evolui' in content_lower and 'organico' in content_lower:
                    score += 15
            
            elif cluster_name == 'TURSO_DATABASE':
                if 'turso' in title_lower:
                    score += 20
                if 'database' in title_lower or 'config' in title_lower:
                    score += 10
            
            elif cluster_name == 'OBSOLETOS':
                if any(word in title_lower for word in ['obsoleto', 'old', 'deprecated']):
                    score += 30
                # Documentos muito antigos sem atualizações
                if 'temp' in title_lower or 'test' in title_lower:
                    score += 20
            
            scores[cluster_name] = score
        
        # Retorna o cluster com maior pontuação
        best_cluster = max(scores.items(), key=lambda x: x[1])
        
        # Se a pontuação é muito baixa, mantém no cluster atual ou move para GERAL
        if best_cluster[1] < 5:
            return current_cluster if current_cluster else 'MCP_INTEGRACAO'
        
        return best_cluster[0]
    
    def reorganize_all_documents(self) -> Dict:
        """Reorganiza todos os documentos nos clusters atualizados"""
        results = {
            'reorganized': 0,
            'archived': 0,
            'clusters_updated': [],
            'movements': []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            # 1. Atualizar tabela de clusters
            for cluster_name, cluster_info in self.final_clusters.items():
                conn.execute("""
                    INSERT OR REPLACE INTO docs_clusters 
                    (name, display_name, description, icon, color, priority)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    cluster_name,
                    cluster_info['display_name'],
                    cluster_info['description'],
                    cluster_info['icon'],
                    '#6366F1',  # Cor padrão
                    cluster_info['priority']
                ))
                results['clusters_updated'].append(cluster_name)
            
            # 2. Reorganizar documentos
            cursor = conn.execute("""
                SELECT id, slug, title, content, cluster_name, content_status
                FROM docs 
                WHERE content_status = 'active'
            """)
            
            documents = cursor.fetchall()
            
            for doc_id, slug, title, content, current_cluster, status in documents:
                # Classificar no novo cluster
                new_cluster = self.classify_document_intelligent(title, content, current_cluster)
                
                if new_cluster != current_cluster:
                    # Atualizar cluster
                    conn.execute("""
                        UPDATE docs SET 
                            cluster_name = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (new_cluster, datetime.now().isoformat(), doc_id))
                    
                    results['reorganized'] += 1
                    results['movements'].append({
                        'doc': slug,
                        'from': current_cluster,
                        'to': new_cluster
                    })
                    
                    print(f"   📁 {slug}: {current_cluster} → {new_cluster}")
            
            # 3. Arquivar documentos obsoletos
            cursor = conn.execute("""
                UPDATE docs SET 
                    content_status = 'archived',
                    updated_at = ?
                WHERE cluster_name = 'OBSOLETOS'
                AND content_status = 'active'
            """, (datetime.now().isoformat(),))
            
            results['archived'] = cursor.rowcount
            
            # 4. Remover clusters vazios antigos
            conn.execute("""
                DELETE FROM docs_clusters 
                WHERE name NOT IN ({})
            """.format(','.join('?' * len(self.final_clusters))), 
            list(self.final_clusters.keys()))
            
            conn.commit()
        
        return results
    
    def get_final_organization(self) -> Dict:
        """Retorna organização final dos clusters"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Clusters com estatísticas
            cursor = conn.execute("""
                SELECT 
                    dc.name,
                    dc.display_name,
                    dc.icon,
                    dc.priority,
                    COUNT(d.id) as total_docs,
                    AVG(d.quality_score) as avg_quality,
                    COUNT(CASE WHEN d.content_status = 'active' THEN 1 END) as active_docs
                FROM docs_clusters dc
                LEFT JOIN docs d ON dc.name = d.cluster_name
                GROUP BY dc.name, dc.display_name, dc.icon, dc.priority
                ORDER BY dc.priority, active_docs DESC
            """)
            
            clusters = []
            total_active = 0
            
            for row in cursor.fetchall():
                cluster_data = dict(row)
                cluster_data['avg_quality'] = round(cluster_data['avg_quality'] or 0, 1)
                clusters.append(cluster_data)
                total_active += cluster_data['active_docs']
            
            return {
                'clusters': clusters,
                'total_active_docs': total_active,
                'total_clusters': len(clusters)
            }
    
    def cleanup_and_optimize(self) -> Dict:
        """Limpeza final e otimização"""
        results = {'actions': []}
        
        with sqlite3.connect(self.db_path) as conn:
            # 1. Atualizar timestamps de sync
            conn.execute("""
                UPDATE docs SET last_sync = ? WHERE last_sync IS NULL
            """, (datetime.now().isoformat(),))
            results['actions'].append("Timestamps de sync atualizados")
            
            # 2. Recalcular qualidade baseada na nova organização
            cursor = conn.execute("SELECT id, content FROM docs WHERE content_status = 'active'")
            
            for doc_id, content in cursor.fetchall():
                # Recalcular qualidade simples
                word_count = len(content.split())
                quality = 5.0
                
                if word_count > 500: quality += 1.0
                if word_count > 1000: quality += 1.0
                if '# ' in content: quality += 0.5
                if '```' in content: quality += 0.5
                if word_count < 100: quality -= 2.0
                
                quality = min(10.0, max(1.0, quality))
                
                conn.execute("""
                    UPDATE docs SET quality_score = ? WHERE id = ?
                """, (quality, doc_id))
            
            results['actions'].append("Qualidade recalculada para todos os documentos")
            
            # 3. VACUUM para otimizar banco
            conn.execute("VACUUM")
            results['actions'].append("Banco otimizado (VACUUM)")
            
            conn.commit()
        
        return results

def main():
    """Executa reorganização completa dos clusters"""
    print("📁 REORGANIZAÇÃO FINAL DE CLUSTERS")
    print("=" * 50)
    
    organizer = ClusterOrganizer()
    
    # 1. Reorganizar documentos
    print("\n🔄 Reorganizando documentos em clusters atualizados...")
    results = organizer.reorganize_all_documents()
    
    print(f"\n📊 RESULTADOS DA REORGANIZAÇÃO:")
    print(f"   📁 Clusters atualizados: {len(results['clusters_updated'])}")
    print(f"   🔄 Documentos reorganizados: {results['reorganized']}")
    print(f"   🗑️ Documentos arquivados: {results['archived']}")
    
    if results['movements']:
        print(f"\n📋 PRINCIPAIS MOVIMENTAÇÕES:")
        for movement in results['movements'][:10]:  # Mostrar primeiros 10
            print(f"      📄 {movement['doc']}: {movement['from']} → {movement['to']}")
    
    # 2. Mostrar organização final
    print(f"\n📁 ORGANIZAÇÃO FINAL DOS CLUSTERS:")
    organization = organizer.get_final_organization()
    
    for cluster in organization['clusters']:
        if cluster['active_docs'] > 0:
            icon = cluster['icon'] or '📁'
            name = cluster['display_name']
            docs = cluster['active_docs']
            quality = cluster['avg_quality']
            print(f"      {icon} {name}: {docs} docs (qualidade: {quality}/10)")
    
    print(f"\n📈 ESTATÍSTICAS FINAIS:")
    print(f"   📄 Total de documentos ativos: {organization['total_active_docs']}")
    print(f"   📁 Total de clusters: {organization['total_clusters']}")
    
    # 3. Limpeza e otimização
    print(f"\n🧹 Executando limpeza final...")
    cleanup = organizer.cleanup_and_optimize()
    
    print(f"\n✅ AÇÕES DE LIMPEZA EXECUTADAS:")
    for action in cleanup['actions']:
        print(f"      ✅ {action}")
    
    print(f"\n🎉 REORGANIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"   📁 Clusters organizados e atualizados")
    print(f"   📄 Documentos classificados inteligentemente")
    print(f"   🗑️ Obsoletos removidos automaticamente")
    print(f"   ⚡ Sistema otimizado para performance")
    print(f"   ✅ Pronto para sincronização!")

if __name__ == "__main__":
    main()