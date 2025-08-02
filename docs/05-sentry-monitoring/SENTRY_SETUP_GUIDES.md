# 🚨 Guias de Setup Sentry - Consolidado

> **Consolidação de todos os guias de configuração Sentry para PRP Agent**

## 📋 **Índice de Guias**

1. [🎯 Criar Projeto Sentry](#criar-projeto-sentry)
2. [🔧 Obter Novas Configurações](#obter-novas-configurações)
3. [🤖 AI Agent Monitoring](#ai-agent-monitoring)
4. [⚡ Setup Rápido FastAPI](#setup-rápido-fastapi)
5. [📊 Release Health](#release-health)

---

## 🎯 **Criar Projeto Sentry**

### **📊 Status Atual**
✅ **Integração PRP Agent**: 100% configurada  
⚠️ **Projeto Sentry**: Precisa ser criado manualmente  
🎯 **Objetivo**: Projeto Python para monitorar agentes PydanticAI

### **🚀 Criar Projeto Sentry (3 minutos)**

#### **1. Acessar Sentry**
```
🌐 Acesse: https://sentry.io/
👤 Faça login ou crie conta gratuita
```

#### **2. Criar Novo Projeto**
```
1. Clique em "Create Project" (canto superior direito)
2. Escolha "Python" como plataforma
3. Configure o projeto:
   📋 Nome: "PRP Agent Python Monitoring"
   🏷️ Slug: "prp-agent-python"
   👥 Team: Sua equipe (ou "My Team")
   🏢 Organization: Sua organização
```

#### **3. Configurar Projeto**
```
✅ Platform: Python
✅ Framework: Nenhum específico (ou FastAPI se usar)
✅ Integration: Python SDK
✅ Environment: Development
```

#### **4. Copiar DSN**
```
📋 Na tela de setup, copie o DSN completo:
   Formato: https://xxxx@o123456.ingest.sentry.io/456789
   
💾 Salve em local seguro
```

---

## 🔧 **Obter Novas Configurações**

### **📋 Suas Configurações ATUAIS (Projeto Antigo):**
```bash
SENTRY_AUTH_TOKEN=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
SENTRY_ORG=coflow  # ✅ MANTER IGUAL
SENTRY_API_URL=https://sentry.io/api/0/  # ✅ MANTER IGUAL
SENTRY_DSN=https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334  # ❌ TROCAR
```

### **🎯 O que Precisa TROCAR:**
- ❌ **SENTRY_DSN** → Novo DSN do projeto PRP Agent
- ❌ **SENTRY_AUTH_TOKEN** → Novo token com permissões apropriadas
- ✅ **SENTRY_ORG** → Manter "coflow"
- ✅ **SENTRY_API_URL** → Manter igual

### **🚀 PASSO-A-PASSO (5 minutos)**

#### **1️⃣ CRIAR NOVO PROJETO (2 minutos)**
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

#### **2️⃣ OBTER NOVO DSN (30 segundos)**
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

#### **3️⃣ GERAR NOVO AUTH TOKEN (2 minutos)**
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

### **⚡ APLICAR CONFIGURAÇÕES**

#### **Atualizar Arquivo .env.sentry:**
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

## 🤖 **AI Agent Monitoring**

### **🎯 Recurso PERFEITO Identificado!**

O **Sentry AI Agent Monitoring (Beta)** é **EXATAMENTE** o que precisamos para o projeto PRP Agent! 

#### **✅ Match Perfeito:**
- 🤖 **AI Agent workflows** → Agentes PydanticAI do PRP
- 🔧 **Tool calls** → Ferramentas MCP (Turso, Sentry)
- 🧠 **Model interactions** → Chamadas OpenAI/Anthropic
- 📊 **Performance tracking** → Otimização de workflows

### **🚀 Configuração Específica para AI Agents**

#### **1. Habilitar AI Agent Monitoring no Sentry**
```bash
# 1. Acesse seu projeto no Sentry
# 2. Vá para: Settings → Features
# 3. Habilite: "AI Agent Monitoring (Beta)"
# 4. Ou crie novo projeto com suporte a AI Agents
```

#### **2. Configuração Otimizada**
```python
# Usar sentry_ai_agent_setup.py ao invés do setup padrão
from sentry_ai_agent_setup import configure_sentry_ai_agent_monitoring

configure_sentry_ai_agent_monitoring(
    dsn="SEU-DSN-AQUI",
    environment="development",
    agent_name="prp-agent"
)
```

#### **3. Monitoramento Completo de Workflows**
```python
# Usar prp_agent_ai_monitoring.py para integração completa
from prp_agent_ai_monitoring import AIMonitoredPRPAgent

# Criar agente com AI Monitoring
ai_agent = AIMonitoredPRPAgent("SEU-DSN", "development")

# Chat monitorado automaticamente
response = await ai_agent.chat_with_ai_monitoring("Crie um PRP para cache Redis")
```

---

## ⚡ **Setup Rápido FastAPI**

### **🔧 Configuração FastAPI + Sentry**

#### **1. Configuração Base**
```python
from fastapi import FastAPI
import sentry_sdk

# ✅ Configuração que FUNCIONOU
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # To reduce the volume of performance data captured, change traces_sample_rate to a value between 0 and 1
    traces_sample_rate=0.1,
)

app = FastAPI()

@app.get("/")
async def root():
    """Rota principal - PRP Agent com Sentry"""
    return {
        "message": "PRP Agent com Sentry - Funcionando!"
    }

@app.get("/sentry-debug")
async def trigger_error():
    """
    Endpoint para verificar integração Sentry
    Conforme documentação oficial: https://docs.sentry.io/platforms/python/integrations/fastapi/
    """
    division_by_zero = 1 / 0
```

#### **2. Testar Integração**
```bash
# Executar server
uvicorn main:app --host 0.0.0.0 --port 8000

# Testar endpoints
curl http://localhost:8000/
curl http://localhost:8000/sentry-debug

# Verificar no Sentry Dashboard
# https://sentry.io/organizations/coflow/projects/python/
```

---

## 📊 **Release Health**

### **🔧 Configuração Release Health**
```python
# Configure SDK seguindo documentação oficial Sentry AI Agents + Release Health
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,

    # ✅ RELEASE HEALTH CONFIGURATION
    release="prp-agent@1.0.0",  # Set release version for tracking
    environment="production",   # Set environment for Release Health
    auto_session_tracking=True  # Enable automatic session tracking
)
```

### **📊 Demo Release Health**
```python
from fastapi import FastAPI
import sentry_sdk
from pydantic import BaseModel
import time
import uuid

sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,
    release="prp-agent-release-health-demo@1.0.0",
    environment="demo",
    auto_session_tracking=True
)

app = FastAPI()

class SessionRequest(BaseModel):
    user_id: str
    action: str

@app.post("/demo/healthy-session")
async def healthy_session(request: SessionRequest):
    session_id = str(uuid.uuid4())
    sentry_sdk.set_user({"id": request.user_id})
    sentry_sdk.set_context("session_info", {"session_id": session_id, "action": request.action, "status": "healthy"})
    sentry_sdk.capture_message(f"Healthy session for user {request.user_id} completed action: {request.action}")
    
    time.sleep(0.1)
    
    return {"status": "healthy", "message": f"Session {session_id} for user {request.user_id} completed successfully."}

@app.post("/demo/errored-session")
async def errored_session(request: SessionRequest):
    session_id = str(uuid.uuid4())
    sentry_sdk.set_user({"id": request.user_id})
    sentry_sdk.set_context("session_info", {"session_id": session_id, "action": request.action, "status": "errored"})
    
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.capture_message(f"Errored session for user {request.user_id} encountered handled error: {e}")
        return {"status": "errored", "message": f"Session {session_id} for user {request.user_id} completed with a handled error."}
```

---

## 🧪 **Teste da Integração**

### **1. Teste Básico**
```bash
cd prp-agent
python ../sentry_prp_agent_setup.py
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

## 🔗 **URLs Diretas:**

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
- 📊 **Release Health** tracking
- ⚡ **FastAPI integration** funcional

### **Diferenças do Setup Básico:**
- ✅ **AI Agent Monitoring** (vs monitoramento genérico)
- ✅ **Workflow traces** completos
- ✅ **Tool call tracking** específico
- ✅ **LLM usage metrics** detalhadas
- ✅ **Agent performance** otimizada

---

**🎉 Após seguir estes guias, seu PRP Agent terá monitoramento AI-nativo de nível enterprise!**

*Guias consolidados dos arquivos de setup Sentry - versão unificada*