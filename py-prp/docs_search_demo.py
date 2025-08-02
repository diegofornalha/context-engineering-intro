#!/usr/bin/env python3
"""
Demo de Busca na Documentação no Turso
Data: 02/08/2025

Interface simples para demonstrar capacidades de busca na documentação migrada.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional

class DocsSearchEngine:
    """
    Motor de busca para documentação no Turso
    """
    
    def __init__(self, db_path: str = "context-memory.db"):
        self.db_path = db_path
    
    def search_docs(self, query: str, category: str = None, 
                   difficulty: str = None, limit: int = 10) -> List[Dict]:
        """
        Busca documentos por texto
        
        Args:
            query: Texto a buscar
            category: Filtrar por categoria (opcional)
            difficulty: Filtrar por dificuldade (opcional)
            limit: Número máximo de resultados
            
        Returns:
            Lista de documentos encontrados
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Construir query
            sql = """
                SELECT 
                    id, slug, title, summary, category, doc_type,
                    difficulty, estimated_read_time, tags, 
                    created_at, updated_at
                FROM docs 
                WHERE (
                    title LIKE ? OR 
                    summary LIKE ? OR 
                    search_text LIKE ? OR
                    content LIKE ?
                )
            """
            
            params = [f"%{query}%"] * 4
            
            # Adicionar filtros
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            if difficulty:
                sql += " AND difficulty = ?"
                params.append(difficulty)
            
            sql += " ORDER BY "
            sql += "CASE "
            sql += f"WHEN title LIKE '%{query}%' THEN 1 "
            sql += f"WHEN summary LIKE '%{query}%' THEN 2 "
            sql += "ELSE 3 END, "
            sql += "estimated_read_time ASC "
            sql += f"LIMIT {limit}"
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            # Converter para dicionários
            docs = []
            for row in results:
                doc = dict(row)
                # Parse tags JSON
                try:
                    doc['tags'] = json.loads(doc['tags']) if doc['tags'] else []
                except:
                    doc['tags'] = []
                docs.append(doc)
            
            return docs
    
    def search_by_tag(self, tag: str, limit: int = 10) -> List[Dict]:
        """Busca documentos por tag"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT
                    d.id, d.slug, d.title, d.summary, d.category, 
                    d.doc_type, d.difficulty, d.estimated_read_time, d.tags
                FROM docs d
                JOIN docs_tag_relations dtr ON d.id = dtr.doc_id
                JOIN docs_tags dt ON dtr.tag_id = dt.id
                WHERE dt.name = ?
                ORDER BY d.estimated_read_time ASC
                LIMIT ?
            """, (tag, limit))
            
            results = cursor.fetchall()
            docs = []
            for row in results:
                doc = dict(row)
                try:
                    doc['tags'] = json.loads(doc['tags']) if doc['tags'] else []
                except:
                    doc['tags'] = []
                docs.append(doc)
            
            return docs
    
    def get_categories(self) -> List[Dict]:
        """Lista todas as categorias com contagens"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    category,
                    COUNT(*) as doc_count,
                    AVG(estimated_read_time) as avg_read_time,
                    COUNT(DISTINCT CASE WHEN difficulty = 'easy' THEN id END) as easy_docs,
                    COUNT(DISTINCT CASE WHEN difficulty = 'medium' THEN id END) as medium_docs,
                    COUNT(DISTINCT CASE WHEN difficulty = 'hard' THEN id END) as hard_docs
                FROM docs
                GROUP BY category
                ORDER BY doc_count DESC
            """)
            
            return [dict(zip([col[0] for col in cursor.description], row)) 
                    for row in cursor.fetchall()]
    
    def get_popular_tags(self, limit: int = 20) -> List[Dict]:
        """Lista tags mais populares"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    dt.name,
                    dt.description,
                    dt.color,
                    COUNT(dtr.doc_id) as usage_count
                FROM docs_tags dt
                LEFT JOIN docs_tag_relations dtr ON dt.id = dtr.tag_id
                GROUP BY dt.id
                ORDER BY usage_count DESC, dt.name ASC
                LIMIT ?
            """, (limit,))
            
            return [dict(zip([col[0] for col in cursor.description], row)) 
                    for row in cursor.fetchall()]
    
    def get_recent_docs(self, limit: int = 10) -> List[Dict]:
        """Lista documentos mais recentes"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    id, slug, title, summary, category, doc_type,
                    difficulty, estimated_read_time, tags, created_at
                FROM docs
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            docs = []
            for row in cursor.fetchall():
                doc = dict(row)
                try:
                    doc['tags'] = json.loads(doc['tags']) if doc['tags'] else []
                except:
                    doc['tags'] = []
                docs.append(doc)
            
            return docs
    
    def get_stats(self) -> Dict:
        """Estatísticas gerais da documentação"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Estatísticas básicas
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_docs,
                    COUNT(DISTINCT category) as total_categories,
                    SUM(estimated_read_time) as total_read_time,
                    AVG(estimated_read_time) as avg_read_time,
                    COUNT(CASE WHEN difficulty = 'easy' THEN 1 END) as easy_docs,
                    COUNT(CASE WHEN difficulty = 'medium' THEN 1 END) as medium_docs,
                    COUNT(CASE WHEN difficulty = 'hard' THEN 1 END) as hard_docs
                FROM docs
            """)
            
            stats = dict(zip([col[0] for col in cursor.description], cursor.fetchone()))
            
            # Contagem de seções e tags
            cursor.execute("SELECT COUNT(*) FROM docs_sections")
            stats['total_sections'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM docs_tags")
            stats['total_tags'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM docs_links")
            stats['total_links'] = cursor.fetchone()[0]
            
            return stats

def print_doc_summary(doc: Dict):
    """Imprime resumo de um documento"""
    print(f"📄 **{doc['title']}**")
    print(f"   📁 {doc['category'].upper()} | 🎯 {doc['difficulty']} | ⏱️  {doc['estimated_read_time']}min")
    if doc['tags']:
        tags_str = ' '.join([f"#{tag}" for tag in doc['tags'][:5]])
        print(f"   🏷️  {tags_str}")
    if doc['summary']:
        summary = doc['summary'][:100] + "..." if len(doc['summary']) > 100 else doc['summary']
        print(f"   📝 {summary}")
    print()

def demo_search_interface():
    """Interface de demonstração da busca"""
    print("🔍 Demo de Busca na Documentação Turso")
    print("=" * 50)
    
    search_engine = DocsSearchEngine()
    
    # Estatísticas gerais
    print("📊 ESTATÍSTICAS GERAIS:")
    stats = search_engine.get_stats()
    print(f"  📚 Total de documentos: {stats['total_docs']}")
    print(f"  📁 Categorias: {stats['total_categories']}")
    print(f"  ⏱️  Tempo total de leitura: {stats['total_read_time']} minutos")
    print(f"  📊 Tempo médio: {stats['avg_read_time']:.1f} minutos")
    print(f"  🎯 Dificuldade: {stats['easy_docs']} fáceis, {stats['medium_docs']} médios, {stats['hard_docs']} difíceis")
    print(f"  📋 Seções: {stats['total_sections']}")
    print(f"  🏷️  Tags: {stats['total_tags']}")
    print(f"  🔗 Links: {stats['total_links']}")
    print()
    
    # Categorias
    print("📁 DOCUMENTOS POR CATEGORIA:")
    categories = search_engine.get_categories()
    for cat in categories:
        print(f"  📁 {cat['category'].upper()}: {cat['doc_count']} docs (⏱️  {cat['avg_read_time']:.1f}min médio)")
    print()
    
    # Tags populares
    print("🏷️  TAGS MAIS POPULARES:")
    tags = search_engine.get_popular_tags(10)
    for tag in tags:
        print(f"  #{tag['name']}: {tag['usage_count']} usos")
    print()
    
    # Exemplos de busca
    searches = [
        ("turso", "Buscar por 'turso'"),
        ("mcp", "Buscar por 'mcp'"),
        ("configuração", "Buscar por 'configuração'"),
        ("integration", "Buscar por 'integration'")
    ]
    
    for query, description in searches:
        print(f"🔍 {description}:")
        results = search_engine.search_docs(query, limit=3)
        if results:
            for doc in results:
                print_doc_summary(doc)
        else:
            print("  Nenhum resultado encontrado.\n")
    
    # Busca por tag
    print("🏷️  BUSCA POR TAG 'mcp':")
    tag_results = search_engine.search_by_tag('mcp', limit=3)
    for doc in tag_results:
        print_doc_summary(doc)
    
    # Documentos recentes
    print("📅 DOCUMENTOS MAIS RECENTES:")
    recent = search_engine.get_recent_docs(5)
    for doc in recent:
        print_doc_summary(doc)
    
    print("🎉 Demo concluída!")
    print()
    print("💡 CAPACIDADES DEMONSTRADAS:")
    print("  ✅ Busca full-text em títulos, resumos e conteúdo")
    print("  ✅ Filtros por categoria e dificuldade")
    print("  ✅ Busca por tags estruturadas")
    print("  ✅ Estatísticas e analytics")
    print("  ✅ Documentos recentes e populares")
    print("  ✅ Metadados automáticos (tempo de leitura, dificuldade)")
    print()
    print("🚀 PRÓXIMOS PASSOS:")
    print("  1. 🌐 Criar interface web interativa")
    print("  2. 🤖 Integrar com agentes LLM para consultas inteligentes")
    print("  3. 📊 Implementar analytics de acesso em tempo real")
    print("  4. 🔄 Sincronização automática com arquivos .md")
    print("  5. ⚡ API REST para integração externa")

def interactive_search():
    """Interface interativa de busca"""
    search_engine = DocsSearchEngine()
    
    print("🔍 Busca Interativa na Documentação")
    print("Digite 'quit' para sair")
    print()
    
    while True:
        query = input("🔍 Buscar: ").strip()
        
        if query.lower() in ['quit', 'exit', 'sair']:
            break
        
        if not query:
            continue
        
        results = search_engine.search_docs(query, limit=5)
        
        if results:
            print(f"\n📚 Encontrados {len(results)} resultados:")
            print("-" * 40)
            for i, doc in enumerate(results, 1):
                print(f"{i}. {doc['title']}")
                print(f"   📁 {doc['category']} | 🎯 {doc['difficulty']} | ⏱️  {doc['estimated_read_time']}min")
                if doc['summary']:
                    summary = doc['summary'][:80] + "..." if len(doc['summary']) > 80 else doc['summary']
                    print(f"   📝 {summary}")
                print()
        else:
            print("❌ Nenhum resultado encontrado.\n")

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_search()
    else:
        demo_search_interface()

if __name__ == "__main__":
    main()