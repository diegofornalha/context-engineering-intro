# 🎯 Guia Completo: Armazenamento de PRPs no Banco de Dados

## 📋 Visão Geral

Este guia explica a **melhor forma de guardar o contexto dos PRPs** (Product Requirement Prompts) no banco de dados `context-memory`, incluindo estrutura, operações e integração com o sistema MCP.

## 🏗️ Estrutura do Banco de Dados

### Tabelas Principais

#### 1. **`prps`** - Tabela Principal
```sql
-- Armazena os PRPs principais
CREATE TABLE prps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,                    -- Nome único do PRP
    title TEXT NOT NULL,                          -- Título descritivo
    description TEXT,                             -- Descrição geral
    objective TEXT NOT NULL,                      -- Objetivo principal
    justification TEXT,                           -- Por que é necessário
    
    -- Conteúdo estruturado em JSON
    context_data TEXT NOT NULL,                   -- JSON com contexto (arquivos, versões, exemplos)
    implementation_details TEXT NOT NULL,         -- JSON com detalhes de implementação
    validation_gates TEXT,                        -- JSON com portões de validação
    
    -- Metadados
    status TEXT DEFAULT 'draft',                  -- draft, active, completed, archived
    priority TEXT DEFAULT 'medium',               -- low, medium, high, critical
    complexity TEXT DEFAULT 'medium',             -- low, medium, high
    
    -- Relacionamentos
    parent_prp_id INTEGER,                        -- PRP pai (para dependências)
    related_prps TEXT,                            -- JSON array de IDs relacionados
    
    -- Controle de versão
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT,
    
    -- Busca e organização
    tags TEXT,                                    -- JSON array de tags
    search_text TEXT                              -- Texto para busca full-text
);
```

#### 2. **`prp_tasks`** - Tarefas Extraídas
```sql
-- Tarefas extraídas do PRP pelo LLM
CREATE TABLE prp_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,                      -- PRP pai
    task_name TEXT NOT NULL,                      -- Nome da tarefa
    description TEXT,                             -- Descrição detalhada
    task_type TEXT DEFAULT 'feature',             -- feature, bugfix, refactor, test, docs, setup
    
    -- Prioridade e estimativa
    priority TEXT DEFAULT 'medium',
    estimated_hours REAL,
    complexity TEXT DEFAULT 'medium',
    
    -- Status e progresso
    status TEXT DEFAULT 'pending',                -- pending, in_progress, review, completed, blocked
    progress INTEGER DEFAULT 0,                   -- 0-100%
    
    -- Dependências
    dependencies TEXT,                            -- JSON array de IDs de tarefas dependentes
    blockers TEXT,                                -- JSON array de IDs de tarefas bloqueadoras
    
    -- Metadados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to TEXT,
    completed_at TIMESTAMP,
    
    -- Contexto específico da tarefa
    context_files TEXT,                           -- JSON array de arquivos relacionados
    acceptance_criteria TEXT                      -- Critérios de aceitação
);
```

#### 3. **`prp_context`** - Contexto e Arquivos
```sql
-- Arquivos, bibliotecas e contexto mencionados no PRP
CREATE TABLE prp_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    context_type TEXT NOT NULL,                   -- file, directory, library, api, example, reference
    name TEXT NOT NULL,                           -- Nome do arquivo/biblioteca/etc
    path TEXT,                                    -- Caminho completo
    content TEXT,                                 -- Conteúdo ou descrição
    version TEXT,                                 -- Versão
    importance TEXT DEFAULT 'medium',             -- low, medium, high, critical
    is_required BOOLEAN DEFAULT 1,                -- Se é obrigatório
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. **`prp_llm_analysis`** - Análises LLM
```sql
-- Histórico de análises feitas pelo LLM
CREATE TABLE prp_llm_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    analysis_type TEXT NOT NULL,                  -- task_extraction, complexity_assessment, dependency_analysis, validation_check
    input_content TEXT NOT NULL,                  -- Conteúdo enviado para o LLM
    output_content TEXT NOT NULL,                 -- Resposta do LLM
    parsed_data TEXT,                             -- JSON com dados estruturados extraídos
    model_used TEXT,                              -- Modelo LLM usado
    tokens_used INTEGER,                          -- Tokens consumidos
    processing_time_ms INTEGER,                   -- Tempo de processamento
    confidence_score REAL,                        -- Score de confiança (0-1)
    status TEXT DEFAULT 'completed',              -- pending, processing, completed, failed
    error_message TEXT,                           -- Mensagem de erro (se falhou)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT
);
```

### Tabelas de Suporte

#### 5. **`prp_tags`** - Tags e Categorias
```sql
-- Tags para categorização
CREATE TABLE prp_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    color TEXT DEFAULT '#007bff',
    category TEXT DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. **`prp_history`** - Histórico e Versionamento
```sql
-- Histórico de mudanças
CREATE TABLE prp_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prp_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    action TEXT NOT NULL,                         -- created, updated, status_changed, archived
    old_data TEXT,                                -- JSON com dados anteriores
    new_data TEXT,                                -- JSON com dados novos
    changes_summary TEXT,                         -- Resumo das mudanças
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    comment TEXT                                  -- Comentário sobre a mudança
);
```

## 🔄 Operações CRUD

### 1. **Criar PRP**

```python
def create_prp(data):
    """Cria um novo PRP"""
    cursor.execute("""
        INSERT INTO prps (
            name, title, description, objective, context_data,
            implementation_details, validation_gates, status, priority, tags, search_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['name'], data['title'], data['description'], data['objective'],
        json.dumps(data['context_data']), json.dumps(data['implementation_details']),
        json.dumps(data['validation_gates']), data['status'], data['priority'],
        json.dumps(data['tags']), data['search_text']
    ))
    return cursor.lastrowid
```

### 2. **Buscar PRPs**

```python
def search_prps(query=None, status=None, priority=None, tags=None):
    """Busca PRPs com filtros"""
    sql = "SELECT * FROM prps WHERE 1=1"
    params = []
    
    if query:
        sql += " AND search_text LIKE ?"
        params.append(f"%{query}%")
    
    if status:
        sql += " AND status = ?"
        params.append(status)
    
    if priority:
        sql += " AND priority = ?"
        params.append(priority)
    
    if tags:
        # Busca por tags (JSON array)
        for tag in tags:
            sql += " AND tags LIKE ?"
            params.append(f"%{tag}%")
    
    cursor.execute(sql, params)
    return cursor.fetchall()
```

### 3. **Extrair Tarefas com LLM**

```python
def extract_tasks_with_llm(prp_id, prp_content):
    """Extrai tarefas do PRP usando LLM"""
    
    # Preparar prompt para o LLM
    prompt = f"""
    Analise o seguinte PRP e extraia as tarefas necessárias:
    
    {prp_content}
    
    Retorne um JSON com a seguinte estrutura:
    {{
        "tasks": [
            {{
                "name": "Nome da tarefa",
                "description": "Descrição detalhada",
                "type": "feature|bugfix|refactor|test|docs|setup",
                "priority": "low|medium|high|critical",
                "estimated_hours": 2.5,
                "complexity": "low|medium|high",
                "context_files": ["arquivo1.py", "arquivo2.ts"],
                "acceptance_criteria": "Critérios de aceitação"
            }}
        ]
    }}
    """
    
    # Chamar LLM (Anthropic Claude)
    response = call_anthropic_api(prompt)
    tasks_data = json.loads(response)
    
    # Salvar análise LLM
    cursor.execute("""
        INSERT INTO prp_llm_analysis (
            prp_id, analysis_type, input_content, output_content, 
            parsed_data, model_used, tokens_used, confidence_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prp_id, 'task_extraction', prp_content, response,
        json.dumps(tasks_data), 'claude-3-sonnet', tokens_used, confidence_score
    ))
    
    # Inserir tarefas extraídas
    for task in tasks_data['tasks']:
        cursor.execute("""
            INSERT INTO prp_tasks (
                prp_id, task_name, description, task_type, priority,
                estimated_hours, complexity, context_files, acceptance_criteria
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prp_id, task['name'], task['description'], task['type'],
            task['priority'], task['estimated_hours'], task['complexity'],
            json.dumps(task['context_files']), task['acceptance_criteria']
        ))
    
    return len(tasks_data['tasks'])
```

## 🎯 Melhores Práticas

### 1. **Estruturação de Dados JSON**

#### Context Data
```json
{
    "files": [
        {
            "path": "src/index.ts",
            "description": "Ponto de entrada principal",
            "importance": "high"
        }
    ],
    "libraries": [
        {
            "name": "@modelcontextprotocol/sdk",
            "version": "^1.0.0",
            "purpose": "SDK principal do MCP"
        }
    ],
    "examples": [
        {
            "path": "examples/database-tools.ts",
            "description": "Exemplo de ferramentas de banco"
        }
    ],
    "references": [
        {
            "url": "https://modelcontextprotocol.io/docs",
            "title": "Documentação oficial MCP"
        }
    ]
}
```

#### Implementation Details
```json
{
    "architecture": "Cloudflare Workers",
    "authentication": "GitHub OAuth",
    "database": "PostgreSQL",
    "llm": {
        "provider": "Anthropic",
        "model": "claude-3-sonnet",
        "api_key_env": "ANTHROPIC_API_KEY"
    },
    "dependencies": [
        "@modelcontextprotocol/sdk",
        "zod",
        "sqlite3"
    ],
    "patterns": [
        "Durable Objects",
        "Pool de conexões",
        "Validação SQL"
    ]
}
```

#### Validation Gates
```json
{
    "tests": {
        "framework": "pytest",
        "coverage": 80,
        "required": true
    },
    "linting": {
        "tool": "ruff",
        "strict": true
    },
    "type_check": {
        "tool": "TypeScript",
        "strict": true
    },
    "security": {
        "sql_injection": "prevented",
        "oauth_validation": "required"
    }
}
```

### 2. **Busca e Filtros Eficientes**

```python
def advanced_prp_search(filters):
    """Busca avançada de PRPs"""
    
    # Construir query dinâmica
    sql = """
        SELECT p.*, 
               COUNT(t.id) as total_tasks,
               COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks
        FROM prps p
        LEFT JOIN prp_tasks t ON p.id = t.prp_id
        WHERE 1=1
    """
    params = []
    
    # Filtros de texto
    if filters.get('search'):
        sql += " AND (p.search_text LIKE ? OR p.title LIKE ? OR p.description LIKE ?)"
        search_term = f"%{filters['search']}%"
        params.extend([search_term, search_term, search_term])
    
    # Filtros de status
    if filters.get('status'):
        sql += " AND p.status = ?"
        params.append(filters['status'])
    
    # Filtros de prioridade
    if filters.get('priority'):
        sql += " AND p.priority = ?"
        params.append(filters['priority'])
    
    # Filtros de complexidade
    if filters.get('complexity'):
        sql += " AND p.complexity = ?"
        params.append(filters['complexity'])
    
    # Filtros de data
    if filters.get('created_after'):
        sql += " AND p.created_at >= ?"
        params.append(filters['created_after'])
    
    # Agrupamento e ordenação
    sql += " GROUP BY p.id ORDER BY p.created_at DESC"
    
    cursor.execute(sql, params)
    return cursor.fetchall()
```

### 3. **Versionamento e Histórico**

```python
def update_prp_with_history(prp_id, updates, user_id, comment=None):
    """Atualiza PRP mantendo histórico"""
    
    # Buscar dados atuais
    cursor.execute("SELECT * FROM prps WHERE id = ?", (prp_id,))
    current_data = cursor.fetchone()
    
    # Preparar dados antigos para histórico
    old_data = {
        'title': current_data[2],
        'status': current_data[8],
        'priority': current_data[9],
        'description': current_data[3]
    }
    
    # Atualizar PRP
    set_clauses = []
    params = []
    
    for field, value in updates.items():
        set_clauses.append(f"{field} = ?")
        params.append(value)
    
    params.append(prp_id)
    
    sql = f"UPDATE prps SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(sql, params)
    
    # Registrar no histórico
    cursor.execute("""
        INSERT INTO prp_history (
            prp_id, version, action, old_data, new_data, 
            changes_summary, created_by, comment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prp_id, current_data[15] + 1, 'updated',
        json.dumps(old_data), json.dumps(updates),
        f"PRP updated by {user_id}", user_id, comment
    ))
```

## 🔧 Integração com MCP

### Ferramentas MCP para PRPs

```typescript
// Exemplo de ferramentas MCP para PRPs
export function registerPRPTools(server: McpServer, env: Env, props: Props) {
  
  // Criar PRP
  server.tool(
    "create_prp",
    "Cria um novo Product Requirement Prompt",
    {
      name: z.string().min(1),
      title: z.string().min(1),
      description: z.string().optional(),
      objective: z.string().min(1),
      context_data: z.string(), // JSON
      implementation_details: z.string(), // JSON
      validation_gates: z.string().optional(), // JSON
      priority: z.enum(['low', 'medium', 'high', 'critical']).optional(),
      tags: z.string().optional() // JSON array
    },
    async (params) => {
      // Implementação
    }
  );
  
  // Analisar PRP com LLM
  server.tool(
    "analyze_prp_with_llm",
    "Analisa um PRP usando LLM para extrair tarefas",
    {
      prp_id: z.number().int().positive(),
      analysis_type: z.enum(['task_extraction', 'complexity_assessment', 'dependency_analysis'])
    },
    async (params) => {
      // Implementação
    }
  );
  
  // Buscar PRPs
  server.tool(
    "search_prps",
    "Busca PRPs com filtros avançados",
    {
      query: z.string().optional(),
      status: z.enum(['draft', 'active', 'completed', 'archived']).optional(),
      priority: z.enum(['low', 'medium', 'high', 'critical']).optional(),
      tags: z.string().optional() // JSON array
    },
    async (params) => {
      // Implementação
    }
  );
}
```

## 📊 Views Úteis

### 1. **Progresso de PRPs**
```sql
-- View para análise de progresso
CREATE VIEW v_prp_progress AS
SELECT 
    p.id, p.name, p.title, p.status as prp_status,
    COUNT(t.id) as total_tasks,
    AVG(t.progress) as avg_task_progress,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
    ROUND(
        (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) * 100.0) / 
        COUNT(t.id), 2
    ) as completion_percentage
FROM prps p
LEFT JOIN prp_tasks t ON p.id = t.prp_id
GROUP BY p.id;
```

### 2. **PRPs com Tags**
```sql
-- View para PRPs com tags
CREATE VIEW v_prps_with_tags AS
SELECT 
    p.*,
    GROUP_CONCAT(t.name) as tag_names,
    GROUP_CONCAT(t.color) as tag_colors
FROM prps p
LEFT JOIN prp_tag_relations ptr ON p.id = ptr.prp_id
LEFT JOIN prp_tags t ON ptr.tag_id = t.id
GROUP BY p.id;
```

## 🚀 Próximos Passos

1. **Implementar servidor MCP para PRPs**
   - Criar ferramentas de CRUD
   - Integrar com LLM para análise
   - Implementar busca avançada

2. **Interface de usuário**
   - Dashboard de PRPs
   - Editor de PRPs
   - Visualização de progresso

3. **Automação**
   - Análise automática de PRPs
   - Extração automática de tarefas
   - Notificações de mudanças

4. **Integração**
   - GitHub/GitLab integration
   - CI/CD pipeline
   - Slack/Teams notifications

## 📝 Conclusão

Esta estrutura oferece:

- ✅ **Flexibilidade**: JSON para dados complexos
- ✅ **Performance**: Índices otimizados
- ✅ **Rastreabilidade**: Histórico completo
- ✅ **Integração**: Pronto para MCP e LLM
- ✅ **Escalabilidade**: Estrutura modular
- ✅ **Busca**: Full-text e filtros avançados

O banco está configurado e pronto para uso! 🎉 