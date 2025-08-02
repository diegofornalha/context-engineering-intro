#!/usr/bin/env python3
"""
Script para documentar erros do MCP Sentry no banco de dados Turso.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

# Dados dos erros coletados via MCP Sentry
SENTRY_ERRORS_DATA = {
    "projects": [
        {
            "name": "coflow",
            "issues": [
                {
                    "title": "Error: This is your first error!",
                    "level": "error",
                    "events": 1,
                    "status": "unresolved"
                },
                {
                    "title": "Session will end abnormally",
                    "level": "warning",
                    "events": 2,
                    "status": "unresolved"
                },
                {
                    "title": "Error: Teste de captura de exceção via MCP Sentry",
                    "level": "warning",
                    "events": 2,
                    "status": "unresolved"
                },
                {
                    "title": "Teste do MCP - 20250802-020905",
                    "level": "info",
                    "events": 1,
                    "status": "unresolved"
                },
                {
                    "title": "Teste do MCP Sentry funcionando perfeitamente no Cursor Agent! 🎉",
                    "level": "info",
                    "events": 1,
                    "status": "unresolved"
                },
                {
                    "title": "Teste do MCP Standalone - Sat Aug 2 00:59:45 -03 2025",
                    "level": "info",
                    "events": 3,
                    "status": "unresolved"
                },
                {
                    "title": "Teste de validação do MCP Sentry - Credenciais funcionando perfeitamente!",
                    "level": "info",
                    "events": 1,
                    "status": "unresolved"
                },
                {
                    "title": "Teste finalizado com sucesso - MCP Sentry funcionando corretamente",
                    "level": "info",
                    "events": 1,
                    "status": "unresolved"
                },
                {
                    "title": "Teste inicial do MCP Sentry no Claude Code",
                    "level": "info",
                    "events": 1,
                    "status": "unresolved"
                },
                {
                    "title": "Test message from React app",
                    "level": "info",
                    "events": 1,
                    "status": "unresolved"
                }
            ]
        },
        {
            "name": "mcp-test-project",
            "issues": []
        }
    ]
}

def create_database_schema(conn: sqlite3.Connection) -> None:
    """Cria o schema do banco de dados."""
    
    # Tabela principal de erros
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentry_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            error_title TEXT NOT NULL,
            error_level TEXT NOT NULL,
            event_count INTEGER DEFAULT 1,
            status TEXT DEFAULT 'unresolved',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de projetos
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentry_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE NOT NULL,
            issue_count INTEGER DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de documentação de problemas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mcp_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mcp_name TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved_at DATETIME NULL
        )
    """)
    
    conn.commit()

def insert_sentry_errors(conn: sqlite3.Connection, data: Dict[str, Any]) -> None:
    """Insere os erros do Sentry no banco de dados."""
    
    for project in data["projects"]:
        project_name = project["name"]
        
        # Inserir projeto
        conn.execute("""
            INSERT OR REPLACE INTO sentry_projects (project_name, issue_count, last_updated)
            VALUES (?, ?, ?)
        """, (project_name, len(project["issues"]), datetime.now()))
        
        # Inserir erros do projeto
        for issue in project["issues"]:
            conn.execute("""
                INSERT INTO sentry_errors (project_name, error_title, error_level, event_count, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                project_name,
                issue["title"],
                issue["level"],
                issue["events"],
                issue["status"]
            ))
    
    conn.commit()

def insert_mcp_issues(conn: sqlite3.Connection) -> None:
    """Insere problemas identificados nos MCPs."""
    
    mcp_issues = [
        {
            "mcp_name": "Turso",
            "issue_type": "authentication",
            "description": "Erro de autenticação JWT: 'could not parse jwt id' - Impossibilidade de acessar bancos de dados"
        },
        {
            "mcp_name": "Sentry",
            "issue_type": "cleanup_needed",
            "description": "Muitos testes antigos no sistema de produção - Necessário limpeza"
        }
    ]
    
    for issue in mcp_issues:
        conn.execute("""
            INSERT INTO mcp_issues (mcp_name, issue_type, description)
            VALUES (?, ?, ?)
        """, (issue["mcp_name"], issue["issue_type"], issue["description"]))
    
    conn.commit()

def generate_report(conn: sqlite3.Connection) -> str:
    """Gera um relatório dos dados inseridos."""
    
    # Estatísticas gerais
    cursor = conn.execute("SELECT COUNT(*) FROM sentry_errors")
    total_errors = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM sentry_errors WHERE error_level = 'error'")
    critical_errors = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM sentry_errors WHERE error_level = 'warning'")
    warnings = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM sentry_errors WHERE error_level = 'info'")
    info_messages = cursor.fetchone()[0]
    
    # Projetos
    cursor = conn.execute("SELECT project_name, issue_count FROM sentry_projects")
    projects = cursor.fetchall()
    
    # Problemas de MCP
    cursor = conn.execute("SELECT mcp_name, issue_type, description FROM mcp_issues")
    mcp_issues = cursor.fetchall()
    
    report = f"""
# Relatório de Documentação de Erros do MCP Sentry

## Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Estatísticas Gerais
- **Total de Issues:** {total_errors}
- **Erros Críticos:** {critical_errors}
- **Warnings:** {warnings}
- **Mensagens Info:** {info_messages}

## Projetos
"""
    
    for project_name, issue_count in projects:
        report += f"- **{project_name}:** {issue_count} issues\n"
    
    report += "\n## Problemas de Infraestrutura MCP\n"
    
    for mcp_name, issue_type, description in mcp_issues:
        report += f"- **{mcp_name} ({issue_type}):** {description}\n"
    
    return report

def main():
    """Função principal."""
    
    # Usar o banco de dados local para documentação
    db_path = "sentry_errors_documentation.db"
    
    try:
        conn = sqlite3.connect(db_path)
        
        print("🔄 Criando schema do banco de dados...")
        create_database_schema(conn)
        
        print("📝 Inserindo erros do Sentry...")
        insert_sentry_errors(conn, SENTRY_ERRORS_DATA)
        
        print("⚠️ Documentando problemas de MCP...")
        insert_mcp_issues(conn)
        
        print("📊 Gerando relatório...")
        report = generate_report(conn)
        
        # Salvar relatório em arquivo
        with open("SENTRY_ERRORS_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("✅ Documentação concluída!")
        print(f"📁 Banco de dados: {db_path}")
        print("📄 Relatório: SENTRY_ERRORS_REPORT.md")
        
        # Mostrar algumas consultas úteis
        print("\n🔍 Consultas úteis:")
        print("SELECT * FROM sentry_errors WHERE error_level = 'error';")
        print("SELECT * FROM mcp_issues WHERE status = 'open';")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main() 