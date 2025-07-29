---
name: "Template PRP de Servidor MCP"
description: Este template é projetado para fornecer um servidor Model Context Protocol (MCP) pronto para produção usando os padrões comprovados deste codebase.
---

## Propósito

Template otimizado para agentes de IA implementarem servidores Model Context Protocol (MCP) prontos para produção com autenticação GitHub OAuth, integração de banco de dados e implantação Cloudflare Workers usando os padrões comprovados deste codebase.

## Princípios Fundamentais

1. **Contexto é Rei**: Incluir TODOS os padrões MCP necessários, fluxos de autenticação e configurações de implantação
2. **Loops de Validação**: Fornecer testes executáveis desde compilação TypeScript até implantação em produção
3. **Segurança Primeiro**: Construir autenticação, autorização e proteção contra injeção SQL
4. **Pronto para Produção**: Incluir monitoramento, tratamento de erros e automação de implantação

---

## Objetivo

Construir um servidor MCP (Model Context Protocol) pronto para produção com:

- [FUNCIONALIDADE MCP ESPECÍFICA] - descrever as ferramentas e recursos específicos a implementar
- Autenticação GitHub OAuth com controle de acesso baseado em funções
- Implantação Cloudflare Workers com monitoramento
- [FUNCIONALIDADES ADICIONAIS] - quaisquer funcionalidades específicas além da autenticação/banco de dados base

## Por que

- **Produtividade do Desenvolvedor**: Habilitar acesso seguro de assistentes de IA a [DADOS/OPERAÇÕES ESPECÍFICOS]
- **Segurança Empresarial**: GitHub OAuth com sistema de permissões granular
- **Escalabilidade**: Implantação global edge do Cloudflare Workers
- **Integração**: [COMO ISSO SE ENCAIXA COM SISTEMAS EXISTENTES]
- **Valor do Usuário**: [BENEFÍCIOS ESPECÍFICOS PARA USUÁRIOS FINAIS]

## O que

### Funcionalidades do Servidor MCP

**Ferramentas MCP Principais:**

- Ferramentas são organizadas em arquivos modulares e registradas via `src/tools/register-tools.ts`
- Cada funcionalidade/domínio obtém seu próprio arquivo de registro de ferramentas (ex: `database-tools.ts`, `analytics-tools.ts`)
- [LISTAR FERRAMENTAS ESPECÍFICAS] - ex: "queryDatabase", "listTables", "executeOperations"
- Autenticação de usuário e validação de permissões acontece durante o registro de ferramentas
- Tratamento abrangente de erros e logging
- [FERRAMENTAS ESPECÍFICAS DO DOMÍNIO] - ferramentas específicas para seu caso de uso

**Autenticação & Autorização:**

- Integração GitHub OAuth 2.0 com sistema de aprovação de cookies assinados
- Controle de acesso baseado em funções (usuários somente leitura vs privilegiados)
- Propagação de contexto do usuário para todas as ferramentas MCP
- Gerenciamento seguro de sessão com cookies assinados HMAC

**Integração de Banco de Dados:**

- Pool de conexões PostgreSQL com limpeza automática
- Proteção contra injeção SQL e validação de consultas
- Separação de operações de leitura/escrita baseada em permissões do usuário
- Sanitização de erros para prevenir vazamento de informações

**Implantação & Monitoramento:**

- Cloudflare Workers com Durable Objects para gerenciamento de estado
- Integração opcional Sentry para rastreamento de erros e monitoramento de performance
- Configuração baseada em ambiente (desenvolvimento vs produção)
- Logging e alertas em tempo real

### Critérios de Sucesso

- [ ] Servidor MCP passa validação com MCP Inspector
- [ ] Fluxo GitHub OAuth funciona end-to-end (autorização → callback → acesso MCP)
- [ ] Compilação TypeScript é bem-sucedida sem erros
- [ ] Servidor de desenvolvimento local inicia e responde corretamente
- [ ] Implantação em produção no Cloudflare Workers é bem-sucedida
- [ ] Autenticação previne acesso não autorizado a operações sensíveis
- [ ] Tratamento de erros fornece mensagens amigáveis ao usuário sem vazar detalhes do sistema
- [ ] [CRITÉRIOS DE SUCESSO ESPECÍFICOS DO DOMÍNIO]

## Todo o Contexto Necessário

### Documentação & Referências (DEVE LER)

```yaml
# PADRÕES MCP CRÍTICOS - Leia estes primeiro
- docfile: PRPs/ai_docs/mcp_patterns.md
  why: Padrões de desenvolvimento MCP, práticas de segurança e tratamento de erros

# Exemplos de código críticos
- docfile: PRPs/ai_docs/claude_api_usage.md
  why: Como usar a API Anthropic para obter resposta de um LLM

# SISTEMA DE REGISTRO DE FERRAMENTAS - Entenda a abordagem modular
- file: src/tools/register-tools.ts
  why: Registro central mostrando como todas as ferramentas são importadas e registradas - ESTUDE este padrão

# EXEMPLOS DE FERRAMENTAS MCP - Veja aqui como criar e registrar novas ferramentas
- file: examples/database-tools.ts
  why: Exemplos de ferramentas para um servidor MCP Postgres mostrando melhores práticas para criação e registro de ferramentas

- file: examples/database-tools-sentry.ts
  why: Exemplos de ferramentas para o servidor MCP Postgres mas com integração Sentry para monitoramento em produção

# PADRÕES DO CODEBASE EXISTENTE - Estude estas implementações
- file: src/index.ts
  why: Servidor MCP completo com autenticação, banco de dados e ferramentas - ESPELHE este padrão

- file: src/github-handler.ts
  why: Implementação do fluxo OAuth - USE este padrão exato para autenticação

- file: src/database.ts
  why: Segurança do banco de dados, pool de conexões, validação SQL - SIGA estes padrões

- file: wrangler.jsonc
  why: Configuração Cloudflare Workers - COPIE este padrão para implantação

# DOCUMENTAÇÃO OFICIAL MCP
- url: https://modelcontextprotocol.io/docs/concepts/tools
  why: Padrões de registro de ferramentas MCP e definição de schema

- url: https://modelcontextprotocol.io/docs/concepts/resources
  why: Implementação de recursos MCP se necessário

# Adicione documentação relacionada ao caso de uso do usuário conforme necessário abaixo
```

### Árvore do Codebase Atual (Execute `tree -I node_modules` na raiz do projeto)

```bash
# INSERIR SAÍDA REAL DA ÁRVORE AQUI
/
├── src/
│   ├── index.ts                 # Servidor MCP autenticado principal ← ESTUDE ISTO
│   ├── index_sentry.ts         # Versão com monitoramento Sentry
│   ├── simple-math.ts          # Exemplo MCP básico ← BOM PONTO DE PARTIDA
│   ├── github-handler.ts       # Implementação OAuth ← USE ESTE PADRÃO
│   ├── database.ts             # Utilitários de banco de dados ← PADRÕES DE SEGURANÇA
│   ├── utils.ts                # Helpers OAuth
│   ├── workers-oauth-utils.ts  # Sistema de segurança de cookies
│   └── tools/                  # Sistema de registro de ferramentas
│       └── register-tools.ts   # Registro central de ferramentas ← ENTENDA ISTO
├── PRPs/
│   ├── templates/prp_mcp_base.md  # Este template
│   └── ai_docs/                   # Guias de implementação ← LEIA TODOS
├── examples/                   # Exemplos de implementação de ferramentas
│   ├── database-tools.ts       # Exemplo de ferramentas de banco de dados ← SIGA PADRÃO
│   └── database-tools-sentry.ts # Com monitoramento Sentry
├── wrangler.jsonc              # Config Cloudflare ← COPIE PADRÕES
├── package.json                # Dependências
└── tsconfig.json               # Config TypeScript
```

### Árvore Desejada do Codebase (Arquivos para adicionar/modificar) relacionada ao caso de uso do usuário conforme necessário abaixo

```bash

```

### Armadilhas Conhecidas & Padrões Críticos MCP/Cloudflare

```typescript
// CRÍTICO: Cloudflare Workers requer padrões específicos
// 1. SEMPRE implemente cleanup para Durable Objects
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  async cleanup(): Promise<void> {
    await closeDb(); // CRÍTICO: Feche conexões do banco de dados
  }

  async alarm(): Promise<void> {
    await this.cleanup(); // CRÍTICO: Lidar com alarmes de Durable Object
  }
}

// 2. SEMPRE valide SQL para prevenir injeção (use padrões existentes)
const validation = validateSqlQuery(sql); // de src/database.ts
if (!validation.isValid) {
  return createErrorResponse(validation.error);
}

// 3. SEMPRE verifique permissões antes de operações sensíveis
const ALLOWED_USERNAMES = new Set(["admin1", "admin2"]);
if (!ALLOWED_USERNAMES.has(this.props.login)) {
  return createErrorResponse("Permissões insuficientes");
}

// 4. SEMPRE use wrapper withDatabase para gerenciamento de conexão
return await withDatabase(this.env.DATABASE_URL, async (db) => {
  // Operações de banco de dados aqui
});

// 5. SEMPRE use Zod para validação de entrada
import { z } from "zod";
const schema = z.object({
  param: z.string().min(1).max(100),
});

// 6. Compilação TypeScript requer correspondência exata de interface
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // Adicione suas variáveis de ambiente aqui
}
```

## Plano de Implementação

### Modelos de Dados & Tipos

Defina interfaces TypeScript e schemas Zod para segurança de tipos e validação.

```typescript
// Props de autenticação de usuário (herdado do OAuth)
type Props = {
  login: string; // Nome de usuário GitHub
  name: string; // Nome de exibição
  email: string; // Endereço de email
  accessToken: string; // Token de acesso GitHub
};

// Schemas de entrada de ferramentas MCP (personalize para suas ferramentas)
const YourToolSchema = z.object({
  param1: z.string().min(1, "Parâmetro não pode estar vazio"),
  param2: z.number().int().positive().optional(),
  options: z.object({}).optional(),
});

// Interface de ambiente (adicione suas variáveis)
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // SUA_VAR_ESPECÍFICA_ENV: string;
}

// Níveis de permissão (personalize para seu caso de uso)
enum Permission {
  READ = "read",
  WRITE = "write",
  ADMIN = "admin",
}
```

### Lista de Tarefas (Complete em ordem)

```yaml
Tarefa 1 - Configuração do Projeto:
  COPIAR wrangler.jsonc para wrangler-[nome-do-servidor].jsonc:
    - MODIFICAR campo name para "[nome-do-servidor]"
    - ADICIONAR quaisquer novas variáveis de ambiente na seção vars
    - MANTER configuração OAuth e banco de dados existente

  CRIAR arquivo .dev.vars (se não existir):
    - ADICIONAR GITHUB_CLIENT_ID=seu_client_id
    - ADICIONAR GITHUB_CLIENT_SECRET=seu_client_secret
    - ADICIONAR DATABASE_URL=postgresql://...
    - ADICIONAR COOKIE_ENCRYPTION_KEY=sua_chave_32_bytes
    - ADICIONAR quaisquer variáveis de ambiente específicas do domínio

Tarefa 2 - Aplicativo GitHub OAuth:
  CRIAR novo aplicativo GitHub OAuth:
    - DEFINIR URL da página inicial: https://seu-worker.workers.dev
    - DEFINIR URL de callback: https://seu-worker.workers.dev/callback
    - COPIAR client ID e secret para .dev.vars

  OU REUTILIZAR aplicativo OAuth existente:
    - ATUALIZAR URL de callback se usando subdomínio diferente
    - VERIFICAR client ID e secret no ambiente

Tarefa 3 - Implementação do Servidor MCP:
  CRIAR src/[nome-do-servidor].ts OU MODIFICAR src/index.ts:
    - COPIAR estrutura de classe de src/index.ts
    - MODIFICAR nome do servidor e versão no construtor McpServer
    - CHAMAR registerAllTools(server, env, props) no método init()
    - MANTER padrões de autenticação e banco de dados idênticos

  CRIAR módulos de ferramentas:
    - CRIAR novos arquivos de ferramentas seguindo padrão examples/database-tools.ts
    - EXPORTAR funções de registro que aceitam (server, env, props)
    - USAR schemas Zod para validação de entrada
    - IMPLEMENTAR tratamento adequado de erros com createErrorResponse
    - ADICIONAR verificação de permissões durante registro de ferramentas

  ATUALIZAR registro de ferramentas:
    - MODIFICAR src/tools/register-tools.ts para importar suas novas ferramentas
    - ADICIONAR sua chamada de função de registro em registerAllTools()

Tarefa 4 - Integração de Banco de Dados (se necessário):
  USAR padrões de banco de dados existentes de src/database.ts:
    - IMPORTAR withDatabase, validateSqlQuery, isWriteOperation
    - IMPLEMENTAR operações de banco de dados com validação de segurança
    - SEPARAR operações de leitura vs escrita baseado em permissões do usuário
    - USAR formatDatabaseError para mensagens de erro amigáveis ao usuário

Tarefa 5 - Configuração de Ambiente:
  CONFIGURAR namespace Cloudflare KV:
    - EXECUTAR: wrangler kv namespace create "OAUTH_KV"
    - ATUALIZAR wrangler.jsonc com ID do namespace retornado

  DEFINIR segredos de produção:
    - EXECUTAR: wrangler secret put GITHUB_CLIENT_ID
    - EXECUTAR: wrangler secret put GITHUB_CLIENT_SECRET
    - EXECUTAR: wrangler secret put DATABASE_URL
    - EXECUTAR: wrangler secret put COOKIE_ENCRYPTION_KEY

Tarefa 6 - Teste Local:
  TESTAR funcionalidade básica:
    - EXECUTAR: wrangler dev
    - VERIFICAR servidor inicia sem erros
    - TESTAR fluxo OAuth: http://localhost:8792/authorize
    - VERIFICAR endpoint MCP: http://localhost:8792/mcp

Tarefa 7 - Implantação em Produção:
  IMPLANTAR no Cloudflare Workers:
    - EXECUTAR: wrangler deploy
    - VERIFICAR sucesso da implantação
    - TESTAR fluxo OAuth de produção
    - VERIFICAR acessibilidade do endpoint MCP
```

### Detalhes de Implementação por Tarefa

```typescript
// Tarefa 3 - Padrão de Implementação do Servidor MCP
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "Nome do Seu Servidor MCP",
    version: "1.0.0",
  });

  // CRÍTICO: Sempre implemente cleanup
  async cleanup(): Promise<void> {
    try {
      await closeDb();
      console.log("Conexões do banco de dados fechadas com sucesso");
    } catch (error) {
      console.error("Erro durante limpeza do banco de dados:", error);
    }
  }

  async alarm(): Promise<void> {
    await this.cleanup();
  }

  async init() {
    // PADRÃO: Use registro centralizado de ferramentas
    registerAllTools(this.server, this.env, this.props);
  }
}

// Tarefa 3 - Padrão de Módulo de Ferramentas (ex: src/tools/your-feature-tools.ts)
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { z } from "zod";

const PRIVILEGED_USERS = new Set(["admin1", "admin2"]);

export function registerYourFeatureTools(server: McpServer, env: Env, props: Props) {
  // Ferramenta 1: Disponível para todos os usuários autenticados
  server.tool(
    "yourBasicTool",
    "Descrição da sua ferramenta básica",
    YourToolSchema, // Schema de validação Zod
    async ({ param1, param2, options }) => {
      try {
        // PADRÃO: Implementação de ferramenta com tratamento de erros
        const result = await performOperation(param1, param2, options);

        return {
          content: [
            {
              type: "text",
              text: `**Sucesso**\n\nOperação completada\n\n**Resultado:**\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\``,
            },
          ],
        };
      } catch (error) {
        return createErrorResponse(`Operação falhou: ${error.message}`);
      }
    },
  );

  // Ferramenta 2: Apenas para usuários privilegiados
  if (PRIVILEGED_USERS.has(props.login)) {
    server.tool(
      "privilegedTool",
      "Ferramenta administrativa para usuários privilegiados",
      { action: z.string() },
      async ({ action }) => {
        // Implementação
        return {
          content: [
            {
              type: "text",
              text: `Ação de admin '${action}' executada por ${props.login}`,
            },
          ],
        };
      },
    );
  }
}

// Tarefa 3 - Atualizar Registro de Ferramentas (src/tools/register-tools.ts)
import { registerYourFeatureTools } from "./your-feature-tools";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // Registros existentes
  registerDatabaseTools(server, env, props);
  
  // Adicionar seu novo registro
  registerYourFeatureTools(server, env, props);
}

// PADRÃO: Exportar provedor OAuth com endpoints MCP
export default new OAuthProvider({
  apiHandlers: {
    "/sse": YourMCP.serveSSE("/sse") as any,
    "/mcp": YourMCP.serve("/mcp") as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### Pontos de Integração

```yaml
CLOUDFLARE_WORKERS:
  - wrangler.jsonc: Atualizar nome, variáveis de ambiente, bindings KV
  - Segredos de ambiente: Credenciais GitHub OAuth, URL do banco de dados, chave de criptografia
  - Durable Objects: Configurar binding do agente MCP para persistência de estado

GITHUB_OAUTH:
  - Aplicativo GitHub: Criar com URL de callback correspondendo ao seu domínio Workers
  - Credenciais do cliente: Armazenar como segredos Cloudflare Workers
  - URL de callback: Deve corresponder exatamente: https://seu-worker.workers.dev/callback

BANCO_DE_DADOS:
  - Conexão PostgreSQL: Usar padrões de pool de conexões existentes
  - Variável de ambiente: DATABASE_URL com string de conexão completa
  - Segurança: Usar validateSqlQuery e isWriteOperation para todo SQL

VARIÁVEIS_DE_AMBIENTE:
  - Desenvolvimento: Arquivo .dev.vars para teste local
  - Produção: Segredos Cloudflare Workers para implantação
  - Obrigatórias: GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, DATABASE_URL, COOKIE_ENCRYPTION_KEY

ARMAZENAMENTO_KV:
  - Estado OAuth: Usado pelo provedor OAuth para gerenciamento de estado
  - Namespace: Criar com `wrangler kv namespace create "OAUTH_KV"`
  - Configuração: Adicionar ID do namespace aos bindings wrangler.jsonc
```

## Portão de Validação

### Nível 1: TypeScript & Configuração

```bash
# CRÍTICO: Execute estes PRIMEIRO - corrija quaisquer erros antes de prosseguir
npm run type-check                 # Compilação TypeScript
wrangler types                     # Gerar tipos Cloudflare Workers

# Esperado: Sem erros TypeScript
# Se erros: Corrija problemas de tipo, interfaces ausentes, problemas de import
```

### Nível 2: Teste de Desenvolvimento Local

```bash
# Iniciar servidor de desenvolvimento local
wrangler dev

# Testar fluxo OAuth (deve redirecionar para GitHub)
curl -v http://localhost:8792/authorize

# Testar endpoint MCP (deve retornar informações do servidor)
curl -v http://localhost:8792/mcp

# Esperado: Servidor inicia, OAuth redireciona para GitHub, MCP responde com informações do servidor
# Se erros: Verifique saída do console, verifique variáveis de ambiente, corrija configuração
```

### Nível 3: Teste unitário de cada funcionalidade, função e arquivo, seguindo padrões de teste existentes se houver.

```bash
npm run test
```

Execute testes unitários com o comando acima (Vitest) para garantir que toda funcionalidade está funcionando.

### Nível 4: Teste de Integração de Banco de Dados (se aplicável)

```bash
# Testar conexão do banco de dados
curl -X POST http://localhost:8792/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "listTables", "arguments": {}}}'

# Testar validação de permissões
# Testar proteção contra injeção SQL e outros tipos de segurança se aplicável
# Testar tratamento de erros para falhas do banco de dados

# Esperado: Operações de banco de dados funcionam, permissões aplicadas, erros tratados graciosamente, etc.
# Se erros: Verifique DATABASE_URL, configurações de conexão, lógica de permissões
```

## Checklist Final de Validação

### Funcionalidade Principal

- [ ] Compilação TypeScript: `npm run type-check` passa
- [ ] Testes unitários passam: `npm run test` passa
- [ ] Servidor local inicia: `wrangler dev` executa sem erros
- [ ] Endpoint MCP responde: `curl http://localhost:8792/mcp` retorna informações do servidor
- [ ] Fluxo OAuth funciona: Autenticação redireciona e completa com sucesso

---

## Anti-Padrões para Evitar

### Específicos MCP

- ❌ Não pule validação de entrada com Zod - sempre valide parâmetros de ferramentas
- ❌ Não esqueça de implementar método cleanup() para Durable Objects
- ❌ Não codifique permissões de usuário - use sistemas de permissão configuráveis

### Processo de Desenvolvimento

- ❌ Não pule os loops de validação - cada nível captura problemas diferentes
- ❌ Não adivinhe sobre configuração OAuth - teste o fluxo completo
- ❌ Não implante sem monitoramento - implemente logging e rastreamento de erros
- ❌ Não ignore erros TypeScript - corrija todos os problemas de tipo antes da implantação
