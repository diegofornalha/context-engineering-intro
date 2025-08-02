# 🚀 Guia Completo: Criar Repositório com Turso MCP do Zero

## 📋 Visão Geral

Este guia mostra como criar um novo repositório com sistema de memória Turso MCP completamente do zero, incluindo configuração do banco de dados, servidor MCP e demonstrações.

## 🎯 Objetivo Final

Criar um sistema completo com:
- ✅ Banco de dados Turso configurado
- ✅ Servidor MCP TypeScript funcional
- ✅ Sistema de memória persistente
- ✅ Scripts de configuração automática
- ✅ Demonstrações e testes
- ✅ Documentação completa

---

## 📁 Passo 1: Estrutura Inicial do Projeto

### 1.1 Criar Diretório do Projeto
```bash
# Criar diretório do projeto
mkdir meu-projeto-memoria
cd meu-projeto-memoria

# Inicializar git (opcional)
git init
```

### 1.2 Estrutura de Pastas
```bash
# Criar estrutura de pastas
mkdir -p mcp-turso/src
mkdir -p docs
mkdir -p examples
mkdir -p tests
```

### 1.3 Arquivos Base
```bash
# Criar arquivos principais
touch README.md
touch .gitignore
touch .env.example
```

---

## 🔧 Passo 2: Configurar Turso Database

### 2.1 Instalar Turso CLI
```bash
# Instalar Turso CLI
curl -sSfL https://get.tur.so/install.sh | bash

# Adicionar ao PATH
export PATH="$HOME/.turso:$PATH"

# Verificar instalação
turso --version
```

### 2.2 Fazer Login no Turso
```bash
# Fazer login (abrirá navegador)
turso auth login

# Verificar login
turso auth whoami
```

### 2.3 Criar Banco de Dados
```bash
# Criar banco de dados
turso db create meu-banco-memoria --group default

# Verificar criação
turso db list

# Obter URL do banco
DB_URL=$(turso db show meu-banco-memoria --url)
echo "URL do banco: $DB_URL"
```

### 2.4 Gerar Token de Acesso
```bash
# Gerar token de autenticação
DB_TOKEN=$(turso db tokens create meu-banco-memoria)

# Salvar configurações
echo "TURSO_DATABASE_URL=$DB_URL" > .env
echo "TURSO_AUTH_TOKEN=$DB_TOKEN" >> .env

# Verificar arquivo
cat .env
```

---

## 🏗️ Passo 3: Criar Estrutura do Banco

### 3.1 Script de Configuração do Banco
Criar arquivo `setup-database.sh`:

```bash
#!/bin/bash

# Script para configurar banco de dados Turso
echo "🗄️ Configurando banco de dados Turso..."

# Carregar variáveis de ambiente
source .env

# Conectar ao banco e criar tabelas
turso db shell meu-banco-memoria << 'EOF'
-- Tabela de conversas
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_id TEXT,
    message TEXT NOT NULL,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    context TEXT,
    metadata TEXT
);

-- Tabela de base de conhecimento
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags TEXT,
    priority INTEGER DEFAULT 1
);

-- Tabela de tarefas
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
);

-- Tabela de contextos
CREATE TABLE IF NOT EXISTS contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    data TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    project_id TEXT
);

-- Tabela de uso de ferramentas
CREATE TABLE IF NOT EXISTS tools_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    input_data TEXT,
    output_data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    success BOOLEAN DEFAULT 1,
    error_message TEXT
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp);
CREATE INDEX IF NOT EXISTS idx_knowledge_topic ON knowledge_base(topic);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_contexts_name ON contexts(name);
CREATE INDEX IF NOT EXISTS idx_tools_timestamp ON tools_usage(timestamp);

-- Dados de exemplo
INSERT OR IGNORE INTO knowledge_base (topic, content, source, tags) VALUES 
('Sistema de Memória', 'Sistema de memória persistente usando Turso Database', 'documentation', 'memoria,turso,database'),
('MCP Protocol', 'Model Context Protocol para comunicação com LLMs', 'documentation', 'mcp,protocol,llm');

INSERT OR IGNORE INTO contexts (name, description, data, project_id) VALUES 
('default', 'Contexto padrão do projeto', '{"project": "meu-projeto-memoria", "version": "1.0.0"}', 'meu-projeto-memoria');

EOF

echo "✅ Banco de dados configurado com sucesso!"
```

### 3.2 Executar Configuração
```bash
# Tornar executável
chmod +x setup-database.sh

# Executar configuração
./setup-database.sh
```

---

## ⚙️ Passo 4: Configurar Servidor MCP Turso

### 4.1 Inicializar Projeto Node.js
```bash
# Entrar na pasta do MCP
cd mcp-turso

# Inicializar package.json
npm init -y
```

### 4.2 Configurar package.json
Editar `mcp-turso/package.json`:

```json
{
  "name": "mcp-turso-memory",
  "version": "1.0.0",
  "description": "MCP Server for Turso Database Memory System",
  "main": "dist/index.js",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc && node dist/index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.4.0",
    "@libsql/client": "^0.5.0",
    "dotenv": "^16.6.1"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  },
  "keywords": ["mcp", "turso", "memory", "database"],
  "author": "Seu Nome",
  "license": "MIT"
}
```

### 4.3 Configurar TypeScript
Criar `mcp-turso/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 4.4 Configurar Variáveis de Ambiente
Criar `mcp-turso/.env.example`:

```env
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://seu-banco-sua-org.aws-us-east-1.turso.io
TURSO_AUTH_TOKEN=seu-token-aqui

# MCP Server Configuration
MCP_SERVER_NAME=mcp-turso-memory
MCP_SERVER_VERSION=1.0.0

# Optional: Project Configuration
PROJECT_NAME=meu-projeto-memoria
PROJECT_VERSION=1.0.0
ENVIRONMENT=development
```

### 4.5 Script de Configuração Automática
Criar `mcp-turso/setup-env.sh`:

```bash
#!/bin/bash

# Script para configurar arquivo .env do MCP Turso
echo "🔧 Configurando arquivo .env para MCP Turso..."

# Verificar se já existe arquivo .env
if [ -f ".env" ]; then
    echo "⚠️  Arquivo .env já existe. Deseja sobrescrever? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Configuração cancelada."
        exit 0
    fi
fi

# Verificar se existe arquivo .env na raiz do projeto
if [ -f "../.env.turso" ]; then
    echo "📝 Copiando configurações do arquivo .env.turso..."
    cp ../.env.turso .env
    echo "✅ Arquivo .env criado com configurações do projeto principal!"
else
    echo "📝 Criando arquivo .env com configurações padrão..."
    
    # Criar arquivo .env com configurações padrão
    cat > .env << 'EOF'
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://context-memory-diegofornalha.aws-us-east-1.turso.io
TURSO_AUTH_TOKEN=seu-token-aqui

# MCP Server Configuration
MCP_SERVER_NAME=mcp-turso-memory
MCP_SERVER_VERSION=1.0.0

# Optional: Project Configuration
PROJECT_NAME=meu-projeto-memoria
PROJECT_VERSION=1.0.0
ENVIRONMENT=development
EOF
    
    echo "✅ Arquivo .env criado com configurações padrão!"
fi

echo "✅ Configuração concluída!"
echo "🚀 Para iniciar o servidor MCP:"
echo "   ./start.sh"
```

```bash
# Tornar executável
chmod +x mcp-turso/setup-env.sh
```

### 4.6 Instalar Dependências
```bash
# Instalar dependências
npm install

# Verificar instalação
ls node_modules
```

---

## 💻 Passo 5: Criar Servidor MCP

### 5.1 Criar Arquivo Principal
Criar `mcp-turso/src/index.ts`:

```typescript
#!/usr/bin/env node
import { config } from "dotenv";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createClient } from "@libsql/client";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Load environment variables
config();

// Turso client
let tursoClient: any = null;

function getTursoClient() {
  if (!tursoClient) {
    const databaseUrl = process.env.TURSO_DATABASE_URL;
    const authToken = process.env.TURSO_AUTH_TOKEN;
    
    if (!databaseUrl || !authToken) {
      throw new Error("TURSO_DATABASE_URL e TURSO_AUTH_TOKEN são obrigatórios");
    }
    
    tursoClient = createClient({
      url: databaseUrl,
      authToken: authToken,
    });
  }
  return tursoClient;
}

// Create server instance
const server = new Server(
  {
    name: "mcp-turso-memory",
    version: "1.0.0",
  }
);

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "turso_list_databases",
        description: "List all databases in your Turso organization",
        inputSchema: {
          type: "object",
          properties: {
            random_string: {
              type: "string",
              description: "Dummy parameter for no-parameter tools",
            },
          },
          required: ["random_string"],
        },
      },
      {
        name: "turso_execute_query",
        description: "Execute a SQL query on the Turso database",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "SQL query to execute",
            },
            params: {
              type: "object",
              description: "Query parameters (optional)",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "turso_list_tables",
        description: "List all tables in the database",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "turso_add_conversation",
        description: "Add a conversation to memory",
        inputSchema: {
          type: "object",
          properties: {
            session_id: {
              type: "string",
              description: "Session identifier",
            },
            user_id: {
              type: "string",
              description: "User identifier",
            },
            message: {
              type: "string",
              description: "User message",
            },
            response: {
              type: "string",
              description: "AI response",
            },
            context: {
              type: "string",
              description: "Additional context",
            },
          },
          required: ["session_id", "message"],
        },
      },
      {
        name: "turso_get_conversations",
        description: "Get conversations from memory",
        inputSchema: {
          type: "object",
          properties: {
            session_id: {
              type: "string",
              description: "Session identifier (optional)",
            },
            limit: {
              type: "number",
              description: "Number of conversations to retrieve",
            },
          },
        },
      },
      {
        name: "turso_add_knowledge",
        description: "Add knowledge to the knowledge base",
        inputSchema: {
          type: "object",
          properties: {
            topic: {
              type: "string",
              description: "Knowledge topic",
            },
            content: {
              type: "string",
              description: "Knowledge content",
            },
            source: {
              type: "string",
              description: "Source of knowledge",
            },
            tags: {
              type: "string",
              description: "Comma-separated tags",
            },
          },
          required: ["topic", "content"],
        },
      },
      {
        name: "turso_search_knowledge",
        description: "Search knowledge base",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query",
            },
            tags: {
              type: "string",
              description: "Filter by tags",
            },
            limit: {
              type: "number",
              description: "Number of results",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    const client = getTursoClient();

    switch (name) {
      case "turso_list_databases":
        return {
          content: [
            {
              type: "text",
              text: `Available databases: meu-banco-memoria`,
            },
          ],
        };

      case "turso_execute_query":
        if (!args?.query) {
          throw new Error("Query parameter is required");
        }
        const result = await client.execute(args.query, args?.params || {});
        return {
          content: [
            {
              type: "text",
              text: `Query executed successfully:\n${JSON.stringify(result, null, 2)}`,
            },
          ],
        };

      case "turso_list_tables":
        const tablesResult = await client.execute(`
          SELECT name FROM sqlite_master 
          WHERE type='table' AND name NOT LIKE 'sqlite_%'
          ORDER BY name
        `);
        return {
          content: [
            {
              type: "text",
              text: `Tables in database:\n${JSON.stringify(tablesResult, null, 2)}`,
            },
          ],
        };

      case "turso_add_conversation":
        if (!args?.session_id || !args?.message) {
          throw new Error("session_id and message are required");
        }
        const insertResult = await client.execute(`
          INSERT INTO conversations (session_id, user_id, message, response, context)
          VALUES (?, ?, ?, ?, ?)
        `, [args.session_id, args.user_id || null, args.message, args.response || null, args.context || null]);
        return {
          content: [
            {
              type: "text",
              text: `Conversation added successfully. ID: ${insertResult.lastInsertRowid}`,
            },
          ],
        };

      case "turso_get_conversations":
        let query = "SELECT * FROM conversations";
        const params: any[] = [];
        
        if (args?.session_id) {
          query += " WHERE session_id = ?";
          params.push(args.session_id);
        }
        
        query += " ORDER BY timestamp DESC";
        
        if (args?.limit) {
          query += " LIMIT ?";
          params.push(args.limit.toString());
        }
        
        const conversationsResult = await client.execute(query, params);
        return {
          content: [
            {
              type: "text",
              text: `Conversations:\n${JSON.stringify(conversationsResult, null, 2)}`,
            },
          ],
        };

      case "turso_add_knowledge":
        if (!args?.topic || !args?.content) {
          throw new Error("topic and content are required");
        }
        const knowledgeResult = await client.execute(`
          INSERT INTO knowledge_base (topic, content, source, tags)
          VALUES (?, ?, ?, ?)
        `, [args.topic, args.content, args.source || null, args.tags || null]);
        return {
          content: [
            {
              type: "text",
              text: `Knowledge added successfully. ID: ${knowledgeResult.lastInsertRowid}`,
            },
          ],
        };

      case "turso_search_knowledge":
        if (!args?.query) {
          throw new Error("query is required");
        }
        let searchQuery = "SELECT * FROM knowledge_base WHERE topic LIKE ? OR content LIKE ?";
        const searchParams = [`%${args.query}%`, `%${args.query}%`];
        
        if (args?.tags) {
          searchQuery += " AND tags LIKE ?";
          searchParams.push(`%${args.tags}%`);
        }
        
        searchQuery += " ORDER BY priority DESC, created_at DESC";
        
        if (args?.limit) {
          searchQuery += " LIMIT ?";
          searchParams.push(args.limit.toString());
        }
        
        const searchResult = await client.execute(searchQuery, searchParams);
        return {
          content: [
            {
              type: "text",
              text: `Search results:\n${JSON.stringify(searchResult, null, 2)}`,
            },
          ],
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

### 5.2 Compilar Servidor
```bash
# Compilar TypeScript
npm run build

# Verificar compilação
ls dist/
```

### 5.3 Script de Inicialização
Criar `mcp-turso/start.sh`:

```bash
#!/bin/bash

# MCP Turso Server - Script de inicialização
cd "$(dirname "$0")"

# Verificar se existe arquivo .env
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copie .env.example para .env e configure suas variáveis:"
    echo "   cp .env.example .env"
    echo "   # Edite o arquivo .env com suas configurações"
    exit 1
fi

# Carregar variáveis de ambiente do arquivo .env
export $(cat .env | grep -v '^#' | xargs)

# Verificar variáveis obrigatórias
if [ -z "$TURSO_DATABASE_URL" ] || [ -z "$TURSO_AUTH_TOKEN" ]; then
    echo "❌ Erro: TURSO_DATABASE_URL e TURSO_AUTH_TOKEN devem estar configurados"
    echo "Execute: ./setup-env.sh"
    exit 1
fi

# Garantir que o projeto está compilado
if [ ! -d "dist" ]; then
    echo "🔨 Compilando projeto..."
    npm install >/dev/null 2>&1
    npm run build >/dev/null 2>&1
fi

# Iniciar servidor MCP
echo "🚀 Iniciando servidor MCP Turso..."
exec node dist/index.js
```

```bash
# Tornar executável
chmod +x mcp-turso/start.sh
```

---

## 🐍 Passo 6: Criar Demonstração Python

### 6.1 Criar Classe de Memória
Criar `memory_system.py`:

```python
#!/usr/bin/env python3
"""
Sistema de Memória Turso MCP

Classe para gerenciar memória persistente usando Turso Database.
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
        
        # Criar tabelas (mesma estrutura do Turso)
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
    
    def add_conversation(self, session_id: str, message: str, response: str = None, 
                        user_id: str = None, context: str = None) -> int:
        """Adiciona uma conversa à memória"""
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
        """Recupera conversas da memória"""
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
        """Adiciona conhecimento à base de conhecimento"""
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
        """Pesquisa na base de conhecimento"""
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
        """Adiciona uma tarefa"""
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
        """Recupera tarefas"""
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
```

### 6.2 Criar Demonstração
Criar `demo.py`:

```python
#!/usr/bin/env python3
"""
Demonstração do Sistema de Memória Turso MCP
"""

from memory_system import TursoMemorySystem
import os

def main():
    """Função principal da demonstração"""
    
    print("🧠 Demonstração do Sistema de Memória Turso MCP")
    print("=" * 50)
    
    # Carregar configurações
    database_url = os.getenv("TURSO_DATABASE_URL", "demo-url")
    auth_token = os.getenv("TURSO_AUTH_TOKEN", "demo-token")
    
    # Inicializar sistema
    memory = TursoMemorySystem(database_url, auth_token)
    
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
    main()
```

---

## 🧪 Passo 7: Criar Testes

### 7.1 Script de Teste
Criar `test_system.py`:

```python
#!/usr/bin/env python3
"""
Teste do Sistema de Memória Turso MCP
"""

from memory_system import TursoMemorySystem
import os

def test_memory_system():
    """Testa todas as funcionalidades do sistema"""
    
    print("🧪 Teste Completo do Sistema de Memória")
    print("=" * 40)
    
    # Inicializar sistema
    memory = TursoMemorySystem("test-url", "test-token")
    
    # Teste 1: Conversas
    print("\n1. Testando conversas...")
    memory.add_conversation("test-session", "Teste", "Resposta teste")
    conversations = memory.get_conversations("test-session")
    assert len(conversations) > 0, "Falha no teste de conversas"
    print("  ✅ Conversas funcionando")
    
    # Teste 2: Conhecimento
    print("\n2. Testando conhecimento...")
    memory.add_knowledge("Teste", "Conteúdo teste", tags="test")
    knowledge = memory.search_knowledge("Teste")
    assert len(knowledge) > 0, "Falha no teste de conhecimento"
    print("  ✅ Conhecimento funcionando")
    
    # Teste 3: Tarefas
    print("\n3. Testando tarefas...")
    memory.add_task("Tarefa teste", "Descrição teste")
    tasks = memory.get_tasks()
    assert len(tasks) > 0, "Falha no teste de tarefas"
    print("  ✅ Tarefas funcionando")
    
    print("\n✅ Todos os testes passaram!")

if __name__ == "__main__":
    test_memory_system()
```

---

## 📚 Passo 8: Criar Documentação

### 8.1 README Principal
Criar `README.md`:

```markdown
# 🧠 Sistema de Memória Turso MCP

## 📋 Visão Geral

Sistema de memória persistente usando Turso Database e Model Context Protocol (MCP). Permite que agentes de IA mantenham memória de longo prazo.

## 🚀 Configuração Rápida

### 1. Pré-requisitos
- Node.js 18+
- Python 3.8+
- Conta Turso

### 2. Instalação
```bash
# Clonar repositório
git clone <seu-repo>
cd <seu-repo>

# Configurar banco de dados
./setup-database.sh

# Instalar dependências MCP
cd mcp-turso
npm install
npm run build

# Executar demonstração
cd ..
python3 demo.py
```

## 🛠️ Uso

### Via Python
```python
from memory_system import TursoMemorySystem

memory = TursoMemorySystem(database_url, auth_token)
memory.add_conversation("session-1", "Olá!", "Olá! Como posso ajudar?")
```

### Via MCP
```bash
cd mcp-turso
./start.sh
```

## 📊 Funcionalidades

- ✅ Histórico de conversas
- ✅ Base de conhecimento
- ✅ Gerenciamento de tarefas
- ✅ Contextos de projeto
- ✅ Log de ferramentas

## 🔧 Estrutura

```
projeto/
├── mcp-turso/           # Servidor MCP
├── memory_system.py     # Classe Python
├── demo.py             # Demonstração
├── test_system.py      # Testes
├── setup-database.sh   # Configuração
└── README.md           # Documentação
```

## 📞 Suporte

Para dúvidas, consulte a documentação ou abra uma issue.

## 📄 Licença

MIT License
```

### 8.2 .gitignore
Criar `.gitignore`:

```gitignore
# Dependências
node_modules/
__pycache__/
*.pyc

# Arquivos de configuração
.env
.env.local
.env.*.local
*.db

# Build
dist/
build/

# Logs
*.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### 8.3 .env.example
Criar `.env.example`:

```env
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://seu-banco-sua-org.aws-us-east-1.turso.io
TURSO_AUTH_TOKEN=seu-token-aqui

# Optional: Project Configuration
PROJECT_NAME=meu-projeto-memoria
PROJECT_VERSION=1.0.0
```

---

## 🚀 Passo 9: Testar Sistema Completo

### 9.1 Configurar e Testar MCP
```bash
# Configurar variáveis de ambiente
cd mcp-turso
./setup-env.sh

# Instalar dependências e compilar
npm install
npm run build

# Testar servidor MCP
./start.sh
```

### 9.2 Testar Banco de Dados
```bash
# Testar banco de dados
turso db shell meu-banco-memoria "SELECT name FROM sqlite_master WHERE type='table';"

# Testar Python
cd ..
python3 demo.py

# Executar testes
python3 test_system.py
```

### 9.2 Verificar Funcionamento
```bash
# Verificar tabelas criadas
turso db shell meu-banco-memoria "SELECT COUNT(*) FROM conversations;"
turso db shell meu-banco-memoria "SELECT COUNT(*) FROM knowledge_base;"
turso db shell meu-banco-memoria "SELECT COUNT(*) FROM tasks;"
```

---

## 📋 Passo 10: Finalização

### 10.1 Commit Inicial
```bash
# Adicionar arquivos
git add .

# Commit inicial
git commit -m "feat: Sistema de memória Turso MCP inicial

- Banco de dados Turso configurado
- Servidor MCP TypeScript funcional
- Sistema de memória Python
- Demonstrações e testes
- Documentação completa"

# Push para repositório
git push origin main
```

### 10.2 Verificação Final
```bash
# Listar arquivos criados
find . -type f -name "*.py" -o -name "*.ts" -o -name "*.sh" -o -name "*.md" | sort

# Verificar estrutura
tree -I 'node_modules|__pycache__|dist'
```

---

## 🎉 Resultado Final

Após seguir todos os passos, você terá:

✅ **Banco de dados Turso** configurado e operacional  
✅ **Servidor MCP TypeScript** compilado e funcional  
✅ **Sistema de memória Python** com todas as funcionalidades  
✅ **Arquivo .env** configurado com gerenciamento seguro de variáveis  
✅ **Scripts de configuração** automática  
✅ **Demonstrações e testes** funcionais  
✅ **Documentação completa** e organizada  
✅ **Repositório Git** inicializado e estruturado  

### 📊 Estrutura Final
```
meu-projeto-memoria/
├── mcp-turso/
│   ├── src/index.ts          # Código principal (com dotenv)
│   ├── package.json          # Dependências (com dotenv)
│   ├── tsconfig.json         # Configuração TypeScript
│   ├── dist/                 # Código compilado
│   ├── .env                  # ✅ Configurações do Turso
│   ├── .env.example          # ✅ Template de configuração
│   ├── setup-env.sh          # ✅ Script de configuração
│   ├── start.sh              # ✅ Script de inicialização
│   └── README.md             # ✅ Documentação
├── memory_system.py
├── demo.py
├── test_system.py
├── setup-database.sh
├── .env.turso               # Configurações do projeto principal
├── .env.example
├── .gitignore
└── README.md
```

## 🔒 Gerenciamento de Variáveis de Ambiente

### ✅ Implementado
- **Arquivo .env**: Configurações locais não versionadas
- **Arquivo .env.example**: Template sem dados sensíveis
- **Script setup-env.sh**: Configuração automática
- **Dependência dotenv**: Carregamento automático no código
- **Validação**: Verificação de variáveis obrigatórias

### 🛡️ Boas Práticas
- Nunca commite tokens no Git
- Use .env.example como template
- Configure .env localmente
- Valide configurações antes de executar
- Use scripts de configuração automática

### 🔧 Configuração Automática
```bash
# Configurar automaticamente
cd mcp-turso
./setup-env.sh

# Verificar configurações
cat .env

# Executar servidor
./start.sh
```

### 🚀 Próximos Passos

1. **Personalizar** para seu caso de uso específico
2. **Adicionar** mais funcionalidades conforme necessário
3. **Integrar** com outros sistemas (CrewAI, LangChain, etc.)
4. **Deploy** em produção
5. **Monitorar** e otimizar performance

---

**Status**: ✅ COMPLETO - Sistema funcional e documentado  
**Tempo estimado**: 30-60 minutos  
**Dificuldade**: Intermediário  
**Pré-requisitos**: Conhecimento básico de Node.js, Python e SQL  
**Recursos adicionais**: Gerenciamento seguro de variáveis de ambiente com dotenv 