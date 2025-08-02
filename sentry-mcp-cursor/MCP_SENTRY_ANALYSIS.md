# Análise Completa do MCP Sentry

## 📊 **Resumo Executivo**

**Versão:** 0.1.0  
**Total de Ferramentas:** 27  
**Categorias:** SDK Tools (12) + API Tools (15)  
**Status:** ✅ Funcionando e Validado  
**Organização:** coflow  

## 🏗️ **Arquitetura do Sistema**

### **Componentes Principais**
- **Server:** MCP Server com transporte stdio
- **Sentry SDK:** Integração com @sentry/node
- **API Client:** Cliente REST para Sentry API
- **Tool Handlers:** 27 ferramentas implementadas

### **Configuração**
```typescript
interface SentryConfig {
  dsn?: string;
  environment?: string;
  release?: string;
  tracesSampleRate?: number;
  debug?: boolean;
}
```

## 🛠️ **Ferramentas SDK (12 ferramentas)**

### 1. **sentry_capture_exception**
**Descrição:** Captura e envia exceções para o Sentry
**Parâmetros:**
- `error` (string, obrigatório): Mensagem ou descrição do erro
- `level` (string, opcional): Nível de severidade (fatal, error, warning, info, debug)
- `tags` (object, opcional): Pares chave-valor para marcar o erro
- `context` (object, opcional): Dados de contexto adicionais
- `user` (object, opcional): Informações do usuário

**Exemplo:**
```json
{
  "name": "sentry_capture_exception",
  "arguments": {
    "error": "Erro de conexão com banco de dados",
    "level": "error",
    "tags": {"component": "database", "operation": "query"},
    "user": {"id": "user123", "email": "user@example.com"}
  }
}
```

### 2. **sentry_capture_message**
**Descrição:** Captura e envia mensagens para o Sentry
**Parâmetros:**
- `message` (string, obrigatório): Mensagem para enviar
- `level` (string, opcional): Nível de severidade
- `tags` (object, opcional): Tags para a mensagem
- `context` (object, opcional): Contexto adicional

### 3. **sentry_add_breadcrumb**
**Descrição:** Adiciona breadcrumb para contexto de debugging
**Parâmetros:**
- `message` (string, obrigatório): Mensagem do breadcrumb
- `category` (string, opcional): Categoria do breadcrumb
- `level` (string, opcional): Nível de severidade
- `data` (object, opcional): Dados adicionais

### 4. **sentry_set_user**
**Descrição:** Define contexto do usuário para o Sentry
**Parâmetros:**
- `id` (string, opcional): ID do usuário
- `email` (string, opcional): Email do usuário
- `username` (string, opcional): Nome de usuário
- `ip_address` (string, opcional): Endereço IP
- `segment` (string, opcional): Segmento do usuário

### 5. **sentry_set_tag**
**Descrição:** Define uma tag que será enviada com todos os eventos
**Parâmetros:**
- `key` (string, obrigatório): Chave da tag
- `value` (string, obrigatório): Valor da tag

### 6. **sentry_set_context**
**Descrição:** Define dados de contexto customizados
**Parâmetros:**
- `name` (string, obrigatório): Nome do contexto
- `context` (object, obrigatório): Dados do contexto

### 7. **sentry_start_transaction**
**Descrição:** Inicia uma transação de monitoramento de performance
**Parâmetros:**
- `name` (string, obrigatório): Nome da transação
- `op` (string, obrigatório): Tipo de operação (http.request, db.query, etc.)
- `description` (string, opcional): Descrição da transação

### 8. **sentry_finish_transaction**
**Descrição:** Finaliza a transação atual
**Parâmetros:**
- `status` (string, opcional): Status da transação (ok, cancelled, etc.)

### 9. **sentry_start_session**
**Descrição:** Inicia uma nova sessão para monitoramento de Release Health
**Parâmetros:**
- `distinctId` (string, opcional): Identificador único do usuário
- `sessionId` (string, opcional): ID customizado da sessão
- `release` (string, opcional): Versão do release
- `environment` (string, opcional): Nome do ambiente

### 10. **sentry_end_session**
**Descrição:** Finaliza a sessão atual com um status específico
**Parâmetros:**
- `status` (string, opcional): Como a sessão terminou (exited, crashed, abnormal, errored)

### 11. **sentry_set_release**
**Descrição:** Define a versão do release para tracking de Release Health
**Parâmetros:**
- `release` (string, obrigatório): Versão do release (ex: myapp@1.0.0)
- `dist` (string, opcional): Identificador de distribuição

### 12. **sentry_capture_session**
**Descrição:** Captura uma sessão manualmente para modo servidor/request
**Parâmetros:**
- `sessionId` (string, obrigatório): Identificador único da sessão
- `distinctId` (string, opcional): Identificador do usuário
- `status` (string, opcional): Status da sessão
- `duration` (number, opcional): Duração da sessão em segundos
- `errors` (number, opcional): Número de erros na sessão

## 🌐 **Ferramentas API (15 ferramentas)**

### 13. **sentry_list_projects**
**Descrição:** Lista todos os projetos da organização
**Parâmetros:** Nenhum
**Retorna:** Lista de projetos com slug, nome e ID

### 14. **sentry_list_issues**
**Descrição:** Lista issues de um projeto
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto
- `query` (string, opcional): Query de busca (ex: is:unresolved, level:error)

### 15. **sentry_create_release**
**Descrição:** Cria um novo release
**Parâmetros:**
- `version` (string, obrigatório): Versão do release (ex: myapp@1.0.0)
- `projects` (array, opcional): Lista de slugs de projetos
- `url` (string, opcional): URL do release
- `dateReleased` (string, opcional): Data do release (formato ISO)

### 16. **sentry_list_releases**
**Descrição:** Lista releases de um projeto
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto

### 17. **sentry_get_organization_stats**
**Descrição:** Obtém estatísticas da organização
**Parâmetros:**
- `stat` (string, obrigatório): Tipo de estatística (received, rejected, blacklisted)
- `since` (string, opcional): Data inicial (formato ISO ou timestamp)
- `until` (string, opcional): Data final (formato ISO ou timestamp)
- `resolution` (string, opcional): Resolução temporal (10s, 1h, 1d)

### 18. **sentry_create_alert_rule**
**Descrição:** Cria uma regra de alerta para um projeto
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto
- `name` (string, obrigatório): Nome da regra de alerta
- `conditions` (array, opcional): Condições do alerta
- `actions` (array, opcional): Ações do alerta
- `frequency` (number, opcional): Frequência de verificação em minutos

### 19. **sentry_resolve_short_id**
**Descrição:** Recupera detalhes sobre um issue usando seu short ID
**Parâmetros:**
- `shortId` (string, obrigatório): Short ID do issue (ex: PROJ-123)

### 20. **sentry_get_event**
**Descrição:** Recupera um evento específico do Sentry
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto
- `eventId` (string, obrigatório): ID do evento

### 21. **sentry_list_error_events_in_project**
**Descrição:** Lista eventos de erro de um projeto específico
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto
- `limit` (number, opcional): Número de eventos a retornar
- `query` (string, opcional): Query de busca

### 22. **sentry_create_project**
**Descrição:** Cria um novo projeto no Sentry
**Parâmetros:**
- `name` (string, obrigatório): Nome do projeto
- `slug` (string, obrigatório): Slug do projeto (identificador URL-friendly)
- `platform` (string, opcional): Plataforma (javascript, python, node)
- `team` (string, obrigatório): Slug do time

### 23. **sentry_list_issue_events**
**Descrição:** Lista eventos de um issue específico
**Parâmetros:**
- `issueId` (string, obrigatório): ID do issue
- `limit` (number, opcional): Número de eventos a retornar

### 24. **sentry_get_issue**
**Descrição:** Recupera e analisa um issue do Sentry
**Parâmetros:**
- `issueId` (string, obrigatório): ID ou URL do issue

### 25. **sentry_list_organization_replays**
**Descrição:** Lista replays de uma organização
**Parâmetros:**
- `project` (string, opcional): ID ou slug do projeto
- `limit` (number, opcional): Número de replays a retornar
- `query` (string, opcional): Query de busca

### 26. **sentry_setup_project**
**Descrição:** Configura Sentry para um projeto retornando DSN e instruções
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto
- `platform` (string, opcional): Plataforma para instruções de instalação

### 27. **sentry_search_errors_in_file**
**Descrição:** Busca erros do Sentry ocorrendo em um arquivo específico
**Parâmetros:**
- `projectSlug` (string, obrigatório): Slug/identificador do projeto
- `filename` (string, obrigatório): Caminho ou nome do arquivo

## 🔧 **Funções Utilitárias**

### **mapSeverityLevel**
**Descrição:** Mapeia níveis de severidade string para Sentry.SeverityLevel
**Parâmetros:**
- `level` (string): Nível de severidade
**Retorna:** Sentry.SeverityLevel

### **initializeSentry**
**Descrição:** Inicializa Sentry com configuração ou variáveis de ambiente
**Parâmetros:**
- `config` (SentryConfig, opcional): Configuração do Sentry
**Retorna:** boolean

## 🚨 **Tratamento de Erros**

### **McpError**
**Descrição:** Erro customizado para erros internos do servidor MCP
**Uso:**
```typescript
throw new McpError(ErrorCode.InternalError, "Mensagem de erro");
```

### **Validações**
- Verificação de inicialização do Sentry
- Validação de parâmetros obrigatórios
- Tratamento de erros da API do Sentry

## 🔐 **Autenticação e Configuração**

### **Variáveis de Ambiente**
- `SENTRY_DSN`: Data Source Name do Sentry
- `SENTRY_AUTH_TOKEN`: Token de autenticação da API
- `SENTRY_ORG`: Slug da organização
- `SENTRY_API_URL`: URL base da API (padrão: https://sentry.io/api/0)

### **Argumentos de Linha de Comando**
- `--dsn`: DSN do Sentry
- `--auth-token`: Token de autenticação
- `--org`: Slug da organização
- `--environment`: Ambiente
- `--release`: Versão do release
- `--debug`: Modo debug

## 📊 **Exemplos de Uso**

### **Capturar Exceção**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "sentry_capture_exception",
    "arguments": {
      "error": "Erro crítico na aplicação",
      "level": "error",
      "tags": {"component": "api", "user_id": "123"},
      "user": {"id": "123", "email": "user@example.com"}
    }
  }
}
```

### **Listar Projetos**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "sentry_list_projects",
    "arguments": {}
  }
}
```

### **Criar Release**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "sentry_create_release",
    "arguments": {
      "version": "myapp@2.0.0",
      "projects": ["coflow"],
      "url": "https://github.com/coflow/myapp/releases/tag/v2.0.0"
    }
  }
}
```

## 🎯 **Status de Implementação**

### **✅ Funcionando (27/27)**
- Todas as 27 ferramentas implementadas
- Testadas e validadas
- Integração completa com Sentry SDK e API
- Tratamento de erros robusto
- Documentação completa

### **🔗 Dashboard**
- **URL:** https://coflow.sentry.io
- **Organização:** coflow
- **Projetos:** 1 projeto ativo
- **Issues:** 8 issues monitoradas

---

**Análise gerada em:** 02/08/2025  
**Versão do código:** 0.1.0  
**Total de ferramentas:** 27  
**Status:** ✅ Completo e Funcional 