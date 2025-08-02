# 🗄️ MCP Turso Server

Servidor MCP (Model Context Protocol) para integração com Turso Database, fornecendo sistema de memória persistente para agentes de IA.

## 🚀 Configuração Rápida

### 1. Instalar Dependências
```bash
npm install
```

### 2. Configurar Variáveis de Ambiente
```bash
# Configuração automática
./setup-env.sh

# Ou manualmente
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 3. Compilar e Executar
```bash
# Compilar TypeScript
npm run build

# Executar servidor
./start.sh
```

## 📋 Configuração

### Arquivo .env
O projeto usa um arquivo `.env` para gerenciar configurações:

```env
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://seu-banco-sua-org.aws-us-east-1.turso.io
TURSO_AUTH_TOKEN=seu-token-aqui

# MCP Server Configuration
MCP_SERVER_NAME=mcp-turso-memory
MCP_SERVER_VERSION=1.0.0

# Optional: Project Configuration
PROJECT_NAME=meu-projeto-memoria
PROJECT_VERSION=1.0.0
ENVIRONMENT=development
```

### Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `setup-env.sh` | Configura automaticamente o arquivo .env |
| `start.sh` | Inicia o servidor MCP |
| `npm run build` | Compila o projeto TypeScript |
| `npm run dev` | Compila e executa em modo desenvolvimento |

## 🛠️ Ferramentas MCP

O servidor fornece as seguintes ferramentas:

### Ferramentas Básicas
- `turso_list_databases` - Listar bancos de dados
- `turso_execute_query` - Executar consultas SQL
- `turso_list_tables` - Listar tabelas
- `turso_describe_table` - Descrever estrutura de tabela

### Ferramentas de Memória
- `turso_add_conversation` - Adicionar conversa
- `turso_get_conversations` - Recuperar conversas
- `turso_add_knowledge` - Adicionar conhecimento
- `turso_search_knowledge` - Pesquisar conhecimento

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
mcp-turso/
├── src/
│   └── index.ts          # Código principal do servidor
├── dist/                 # Código compilado
├── package.json          # Dependências
├── tsconfig.json         # Configuração TypeScript
├── .env                  # Variáveis de ambiente
├── .env.example          # Template de configuração
├── setup-env.sh          # Script de configuração
├── start.sh              # Script de inicialização
└── README.md             # Esta documentação
```

### Dependências Principais
- `@modelcontextprotocol/sdk` - SDK do MCP
- `@libsql/client` - Cliente Turso Database
- `dotenv` - Gerenciamento de variáveis de ambiente

### Compilação
```bash
# Desenvolvimento
npm run dev

# Produção
npm run build
npm start
```

## 🧪 Testes

### Testar Conexão
```bash
# Verificar se o servidor inicia
./start.sh

# Testar com dados de exemplo
node -e "
const { createClient } = require('@libsql/client');
const client = createClient({
  url: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN
});
client.execute('SELECT 1').then(console.log);
"
```

## 🔒 Segurança

- **Tokens**: Nunca commite tokens no Git
- **Arquivo .env**: Está no .gitignore
- **Validação**: Todas as queries são validadas
- **Erro handling**: Tratamento robusto de erros

## 🚨 Troubleshooting

### Erro: "Arquivo .env não encontrado"
```bash
./setup-env.sh
```

### Erro: "Could not parse jwt id"
- Verifique se o token está correto
- Gere um novo token: `turso db tokens create seu-banco`

### Erro: "Module not found"
```bash
npm install
npm run build
```

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se o arquivo `.env` está configurado
2. Teste a conexão com Turso CLI
3. Verifique os logs do servidor
4. Consulte a documentação do Turso

## 📄 Licença

MIT License 