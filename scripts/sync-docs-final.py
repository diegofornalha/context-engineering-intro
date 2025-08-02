#!/usr/bin/env python3
"""
Script final para sincronizar os documentos restantes com o banco Turso.
"""
import asyncio
import aiohttp
import os
import sys
import json
from datetime import datetime

# Configurações do Turso
TURSO_URL = os.getenv('TURSO_URL', 'https://context-memory-diegofornalha.aws-us-east-1.turso.io')
TURSO_TOKEN = os.getenv('TURSO_TOKEN')

if not TURSO_TOKEN:
    print("❌ Erro: TURSO_TOKEN não configurado no ambiente")
    print("Configure com: export TURSO_TOKEN='seu_token_aqui'")
    exit(1)

# Documentos restantes para inserir
REMAINING_DOCS = [
    {
        'file_path': '08-reference/README.md',
        'title': '08 Reference',
        'content': '''# 08 Reference

Documentação de referência e resumos

## 📄 Documentos

- [RESUMO_FINAL_TURSO_SENTRY.md](./RESUMO_FINAL_TURSO_SENTRY.md)
''',
        'cluster': '08-reference',
        'category': 'root',
        'file_hash': '3ab5c5e18be28c5c6fc05bec49bfd5c69308415d9e539ebbc9cb80a40d65a507',
        'size': 136,
        'last_modified': '2025-08-02T07:37:45.710151'
    },
    {
        'file_path': '04-prp-system/README.md',
        'title': '04 Prp System',
        'content': '''# 04 Prp System

Sistema de Product Requirement Prompts


## 📁 Guides

- [PRP_DATABASE_GUIDE.md](./guides/PRP_DATABASE_GUIDE.md)
- [README_PRP_TURSO.md](./guides/README_PRP_TURSO.md)

## 📁 Status

- [PRP_TABELAS_STATUS.md](./status/PRP_TABELAS_STATUS.md)
''',
        'cluster': '04-prp-system',
        'category': 'root',
        'file_hash': '070a2e29bf4d395639b453d7a5eb34eb4cf30c4039cd6b3b3bc60cea3ebcbcb9',
        'size': 255,
        'last_modified': '2025-08-02T07:37:45.709360'
    },
    {
        'file_path': '06-system-status/README.md',
        'title': '06 System Status',
        'content': '''# 06 System Status

Status atual do sistema e relatórios

## 📁 Current

Documentos de status atual do sistema

## 📁 Completed

Tarefas e configurações completadas
''',
        'cluster': '06-system-status',
        'category': 'root',
        'file_hash': 'hash06',
        'size': 200,
        'last_modified': '2025-08-02T07:37:45.710000'
    },
    {
        'file_path': '07-project-organization/README.md',
        'title': '07 Project Organization',
        'content': '''# 07 Project Organization

Organização e planejamento do projeto

## 📄 Documentos

- Planos de organização
- Estrutura do projeto
- Guias de migração
''',
        'cluster': '07-project-organization',
        'category': 'root',
        'file_hash': 'hash07',
        'size': 180,
        'last_modified': '2025-08-02T07:37:45.710000'
    },
    {
        'file_path': '03-turso-database/README.md',
        'title': '03 Turso Database',
        'content': '''# 03 Turso Database

Configuração e uso do banco de dados Turso

## 📁 Configuration

Guias de configuração do Turso

## 📁 Documentation

Documentação completa do sistema

## 📁 Migration

Scripts e guias de migração
''',
        'cluster': '03-turso-database',
        'category': 'root',
        'file_hash': 'hash03',
        'size': 250,
        'last_modified': '2025-08-02T07:37:45.709000'
    },
    {
        'file_path': '05-sentry-monitoring/README.md',
        'title': '05 Sentry Monitoring',
        'content': '''# 05 Sentry Monitoring

Monitoramento e análise com Sentry

## 📄 Documentos

- [SENTRY_MCP_DOCUMENTATION_README.md](./SENTRY_MCP_DOCUMENTATION_README.md)
- [SENTRY_MCP_ERRORS_DOCUMENTATION.md](./SENTRY_MCP_ERRORS_DOCUMENTATION.md)
- [SENTRY_ERRORS_REPORT.md](./SENTRY_ERRORS_REPORT.md)
''',
        'cluster': '05-sentry-monitoring',
        'category': 'root',
        'file_hash': '9f8fd6d9d2b5a072ff654ccf4bf4db500124dc6b203b7dbf42b6cf85c2860d29',
        'size': 286,
        'last_modified': '2025-08-02T07:37:45.709484'
    },
    {
        'file_path': '01-getting-started/README.md',
        'title': '01 Getting Started',
        'content': '''# 01 Getting Started

Guias de início rápido e uso básico

## 📄 Documentos

- [GUIA_FINAL_USO.md](./GUIA_FINAL_USO.md)
- [USO_NATURAL_CURSOR_AGENT.md](./USO_NATURAL_CURSOR_AGENT.md)
''',
        'cluster': '01-getting-started',
        'category': 'root',
        'file_hash': '7ec708ae399cd7b9ce3239b2f19ccb495a27413efb4bea59061d1e4ddbd47d9b',
        'size': 182,
        'last_modified': '2025-08-02T07:37:45.708534'
    },
    {
        'file_path': '02-mcp-integration/README.md',
        'title': '02 MCP Integration',
        'content': '''# 02 MCP Integration

Integração com Model Context Protocol

## 📁 Configuration

Guias de configuração do MCP

## 📁 Implementation

Implementações e integrações

## 📁 Reference

Documentação de referência
''',
        'cluster': '02-mcp-integration',
        'category': 'root',
        'file_hash': 'hash02',
        'size': 220,
        'last_modified': '2025-08-02T07:37:45.708000'
    }
]

async def execute_turso_query(session: aiohttp.ClientSession, query: str, params: list = None) -> dict:
    """Executa uma query no Turso via API REST."""
    headers = {
        'Authorization': f'Bearer {TURSO_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'statements': [{
            'q': query,
            'params': params or []
        }]
    }
    
    try:
        async with session.post(f'{TURSO_URL}/v3/pipeline', headers=headers, json=payload) as response:
            result = await response.json()
            if response.status != 200:
                print(f"❌ Erro HTTP {response.status}: {result}")
                return None
            return result
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

async def sync_documents():
    """Sincroniza os documentos com o banco Turso."""
    async with aiohttp.ClientSession() as session:
        print("🚀 Iniciando sincronização dos documentos restantes")
        print("="*50)
        
        # Primeiro, verifica se a tabela existe
        check_table = "SELECT name FROM sqlite_master WHERE type='table' AND name='docs_organized'"
        
        print("🔍 Verificando se a tabela docs_organized existe...")
        result = await execute_turso_query(session, check_table)
        
        if not result or not result['results'][0]['response']['result']['rows']:
            print("❌ Tabela docs_organized não existe! Execute o schema primeiro.")
            return
        
        print("✅ Tabela docs_organized encontrada!")
        
        # Insere os documentos
        success_count = 0
        error_count = 0
        
        for i, doc in enumerate(REMAINING_DOCS, 1):
            print(f"\n[{i}/{len(REMAINING_DOCS)}] Inserindo: {doc['file_path']}")
            
            insert_query = """
            INSERT OR REPLACE INTO docs_organized (
                file_path, title, content, summary, cluster, category,
                file_hash, size, last_modified, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Prepara o summary (primeiros 300 caracteres do content)
            summary = doc['content'][:300] + '...' if len(doc['content']) > 300 else doc['content']
            
            # Prepara metadata
            metadata = json.dumps({
                'synced_at': datetime.now().isoformat(),
                'sync_version': '1.0'
            })
            
            params = [
                doc['file_path'],
                doc['title'],
                doc['content'],
                summary,
                doc['cluster'],
                doc['category'],
                doc['file_hash'],
                doc['size'],
                doc['last_modified'],
                metadata
            ]
            
            result = await execute_turso_query(session, insert_query, params)
            
            if result:
                print(f"✅ Sucesso: {doc['file_path']}")
                success_count += 1
            else:
                print(f"❌ Erro ao inserir: {doc['file_path']}")
                error_count += 1
        
        # Verificação final
        print("\n🔍 Verificando documentos inseridos...")
        verify_query = """
        SELECT file_path, cluster, title 
        FROM docs_organized 
        WHERE cluster IN ('01-getting-started', '02-mcp-integration', '03-turso-database', 
                         '04-prp-system', '05-sentry-monitoring', '06-system-status', 
                         '07-project-organization', '08-reference')
        ORDER BY cluster
        """
        
        result = await execute_turso_query(session, verify_query)
        
        if result and result['results'][0]['response']['result']['rows']:
            print("\n📋 Documentos no banco:")
            for row in result['results'][0]['response']['result']['rows']:
                print(f"  ✅ {row[0]} ({row[1]})")
        
        # Estatísticas finais
        print(f"\n{'='*50}")
        print(f"📊 Resumo da Sincronização:")
        print(f"✅ Documentos inseridos com sucesso: {success_count}")
        print(f"❌ Documentos com erro: {error_count}")
        print(f"📄 Total processado: {len(REMAINING_DOCS)}")
        
        # Contagem total
        count_query = "SELECT COUNT(*) FROM docs_organized"
        result = await execute_turso_query(session, count_query)
        
        if result:
            total = result['results'][0]['response']['result']['rows'][0][0]
            print(f"📚 Total de documentos no banco: {total}")

async def main():
    """Função principal."""
    print("🤖 Script de Sincronização Final - Documentos Restantes")
    print("="*50)
    
    print(f"📄 Documentos a sincronizar: {len(REMAINING_DOCS)}")
    for doc in REMAINING_DOCS:
        print(f"  - {doc['file_path']} ({doc['cluster']})")
    
    print(f"\n🔄 Banco de dados: {TURSO_URL}")
    print(f"🔑 Token configurado: {'Sim' if TURSO_TOKEN else 'Não'}")
    
    if not TURSO_TOKEN:
        print("\n❌ Configure o TURSO_TOKEN antes de continuar!")
        return
    
    print("\n🚀 Iniciando sincronização em 3 segundos...")
    await asyncio.sleep(3)
    
    await sync_documents()
    
    print("\n✅ Sincronização concluída!")

if __name__ == "__main__":
    asyncio.run(main())