# Usando o MCP Sentry com API Token

## Configuração com Token

### 1. Via variáveis de ambiente (.env)

```bash
# No arquivo .env do projeto raiz
SENTRY_AUTH_TOKEN=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
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0/
SENTRY_DSN=sua-dsn-aqui
```

### 2. Via argumentos de linha de comando

```bash
./start.sh --dsn "sua-dsn" --auth-token "sntryu_102583..." --org "coflow"
```

### 3. No Claude Desktop config

```json
{
  "mcpServers": {
    "sentry": {
      "command": "node",
      "args": ["/path/to/mcp-sentry/dist/index.js"],
      "env": {
        "SENTRY_DSN": "sua-dsn-aqui",
        "SENTRY_AUTH_TOKEN": "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",
        "SENTRY_ORG": "coflow"
      }
    }
  }
}
```

## Exemplos de Uso das APIs

### Listar Projetos

```javascript
// Via MCP no Claude
await sentry_list_projects();

// Resposta:
// Found 3 projects:
// - frontend: Frontend App
// - backend: Backend API
// - mobile: Mobile App
```

### Listar Issues

```javascript
// Listar issues não resolvidas
await sentry_list_issues({
  projectSlug: "frontend",
  query: "is:unresolved"
});

// Listar erros críticos
await sentry_list_issues({
  projectSlug: "backend",
  query: "level:error is:unresolved"
});
```

### Criar Release

```javascript
// Criar novo release
await sentry_create_release({
  version: "frontend@2.0.0",
  projects: ["frontend"],
  url: "https://github.com/coflow/frontend/releases/tag/v2.0.0",
  dateReleased: new Date().toISOString()
});

// Depois de fazer deploy
await sentry_deploy_release({
  version: "frontend@2.0.0",
  environment: "production"
});
```

### Criar Alerta

```javascript
// Alerta para novos erros
await sentry_create_alert_rule({
  projectSlug: "frontend",
  name: "Alert on New Errors",
  conditions: [
    {
      id: "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition"
    }
  ],
  actions: [
    {
      id: "sentry.rules.actions.notify_event.NotifyEventAction"
    }
  ],
  frequency: 30
});

// Alerta para taxa de erro alta
await sentry_create_alert_rule({
  projectSlug: "backend",
  name: "High Error Rate Alert",
  conditions: [
    {
      id: "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
      value: 100,
      comparisonType: "count",
      interval: "1h"
    }
  ]
});
```

### Obter Estatísticas

```javascript
// Eventos recebidos nas últimas 24h
await sentry_get_organization_stats({
  stat: "received",
  since: Date.now() - 86400000, // 24h atrás
  until: Date.now(),
  resolution: "1h"
});
```

## Workflow Completo: Deploy com Monitoramento

```javascript
// 1. Criar release
const version = "myapp@1.2.0";
await sentry_create_release({
  version,
  projects: ["frontend", "backend"]
});

// 2. Fazer deploy (seu processo)
// ... código de deploy ...

// 3. Marcar deploy no Sentry
await sentry_set_release({
  release: version,
  dist: "production"
});

// 4. Iniciar sessão para monitorar
await sentry_start_session({
  release: version,
  environment: "production"
});

// 5. Criar alerta para o novo release
await sentry_create_alert_rule({
  projectSlug: "frontend",
  name: `Monitor ${version}`,
  conditions: [
    {
      id: "sentry.rules.filters.tagged_event.TaggedEventFilter",
      key: "release",
      match: "eq",
      value: version
    }
  ]
});
```

## Permissões do Token

Seu token tem as seguintes permissões:
- ✅ alerts:read, alerts:write
- ✅ event:admin, event:read, event:write
- ✅ member:admin, member:invite, member:read, member:write
- ✅ org:admin, org:integrations, org:read, org:write
- ✅ project:admin, project:read, project:releases, project:write
- ✅ team:admin, team:read, team:write

Isso permite acesso completo a todas as funcionalidades da API do Sentry!