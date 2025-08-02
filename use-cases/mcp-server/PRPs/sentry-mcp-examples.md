# Exemplos Práticos - MCP Sentry

## 🚀 Guia Rápido de Uso

### 1. Configuração Inicial

#### Passo 1: Configurar Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
SENTRY_DSN=https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334
SENTRY_AUTH_TOKEN=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
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0/
EOF
```

#### Passo 2: Instalar no Claude Code
```bash
cd /Users/agents/Desktop/context-engineering-intro/mcp-sentry
./add-to-claude-code.sh
```

### 2. Exemplos de Uso por Cenário

#### 📱 Aplicação React

##### Setup Inicial
```javascript
// 1. Configurar projeto
await mcp__sentry__sentry_setup_project({
  projectSlug: "react-app",
  platform: "javascript"
});

// 2. Implementar no React
// App.tsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_DSN_HERE",
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

##### Monitoramento de Componentes
```javascript
// Capturar erro em componente
try {
  // código que pode falhar
} catch (error) {
  await mcp__sentry__sentry_capture_exception({
    error: error.message,
    level: "error",
    tags: {
      component: "UserProfile",
      action: "fetchData"
    },
    context: {
      userId: currentUser.id,
      endpoint: "/api/profile"
    }
  });
}

// Rastrear ação do usuário
await mcp__sentry__sentry_add_breadcrumb({
  message: "User clicked save button",
  category: "ui.click",
  level: "info",
  data: {
    formId: "profile-form",
    timestamp: Date.now()
  }
});
```

#### 🖥️ API Node.js

##### Setup e Middleware
```javascript
// 1. Configurar projeto
await mcp__sentry__sentry_setup_project({
  projectSlug: "api-server",
  platform: "node"
});

// 2. Middleware Express
app.use((err, req, res, next) => {
  mcp__sentry__sentry_capture_exception({
    error: err.message,
    level: "error",
    tags: {
      endpoint: req.path,
      method: req.method,
      statusCode: res.statusCode
    },
    context: {
      request: {
        body: req.body,
        query: req.query,
        headers: req.headers
      }
    },
    user: {
      id: req.user?.id,
      email: req.user?.email
    }
  });
  
  res.status(500).json({ error: "Internal server error" });
});
```

##### Performance Monitoring
```javascript
// Monitorar endpoint crítico
app.get('/api/users/:id', async (req, res) => {
  // Iniciar transação
  await mcp__sentry__sentry_start_transaction({
    name: "GET /api/users/:id",
    op: "http.request",
    description: "Fetch user details"
  });

  try {
    const user = await db.users.findById(req.params.id);
    
    // Finalizar com sucesso
    await mcp__sentry__sentry_finish_transaction({
      status: "ok"
    });
    
    res.json(user);
  } catch (error) {
    // Finalizar com erro
    await mcp__sentry__sentry_finish_transaction({
      status: "internal_error"
    });
    
    throw error;
  }
});
```

#### 📊 Análise e Debugging

##### Investigar Issue Específico
```javascript
// 1. Buscar pelo short ID
const issue = await mcp__sentry__sentry_resolve_short_id({
  shortId: "MYAPP-123"
});

console.log(`Issue: ${issue.group.metadata.title}`);
console.log(`Status: ${issue.group.status}`);
console.log(`Users affected: ${issue.group.userCount}`);

// 2. Obter eventos do issue
const events = await mcp__sentry__sentry_list_issue_events({
  issueId: issue.groupId,
  limit: 10
});

// 3. Analisar evento específico
const eventDetails = await mcp__sentry__sentry_get_event({
  projectSlug: issue.projectSlug,
  eventId: events[0].eventID
});
```

##### Buscar Erros por Arquivo
```javascript
// Encontrar todos os erros em um componente
const errors = await mcp__sentry__sentry_search_errors_in_file({
  projectSlug: "react-app",
  filename: "components/UserProfile.tsx"
});

console.log(`Found ${errors.length} issues in UserProfile.tsx:`);
errors.forEach(error => {
  console.log(`- ${error.shortId}: ${error.title} (${error.count} events)`);
});
```

#### 🚀 Release Management

##### Deploy com Rastreamento
```javascript
// 1. Criar release antes do deploy
const version = `my-app@${process.env.BUILD_VERSION}`;

await mcp__sentry__sentry_create_release({
  version: version,
  projects: ["my-app"],
  dateReleased: new Date().toISOString(),
  url: `https://github.com/myorg/myapp/releases/tag/${version}`
});

// 2. Durante o deploy
await mcp__sentry__sentry_set_release({
  release: version,
  dist: process.env.BUILD_ID
});

// 3. Monitorar saúde da release
await mcp__sentry__sentry_start_session({
  release: version,
  environment: "production",
  distinctId: "deployment-monitor"
});
```

##### Análise Pós-Deploy
```javascript
// Verificar estatísticas após deploy
const stats = await mcp__sentry__sentry_get_organization_stats({
  stat: "received",
  resolution: "1h",
  since: new Date(Date.now() - 24*60*60*1000).toISOString() // últimas 24h
});

// Listar issues da nova release
const issues = await mcp__sentry__sentry_list_issues({
  projectSlug: "my-app",
  query: `release:${version} is:unresolved`
});
```

#### 🔔 Alertas e Monitoramento

##### Criar Alerta para Taxa de Erro
```javascript
await mcp__sentry__sentry_create_alert_rule({
  projectSlug: "my-app",
  name: "High Error Rate - Production",
  conditions: [{
    id: "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
    interval: "1h",
    value: 100,
    comparisonType: "count"
  }],
  actions: [{
    id: "sentry.rules.actions.notify_event_service.NotifyEventServiceAction",
    service: "slack",
    channel: "#alerts-production"
  }],
  frequency: 30
});
```

##### Alerta para Novo Tipo de Erro
```javascript
await mcp__sentry__sentry_create_alert_rule({
  projectSlug: "my-app",
  name: "New Error Type Detected",
  conditions: [{
    id: "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition"
  }],
  actions: [{
    id: "sentry.rules.actions.notify_event.NotifyEventAction",
    targetType: "Member",
    targetIdentifier: "tech-lead"
  }]
});
```

### 3. Workflows Completos

#### 🔍 Workflow de Investigação de Incidente

```javascript
async function investigateIncident(shortId) {
  // 1. Resolver short ID
  const issueInfo = await mcp__sentry__sentry_resolve_short_id({ shortId });
  
  // 2. Obter detalhes do issue
  const issue = await mcp__sentry__sentry_get_issue({
    issueId: issueInfo.groupId
  });
  
  // 3. Listar eventos recentes
  const events = await mcp__sentry__sentry_list_issue_events({
    issueId: issueInfo.groupId,
    limit: 5
  });
  
  // 4. Analisar padrões
  const report = {
    issue: issue.title,
    severity: issue.level,
    affectedUsers: issue.userCount,
    totalEvents: issue.count,
    firstSeen: issue.firstSeen,
    lastSeen: issue.lastSeen,
    status: issue.status,
    recentEvents: events.map(e => ({
      id: e.eventID,
      date: e.dateCreated,
      user: e.user?.email || 'anonymous'
    }))
  };
  
  return report;
}

// Uso
const report = await investigateIncident("MYAPP-456");
console.log(JSON.stringify(report, null, 2));
```

#### 📈 Workflow de Monitoramento de Saúde

```javascript
async function healthCheck(projectSlug) {
  // 1. Estatísticas gerais
  const stats = await mcp__sentry__sentry_get_organization_stats({
    stat: "received",
    resolution: "1d",
    since: new Date(Date.now() - 7*24*60*60*1000).toISOString()
  });
  
  // 2. Issues não resolvidos
  const unresolvedIssues = await mcp__sentry__sentry_list_issues({
    projectSlug,
    query: "is:unresolved level:error"
  });
  
  // 3. Releases recentes
  const releases = await mcp__sentry__sentry_list_releases({
    projectSlug
  });
  
  // 4. Gerar relatório
  return {
    errorTrend: stats,
    criticalIssues: unresolvedIssues.filter(i => i.level === 'error').length,
    totalUnresolved: unresolvedIssues.length,
    latestRelease: releases[0]?.version,
    releaseHealth: releases[0]?.newGroups || 0
  };
}

// Uso
const health = await healthCheck("my-app");
console.log(`Health Status:
- Critical Issues: ${health.criticalIssues}
- Total Unresolved: ${health.totalUnresolved}
- Latest Release: ${health.latestRelease}
- New Issues in Release: ${health.releaseHealth}`);
```

### 4. Dicas e Truques

#### 💡 Contexto Rico em Erros
```javascript
// Sempre incluir contexto máximo
await mcp__sentry__sentry_capture_exception({
  error: error.message,
  level: "error",
  tags: {
    feature: "checkout",
    paymentMethod: "credit-card",
    environment: process.env.NODE_ENV
  },
  context: {
    order: {
      id: orderId,
      total: orderTotal,
      items: itemCount
    },
    session: {
      duration: Date.now() - sessionStart,
      pageViews: pageViewCount
    }
  },
  user: {
    id: user.id,
    email: user.email,
    segment: user.isPremium ? "premium" : "free"
  }
});
```

#### 🎯 Tags Efetivas
```javascript
// Tags recomendadas para facilitar filtragem
const standardTags = {
  environment: "production",        // dev, staging, production
  feature: "user-auth",            // área funcional
  severity: "high",                // business impact
  browser: userAgent.browser,      // para apps web
  version: appVersion,             // versão do app
  customer: customerId,            // para B2B
  locale: userLocale,              // idioma/região
  experiment: abTestVariant        // para A/B tests
};
```

#### 📊 Queries Úteis
```javascript
// Issues mais frequentes
"is:unresolved sort:freq"

// Erros de hoje
"is:unresolved age:-24h"

// Erros de um usuário específico
"user.email:user@example.com"

// Erros em arquivo específico
"filename:Button.tsx"

// Erros com tag específica
"tags.feature:checkout"

// Combinações
"is:unresolved level:error tags.environment:production age:-1h"
```

### 5. Integração com CI/CD

#### GitHub Actions
```yaml
# .github/workflows/sentry-release.yml
name: Create Sentry Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Create Sentry Release
        run: |
          # Usar MCP para criar release
          npx @modelcontextprotocol/cli call sentry sentry_create_release \
            --version "${{ github.ref_name }}" \
            --projects '["my-app"]' \
            --url "https://github.com/${{ github.repository }}/releases/tag/${{ github.ref_name }}"
```

### 6. Troubleshooting Comum

#### Problema: "API client not initialized"
```javascript
// Solução: Verificar se token está configurado
if (!process.env.SENTRY_AUTH_TOKEN) {
  console.error("SENTRY_AUTH_TOKEN não configurado");
  process.exit(1);
}
```

#### Problema: "Failed to connect"
```bash
# Verificar status do MCP
claude mcp list

# Reinstalar se necessário
cd mcp-sentry
./remove-from-claude-code.sh
./add-to-claude-code.sh
```

#### Problema: Eventos não aparecem
```javascript
// Verificar DSN e flush
await mcp__sentry__sentry_capture_exception({
  error: "Test error",
  level: "error"
});

// Aguardar envio (em Node.js)
await new Promise(resolve => setTimeout(resolve, 2000));
```