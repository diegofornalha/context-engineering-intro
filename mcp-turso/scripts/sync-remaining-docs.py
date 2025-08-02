#!/usr/bin/env python3
"""
Script para sincronizar os documentos restantes com o banco Turso.
Lê o arquivo execute-remaining.sql e executa os inserts.
"""
import asyncio
import aiohttp
import os
import re
from datetime import datetime
from typing import List, Dict, Any
import hashlib
import json

# Configurações do Turso
TURSO_URL = os.getenv('TURSO_URL', 'https://my-turso-db-ruv.turso.io')
TURSO_TOKEN = os.getenv('TURSO_TOKEN')

if not TURSO_TOKEN:
    print("❌ Erro: TURSO_TOKEN não configurado no ambiente")
    exit(1)

def parse_sql_inserts(sql_content: str) -> List[Dict[str, Any]]:
    """Extrai os valores dos INSERT statements do SQL."""
    documents = []
    
    # Pattern para capturar os INSERT statements
    insert_pattern = r"INSERT OR REPLACE INTO docs_organized.*?VALUES\s*\((.*?)\);?"
    
    # Encontra todos os INSERT statements
    inserts = re.findall(insert_pattern, sql_content, re.DOTALL | re.IGNORECASE)
    
    for insert_values in inserts:
        # Remove espaços e quebras de linha extras
        values = insert_values.strip()
        
        # Extrai os valores (simplificado - assume ordem correta)
        # Esta é uma versão simplificada - em produção, use um parser SQL adequado
        try:
            # Remove comentários SQL
            values = re.sub(r'--.*?\n', '', values)
            
            # Tenta extrair valores entre aspas simples
            value_pattern = r"'([^']*(?:''[^']*)*)'"
            matches = re.findall(value_pattern, values)
            
            if len(matches) >= 10:  # Esperamos pelo menos 10 campos
                doc = {
                    'file_path': matches[0].replace("''", "'"),
                    'title': matches[1].replace("''", "'"),
                    'content': matches[2].replace("''", "'"),
                    'summary': matches[3].replace("''", "'"),
                    'cluster': matches[4],
                    'category': matches[5],
                    'file_hash': matches[6],
                    'size': int(matches[7]) if matches[7].isdigit() else 0,
                    'last_modified': matches[8],
                    'metadata': matches[9]
                }
                documents.append(doc)
                print(f"✅ Parseado: {doc['file_path']}")
        except Exception as e:
            print(f"⚠️ Erro ao parsear insert: {str(e)}")
            continue
    
    return documents

async def execute_turso_query(session: aiohttp.ClientSession, query: str, params: List[Any] = None) -> Dict:
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
    
    async with session.post(f'{TURSO_URL}/v3/pipeline', headers=headers, json=payload) as response:
        result = await response.json()
        if response.status != 200:
            raise Exception(f"Erro na API Turso: {result}")
        return result

async def sync_documents(documents: List[Dict[str, Any]]):
    """Sincroniza os documentos com o banco Turso."""
    async with aiohttp.ClientSession() as session:
        # Primeiro, verifica se a tabela existe
        check_table = """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='docs_organized'
        """
        
        try:
            result = await execute_turso_query(session, check_table)
            if not result['results'][0]['response']['result']['rows']:
                print("❌ Tabela docs_organized não existe! Execute o schema primeiro.")
                return
        except Exception as e:
            print(f"❌ Erro ao verificar tabela: {e}")
            return
        
        # Insere os documentos
        success_count = 0
        error_count = 0
        
        for i, doc in enumerate(documents, 1):
            print(f"\n[{i}/{len(documents)}] Inserindo: {doc['file_path']}")
            
            insert_query = """
            INSERT OR REPLACE INTO docs_organized (
                file_path, title, content, summary, cluster, category,
                file_hash, size, last_modified, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = [
                doc['file_path'],
                doc['title'],
                doc['content'],
                doc['summary'],
                doc['cluster'],
                doc['category'],
                doc['file_hash'],
                doc['size'],
                doc['last_modified'],
                doc['metadata']
            ]
            
            try:
                await execute_turso_query(session, insert_query, params)
                print(f"✅ Sucesso: {doc['file_path']}")
                success_count += 1
            except Exception as e:
                print(f"❌ Erro: {e}")
                error_count += 1
        
        # Estatísticas finais
        print(f"\n{'='*50}")
        print(f"📊 Resumo da Sincronização:")
        print(f"✅ Documentos inseridos com sucesso: {success_count}")
        print(f"❌ Documentos com erro: {error_count}")
        print(f"📄 Total processado: {len(documents)}")

async def main():
    """Função principal."""
    print("🚀 Sincronização de Documentos Restantes")
    print("="*50)
    
    # Lê o arquivo SQL
    sql_file = "/Users/agents/Desktop/context-engineering-intro/sql/operations/execute-remaining.sql"
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        print(f"✅ Arquivo SQL lido: {sql_file}")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo SQL: {e}")
        return
    
    # Parseia os INSERT statements
    documents = parse_sql_inserts(sql_content)
    print(f"\n📄 Total de documentos encontrados: {len(documents)}")
    
    if not documents:
        print("⚠️ Nenhum documento encontrado para sincronizar!")
        return
    
    # Mostra os documentos que serão sincronizados
    print("\n📋 Documentos a sincronizar:")
    for doc in documents:
        print(f"  - {doc['file_path']} ({doc['cluster']})")
    
    # Pergunta confirmação
    print(f"\n🔄 Pronto para sincronizar {len(documents)} documentos?")
    input("Pressione Enter para continuar ou Ctrl+C para cancelar...")
    
    # Executa a sincronização
    await sync_documents(documents)
    
    print("\n✅ Sincronização concluída!")

if __name__ == "__main__":
    asyncio.run(main())