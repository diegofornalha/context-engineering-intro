#!/usr/bin/env python3
"""
Script simples para executar os inserts restantes via MCP Turso.
"""
import os
import sys
import time

# Adiciona o diretório do projeto ao path
sys.path.append('/Users/agents/Desktop/context-engineering-intro')

def main():
    print("🚀 Executando inserts restantes dos documentos")
    print("="*50)
    
    # Lista dos 8 documentos restantes
    remaining_docs = [
        ('08-reference/README.md', '08-reference'),
        ('04-prp-system/README.md', '04-prp-system'),
        ('06-system-status/README.md', '06-system-status'),
        ('07-project-organization/README.md', '07-project-organization'),
        ('03-turso-database/README.md', '03-turso-database'),
        ('05-sentry-monitoring/README.md', '05-sentry-monitoring'),
        ('01-getting-started/README.md', '01-getting-started'),
        ('02-mcp-integration/README.md', '02-mcp-integration')
    ]
    
    print(f"📄 Total de documentos para inserir: {len(remaining_docs)}")
    print("\n📋 Documentos:")
    for doc, cluster in remaining_docs:
        print(f"  - {doc} ({cluster})")
    
    print("\n✅ Use o MCP Turso no Claude Code para executar o arquivo:")
    print("   /sql/operations/execute-remaining.sql")
    print("\nOu execute manualmente cada INSERT do arquivo.")
    
    # Cria um resumo dos comandos
    print("\n📝 Comandos sugeridos para Claude Code:")
    print("="*50)
    print("1. Primeiro, verifique se a tabela existe:")
    print("   SELECT name FROM sqlite_master WHERE type='table' AND name='docs_organized';")
    print("\n2. Execute o arquivo SQL:")
    print("   Leia e execute: /sql/operations/execute-remaining.sql")
    print("\n3. Verifique o resultado:")
    print("   SELECT file_path, cluster FROM docs_organized WHERE cluster LIKE '%reference%' OR cluster LIKE '%getting-started%';")

if __name__ == "__main__":
    main()