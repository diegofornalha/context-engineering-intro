#!/usr/bin/env python3
"""
Sync da documentação consolidada para Turso via MCP
Data: 02/08/2025

Este script sincroniza os documentos consolidados da pasta docs/ 
para o banco Turso usando a estrutura de tabela correta.
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path

def get_file_hash(content: str) -> str:
    """Gera hash do conteúdo do arquivo"""
    return hashlib.sha256(content.encode()).hexdigest()

def extract_title_from_content(content: str, filename: str) -> str:
    """Extrai título do conteúdo markdown"""
    lines = content.split('\n')
    for line in lines[:10]:  # Procura nos primeiros 10 linhas
        if line.startswith('# '):
            return line[2:].strip()
    
    # Fallback para nome do arquivo
    return filename.replace('.md', '').replace('_', ' ').replace('-', ' ').title()

def classify_cluster(filepath: str) -> str:
    """Classifica documento em cluster baseado no caminho"""
    parts = filepath.split('/')
    
    if 'sentry' in filepath.lower():
        return 'SENTRY_MONITORING'
    elif 'mcp' in filepath.lower():
        return 'MCP_INTEGRATION'
    elif 'turso' in filepath.lower():
        return 'TURSO_DATABASE'
    elif 'prp' in filepath.lower():
        return 'PRP_SYSTEM'
    elif 'getting-started' in filepath:
        return 'GETTING_STARTED'
    elif 'system-status' in filepath:
        return 'SYSTEM_STATUS'
    elif 'project-organization' in filepath:
        return 'PROJECT_ORGANIZATION'
    else:
        return 'DOCUMENTATION'

def classify_category(filepath: str, content: str) -> str:
    """Classifica categoria do documento"""
    if 'guide' in filepath.lower() or 'guia' in filepath.lower():
        return 'guide'
    elif 'status' in filepath.lower() or 'report' in filepath.lower():
        return 'status'
    elif 'setup' in filepath.lower() or 'config' in filepath.lower():
        return 'setup'
    elif 'success' in filepath.lower() or 'sucesso' in filepath.lower():
        return 'success'
    elif 'analysis' in filepath.lower() or 'analise' in filepath.lower():
        return 'analysis'
    else:
        return 'documentation'

def estimate_read_time(content: str) -> int:
    """Estima tempo de leitura em minutos (200 palavras/min)"""
    words = len(content.split())
    return max(1, words // 200)

def extract_summary(content: str) -> str:
    """Extrai resumo do documento"""
    lines = content.split('\n')
    summary_lines = []
    
    # Procura por linhas após o título que não sejam vazias ou markdown
    in_summary = False
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            in_summary = True
            continue
        elif in_summary and line and not line.startswith('#') and not line.startswith('!['):
            if line.startswith('>'):
                line = line[1:].strip()
            summary_lines.append(line)
            if len(' '.join(summary_lines)) > 200:
                break
        elif in_summary and line.startswith('##'):
            break
    
    summary = ' '.join(summary_lines)[:300]
    return summary if summary else "Documentação do projeto"

def sync_docs_to_turso():
    """Sincroniza documentos consolidados para Turso"""
    
    print("🔄 Sincronizando documentação consolidada para Turso...")
    print("=" * 60)
    
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ Pasta 'docs' não encontrada!")
        return
    
    # Encontrar todos os arquivos .md
    md_files = list(docs_dir.rglob("*.md"))
    print(f"📁 Encontrados {len(md_files)} arquivos .md")
    
    synced = 0
    errors = 0
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair metadados
            relative_path = str(md_file.relative_to(Path(".")))
            title = extract_title_from_content(content, md_file.name)
            summary = extract_summary(content)
            cluster = classify_cluster(relative_path)
            category = classify_category(relative_path, content)
            read_time = estimate_read_time(content)
            file_hash = get_file_hash(content)
            
            print(f"📄 Sync: {md_file.name}")
            print(f"   Cluster: {cluster}")
            print(f"   Categoria: {category}")
            print(f"   Tamanho: {len(content)} chars")
            
            # Simular inserção no Turso (estrutura correta)
            insert_query = """
            INSERT INTO docs (
                slug, title, content, summary, cluster_name, category, 
                difficulty, estimated_read_time, content_status, 
                quality_score, relevance_score, tags, keywords
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ON CONFLICT(slug) DO UPDATE SET
                title = excluded.title,
                content = excluded.content,
                summary = excluded.summary,
                cluster_name = excluded.cluster_name,
                category = excluded.category,
                estimated_read_time = excluded.estimated_read_time,
                updated_at = CURRENT_TIMESTAMP
            """
            
            # Dados para inserção
            slug = relative_path.replace('.md', '').replace('/', '-').lower()
            keywords = f"{cluster.lower()}, {category}, documentation"
            tags = f"#{cluster.lower()}, #{category}"
            
            insert_data = (
                slug,
                title,
                content,
                summary,
                cluster,
                category,
                'medium',
                read_time,
                'active',
                8.5,  # quality_score
                9.0,  # relevance_score  
                tags,
                keywords
            )
            
            print(f"   ✅ Preparado para Turso")
            synced += 1
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            errors += 1
    
    print("=" * 60)
    print("📊 RESUMO DO SYNC")
    print("=" * 60)
    print(f"📄 Arquivos encontrados: {len(md_files)}")
    print(f"✅ Preparados para sync: {synced}")
    print(f"❌ Erros: {errors}")
    
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Execute o sync real via MCP Turso")
    print("   2. Verifique os dados no banco context-memory")
    print("   3. Teste busca e navegação")
    
    print("\n🎯 Para executar o sync real:")
    print("   Use as ferramentas MCP do Cursor Agent para inserir os dados")

if __name__ == "__main__":
    sync_docs_to_turso()