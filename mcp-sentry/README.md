# 🚀 MCP Sentry - Model Context Protocol Server

Um servidor MCP completo para integração com Sentry, oferecendo 27 ferramentas para monitoramento de erros, performance e saúde de aplicações.

## ✨ Características

- **27 Ferramentas Completas**: 12 SDK + 15 API
- **Release Health**: Monitoramento completo de sessões
- **Performance Monitoring**: Transações e spans
- **Alertas Customizados**: Regras de alerta automatizadas
- **Busca Avançada**: Por arquivo, short ID, queries complexas
- **Setup Automático**: Configuração de projetos com um comando

## 🛠️ Instalação Rápida

### 1. Clone e Configure
```bash
cd /Users/agents/Desktop/context-engineering-intro/mcp-sentry
npm install
npm run build
```

### 2. Configure as Credenciais
```bash
# Edite config.env com suas credenciais
nano config.env
```

### 3. Adicione ao Claude Code
```bash
./add-to-claude-code.sh
```

## 📚 Scripts Disponíveis

### 🚀 Inicialização
- `./start.sh` - Inicia o servidor MCP padrão
- `./start-standalone.sh` - Inicia com validações e status detalhado
- `./start-mcp.sh` - Inicia com configurações hardcoded

### 🧪 Testes e Monitoramento
- `./test-standalone.sh` - Executa suite completa de testes
- `./monitor.sh` - Monitor em tempo real com estatísticas

### 🔧 Gerenciamento
- `./add-to-claude-code.sh` - Adiciona ao Claude Code
- `./remove-from-claude-code.sh` - Remove do Claude Code

## 🎯 Ferramentas Disponíveis

### SDK Tools (12)
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
12. `sentry_capture_session` - Captura sessão

### API Tools (15)
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

## 💡 Exemplos de Uso

### Captura de Erro com Contexto Rico
```javascript
await mcp__sentry__sentry_capture_exception({
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
});
```

### Setup Automático de Projeto
```javascript
await mcp__sentry__sentry_setup_project({
  projectSlug: "my-app",
  platform: "javascript"
});
// Retorna DSN e instruções de instalação
```

### Investigar Issue por Short ID
```javascript
await mcp__sentry__sentry_resolve_short_id({
  shortId: "MYAPP-123"
});
// Retorna detalhes completos do issue
```

### Monitoramento de Performance
```javascript
// Iniciar transação
await mcp__sentry__sentry_start_transaction({
  name: "api.request",
  op: "http.request"
});

// Finalizar transação
await mcp__sentry__sentry_finish_transaction({
  status: "ok"
});
```

## 📊 Monitoramento

Execute o monitor em tempo real:
```bash
./monitor.sh
```

Exibe:
- Status do servidor
- Estatísticas das últimas 24h
- Issues não resolvidas
- Última release
- Atualização automática a cada 30s

## 🧪 Testes

Execute a suite completa de testes:
```bash
./test-standalone.sh
```

Testa:
- Listagem de ferramentas
- Captura de mensagens
- Listagem de projetos/issues
- Criação de releases
- Performance monitoring
- Breadcrumbs

## 🔍 Troubleshooting

### Servidor não conecta
```bash
# Verificar status
claude mcp list

# Reinstalar
./remove-from-claude-code.sh
./add-to-claude-code.sh
```

### Variáveis não configuradas
```bash
# Verificar config.env
cat config.env

# Testar standalone
./start-standalone.sh
```

### Erros de compilação
```bash
# Limpar e recompilar
rm -rf node_modules dist
npm install
npm run build
```

## 📝 Configuração

### config.env
```bash
SENTRY_DSN=https://[key]@[org].ingest.sentry.io/[project]
SENTRY_AUTH_TOKEN=sntryu_[token]
SENTRY_ORG=your-org
SENTRY_API_URL=https://sentry.io/api/0/
SENTRY_RELEASE=mcp-sentry@1.0.0
SENTRY_ENVIRONMENT=production
```

## 🔗 Links Úteis

- [Documentação Sentry](https://docs.sentry.io)
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
- [Dashboard Sentry](https://sentry.io)

## 📄 Licença

MIT

---

Desenvolvido com ❤️ para Claude Code