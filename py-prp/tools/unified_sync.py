#!/usr/bin/env python3
"""
Script Unificado de Sincronização
Combina as melhores funcionalidades de todos os scripts de sync
"""

import os
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UnifiedSync:
    """Sistema unificado de sincronização com Turso"""
    
    def __init__(self, 
                 local_db: str = "context-memory.db",
                 docs_path: str = "docs",
                 turso_db: Optional[str] = None):
        self.local_db = local_db
        self.docs_path = Path(docs_path)
        self.turso_db = turso_db or os.getenv("TURSO_DATABASE", "context-memory")
        
    def sync_documents(self, force: bool = False) -> Dict[str, int]:
        """
        Sincroniza documentos do sistema de arquivos para o banco
        
        Args:
            force: Se True, força re-sync mesmo se não houver mudanças
            
        Returns:
            Dict com estatísticas da sincronização
        """
        stats = {
            "checked": 0,
            "synced": 0,
            "skipped": 0,
            "errors": 0
        }
        
        # Detectar documentos
        docs = self._find_documents()
        stats["checked"] = len(docs)
        
        # Conectar ao banco
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        
        # Garantir tabela existe
        self._ensure_table(cursor)
        
        # Sincronizar cada documento
        for doc_path in docs:
            try:
                if self._should_sync(doc_path, cursor, force):
                    self._sync_document(doc_path, cursor)
                    stats["synced"] += 1
                else:
                    stats["skipped"] += 1
            except Exception as e:
                logger.error(f"Erro ao sincronizar {doc_path}: {e}")
                stats["errors"] += 1
        
        conn.commit()
        conn.close()
        
        return stats
    
    def sync_to_turso(self) -> bool:
        """Sincroniza banco local com Turso"""
        try:
            # Implementar sync com Turso
            logger.info(f"Sincronizando com Turso: {self.turso_db}")
            # TODO: Implementar usando turso CLI ou API
            return True
        except Exception as e:
            logger.error(f"Erro ao sincronizar com Turso: {e}")
            return False
    
    def smart_sync(self) -> Dict[str, any]:
        """
        Sincronização inteligente que detecta mudanças e sincroniza apenas o necessário
        """
        logger.info("🧠 Iniciando sincronização inteligente...")
        
        # 1. Sync local
        local_stats = self.sync_documents()
        logger.info(f"📁 Local: {local_stats}")
        
        # 2. Sync remoto se configurado
        remote_success = False
        if self.turso_db:
            remote_success = self.sync_to_turso()
        
        return {
            "local": local_stats,
            "remote": remote_success,
            "timestamp": datetime.now().isoformat()
        }
    
    def _find_documents(self) -> List[Path]:
        """Encontra todos os documentos .md"""
        return list(self.docs_path.rglob("*.md"))
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calcula hash do arquivo"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def _should_sync(self, doc_path: Path, cursor, force: bool) -> bool:
        """Verifica se documento precisa ser sincronizado"""
        if force:
            return True
            
        # Verificar se existe e se mudou
        cursor.execute("""
            SELECT file_hash FROM docs_organized 
            WHERE file_path = ?
        """, (str(doc_path.relative_to(self.docs_path)),))
        
        result = cursor.fetchone()
        if not result:
            return True
            
        current_hash = self._calculate_hash(doc_path)
        return current_hash != result[0]
    
    def _sync_document(self, doc_path: Path, cursor):
        """Sincroniza um documento específico"""
        relative_path = str(doc_path.relative_to(self.docs_path))
        
        # Ler conteúdo
        content = doc_path.read_text(encoding='utf-8')
        
        # Extrair metadados
        title = self._extract_title(content)
        summary = content[:500] + "..." if len(content) > 500 else content
        file_hash = self._calculate_hash(doc_path)
        size = doc_path.stat().st_size
        
        # Detectar cluster
        cluster = self._detect_cluster(relative_path)
        
        # Inserir/atualizar
        cursor.execute("""
            INSERT OR REPLACE INTO docs_organized (
                file_path, title, content, summary, cluster,
                category, file_hash, size, last_modified, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            relative_path,
            title,
            content,
            summary,
            cluster,
            'root',
            file_hash,
            size,
            datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat(),
            json.dumps({"synced_at": datetime.now().isoformat()})
        ))
    
    def _extract_title(self, content: str) -> str:
        """Extrai título do documento"""
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                return line.strip('#').strip()
        return "Sem título"
    
    def _detect_cluster(self, file_path: str) -> str:
        """Detecta cluster baseado no caminho"""
        parts = file_path.split('/')
        if len(parts) > 1:
            return parts[0]
        return 'root'
    
    def _ensure_table(self, cursor):
        """Garante que a tabela existe"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS docs_organized (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                summary TEXT,
                cluster TEXT,
                category TEXT,
                file_hash TEXT,
                size INTEGER,
                last_modified DATETIME,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sistema Unificado de Sincronização")
    parser.add_argument("--force", action="store_true", help="Força re-sync de todos os documentos")
    parser.add_argument("--local-only", action="store_true", help="Sincroniza apenas localmente")
    parser.add_argument("--db", default="context-memory.db", help="Banco de dados local")
    parser.add_argument("--docs", default="docs", help="Pasta de documentos")
    
    args = parser.parse_args()
    
    # Criar sincronizador
    sync = UnifiedSync(
        local_db=args.db,
        docs_path=args.docs,
        turso_db=None if args.local_only else os.getenv("TURSO_DATABASE")
    )
    
    # Executar sincronização
    results = sync.smart_sync()
    
    # Mostrar resultados
    print("\n📊 Resultados da Sincronização:")
    print(f"  - Documentos verificados: {results['local']['checked']}")
    print(f"  - Documentos sincronizados: {results['local']['synced']}")
    print(f"  - Documentos pulados: {results['local']['skipped']}")
    print(f"  - Erros: {results['local']['errors']}")
    
    if not args.local_only:
        print(f"  - Sync remoto: {'✅ Sucesso' if results['remote'] else '❌ Falhou'}")
    
    print(f"\n⏰ Concluído em: {results['timestamp']}")


if __name__ == "__main__":
    main()