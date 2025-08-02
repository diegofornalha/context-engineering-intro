#!/usr/bin/env python3
"""
Sistema de Organização de Documentos em Clusters
Analisa, categoriza e reorganiza documentos em uma estrutura clusterizada
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import hashlib

class DocOrganizer:
    def __init__(self, docs_path):
        self.docs_path = Path(docs_path)
        self.backup_path = self.docs_path.parent / "docs_backup"
        self.clusters = {
            "01-getting-started": {
                "description": "Guias de início rápido e uso básico",
                "files": [
                    "GUIA_FINAL_USO.md",
                    "USO_NATURAL_CURSOR_AGENT.md"
                ]
            },
            "02-mcp-integration": {
                "description": "Integração com Model Context Protocol",
                "subdirs": {
                    "configuration": [
                        "ATIVACAO_MCP_REAL_CURSOR.md",
                        "CONFIGURACAO_CURSOR_MCP.md",
                        "MCP_ENV_CAPABILITIES.md"
                    ],
                    "implementation": [
                        "MCP_SYNC_INTELIGENTE_IMPLEMENTADO.md",
                        "INTEGRACAO_TURSO_MCP_FINAL.md"
                    ],
                    "reference": [
                        "mcp-comparison-diagram.md",
                        "MCP_SERVERS_STATUS.md"
                    ]
                }
            },
            "03-turso-database": {
                "description": "Configuração e uso do Turso Database",
                "subdirs": {
                    "configuration": [
                        "TURSO_CONFIGURATION_SUMMARY.md",
                        "ENV_CONFIGURATION_SUMMARY.md"
                    ],
                    "documentation": [
                        "TURSO_MEMORY_README.md",
                        "GUIA_COMPLETO_TURSO_MCP.md"
                    ],
                    "migration": [
                        "MCP_TURSO_MIGRATION_PLAN.md",
                        "DOCS_TURSO_MIGRATION_SUCCESS.md"
                    ]
                }
            },
            "04-prp-system": {
                "description": "Sistema de Product Requirement Prompts",
                "subdirs": {
                    "guides": [
                        "PRP_DATABASE_GUIDE.md",
                        "README_PRP_TURSO.md"
                    ],
                    "status": [
                        "PRP_TABELAS_STATUS.md"
                    ]
                }
            },
            "05-sentry-monitoring": {
                "description": "Monitoramento e análise com Sentry",
                "files": [
                    "SENTRY_MCP_DOCUMENTATION_README.md",
                    "SENTRY_MCP_ERRORS_DOCUMENTATION.md",
                    "SENTRY_ERRORS_REPORT.md"
                ]
            },
            "06-system-status": {
                "description": "Status e relatórios do sistema",
                "subdirs": {
                    "current": [
                        "SISTEMA_FINAL_SIMPLIFICADO_FUNCIONANDO.md",
                        "MEMORY_SYSTEM_STATUS.md",
                        "MEMORY_SYSTEM_SUMMARY.md",
                        "TURSO_MCP_STATUS.md"
                    ],
                    "completed": [
                        "SISTEMA_DOCS_CLUSTERS_FUNCIONANDO.md"
                    ]
                }
            },
            "07-project-organization": {
                "description": "Organização e estrutura do projeto",
                "files": [
                    "ESTRUTURA_ORGANIZACAO.md",
                    "PROJETO_VIVO_ADAPTATIVO.md",
                    "plan.md"
                ]
            },
            "08-reference": {
                "description": "Documentação de referência e resumos",
                "files": [
                    "RESUMO_FINAL_TURSO_SENTRY.md"
                ]
            },
            "archive": {
                "description": "Documentos arquivados e depreciados",
                "subdirs": {
                    "deprecated": [
                        "diagnostico-mcp.md",
                        "SOLUCAO_MCP_TURSO.md",
                        "IMPLEMENTACAO_RAPIDA.md"
                    ],
                    "duplicates": [
                        "GUIA_INTEGRACAO_FINAL.md",
                        "GUIA_USO_CURSOR_AGENT_TURSO.md",
                        "INTEGRACAO_PRP_MCP_TURSO.md",
                        "INTEGRACAO_AGENTE_MCP_CURSOR.md",
                        "ENV_CONFIGURATION_EXPLANATION.md"
                    ]
                }
            }
        }
        
        self.metadata = {
            "organized_at": datetime.now().isoformat(),
            "total_files": 0,
            "clusters_created": 0,
            "files_moved": 0,
            "duplicates_found": 0
        }

    def create_backup(self):
        """Cria backup da estrutura atual antes de reorganizar"""
        print("📦 Criando backup dos documentos...")
        if self.backup_path.exists():
            shutil.rmtree(self.backup_path)
        shutil.copytree(self.docs_path, self.backup_path)
        print(f"✅ Backup criado em: {self.backup_path}")

    def calculate_file_hash(self, filepath):
        """Calcula hash do arquivo para detectar duplicatas"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def create_cluster_structure(self):
        """Cria a nova estrutura de clusters"""
        print("\n🏗️  Criando estrutura de clusters...")
        
        for cluster_name, cluster_info in self.clusters.items():
            cluster_path = self.docs_path / cluster_name
            
            # Criar diretório principal do cluster
            cluster_path.mkdir(exist_ok=True)
            self.metadata["clusters_created"] += 1
            
            # Criar README do cluster
            readme_content = f"# {cluster_name.replace('-', ' ').title()}\n\n"
            readme_content += f"{cluster_info['description']}\n\n"
            
            # Processar arquivos diretos
            if "files" in cluster_info:
                readme_content += "## 📄 Documentos\n\n"
                for file in cluster_info["files"]:
                    readme_content += f"- [{file}](./{file})\n"
            
            # Processar subdiretórios
            if "subdirs" in cluster_info:
                for subdir, files in cluster_info["subdirs"].items():
                    subdir_path = cluster_path / subdir
                    subdir_path.mkdir(exist_ok=True)
                    
                    readme_content += f"\n## 📁 {subdir.title()}\n\n"
                    for file in files:
                        readme_content += f"- [{file}](./{subdir}/{file})\n"
            
            # Salvar README do cluster
            readme_path = cluster_path / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"✅ Cluster criado: {cluster_name}")

    def move_files_to_clusters(self):
        """Move arquivos para seus respectivos clusters"""
        print("\n📂 Movendo arquivos para clusters...")
        
        # Coletar todos os arquivos atuais
        current_files = list(self.docs_path.glob("*.md"))
        self.metadata["total_files"] = len(current_files)
        
        # Criar mapeamento de arquivo -> destino
        file_destinations = {}
        
        for cluster_name, cluster_info in self.clusters.items():
            cluster_path = self.docs_path / cluster_name
            
            # Arquivos diretos
            if "files" in cluster_info:
                for file in cluster_info["files"]:
                    file_destinations[file] = cluster_path / file
            
            # Arquivos em subdiretórios
            if "subdirs" in cluster_info:
                for subdir, files in cluster_info["subdirs"].items():
                    subdir_path = cluster_path / subdir
                    for file in files:
                        file_destinations[file] = subdir_path / file
        
        # Mover arquivos
        for current_file in current_files:
            filename = current_file.name
            
            if filename in file_destinations:
                destination = file_destinations[filename]
                
                # Criar diretório de destino se não existir
                destination.parent.mkdir(parents=True, exist_ok=True)
                
                # Mover arquivo
                shutil.move(str(current_file), str(destination))
                self.metadata["files_moved"] += 1
                print(f"  ↪️  {filename} → {destination.parent.relative_to(self.docs_path)}")

    def create_main_readme(self):
        """Cria README principal com índice de todos os clusters"""
        print("\n📝 Criando README principal...")
        
        readme_content = """# 📚 Documentação do Projeto - Context Engineering

> Documentação organizada em clusters temáticos para facilitar navegação e manutenção.

## 🏗️ Estrutura de Clusters

"""
        
        for cluster_name, cluster_info in self.clusters.items():
            if cluster_name != "archive":  # Não incluir archive no índice principal
                readme_content += f"### [{cluster_name.replace('-', ' ').title()}](./{cluster_name}/)\n"
                readme_content += f"{cluster_info['description']}\n\n"
        
        readme_content += f"""
## 📊 Estatísticas da Organização

- **Data da organização:** {self.metadata['organized_at']}
- **Total de arquivos:** {self.metadata['total_files']}
- **Clusters criados:** {self.metadata['clusters_created']}
- **Arquivos movidos:** {self.metadata['files_moved']}

## 🔄 Manutenção

Para manter a documentação organizada:

1. Sempre adicione novos documentos no cluster apropriado
2. Atualize o README do cluster ao adicionar/remover documentos
3. Marque documentos obsoletos antes de arquivá-los
4. Use convenção de nomenclatura consistente

## 🗄️ Arquivos Arquivados

Documentos obsoletos ou duplicados estão em [`./archive/`](./archive/)

---
*Organização automática realizada por `organize-docs-clusters.py`*
"""
        
        readme_path = self.docs_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README principal criado")

    def save_metadata(self):
        """Salva metadados da organização"""
        metadata_path = self.docs_path / ".organization-metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"\n💾 Metadados salvos em: {metadata_path}")

    def organize(self):
        """Executa todo o processo de organização"""
        print("🚀 Iniciando organização de documentos em clusters\n")
        
        # 1. Criar backup
        self.create_backup()
        
        # 2. Criar estrutura de clusters
        self.create_cluster_structure()
        
        # 3. Mover arquivos
        self.move_files_to_clusters()
        
        # 4. Criar README principal
        self.create_main_readme()
        
        # 5. Salvar metadados
        self.save_metadata()
        
        print("\n✅ Organização concluída com sucesso!")
        print(f"\n📊 Resumo:")
        print(f"  - Clusters criados: {self.metadata['clusters_created']}")
        print(f"  - Arquivos organizados: {self.metadata['files_moved']}")
        print(f"  - Backup disponível em: {self.backup_path}")


if __name__ == "__main__":
    # Caminho dos documentos
    docs_path = "/Users/agents/Desktop/context-engineering-intro/docs"
    
    # Confirmar execução
    print("⚠️  Este script irá reorganizar todos os documentos em clusters.")
    print(f"📁 Diretório: {docs_path}")
    response = input("\nDeseja continuar? (s/n): ")
    
    if response.lower() == 's':
        organizer = DocOrganizer(docs_path)
        organizer.organize()
    else:
        print("❌ Operação cancelada")