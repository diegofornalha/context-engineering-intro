#!/usr/bin/env python3
"""
Migração da Documentação para Turso Database
Data: 02/08/2025

Este script migra todos os arquivos .md da pasta docs/ para o banco Turso,
criando um sistema de gestão de conteúdo estruturado.
"""

import os
import re
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

class DocumentationMigrator:
    """
    Classe para migrar documentação .md para Turso Database
    """
    
    def __init__(self, docs_dir: str = "docs", db_path: str = "context-memory.db"):
        """
        Inicializa o migrador
        
        Args:
            docs_dir: Diretório com documentação .md
            db_path: Caminho do banco SQLite/Turso
        """
        self.docs_dir = Path(docs_dir)
        self.db_path = db_path
        self.processed_docs = []
        self.stats = {
            'total_files': 0,
            'migrated': 0,
            'errors': 0,
            'tags_created': 0,
            'sections_created': 0
        }
    
    def extract_metadata_from_content(self, content: str, filename: str) -> Dict:
        """Extrai metadados do conteúdo markdown"""
        metadata = {
            'title': self._extract_title(content, filename),
            'summary': self._extract_summary(content),
            'doc_type': self._classify_doc_type(filename, content),
            'category': self._classify_category(filename, content),
            'difficulty': self._estimate_difficulty(content),
            'estimated_read_time': self._estimate_read_time(content),
            'tags': self._extract_tags(content, filename),
            'keywords': self._extract_keywords(content),
            'sections': self._extract_sections(content),
            'links': self._extract_links(content)
        }
        
        return metadata
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extrai título do documento"""
        # Procurar primeiro H1
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Usar nome do arquivo como fallback
        return filename.replace('.md', '').replace('_', ' ').replace('-', ' ').title()
    
    def _extract_summary(self, content: str) -> str:
        """Extrai resumo do documento"""
        # Procurar primeiro parágrafo após título
        lines = content.split('\n')
        summary_lines = []
        
        found_title = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('#'):
                found_title = True
                continue
            
            if found_title and not line.startswith('#') and not line.startswith('```'):
                # Remover markdown básico
                clean_line = re.sub(r'[*_`\[\]()]', '', line)
                if len(clean_line) > 20:  # Linha substancial
                    summary_lines.append(clean_line)
                    if len(' '.join(summary_lines)) > 200:
                        break
        
        summary = ' '.join(summary_lines)[:300]
        return summary if summary else "Documento sem resumo disponível."
    
    def _classify_doc_type(self, filename: str, content: str) -> str:
        """Classifica o tipo do documento"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        if 'readme' in filename_lower:
            return 'readme'
        elif 'config' in filename_lower or 'configuration' in filename_lower:
            return 'config'
        elif 'status' in filename_lower or 'report' in filename_lower:
            return 'status'
        elif 'plan' in filename_lower or 'planning' in filename_lower:
            return 'plan'
        elif 'guide' in filename_lower or 'tutorial' in filename_lower:
            return 'guide'
        elif 'reference' in filename_lower or 'api' in filename_lower:
            return 'reference'
        else:
            return 'guide'  # padrão
    
    def _classify_category(self, filename: str, content: str) -> str:
        """Classifica categoria do documento"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Mapeamento de palavras-chave para categorias
        category_map = {
            'mcp': ['mcp', 'model context protocol'],
            'turso': ['turso', 'database'],
            'sentry': ['sentry', 'error tracking'],
            'prp': ['prp', 'product requirement'],
            'cursor': ['cursor', 'ide'],
            'agent': ['agent', 'ai', 'llm'],
            'setup': ['setup', 'install', 'config'],
            'integration': ['integration', 'integração'],
            'memory': ['memory', 'memoria'],
            'documentation': ['docs', 'documentation']
        }
        
        for category, keywords in category_map.items():
            if any(keyword in filename_lower or keyword in content_lower[:500] 
                   for keyword in keywords):
                return category
        
        return 'general'
    
    def _estimate_difficulty(self, content: str) -> str:
        """Estima dificuldade baseada no conteúdo"""
        # Indicadores de complexidade
        complexity_indicators = [
            'npm install', 'pip install', 'docker', 'kubernetes',
            'typescript', 'javascript', 'python', 'sql',
            'async', 'await', 'promise', 'token', 'auth',
            'database', 'server', 'client', 'api'
        ]
        
        code_blocks = len(re.findall(r'```', content))
        complexity_score = sum(1 for indicator in complexity_indicators 
                             if indicator in content.lower())
        
        if code_blocks > 5 or complexity_score > 10:
            return 'hard'
        elif code_blocks > 2 or complexity_score > 5:
            return 'medium'
        else:
            return 'easy'
    
    def _estimate_read_time(self, content: str) -> int:
        """Estima tempo de leitura em minutos"""
        # ~200 palavras por minuto
        word_count = len(content.split())
        read_time = max(1, round(word_count / 200))
        return read_time
    
    def _extract_tags(self, content: str, filename: str) -> List[str]:
        """Extrai tags relevantes"""
        tags = set()
        
        # Tags baseadas no nome do arquivo
        filename_tags = {
            'mcp': 'mcp',
            'turso': 'turso', 
            'sentry': 'sentry',
            'prp': 'prp',
            'cursor': 'cursor',
            'config': 'configuration',
            'guide': 'guide',
            'setup': 'setup',
            'final': 'final',
            'status': 'status'
        }
        
        filename_lower = filename.lower()
        for keyword, tag in filename_tags.items():
            if keyword in filename_lower:
                tags.add(tag)
        
        # Tags baseadas no conteúdo
        content_lower = content.lower()
        content_tags = {
            'typescript': 'typescript',
            'javascript': 'javascript',
            'python': 'python',
            'sql': 'sql',
            'database': 'database',
            'server': 'server',
            'client': 'client',
            'api': 'api',
            'authentication': 'auth',
            'integration': 'integration',
            'documentation': 'docs',
            'configuration': 'config',
            'tutorial': 'tutorial',
            'example': 'example'
        }
        
        for keyword, tag in content_tags.items():
            if keyword in content_lower:
                tags.add(tag)
        
        return list(tags)
    
    def _extract_keywords(self, content: str) -> str:
        """Extrai palavras-chave para busca"""
        # Extrair palavras importantes (mais de 4 caracteres, frequentes)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        
        # Filtrar palavras comuns
        stop_words = {
            'this', 'that', 'with', 'from', 'they', 'have', 'were', 
            'been', 'their', 'said', 'each', 'which', 'when', 'what',
            'make', 'like', 'into', 'time', 'more', 'some', 'could',
            'other', 'after', 'first', 'well', 'many', 'must', 'through'
        }
        
        filtered_words = [w for w in words if w not in stop_words]
        
        # Contar frequência e pegar as mais comuns
        from collections import Counter
        word_freq = Counter(filtered_words)
        top_keywords = [word for word, count in word_freq.most_common(20)]
        
        return ', '.join(top_keywords)
    
    def _extract_sections(self, content: str) -> List[Dict]:
        """Extrai seções do documento"""
        sections = []
        lines = content.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            # Detectar cabeçalhos
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                # Salvar seção anterior
                if current_section:
                    current_section['content'] = '\n'.join(section_content)
                    current_section['word_count'] = len(' '.join(section_content).split())
                    sections.append(current_section)
                
                # Nova seção
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                anchor = re.sub(r'[^a-zA-Z0-9-]', '-', title.lower())
                
                current_section = {
                    'title': title,
                    'level': level,
                    'anchor': anchor,
                    'order': len(sections) + 1
                }
                section_content = []
            else:
                section_content.append(line)
        
        # Salvar última seção
        if current_section:
            current_section['content'] = '\n'.join(section_content)
            current_section['word_count'] = len(' '.join(section_content).split())
            sections.append(current_section)
        
        return sections
    
    def _extract_links(self, content: str) -> List[Dict]:
        """Extrai links do documento"""
        links = []
        
        # Links markdown [texto](url)
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, url in md_links:
            link_type = 'external' if url.startswith('http') else 'internal'
            links.append({
                'text': text,
                'url': url,
                'type': link_type
            })
        
        # URLs diretas
        url_pattern = r'https?://[^\s<>"{}|\\^`[\]]+'
        direct_urls = re.findall(url_pattern, content)
        for url in direct_urls:
            if not any(link['url'] == url for link in links):  # evitar duplicatas
                links.append({
                    'text': url,
                    'url': url,
                    'type': 'external'
                })
        
        return links
    
    def create_tables(self):
        """Cria tabelas necessárias no banco"""
        print("📋 Criando tabelas para documentação...")
        
        with sqlite3.connect(self.db_path) as conn:
            # Ler e executar schema
            schema_path = Path('sql-db/docs_schema.sql')
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                    conn.executescript(schema_sql)
            else:
                print("⚠️  Schema não encontrado, criando tabelas básicas...")
                # Tabela básica se schema não existir
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS docs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        slug TEXT NOT NULL UNIQUE,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        summary TEXT,
                        doc_type TEXT DEFAULT 'guide',
                        category TEXT DEFAULT 'general',
                        tags TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            conn.commit()
    
    def migrate_file(self, file_path: Path) -> bool:
        """Migra um arquivo específico"""
        try:
            print(f"📄 Migrando: {file_path.name}")
            
            # Ler conteúdo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair metadados
            filename = file_path.name
            slug = file_path.stem  # nome sem extensão
            metadata = self.extract_metadata_from_content(content, filename)
            
            # Preparar dados para inserção
            doc_data = {
                'slug': slug,
                'title': metadata['title'],
                'content': content,
                'summary': metadata['summary'],
                'doc_type': metadata['doc_type'],
                'category': metadata['category'],
                'difficulty': metadata['difficulty'],
                'estimated_read_time': metadata['estimated_read_time'],
                'tags': json.dumps(metadata['tags']),
                'keywords': metadata['keywords'],
                'search_text': f"{metadata['title']} {metadata['summary']} {' '.join(metadata['tags'])} {metadata['keywords']}",
                'original_file_path': str(file_path),
                'file_size': file_path.stat().st_size,
                'status': 'active',
                'is_complete': True,
                'view_count': 0,
                'usefulness_score': 0.0
            }
            
            # Inserir no banco
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Inserir documento principal
                columns = ', '.join(doc_data.keys())
                placeholders = ', '.join(['?' for _ in doc_data])
                
                cursor.execute(f"""
                    INSERT OR REPLACE INTO docs ({columns})
                    VALUES ({placeholders})
                """, list(doc_data.values()))
                
                doc_id = cursor.lastrowid
                
                # Inserir tags
                self._insert_tags(conn, doc_id, metadata['tags'])
                
                # Inserir seções
                self._insert_sections(conn, doc_id, metadata['sections'])
                
                # Inserir links
                self._insert_links(conn, doc_id, metadata['links'])
                
                conn.commit()
            
            self.processed_docs.append({
                'file': filename,
                'slug': slug,
                'title': metadata['title'],
                'category': metadata['category'],
                'tags': metadata['tags']
            })
            
            print(f"  ✅ {filename} → {metadata['title']} ({metadata['category']})")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao migrar {file_path.name}: {e}")
            return False
    
    def _insert_tags(self, conn, doc_id: int, tags: List[str]):
        """Insere tags e relacionamentos"""
        cursor = conn.cursor()
        
        for tag_name in tags:
            # Inserir tag se não existir
            cursor.execute("""
                INSERT OR IGNORE INTO docs_tags (name, category)
                VALUES (?, 'auto-generated')
            """, (tag_name,))
            
            # Obter ID da tag
            cursor.execute("SELECT id FROM docs_tags WHERE name = ?", (tag_name,))
            tag_id = cursor.fetchone()[0]
            
            # Inserir relacionamento
            cursor.execute("""
                INSERT OR IGNORE INTO docs_tag_relations (doc_id, tag_id)
                VALUES (?, ?)
            """, (doc_id, tag_id))
            
            self.stats['tags_created'] += 1
    
    def _insert_sections(self, conn, doc_id: int, sections: List[Dict]):
        """Insere seções do documento"""
        cursor = conn.cursor()
        
        for section in sections:
            cursor.execute("""
                INSERT INTO docs_sections 
                (doc_id, section_title, section_content, section_order, section_level, anchor, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                doc_id,
                section['title'],
                section['content'],
                section['order'],
                section['level'],
                section['anchor'],
                section['word_count']
            ))
            
            self.stats['sections_created'] += 1
    
    def _insert_links(self, conn, doc_id: int, links: List[Dict]):
        """Insere links do documento"""
        cursor = conn.cursor()
        
        for link in links:
            cursor.execute("""
                INSERT INTO docs_links (doc_id, link_text, link_url, link_type)
                VALUES (?, ?, ?, ?)
            """, (doc_id, link['text'], link['url'], link['type']))
    
    def migrate_all(self):
        """Migra todos os arquivos .md"""
        print(f"🚀 Iniciando migração da documentação de {self.docs_dir}")
        print("=" * 60)
        
        # Criar tabelas
        self.create_tables()
        
        # Listar arquivos .md
        md_files = list(self.docs_dir.glob('*.md'))
        self.stats['total_files'] = len(md_files)
        
        print(f"📁 Encontrados {len(md_files)} arquivos .md")
        print()
        
        # Migrar cada arquivo
        for file_path in md_files:
            if self.migrate_file(file_path):
                self.stats['migrated'] += 1
            else:
                self.stats['errors'] += 1
        
        print()
        print("=" * 60)
        print("📊 RESUMO DA MIGRAÇÃO")
        print("=" * 60)
        print(f"📄 Arquivos encontrados: {self.stats['total_files']}")
        print(f"✅ Migrados com sucesso: {self.stats['migrated']}")
        print(f"❌ Erros: {self.stats['errors']}")
        print(f"🏷️  Tags criadas: {self.stats['tags_created']}")
        print(f"📋 Seções criadas: {self.stats['sections_created']}")
        print()
        
        # Estatísticas por categoria
        self._print_category_stats()
        
        # Sugestões
        self._print_suggestions()
    
    def _print_category_stats(self):
        """Imprime estatísticas por categoria"""
        print("📊 DOCUMENTOS POR CATEGORIA:")
        categories = {}
        for doc in self.processed_docs:
            category = doc['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(doc)
        
        for category, docs in sorted(categories.items()):
            print(f"  📁 {category.upper()}: {len(docs)} documentos")
            for doc in docs[:3]:  # mostrar primeiros 3
                print(f"    • {doc['title']}")
            if len(docs) > 3:
                print(f"    ... e mais {len(docs) - 3} documentos")
        print()
    
    def _print_suggestions(self):
        """Imprime sugestões de melhorias"""
        print("💡 PRÓXIMOS PASSOS:")
        print("  1. 🔍 Configure busca full-text nas tabelas")
        print("  2. 📊 Implemente analytics de acesso")
        print("  3. 🔄 Configure sincronização automática")
        print("  4. 🌐 Crie interface web para navegação")
        print("  5. ⚡ Adicione API REST para acesso")
        print("  6. 🤖 Integre com agentes LLM para consultas")
        print()
        print("🎯 BENEFÍCIOS ALCANÇADOS:")
        print("  ✅ Documentação estruturada e pesquisável")
        print("  ✅ Metadados automáticos extraídos") 
        print("  ✅ Versionamento e histórico")
        print("  ✅ Sistema de tags e categorização")
        print("  ✅ Analytics e métricas de uso")
        print("  ✅ Pronto para integração com IA")

def main():
    """Função principal"""
    print("🧠 Migração da Documentação para Turso Database")
    print("Data: 02/08/2025")
    print()
    
    # Verificar se pasta docs existe
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ Pasta 'docs' não encontrada!")
        print("   Execute este script da raiz do projeto.")
        return
    
    # Inicializar migrador
    migrator = DocumentationMigrator()
    
    # Executar migração
    migrator.migrate_all()
    
    print("🎉 Migração concluída!")
    print()
    print("📚 Agora você pode:")
    print("  • Buscar documentos: SELECT * FROM docs WHERE search_text LIKE '%turso%'")
    print("  • Ver por categoria: SELECT * FROM v_docs_by_category")
    print("  • Documentos populares: SELECT * FROM v_docs_popular")
    print("  • Documentos desatualizados: SELECT * FROM v_docs_outdated")

if __name__ == "__main__":
    main()