"""
Agente PRP Principal.

Este módulo contém o agente PydanticAI especializado em análise e gerenciamento de PRPs.
"""

import logging
from pydantic_ai import Agent, RunContext
from .providers import get_llm_model, get_test_model
from .dependencies import PRPAgentDependencies
from .tools import (
    create_prp, 
    search_prps, 
    analyze_prp_with_llm, 
    get_prp_details, 
    update_prp_status
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prompt do sistema para o agente PRP
SYSTEM_PROMPT = """
Você é um assistente especializado em análise e gerenciamento de PRPs (Product Requirement Prompts).

## 🎯 Suas Capacidades Principais:

### 1. **Análise LLM Inteligente**
- Analisa PRPs e extrai tarefas automaticamente
- Avalia complexidade e prioridade das tarefas
- Identifica dependências entre componentes
- Sugere melhorias e otimizações

### 2. **Gerenciamento de Banco de Dados**
- CRUD completo para PRPs no banco context-memory
- Armazenamento de análises LLM
- Histórico de conversas e contexto
- Busca e filtros avançados

### 3. **Interface Conversacional Natural**
- Respostas claras e úteis
- Explicações detalhadas quando necessário
- Sugestões proativas baseadas no contexto
- Manutenção de histórico de conversação

## 📋 Diretrizes para Análise de PRPs:

### ✅ **Extração de Tarefas**
- Identifique tarefas específicas e acionáveis
- Avalie complexidade técnica e de negócio
- Estime tempo de desenvolvimento realisticamente
- Priorize baseado em dependências e valor

### ✅ **Avaliação de Qualidade**
- Verifique clareza e completude do PRP
- Identifique requisitos faltantes ou ambíguos
- Sugira melhorias na estrutura e detalhamento
- Valide viabilidade técnica

### ✅ **Contexto e Dependências**
- Identifique dependências entre tarefas
- Considere impactos em outros sistemas
- Avalie riscos e mitigações
- Mantenha contexto histórico

## 🛠️ Diretrizes para Gerenciamento:

### ✅ **Validação de Dados**
- Valide dados antes de salvar no banco
- Verifique integridade e consistência
- Trate erros graciosamente
- Forneça feedback claro sobre operações

### ✅ **Histórico e Rastreabilidade**
- Mantenha histórico completo de mudanças
- Registre análises LLM realizadas
- Preserve contexto de conversas
- Permita auditoria de decisões

### ✅ **Performance e Escalabilidade**
- Otimize consultas ao banco de dados
- Use cache quando apropriado
- Monitore uso de recursos
- Mantenha respostas rápidas

## 🎯 Comportamento Esperado:

1. **Seja Útil e Preciso**: Forneça informações relevantes e acionáveis
2. **Mantenha Contexto**: Use histórico de conversas para melhorar respostas
3. **Seja Proativo**: Sugira ações e melhorias quando apropriado
4. **Seja Claro**: Use linguagem simples e explique conceitos complexos
5. **Seja Consistente**: Mantenha padrões de resposta e formatação

## 🔧 Ferramentas Disponíveis:

- `create_prp`: Criar novo PRP no banco
- `search_prps`: Buscar PRPs com filtros
- `analyze_prp_with_llm`: Analisar PRP com LLM
- `get_prp_details`: Obter detalhes completos
- `update_prp_status`: Atualizar status do PRP

Sempre seja útil, preciso e mantenha o contexto da conversação. Use as ferramentas apropriadas para cada situação.
"""

# Criar o agente PRP
prp_agent = Agent(
    get_llm_model(),
    deps_type=PRPAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)

# Registrar todas as ferramentas
prp_agent.tool(create_prp)
prp_agent.tool(search_prps)
prp_agent.tool(analyze_prp_with_llm)
prp_agent.tool(get_prp_details)
prp_agent.tool(update_prp_status)

# Função principal para conversar com o agente
async def chat_with_prp_agent(
    message: str, 
    deps: PRPAgentDependencies = None,
    use_test_model: bool = False
) -> str:
    """
    Conversar com o agente PRP.
    
    Args:
        message: Mensagem do usuário
        deps: Dependências do agente (opcional)
        use_test_model: Se deve usar modelo de teste (para desenvolvimento)
    
    Returns:
        Resposta do agente
    """
    if deps is None:
        deps = PRPAgentDependencies()
    
    try:
        if use_test_model:
            # Usar modelo de teste para desenvolvimento
            test_model = get_test_model()
            with prp_agent.override(model=test_model):
                result = await prp_agent.run(message, deps=deps)
        else:
            # Usar modelo real
            result = await prp_agent.run(message, deps=deps)
        
        return result.data
        
    except Exception as e:
        logger.error(f"Erro na conversa com agente: {e}")
        return f"❌ Erro interno do agente: {str(e)}"

def chat_with_prp_agent_sync(
    message: str, 
    deps: PRPAgentDependencies = None,
    use_test_model: bool = False
) -> str:
    """
    Versão síncrona para conversar com o agente PRP.
    
    Args:
        message: Mensagem do usuário
        deps: Dependências do agente (opcional)
        use_test_model: Se deve usar modelo de teste (para desenvolvimento)
    
    Returns:
        Resposta do agente
    """
    if deps is None:
        deps = PRPAgentDependencies()
    
    try:
        if use_test_model:
            # Usar modelo de teste para desenvolvimento
            test_model = get_test_model()
            with prp_agent.override(model=test_model):
                result = prp_agent.run_sync(message, deps=deps)
        else:
            # Usar modelo real
            result = prp_agent.run_sync(message, deps=deps)
        
        return result.data
        
    except Exception as e:
        logger.error(f"Erro na conversa com agente: {e}")
        return f"❌ Erro interno do agente: {str(e)}"

# Função para obter estatísticas do agente
def get_agent_stats(deps: PRPAgentDependencies) -> dict:
    """Obter estatísticas do agente."""
    return {
        "session_id": deps.session_id,
        "conversation_count": len(deps.conversation_history),
        "project_context": deps.project_context,
        "database_path": deps.database_path,
        "max_tokens_per_analysis": deps.max_tokens_per_analysis
    }

# Função para limpar histórico de conversas
def clear_conversation_history(deps: PRPAgentDependencies):
    """Limpar histórico de conversas."""
    deps.conversation_history.clear()
    logger.info("Histórico de conversas limpo")

# Função para exportar conversas
def export_conversations(deps: PRPAgentDependencies) -> list:
    """Exportar histórico de conversas."""
    return deps.conversation_history.copy() 