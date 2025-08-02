#!/usr/bin/env python3
"""
Sync Automático de Documentação
Data: 02/08/2025

Sistema que sincroniza automaticamente os arquivos .md da pasta docs/
com o banco de dados local e remoto, mantendo tudo atualizado.
"""

import os
import re
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import subprocess

class DocsAutoSync:
    """Sistema de sincronização automática de documentação"""
    
    def __init__(self, docs_folder: str = "docs", db_path: str = "context-memory.db"):
        self.docs_folder = Path(docs_folder)
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Configura banco com schema simplificado"""
        with sqlite3.connect(self.db_path) as conn:
            # Aplicar schema simplificado
            schema_path = Path("sql-db/schema_simplificado_final.sql")
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    conn.executescript(f.read())
    
    def extract_metadata_from_md(self, content: str, file_path: Path) -> Dict:
        """Extrai metadados do arquivo markdown"""
        lines = content.split('\n')
        
        # Extrair título (primeira linha com #)
        title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        for line in lines[:10]:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Gerar resumo (primeiros parágrafos sem markdown)
        summary_lines = []
        for line in lines[:20]:
            clean_line = re.sub(r'[#*`\-\[\]()]', '', line).strip()
            if clean_line and len(clean_line) > 20:
                summary_lines.append(clean_line)
                if len(summary_lines) >= 3:
                    break
        
        summary = ' '.join(summary_lines)[:300] + '...' if summary_lines else ''
        
        # Detectar categoria baseada no nome/conteúdo
        category = self.detect_category(file_path.name, content)
        
        # Detectar cluster baseado no nome/conteúdo
        cluster = self.detect_cluster(file_path.name, content)
        
        # Extrair tags simples
        tags = self.extract_tags(file_path.name, content)
        
        # Calcular qualidade baseada em tamanho e estrutura
        quality_score = self.calculate_quality_score(content)
        
        # Estimar tempo de leitura
        word_count = len(content.split())
        read_time = max(1, word_count // 200)  # ~200 palavras por minuto
        
        # Extrair palavras-chave
        keywords = self.extract_keywords(title, content)
        
        return {
            'title': title,
            'summary': summary,
            'category': category,
            'cluster_name': cluster,
            'tags': json.dumps(tags),
            'quality_score': quality_score,
            'estimated_read_time': read_time,
            'keywords': keywords,
            'content_hash': hashlib.md5(content.encode()).hexdigest()
        }
    
    def detect_category(self, filename: str, content: str) -> str:
        """Detecta categoria do documento"""
        name_lower = filename.lower()
        content_lower = content.lower()
        
        if any(word in name_lower for word in ['guia', 'guide', 'tutorial', 'how']):
            return 'guia'
        elif any(word in name_lower for word in ['config', 'setup', 'install']):
            return 'configuracao'
        elif any(word in name_lower for word in ['status', 'report', 'resumo', 'summary']):
            return 'relatorio'
        elif any(word in name_lower for word in ['erro', 'error', 'troubleshoot', 'debug']):
            return 'troubleshooting'
        elif any(word in name_lower for word in ['implementacao', 'impl', 'develop']):
            return 'desenvolvimento'
        elif any(word in name_lower for word in ['final', 'completo', 'complete']):
            return 'final'
        else:
            return 'documentacao'
    
    def detect_cluster(self, filename: str, content: str) -> str:
        """Detecta cluster baseado no conteúdo"""
        name_lower = filename.lower()
        content_lower = content.lower()
        
        # Clusters específicos baseados em palavras-chave
        if any(word in name_lower + content_lower for word in ['mcp', 'model context protocol']):
            return 'mcp-integracao'
        elif any(word in name_lower + content_lower for word in ['turso', 'database', 'sql']):
            return 'turso-database'
        elif any(word in name_lower + content_lower for word in ['sync', 'sincronizacao', 'integration']):
            return 'sync-sistema'
        elif any(word in name_lower for word in ['final', 'completo', 'guia_final', 'essencial']):
            return 'guias-essenciais'
        elif any(word in name_lower + content_lower for word in ['desenvolvimento', 'implementacao', 'codigo']):
            return 'desenvolvimento'
        elif any(word in name_lower for word in ['obsoleto', 'deprecated', 'old', 'antigo']):
            return 'obsoletos'
        else:
            return 'documentacao'
    
    def extract_tags(self, filename: str, content: str) -> List[str]:
        """Extrai tags relevantes"""
        tags = set()
        
        # Tags baseadas no nome do arquivo
        name_parts = re.split(r'[_\-\.]', filename.lower())
        for part in name_parts:
            if len(part) > 2 and part not in ['md', 'the', 'and', 'for', 'with']:
                tags.add(part)
        
        # Tags baseadas em palavras-chave comuns
        tech_keywords = [
            'mcp', 'turso', 'sync', 'cursor', 'agent', 'prp', 'sentry',
            'python', 'typescript', 'javascript', 'sql', 'database',
            'integration', 'implementation', 'configuration', 'setup'
        ]
        
        content_lower = content.lower()
        for keyword in tech_keywords:
            if keyword in content_lower:
                tags.add(keyword)
        
        return sorted(list(tags))
    
    def calculate_quality_score(self, content: str) -> float:
        """Calcula score de qualidade do documento"""
        score = 5.0  # Base
        
        # Bônus por tamanho adequado
        word_count = len(content.split())
        if word_count > 500:
            score += 1.0
        if word_count > 1000:
            score += 1.0
        
        # Bônus por estrutura
        if '# ' in content:  # Tem títulos
            score += 0.5
        if '## ' in content:  # Tem subtítulos
            score += 0.5
        if '```' in content:  # Tem código
            score += 0.5
        if '- ' in content or '* ' in content:  # Tem listas
            score += 0.5
        
        # Penalidade por muito curto
        if word_count < 100:
            score -= 2.0
        
        return min(10.0, max(1.0, score))
    
    def extract_keywords(self, title: str, content: str) -> str:
        """Extrai palavras-chave para busca"""
        # Combinar título e primeiras linhas
        text = f"{title} {content[:500]}"
        
        # Remover markdown e caracteres especiais
        clean_text = re.sub(r'[#*`\-\[\](){}]', ' ', text)
        
        # Extrair palavras importantes
        words = clean_text.lower().split()
        keywords = []
        
        for word in words:
            if len(word) > 3 and word.isalpha():
                keywords.append(word)
                if len(keywords) >= 20:
                    break
        
        return ' '.join(keywords)
    
    def is_file_obsolete(self, file_path: Path) -> bool:
        """Verifica se arquivo deve ser considerado obsoleto"""
        name_lower = file_path.name.lower()
        
        # Arquivos marcados como obsoletos
        obsolete_indicators = [
            'obsoleto', 'deprecated', 'old', 'antigo', 'removido',
            'deleted', 'backup', 'temp', 'test'
        ]
        
        return any(indicator in name_lower for indicator in obsolete_indicators)
    
    def get_file_content_hash(self, file_path: Path) -> str:
        """Calcula hash do conteúdo do arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return hashlib.md5(content.encode()).hexdigest()
        except:
            return ""
    
    def sync_single_file(self, file_path: Path) -> Dict:
        """Sincroniza um arquivo específico"""
        try:
            # Ler conteúdo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair metadados
            metadata = self.extract_metadata_from_md(content, file_path)
            
            # Gerar slug único
            slug = file_path.stem.lower().replace('_', '-').replace(' ', '-')
            
            # Status baseado em obsolescência
            content_status = 'archived' if self.is_file_obsolete(file_path) else 'active'
            
            with sqlite3.connect(self.db_path) as conn:
                # Verificar se já existe
                cursor = conn.execute("SELECT id, content FROM docs WHERE slug = ?", (slug,))
                existing = cursor.fetchone()
                
                if existing:
                    # Verificar se mudou
                    existing_hash = hashlib.md5(existing[1].encode()).hexdigest()
                    if existing_hash != metadata['content_hash']:
                        # Atualizar
                        conn.execute("""
                            UPDATE docs SET
                                title = ?, content = ?, summary = ?, file_path = ?,
                                category = ?, tags = ?, cluster_name = ?,
                                quality_score = ?, estimated_read_time = ?, keywords = ?,
                                content_status = ?, last_sync = ?, updated_at = ?
                            WHERE slug = ?
                        """, (
                            metadata['title'], content, metadata['summary'], str(file_path),
                            metadata['category'], metadata['tags'], metadata['cluster_name'],
                            metadata['quality_score'], metadata['estimated_read_time'], metadata['keywords'],
                            content_status, datetime.now().isoformat(), datetime.now().isoformat(),
                            slug
                        ))
                        return {'action': 'updated', 'slug': slug}
                    else:
                        # Só atualizar timestamp de sync
                        conn.execute("UPDATE docs SET last_sync = ? WHERE slug = ?", 
                                   (datetime.now().isoformat(), slug))
                        return {'action': 'unchanged', 'slug': slug}
                else:
                    # Inserir novo
                    conn.execute("""
                        INSERT INTO docs (
                            slug, title, content, summary, file_path, category, tags, cluster_name,
                            quality_score, estimated_read_time, keywords, content_status, last_sync
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        slug, metadata['title'], content, metadata['summary'], str(file_path),
                        metadata['category'], metadata['tags'], metadata['cluster_name'],
                        metadata['quality_score'], metadata['estimated_read_time'], metadata['keywords'],
                        content_status, datetime.now().isoformat()
                    ))
                    return {'action': 'created', 'slug': slug}
        
        except Exception as e:
            return {'action': 'error', 'slug': str(file_path), 'error': str(e)}
    
    def sync_all_docs(self) -> Dict:
        """Sincroniza todos os documentos da pasta docs/"""
        results = {
            'created': [],
            'updated': [],
            'unchanged': [],
            'errors': [],
            'total_files': 0,
            'start_time': datetime.now()
        }
        
        print(f"🔄 Sincronizando documentos da pasta {self.docs_folder}/")
        
        # Processar todos os arquivos .md
        md_files = list(self.docs_folder.glob("*.md"))
        results['total_files'] = len(md_files)
        
        for file_path in md_files:
            print(f"   📄 {file_path.name}...", end=' ')
            
            result = self.sync_single_file(file_path)
            action = result['action']
            
            if action == 'created':
                results['created'].append(result['slug'])
                print("✅ Criado")
            elif action == 'updated':
                results['updated'].append(result['slug'])
                print("🔄 Atualizado")
            elif action == 'unchanged':
                results['unchanged'].append(result['slug'])
                print("⏸️ Inalterado")
            elif action == 'error':
                results['errors'].append(f"{result['slug']}: {result['error']}")
                print(f"❌ Erro: {result['error']}")
        
        # Marcar documentos órfãos (arquivos deletados)
        self.mark_orphaned_docs()
        
        results['end_time'] = datetime.now()
        results['duration'] = (results['end_time'] - results['start_time']).total_seconds()
        
        return results
    
    def mark_orphaned_docs(self):
        """Marca documentos que não existem mais no sistema de arquivos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT slug, file_path FROM docs WHERE content_status = 'active'")
            
            for slug, file_path in cursor.fetchall():
                if not Path(file_path).exists():
                    conn.execute("""
                        UPDATE docs SET 
                            content_status = 'archived',
                            cluster_name = 'obsoletos',
                            updated_at = ?
                        WHERE slug = ?
                    """, (datetime.now().isoformat(), slug))
                    print(f"   🗑️ Arquivado: {slug} (arquivo não existe mais)")
    
    def cleanup_obsolete_docs(self) -> Dict:
        """Remove documentos obsoletos e reorganiza"""
        results = {
            'archived': 0,
            'moved_to_obsolete': 0,
            'cleaned_clusters': []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            # Mover docs obsoletos para cluster 'obsoletos'
            cursor = conn.execute("""
                UPDATE docs SET 
                    cluster_name = 'obsoletos',
                    content_status = 'archived',
                    updated_at = ?
                WHERE (
                    LOWER(title) LIKE '%obsolet%' OR 
                    LOWER(title) LIKE '%deprecat%' OR
                    LOWER(title) LIKE '%antigo%' OR
                    LOWER(slug) LIKE '%old%' OR
                    LOWER(slug) LIKE '%temp%'
                ) AND content_status != 'archived'
            """, (datetime.now().isoformat(),))
            
            results['moved_to_obsolete'] = cursor.rowcount
            
            # Arquivar documentos muito antigos sem atualizações
            cursor = conn.execute("""
                UPDATE docs SET 
                    content_status = 'archived',
                    cluster_name = 'obsoletos',
                    updated_at = ?
                WHERE updated_at < datetime('now', '-30 days') 
                AND view_count = 0 
                AND content_status = 'active'
            """, (datetime.now().isoformat(),))
            
            results['archived'] = cursor.rowcount
            
            conn.commit()
        
        return results
    
    def get_sync_stats(self) -> Dict:
        """Estatísticas do sistema de documentação"""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            
            # Total por status
            cursor = conn.execute("""
                SELECT content_status, COUNT(*) 
                FROM docs 
                GROUP BY content_status
            """)
            stats['by_status'] = dict(cursor.fetchall())
            
            # Total por cluster
            cursor = conn.execute("""
                SELECT cluster_name, COUNT(*) 
                FROM docs 
                WHERE content_status = 'active'
                GROUP BY cluster_name 
                ORDER BY COUNT(*) DESC
            """)
            stats['by_cluster'] = dict(cursor.fetchall())
            
            # Qualidade média
            cursor = conn.execute("""
                SELECT AVG(quality_score), MIN(quality_score), MAX(quality_score)
                FROM docs 
                WHERE content_status = 'active'
            """)
            avg_qual, min_qual, max_qual = cursor.fetchone()
            stats['quality'] = {
                'average': round(avg_qual or 0, 1),
                'min': min_qual or 0,
                'max': max_qual or 0
            }
            
            # Últimas sincronizações
            cursor = conn.execute("""
                SELECT COUNT(*) 
                FROM docs 
                WHERE last_sync > datetime('now', '-1 hour')
            """)
            stats['synced_last_hour'] = cursor.fetchone()[0]
            
            return stats

def main():
    """Demonstração do sync automático"""
    print("📚 SYNC AUTOMÁTICO DE DOCUMENTAÇÃO")
    print("=" * 50)
    
    # Inicializar sistema
    sync = DocsAutoSync()
    
    # Executar sincronização completa
    results = sync.sync_all_docs()
    
    # Limpar obsoletos
    cleanup_results = sync.cleanup_obsolete_docs()
    
    # Mostrar resultados
    print(f"\n📊 RESULTADOS DA SINCRONIZAÇÃO:")
    print(f"   📁 Arquivos processados: {results['total_files']}")
    print(f"   ✅ Criados: {len(results['created'])}")
    print(f"   🔄 Atualizados: {len(results['updated'])}")
    print(f"   ⏸️ Inalterados: {len(results['unchanged'])}")
    print(f"   ❌ Erros: {len(results['errors'])}")
    print(f"   ⏱️ Duração: {results['duration']:.1f}s")
    
    print(f"\n🧹 LIMPEZA DE OBSOLETOS:")
    print(f"   🗑️ Movidos para obsoletos: {cleanup_results['moved_to_obsolete']}")
    print(f"   📦 Arquivados: {cleanup_results['archived']}")
    
    # Estatísticas finais
    stats = sync.get_sync_stats()
    print(f"\n📈 ESTATÍSTICAS FINAIS:")
    print(f"   📄 Documentos ativos: {stats['by_status'].get('active', 0)}")
    print(f"   📦 Documentos arquivados: {stats['by_status'].get('archived', 0)}")
    print(f"   ⭐ Qualidade média: {stats['quality']['average']}/10")
    print(f"   🔄 Sincronizados (última hora): {stats['synced_last_hour']}")
    
    if stats['by_cluster']:
        print(f"\n📁 CLUSTERS MAIS POPULARES:")
        for cluster, count in list(stats['by_cluster'].items())[:5]:
            print(f"      {cluster}: {count} documentos")
    
    print(f"\n🎉 Sincronização automática concluída com sucesso!")

if __name__ == "__main__":
    main()