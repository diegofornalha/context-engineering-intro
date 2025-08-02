# MCP Sentry Standalone

## 🚀 Instância Independente do MCP Sentry

Esta é uma instância standalone do MCP (Model Context Protocol) Sentry, configurada e validada para uso independente.

## ✅ Status de Validação

**Credenciais Validadas:**
- ✅ **DSN**: `https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334`
- ✅ **Auth Token**: Válido e funcionando
- ✅ **Organização**: `coflow` (ID: 927801)
- ✅ **API URL**: `https://sentry.io/api/0`

## 🛠️ Ferramentas Disponíveis

### SDK Tools (12 ferramentas)
- `sentry_capture_exception` - Captura e envia exceções
- `sentry_capture_message` - Captura e envia mensagens
- `sentry_add_breadcrumb` - Adiciona breadcrumbs
- `sentry_set_user` - Define contexto de usuário
- `sentry_set_tag` - Define tags
- `sentry_set_context` - Define contexto customizado
- `sentry_start_transaction` - Inicia transação de performance
- `sentry_finish_transaction` - Finaliza transação
- `sentry_start_session` - Inicia sessão (Release Health)
- `sentry_end_session` - Finaliza sessão
- `sentry_set_release` - Define versão de release
- `sentry_capture_session` - Captura sessão manual

### API Tools (15 ferramentas)
- `sentry_list_projects` - Lista projetos
- `sentry_list_issues` - Lista issues
- `sentry_create_release` - Cria release
- `sentry_list_releases` - Lista releases
- `sentry_get_organization_stats` - Estatísticas da organização
- `sentry_create_alert_rule` - Cria regra de alerta
- `sentry_resolve_short_id` - Resolve IDs curtos
- `sentry_get_event` - Obtém evento específico
- `sentry_list_error_events_in_project` - Lista eventos de erro
- `sentry_create_project` - Cria projeto
- `sentry_list_issue_events` - Lista eventos de issue
- `sentry_get_issue` - Obtém detalhes de issue
- `sentry_list_organization_replays` - Lista replays
- `sentry_setup_project` - Setup automático com DSN
- `sentry_search_errors_in_file` - Busca erros por arquivo

## 🚀 Instalação Rápida

### 1. Instalar Dependências
```bash
npm install
```

### 2. Compilar o Projeto
```bash
npm run build
```

### 3. Configurar Variáveis de Ambiente
```bash
export SENTRY_DSN="https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334"
export SENTRY_AUTH_TOKEN="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"
export SENTRY_ORG="coflow"
export SENTRY_API_URL="https://sentry.io/api/0"
```

### 4. Testar o MCP
```bash
# Listar ferramentas disponíveis
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | node dist/index.js

# Listar projetos
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sentry_list_projects", "arguments": {}}}' | node dist/index.js

# Enviar mensagem de teste
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "sentry_capture_message", "arguments": {"message": "Teste do MCP Standalone", "level": "info"}}}' | node dist/index.js
```

## 📊 Dashboard Sentry

Acesse seu dashboard em: **https://coflow.sentry.io**

## 🔧 Scripts Úteis

- `./add-to-claude-code.sh` - Adiciona MCP ao Claude Code
- `./remove-from-claude-code.sh` - Remove MCP do Claude Code
- `./start.sh` - Inicia o servidor MCP
- `npm run dev` - Modo desenvolvimento
- `npm test` - Executa testes

## 📝 Exemplos de Uso

### Capturar Exceção
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "sentry_capture_exception", "arguments": {"error": "Erro de teste", "level": "error"}}}' | node dist/index.js
```

### Listar Issues
```bash
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "sentry_list_issues", "arguments": {"projectSlug": "coflow", "query": "is:unresolved"}}}' | node dist/index.js
```

### Criar Release
```bash
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "sentry_create_release", "arguments": {"version": "myapp@1.0.0", "projects": ["coflow"]}}}' | node dist/index.js
```

## 🎯 Resultados de Teste

**Projetos Encontrados:** 1 projeto (coflow)
**Issues Ativas:** 6 issues
**Release Criado:** mcp-sentry@1.0.0
**Status:** ✅ Funcionando perfeitamente

---

**Criado em:** 02/08/2025
**Versão:** 1.0.0
**Organização:** coflow 