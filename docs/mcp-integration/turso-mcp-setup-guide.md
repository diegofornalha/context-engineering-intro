# 🚀 Guia de Configuração do MCP Turso no Claude Code

## 📋 Visão Geral

O servidor MCP Turso permite integração direta entre o Claude Code e bancos de dados Turso, oferecendo operações de leitura, escrita e gerenciamento de bancos de dados.

## ✅ Status Atual

O servidor MCP Turso está **configurado e funcionando** no Claude Code! 

```bash
# Verificar status
claude mcp list

# Resultado:
mcp-turso-cloud: node /Users/agents/Desktop/context-engineering-intro/mcp-turso/dist/index.js - ✓ Connected
```

## 🔧 Como Foi Configurado

### 1. Compilação do Projeto
```bash
cd mcp-turso
npm install
npm run build
```

### 2. Adição ao Claude Code
```bash
claude mcp add mcp-turso-cloud node /Users/agents/Desktop/context-engineering-intro/mcp-turso/dist/index.js \
  --env TURSO_API_TOKEN="seu-turso-api-token" \
  --env TURSO_ORGANIZATION="sua-organizacao" \
  --env TURSO_DEFAULT_DATABASE="seu-database-padrao"
```

## 🔑 Configuração de Credenciais

### Obter Token da API Turso

1. **Acesse o Dashboard Turso**
   - Vá para [https://turso.tech](https://turso.tech)
   - Faça login em sua conta

2. **Navegue até Settings**
   - Clique em seu perfil (canto superior direito)
   - Selecione "Settings"

3. **Gere um Token de API**
   - Vá para a seção "API Tokens"
   - Clique em "Create Token"
   - Dê um nome descritivo (ex: "claude-code-integration")
   - Copie o token gerado

4. **Anote sua Organização**
   - Na página principal do dashboard
   - Veja o nome da sua organização no topo

### Atualizar Configuração

Para atualizar as credenciais:

1. Remova a configuração atual:
```bash
claude mcp remove mcp-turso-cloud
```

2. Adicione novamente com suas credenciais reais:
```bash
claude mcp add mcp-turso-cloud node /Users/agents/Desktop/context-engineering-intro/mcp-turso/dist/index.js \
  --env TURSO_API_TOKEN="seu-token-real-aqui" \
  --env TURSO_ORGANIZATION="sua-organizacao-real" \
  --env TURSO_DEFAULT_DATABASE="nome-do-database-padrao"
```

## 🛠️ Ferramentas Disponíveis

### Operações de Organização
- `list_databases` - Listar todos os bancos de dados
- `create_database` - Criar novo banco de dados
- `delete_database` - Deletar banco de dados
- `generate_database_token` - Gerar token para banco específico

### Operações de Banco de Dados
- `list_tables` - Listar tabelas em um banco
- `execute_read_only_query` - Executar queries SELECT/PRAGMA
- `execute_query` - Executar queries de modificação
- `describe_table` - Obter schema de uma tabela
- `vector_search` - Busca por similaridade vetorial

## 📝 Exemplos de Uso

### Listar Bancos de Dados
```
Usar ferramenta: list_databases
```

### Executar Query de Leitura
```
Usar ferramenta: execute_read_only_query
Parâmetros:
- query: "SELECT * FROM users LIMIT 10"
- database: "meu-database"
```

### Criar Novo Banco
```
Usar ferramenta: create_database
Parâmetros:
- name: "novo-database"
- regions: ["iad", "fra"]
```

## ⚠️ Segurança

- **Queries Destrutivas**: O servidor separa operações de leitura e escrita
- **Tokens**: Nunca compartilhe seus tokens de API
- **Permissões**: Configure tokens com permissões mínimas necessárias

## 🐛 Troubleshooting

### Erro de Autenticação
- Verifique se o token está correto
- Confirme o nome da organização
- Certifique-se que o token tem as permissões necessárias

### Erro de Conexão
- Verifique conexão com internet
- Confirme que o banco de dados existe
- Verifique nome do banco está correto

## 📚 Recursos Adicionais

- [Documentação Turso](https://docs.turso.tech)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Código Fonte](https://github.com/diegofornalha/mcp-turso-cloud)

---

**Status**: ✅ Configurado e Funcionando
**Última Atualização**: 02/08/2025