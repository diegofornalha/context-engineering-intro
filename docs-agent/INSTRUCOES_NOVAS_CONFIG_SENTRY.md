# 🔧 Como Obter Novas Configurações Sentry para PRP Agent

## 📋 **Suas Configurações ATUAIS (Projeto Antigo):**
```bash
SENTRY_AUTH_TOKEN=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
SENTRY_ORG=coflow  # ✅ MANTER IGUAL
SENTRY_API_URL=https://sentry.io/api/0/  # ✅ MANTER IGUAL
SENTRY_DSN=https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334  # ❌ TROCAR
```

---

## 🎯 **O que Precisa TROCAR:**
- ❌ **SENTRY_DSN** → Novo DSN do projeto PRP Agent
- ❌ **SENTRY_AUTH_TOKEN** → Novo token com permissões apropriadas
- ✅ **SENTRY_ORG** → Manter "coflow"
- ✅ **SENTRY_API_URL** → Manter igual

---

## 🚀 **PASSO-A-PASSO (5 minutos)**

### **1️⃣ CRIAR NOVO PROJETO (2 minutos)**
```bash
# 🌐 Acesse: https://sentry.io/organizations/coflow/projects/new/

# 📋 Configurar projeto:
Nome: "PRP Agent Python Monitoring"
Slug: "prp-agent-python-monitoring"  
Plataforma: Python
Team: Sua equipe

# 🤖 CRÍTICO: Habilite "AI Agent Monitoring (Beta)"
# (Esta é a funcionalidade específica para agentes de IA)
```

### **2️⃣ OBTER NOVO DSN (30 segundos)**
```bash
# 📄 Na tela de setup do projeto, você verá:
# 
# Configure SDK:
# sentry_sdk.init(
#     dsn="https://NOVA-KEY@o927801.ingest.us.sentry.io/NOVO-PROJECT-ID",
#     ...
# )
#
# 📋 COPIE APENAS O DSN:
# https://NOVA-KEY@o927801.ingest.us.sentry.io/NOVO-PROJECT-ID
```

### **3️⃣ GERAR NOVO AUTH TOKEN (2 minutos)**
```bash
# 🔗 Acesse: https://sentry.io/settings/coflow/auth-tokens/
# ➕ Clique "Create New Token"

# 📝 Configurar token:
Nome: "PRP Agent Token"
Organização: coflow

# ✅ Scopes OBRIGATÓRIOS:
☑️ project:read    # Ler informações do projeto
☑️ project:write   # Criar/modificar projeto
☑️ event:read      # Ler eventos/erros
☑️ event:write     # Enviar eventos/erros  
☑️ org:read        # Ler informações da organização

# 📋 COPIE O TOKEN GERADO (aparece apenas uma vez!)
```

---

## ⚡ **APLICAR CONFIGURAÇÕES**

### **Atualizar Arquivo .env.sentry:**
```bash
# 📁 Edite o arquivo:
nano .env.sentry

# 🔄 Substitua estas linhas:
SENTRY_DSN=SEU-NOVO-DSN-COPIADO
SENTRY_AUTH_TOKEN=SEU-NOVO-TOKEN-GERADO

# 📋 Exemplo final:
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0/
SENTRY_DSN=https://abc123@o927801.ingest.us.sentry.io/4567890
SENTRY_AUTH_TOKEN=sntryu_NOVO_TOKEN_AQUI
```

---

## 🧪 **TESTAR CONFIGURAÇÃO**

### **1. Teste Básico:**
```bash
cd prp-agent
python sentry_ai_agent_setup.py
```

### **2. Resultado Esperado:**
```bash
🤖 Sentry AI Agent Monitoring configurado para prp-agent
📊 Ambiente: development
🔗 Acesse: https://sentry.io/ → AI Agents

🤖 Testando Sentry AI Agent Monitoring...
✅ Workflow de AI Agent iniciado
✅ Chamada LLM rastreada
✅ Execução de ferramenta rastreada
✅ Decisão do agente rastreada
✅ Workflow de AI Agent finalizado

🎯 Workflow completo rastreado no Sentry AI Agent Monitoring!
```

### **3. Verificar Dashboard:**
```bash
# 🌐 Acesse: https://sentry.io/organizations/coflow/projects/prp-agent-python-monitoring/
# 📊 Vá para: AI Agents (Beta)
# 🔍 Visualize: Workflows, traces, performance
```

---

## 🎯 **CONFIGURAÇÃO FINAL (Copy/Paste)**

### **Template .env.sentry Atualizado:**
```bash
# === MANTER IGUAL ===
SENTRY_ORG=coflow
SENTRY_API_URL=https://sentry.io/api/0/

# === TROCAR POR NOVOS VALORES ===
SENTRY_DSN=NOVO-DSN-DO-PROJETO-PRP-AGENT
SENTRY_AUTH_TOKEN=NOVO-TOKEN-COM-PERMISSOES

# === CONFIGURAÇÕES AI AGENT ===
SENTRY_ENVIRONMENT=development
SENTRY_RELEASE=prp-agent@1.0.0
SENTRY_DEBUG=true
ENABLE_AI_AGENT_MONITORING=true
SENTRY_TRACES_SAMPLE_RATE=1.0
```

---

## 🔍 **URLs Diretas:**

### **Para Facilitar o Processo:**
- 🚀 **Criar Projeto**: https://sentry.io/organizations/coflow/projects/new/
- 🔑 **Criar Token**: https://sentry.io/settings/coflow/auth-tokens/
- 📊 **Ver Dashboard**: https://sentry.io/organizations/coflow/

---

## 📈 **Resultado Final:**

### **Após Configurar Você Terá:**
- 🤖 **Projeto específico** para PRP Agent
- 🔧 **AI Agent Monitoring** habilitado
- 📊 **Monitoramento avançado** de workflows
- 🎯 **Dashboard dedicado** para agentes
- 🔔 **Alertas específicos** para IA

### **Diferenças do Projeto Antigo:**
- ✅ **AI Agent Monitoring** (vs monitoramento genérico)
- ✅ **Workflow traces** completos
- ✅ **Tool call tracking** específico
- ✅ **LLM usage metrics** detalhadas
- ✅ **Agent performance** otimizada

---

## ⚠️ **PONTOS IMPORTANTES:**

### **1. Token de Segurança:**
- 🔒 **Novo token** tem escopo limitado (mais seguro)
- 🔄 **Token antigo** pode continuar funcionando para outros projetos
- 📝 **Anote o token** em local seguro (aparece apenas uma vez)

### **2. Organização:**
- ✅ **Mantém "coflow"** - não muda
- ✅ **Projeto específico** para PRP Agent
- 🎯 **Separação limpa** de projetos

### **3. AI Agent Monitoring:**
- 🤖 **Recurso Beta** - habilite no projeto
- 📊 **Específico para IA** - não é monitoramento genérico
- 🔧 **Workflows completos** rastreados

---

**🎉 Após seguir estes passos, seu PRP Agent terá monitoramento AI-nativo de nível enterprise!**