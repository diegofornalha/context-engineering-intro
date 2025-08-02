#!/usr/bin/env python3
"""
Sistema de Sincronização de Documentos com Turso
Sincroniza documentos organizados em clusters com o banco de dados
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess

class DocSyncTurso:
    def __init__(self, docs_path):
        self.docs_path = Path(docs_path)
        self.metadata = {
            "synced_at": datetime.now().isoformat(),
            "total_docs": 0,
            "clusters_synced": 0,
            "docs_updated": 0,
            "new_docs": 0,
            "errors": []
        }

    def calculate_file_hash(self, filepath):
        """Calcula hash do arquivo para detectar mudanças"""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def extract_doc_metadata(self, filepath):
        """Extrai metadados do documento"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extrair título (primeira linha # )
        lines = content.split('\n')
        title = "Sem título"
        for line in lines:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                break
        
        # Calcular tamanho e resumo
        size = len(content)
        summary = ' '.join(content.split()[:50]) + "..." if len(content.split()) > 50 else content
        
        return {
            "title": title,
            "size": size,
            "summary": summary,
            "content": content
        }

    def get_cluster_info(self, filepath):
        """Determina o cluster e categoria do arquivo"""
        relative_path = filepath.relative_to(self.docs_path)
        parts = relative_path.parts
        
        if len(parts) >= 1:
            cluster = parts[0]
            category = parts[1] if len(parts) > 2 else "root"
            return cluster, category
        
        return "uncategorized", "root"

    def create_turso_queries(self):
        """Cria as queries SQL para o Turso"""
        queries = []
        
        # Verificar se tabelas existem
        check_tables = """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name IN ('docs', 'docs_clusters', 'docs_changes')
        """
        queries.append(("check", check_tables))
        
        # Query para inserir/atualizar documento
        upsert_doc = """
        INSERT INTO docs (
            file_path, title, content, summary, cluster, category, 
            file_hash, size, last_modified, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(file_path) DO UPDATE SET
            title = excluded.title,
            content = excluded.content,
            summary = excluded.summary,
            cluster = excluded.cluster,
            category = excluded.category,
            file_hash = excluded.file_hash,
            size = excluded.size,
            last_modified = excluded.last_modified,
            metadata = excluded.metadata,
            updated_at = CURRENT_TIMESTAMP
        """
        queries.append(("upsert", upsert_doc))
        
        # Query para registrar mudanças
        log_change = """
        INSERT INTO docs_changes (
            doc_id, change_type, old_hash, new_hash, 
            changed_by, change_summary
        ) VALUES (
            (SELECT id FROM docs WHERE file_path = ?),
            ?, ?, ?, 'sync-script', ?
        )
        """
        queries.append(("log_change", log_change))
        
        return queries

    def sync_document(self, filepath):
        """Sincroniza um documento individual"""
        try:
            # Extrair informações
            cluster, category = self.get_cluster_info(filepath)
            metadata = self.extract_doc_metadata(filepath)
            file_hash = self.calculate_file_hash(filepath)
            
            doc_info = {
                "file_path": str(filepath.relative_to(self.docs_path)),
                "title": metadata["title"],
                "content": metadata["content"],
                "summary": metadata["summary"],
                "cluster": cluster,
                "category": category,
                "file_hash": file_hash,
                "size": metadata["size"],
                "last_modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
                "metadata": json.dumps({
                    "synced_at": datetime.now().isoformat(),
                    "sync_version": "1.0"
                })
            }
            
            return doc_info
            
        except Exception as e:
            self.metadata["errors"].append({
                "file": str(filepath),
                "error": str(e)
            })
            return None

    def sync_all_documents(self):
        """Sincroniza todos os documentos"""
        print("🔄 Iniciando sincronização com Turso...\n")
        
        # Coletar todos os arquivos .md
        all_docs = list(self.docs_path.rglob("*.md"))
        self.metadata["total_docs"] = len(all_docs)
        
        print(f"📄 Encontrados {len(all_docs)} documentos para sincronizar")
        
        # Preparar dados para sincronização
        sync_data = []
        clusters = set()
        
        for doc_path in all_docs:
            print(f"  📝 Processando: {doc_path.relative_to(self.docs_path)}")
            
            doc_info = self.sync_document(doc_path)
            if doc_info:
                sync_data.append(doc_info)
                clusters.add(doc_info["cluster"])
        
        self.metadata["clusters_synced"] = len(clusters)
        
        # Salvar dados para script SQL
        self.save_sync_data(sync_data)
        
        print(f"\n✅ Sincronização preparada!")
        print(f"  - Documentos processados: {len(sync_data)}")
        print(f"  - Clusters identificados: {len(clusters)}")
        print(f"  - Erros encontrados: {len(self.metadata['errors'])}")

    def save_sync_data(self, sync_data):
        """Salva dados de sincronização"""
        # Salvar JSON com dados
        sync_file = self.docs_path / ".sync-data.json"
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": self.metadata,
                "documents": sync_data
            }, f, indent=2)
        
        print(f"\n💾 Dados de sincronização salvos em: {sync_file}")
        
        # Criar script SQL
        sql_file = self.docs_path / "sync-to-turso.sql"
        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write("-- Script de sincronização de documentos para Turso\n")
            f.write(f"-- Gerado em: {datetime.now().isoformat()}\n\n")
            
            # Criar tabelas se não existirem
            f.write("""
-- Criar tabela de documentos se não existir
CREATE TABLE IF NOT EXISTS docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    cluster TEXT NOT NULL,
    category TEXT,
    file_hash TEXT NOT NULL,
    size INTEGER,
    last_modified DATETIME,
    metadata TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_docs_cluster ON docs(cluster);
CREATE INDEX IF NOT EXISTS idx_docs_category ON docs(category);
CREATE INDEX IF NOT EXISTS idx_docs_file_hash ON docs(file_hash);

-- Criar tabela de mudanças
CREATE TABLE IF NOT EXISTS docs_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER REFERENCES docs(id),
    change_type TEXT NOT NULL,
    old_hash TEXT,
    new_hash TEXT,
    changed_by TEXT,
    change_summary TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Inserir/Atualizar documentos
""")
            
            # Gerar INSERTs
            for doc in sync_data:
                f.write(f"""
INSERT INTO docs (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '{doc['file_path']}',
    '{doc['title'].replace("'", "''")}',
    '{doc['content'].replace("'", "''")}',
    '{doc['summary'].replace("'", "''")}',
    '{doc['cluster']}',
    '{doc['category']}',
    '{doc['file_hash']}',
    {doc['size']},
    '{doc['last_modified']}',
    '{doc['metadata']}'
)
ON CONFLICT(file_path) DO UPDATE SET
    title = excluded.title,
    content = excluded.content,
    summary = excluded.summary,
    cluster = excluded.cluster,
    category = excluded.category,
    file_hash = excluded.file_hash,
    size = excluded.size,
    last_modified = excluded.last_modified,
    metadata = excluded.metadata,
    updated_at = CURRENT_TIMESTAMP;
""")
        
        print(f"📝 Script SQL gerado em: {sql_file}")

    def create_sync_script(self):
        """Cria script executável para sincronização via MCP"""
        script_content = '''#!/bin/bash
# Script para executar sincronização via MCP Turso

echo "🚀 Executando sincronização de documentos com Turso..."

# Usar o Claude Code para executar via MCP
cat << 'EOF'
Use a ferramenta mcp__turso__execute_query para executar o script SQL em sync-to-turso.sql no banco context-memory.
Leia o arquivo docs/sync-to-turso.sql e execute todas as queries.
EOF
'''
        
        script_path = self.docs_path / "execute-sync.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        print(f"🔧 Script de execução criado: {script_path}")


if __name__ == "__main__":
    # Caminho dos documentos
    docs_path = "/Users/agents/Desktop/context-engineering-intro/docs"
    
    # Executar sincronização
    syncer = DocSyncTurso(docs_path)
    syncer.sync_all_documents()
    syncer.create_sync_script()
    
    print("\n📌 Próximos passos:")
    print("1. Revise o arquivo sync-to-turso.sql")
    print("2. Execute o script SQL no Turso via MCP")
    print("3. Ou use ./execute-sync.sh no Claude Code")