# 🚀 MCP Sentry para Cursor

Configuração do MCP Sentry para funcionar no Cursor IDE.

## ✅ Status

O MCP Sentry está **totalmente configurado** e funcionando no Cursor com todas as 27 ferramentas disponíveis.

## 📁 Arquivos de Configuração

### Cursor MCP Config
**Localização**: `/Users/agents/Desktop/context-engineering-intro/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "sentry": {
      "type": "stdio",
      "command": "./mcp-sentry/start-cursor.sh",
      "args": []
    },
    "turso": {
      "type": "stdio",
      "command": "./mcp-turso-cloud/start-claude.sh",
      "args": []
    }
  }
}
```

### Script de Inicialização
**Arquivo**: `mcp-sentry/start-cursor.sh`
- Configura variáveis de ambiente
- Compila o projeto se necessário
- Inicia o servidor MCP

## 🛠️ Instalação

### Opção 1: Script Automático
```bash
cd /Users/agents/Desktop/context-engineering-intro/mcp-sentry
./add-to-cursor.sh
```

### Opção 2: Manual
1. Certifique-se que o projeto está compilado:
   ```bash
   npm install
   npm run build
   ```

2. A configuração já está em `.cursor/mcp.json`

3. Reinicie o Cursor

## 🧪 Teste

Para verificar se está funcionando:
```bash
./test-cursor.sh
```

Deve retornar `27` (número de ferramentas disponíveis).

## 📚 Ferramentas Disponíveis

### SDK Tools (12)
- `sentry_capture_exception` - Captura exceções
- `sentry_capture_message` - Envia mensagens
- `sentry_add_breadcrumb` - Adiciona contexto
- `sentry_set_user` - Define usuário
- `sentry_set_tag` - Define tags
- `sentry_set_context` - Contexto customizado
- `sentry_start_transaction` - Performance monitoring
- `sentry_finish_transaction` - Finaliza transação
- `sentry_start_session` - Inicia sessão
- `sentry_end_session` - Finaliza sessão
- `sentry_set_release` - Define release
- `sentry_capture_session` - Captura sessão manual

### API Tools (15)
- `sentry_list_projects` - Lista projetos
- `sentry_list_issues` - Lista issues
- `sentry_create_release` - Cria releases
- `sentry_list_releases` - Lista releases
- `sentry_get_organization_stats` - Estatísticas
- `sentry_create_alert_rule` - Cria alertas
- `sentry_resolve_short_id` - Resolve IDs curtos
- `sentry_get_event` - Obtém evento específico
- `sentry_list_error_events_in_project` - Lista erros
- `sentry_create_project` - Cria projeto
- `sentry_list_issue_events` - Lista eventos de issue
- `sentry_get_issue` - Obtém issue
- `sentry_list_organization_replays` - Lista replays
- `sentry_setup_project` - Configura projeto
- `sentry_search_errors_in_file` - Busca erros em arquivo

## 💡 Como Usar no Cursor

1. **Reinicie o Cursor** após a configuração

2. **Use comandos naturais**:
   - "Use the sentry tool to list all projects"
   - "Capture an exception with sentry"
   - "Show me recent issues from sentry"

3. **Exemplos específicos**:
   ```
   Use sentry_list_projects to show all projects
   Use sentry_list_issues with projectSlug "coflow" 
   Use sentry_capture_message to send "Test from Cursor"
   ```

## 🔧 Configuração

### Variáveis de Ambiente
Definidas em `start-cursor.sh`:
- `SENTRY_DSN` - DSN do projeto
- `SENTRY_AUTH_TOKEN` - Token de autenticação
- `SENTRY_ORG` - Organização (coflow)
- `SENTRY_API_URL` - URL da API

### Credenciais
As credenciais estão configuradas no script e apontam para:
- **Organização**: coflow
- **Projeto**: Configurado via DSN

## 🐛 Troubleshooting

### Servidor não conecta
1. Verifique se o projeto está compilado:
   ```bash
   cd mcp-sentry
   npm run build
   ```

2. Teste diretamente:
   ```bash
   ./test-cursor.sh
   ```

### Ferramentas não aparecem
1. Reinicie o Cursor
2. Verifique o arquivo `.cursor/mcp.json`
3. Confirme que o caminho está correto

## 📝 Notas

- O mesmo servidor funciona tanto no Claude Code quanto no Cursor
- As 27 ferramentas estão disponíveis em ambos
- A configuração é persistente no diretório `.cursor/`