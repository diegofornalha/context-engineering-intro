# 🎯 Guia Completo: Como Gerar PRPs (Product Requirement Prompts)

## 📊 Visão Geral

Existem **5 formas principais** de gerar PRPs no projeto, cada uma com seu propósito específico.

## 🚀 Formas de Gerar PRPs

### 1. **Via Agente PRP (PydanticAI)** - RECOMENDADO
**Local:** `/agents/`  
**Como usar:**
```python
from agents.agent import prp_agent
from agents.dependencies import PRPAgentDependencies

# Criar dependências
deps = PRPAgentDependencies(session_id="minha-sessao")

# Gerar PRP via conversa natural
result = await prp_agent.run(
    "Crie um PRP para sistema de autenticação JWT",
    deps=deps
)
```

**Vantagens:**
- ✅ Interface conversacional natural
- ✅ Análise LLM inteligente
- ✅ Extração automática de tarefas
- ✅ Salva no banco de dados

### 2. **Via Framework PRP-Agent (Template)**
**Local:** `/prp-agent/`  
**Como usar:**
```bash
# 1. Definir requisitos em PRPs/INITIAL.md
# 2. Gerar PRP baseado nos requisitos
/generate-pydantic-ai-prp PRPs/INITIAL.md
# 3. Executar PRP para criar agente
/execute-pydantic-ai-prp PRPs/generated_prp.md
```

**Vantagens:**
- ✅ Metodologia estruturada
- ✅ Pesquisa extensiva incluída
- ✅ Loops de validação
- ✅ Ideal para criar novos agentes

### 3. **Via Scripts Python Diretos**
**Local:** `/prp-agent/` e `/py-prp/`  
**Scripts disponíveis:**
```python
# generate_prp.py - Geração básica
python generate_prp.py

# create_prp_manual.py - Criação manual
python create_prp_manual.py

# exemplo_prp_organizacao.py - Exemplo específico
python exemplo_prp_organizacao.py
```

**Vantagens:**
- ✅ Controle total sobre o processo
- ✅ Customização específica
- ✅ Útil para casos especiais

### 4. **Via Integração MCP Turso**
**Local:** `/py-prp/prp_mcp_integration.py`  
**Como usar:**
```python
from py_prp.prp_mcp_integration import PRPMCPIntegration

# Criar integração
integration = PRPMCPIntegration()

# Criar PRP e salvar no Turso
prp_data = {
    "title": "Meu PRP",
    "description": "Descrição detalhada",
    "tasks": ["tarefa1", "tarefa2"]
}
await integration.create_prp(prp_data)
```

**Vantagens:**
- ✅ Integração com banco remoto
- ✅ Persistência garantida
- ✅ Sincronização automática

### 5. **Via Interface Natural (Cursor Final)**
**Local:** `/prp-agent/cursor_final.py`  
**Como usar:**
```python
from cursor_final import chat_natural, suggest_prp

# Conversa natural
response = await chat_natural("Preciso de um PRP para e-commerce")

# Sugestão direta
prp = await suggest_prp("Sistema de pagamentos", "E-commerce")
```

**Vantagens:**
- ✅ Interface mais natural
- ✅ Integração com Cursor
- ✅ Respostas contextuais

## 📋 Comparação das Formas

| Método | Complexidade | Automação | Persistência | Melhor Para |
|--------|--------------|-----------|--------------|-------------|
| Agente PRP | Baixa | Alta | ✅ Sim | Uso geral, produção |
| Framework | Média | Média | ❌ Manual | Criar novos agentes |
| Scripts | Alta | Baixa | ❌ Manual | Casos específicos |
| MCP Turso | Média | Alta | ✅ Sim | Integração remota |
| Cursor | Baixa | Alta | ✅ Sim | Interface natural |

## 🎯 Qual Usar?

### Para Uso Diário:
**Use o Agente PRP** (`/agents/`)
- Interface conversacional
- Análise inteligente
- Persistência automática

### Para Criar Novos Agentes:
**Use o Framework PRP-Agent** (`/prp-agent/`)
- Metodologia completa
- Templates prontos
- Validação incluída

### Para Integração com Sistemas:
**Use MCP Turso Integration**
- Sincronização remota
- APIs disponíveis
- Escalável

## 💡 Exemplo Prático Completo

```python
# 1. Importar o agente PRP
from agents.agent import prp_agent
from agents.dependencies import PRPAgentDependencies

# 2. Criar sessão
deps = PRPAgentDependencies(
    session_id="projeto-ecommerce",
    database_path="./context-memory.db"
)

# 3. Gerar PRP via conversa
async def gerar_prp_ecommerce():
    # Primeira interação
    result = await prp_agent.run(
        "Preciso criar um sistema de e-commerce completo",
        deps=deps
    )
    print(result.data)
    
    # Refinamento
    result = await prp_agent.run(
        "Adicione módulo de pagamento com PIX e cartão",
        deps=deps
    )
    print(result.data)
    
    # Buscar PRPs criados
    result = await prp_agent.run(
        "Liste todos os PRPs do projeto e-commerce",
        deps=deps
    )
    print(result.data)

# 4. Executar
import asyncio
asyncio.run(gerar_prp_ecommerce())
```

## 🔧 Configuração Necessária

### 1. Variáveis de Ambiente (.env):
```env
# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=sua-chave-aqui
LLM_MODEL=gpt-4

# Database
DATABASE_PATH=./context-memory.db

# Language (opcional)
USE_DEFAULT_LANGUAGE=true
DEFAULT_LANGUAGE=pt-br
```

### 2. Banco de Dados:
```bash
# Criar banco se não existir
python py-prp/setup_prp_database.py
```

## 📚 Recursos Adicionais

- **Documentação PRPs:** `/docs/04-prp-system/`
- **Exemplos:** `/prp-agent/examples/`
- **Templates:** `/prp-agent/PRPs/templates/`
- **Guia do Agente:** `/agents/README.md`

## 🎉 Dica Final

Para 90% dos casos, use o **Agente PRP** - é a forma mais simples e poderosa de gerar PRPs com qualidade profissional!

---
*Guia criado para facilitar a geração de PRPs no projeto*