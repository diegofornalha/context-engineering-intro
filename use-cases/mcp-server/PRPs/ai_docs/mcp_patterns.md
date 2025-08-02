# Padrões de Desenvolvimento de Servidor MCP

Este documento contém padrões comprovados para desenvolver servidores Model Context Protocol (MCP) usando TypeScript e Cloudflare Workers, baseado na implementação neste codebase.

## Arquitetura Principal do Servidor MCP

### Padrão de Classe Base do Servidor

```typescript
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Props de autenticação do fluxo OAuth
type Props = {
  login: string;
  name: string;
  email: string;
  accessToken: string;
};

export class CustomMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "Nome do Seu Servidor MCP",
    version: "1.0.0",
  });

  // CRÍTICO: Implementar cleanup para Durable Objects
  async cleanup(): Promise<void> {
    try {
      // Fechar conexões do banco de dados
      await closeDb();
      console.log('Conexões do banco de dados fechadas com sucesso');
    } catch (error) {
      console.error('Erro durante limpeza do banco de dados:', error);
    }
  }

  // CRÍTICO: Manipulador de alarme de Durable Objects
  async alarm(): Promise<void> {
    await this.cleanup();
  }

  // Inicializar todas as ferramentas e recursos
  async init() {
    // Registrar ferramentas aqui
    this.registerTools();
    
    // Registrar recursos se necessário
    this.registerResources();
  }

  private registerTools() {
    // Lógica de registro de ferramentas
  }

  private registerResources() {
    // Lógica de registro de recursos
  }
}
```

### Padrão de Registro de Ferramentas

```typescript
// Registro básico de ferramenta
this.server.tool(
  "toolName",
  "Descrição da ferramenta para o LLM",
  {
    param1: z.string().describe("Descrição do parâmetro"),
    param2: z.number().optional().describe("Parâmetro opcional"),
  },
  async ({ param1, param2 }) => {
    try {
      // Implementação da ferramenta
      const result = await performOperation(param1, param2);
      
      return {
        content: [
          {
            type: "text",
            text: `Sucesso: ${JSON.stringify(result, null, 2)}`
          }
        ]
      };
    } catch (error) {
      console.error('Erro da ferramenta:', error);
      return {
        content: [
          {
            type: "text",
            text: `Erro: ${error.message}`,
            isError: true
          }
        ]
      };
    }
  }
);
```

### Registro Condicional de Ferramentas (Baseado em Permissões)

```typescript
// Disponibilidade de ferramentas baseada em permissões
const ALLOWED_USERNAMES = new Set<string>([
  'admin1',
  'admin2'
]);

// Registrar ferramentas privilegiadas apenas para usuários autorizados
if (ALLOWED_USERNAMES.has(this.props.login)) {
  this.server.tool(
    "privilegedTool",
    "Ferramenta disponível apenas para usuários autorizados",
    { /* parâmetros */ },
    async (params) => {
      // Operação privilegiada
      return {
        content: [
          {
            type: "text",
            text: `Operação privilegiada executada por: ${this.props.login}`
          }
        ]
      };
    }
  );
}
```

## Padrões de Integração de Banco de Dados

### Padrão de Conexão de Banco de Dados

```typescript
import { withDatabase, validateSqlQuery, isWriteOperation, formatDatabaseError } from "./database";

// Operação de banco de dados com gerenciamento de conexão
async function performDatabaseOperation(sql: string) {
  try {
    // Validar consulta SQL
    const validation = validateSqlQuery(sql);
    if (!validation.isValid) {
      return {
        content: [
          {
            type: "text",
            text: `Consulta SQL inválida: ${validation.error}`,
            isError: true
          }
        ]
      };
    }

    // Executar com gerenciamento automático de conexão
    return await withDatabase(this.env.DATABASE_URL, async (db) => {
      const results = await db.unsafe(sql);
      
      return {
        content: [
          {
            type: "text",
            text: `**Resultados da Consulta**\n\`\`\`sql\n${sql}\n\`\`\`\n\n**Resultados:**\n\`\`\`json\n${JSON.stringify(results, null, 2)}\n\`\`\`\n\n**Linhas retornadas:** ${Array.isArray(results) ? results.length : 1}`
          }
        ]
      };
    });
  } catch (error) {
    console.error('Erro na operação do banco de dados:', error);
    return {
      content: [
        {
          type: "text",
          text: `Erro do banco de dados: ${formatDatabaseError(error)}`,
          isError: true
        }
      ]
    };
  }
}
```

### Manipulação de Operações de Leitura vs Escrita

```typescript
// Verificar se a operação é somente leitura
if (isWriteOperation(sql)) {
  return {
    content: [
      {
        type: "text",
        text: "Operações de escrita não são permitidas com esta ferramenta. Use a ferramenta privilegiada se você tem permissões de escrita.",
        isError: true
      }
    ]
  };
}
```

## Padrões de Autenticação & Autorização

### Padrão de Integração OAuth

```typescript
import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { GitHubHandler } from "./github-handler";

// Configuração OAuth
export default new OAuthProvider({
  apiHandlers: {
    '/sse': MyMCP.serveSSE('/sse') as any,
    '/mcp': MyMCP.serve('/mcp') as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### Verificação de Permissões do Usuário

```typescript
// Padrão de validação de permissões
function hasPermission(username: string, operation: string): boolean {
  const WRITE_PERMISSIONS = new Set(['admin1', 'admin2']);
  const READ_PERMISSIONS = new Set(['user1', 'user2', ...WRITE_PERMISSIONS]);
  
  switch (operation) {
    case 'read':
      return READ_PERMISSIONS.has(username);
    case 'write':
      return WRITE_PERMISSIONS.has(username);
    default:
      return false;
  }
}
```

## Padrões de Tratamento de Erros

### Resposta de Erro Padronizada

```typescript
// Padrão de resposta de erro
function createErrorResponse(error: Error, operation: string) {
  console.error(`Erro de ${operation}:`, error);
  
  return {
    content: [
      {
        type: "text",
        text: `${operation} falhou: ${error.message}`,
        isError: true
      }
    ]
  };
}
```

### Formatação de Erro de Banco de Dados

```typescript
// Usar o formatador de erro de banco de dados integrado
import { formatDatabaseError } from "./database";

try {
  // Operação de banco de dados
} catch (error) {
  return {
    content: [
      {
        type: "text",
        text: `Erro do banco de dados: ${formatDatabaseError(error)}`,
        isError: true
      }
    ]
  };
}
```

## Padrões de Registro de Recursos

### Padrão Básico de Recurso

```typescript
// Registro de recurso
this.server.resource(
  "resource://example/{id}",
  "Descrição do recurso",
  async (uri) => {
    const id = uri.path.split('/').pop();
    
    try {
      const data = await fetchResourceData(id);
      
      return {
        contents: [
          {
            uri: uri.href,
            mimeType: "application/json",
            text: JSON.stringify(data, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Falha ao buscar recurso: ${error.message}`);
    }
  }
);
```

## Padrões de Teste

### Padrão de Teste de Ferramenta

```typescript
// Testar funcionalidade da ferramenta
async function testTool(toolName: string, params: any) {
  try {
    const result = await server.callTool(toolName, params);
    console.log(`Teste de ${toolName} passou:`, result);
    return true;
  } catch (error) {
    console.error(`Teste de ${toolName} falhou:`, error);
    return false;
  }
}
```

### Teste de Conexão de Banco de Dados

```typescript
// Testar conectividade do banco de dados
async function testDatabaseConnection() {
  try {
    await withDatabase(process.env.DATABASE_URL, async (db) => {
      const result = await db`SELECT 1 as test`;
      console.log('Teste de conexão do banco de dados passou:', result);
    });
    return true;
  } catch (error) {
    console.error('Teste de conexão do banco de dados falhou:', error);
    return false;
  }
}
```

## Melhores Práticas de Segurança

### Validação de Entrada

```typescript
// Sempre validar entradas com Zod
const inputSchema = z.object({
  query: z.string().min(1).max(1000),
  parameters: z.array(z.string()).optional()
});

// No manipulador de ferramenta
try {
  const validated = inputSchema.parse(params);
  // Usar dados validados
} catch (error) {
  return createErrorResponse(error, "Validação de entrada");
}
```

### Prevenção de Injeção SQL

```typescript
// Usar a validação SQL integrada
import { validateSqlQuery } from "./database";

const validation = validateSqlQuery(sql);
if (!validation.isValid) {
  return createErrorResponse(new Error(validation.error), "Validação SQL");
}
```

### Controle de Acesso

```typescript
// Sempre verificar permissões antes de executar operações sensíveis
if (!hasPermission(this.props.login, 'write')) {
  return {
    content: [
      {
        type: "text",
        text: "Acesso negado: permissões insuficientes",
        isError: true
      }
    ]
  };
}
```

## Padrões de Performance

### Pool de Conexões

```typescript
// Usar o pool de conexões integrado
import { withDatabase } from "./database";

// A função withDatabase gerencia o pool de conexões automaticamente
await withDatabase(databaseUrl, async (db) => {
  // Operações de banco de dados
});
```

### Limpeza de Recursos

```typescript
// Implementar limpeza adequada em Durable Objects
async cleanup(): Promise<void> {
  try {
    // Fechar conexões do banco de dados
    await closeDb();
    
    // Limpar outros recursos
    await cleanupResources();
    
    console.log('Limpeza completada com sucesso');
  } catch (error) {
    console.error('Erro na limpeza:', error);
  }
}
```

## Armadilhas Comuns

### 1. Implementação de Limpeza Ausente
- Sempre implementar método `cleanup()` em Durable Objects
- Lidar adequadamente com limpeza de conexões do banco de dados
- Configurar manipulador de alarme para limpeza automática

### 2. Vulnerabilidades de Injeção SQL
- Sempre usar `validateSqlQuery()` antes de executar SQL
- Nunca concatenar entrada do usuário diretamente em strings SQL
- Usar consultas parametrizadas quando possível

### 3. Bypasses de Permissão
- Verificar permissões para toda operação sensível
- Não confiar apenas no registro de ferramentas para segurança
- Sempre validar identidade do usuário a partir de props

### 4. Vazamento de Informações de Erro
- Usar `formatDatabaseError()` para sanitizar mensagens de erro
- Não expor detalhes internos do sistema em respostas de erro
- Registrar erros detalhados no servidor, retornar mensagens genéricas ao cliente

### 5. Vazamentos de Recursos
- Sempre usar `withDatabase()` para operações de banco de dados
- Implementar tratamento adequado de erros em operações assíncronas
- Limpar recursos em blocos finally

## Configuração de Ambiente

### Variáveis de Ambiente Necessárias

```typescript
// Definição de tipo de ambiente
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // Adicionar outros bindings conforme necessário
}
```

### Padrão de Configuração Wrangler

```toml
# wrangler.toml
name = "mcp-server"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "OAUTH_KV"
id = "seu-id-de-namespace-kv"

[env.production]
# Configuração específica de produção
```

Este documento fornece os padrões principais para construir servidores MCP seguros e escaláveis usando a arquitetura comprovada neste codebase.