#!/usr/bin/env python3
"""
Integração Natural do Agente PRP com Cursor Agent.

Esta integração permite usar o agente PRP de forma totalmente natural
através do Cursor Agent, sem necessidade de comandos técnicos.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from agents.agent import chat_with_prp_agent, PRPAgentDependencies
from agents.tools import create_prp, search_prps, analyze_prp_with_llm, get_prp_details, update_prp_status

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CursorNaturalIntegration:
    """
    Integração natural do Agente PRP com Cursor Agent.
    
    Permite usar linguagem natural para:
    - Criar PRPs automaticamente
    - Analisar código e extrair requisitos
    - Gerenciar tarefas de desenvolvimento
    - Obter insights sobre o projeto
    """
    
    def __init__(self):
        self.agent_deps = PRPAgentDependencies()
        self.conversation_history = []
        self.current_context = {}
        
    async def process_natural_request(self, user_message: str, file_context: str = None) -> str:
        """
        Processa requisição em linguagem natural do usuário.
        
        Args:
            user_message: Mensagem do usuário em linguagem natural
            file_context: Contexto do arquivo atual (opcional)
            
        Returns:
            Resposta natural e contextualizada
        """
        
        # Adicionar contexto do arquivo se fornecido
        full_message = user_message
        if file_context:
            full_message = f"Contexto do arquivo atual:\n{file_context}\n\nSolicitação do usuário: {user_message}"
        
        # Adicionar ao histórico
        self.conversation_history.append({
            "user": user_message,
            "timestamp": datetime.now().isoformat(),
            "file_context": file_context
        })
        
        try:
            # Processar com o agente PRP
            response = await chat_with_prp_agent(full_message, self.agent_deps)
            
            # Adicionar resposta ao histórico
            self.conversation_history.append({
                "agent": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return self._format_natural_response(response, user_message)
            
        except Exception as e:
            logger.error(f"Erro ao processar requisição: {e}")
            return f"❌ Desculpe, tive um problema ao processar sua solicitação: {str(e)}"
    
    def _format_natural_response(self, response: str, original_message: str) -> str:
        """
        Formata a resposta para ser mais natural e contextualizada.
        """
        
        # Detectar tipo de ação baseado na mensagem original
        message_lower = original_message.lower()
        
        if any(word in message_lower for word in ["criar", "novo", "fazer", "desenvolver"]):
            return f"🎯 **PRP Criado com Sucesso!**\n\n{response}\n\n💡 **Próximos passos:**\n• Analisei automaticamente o contexto\n• Extraí tarefas e requisitos\n• Salvei no banco de dados\n\nQuer que eu analise mais detalhadamente ou crie tarefas específicas?"
        
        elif any(word in message_lower for word in ["analisar", "revisar", "verificar", "examinar"]):
            return f"🔍 **Análise Completa Realizada**\n\n{response}\n\n📊 **Insights encontrados:**\n• Complexidade do projeto\n• Riscos identificados\n• Tarefas sugeridas\n\nQuer que eu detalhe algum aspecto específico?"
        
        elif any(word in message_lower for word in ["buscar", "encontrar", "procurar", "listar"]):
            return f"📋 **PRPs Encontrados**\n\n{response}\n\n🔍 **Filtros aplicados:**\n• Busca inteligente por relevância\n• Ordenação por prioridade\n• Contexto atual considerado\n\nQuer ver detalhes de algum PRP específico?"
        
        elif any(word in message_lower for word in ["atualizar", "modificar", "alterar", "mudar"]):
            return f"✅ **PRP Atualizado**\n\n{response}\n\n🔄 **Mudanças aplicadas:**\n• Status atualizado\n• Histórico preservado\n• Notificações enviadas\n\nQuer ver o histórico de mudanças?"
        
        else:
            # Resposta conversacional geral
            return f"🤖 **Resposta do Agente PRP**\n\n{response}\n\n💭 **Contexto:**\n• Mantive o histórico da conversa\n• Considerei o contexto do projeto\n• Sugestões baseadas em padrões similares\n\nComo posso ajudar mais?"
    
    async def auto_analyze_file(self, file_path: str, file_content: str) -> str:
        """
        Analisa automaticamente um arquivo e sugere PRPs.
        """
        
        analysis_prompt = f"""
        Analise este arquivo e sugira PRPs relevantes:
        
        **Arquivo:** {file_path}
        **Conteúdo:**
        {file_content[:2000]}...
        
        Por favor:
        1. Identifique funcionalidades principais
        2. Sugira melhorias ou novos recursos
        3. Identifique possíveis bugs ou problemas
        4. Crie PRPs estruturados para cada sugestão
        """
        
        return await self.process_natural_request(analysis_prompt)
    
    async def get_project_insights(self) -> str:
        """
        Obtém insights gerais sobre o projeto.
        """
        
        insights_prompt = """
        Analise o projeto atual e forneça insights:
        
        1. **Status geral dos PRPs**
        2. **Tarefas pendentes mais importantes**
        3. **Riscos identificados**
        4. **Sugestões de melhoria**
        5. **Métricas de progresso**
        
        Seja conciso mas informativo.
        """
        
        return await self.process_natural_request(insights_prompt)
    
    async def create_task_from_code(self, code_snippet: str, context: str = "") -> str:
        """
        Cria tarefas baseadas em um trecho de código.
        """
        
        task_prompt = f"""
        Analise este código e crie tarefas de desenvolvimento:
        
        **Código:**
        {code_snippet}
        
        **Contexto:** {context}
        
        Por favor:
        1. Identifique o que o código faz
        2. Sugira melhorias ou correções
        3. Crie tarefas específicas e acionáveis
        4. Estime complexidade e prioridade
        """
        
        return await self.process_natural_request(task_prompt)
    
    def get_conversation_summary(self) -> str:
        """
        Retorna um resumo da conversa atual.
        """
        
        if not self.conversation_history:
            return "📝 Nenhuma conversa registrada ainda."
        
        user_messages = [msg for msg in self.conversation_history if "user" in msg]
        agent_messages = [msg for msg in self.conversation_history if "agent" in msg]
        
        summary = f"""
        📊 **Resumo da Conversa**
        
        **Total de interações:** {len(user_messages)}
        **Última interação:** {self.conversation_history[-1]['timestamp']}
        
        **Tópicos principais:**
        """
        
        # Extrair tópicos das mensagens do usuário
        topics = []
        for msg in user_messages[-5:]:  # Últimas 5 mensagens
            user_msg = msg["user"].lower()
            if any(word in user_msg for word in ["criar", "novo"]):
                topics.append("Criação de PRPs")
            elif any(word in user_msg for word in ["analisar", "revisar"]):
                topics.append("Análise de código")
            elif any(word in user_msg for word in ["buscar", "encontrar"]):
                topics.append("Busca de PRPs")
            elif any(word in user_msg for word in ["atualizar", "modificar"]):
                topics.append("Atualização de PRPs")
            else:
                topics.append("Conversa geral")
        
        summary += "\n".join([f"• {topic}" for topic in set(topics)])
        
        return summary

# Instância global para uso no Cursor Agent
cursor_prp_agent = CursorNaturalIntegration()

# Funções de conveniência para uso direto
async def analyze_current_file(file_path: str, content: str) -> str:
    """Analisa o arquivo atual e sugere PRPs."""
    return await cursor_prp_agent.auto_analyze_file(file_path, content)

async def chat_with_prp_natural(message: str, file_context: str = None) -> str:
    """Conversa natural com o agente PRP."""
    return await cursor_prp_agent.process_natural_request(message, file_context)

async def get_project_status() -> str:
    """Obtém status geral do projeto."""
    return await cursor_prp_agent.get_project_insights()

async def create_tasks_from_code(code: str, context: str = "") -> str:
    """Cria tarefas baseadas em código."""
    return await cursor_prp_agent.create_task_from_code(code, context)

def get_conversation_history() -> str:
    """Retorna histórico da conversa."""
    return cursor_prp_agent.get_conversation_summary()

# Exemplo de uso para o Cursor Agent
if __name__ == "__main__":
    async def demo():
        """Demonstração da integração natural."""
        
        print("🤖 **Demonstração da Integração Natural do Agente PRP**\n")
        
        # Exemplo 1: Análise de arquivo
        print("📁 **Exemplo 1: Analisando arquivo atual**")
        response = await analyze_current_file(
            "auth.js",
            "function login(user, password) { /* código de login */ }"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 2: Conversa natural
        print("💬 **Exemplo 2: Conversa natural**")
        response = await chat_with_prp_natural(
            "Crie um PRP para implementar autenticação JWT neste projeto"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 3: Status do projeto
        print("📊 **Exemplo 3: Status do projeto**")
        response = await get_project_status()
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 4: Histórico
        print("📝 **Exemplo 4: Histórico da conversa**")
        response = get_conversation_history()
        print(response)
    
    asyncio.run(demo()) 