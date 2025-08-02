# 🚨 Guia Completo: Sentry para PRP Agent

## 📋 Visão Geral

Integração completa do **Sentry** no projeto **PRP Agent** para monitoramento avançado de:
- 🤖 **Agentes PydanticAI** (conversas, análises LLM)
- 🔧 **Ferramentas MCP** (Turso, Sentry, outros)
- 📊 **Operações de PRPs** (criação, análise, atualização)
- 🗄️ **Banco de Dados** SQLite (queries, performance)
- ⚡ **Performance** e métricas de uso

---

## 🚀 Configuração Rápida (5 minutos)

### 1. **Criar Projeto no Sentry**
```bash
# 1. Acesse https://sentry.io/
# 2. Crie novo projeto
# 3. Escolha "Python" como plataforma
# 4. Copie o DSN do projeto
```

### 2. **Configurar Ambiente**
```bash
cd prp-agent

# Copiar arquivo de configuração
cp ../prp_agent_env_sentry.example .env.sentry

# Editar com suas credenciais
nano .env.sentry
```

### 3. **Instalar Dependências**
```bash
# Adicionar ao requirements.txt
echo "sentry-sdk[fastapi]==1.40.0" >> requirements.txt

# Instalar
source venv/bin/activate
pip install -r requirements.txt
```

### 4. **Integrar com Agentes Existentes**
```python
# Em agents/settings.py - adicionar
SENTRY_DSN: str = Field(default="", description="Sentry DSN para monitoramento")
SENTRY_ENVIRONMENT: str = Field(default="development", description="Ambiente Sentry")

# Em agents/agent.py - no início do arquivo
from sentry_prp_agent_setup import configure_sentry_for_prp_agent
from prp_agent_sentry_integration import PRPAgentSentryIntegration

# Configurar Sentry
if settings.sentry_dsn:
    configure_sentry_for_prp_agent(settings.sentry_dsn, settings.sentry_environment)
```

---

## 📊 Funcionalidades de Monitoramento

### 🤖 **Monitoramento de Agentes**
```python
# Exemplo de uso no chat_with_prp_agent
@monitor_agent_operation("prp_chat", component="pydantic_ai")
async def chat_with_prp_agent(message: str, deps: PRPAgentDependencies):
    # ... código existente ...
    pass
```

### 🔧 **Monitoramento MCP Tools**
```python
# Em agents/tools.py
from prp_agent_sentry_integration import PRPAgentSentryIntegration

sentry_integration = PRPAgentSentryIntegration(settings.sentry_dsn)

async def create_prp(ctx, name, title, ...):
    # Monitorar operação MCP
    sentry_integration.monitor_mcp_tool_call("create_prp", {
        "name": name, "title": title
    })
    
    try:
        # ... código existente ...
        result = await execute_query(...)
        
        # Registrar sucesso
        sentry_integration.monitor_database_operation("INSERT", "prps", True)
        return result
    except Exception as e:
        # Registrar erro
        sentry_integration.monitor_database_operation("INSERT", "prps", False)
        raise
```

### 📈 **Métricas de Performance**
```python
# Monitorar tempo de resposta dos agentes
import time

start_time = time.time()
result = await prp_agent.run(message, deps=deps)
duration = time.time() - start_time

sentry_integration.capture_agent_performance_metrics("prp_agent", {
    "response_time_ms": duration * 1000,
    "message_length": len(message),
    "response_length": len(result.data)
})
```

---

## 🔍 Tipos de Eventos Monitorados

### ✅ **Eventos de Sucesso**
- 💬 **Chat completado** com tempo de resposta
- 📋 **PRP criado** com detalhes
- 🔍 **Análise LLM** concluída
- 🗄️ **Query SQL** executada com sucesso

### ❌ **Eventos de Erro**
- 🚫 **Falhas de LLM** (timeout, limite de tokens)
- 💥 **Erros de MCP** (conexão, autenticação)
- 🗄️ **Erros de banco** (SQL inválido, lock)
- ⚠️ **Validação** de entrada falhada

### 📊 **Métricas de Performance**
- ⏱️ **Tempo de resposta** dos agentes
- 🔢 **Tokens utilizados** por análise
- 💾 **Uso de memória** durante operações
- 🔄 **Taxa de sucesso** das operações

---

## 🛠️ Integração com Componentes Existentes

### 📁 **1. Atualizar `agents/settings.py`**
```python
# Adicionar campos Sentry
sentry_dsn: str = Field(default="", description="Sentry DSN")
sentry_environment: str = Field(default="development", description="Ambiente")
enable_sentry_monitoring: bool = Field(default=True, description="Habilitar Sentry")
```

### 📁 **2. Atualizar `agents/agent.py`**
```python
# Adicionar no início
from sentry_prp_agent_setup import configure_sentry_for_prp_agent

# Configurar Sentry
if settings.sentry_dsn and settings.enable_sentry_monitoring:
    configure_sentry_for_prp_agent(
        dsn=settings.sentry_dsn,
        environment=settings.sentry_environment
    )
```

### 📁 **3. Atualizar `agents/tools.py`**
```python
# Adicionar monitoramento em cada ferramenta
from prp_agent_sentry_integration import PRPAgentSentryIntegration

async def create_prp(ctx: RunContext[PRPAgentDependencies], ...):
    sentry_integration = PRPAgentSentryIntegration(settings.sentry_dsn)
    
    # Monitorar operação
    sentry_integration.monitor_prp_operation(None, "create", {
        "name": name, "title": title
    })
    
    # ... resto do código ...
```

### 📁 **4. Atualizar integrações Cursor**
```python
# Em cursor_turso_integration.py
from sentry_prp_agent_setup import configure_sentry_for_prp_agent

class CursorTursoIntegration:
    def __init__(self):
        # Configurar Sentry
        sentry_dsn = os.getenv("SENTRY_DSN")
        if sentry_dsn:
            configure_sentry_for_prp_agent(sentry_dsn, "development")
```

---

## 📈 Dashboard e Alertas

### 🎯 **Métricas Principais para Acompanhar**
1. **Taxa de Erro** dos agentes PRP
2. **Tempo de Resposta** médio
3. **Uso de Tokens** LLM por operação
4. **Performance** das queries SQL
5. **Disponibilidade** dos MCPs

### 🔔 **Alertas Recomendados**
- ⚠️ **Taxa de erro > 5%** em 10 minutos
- 🐌 **Tempo de resposta > 30s** consistente
- 💸 **Uso excessivo de tokens** LLM
- 🔌 **Falhas de MCP** repetidas
- 🗄️ **Queries SQL lentas** (> 5s)

### 📊 **Dashboard Personalizado**
```json
{
  "widgets": [
    {
      "title": "PRP Agent Health",
      "query": "project:prp-agent component:pydantic_ai"
    },
    {
      "title": "MCP Tools Performance", 
      "query": "project:prp-agent category:mcp"
    },
    {
      "title": "LLM Usage Metrics",
      "query": "project:prp-agent category:llm"
    }
  ]
}
```

---

## 🧪 Teste da Integração

### 1. **Teste Básico**
```bash
cd prp-agent
python ../sentry_prp_agent_setup.py
```

### 2. **Teste com Agente Real**
```python
from prp_agent_sentry_integration import SentryEnhancedPRPAgent

# Criar agente com monitoramento
agent = SentryEnhancedPRPAgent("YOUR_SENTRY_DSN", "development")

# Testar chat
await agent.chat_with_monitoring("Crie um PRP para sistema de notificações")
```

### 3. **Verificar Dashboard**
- Acesse https://sentry.io/
- Navegue para seu projeto
- Verifique eventos em **Issues** > **All Issues**
- Confira métricas em **Performance**

---

## 🔧 Configurações Avançadas

### 🎛️ **Filtros Personalizados**
```python
# Em sentry_prp_agent_setup.py
def filter_prp_agent_events(event, hint):
    # Ignorar warnings específicos
    if event.get('level') == 'warning':
        if 'pydantic' in event.get('message', '').lower():
            return None
    
    # Adicionar contexto específico
    event['extra']['agent_version'] = "1.0.0"
    event['extra']['project'] = "prp-agent"
    
    return event
```

### 📊 **Contexto Personalizado**
```python
# Adicionar contexto específico do PRP
sentry_sdk.set_context("prp_agent", {
    "version": "1.0.0",
    "database_path": "../context-memory.db", 
    "llm_provider": "openai",
    "mcp_servers": ["turso", "sentry"]
})
```

### 🏷️ **Tags Específicas**
```python
# Tags automáticas baseadas no contexto
sentry_sdk.set_tag("agent_type", "prp")
sentry_sdk.set_tag("llm_model", "gpt-4o")
sentry_sdk.set_tag("has_mcp", True)
sentry_sdk.set_tag("environment", "development")
```

---

## ✅ Checklist de Implementação

### 📋 **Configuração Básica**
- [ ] Projeto Sentry criado
- [ ] DSN configurado no .env
- [ ] Dependências instaladas
- [ ] Sentry configurado em settings.py

### 🔧 **Integração com Componentes**
- [ ] agents/agent.py com monitoramento
- [ ] agents/tools.py com tracking MCP
- [ ] Integrações Cursor atualizadas
- [ ] Database operations monitoradas

### 📊 **Monitoramento Avançado**
- [ ] Performance metrics configuradas
- [ ] Error tracking ativo
- [ ] Custom contexts definidos
- [ ] Alerts configurados

### 🧪 **Teste e Validação**
- [ ] Teste básico executado
- [ ] Eventos aparecendo no dashboard
- [ ] Alertas funcionando
- [ ] Performance metrics coletadas

---

## 🔗 Próximos Passos

### 1. **Configuração Imediata**
```bash
# Execute agora:
cd prp-agent
cp ../prp_agent_env_sentry.example .env.sentry
# Edite o arquivo com seu SENTRY_DSN
python ../sentry_prp_agent_setup.py
```

### 2. **Integração Gradual**
- Comece com monitoramento básico
- Adicione métricas de performance
- Configure alertas personalizados
- Expanda para outros componentes

### 3. **Otimização**
- Analise padrões de erro
- Otimize performance baseado nas métricas
- Configure alertas mais específicos
- Implemente correções automáticas

---

## 📞 Suporte

### 🐛 **Problemas Comuns**
- **DSN inválido**: Verifique se copiou corretamente do Sentry
- **Eventos não aparecem**: Confirme se `debug=True` em development
- **Performance lenta**: Reduza `traces_sample_rate` em produção

### 📚 **Documentação**
- **Sentry Python**: https://docs.sentry.io/platforms/python/
- **PydanticAI**: https://ai.pydantic.dev/
- **MCP Protocol**: Documentação local do projeto

### 🎯 **Resultado Esperado**
Após seguir este guia você terá:
- ✅ **Monitoramento completo** do PRP Agent
- 📊 **Visibilidade total** de erros e performance  
- 🔔 **Alertas automáticos** para problemas
- 📈 **Métricas detalhadas** de uso

**🚀 Seu PRP Agent agora tem monitoramento de nível enterprise!**