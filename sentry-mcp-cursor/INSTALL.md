# Instalação do MCP Sentry no Claude Desktop

## 1. Localizar arquivo de configuração

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

## 2. Adicionar configuração

Abra o arquivo e adicione/mescle com a configuração existente:

```json
{
  "mcpServers": {
    "sentry": {
      "command": "/Users/agents/Desktop/context-engineering-intro/mcp-sentry/start.sh",
      "args": [],
      "env": {
        "SENTRY_DSN": "ADICIONE_SUA_DSN_AQUI",
        "SENTRY_AUTH_TOKEN": "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",
        "SENTRY_ORG": "coflow",
        "SENTRY_API_URL": "https://sentry.io/api/0/"
      }
    }
  }
}
```

## 3. Substituir DSN

Substitua `ADICIONE_SUA_DSN_AQUI` pelo DSN do seu projeto Sentry:
- Acesse https://coflow.sentry.io
- Vá em Settings > Projects > Seu Projeto > Client Keys (DSN)
- Copie o DSN e cole no lugar

## 4. Reiniciar Claude Desktop

Após salvar o arquivo, reinicie o Claude Desktop para carregar o servidor MCP.

## 5. Verificar instalação

No Claude, você pode verificar se o servidor está funcionando tentando usar uma ferramenta:

```
Use a ferramenta sentry_list_projects para listar os projetos
```

## Solução de Problemas

### Se não funcionar:

1. **Verifique o caminho:** O caminho do comando deve ser absoluto
2. **Verifique permissões:** O arquivo start.sh deve ser executável
3. **Verifique logs:** Procure por erros nos logs do Claude Desktop
4. **Teste manualmente:**
   ```bash
   cd /Users/agents/Desktop/context-engineering-intro/mcp-sentry
   ./start.sh --dsn "sua-dsn-aqui"
   ```