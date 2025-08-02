# 🎯 Usos Práticos do MCP Sentry: Guia de Cenários

## 📋 Índice
1. [Setup e Configuração](#setup-e-configuração)
2. [Desenvolvimento Diário](#desenvolvimento-diário)
3. [Debugging e Investigação](#debugging-e-investigação)
4. [Deploy e Release Management](#deploy-e-release-management)
5. [Monitoramento em Produção](#monitoramento-em-produção)
6. [Análise de Performance](#análise-de-performance)
7. [Automação e CI/CD](#automação-e-cicd)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup e Configuração

### **Cenário: Primeira Instalação**

**Situação:** Novo desenvolvedor na equipe precisa configurar o MCP Sentry.

**Fluxo:**
```bash
# 1. Clone o repositório
git clone <repo>
cd sentry-mcp-cursor

# 2. Instalação automatizada
./add-to-cursor.sh

# 3. Verificar instalação
./test-standalone.sh

# 4. Iniciar monitoramento
./monitor.sh
```

**Ferramentas MCP utilizadas:**
```javascript
// Verificar se está funcionando
await mcp__sentry__sentry_list_projects()

// Testar captura de mensagem
await mcp__sentry__sentry_capture_message({
  message: "MCP Sentry configurado com sucesso",
  level: "info"
})
```

**Resultado:** Setup completo em menos de 2 minutos, sem erros de configuração.

---

## 💻 Desenvolvimento Diário

### **Cenário: Desenvolvendo uma Nova Feature**

**Situação:** Desenvolvedor trabalhando em uma feature de pagamento.

**Fluxo:**
```javascript
// 1. Iniciar sessão de desenvolvimento
await mcp__sentry__sentry_start_session({
  distinctId: "dev-session-123",
  release: "feature-payment-v2",
  environment: "development"
})

// 2. Adicionar breadcrumbs durante desenvolvimento
await mcp__sentry__sentry_add_breadcrumb({
  message: "Iniciando processamento de pagamento",
  category: "payment",
  data: { amount: 150.00, currency: "BRL" }
})

// 3. Capturar erros durante testes
await mcp__sentry__sentry_capture_exception({
  error: "Erro de validação de cartão",
  level: "warning",
  tags: { feature: "payment", stage: "validation" }
})

// 4. Definir contexto do usuário
await mcp__sentry__sentry_set_user({
  id: "dev-123",
  email: "dev@coflow.com",
  username: "payment-dev"
})

// 5. Finalizar sessão
await mcp__sentry__sentry_end_session({ status: "exited" })
```

**Monitoramento em tempo real:**
```bash
# Manter monitor.sh rodando em outro terminal
./monitor.sh
```

**Benefícios:**
- ✅ Rastreamento completo do desenvolvimento
- ✅ Debugging facilitado com breadcrumbs
- ✅ Contexto rico para análise posterior

---

## 🔍 Debugging e Investigação

### **Cenário: Investigando Erro em Produção**

**Situação:** Erro crítico reportado pelos usuários.

**Fluxo de Investigação:**
```javascript
// 1. Identificar o problema via short ID
const issueDetails = await mcp__sentry__sentry_resolve_short_id({
  shortId: "PROJ-123"
})

// 2. Obter detalhes completos
const fullIssue = await mcp__sentry__sentry_get_issue({
  issueId: issueDetails.issueId
})

// 3. Listar eventos relacionados
const events = await mcp__sentry__sentry_list_issue_events({
  issueId: fullIssue.id,
  limit: 50
})

// 4. Buscar erros em arquivos específicos
const fileErrors = await mcp__sentry__sentry_search_errors_in_file({
  projectSlug: "frontend",
  filename: "payment-service.js"
})

// 5. Capturar contexto da investigação
await mcp__sentry__sentry_set_context({
  name: "investigation",
  context: {
    incident_id: "INC-2024-001",
    investigator: "dev-team",
    priority: "high",
    affected_users: 150
  }
})

// 6. Marcar como investigada
await mcp__sentry__sentry_capture_message({
  message: "Issue investigada - causa identificada: timeout na API",
  level: "info",
  tags: { status: "investigated", incident: "INC-2024-001" }
})
```

**Monitoramento durante investigação:**
```bash
# Usar monitor.sh para acompanhar em tempo real
./monitor.sh
```

**Resultado:** Investigação estruturada com contexto completo para análise posterior.

---

## 🚀 Deploy e Release Management

### **Cenário: Deploy de Nova Versão**

**Situação:** Fazendo deploy da versão 2.1.0.

**Fluxo Pré-Deploy:**
```javascript
// 1. Verificar issues críticas antes do deploy
const criticalIssues = await mcp__sentry__sentry_list_issues({
  projectSlug: "frontend",
  query: "level:error is:unresolved"
})

if (criticalIssues.length > 0) {
  await mcp__sentry__sentry_capture_message({
    message: `Deploy bloqueado: ${criticalIssues.length} issues críticas`,
    level: "warning"
  })
  // Bloquear deploy
}

// 2. Criar release
await mcp__sentry__sentry_create_release({
  version: "frontend@2.1.0",
  projects: ["frontend", "backend"],
  url: "https://github.com/coflow/app/releases/tag/v2.1.0",
  dateReleased: new Date().toISOString()
})

// 3. Definir release para monitoramento
await mcp__sentry__sentry_set_release({
  release: "frontend@2.1.0"
})
```

**Fluxo Pós-Deploy:**
```javascript
// 4. Iniciar sessão de monitoramento
await mcp__sentry__sentry_start_session({
  distinctId: "deploy-2024-01-15",
  release: "frontend@2.1.0",
  environment: "production"
})

// 5. Verificar se há novos erros (após 5 minutos)
setTimeout(async () => {
  const newErrors = await mcp__sentry__sentry_list_issues({
    projectSlug: "frontend",
    query: "firstSeen:>2024-01-15T10:00:00Z level:error"
  })
  
  if (newErrors.length > 0) {
    await mcp__sentry__sentry_capture_message({
      message: `Deploy 2.1.0 introduziu ${newErrors.length} novos erros`,
      level: "warning"
    })
  }
}, 300000)

// 6. Criar alerta para novos erros
await mcp__sentry__sentry_create_alert_rule({
  projectSlug: "frontend",
  name: "Alert: New Errors in v2.1.0",
  conditions: [
    { id: "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition" }
  ],
  actions: [
    { id: "sentry.integrations.slack.notify_action.SlackNotifyServiceAction" }
  ]
})
```

**Monitoramento:**
```bash
# Acompanhar deploy via monitor
./monitor.sh
```

---

## 📊 Monitoramento em Produção

### **Cenário: Monitoramento Contínuo**

**Situação:** Monitoramento 24/7 da aplicação em produção.

**Fluxo de Monitoramento:**
```javascript
// 1. Verificar saúde geral dos projetos
const projects = await mcp__sentry__sentry_list_projects()

for (const project of projects) {
  // 2. Listar issues ativas
  const activeIssues = await mcp__sentry__sentry_list_issues({
    projectSlug: project.slug,
    query: "is:unresolved"
  })
  
  // 3. Verificar eventos recentes
  const recentEvents = await mcp__sentry__sentry_list_error_events_in_project({
    projectSlug: project.slug,
    limit: 10
  })
  
  // 4. Analisar estatísticas
  const stats = await mcp__sentry__sentry_get_organization_stats({
    stat: "received",
    since: "2024-01-01T00:00:00Z",
    until: new Date().toISOString(),
    resolution: "1d"
  })
  
  // 5. Alertar se há muitas issues
  if (activeIssues.length > 10) {
    await mcp__sentry__sentry_capture_message({
      message: `${project.name}: ${activeIssues.length} issues ativas`,
      level: "warning",
      tags: { project: project.name, alert: "high-issues" }
    })
  }
}
```

**Monitoramento Visual:**
```bash
# Manter monitor.sh rodando
./monitor.sh
```

**Benefícios:**
- ✅ Detecção proativa de problemas
- ✅ Visibilidade completa da saúde da aplicação
- ✅ Alertas automáticos para situações críticas

---

## ⚡ Análise de Performance

### **Cenário: Otimizando Performance**

**Situação:** Análise de performance do fluxo de checkout.

**Fluxo de Análise:**
```javascript
// 1. Iniciar transação de performance
await mcp__sentry__sentry_start_transaction({
  name: "checkout-flow",
  op: "http.request",
  description: "Análise completa do fluxo de checkout"
})

// 2. Adicionar breadcrumbs de performance
await mcp__sentry__sentry_add_breadcrumb({
  message: "Iniciando validação de cartão",
  category: "performance",
  data: { step: "card-validation", timestamp: Date.now() }
})

// 3. Monitorar etapas críticas
await mcp__sentry__sentry_add_breadcrumb({
  message: "Processando pagamento",
  category: "performance",
  data: { step: "payment-processing", duration: 1500 }
})

// 4. Finalizar transação
await mcp__sentry__sentry_finish_transaction({
  status: "ok"
})

// 5. Analisar replays de sessões problemáticas
const slowSessions = await mcp__sentry__sentry_list_organization_replays({
  project: "frontend",
  limit: 20,
  query: "duration:>5000" // Sessões com mais de 5s
})

// 6. Buscar erros relacionados à performance
const perfErrors = await mcp__sentry__sentry_search_errors_in_file({
  projectSlug: "frontend",
  filename: "checkout-service.js"
})
```

**Resultado:** Identificação de bottlenecks e otimizações específicas.

---

## 🤖 Automação e CI/CD

### **Cenário: Pipeline Automatizado**

**Situação:** Pipeline de CI/CD com qualidade automatizada.

**Fluxo de Qualidade:**
```javascript
// 1. Verificar qualidade antes do deploy
const preDeployCheck = async () => {
  // Listar issues críticas
  const criticalIssues = await mcp__sentry__sentry_list_issues({
    projectSlug: "frontend",
    query: "level:error is:unresolved"
  })
  
  if (criticalIssues.length > 0) {
    await mcp__sentry__sentry_capture_message({
      message: `Pipeline bloqueado: ${criticalIssues.length} issues críticas`,
      level: "error"
    })
    throw new Error(`Pipeline bloqueado: ${criticalIssues.length} issues críticas`)
  }
  
  // 2. Criar release automaticamente
  await mcp__sentry__sentry_create_release({
    version: `frontend@${process.env.BUILD_VERSION}`,
    projects: ["frontend"],
    url: process.env.BUILD_URL
  })
  
  // 3. Configurar monitoramento
  await mcp__sentry__sentry_setup_project({
    projectSlug: "frontend",
    platform: "javascript"
  })
}

// 4. Monitoramento pós-deploy
const postDeployMonitoring = async () => {
  // Aguardar e verificar novos erros
  setTimeout(async () => {
    const newErrors = await mcp__sentry__sentry_list_issues({
      projectSlug: "frontend",
      query: `firstSeen:>${new Date().toISOString()} level:error`
    })
    
    if (newErrors.length > 0) {
      await mcp__sentry__sentry_capture_message({
        message: `Deploy ${process.env.BUILD_VERSION} introduziu ${newErrors.length} novos erros`,
        level: "warning"
      })
    }
  }, 300000) // 5 minutos
}
```

**Integração com CI/CD:**
```bash
# No pipeline
./add-to-cursor.sh  # Configurar MCP
npm test           # Testes
preDeployCheck()   # Verificação de qualidade
deploy()           # Deploy
postDeployMonitoring() # Monitoramento
```

---

## 🔧 Troubleshooting

### **Cenário: Problemas de Configuração**

**Situação:** MCP não está funcionando corretamente.

**Fluxo de Diagnóstico:**
```bash
# 1. Verificar status do servidor
./monitor.sh

# 2. Verificar configuração
cat .cursor/mcp.json

# 3. Testar conexão
./test-standalone.sh

# 4. Verificar logs
tail -f logs/mcp-sentry.log
```

**Problemas Comuns:**

**Problema:** Servidor MCP não inicia
```bash
# Solução:
cd sentry-mcp-cursor
npm install
npm run build
./start-cursor.sh
```

**Problema:** Configuração não encontrada
```bash
# Solução:
./add-to-cursor.sh
# Reiniciar Cursor
```

**Problema:** Credenciais inválidas
```bash
# Solução:
# Verificar config.env
cat config.env
# Atualizar credenciais se necessário
```

---

## 📈 Métricas e KPIs

### **Métricas Importantes:**

1. **Tempo de Resolução de Issues**
   - Issues resolvidas por dia
   - Tempo médio de resolução

2. **Qualidade de Releases**
   - Novos erros por release
   - Rollbacks necessários

3. **Performance**
   - Transações lentas
   - Sessões problemáticas

4. **Cobertura de Monitoramento**
   - Projetos monitorados
   - Ferramentas utilizadas

### **Relatórios Automatizados:**
```javascript
// Relatório semanal
const weeklyReport = async () => {
  const stats = await mcp__sentry__sentry_get_organization_stats({
    stat: "received",
    since: "7d",
    resolution: "1d"
  })
  
  const issues = await mcp__sentry__sentry_list_issues({
    projectSlug: "frontend",
    query: "firstSeen:>7d"
  })
  
  await mcp__sentry__sentry_capture_message({
    message: `Relatório Semanal: ${stats.length} eventos, ${issues.length} issues`,
    level: "info"
  })
}
```

---

## 🎯 Conclusão

O MCP Sentry com as melhorias implementadas oferece:

- ✅ **Setup automatizado** e sem erros
- ✅ **Monitoramento em tempo real** via `monitor.sh`
- ✅ **27 ferramentas** para todos os cenários
- ✅ **Configuração flexível** via `config.env`
- ✅ **Troubleshooting facilitado**
- ✅ **Integração perfeita** com Cursor

**Transforme seu desenvolvimento com observabilidade completa!** 🚀 