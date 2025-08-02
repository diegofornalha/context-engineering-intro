# 🔄 Distinção Crítica: MCP Claude Code vs MCP Cursor Agent

## ⚠️ **IMPORTANTE: NÃO CONFUNDIR OS CONTEXTOS**

### **MCP Claude Code (Separado)**
- **É uma ferramenta DIFERENTE** do Cursor Agent
- Funciona no **Claude Desktop/Code**
- Tem suas próprias configurações e ferramentas
- **NÃO é o que estamos usando aqui**
- Configuração separada e independente
- Usa `claude mcp` commands

### **MCP Cursor Agent (Aqui)**
- **É o que estamos usando neste contexto**
- Integrado ao **Cursor Agent**
- Ferramentas disponíveis através do **Cursor Agent**
- **É o que importa para nosso projeto**
- Usa ferramentas `mcp_turso_*` no Cursor Agent
- Configurado via Cursor Agent

## 🎯 **Contexto do Projeto**

### **Ferramentas Disponíveis (Cursor Agent):**
- `mcp_turso_list_databases`
- `mcp_turso_execute_read_only_query`
- `mcp_turso_execute_query`
- `mcp_turso_describe_table`
- `mcp_turso_list_tables`
- `mcp_turso_add_conversation`
- `mcp_turso_get_conversations`
- `mcp_turso_add_knowledge`
- `mcp_turso_search_knowledge`
- `mcp_turso_setup_memory_tables`
- `mcp_turso_vector_search`
- `mcp_turso_generate_database_token`
- `mcp_turso_create_database`
- `mcp_turso_delete_database`

### **Configuração Atual:**
- **Servidor:** `./mcp-turso/start-claude.sh`
- **Status:** ✅ Connected
- **Banco:** context-memory
- **Organização:** diegofornalha

## 🚫 **O que NÃO fazer:**
- ❌ Confundir com MCP do Claude Code
- ❌ Usar comandos `claude mcp` neste contexto
- ❌ Misturar configurações dos dois sistemas

## ✅ **O que fazer:**
- ✅ Usar ferramentas `mcp_turso_*` do Cursor Agent
- ✅ Focar no contexto do Cursor Agent
- ✅ Manter esta distinção clara em todo o projeto

## 📝 **Nota para Desenvolvedores:**
Sempre verificar se está no contexto correto antes de usar ferramentas MCP. O Cursor Agent tem suas próprias ferramentas MCP que são diferentes do Claude Code.

---
*Documentação criada para evitar confusões futuras entre os dois sistemas MCP* 