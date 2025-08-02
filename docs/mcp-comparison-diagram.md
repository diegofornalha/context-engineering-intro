# 🔵 Diagrama de Arquitetura: Claude Code MCP Sentry

## Diagrama de Arquitetura e Componentes

![Diagrama Claude Code MCP Sentry](claude-code.png)

## 📋 Análise Detalhada do Diagrama

### 🎯 **Visão Geral**
O diagrama mostra a arquitetura completa do **Claude Code MCP Sentry**, ilustrando como os componentes se interconectam para fornecer 27 ferramentas de monitoramento e observabilidade.

---

## 🏗️ **Componentes Principais**

### 1. **📜 Scripts de Gerenciamento (Seção Superior)**
**Localização:** Retângulo azul claro na parte superior

**Scripts Disponíveis:**
- `start.sh` - Script principal de inicialização
- `start-mcp.sh` - Inicialização específica do MCP
- `start-standalone.sh` - Modo autônomo
- `test-standalone.sh` - Testes da versão autônoma
- `monitor.sh` - Monitoramento em tempo real
- `add-to-claude-code.sh` - Adicionar ao Claude Code
- `remove-from-claude-code.sh` - Remover do Claude Code

### 2. **⚙️ Configuração (Seção Esquerda)**
**Localização:** Retângulo amarelo claro

**Arquivos de Configuração:**
- `config.env` - Variáveis de ambiente principais
- `.env` - Variáveis de ambiente alternativas
- **Hardcoded env vars** - Variáveis embutidas no código

**Fluxo:** `start.sh` → `config.env` e `.env`

### 3. **🧠 Núcleo Central - index.ts**
**Localização:** Retângulo verde claro no centro

**Características:**
- **27 ferramentas** integradas
- Ponto central de toda a lógica
- Recebe configurações dos scripts
- Expõe ferramentas via prefixo `mcp__sentry__`

### 4. **🔧 Módulos Internos**
**Localização:** Caixas azuis claras abaixo do index.ts

**Componentes:**
- `sentry-api-client.ts` - Cliente para API do Sentry
- `types.ts` - Definições de tipos TypeScript

---

## 🛠️ **Ferramentas Disponíveis**

### **SDK Tools (12 ferramentas)**
**Localização:** Caixa verde clara no lado direito

**Ferramentas Principais:**
- `capture_exception` - Captura de exceções
- `capture_message` - Captura de mensagens
- `add_breadcrumb` - Trilhas de eventos
- `set_user/tag/context` - Definição de contexto
- `start/finish_transaction` - Monitoramento de performance
- `start/end_session` - Gestão de sessões

### **API Tools (15 ferramentas)**
**Localização:** Caixa verde clara conectada às SDK Tools

**Ferramentas Principais:**
- `list_projects/issues` - Listagem de projetos e issues
- `create/list_releases` - Gestão de releases
- `resolve_short_id` - Resolução de IDs curtos
- `get_event/issue` - Obtenção de detalhes
- `setup_project` - Configuração de projetos
- `search_errors_in_file` - Busca de erros por arquivo

---

## ☁️ **Integração Sentry Cloud**

### **Serviços Sentry (Seção Inferior)**
**Localização:** Retângulo marrom na parte inferior

**Componentes:**
- `API Sentry` - Interface de programação
- `SDK Sentry` - Kit de desenvolvimento
- `Dashboard coflow.sentry.io` - Painel de controle

**Conexões:**
- `sentry-api-client.ts` → `API Sentry`
- `types.ts` → `SDK Sentry`

---

## 📝 **Configuração Global**

### **Arquivo de Registro**
**Localização:** Retângulo amarelo claro no canto superior direito

**Componente:** `~/.claude.json`

**Função:** 
- Registro global do MCP no Claude Code
- Configuração via `add-to-claude-code.sh`
- Prefixo `mcp__sentry__` para acesso às ferramentas

---

## 🔄 **Fluxo de Execução**

```
1. Scripts de Inicialização (start.sh, start-mcp.sh)
   ↓
2. Carregamento de Configuração (config.env, .env)
   ↓
3. Inicialização do Núcleo (index.ts)
   ↓
4. Carregamento de Módulos (sentry-api-client.ts, types.ts)
   ↓
5. Conexão com Sentry Cloud (API + SDK)
   ↓
6. Exposição de 27 Ferramentas (12 SDK + 15 API)
   ↓
7. Acesso via Prefixo mcp__sentry__
```

---

## 🎯 **Características Técnicas**

### **Arquitetura:**
- ✅ **Modular** - Componentes bem separados
- ✅ **Configurável** - Múltiplas opções de configuração
- ✅ **Extensível** - 27 ferramentas disponíveis
- ✅ **Integrado** - Conexão completa com Sentry

### **Funcionalidades:**
- 🔍 **Monitoramento** - Captura de erros e eventos
- 📊 **Performance** - Transações e métricas
- 👥 **Contexto** - Informações de usuário e sessão
- 🚀 **Releases** - Gestão de versões
- 🔧 **API Completa** - Acesso a todos os recursos Sentry

---

## 💡 **Benefícios da Arquitetura**

1. **Simplicidade de Uso** - Scripts automatizados para setup
2. **Flexibilidade** - Múltiplas opções de configuração
3. **Completude** - Todas as funcionalidades Sentry disponíveis
4. **Integração Nativa** - Funciona perfeitamente com Claude Code
5. **Monitoramento Real-time** - Acompanhamento contínuo via monitor.sh

---

## 🚀 **Como Usar**

### **Setup Inicial:**
```bash
cd mcp-sentry
./add-to-claude-code.sh
```

### **Inicialização:**
```bash
./start.sh
# ou
./start-standalone.sh
```

### **Monitoramento:**
```bash
./monitor.sh
```

### **Testes:**
```bash
./test-standalone.sh
```

---

## 🎉 **Conclusão**

O diagrama mostra uma arquitetura **robusta e bem estruturada** do Claude Code MCP Sentry, com:

- **7 scripts** para diferentes cenários de uso
- **2 arquivos** de configuração flexíveis
- **1 núcleo central** com 27 ferramentas
- **2 módulos** especializados (API + Types)
- **3 serviços** Sentry integrados
- **1 arquivo** de registro global

**Resultado:** Sistema completo de observabilidade integrado ao Claude Code! 🎯