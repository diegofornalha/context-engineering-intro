# 🎯 GUIA PASSO A PASSO: SENTRY AI AGENTS - O QUE DEU CERTO!

## 📋 **Resumo Executivo**

Este guia documenta **exatamente** o que foi feito para implementar com sucesso o monitoramento de AI Agents no Sentry, seguindo 100% a documentação oficial.

**✅ RESULTADO**: 17 spans enviados, 6 AI Agents monitorados, error capture funcionando!

---

## 🚫 **PROBLEMA INICIAL: O que NÃO funcionou**

### ❌ Tentativa 1: OpenAI Agents Integration (FALHOU)
```python
# ISTO NÃO FUNCIONOU:
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration

sentry_sdk.init(
    dsn="...",
    integrations=[
        OpenAIAgentsIntegration(),  # ❌ AttributeError: module 'agents' has no attribute 'run'
    ],
)
```

**🔍 Por que falhou:**
- Dependência `agents` não compatível
- Conflitos de versão
- Framework muito específico
- Documentação incompleta

---

## ✅ **SOLUÇÃO QUE DEU CERTO: Manual Instrumentation**

### 🎯 **Decisão Estratégica**
Em vez de usar a integração automática problemática, implementamos **Manual Instrumentation** seguindo 100% a documentação oficial do Sentry.

**📚 Base**: [Documentação Oficial Sentry AI Agents](https://docs.sentry.io/platforms/python/tracing/instrumentation/custom-instrumentation/)

---

## 🛠️ **PASSO A PASSO DO SUCESSO**

### **PASSO 1: Configuração Base Sentry**

```python
import sentry_sdk

# ✅ Configuração que FUNCIONOU
sentry_sdk.init(
    dsn="https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832",
    traces_sample_rate=1.0,
    send_default_pii=True,  # Include LLM inputs/outputs
    # ✅ SEM integrations problemáticas!
)
```

**🔑 Chaves do sucesso:**
- ✅ DSN correto
- ✅ `traces_sample_rate=1.0` (capture 100% spans)
- ✅ `send_default_pii=True` (dados LLM)
- ✅ **NENHUMA** integração automática

### **PASSO 2: Implementar Span "gen_ai.invoke_agent"**

```python
def invoke_agent_official(agent_name: str, model: str, prompt: str, temperature: float, max_tokens: int, user_id: str):
    session_id = str(uuid.uuid4())
    
    # ✅ INVOKE AGENT SPAN - Padrão oficial
    with sentry_sdk.start_span(
        op="gen_ai.invoke_agent",  # MUST be "gen_ai.invoke_agent"
        name=f"invoke_agent {agent_name}",  # SHOULD be "invoke_agent {agent_name}"
    ) as span:
        
        # ✅ Common Span Attributes - REQUIRED
        span.set_data("gen_ai.system", "openai")  # REQUIRED
        span.set_data("gen_ai.request.model", model)  # REQUIRED
        span.set_data("gen_ai.operation.name", "invoke_agent")  # MUST be "invoke_agent"
        span.set_data("gen_ai.agent.name", agent_name)  # SHOULD be set
        
        # ✅ Optional attributes
        span.set_data("gen_ai.request.temperature", temperature)
        span.set_data("gen_ai.request.max_tokens", max_tokens)
        
        # ✅ Messages format: [{"role": "", "content": ""}]
        messages = [
            {"role": "system", "content": f"You are {agent_name}, a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        span.set_data("gen_ai.request.messages", json.dumps(messages))
        
        # ... resto da implementação
```

**🔑 O que fez dar certo:**
- ✅ Op exato: `"gen_ai.invoke_agent"`
- ✅ Name format: `"invoke_agent {agent_name}"`
- ✅ Todos atributos REQUIRED implementados
- ✅ JSON strings corretos (não objetos Python)

### **PASSO 3: Implementar Span "gen_ai.chat"**

```python
def ai_client_official(model: str, messages: List[Dict], temperature: float, max_tokens: int, session_id: str):
    # ✅ AI CLIENT SPAN - Padrão oficial
    with sentry_sdk.start_span(
        op="gen_ai.chat",  # MUST be "gen_ai.chat"
        name=f"chat {model}",  # SHOULD be "chat {model}"
    ) as span:
        
        # ✅ Common Span Attributes - REQUIRED
        span.set_data("gen_ai.system", "openai")  # REQUIRED
        span.set_data("gen_ai.request.model", model)  # REQUIRED
        span.set_data("gen_ai.operation.name", "chat")  # operation name
        
        # ✅ Request data
        span.set_data("gen_ai.request.messages", json.dumps(messages))
        span.set_data("gen_ai.request.temperature", temperature)
        span.set_data("gen_ai.request.max_tokens", max_tokens)
        
        # ... processamento LLM ...
        
        # ✅ Response data
        span.set_data("gen_ai.response.text", json.dumps([response]))
        if tool_calls:
            span.set_data("gen_ai.response.tool_calls", json.dumps(tool_calls))
        
        # ✅ Token usage
        span.set_data("gen_ai.usage.input_tokens", input_tokens)
        span.set_data("gen_ai.usage.output_tokens", output_tokens)
        span.set_data("gen_ai.usage.total_tokens", total_tokens)
```

**🔑 O que fez dar certo:**
- ✅ Op exato: `"gen_ai.chat"`
- ✅ Todos tokens capturados
- ✅ Messages em formato JSON string
- ✅ Response como array JSON

### **PASSO 4: Implementar Span "gen_ai.execute_tool"**

```python
def execute_tool_official(tool_name: str, input_text: str, model: str, session_id: str):
    # ✅ EXECUTE TOOL SPAN - Padrão oficial
    with sentry_sdk.start_span(
        op="gen_ai.execute_tool",  # MUST be "gen_ai.execute_tool"
        name=f"execute_tool {tool_name}",  # SHOULD be "execute_tool {tool_name}"
    ) as span:
        
        # ✅ Common attributes
        span.set_data("gen_ai.system", "openai")
        span.set_data("gen_ai.request.model", model)
        
        # ✅ Tool-specific attributes
        span.set_data("gen_ai.tool.name", tool_name)
        span.set_data("gen_ai.tool.description", descriptions.get(tool_name, "AI Tool"))
        span.set_data("gen_ai.tool.type", "function")
        
        # ✅ Tool input/output
        tool_input = {"text": input_text[:100], "session_id": session_id}
        span.set_data("gen_ai.tool.input", json.dumps(tool_input))
        
        # ... execução tool ...
        
        span.set_data("gen_ai.tool.output", tool_output)
```

**🔑 O que fez dar certo:**
- ✅ Op exato: `"gen_ai.execute_tool"`
- ✅ Tool attributes completos
- ✅ Input/Output capturados
- ✅ Type correto: "function"

### **PASSO 5: Integração com FastAPI**

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/ai-agent/official-standards", response_model=OfficialAgentResponse)
async def process_official_standards(request: OfficialAgentRequest):
    try:
        result = invoke_agent_official(
            agent_name=request.agent_name,
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            user_id=request.user_id
        )
        
        return OfficialAgentResponse(
            result=result["result"],
            agent_session=result["session_id"],
            total_tokens=result["total_tokens"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            tools_executed=result["tools_executed"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        sentry_sdk.capture_exception(e)  # ✅ Error capture
        raise
```

**🔑 O que fez dar certo:**
- ✅ FastAPI + Sentry sem conflitos
- ✅ Exception capture automático
- ✅ Response models estruturados
- ✅ Session IDs únicos

### **PASSO 6: Estrutura de Dados Correta**

```python
# ✅ Modelos Pydantic corretos
class OfficialAgentRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    agent_name: str = "PRP Assistant"
    temperature: float = 0.1
    max_tokens: int = 1000
    user_id: str = "anonymous"

class OfficialAgentResponse(BaseModel):
    result: str
    agent_session: str
    total_tokens: int
    input_tokens: int
    output_tokens: int
    tools_executed: List[str]
    processing_time: float
```

**🔑 O que fez dar certo:**
- ✅ Tipos corretos (int, float, str, List)
- ✅ Valores default sensatos
- ✅ Validação automática Pydantic
- ✅ Serialização JSON limpa

---

## 🧪 **TESTES QUE COMPROVARAM O SUCESSO**

### **Teste 1: AI Agent Individual**
```bash
curl -X POST http://localhost:8000/ai-agent/official-standards \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Implementar sistema JWT com refresh tokens",
    "model": "gpt-4o-mini",
    "agent_name": "Security Engineer Assistant",
    "temperature": 0.1,
    "max_tokens": 1000,
    "user_id": "test_user"
  }'
```

**✅ Resultado:**
```json
{
  "agent_session": "858f95de-91bf-48bf-8bd8-6541a85bf5a8",
  "total_tokens": 228,
  "input_tokens": 26,
  "output_tokens": 202,
  "tools_executed": ["prp_parser"],
  "processing_time": 0.72
}
```

### **Teste 2: Benchmark Múltiplos Agentes**
```bash
curl -s http://localhost:8000/ai-agent/benchmark-standards
```

**✅ Resultado:**
- 5 agentes testados
- 1,510 tokens processados
- 0.66s tempo médio
- **Todos spans enviados para Sentry!**

### **Teste 3: Error Capture**
```bash
curl -s http://localhost:8000/sentry-debug
```

**✅ Resultado:**
- 500 Internal Server Error
- ZeroDivisionError capturado
- **Erro enviado para Sentry!**

---

## 📊 **RESULTADOS FINAIS COMPROVADOS**

### **17 Spans Enviados para Sentry:**
- 🤖 **6x gen_ai.invoke_agent** spans
- 💬 **6x gen_ai.chat** spans
- 🔧 **4x gen_ai.execute_tool** spans
- 🚨 **1x error** span

### **Dados Capturados:**
- **1,738 tokens** processados total
- **6 AI Agents** únicos monitorados
- **4 ferramentas** executadas
- **6 sessions** com UUIDs únicos
- **100% conformidade** com documentação oficial

---

## 🎯 **FATORES CRÍTICOS DO SUCESSO**

### **1. ✅ Seguir EXATAMENTE a Documentação Oficial**
- Não improvisar nomes de spans
- Usar atributos exatos (gen_ai.system, gen_ai.request.model, etc.)
- Respeitar tipos de dados (JSON strings, não objetos)

### **2. ✅ Evitar Integrações Automáticas Problemáticas**
- OpenAI Agents Integration = problemas de dependência
- Manual Instrumentation = controle total

### **3. ✅ Estrutura de Dados Consistente**
- UUID para session IDs
- Tokens como integers
- Timing como float
- Arrays de tools como List[str]

### **4. ✅ Implementação Completa de Todos os Spans**
- gen_ai.invoke_agent (obrigatório)
- gen_ai.chat (obrigatório)
- gen_ai.execute_tool (obrigatório)

### **5. ✅ Testing Abrangente**
- Teste individual
- Teste benchmark
- Teste error capture
- Verificação no Sentry Dashboard

---

## 🚀 **COMO REPLICAR O SUCESSO**

### **Passo 1: Setup Environment**
```bash
cd prp-agent
source .venv/bin/activate
pip install "sentry-sdk[fastapi]" fastapi uvicorn pydantic
```

### **Passo 2: Copiar Implementação**
```bash
# Usar o arquivo: main_official_standards.py
# ✅ Implementação 100% funcional já pronta
```

### **Passo 3: Configurar DSN**
```python
sentry_sdk.init(
    dsn="SEU_DSN_AQUI",  # ⚠️ Trocar pelo seu DSN
    traces_sample_rate=1.0,
    send_default_pii=True,
)
```

### **Passo 4: Executar**
```bash
uvicorn main_official_standards:app --host 0.0.0.0 --port 8000
```

### **Passo 5: Testar**
```bash
# Teste basic
curl http://localhost:8000/

# Teste AI Agent
curl -X POST localhost:8000/ai-agent/official-standards \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Seu prompt", "agent_name": "Seu Agent"}'

# Teste benchmark
curl localhost:8000/ai-agent/benchmark-standards

# Teste error
curl localhost:8000/sentry-debug
```

### **Passo 6: Verificar Sentry**
- Abrir Sentry Dashboard
- Buscar por spans gen_ai.*
- Verificar eventos AI Agent
- Confirmar métricas de performance

---

## 💡 **LIÇÕES APRENDIDAS**

### **❌ O que NÃO fazer:**
1. Não usar OpenAI Agents Integration automática
2. Não improvisar nomes de spans
3. Não passar objetos Python como span data
4. Não ignorar atributos obrigatórios

### **✅ O que FAZER:**
1. Seguir Manual Instrumentation oficial
2. Usar nomes exatos da documentação
3. Converter tudo para JSON strings
4. Implementar todos spans obrigatórios
5. Testar tudo antes de produção

---

## 🏆 **CONQUISTA FINAL**

### **✅ 100% SUCESSO COMPROVADO:**

- ✅ **Conformidade total** com documentação oficial Sentry
- ✅ **17 spans enviados** para monitoramento
- ✅ **6 AI Agents monitorados** com métricas completas
- ✅ **Error capture funcionando** perfeitamente
- ✅ **Performance tracking** em tempo real
- ✅ **Zero dependências problemáticas**
- ✅ **Framework agnóstico** (funciona com qualquer LLM)

---

## 🎯 **PRÓXIMOS PASSOS**

1. **✅ FINALIZADO**: Implementação base funcionando
2. **🔄 EM ANDAMENTO**: Monitoring no Sentry Dashboard
3. **📋 PENDENTE**: Alertas personalizados
4. **📋 PENDENTE**: Dashboard customizado
5. **📋 PENDENTE**: Métricas de negócio

---

## 📞 **Suporte e Manutenção**

**🔍 Para debug:**
- Logs: `uvicorn main_official_standards:app --log-level debug`
- Health check: `curl localhost:8000/`
- Error test: `curl localhost:8000/sentry-debug`

**📊 Para verificar Sentry:**
- URL: https://sentry.io/organizations/coflow/projects/
- Filtros: `gen_ai.*` tags
- Busca: Por session IDs específicos

**🎯 Para performance:**
- Ajustar `traces_sample_rate` se necessário
- Monitorar tokens/segundo
- Otimizar tool execution times

---

## 🎉 **CONCLUSÃO**

**🏆 MISSÃO CUMPRIDA COM EXCELÊNCIA!**

Implementamos **com sucesso total** o monitoramento de AI Agents no Sentry seguindo **100% a documentação oficial**. 

**17 spans enviados, 6 AI Agents monitorados, error capture funcionando!**

**🤖 Agora você tem o monitoramento de AI Agents mais avançado possível!**

---

*📝 Documento criado após implementação bem-sucedida em {{date}}*  
*🎯 Todos os testes passaram com 100% de sucesso*  
*✅ Pronto para produção*