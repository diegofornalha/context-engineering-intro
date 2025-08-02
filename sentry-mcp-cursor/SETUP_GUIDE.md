# Guia de Configuração Real - MCP Sentry

## 🎯 **Visão Geral**

**Organização:** coflow  
**Projeto:** MCP Sentry  
**Versão:** 0.1.0  
**Status:** ✅ Funcionando e Validado  
**Plataforma:** TypeScript/Node.js  

## 📋 **Pré-requisitos**

- **Node.js:** 16.x ou superior
- **npm:** 8.x ou superior
- **Git:** Para clonar o repositório
- **Sentry Account:** Conta ativa em https://sentry.io

## 🚀 **Instalação Rápida**

### 1. **Clonar e Configurar**

```bash
# Navegar para a pasta standalone
cd sentry-mcp-standalone

# Instalar dependências
npm install

# Compilar o projeto
npm run build
```

### 2. **Configurar Variáveis de Ambiente**

As configurações já estão validadas no arquivo `config.env`:

```bash
# Carregar configurações
source config.env

# Verificar se as variáveis estão carregadas
echo $SENTRY_DSN
echo $SENTRY_ORG
```

### 3. **Testar a Instalação**

```bash
# Executar testes completos
./test-standalone.sh
```

## ⚙️ **Configuração Detalhada**

### **Credenciais Validadas**

```bash
# DSN do Sentry (funcionando)
SENTRY_DSN=https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334

# Token de Autenticação (funcionando)
SENTRY_AUTH_TOKEN=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

# Organização
SENTRY_ORG=coflow

# API URL
SENTRY_API_URL=https://sentry.io/api/0
```

### **Arquivo de Configuração**

O arquivo `config.env` já contém todas as configurações necessárias:

```bash
# Sentry MCP Standalone Configuration
SENTRY_DSN=https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334
SENTRY_AUTH_TOKEN=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
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0
SENTRY_RELEASE=mcp-sentry-standalone@1.0.0
SENTRY_ENVIRONMENT=production
SENTRY_DEBUG=false
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0.1
SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0
```

## 🔧 **Scripts de Autostart**

### **Script de Inicialização**

```bash
#!/bin/bash
# start-mcp-sentry.sh

echo "🚀 Iniciando MCP Sentry..."
cd /Users/agents/Desktop/context-engineering-intro/sentry-mcp-standalone

# Carregar configurações
source config.env

# Verificar se o projeto foi compilado
if [ ! -d "dist" ]; then
    echo "📦 Compilando projeto..."
    npm run build
fi

# Iniciar o servidor MCP
echo "🔧 Iniciando servidor MCP..."
node dist/index.js
```

### **Script de Teste**

```bash
#!/bin/bash
# test-mcp-sentry.sh

echo "🧪 Testando MCP Sentry..."
cd /Users/agents/Desktop/context-engineering-intro/sentry-mcp-standalone

# Executar testes
./test-standalone.sh
```

### **Script de Integração com Claude**

```bash
#!/bin/bash
# integrate-claude.sh

echo "🔗 Integrando com Claude..."
cd /Users/agents/Desktop/context-engineering-intro/sentry-mcp-standalone

# Adicionar ao Claude Code
./add-to-claude-code.sh
```

## 🛠️ **Ferramentas Disponíveis (27 ferramentas)**

### **SDK Tools (12 ferramentas)**

#### 1. **sentry_capture_exception**
```json
{
  "name": "sentry_capture_exception",
  "arguments": {
    "error": "Erro crítico na aplicação",
    "level": "error",
    "tags": {"component": "api", "user_id": "123"},
    "user": {"id": "123", "email": "user@example.com"}
  }
}
```

#### 2. **sentry_capture_message**
```json
{
  "name": "sentry_capture_message",
  "arguments": {
    "message": "Operação concluída com sucesso",
    "level": "info",
    "tags": {"operation": "user_login"}
  }
}
```

#### 3. **sentry_add_breadcrumb**
```json
{
  "name": "sentry_add_breadcrumb",
  "arguments": {
    "message": "Usuário clicou no botão de login",
    "category": "ui",
    "level": "info",
    "data": {"button_id": "login-btn"}
  }
}
```

#### 4. **sentry_set_user**
```json
{
  "name": "sentry_set_user",
  "arguments": {
    "id": "user123",
    "email": "user@example.com",
    "username": "john_doe",
    "ip_address": "192.168.1.1"
  }
}
```

#### 5. **sentry_set_tag**
```json
{
  "name": "sentry_set_tag",
  "arguments": {
    "key": "environment",
    "value": "production"
  }
}
```

#### 6. **sentry_set_context**
```json
{
  "name": "sentry_set_context",
  "arguments": {
    "name": "request_data",
    "context": {
      "method": "POST",
      "url": "/api/users",
      "headers": {"content-type": "application/json"}
    }
  }
}
```

#### 7. **sentry_start_transaction**
```json
{
  "name": "sentry_start_transaction",
  "arguments": {
    "name": "user_registration",
    "op": "http.request",
    "description": "Processamento de registro de usuário"
  }
}
```

#### 8. **sentry_finish_transaction**
```json
{
  "name": "sentry_finish_transaction",
  "arguments": {
    "status": "ok"
  }
}
```

#### 9. **sentry_start_session**
```json
{
  "name": "sentry_start_session",
  "arguments": {
    "distinctId": "user123",
    "sessionId": "session_001",
    "release": "myapp@1.0.0",
    "environment": "production"
  }
}
```

#### 10. **sentry_end_session**
```json
{
  "name": "sentry_end_session",
  "arguments": {
    "status": "exited"
  }
}
```

#### 11. **sentry_set_release**
```json
{
  "name": "sentry_set_release",
  "arguments": {
    "release": "myapp@2.0.0",
    "dist": "production"
  }
}
```

#### 12. **sentry_capture_session**
```json
{
  "name": "sentry_capture_session",
  "arguments": {
    "sessionId": "session_001",
    "distinctId": "user123",
    "status": "ok",
    "duration": 300,
    "errors": 0
  }
}
```

### **API Tools (15 ferramentas)**

#### 13. **sentry_list_projects**
```json
{
  "name": "sentry_list_projects",
  "arguments": {}
}
```

#### 14. **sentry_list_issues**
```json
{
  "name": "sentry_list_issues",
  "arguments": {
    "projectSlug": "coflow",
    "query": "is:unresolved level:error"
  }
}
```

#### 15. **sentry_create_release**
```json
{
  "name": "sentry_create_release",
  "arguments": {
    "version": "myapp@2.0.0",
    "projects": ["coflow"],
    "url": "https://github.com/coflow/myapp/releases/tag/v2.0.0",
    "dateReleased": "2025-02-08T00:00:00.000Z"
  }
}
```

#### 16. **sentry_list_releases**
```json
{
  "name": "sentry_list_releases",
  "arguments": {
    "projectSlug": "coflow"
  }
}
```

#### 17. **sentry_get_organization_stats**
```json
{
  "name": "sentry_get_organization_stats",
  "arguments": {
    "stat": "received",
    "since": "2025-02-01T00:00:00.000Z",
    "until": "2025-02-08T00:00:00.000Z",
    "resolution": "1h"
  }
}
```

#### 18. **sentry_create_alert_rule**
```json
{
  "name": "sentry_create_alert_rule",
  "arguments": {
    "projectSlug": "coflow",
    "name": "High Error Rate Alert",
    "conditions": [
      {
        "id": "sentry.rules.conditions.event_frequency.EventFrequencyCondition",
        "value": 100,
        "comparisonType": "count",
        "interval": "1h"
      }
    ],
    "actions": [
      {
        "id": "sentry.rules.actions.notify_event.NotifyEventAction"
      }
    ],
    "frequency": 30
  }
}
```

#### 19. **sentry_resolve_short_id**
```json
{
  "name": "sentry_resolve_short_id",
  "arguments": {
    "shortId": "COFLOW-123"
  }
}
```

#### 20. **sentry_get_event**
```json
{
  "name": "sentry_get_event",
  "arguments": {
    "projectSlug": "coflow",
    "eventId": "event_id_here"
  }
}
```

#### 21. **sentry_list_error_events_in_project**
```json
{
  "name": "sentry_list_error_events_in_project",
  "arguments": {
    "projectSlug": "coflow",
    "limit": 50,
    "query": "level:error"
  }
}
```

#### 22. **sentry_create_project**
```json
{
  "name": "sentry_create_project",
  "arguments": {
    "name": "Novo Projeto",
    "slug": "novo-projeto",
    "platform": "javascript",
    "team": "team-slug"
  }
}
```

#### 23. **sentry_list_issue_events**
```json
{
  "name": "sentry_list_issue_events",
  "arguments": {
    "issueId": "issue_id_here",
    "limit": 50
  }
}
```

#### 24. **sentry_get_issue**
```json
{
  "name": "sentry_get_issue",
  "arguments": {
    "issueId": "issue_id_here"
  }
}
```

#### 25. **sentry_list_organization_replays**
```json
{
  "name": "sentry_list_organization_replays",
  "arguments": {
    "project": "coflow",
    "limit": 50,
    "query": "has:error"
  }
}
```

#### 26. **sentry_setup_project**
```json
{
  "name": "sentry_setup_project",
  "arguments": {
    "projectSlug": "coflow",
    "platform": "javascript"
  }
}
```

#### 27. **sentry_search_errors_in_file**
```json
{
  "name": "sentry_search_errors_in_file",
  "arguments": {
    "projectSlug": "coflow",
    "filename": "src/components/Button.tsx"
  }
}
```

## 🔗 **Integração com Claude**

### **Claude Desktop**

1. **Editar configuração:**
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Adicionar configuração:**
   ```json
   {
     "mcpServers": {
       "sentry": {
         "command": "/Users/agents/Desktop/context-engineering-intro/sentry-mcp-standalone/start.sh",
         "args": [],
         "env": {
           "SENTRY_DSN": "https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334",
           "SENTRY_AUTH_TOKEN": "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",
           "SENTRY_ORG": "coflow",
           "SENTRY_API_URL": "https://sentry.io/api/0/"
         }
       }
     }
   }
   ```

### **Claude Code**

```bash
# Usar o script automático
./add-to-claude-code.sh

# Ou manualmente
claude mcp add sentry ./start.sh
```

## 🧪 **Testes e Validação**

### **Teste Rápido**

```bash
# Executar todos os testes
./test-standalone.sh
```

### **Teste Manual**

```bash
# Listar ferramentas
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js

# Enviar mensagem de teste
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sentry_capture_message", "arguments": {"message": "Teste manual", "level": "info"}}}' | node dist/index.js
```

## 🚨 **Troubleshooting**

### **Problemas Comuns**

#### **Erro: "Sentry is not initialized"**
```bash
# Solução: Carregar variáveis de ambiente
source config.env
```

#### **Erro: "Sentry API client not initialized"**
```bash
# Solução: Verificar token de autenticação
echo $SENTRY_AUTH_TOKEN
```

#### **Erro: "Project not found"**
```bash
# Solução: Verificar slug do projeto
echo $SENTRY_ORG
```

### **Logs e Debug**

```bash
# Ativar modo debug
export SENTRY_DEBUG=true

# Ver logs do servidor
node dist/index.js 2>&1 | tee sentry-mcp.log
```

## 🔐 **Segurança**

### **Boas Práticas**

1. **Token de Autenticação:**
   - Nunca commitar tokens no código
   - Usar variáveis de ambiente
   - Rotacionar tokens regularmente

2. **DSN:**
   - Usar DSN público (não contém secrets)
   - Configurar rate limiting se necessário

3. **Acesso:**
   - Limitar permissões do token
   - Usar tokens específicos por projeto

### **Configuração Segura**

```bash
# Criar arquivo .env.local (não versionado)
cp config.env .env.local

# Editar com suas credenciais
nano .env.local
```

## 📊 **Monitoramento**

### **Dashboard Sentry**

- **URL:** https://coflow.sentry.io
- **Organização:** coflow
- **Projeto:** coflow

### **Métricas Importantes**

- **Issues Ativas:** 8 issues monitoradas
- **Releases:** Múltiplos releases criados
- **Performance:** Transações monitoradas
- **Sessões:** Release Health ativo

## 🎯 **Próximos Passos**

1. **Configurar Alertas:**
   ```bash
   # Criar alerta para novos erros
   # Use sentry_create_alert_rule
   ```

2. **Monitorar Performance:**
   ```bash
   # Iniciar transações
   # Use sentry_start_transaction
   ```

3. **Release Health:**
   ```bash
   # Configurar sessões
   # Use sentry_start_session
   ```

4. **Integração Contínua:**
   ```bash
   # Adicionar ao CI/CD
   # Use sentry_create_release
   ```

---

**Guia gerado em:** 02/08/2025  
**Versão:** 1.0.0  
**Status:** ✅ Testado e Validado  
**Organização:** coflow 