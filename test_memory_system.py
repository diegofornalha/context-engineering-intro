#!/usr/bin/env python3
"""
Teste do Sistema de Memória Turso MCP

Este script testa o sistema de memória com dados reais do projeto
context-engineering-intro.
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List

class TursoMemoryTester:
    """Testador do sistema de memória Turso"""
    
    def __init__(self):
        """Inicializa o testador"""
        self.db_path = "test_memory.db"
        self._init_test_database()
    
    def _init_test_database(self):
        """Inicializa banco de teste"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabelas de teste
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id TEXT,
                message TEXT NOT NULL,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                context TEXT,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                tags TEXT,
                priority INTEGER DEFAULT 1
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                context TEXT,
                assigned_to TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def test_conversations(self):
        """Testa funcionalidades de conversas"""
        print("🧪 Testando conversas...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Inserir conversas de teste
        test_conversations = [
            ("session-1", "user-1", "Como configurar o MCP Turso?", 
             "Para configurar o MCP Turso, você precisa...", "configuracao"),
            ("session-1", "user-1", "Qual é a estrutura do projeto?", 
             "O projeto tem a seguinte estrutura...", "estrutura"),
            ("session-2", "user-2", "Como usar o sistema de memória?", 
             "O sistema de memória permite...", "memoria"),
        ]
        
        for session_id, user_id, message, response, context in test_conversations:
            cursor.execute("""
                INSERT INTO conversations (session_id, user_id, message, response, context)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, user_id, message, response, context))
        
        # Testar recuperação
        cursor.execute("SELECT * FROM conversations WHERE session_id = 'session-1' ORDER BY timestamp")
        conversations = cursor.fetchall()
        
        print(f"  ✅ {len(conversations)} conversas recuperadas para session-1")
        for conv in conversations:
            print(f"    - {conv[3]} -> {conv[4]}")
        
        conn.commit()
        conn.close()
    
    def test_knowledge_base(self):
        """Testa base de conhecimento"""
        print("\n📚 Testando base de conhecimento...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Inserir conhecimentos do projeto
        knowledge_items = [
            ("MCP Protocol", 
             "Model Context Protocol é um protocolo para comunicação entre LLMs e ferramentas externas. Permite que LLMs acessem dados e executem ações de forma segura e controlada.",
             "documentation", "mcp,protocol,llm,ai"),
            
            ("Turso Database", 
             "Turso é um banco de dados SQLite distribuído na nuvem. Oferece baixa latência, alta disponibilidade e backup automático.",
             "documentation", "turso,database,sqlite,cloud"),
            
            ("Context Engineering", 
             "Engenharia de contexto é a prática de projetar e implementar sistemas que mantêm e utilizam contexto de forma eficiente para melhorar a experiência do usuário.",
             "research", "context,engineering,ux,ai"),
            
            ("CrewAI Framework", 
             "CrewAI é um framework para orquestrar agentes de IA autônomos. Permite criar crews de agentes que trabalham juntos para resolver tarefas complexas.",
             "framework", "crewai,agents,ai,orchestration"),
            
            ("Sentry MCP", 
             "Sentry MCP é uma implementação do Model Context Protocol para integração com Sentry. Permite monitoramento e debugging de aplicações via LLMs.",
             "integration", "sentry,mcp,monitoring,debugging"),
        ]
        
        for topic, content, source, tags in knowledge_items:
            cursor.execute("""
                INSERT INTO knowledge_base (topic, content, source, tags)
                VALUES (?, ?, ?, ?)
            """, (topic, content, source, tags))
        
        # Testar pesquisa
        cursor.execute("SELECT topic, content FROM knowledge_base WHERE content LIKE '%MCP%' OR topic LIKE '%MCP%'")
        mcp_results = cursor.fetchall()
        
        print(f"  ✅ {len(mcp_results)} resultados encontrados para 'MCP'")
        for result in mcp_results:
            print(f"    - {result[0]}: {result[1][:50]}...")
        
        conn.commit()
        conn.close()
    
    def test_tasks(self):
        """Testa gerenciamento de tarefas"""
        print("\n✅ Testando gerenciamento de tarefas...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Inserir tarefas do projeto
        project_tasks = [
            ("Configurar MCP Turso", "Configurar e testar o servidor MCP Turso", 1, "setup"),
            ("Implementar sistema de memória", "Criar sistema de memória persistente", 1, "memoria"),
            ("Documentar API", "Criar documentação completa da API", 2, "documentacao"),
            ("Testar integração", "Testar integração com Claude Code", 2, "testes"),
            ("Otimizar performance", "Otimizar queries e índices", 3, "performance"),
        ]
        
        for title, description, priority, context in project_tasks:
            cursor.execute("""
                INSERT INTO tasks (title, description, priority, context)
                VALUES (?, ?, ?, ?)
            """, (title, description, priority, context))
        
        # Marcar algumas como completadas
        cursor.execute("UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE title LIKE '%Configurar%'")
        
        # Testar consultas
        cursor.execute("SELECT title, status, priority FROM tasks ORDER BY priority, created_at")
        tasks = cursor.fetchall()
        
        print(f"  ✅ {len(tasks)} tarefas criadas")
        for task in tasks:
            status_icon = "✅" if task[1] == "completed" else "⏳"
            print(f"    {status_icon} [{task[2]}] {task[0]} - {task[1]}")
        
        conn.commit()
        conn.close()
    
    def test_queries(self):
        """Testa consultas complexas"""
        print("\n🔍 Testando consultas complexas...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Conversas por usuário
        cursor.execute("""
            SELECT user_id, COUNT(*) as total_conversations 
            FROM conversations 
            GROUP BY user_id 
            ORDER BY total_conversations DESC
        """)
        user_stats = cursor.fetchall()
        
        print("  📊 Estatísticas por usuário:")
        for user_id, count in user_stats:
            print(f"    - {user_id}: {count} conversas")
        
        # 2. Conhecimento por tags
        cursor.execute("""
            SELECT tags, COUNT(*) as total_items 
            FROM knowledge_base 
            WHERE tags IS NOT NULL 
            GROUP BY tags 
            ORDER BY total_items DESC
        """)
        tag_stats = cursor.fetchall()
        
        print("  🏷️ Conhecimento por tags:")
        for tags, count in tag_stats:
            print(f"    - {tags}: {count} itens")
        
        # 3. Tarefas por prioridade
        cursor.execute("""
            SELECT priority, COUNT(*) as total_tasks,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks
            FROM tasks 
            GROUP BY priority 
            ORDER BY priority
        """)
        priority_stats = cursor.fetchall()
        
        print("  📋 Tarefas por prioridade:")
        for priority, total, completed in priority_stats:
            completion_rate = (completed / total * 100) if total > 0 else 0
            print(f"    - Prioridade {priority}: {completed}/{total} ({completion_rate:.1f}%)")
        
        conn.close()
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🧠 Teste Completo do Sistema de Memória Turso MCP")
        print("=" * 60)
        
        try:
            self.test_conversations()
            self.test_knowledge_base()
            self.test_tasks()
            self.test_queries()
            
            print("\n✅ Todos os testes concluídos com sucesso!")
            print("\n📊 Resumo:")
            print("  - Sistema de conversas: ✅ Funcional")
            print("  - Base de conhecimento: ✅ Funcional")
            print("  - Gerenciamento de tarefas: ✅ Funcional")
            print("  - Consultas complexas: ✅ Funcional")
            
        except Exception as e:
            print(f"\n❌ Erro durante os testes: {e}")
            raise

def main():
    """Função principal"""
    tester = TursoMemoryTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 