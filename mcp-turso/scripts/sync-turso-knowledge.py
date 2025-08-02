#!/usr/bin/env python3
"""
Sistema de Sincronização de Conhecimento Turso Agent

Script para manter o conhecimento do Turso Agent atualizado,
detectar dados obsoletos e sincronizar com fontes externas.
"""

import os
import glob
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

class TursoKnowledgeSync:
    """
    Sistema de sincronização de conhecimento do Turso Agent
    """
    
    def __init__(self, db_path: str = "context-memory.db"):
        """
        Inicializa o sistema de sync
        
        Args:
            db_path: Caminho para o banco de dados
        """
        self.db_path = db_path
        self.sync_log = []
        
        # Verificar se o banco existe
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Banco de dados não encontrado: {self.db_path}")
        
    def connect_db(self):
        """Conecta ao banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def get_file_hash(self, file_path: str) -> str:
        """Calcula hash MD5 de um arquivo"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_knowledge_hash(self, content: str) -> str:
        """Calcula hash do conteúdo de conhecimento"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def detect_obsolete_knowledge(self, days_threshold: int = 30) -> List[Dict]:
        """
        Detecta conhecimento obsoleto baseado em:
        - Tempo desde última atualização
        - Mudanças em arquivos fonte
        - Inconsistências de dados
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Buscar conhecimento antigo
        threshold_date = datetime.now() - timedelta(days=days_threshold)
        
        cursor.execute("""
            SELECT id, topic, content, updated_at, source, tags
            FROM turso_agent_knowledge 
            WHERE updated_at < ?
            ORDER BY updated_at ASC
        """, (threshold_date.strftime('%Y-%m-%d %H:%M:%S'),))
        
        obsolete_records = []
        for row in cursor.fetchall():
            record = {
                'id': row[0],
                'topic': row[1],
                'content': row[2],
                'updated_at': row[3],
                'source': row[4],
                'tags': row[5],
                'reason': 'old_data'
            }
            obsolete_records.append(record)
        
        conn.close()
        return obsolete_records
    
    def scan_docs_turso_files(self) -> List[Dict]:
        """
        Escaneia arquivos da pasta docs-turso para detectar mudanças
        """
        docs_files = []
        
        # Padrões de arquivos para escanear
        patterns = [
            "docs-turso/**/*.md",
            "docs-turso/**/*.txt",
            "docs-turso/**/*.json"
        ]
        
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                if os.path.isfile(file_path):
                    file_hash = self.get_file_hash(file_path)
                    file_info = {
                        'path': file_path,
                        'hash': file_hash,
                        'size': os.path.getsize(file_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path)),
                        'content': self.read_file_content(file_path)
                    }
                    docs_files.append(file_info)
        
        return docs_files
    
    def read_file_content(self, file_path: str) -> str:
        """Lê conteúdo de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {e}"
    
    def extract_knowledge_from_file(self, file_info: Dict) -> List[Dict]:
        """
        Extrai conhecimento estruturado de um arquivo
        """
        content = file_info['content']
        file_path = file_info['path']
        
        # Determinar categoria baseada no caminho
        if 'configuration' in file_path:
            category = 'Configuration'
        elif 'documentation' in file_path:
            category = 'Documentation'
        elif 'migration' in file_path:
            category = 'Migration'
        else:
            category = 'General'
        
        # Extrair tópico do nome do arquivo
        filename = os.path.basename(file_path)
        topic = filename.replace('.md', '').replace('.txt', '').replace('_', ' ').title()
        
        # Gerar tags baseadas no conteúdo
        tags = self.extract_tags_from_content(content)
        
        # Calcular expertise baseada no tamanho e complexidade
        expertise = self.calculate_expertise_level(content)
        
        knowledge = {
            'topic': topic,
            'content': content[:1000] + "..." if len(content) > 1000 else content,
            'category': category,
            'expertise_level': expertise,
            'tags': ','.join(tags),
            'source': file_path,
            'file_hash': file_info['hash'],
            'priority': self.calculate_priority(content, category)
        }
        
        return [knowledge]
    
    def extract_tags_from_content(self, content: str) -> List[str]:
        """Extrai tags relevantes do conteúdo"""
        tags = []
        content_lower = content.lower()
        
        # Tags baseadas em palavras-chave
        keyword_tags = {
            'turso': ['turso', 'database', 'libsql'],
            'mcp': ['mcp', 'model context protocol'],
            'configuration': ['config', 'setup', 'install'],
            'migration': ['migrate', 'migration', 'transfer'],
            'documentation': ['docs', 'documentation', 'guide'],
            'integration': ['integration', 'connect', 'api'],
            'security': ['security', 'auth', 'token'],
            'performance': ['performance', 'optimization', 'speed']
        }
        
        for tag_group, keywords in keyword_tags.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag_group)
        
        return list(set(tags))
    
    def calculate_expertise_level(self, content: str) -> str:
        """Calcula nível de expertise baseado no conteúdo"""
        # Critérios para determinar expertise
        if len(content) > 5000:
            return 'expert'
        elif len(content) > 2000:
            return 'intermediate'
        else:
            return 'beginner'
    
    def calculate_priority(self, content: str, category: str) -> int:
        """Calcula prioridade do conhecimento"""
        priority = 1
        
        # Aumentar prioridade baseado em critérios
        if 'error' in content.lower() or 'troubleshoot' in content.lower():
            priority += 2
        if category == 'Configuration':
            priority += 1
        if len(content) > 3000:
            priority += 1
        
        return min(priority, 5)  # Máximo 5
    
    def sync_knowledge_from_files(self) -> Dict:
        """
        Sincroniza conhecimento dos arquivos docs-turso
        """
        files = self.scan_docs_turso_files()
        sync_results = {
            'files_scanned': len(files),
            'knowledge_extracted': 0,
            'updated_records': 0,
            'new_records': 0,
            'obsolete_removed': 0
        }
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        for file_info in files:
            knowledge_list = self.extract_knowledge_from_file(file_info)
            
            for knowledge in knowledge_list:
                # Verificar se já existe registro com mesmo source
                cursor.execute("""
                    SELECT id, file_hash FROM turso_agent_knowledge 
                    WHERE source = ?
                """, (knowledge['source'],))
                
                existing = cursor.fetchone()
                
                if existing:
                    record_id, existing_hash = existing
                    
                    # Se hash mudou, atualizar
                    if existing_hash != knowledge['file_hash']:
                        cursor.execute("""
                            UPDATE turso_agent_knowledge 
                            SET topic = ?, content = ?, category = ?, 
                                expertise_level = ?, tags = ?, priority = ?,
                                file_hash = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                        """, (
                            knowledge['topic'], knowledge['content'],
                            knowledge['category'], knowledge['expertise_level'],
                            knowledge['tags'], knowledge['priority'],
                            knowledge['file_hash'], record_id
                        ))
                        sync_results['updated_records'] += 1
                        self.sync_log.append(f"Atualizado: {knowledge['topic']}")
                else:
                    # Inserir novo registro
                    cursor.execute("""
                        INSERT INTO turso_agent_knowledge 
                        (topic, content, category, expertise_level, tags, 
                         source, file_hash, priority, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """, (
                        knowledge['topic'], knowledge['content'],
                        knowledge['category'], knowledge['expertise_level'],
                        knowledge['tags'], knowledge['source'],
                        knowledge['file_hash'], knowledge['priority']
                    ))
                    sync_results['new_records'] += 1
                    self.sync_log.append(f"Novo: {knowledge['topic']}")
                
                sync_results['knowledge_extracted'] += 1
        
        # Remover registros obsoletos
        obsolete = self.detect_obsolete_knowledge(days_threshold=60)
        for record in obsolete:
            cursor.execute("DELETE FROM turso_agent_knowledge WHERE id = ?", (record['id'],))
            sync_results['obsolete_removed'] += 1
            self.sync_log.append(f"Removido obsoleto: {record['topic']}")
        
        conn.commit()
        conn.close()
        
        return sync_results
    
    def generate_sync_report(self, sync_results: Dict) -> str:
        """Gera relatório de sincronização"""
        report = f"""
🔄 RELATÓRIO DE SINCRONIZAÇÃO TURSO KNOWLEDGE
{'='*50}

📊 RESULTADOS:
• Arquivos escaneados: {sync_results['files_scanned']}
• Conhecimento extraído: {sync_results['knowledge_extracted']}
• Registros atualizados: {sync_results['updated_records']}
• Novos registros: {sync_results['new_records']}
• Obsoletos removidos: {sync_results['obsolete_removed']}

📝 LOG DE MUDANÇAS:
"""
        
        for log_entry in self.sync_log:
            report += f"• {log_entry}\n"
        
        report += f"""
⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
✅ Sincronização concluída!
"""
        
        return report
    
    def validate_knowledge_integrity(self) -> Dict:
        """
        Valida integridade do conhecimento
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Verificar registros duplicados
        cursor.execute("""
            SELECT topic, COUNT(*) as count 
            FROM turso_agent_knowledge 
            GROUP BY topic 
            HAVING count > 1
        """)
        duplicates = cursor.fetchall()
        
        # Verificar registros sem conteúdo
        cursor.execute("""
            SELECT COUNT(*) FROM turso_agent_knowledge 
            WHERE content IS NULL OR content = ''
        """)
        empty_content = cursor.fetchone()[0]
        
        # Verificar registros sem tags
        cursor.execute("""
            SELECT COUNT(*) FROM turso_agent_knowledge 
            WHERE tags IS NULL OR tags = ''
        """)
        empty_tags = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'duplicates': len(duplicates),
            'empty_content': empty_content,
            'empty_tags': empty_tags,
            'total_records': self.get_total_records()
        }
    
    def get_total_records(self) -> int:
        """Retorna total de registros"""
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM turso_agent_knowledge")
        total = cursor.fetchone()[0]
        conn.close()
        return total

def main():
    """Função principal"""
    print("🔄 Iniciando sincronização de conhecimento Turso Agent...")
    
    # Inicializar sistema
    sync_system = TursoKnowledgeSync()
    
    # Executar sincronização
    print("📁 Escaneando arquivos docs-turso...")
    sync_results = sync_system.sync_knowledge_from_files()
    
    # Gerar relatório
    report = sync_system.generate_sync_report(sync_results)
    print(report)
    
    # Validar integridade
    print("🔍 Validando integridade do conhecimento...")
    integrity = sync_system.validate_knowledge_integrity()
    
    print(f"""
📊 VALIDAÇÃO DE INTEGRIDADE:
• Total de registros: {integrity['total_records']}
• Duplicatas encontradas: {integrity['duplicates']}
• Conteúdo vazio: {integrity['empty_content']}
• Tags vazias: {integrity['empty_tags']}
""")
    
    # Salvar relatório
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"sync_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
        f.write(f"\nINTEGRIDADE: {json.dumps(integrity, indent=2)}")
    
    print(f"📄 Relatório salvo em: {report_file}")

if __name__ == "__main__":
    main() 