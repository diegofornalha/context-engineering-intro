# PRPs - MCP Sentry Server

## Padrões, Referências e Práticas

### 📋 Visão Geral

O MCP Sentry é um servidor Model Context Protocol que integra completamente com o Sentry, oferecendo 27 ferramentas para monitoramento de erros, performance e saúde de aplicações.

### 🎯 Padrões de Implementação

#### 1. Estrutura do Projeto
```
mcp-sentry/
├── src/
│   ├── index.ts           # Servidor principal MCP
│   ├── sentry-api-client.ts # Cliente API Sentry
│   └── types.ts           # Tipos TypeScript
├── dist/                  # Código compilado
├── package.json
├── tsconfig.json
├── .env                   # Configurações
├── start-mcp.sh          # Script de inicialização
└── add-to-claude-code.sh # Script de instalação
```

#### 2. Configuração de Ambiente
```bash
# .env
SENTRY_DSN=https://[key]@[org].ingest.sentry.io/[project]
SENTRY_AUTH_TOKEN=sntryu_[token]
SENTRY_ORG=your-org
SENTRY_API_URL=https://sentry.io/api/0/
```

#### 3. Inicialização do Servidor
```typescript
// Dupla inicialização: SDK + API
const sentryInitialized = initializeSentry(config); // SDK
const apiClient = new SentryAPIClient({ authToken, org }); // API
```

### 🔧 Referências Técnicas

#### Ferramentas SDK (12)
1. `sentry_capture_exception` - Captura exceções
2. `sentry_capture_message` - Captura mensagens
3. `sentry_add_breadcrumb` - Adiciona breadcrumbs
4. `sentry_set_user` - Define usuário
5. `sentry_set_tag` - Define tags
6. `sentry_set_context` - Define contexto
7. `sentry_start_transaction` - Inicia transação
8. `sentry_finish_transaction` - Finaliza transação
9. `sentry_start_session` - Inicia sessão
10. `sentry_end_session` - Finaliza sessão
11. `sentry_set_release` - Define release
12. `sentry_capture_session` - Captura sessão manual

#### Ferramentas API (15)
1. `sentry_list_projects` - Lista projetos
2. `sentry_list_issues` - Lista issues
3. `sentry_create_release` - Cria release
4. `sentry_list_releases` - Lista releases
5. `sentry_get_organization_stats` - Estatísticas
6. `sentry_create_alert_rule` - Cria alertas
7. `sentry_resolve_short_id` - Resolve IDs curtos
8. `sentry_get_event` - Obtém evento
9. `sentry_list_error_events_in_project` - Lista erros
10. `sentry_create_project` - Cria projeto
11. `sentry_list_issue_events` - Lista eventos de issue
12. `sentry_get_issue` - Obtém issue
13. `sentry_list_organization_replays` - Lista replays
14. `sentry_setup_project` - Setup de projeto
15. `sentry_search_errors_in_file` - Busca erros em arquivo

### 💡 Práticas Recomendadas

#### 1. Instalação no Claude Code
```bash
# Método recomendado
cd /path/to/mcp-sentry
./add-to-claude-code.sh

# Verificar status
claude mcp list
```

#### 2. Uso de Ferramentas

##### Captura de Erros
```javascript
// Melhor prática: incluir contexto completo
mcp_sentry_capture_exception({
  error: "Database connection failed",
  level: "error",
  tags: {
    component: "database",
    environment: "production"
  },
  context: {
    database: {
      host: "db.example.com",
      attempt: 3
    }
  },
  user: {
    id: "user123",
    email: "user@example.com"
  }
})
```

##### Release Health
```javascript
// Iniciar sessão no início da aplicação
mcp_sentry_start_session({
  distinctId: "user123",
  environment: "production",
  release: "1.0.0"
})

// Finalizar com status apropriado
mcp_sentry_end_session({
  status: "exited" // ou "crashed", "abnormal", "errored"
})
```

##### Performance Monitoring
```javascript
// Iniciar transação
mcp_sentry_start_transaction({
  name: "api.request",
  op: "http.request",
  description: "GET /api/users"
})

// Finalizar com status
mcp_sentry_finish_transaction({
  status: "ok"
})
```

#### 3. Fluxos de Trabalho

##### Setup Inicial de Projeto
```javascript
// 1. Criar projeto
mcp_sentry_create_project({
  name: "My App",
  slug: "my-app",
  platform: "javascript",
  team: "frontend-team"
})

// 2. Obter DSN e instruções
mcp_sentry_setup_project({
  projectSlug: "my-app",
  platform: "javascript"
})

// 3. Criar release inicial
mcp_sentry_create_release({
  version: "my-app@1.0.0",
  projects: ["my-app"]
})
```

##### Investigação de Erros
```javascript
// 1. Buscar erros em arquivo específico
mcp_sentry_search_errors_in_file({
  projectSlug: "my-app",
  filename: "Button.tsx"
})

// 2. Resolver short ID
mcp_sentry_resolve_short_id({
  shortId: "MYAPP-123"
})

// 3. Obter detalhes do issue
mcp_sentry_get_issue({
  issueId: "123456789"
})

// 4. Listar eventos do issue
mcp_sentry_list_issue_events({
  issueId: "123456789",
  limit: 10
})
```

### 🚀 Casos de Uso Avançados

#### 1. Monitoramento Completo de Deploy
```javascript
// Antes do deploy
const release = await mcp_sentry_create_release({
  version: "my-app@2.0.0",
  projects: ["my-app"],
  dateReleased: new Date().toISOString()
});

// Durante o deploy
await mcp_sentry_set_release({
  release: "my-app@2.0.0"
});

// Após o deploy
await mcp_sentry_start_session({
  release: "my-app@2.0.0",
  environment: "production"
});
```

#### 2. Alertas Customizados
```javascript
mcp_sentry_create_alert_rule({
  projectSlug: "my-app",
  name: "High Error Rate Alert",
  conditions: [{
    id: "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
    interval: "1h",
    value: 100
  }],
  actions: [{
    id: "sentry.rules.actions.notify_event.NotifyEventAction",
    targetType: "Member",
    targetIdentifier: "team-lead"
  }],
  frequency: 30
})
```

#### 3. Análise de Performance
```javascript
// Obter estatísticas
const stats = await mcp_sentry_get_organization_stats({
  stat: "received",
  resolution: "1h",
  since: "2024-01-01T00:00:00Z"
});

// Analisar tendências de erros
const projectStats = await apiClient.getProjectStats(
  "my-app",
  "received",
  { resolution: "1d", period: "30d" }
);
```

### 📊 Métricas e KPIs

#### Métricas Recomendadas
1. **Taxa de Crash** - `crashed_sessions / total_sessions`
2. **Taxa de Adoção** - `users_with_sessions / total_users`
3. **Estabilidade** - `healthy_sessions / total_sessions`
4. **MTTR** - Tempo médio para resolver issues
5. **Volume de Erros** - Erros por período

#### Dashboard Sugerido
```javascript
// Coletar métricas principais
const metrics = {
  projects: await mcp_sentry_list_projects(),
  recentIssues: await mcp_sentry_list_issues({ 
    projectSlug: "my-app",
    query: "is:unresolved" 
  }),
  stats: await mcp_sentry_get_organization_stats({
    stat: "received",
    resolution: "1d"
  }),
  releases: await mcp_sentry_list_releases({
    projectSlug: "my-app"
  })
};
```

### 🛡️ Segurança e Compliance

#### Boas Práticas
1. **Nunca commitar** `.env` ou credenciais
2. **Usar variáveis de ambiente** para configurações sensíveis
3. **Rotacionar tokens** regularmente
4. **Limitar escopo** dos tokens às operações necessárias
5. **Sanitizar dados** antes de enviar ao Sentry

#### Configuração Segura
```bash
# start-mcp.sh com validação
#!/bin/bash
if [ -z "$SENTRY_DSN" ]; then
  echo "Error: SENTRY_DSN not set"
  exit 1
fi

if [ -z "$SENTRY_AUTH_TOKEN" ]; then
  echo "Error: SENTRY_AUTH_TOKEN not set"
  exit 1
fi
```

### 🔄 Manutenção e Troubleshooting

#### Comandos Úteis
```bash
# Verificar logs
npm run build && node dist/index.js

# Testar conexão
claude mcp list

# Recompilar após mudanças
npm run build

# Limpar e reinstalar
rm -rf node_modules dist
npm install
npm run build
```

#### Problemas Comuns
1. **"Failed to connect"** - Verificar caminho do script e permissões
2. **"API error 401"** - Token inválido ou expirado
3. **"DSN not provided"** - Configurar variáveis de ambiente
4. **Timeout** - Verificar conectividade com Sentry

### 📚 Recursos Adicionais

- [Documentação Sentry](https://docs.sentry.io)
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
- [Sentry API Reference](https://docs.sentry.io/api/)
- [Release Health Guide](https://docs.sentry.io/product/releases/health/)

### 🎯 Roadmap Futuro

1. **Formatação de Output** - Suporte para markdown/plain
2. **Modo Debug** - Logs detalhados opcionais
3. **Cache Inteligente** - Reduzir chamadas API
4. **Webhooks** - Integração com Sentry webhooks
5. **Batch Operations** - Operações em lote