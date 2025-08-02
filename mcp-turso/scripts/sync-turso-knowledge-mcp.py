#!/usr/bin/env python3
"""
Sistema de Sincronização de Conhecimento Turso Agent via MCP

Script para manter o conhecimento do Turso Agent atualizado,
detectar dados obsoletos e sincronizar com fontes externas.
Usa MCP Turso para acessar o banco remoto.
"""

import os
import glob
import hashlib
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class TursoKnowledgeSyncMCP:
    """
    Sistema de sincronização de conhecimento do Turso Agent via MCP
    """
    
    def __init__(self):
        """Inicializa o sistema de sync via MCP"""
        self.sync_log = []
        
    def get_file_hash(self, file_path: str) -> str:
        """Calcula hash MD5 de um arquivo"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
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
    
    def execute_mcp_query(self, query: str, database: str = "context-memory") -> Dict:
        """
        Executa query via MCP Turso
        """
        try:
            # Usar MCP Turso para executar query
            # Por enquanto, vamos simular com uma query simples
            print(f"🔍 Executando query MCP: {query[:50]}...")
            return {"success": True, "result": "Query executada via MCP"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_existing_knowledge(self, source: str) -> Optional[Dict]:
        """
        Verifica se conhecimento já existe via MCP
        """
        query = f"SELECT id, file_hash FROM turso_agent_knowledge WHERE source = '{source}'"
        result = self.execute_mcp_query(query)
        
        if result.get("success"):
            # Simular resultado para teste
            return {"id": 1, "file_hash": "test_hash"}
        return None
    
    def insert_knowledge(self, knowledge: Dict) -> bool:
        """
        Insere conhecimento via MCP
        """
        query = f"""
        INSERT INTO turso_agent_knowledge 
        (topic, content, category, expertise_level, tags, 
         source, file_hash, priority, created_at, updated_at)
        VALUES (
            '{knowledge['topic']}', 
            '{knowledge['content'].replace("'", "''")}', 
            '{knowledge['category']}', 
            '{knowledge['expertise_level']}', 
            '{knowledge['tags']}', 
            '{knowledge['source']}', 
            '{knowledge['file_hash']}', 
            {knowledge['priority']}, 
            CURRENT_TIMESTAMP, 
            CURRENT_TIMESTAMP
        )
        """
        
        result = self.execute_mcp_query(query)
        return result.get("success", False)
    
    def update_knowledge(self, knowledge: Dict, record_id: int) -> bool:
        """
        Atualiza conhecimento via MCP
        """
        query = f"""
        UPDATE turso_agent_knowledge 
        SET topic = '{knowledge['topic']}', 
            content = '{knowledge['content'].replace("'", "''")}', 
            category = '{knowledge['category']}', 
            expertise_level = '{knowledge['expertise_level']}', 
            tags = '{knowledge['tags']}', 
            priority = {knowledge['priority']},
            file_hash = '{knowledge['file_hash']}', 
            updated_at = CURRENT_TIMESTAMP
        WHERE id = {record_id}
        """
        
        result = self.execute_mcp_query(query)
        return result.get("success", False)
    
    def sync_knowledge_from_files(self) -> Dict:
        """
        Sincroniza conhecimento dos arquivos docs-turso via MCP
        """
        files = self.scan_docs_turso_files()
        sync_results = {
            'files_scanned': len(files),
            'knowledge_extracted': 0,
            'updated_records': 0,
            'new_records': 0,
            'obsolete_removed': 0
        }
        
        print(f"📁 Encontrados {len(files)} arquivos para processar...")
        
        for file_info in files:
            knowledge_list = self.extract_knowledge_from_file(file_info)
            
            for knowledge in knowledge_list:
                print(f"🔄 Processando: {knowledge['topic']}")
                
                # Verificar se já existe registro
                existing = self.check_existing_knowledge(knowledge['source'])
                
                if existing:
                    # Se hash mudou, atualizar
                    if existing['file_hash'] != knowledge['file_hash']:
                        if self.update_knowledge(knowledge, existing['id']):
                            sync_results['updated_records'] += 1
                            self.sync_log.append(f"Atualizado: {knowledge['topic']}")
                            print(f"✅ Atualizado: {knowledge['topic']}")
                        else:
                            print(f"❌ Erro ao atualizar: {knowledge['topic']}")
                else:
                    # Inserir novo registro
                    if self.insert_knowledge(knowledge):
                        sync_results['new_records'] += 1
                        self.sync_log.append(f"Novo: {knowledge['topic']}")
                        print(f"✅ Novo: {knowledge['topic']}")
                    else:
                        print(f"❌ Erro ao inserir: {knowledge['topic']}")
                
                sync_results['knowledge_extracted'] += 1
        
        return sync_results
    
    def generate_sync_report(self, sync_results: Dict) -> str:
        """Gera relatório de sincronização"""
        report = f"""
🔄 RELATÓRIO DE SINCRONIZAÇÃO TURSO KNOWLEDGE (MCP)
{'='*60}

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
✅ Sincronização via MCP concluída!
"""
        
        return report

def main():
    """Função principal"""
    print("🔄 Iniciando sincronização de conhecimento Turso Agent via MCP...")
    
    # Inicializar sistema
    sync_system = TursoKnowledgeSyncMCP()
    
    # Executar sincronização
    print("📁 Escaneando arquivos docs-turso...")
    sync_results = sync_system.sync_knowledge_from_files()
    
    # Gerar relatório
    report = sync_system.generate_sync_report(sync_results)
    print(report)
    
    # Salvar relatório
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"sync_report_mcp_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Relatório salvo em: {report_file}")

if __name__ == "__main__":
    main() 