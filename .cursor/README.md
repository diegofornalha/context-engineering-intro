# Configuração MCP (Model Context Protocol) para Cursor

Este documento detalha a configuração do servidor MCP Sentry customizado para uso com o Cursor neste projeto.

## Entendendo o MCP (Model Context Protocol)

O MCP é um protocolo que permite que agentes de IA (como o Claude ou o Cursor) utilizem ferramentas externas. Ele padroniza como aplicativos fornecem contexto e ferramentas para LLMs (Large Language Models). Pense no MCP como um sistema de plugins que estende as capacidades do Agente, conectando-o a várias fontes de dados e ferramentas.

## Configuração do Servidor Sentry MCP

### 1.1 Entendendo o Sentry MCP
O Sentry MCP customizado permite usar funcionalidades do Sentry (monitoramento de erros, performance, releases) como ferramentas para LLMs através do protocolo MCP.

### 1.2 Configuração do Arquivo MCP
Para o Cursor reconhecer o servidor MCP, criamos um arquivo de configuração no diretório do projeto:
```
.cursor/mcp.json
```

Com o seguinte conteúdo:
```json
{
  "mcpServers": {
    "sentry": {
      "type": "stdio",
      "command": "./sentry-mcp-standalone/start-cursor.sh",
      "args": []
    }
  }
}
```

**Nota:** As variáveis de ambiente são definidas diretamente no script `start-cursor.sh` para garantir que sejam carregadas corretamente pelo Cursor.

### 1.3 Script Wrapper para Cursor
Criamos um script wrapper específico (`start-cursor.sh`) que:
- Define as variáveis de ambiente diretamente
- Garante que o diretório correto seja usado
- Compila o projeto se necessário
- Inicia o servidor MCP

### 1.4 Ferramentas Disponíveis
O servidor Sentry MCP customizado oferece **27 ferramentas** divididas em duas categorias:

#### Ferramentas SDK (12 ferramentas):
- `sentry_capture_exception` - Capturar exceções
- `sentry_capture_message` - Capturar mensagens
- `sentry_add_breadcrumb` - Adicionar breadcrumbs
- `sentry_set_user` - Definir contexto do usuário
- `sentry_set_tag` - Definir tags
- `sentry_set_context` - Definir contexto customizado
- `sentry_start_transaction` - Iniciar transação de performance
- `sentry_finish_transaction` - Finalizar transação
- `sentry_start_session` - Iniciar sessão
- `sentry_end_session` - Finalizar sessão
- `sentry_set_release` - Definir versão de release
- `sentry_capture_session` - Capturar sessão manualmente

#### Ferramentas API (15 ferramentas):
- `sentry_list_projects` - Listar projetos
- `sentry_list_issues` - Listar issues
- `sentry_create_release` - Criar releases
- `sentry_list_releases` - Listar releases
- `sentry_get_organization_stats` - Estatísticas da organização
- `sentry_create_alert_rule` - Criar regras de alerta
- `sentry_resolve_short_id` - Resolver IDs curtos
- `sentry_get_event` - Obter eventos específicos
- `sentry_list_error_events_in_project` - Listar eventos de erro
- `sentry_create_project` - Criar projetos
- `sentry_list_issue_events` - Listar eventos de issues
- `sentry_get_issue` - Obter detalhes de issues
- `sentry_list_organization_replays` - Listar replays
- `sentry_setup_project` - Configurar projetos
- `sentry_search_errors_in_file` - Buscar erros em arquivos

## 2. Uso do Servidor MCP no Cursor

### 2.1 Verificação das Ferramentas no Cursor
Após reiniciar o Cursor, você pode verificar se as ferramentas estão disponíveis:

1. Abra o Cursor e vá para a página de Configurações (Settings)
2. Na seção "Developer" ou "MCP", você deve ver "sentry" listado nos servidores MCP
3. Ao usar o chat do Cursor, você deve ver um ícone de ferramentas indicando que ferramentas MCP estão disponíveis

### 2.2 Exemplos de Uso
```bash
# Listar projetos no Sentry
Use a ferramenta sentry_list_projects para listar os projetos da organização

# Capturar uma mensagem de teste
Use sentry_capture_message com a mensagem "Teste do Cursor MCP" e nível "info"

# Listar issues de um projeto
Use sentry_list_issues com projectSlug "coflow" para listar issues não resolvidas
```

## 3. Solução de Problemas

### 3.1 Erros Comuns e Soluções

- **Erro "Sentry DSN not provided"**:
  - Verifique se o script `start-cursor.sh` tem permissões de execução
  - Confirme que as variáveis estão definidas no script

- **Erro "No tools or prompts"**:
  - Reinicie o Cursor completamente
  - Verifique se o caminho do script está correto
  - Teste manualmente o script: `echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | ./sentry-mcp-standalone/start-cursor.sh`

- **Erro de autenticação**:
  - Verifique se o token de autenticação está válido no script
  - Confirme se a organização está correta

### 3.2 Teste Manual
Para testar se o servidor MCP está funcionando:
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | ./sentry-mcp-standalone/start-cursor.sh
```

## 4. Configuração Global vs. Projeto

**Configuração Local (Recomendada):**
- Arquivo: `.cursor/mcp.json` (este projeto)
- Escopo: Apenas este projeto
- Vantagens: Versionável, compartilhável, isolado

**Configuração Global:**
- Arquivo: `~/.cursor/mcp.json`
- Escopo: Todos os projetos
- Vantagens: Disponível em todos os projetos

## 5. Referências

- [Documentação do Model Context Protocol (MCP)](https://docs.cursor.com/context/model-context-protocol)
- [Blog do Sentry sobre MCP e Cursor](https://blog.sentry.io/smarter-debugging-sentry-mcp-cursor/)
- [Cursor Directory - Sentry MCP](https://cursor.directory/mcp/sentry) 