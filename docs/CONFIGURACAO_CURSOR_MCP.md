# 🔧 Configuração do Cursor para MCP Agente PRP

## 📋 **Visão Geral**

Este guia mostra como configurar o Cursor IDE para usar o MCP do agente PRP, permitindo integração completa entre desenvolvimento e análise de PRPs.

## 🎯 **Arquitetura de Integração**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cursor IDE    │    │   MCP PRP       │    │   MCP Turso     │
│                 │    │   Agent         │    │                 │
│ • Comandos      │◄──►│ • Ferramentas   │◄──►│ • Banco de      │
│ • Extensões     │    │ • Análise LLM   │    │   Dados         │
│ • Interface     │    │ • Conversação   │    │ • Persistência  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 **Passo 1: Configurar MCP Servers**

### 1.1 Localizar arquivo de configuração do Cursor

```bash
# macOS
~/.cursor/mcp_servers.json

# Linux
~/.cursor/mcp_servers.json

# Windows
%APPDATA%\Cursor\mcp_servers.json
```

### 1.2 Criar/editar arquivo de configuração

```json
{
  "mcpServers": {
    "turso": {
      "command": "node",
      "args": ["/Users/agents/Desktop/context-engineering-intro/mcp-turso-cloud/dist/index.js"],
      "env": {
        "TURSO_API_TOKEN": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
        "TURSO_ORGANIZATION": "diegofornalha",
        "TURSO_DEFAULT_DATABASE": "context-memory"
      }
    },
    "prp-agent": {
      "command": "python",
      "args": ["/Users/agents/Desktop/context-engineering-intro/prp-agent/mcp_server.py"],
      "env": {
        "LLM_PROVIDER": "openai",
        "LLM_API_KEY": "sua_chave_openai_aqui",
        "LLM_MODEL": "gpt-4",
        "LLM_BASE_URL": "https://api.openai.com/v1",
        "DATABASE_PATH": "/Users/agents/Desktop/context-engineering-intro/context-memory.db"
      }
    },
    "sentry": {
      "command": "node",
      "args": ["/Users/agents/Desktop/context-engineering-intro/sentry-mcp-cursor/dist/index.js"],
      "env": {
        "SENTRY_AUTH_TOKEN": "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",
        "SENTRY_ORG": "coflow",
        "SENTRY_API_URL": "https://sentry.io/api/0/"
      }
    }
  }
}
```

## 🚀 **Passo 2: Instalar Dependências**

### 2.1 Instalar MCP Python

```bash
cd prp-agent
source venv/bin/activate
pip install mcp
```

### 2.2 Verificar instalação

```bash
# Testar se o MCP está funcionando
python -c "import mcp; print('MCP instalado com sucesso!')"
```

## 🧪 **Passo 3: Testar MCP**

### 3.1 Testar servidor MCP localmente

```bash
cd prp-agent
source venv/bin/activate

# Testar servidor MCP
python mcp_server.py
```

### 3.2 Testar com cliente MCP

```bash
# Em outro terminal
python -m mcp.client stdio --server prp-agent

# Testar ferramentas
# Listar ferramentas disponíveis
# Chamar prp_create, prp_search, etc.
```

## 💻 **Passo 4: Usar no Cursor**

### 4.1 Comandos disponíveis no Cursor

Após configurar o MCP, você pode usar os seguintes comandos no Cursor:

#### **Criar PRP:**
```
/prp create
- name: "sistema-autenticacao"
- title: "Sistema de Autenticação JWT"
- description: "Implementar sistema de autenticação com JWT"
- objective: "Permitir login seguro de usuários"
```

#### **Buscar PRPs:**
```
/prp search
- query: "autenticação"
- status: "active"
- limit: 5
```

#### **Analisar PRP:**
```
/prp analyze
- prp_id: 1
- analysis_type: "task_extraction"
```

#### **Conversar com Agente:**
```
/prp chat
- message: "Analise este código e crie um PRP"
- context: "Arquivo: auth.js"
```

### 4.2 Exemplos de uso prático

#### **Exemplo 1: Criar PRP do arquivo atual**
```
1. Abrir arquivo no Cursor
2. Selecionar código relevante
3. Usar comando: /prp create
4. Preencher informações do PRP
5. Agente analisa e cria PRP automaticamente
```

#### **Exemplo 2: Analisar PRP existente**
```
1. Usar comando: /prp search
2. Encontrar PRP desejado
3. Usar comando: /prp analyze
4. Agente extrai tarefas e insights
5. Resultados salvos no banco
```

#### **Exemplo 3: Conversa natural**
```
1. Usar comando: /prp chat
2. Perguntar: "Como melhorar este PRP?"
3. Agente analisa e sugere melhorias
4. Contexto mantido na conversa
```

## 🔧 **Passo 5: Configurações Avançadas**

### 5.1 Configurar atalhos de teclado

Adicionar ao `keybindings.json` do Cursor:

```json
[
  {
    "key": "ctrl+shift+p",
    "command": "workbench.action.quickOpen",
    "args": {
      "value": "/prp"
    }
  },
  {
    "key": "ctrl+shift+r",
    "command": "workbench.action.quickOpen",
    "args": {
      "value": "/prp create"
    }
  }
]
```

### 5.2 Configurar snippets

Adicionar ao `snippets.json`:

```json
{
  "PRP Template": {
    "prefix": "prp",
    "body": [
      "name: \"$1\"",
      "title: \"$2\"",
      "description: \"$3\"",
      "objective: \"$4\"",
      "priority: \"medium\"",
      "tags: \"$5\""
    ],
    "description": "Template para criar PRP"
  }
}
```

## 📊 **Passo 6: Monitoramento e Debug**

### 6.1 Verificar logs do MCP

```bash
# Verificar se MCP está rodando
ps aux | grep mcp_server.py

# Verificar logs do Cursor
tail -f ~/.cursor/logs/main.log
```

### 6.2 Testar conectividade

```bash
# Testar conexão com MCP Turso
curl -X POST http://localhost:8080/tools/list

# Testar agente PRP
python -c "
from agents.agent import chat_with_prp_agent
import asyncio
result = asyncio.run(chat_with_prp_agent('Teste de conectividade'))
print(result)
"
```

## 🎯 **Fluxo de Trabalho Integrado**

### **Desenvolvimento com Cursor + MCP:**

1. **Escrever código** no Cursor
2. **Detectar padrões** automaticamente
3. **Sugerir criação** de PRP
4. **Analisar com LLM** via agente
5. **Extrair tarefas** automaticamente
6. **Salvar no banco** via MCP Turso
7. **Mostrar progresso** no Cursor

### **Análise Automática:**

1. **Arquivo salvo** no Cursor
2. **MCP detecta** mudanças
3. **Agente analisa** automaticamente
4. **Atualiza PRP** no banco
5. **Notifica** desenvolvedor

## 🎉 **Benefícios Alcançados**

### ✅ **Para o Desenvolvedor:**
- **Análise Automática** - PRPs criados automaticamente
- **Contexto Persistente** - Histórico mantido no banco
- **Insights Inteligentes** - LLM analisa e sugere melhorias
- **Integração Nativa** - Funciona dentro do Cursor

### ✅ **Para o Projeto:**
- **Rastreabilidade** - Todo desenvolvimento documentado
- **Qualidade** - Análise LLM constante
- **Produtividade** - Automação de tarefas repetitivas
- **Colaboração** - Dados compartilhados via MCP

## 🔧 **Troubleshooting**

### **Problema: MCP não conecta**
```bash
# Verificar se servidor está rodando
ps aux | grep mcp_server.py

# Verificar configuração
cat ~/.cursor/mcp_servers.json

# Testar manualmente
python mcp_server.py
```

### **Problema: Ferramentas não aparecem**
```bash
# Verificar logs do Cursor
tail -f ~/.cursor/logs/main.log

# Reiniciar Cursor
# Verificar se MCP está listado em Settings > MCP
```

### **Problema: Erro de permissão**
```bash
# Verificar permissões do arquivo
chmod +x mcp_server.py

# Verificar se venv está ativo
source venv/bin/activate
```

## 🚀 **Próximos Passos**

1. **Testar integração** completa
2. **Adicionar mais ferramentas** ao MCP
3. **Criar extensão Cursor** customizada
4. **Implementar análise automática** de arquivos
5. **Adicionar dashboard** de métricas

---

**Status:** ✅ **Configuração Completa**
**Próximo:** Testar integração no Cursor 