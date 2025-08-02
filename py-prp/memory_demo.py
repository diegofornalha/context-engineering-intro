#!/usr/bin/env python3
"""
Demonstração do Sistema de Memória Turso MCP

Este script demonstra como usar o banco de dados Turso para criar
um sistema de memória persistente para agentes de IA.
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any

class TursoMemorySystem:
    """
    Sistema de memória usando Turso Database
    """
    
    def __init__(self, database_url: str, auth_token: str):
        """
        Inicializa o sistema de memória
        
        Args:
            database_url: URL do banco de dados Turso
            auth_token: Token de autenticação
        """
        self.database_url = database_url
        self.auth_token = auth_token
        # Para demonstração, usaremos SQLite local
        # Em produção, usaríamos o cliente Turso
        self.db_path = "memory_demo.db"
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabelas
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                project_id TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tools_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                success BOOLEAN DEFAULT 1,
                error_message TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_conversation(self, session_id: str, message: str, response: str = None, 
                        user_id: str = None, context: str = None) -> int:
        """
        Adiciona uma conversa à memória
        
        Args:
            session_id: ID da sessão
            message: Mensagem do usuário
            response: Resposta da IA
            user_id: ID do usuário
            context: Contexto adicional
            
        Returns:
            ID da conversa inserida
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (session_id, user_id, message, response, context)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_id, message, response, context))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def get_conversations(self, session_id: str = None, limit: int = 10) -> List[Dict]:
        """
        Recupera conversas da memória
        
        Args:
            session_id: ID da sessão (opcional)
            limit: Número máximo de conversas
            
        Returns:
            Lista de conversas
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM conversations"
        params = []
        
        if session_id:
            query += " WHERE session_id = ?"
            params.append(session_id)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conversations = []
        for row in rows:
            conversations.append({
                'id': row[0],
                'session_id': row[1],
                'user_id': row[2],
                'message': row[3],
                'response': row[4],
                'timestamp': row[5],
                'context': row[6],
                'metadata': row[7]
            })
        
        conn.close()
        return conversations
    
    def add_knowledge(self, topic: str, content: str, source: str = None, 
                     tags: str = None) -> int:
        """
        Adiciona conhecimento à base de conhecimento
        
        Args:
            topic: Tópico do conhecimento
            content: Conteúdo do conhecimento
            source: Fonte do conhecimento
            tags: Tags separadas por vírgula
            
        Returns:
            ID do conhecimento inserido
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, tags)
            VALUES (?, ?, ?, ?)
        """, (topic, content, source, tags))
        
        knowledge_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return knowledge_id
    
    def search_knowledge(self, query: str, tags: str = None, limit: int = 10) -> List[Dict]:
        """
        Pesquisa na base de conhecimento
        
        Args:
            query: Termo de pesquisa
            tags: Tags para filtrar
            limit: Número máximo de resultados
            
        Returns:
            Lista de conhecimentos encontrados
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_query = "SELECT * FROM knowledge_base WHERE topic LIKE ? OR content LIKE ?"
        params = [f"%{query}%", f"%{query}%"]
        
        if tags:
            search_query += " AND tags LIKE ?"
            params.append(f"%{tags}%")
        
        search_query += " ORDER BY priority DESC, created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(search_query, params)
        rows = cursor.fetchall()
        
        knowledge = []
        for row in rows:
            knowledge.append({
                'id': row[0],
                'topic': row[1],
                'content': row[2],
                'source': row[3],
                'created_at': row[4],
                'updated_at': row[5],
                'tags': row[6],
                'priority': row[7]
            })
        
        conn.close()
        return knowledge
    
    def add_task(self, title: str, description: str = None, priority: int = 1,
                 context: str = None) -> int:
        """
        Adiciona uma tarefa
        
        Args:
            title: Título da tarefa
            description: Descrição da tarefa
            priority: Prioridade (1-5)
            context: Contexto da tarefa
            
        Returns:
            ID da tarefa inserida
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, context)
            VALUES (?, ?, ?, ?)
        """, (title, description, priority, context))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    def get_tasks(self, status: str = None, limit: int = 10) -> List[Dict]:
        """
        Recupera tarefas
        
        Args:
            status: Status das tarefas (pending, completed, etc.)
            limit: Número máximo de tarefas
            
        Returns:
            Lista de tarefas
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM tasks"
        params = []
        
        if status:
            query += " WHERE status = ?"
            params.append(status)
        
        query += " ORDER BY priority DESC, created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        tasks = []
        for row in rows:
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'status': row[3],
                'priority': row[4],
                'created_at': row[5],
                'completed_at': row[6],
                'context': row[7],
                'assigned_to': row[8]
            })
        
        conn.close()
        return tasks

def demo_memory_system():
    """Demonstra o uso do sistema de memória"""
    
    print("🧠 Sistema de Memória Turso MCP - Demonstração")
    print("=" * 50)
    
    # Inicializar sistema de memória
    memory = TursoMemorySystem(
        database_url="libsql://context-memory-diegofornalha.aws-us-east-1.turso.io",
        auth_token="demo-token"
    )
    
    # 1. Adicionar conversas
    print("\n1. 📝 Adicionando conversas...")
    session_id = "demo-session-1"
    
    memory.add_conversation(
        session_id=session_id,
        message="Olá! Como você está?",
        response="Olá! Estou funcionando perfeitamente. Como posso ajudá-lo?",
        user_id="user-1"
    )
    
    memory.add_conversation(
        session_id=session_id,
        message="Preciso de ajuda com Python",
        response="Claro! Python é uma linguagem excelente. Que tipo de ajuda você precisa?",
        user_id="user-1"
    )
    
    # 2. Recuperar conversas
    print("\n2. 📖 Recuperando conversas...")
    conversations = memory.get_conversations(session_id=session_id)
    
    for conv in conversations:
        print(f"  [{conv['timestamp']}] {conv['message']}")
        print(f"  Resposta: {conv['response']}")
        print()
    
    # 3. Adicionar conhecimento
    print("\n3. 📚 Adicionando conhecimento...")
    memory.add_knowledge(
        topic="Python Programming",
        content="Python é uma linguagem de programação de alto nível, interpretada e orientada a objetos.",
        source="documentation",
        tags="python,programming,language"
    )
    
    memory.add_knowledge(
        topic="MCP Protocol",
        content="Model Context Protocol (MCP) é um protocolo para comunicação entre LLMs e ferramentas externas.",
        source="research",
        tags="mcp,protocol,llm,ai"
    )
    
    # 4. Pesquisar conhecimento
    print("\n4. 🔍 Pesquisando conhecimento...")
    knowledge = memory.search_knowledge("Python")
    
    for item in knowledge:
        print(f"  Tópico: {item['topic']}")
        print(f"  Conteúdo: {item['content']}")
        print(f"  Tags: {item['tags']}")
        print()
    
    # 5. Adicionar tarefas
    print("\n5. ✅ Adicionando tarefas...")
    memory.add_task(
        title="Implementar sistema de memória",
        description="Criar sistema de memória persistente usando Turso",
        priority=1,
        context="projeto-mcp"
    )
    
    memory.add_task(
        title="Documentar API",
        description="Criar documentação da API de memória",
        priority=2,
        context="projeto-mcp"
    )
    
    # 6. Listar tarefas
    print("\n6. 📋 Listando tarefas...")
    tasks = memory.get_tasks()
    
    for task in tasks:
        print(f"  [{task['priority']}] {task['title']} - {task['status']}")
        print(f"  Descrição: {task['description']}")
        print()
    
    print("✅ Demonstração concluída!")
    print("\n💡 Este sistema pode ser usado para:")
    print("  - Manter histórico de conversas")
    print("  - Armazenar conhecimento aprendido")
    print("  - Gerenciar tarefas e projetos")
    print("  - Manter contexto entre sessões")

if __name__ == "__main__":
    demo_memory_system() 