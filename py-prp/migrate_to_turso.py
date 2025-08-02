#!/usr/bin/env python3
"""
Script para migrar dados documentados do SQLite local para o banco de dados Turso.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

def read_local_database(db_path: str) -> Dict[str, Any]:
    """Lê os dados do banco de dados local."""
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Banco de dados não encontrado: {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Ler erros do Sentry
        cursor = conn.execute("""
            SELECT project_name, error_title, error_level, event_count, status, created_at
            FROM sentry_errors
            ORDER BY created_at DESC
        """)
        sentry_errors = cursor.fetchall()
        
        # Ler projetos
        cursor = conn.execute("""
            SELECT project_name, issue_count, last_updated
            FROM sentry_projects
        """)
        projects = cursor.fetchall()
        
        # Ler problemas de MCP
        cursor = conn.execute("""
            SELECT mcp_name, issue_type, description, status, created_at
            FROM mcp_issues
        """)
        mcp_issues = cursor.fetchall()
        
        return {
            "sentry_errors": sentry_errors,
            "projects": projects,
            "mcp_issues": mcp_issues
        }
        
    finally:
        conn.close()

def generate_turso_migration_script(data: Dict[str, Any]) -> str:
    """Gera script SQL para migração para Turso."""
    
    script = f"""
-- Script de Migração para Turso
-- Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
-- Total de registros: {len(data['sentry_errors'])} erros, {len(data['projects'])} projetos, {len(data['mcp_issues'])} problemas MCP

-- Criar tabelas no Turso
CREATE TABLE IF NOT EXISTS sentry_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    error_title TEXT NOT NULL,
    error_level TEXT NOT NULL,
    event_count INTEGER DEFAULT 1,
    status TEXT DEFAULT 'unresolved',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sentry_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT UNIQUE NOT NULL,
    issue_count INTEGER DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mcp_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mcp_name TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME NULL
);

-- Inserir projetos
"""
    
    for project_name, issue_count, last_updated in data['projects']:
        script += f"INSERT OR REPLACE INTO sentry_projects (project_name, issue_count, last_updated) VALUES ('{project_name}', {issue_count}, '{last_updated}');\n"
    
    script += "\n-- Inserir erros do Sentry\n"
    
    for project_name, error_title, error_level, event_count, status, created_at in data['sentry_errors']:
        # Escapar aspas simples no título
        safe_title = error_title.replace("'", "''")
        script += f"INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status, created_at) VALUES ('{project_name}', '{safe_title}', '{error_level}', {event_count}, '{status}', '{created_at}');\n"
    
    script += "\n-- Inserir problemas de MCP\n"
    
    for mcp_name, issue_type, description, status, created_at in data['mcp_issues']:
        # Escapar aspas simples na descrição
        safe_description = description.replace("'", "''")
        script += f"INSERT INTO mcp_issues (mcp_name, issue_type, description, status, created_at) VALUES ('{mcp_name}', '{issue_type}', '{safe_description}', '{status}', '{created_at}');\n"
    
    return script

def generate_verification_queries() -> str:
    """Gera queries para verificar a migração."""
    
    return """
-- Queries para verificar a migração

-- Verificar total de registros
SELECT 'sentry_errors' as table_name, COUNT(*) as total FROM sentry_errors
UNION ALL
SELECT 'sentry_projects' as table_name, COUNT(*) as total FROM sentry_projects
UNION ALL
SELECT 'mcp_issues' as table_name, COUNT(*) as total FROM mcp_issues;

-- Verificar erros críticos
SELECT project_name, error_title, error_level, event_count 
FROM sentry_errors 
WHERE error_level = 'error';

-- Verificar problemas de MCP abertos
SELECT mcp_name, issue_type, description 
FROM mcp_issues 
WHERE status = 'open';

-- Estatísticas por projeto
SELECT 
    project_name,
    COUNT(*) as total_issues,
    SUM(CASE WHEN error_level = 'error' THEN 1 ELSE 0 END) as critical_errors,
    SUM(CASE WHEN error_level = 'warning' THEN 1 ELSE 0 END) as warnings,
    SUM(CASE WHEN error_level = 'info' THEN 1 ELSE 0 END) as info_messages
FROM sentry_errors 
GROUP BY project_name;
"""

def main():
    """Função principal."""
    
    local_db_path = "sentry_errors_documentation.db"
    
    try:
        print("📖 Lendo dados do banco local...")
        data = read_local_database(local_db_path)
        
        print("📝 Gerando script de migração...")
        migration_script = generate_turso_migration_script(data)
        
        # Salvar script de migração
        with open("migrate_to_turso.sql", "w", encoding="utf-8") as f:
            f.write(migration_script)
        
        print("🔍 Gerando queries de verificação...")
        verification_queries = generate_verification_queries()
        
        # Salvar queries de verificação
        with open("verify_migration.sql", "w", encoding="utf-8") as f:
            f.write(verification_queries)
        
        print("✅ Scripts gerados com sucesso!")
        print("📄 Script de migração: migrate_to_turso.sql")
        print("🔍 Queries de verificação: verify_migration.sql")
        
        print(f"\n📊 Resumo dos dados:")
        print(f"- Erros do Sentry: {len(data['sentry_errors'])}")
        print(f"- Projetos: {len(data['projects'])}")
        print(f"- Problemas MCP: {len(data['mcp_issues'])}")
        
        print("\n🚀 Para migrar para o Turso:")
        print("1. Resolver problema de autenticação do MCP Turso")
        print("2. Executar: turso db shell sentry-errors-doc < migrate_to_turso.sql")
        print("3. Verificar: turso db shell sentry-errors-doc < verify_migration.sql")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 