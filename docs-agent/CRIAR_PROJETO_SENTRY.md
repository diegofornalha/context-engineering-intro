# 🚨 Criando Projeto Sentry para PRP Agent

## 📊 Status Atual

✅ **Integração PRP Agent**: 100% configurada  
⚠️ **Projeto Sentry**: Precisa ser criado manualmente  
🎯 **Objetivo**: Projeto Python para monitorar agentes PydanticAI

---

## 🚀 Criar Projeto Sentry (3 minutos)

### **1. Acessar Sentry**
```
🌐 Acesse: https://sentry.io/
👤 Faça login ou crie conta gratuita
```

### **2. Criar Novo Projeto**
```
1. Clique em "Create Project" (canto superior direito)
2. Escolha "Python" como plataforma
3. Configure o projeto:
   📋 Nome: "PRP Agent Python Monitoring"
   🏷️ Slug: "prp-agent-python"
   👥 Team: Sua equipe (ou "My Team")
   🏢 Organization: Sua organização
```

### **3. Configurar Projeto**
```
✅ Platform: Python
✅ Framework: Nenhum específico (ou FastAPI se usar)
✅ Integration: Python SDK
✅ Environment: Development
```

### **4. Copiar DSN**
```
📋 Na tela de setup, copie o DSN completo:
   Formato: https://xxxx@o123456.ingest.sentry.io/456789
   
💾 Salve em local seguro
```

---

## 🔧 Configurar no PRP Agent

### **1. Editar Arquivo de Configuração**
```bash
cd prp-agent
nano .env.sentry

# Substitua esta linha:
SENTRY_DSN=https://your-dsn-here@sentry.io/your-project-id

# Por seu DSN real:
SENTRY_DSN=https://SEU-DSN-COPIADO@o123456.ingest.sentry.io/456789
```

### **2. Ativar Monitoramento**
```bash
# Instalar dependência (se ainda não fez)
source venv/bin/activate
pip install sentry-sdk[fastapi]==1.40.0

# Testar integração
python sentry_prp_agent_setup.py
```

### **3. Verificar Funcionamento**
```bash
# Execute este comando para enviar evento teste:
python -c "
import os
os.environ['SENTRY_DSN'] = 'SEU-DSN-AQUI'

from sentry_prp_agent_setup import configure_sentry_for_prp_agent
configure_sentry_for_prp_agent(os.environ['SENTRY_DSN'], 'development')

import sentry_sdk
sentry_sdk.capture_message('🎉 PRP Agent conectado ao Sentry!', level='info')
print('✅ Evento teste enviado! Verifique no dashboard Sentry.')
"
```

---

## 📊 Configurações Recomendadas

### **🔔 Alertas (opcional)**
```
1. No projeto Sentry, vá para "Alerts"
2. Criar regra: "Error rate > 5% in 10 minutes"
3. Configurar notificação por email
4. Adicionar Slack/Discord se usar
```

### **📈 Dashboard (opcional)**
```
1. Vá para "Dashboards" → "Create Dashboard"
2. Nome: "PRP Agent Health"
3. Adicionar widgets:
   • Error Rate
   • Performance Metrics  
   • LLM Usage
   • Database Operations
```

### **🏷️ Tags Personalizadas**
```
Seu projeto já configurará automaticamente:
• project: prp-agent
• component: pydantic-ai
• environment: development
• llm_model: gpt-4o (ou seu modelo)
```

---

## 🧪 Teste Completo

### **1. Testar Chat do Agente**
```python
# Se tiver o agente configurado:
from agents.agent import chat_with_prp_agent_sync

# Teste que será monitorado:
response = chat_with_prp_agent_sync("Crie um PRP para sistema de cache")
print(f"Resposta: {response}")

# ✅ Essa operação aparecerá no Sentry automaticamente!
```

### **2. Verificar no Dashboard**
```
🌐 Acesse: https://sentry.io/organizations/SUA-ORG/projects/prp-agent-python/

📊 Você verá:
• Issues (erros e eventos)
• Performance (tempo de resposta)
• Releases (versões do código)
• User Feedback (se configurado)
```

---

## 🎯 Resultado Final

### **✅ Quando Concluído Você Terá:**
- 🚨 **Projeto Sentry ativo** para PRP Agent
- 📊 **Monitoramento em tempo real** de todas as operações
- 🤖 **Agentes PydanticAI** totalmente rastreados
- 🔧 **MCP Tools** (Turso, Sentry) monitorados
- 📈 **Métricas de performance** LLM
- 🔔 **Alertas automáticos** para problemas

### **🚀 Benefícios Imediatos:**
- Visibilidade total do sistema
- Detecção precoce de problemas
- Otimização baseada em dados
- Debugging mais eficiente
- Confiabilidade aumentada

---

## 📞 Suporte

### **❓ Problemas Comuns:**
- **DSN inválido**: Verifique se copiou completo
- **Eventos não aparecem**: Confirme environment=development
- **Permissões**: Verifique se tem acesso ao projeto

### **✅ Pronto para Produção:**
```bash
# Para produção, altere apenas:
SENTRY_ENVIRONMENT=production
SENTRY_DEBUG=false
```

**🎉 Seu PRP Agent agora tem monitoramento enterprise!**