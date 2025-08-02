# 🔗 Integração PRP ao Sistema MCP Turso Existente

## 📋 Visão Geral

Ao invés de criar um novo servidor MCP, vamos **integrar as funcionalidades de PRP ao sistema MCP Turso existente**, aproveitando a infraestrutura já funcionando.

## ✅ **Por que Integrar ao Existente?**

### Vantagens:
- ✅ **Reutiliza infraestrutura** já testada e funcionando
- ✅ **Mantém consistência** no sistema
- ✅ **Evita duplicação** de código e configuração
- ✅ **Aproveita autenticação** e segurança existentes
- ✅ **Banco de dados único** para todos os dados
- ✅ **Manutenção simplificada**

## 🏗️ **Estrutura Atual do Sistema**

### Banco de Dados: `context-memory`
```
Tabelas Existentes:
├── contexts          # Contextos gerais
├── conversations     # Histórico de conversas
├── knowledge_base    # Base de conhecimento
├── tasks            # Tarefas gerais
└── tools_usage      # Uso de ferramentas

Tabelas PRP (já criadas):
├── prps             # PRPs principais
├── prp_tasks        # Tarefas extraídas
├── prp_context      # Contexto específico
├── prp_tags         # Tags e categorias
├── prp_history      # Histórico de mudanças
├── prp_llm_analysis # Análises LLM
└── prp_tag_relations # Relacionamentos
```

### Servidor MCP Turso
- ✅ **Funcionando** e testado
- ✅ **Ferramentas** de banco de dados
- ✅ **Autenticação** configurada
- ✅ **Estrutura modular** para novas ferramentas

## 🔧 **Plano de Integração**

### Fase 1: Adicionar Ferramentas PRP ao MCP Turso

#### 1.1 **Ferramentas de CRUD PRP**

```typescript
// Adicionar ao src/tools/handler.ts

// Criar PRP
{
    name: 'create_prp',
    description: 'Cria um novo Product Requirement Prompt',
    inputSchema: {
        type: 'object',
        properties: {
            name: { type: 'string', description: 'Nome único do PRP' },
            title: { type: 'string', description: 'Título descritivo' },
            description: { type: 'string', description: 'Descrição geral' },
            objective: { type: 'string', description: 'Objetivo principal' },
            context_data: { type: 'string', description: 'JSON com contexto' },
            implementation_details: { type: 'string', description: 'JSON com detalhes' },
            validation_gates: { type: 'string', description: 'JSON com portões' },
            priority: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
            tags: { type: 'string', description: 'JSON array de tags' }
        },
        required: ['name', 'title', 'objective', 'context_data', 'implementation_details']
    }
}

// Buscar PRPs
{
    name: 'search_prps',
    description: 'Busca PRPs com filtros avançados',
    inputSchema: {
        type: 'object',
        properties: {
            query: { type: 'string', description: 'Termo de busca' },
            status: { type: 'string', enum: ['draft', 'active', 'completed', 'archived'] },
            priority: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
            tags: { type: 'string', description: 'JSON array de tags' },
            limit: { type: 'number', description: 'Limite de resultados' }
        }
    }
}

// Obter PRP específico
{
    name: 'get_prp',
    description: 'Obtém detalhes de um PRP específico',
    inputSchema: {
        type: 'object',
        properties: {
            prp_id: { type: 'number', description: 'ID do PRP' }
        },
        required: ['prp_id']
    }
}

// Atualizar PRP
{
    name: 'update_prp',
    description: 'Atualiza um PRP existente',
    inputSchema: {
        type: 'object',
        properties: {
            prp_id: { type: 'number', description: 'ID do PRP' },
            title: { type: 'string' },
            description: { type: 'string' },
            status: { type: 'string', enum: ['draft', 'active', 'completed', 'archived'] },
            priority: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] }
        },
        required: ['prp_id']
    }
}
```

#### 1.2 **Ferramentas de Análise LLM**

```typescript
// Analisar PRP com LLM
{
    name: 'analyze_prp_with_llm',
    description: 'Analisa um PRP usando LLM para extrair tarefas',
    inputSchema: {
        type: 'object',
        properties: {
            prp_id: { type: 'number', description: 'ID do PRP' },
            analysis_type: { 
                type: 'string', 
                enum: ['task_extraction', 'complexity_assessment', 'dependency_analysis'],
                description: 'Tipo de análise a realizar'
            },
            llm_model: { 
                type: 'string', 
                default: 'claude-3-sonnet',
                description: 'Modelo LLM a usar'
            }
        },
        required: ['prp_id', 'analysis_type']
    }
}

// Obter análises LLM
{
    name: 'get_prp_llm_analyses',
    description: 'Obtém histórico de análises LLM de um PRP',
    inputSchema: {
        type: 'object',
        properties: {
            prp_id: { type: 'number', description: 'ID do PRP' },
            analysis_type: { type: 'string', description: 'Filtrar por tipo' },
            limit: { type: 'number', default: 10, description: 'Limite de resultados' }
        },
        required: ['prp_id']
    }
}
```

#### 1.3 **Ferramentas de Tarefas**

```typescript
// Listar tarefas de um PRP
{
    name: 'list_prp_tasks',
    description: 'Lista tarefas extraídas de um PRP',
    inputSchema: {
        type: 'object',
        properties: {
            prp_id: { type: 'number', description: 'ID do PRP' },
            status: { type: 'string', enum: ['pending', 'in_progress', 'review', 'completed', 'blocked'] },
            priority: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] }
        },
        required: ['prp_id']
    }
}

// Atualizar status de tarefa
{
    name: 'update_prp_task',
    description: 'Atualiza status e progresso de uma tarefa',
    inputSchema: {
        type: 'object',
        properties: {
            task_id: { type: 'number', description: 'ID da tarefa' },
            status: { type: 'string', enum: ['pending', 'in_progress', 'review', 'completed', 'blocked'] },
            progress: { type: 'number', minimum: 0, maximum: 100, description: 'Progresso em %' },
            assigned_to: { type: 'string', description: 'Usuário responsável' }
        },
        required: ['task_id']
    }
}
```

#### 1.4 **Ferramentas de Contexto e Tags**

```typescript
// Gerenciar tags
{
    name: 'list_prp_tags',
    description: 'Lista todas as tags disponíveis',
    inputSchema: {
        type: 'object',
        properties: {
            category: { type: 'string', description: 'Filtrar por categoria' }
        }
    }
}

// Adicionar contexto a PRP
{
    name: 'add_prp_context',
    description: 'Adiciona contexto (arquivos, bibliotecas) a um PRP',
    inputSchema: {
        type: 'object',
        properties: {
            prp_id: { type: 'number', description: 'ID do PRP' },
            context_type: { 
                type: 'string', 
                enum: ['file', 'directory', 'library', 'api', 'example', 'reference'],
                description: 'Tipo de contexto'
            },
            name: { type: 'string', description: 'Nome do contexto' },
            path: { type: 'string', description: 'Caminho (se aplicável)' },
            content: { type: 'string', description: 'Conteúdo ou descrição' },
            importance: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] }
        },
        required: ['prp_id', 'context_type', 'name']
    }
}
```

### Fase 2: Implementação das Funções

#### 2.1 **Criar arquivo de ferramentas PRP**

```typescript
// src/tools/prp-tools.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import * as database_client from '../clients/database.js';

export async function create_prp(params: any): Promise<any> {
    const { name, title, description, objective, context_data, 
            implementation_details, validation_gates, priority, tags } = params;
    
    const sql = `
        INSERT INTO prps (
            name, title, description, objective, context_data,
            implementation_details, validation_gates, status, priority, tags, search_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?)
    `;
    
    const search_text = `${title} ${description} ${objective}`.toLowerCase();
    
    const result = await database_client.execute_query({
        database: 'context-memory',
        query: sql,
        params: [name, title, description, objective, context_data,
                implementation_details, validation_gates, priority, tags, search_text]
    });
    
    return {
        content: [{
            type: 'text',
            text: `✅ PRP "${title}" criado com sucesso!\n\n**ID:** ${result.lastInsertId}\n**Status:** draft\n**Próximo passo:** Analisar com LLM para extrair tarefas`
        }]
    };
}

export async function search_prps(params: any): Promise<any> {
    const { query, status, priority, tags, limit = 10 } = params;
    
    let sql = `
        SELECT p.*, 
               COUNT(t.id) as total_tasks,
               COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks
        FROM prps p
        LEFT JOIN prp_tasks t ON p.id = t.prp_id
        WHERE 1=1
    `;
    
    const sqlParams = [];
    
    if (query) {
        sql += ` AND p.search_text LIKE ?`;
        sqlParams.push(`%${query}%`);
    }
    
    if (status) {
        sql += ` AND p.status = ?`;
        sqlParams.push(status);
    }
    
    if (priority) {
        sql += ` AND p.priority = ?`;
        sqlParams.push(priority);
    }
    
    sql += ` GROUP BY p.id ORDER BY p.created_at DESC LIMIT ?`;
    sqlParams.push(limit);
    
    const result = await database_client.execute_read_only_query({
        database: 'context-memory',
        query: sql,
        params: sqlParams
    });
    
    return {
        content: [{
            type: 'text',
            text: `🔍 **Resultados da busca:** ${result.rows.length} PRPs encontrados\n\n${format_prp_results(result.rows)}`
        }]
    };
}

export async function analyze_prp_with_llm(params: any): Promise<any> {
    const { prp_id, analysis_type, llm_model = 'claude-3-sonnet' } = params;
    
    // 1. Buscar PRP
    const prp_result = await database_client.execute_read_only_query({
        database: 'context-memory',
        query: 'SELECT * FROM prps WHERE id = ?',
        params: [prp_id]
    });
    
    if (prp_result.rows.length === 0) {
        return {
            content: [{
                type: 'text',
                text: '❌ PRP não encontrado',
                isError: true
            }]
        };
    }
    
    const prp = prp_result.rows[0];
    
    // 2. Preparar prompt para LLM
    const prompt = build_llm_prompt(prp, analysis_type);
    
    // 3. Chamar LLM (implementar integração com Anthropic)
    const llm_response = await call_anthropic_api(prompt, llm_model);
    
    // 4. Salvar análise
    await database_client.execute_query({
        database: 'context-memory',
        query: `
            INSERT INTO prp_llm_analysis (
                prp_id, analysis_type, input_content, output_content,
                parsed_data, model_used, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        `,
        params: [prp_id, analysis_type, prompt, llm_response.content, 
                JSON.stringify(llm_response.parsed), llm_model, llm_response.confidence]
    });
    
    // 5. Se for extração de tarefas, salvar tarefas
    if (analysis_type === 'task_extraction' && llm_response.parsed.tasks) {
        for (const task of llm_response.parsed.tasks) {
            await database_client.execute_query({
                database: 'context-memory',
                query: `
                    INSERT INTO prp_tasks (
                        prp_id, task_name, description, task_type, priority,
                        estimated_hours, complexity, context_files, acceptance_criteria
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                `,
                params: [prp_id, task.name, task.description, task.type,
                        task.priority, task.estimated_hours, task.complexity,
                        JSON.stringify(task.context_files), task.acceptance_criteria]
            });
        }
    }
    
    return {
        content: [{
            type: 'text',
            text: `🧠 **Análise LLM concluída!**\n\n**Tipo:** ${analysis_type}\n**Modelo:** ${llm_model}\n**Confiança:** ${llm_response.confidence}%\n\n${format_llm_response(llm_response)}`
        }]
    };
}
```

#### 2.2 **Integrar ao handler principal**

```typescript
// src/tools/handler.ts - Adicionar ao final

// Importar ferramentas PRP
import * as prp_tools from './prp-tools.js';

// Adicionar ao register_tools()
export function register_tools(server: Server): void {
    // ... ferramentas existentes ...
    
    // Registrar ferramentas PRP
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        const { name, arguments: args } = request.params;
        
        try {
            switch (name) {
                // ... casos existentes ...
                
                // Ferramentas PRP
                case 'create_prp':
                    return await prp_tools.create_prp(args);
                
                case 'search_prps':
                    return await prp_tools.search_prps(args);
                
                case 'get_prp':
                    return await prp_tools.get_prp(args);
                
                case 'update_prp':
                    return await prp_tools.update_prp(args);
                
                case 'analyze_prp_with_llm':
                    return await prp_tools.analyze_prp_with_llm(args);
                
                case 'list_prp_tasks':
                    return await prp_tools.list_prp_tasks(args);
                
                case 'update_prp_task':
                    return await prp_tools.update_prp_task(args);
                
                case 'list_prp_tags':
                    return await prp_tools.list_prp_tags(args);
                
                case 'add_prp_context':
                    return await prp_tools.add_prp_context(args);
                
                default:
                    throw new Error(`Unknown tool: ${name}`);
            }
        } catch (error) {
            console.error(`Error in tool ${name}:`, error);
            return {
                content: [{
                    type: 'text',
                    text: `❌ Erro na ferramenta ${name}: ${error.message}`,
                    isError: true
                }]
            };
        }
    });
}
```

### Fase 3: Integração com LLM

#### 3.1 **Configurar integração Anthropic**

```typescript
// src/clients/anthropic.ts
import { Anthropic } from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function call_anthropic_api(prompt: string, model: string = 'claude-3-sonnet') {
    try {
        const response = await anthropic.messages.create({
            model,
            max_tokens: 4000,
            messages: [{
                role: 'user',
                content: prompt
            }]
        });
        
        const content = response.content[0].text;
        
        // Tentar parsear JSON se for análise estruturada
        let parsed = null;
        try {
            parsed = JSON.parse(content);
        } catch (e) {
            // Se não for JSON, usar texto puro
        }
        
        return {
            content,
            parsed,
            confidence: 0.9, // Placeholder
            tokens_used: response.usage?.input_tokens + response.usage?.output_tokens
        };
    } catch (error) {
        throw new Error(`Erro na API Anthropic: ${error.message}`);
    }
}

export function build_llm_prompt(prp: any, analysis_type: string): string {
    switch (analysis_type) {
        case 'task_extraction':
            return `
Analise o seguinte PRP e extraia as tarefas necessárias para implementá-lo:

**PRP:** ${prp.title}
**Objetivo:** ${prp.objective}
**Descrição:** ${prp.description}
**Contexto:** ${prp.context_data}
**Implementação:** ${prp.implementation_details}
**Validação:** ${prp.validation_gates}

Retorne um JSON com a seguinte estrutura:
{
    "tasks": [
        {
            "name": "Nome da tarefa",
            "description": "Descrição detalhada",
            "type": "feature|bugfix|refactor|test|docs|setup",
            "priority": "low|medium|high|critical",
            "estimated_hours": 2.5,
            "complexity": "low|medium|high",
            "context_files": ["arquivo1.py", "arquivo2.ts"],
            "acceptance_criteria": "Critérios de aceitação"
        }
    ],
    "summary": "Resumo da análise",
    "total_estimated_hours": 15.5,
    "complexity_assessment": "low|medium|high"
}
            `;
        
        case 'complexity_assessment':
            return `
Avalie a complexidade do seguinte PRP:

**PRP:** ${prp.title}
**Objetivo:** ${prp.objective}
**Contexto:** ${prp.context_data}
**Implementação:** ${prp.implementation_details}

Retorne um JSON com:
{
    "overall_complexity": "low|medium|high",
    "technical_complexity": "low|medium|high",
    "business_complexity": "low|medium|high",
    "risk_factors": ["fator1", "fator2"],
    "recommendations": ["recomendação1", "recomendação2"],
    "estimated_timeline": "2-3 semanas"
}
            `;
        
        default:
            return `Analise o PRP: ${prp.title}`;
    }
}
```

## 🚀 **Plano de Implementação**

### Passo 1: Preparar Ambiente
```bash
# 1. Adicionar dependência Anthropic
cd mcp-turso-cloud
npm install @anthropic-ai/sdk

# 2. Configurar variável de ambiente
echo "ANTHROPIC_API_KEY=sua_chave_aqui" >> .env
```

### Passo 2: Implementar Ferramentas
```bash
# 1. Criar arquivo de ferramentas PRP
# 2. Integrar ao handler principal
# 3. Testar compilação
npm run build
```

### Passo 3: Testar Integração
```bash
# 1. Reiniciar servidor MCP
./start-claude.sh

# 2. Testar ferramentas
# - Criar PRP
# - Buscar PRPs
# - Analisar com LLM
```

## 📊 **Benefícios da Integração**

### ✅ **Reutilização de Infraestrutura**
- Banco de dados único (`context-memory`)
- Autenticação e segurança existentes
- Ferramentas de banco já funcionando

### ✅ **Consistência**
- Mesmo padrão de ferramentas
- Mesma estrutura de resposta
- Mesmo tratamento de erros

### ✅ **Manutenção Simplificada**
- Um servidor para manter
- Configuração centralizada
- Logs unificados

### ✅ **Funcionalidades Extendidas**
- PRPs integrados ao sistema de memória
- Análise LLM automática
- Busca e filtros avançados
- Histórico completo

## 🎯 **Próximos Passos**

1. **Implementar ferramentas PRP** no MCP Turso
2. **Configurar integração Anthropic**
3. **Testar funcionalidades**
4. **Documentar uso**
5. **Criar exemplos práticos**

Esta abordagem é muito mais eficiente e mantém a consistência do sistema! 🚀 