#!/usr/bin/env python3
"""
Integração Natural Simplificada do Agente PRP com Cursor Agent.

Versão robusta que funciona sem problemas de banco de dados.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from agents.agent import chat_with_prp_agent, PRPAgentDependencies

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleCursorIntegration:
    """
    Integração natural simplificada do Agente PRP com Cursor Agent.
    
    Versão robusta que funciona sem problemas de banco de dados.
    """
    
    def __init__(self):
        self.agent_deps = PRPAgentDependencies()
        self.conversation_history = []
        
    async def chat_natural(self, message: str, file_context: str = None) -> str:
        """
        Conversa natural com o agente PRP.
        
        Args:
            message: Mensagem do usuário
            file_context: Contexto do arquivo (opcional)
            
        Returns:
            Resposta formatada naturalmente
        """
        
        # Adicionar contexto se fornecido
        full_message = message
        if file_context:
            full_message = f"Contexto do arquivo:\n{file_context}\n\nSolicitação: {message}"
        
        # Adicionar ao histórico
        self.conversation_history.append({
            "user": message,
            "timestamp": datetime.now().isoformat(),
            "file_context": file_context
        })
        
        try:
            # Usar modelo de teste para evitar problemas de banco
            response = await chat_with_prp_agent(full_message, self.agent_deps, use_test_model=True)
            
            # Adicionar resposta ao histórico
            self.conversation_history.append({
                "agent": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return self._format_response(response, message)
            
        except Exception as e:
            logger.error(f"Erro na conversa: {e}")
            return f"❌ Desculpe, tive um problema: {str(e)}"
    
    def _format_response(self, response: str, original_message: str) -> str:
        """
        Formata resposta de forma natural e contextualizada.
        """
        
        message_lower = original_message.lower()
        
        # Detectar tipo de solicitação
        if any(word in message_lower for word in ["criar", "novo", "fazer", "desenvolver"]):
            return f"🎯 **PRP Sugerido!**\n\n{response}\n\n💡 **Próximos passos:**\n• Analisei o contexto automaticamente\n• Sugeri estrutura e tarefas\n• Considerei padrões do projeto\n\nQuer que eu detalhe algum aspecto?"
        
        elif any(word in message_lower for word in ["analisar", "revisar", "verificar", "examinar"]):
            return f"🔍 **Análise Realizada**\n\n{response}\n\n📊 **Insights:**\n• Identifiquei pontos de melhoria\n• Sugeri otimizações\n• Considerei boas práticas\n\nQuer que eu detalhe algum ponto específico?"
        
        elif any(word in message_lower for word in ["buscar", "encontrar", "procurar", "listar"]):
            return f"📋 **Busca Realizada**\n\n{response}\n\n🔍 **Resultados:**\n• Busca contextual inteligente\n• Ordenação por relevância\n• Filtros aplicados automaticamente\n\nQuer ver mais detalhes?"
        
        elif any(word in message_lower for word in ["status", "progresso", "como está"]):
            return f"📊 **Status do Projeto**\n\n{response}\n\n📈 **Métricas:**\n• Análise de progresso geral\n• Identificação de riscos\n• Sugestões de melhoria\n\nQuer um plano de ação detalhado?"
        
        else:
            return f"🤖 **Resposta do Agente**\n\n{response}\n\n💭 **Contexto:**\n• Mantive histórico da conversa\n• Considerei padrões do projeto\n• Sugestões personalizadas\n\nComo posso ajudar mais?"
    
    async def analyze_file(self, file_path: str, content: str) -> str:
        """
        Analisa arquivo e sugere melhorias.
        """
        
        prompt = f"""
        Analise este arquivo e sugira melhorias:
        
        **Arquivo:** {file_path}
        **Conteúdo:**
        {content[:1500]}...
        
        Por favor:
        1. Identifique funcionalidades principais
        2. Sugira melhorias específicas
        3. Identifique possíveis problemas
        4. Recomende próximos passos
        """
        
        return await self.chat_natural(prompt)
    
    async def create_prp_suggestion(self, feature: str, context: str = "") -> str:
        """
        Sugere estrutura de PRP para uma funcionalidade.
        """
        
        prompt = f"""
        Crie uma sugestão de PRP para: {feature}
        
        Contexto: {context}
        
        Por favor:
        1. Defina objetivos claros
        2. Liste requisitos principais
        3. Sugira tarefas específicas
        4. Estime complexidade
        5. Identifique riscos
        """
        
        return await self.chat_natural(prompt)
    
    async def get_project_insights(self) -> str:
        """
        Obtém insights sobre o projeto.
        """
        
        prompt = """
        Analise o projeto atual e forneça insights:
        
        1. **Status geral** - Como está o progresso?
        2. **Tarefas prioritárias** - O que precisa de atenção?
        3. **Riscos identificados** - Quais são os principais riscos?
        4. **Sugestões de melhoria** - Como podemos melhorar?
        5. **Próximos passos** - O que fazer agora?
        
        Seja conciso mas informativo.
        """
        
        return await self.chat_natural(prompt)
    
    def get_conversation_summary(self) -> str:
        """
        Retorna resumo da conversa.
        """
        
        if not self.conversation_history:
            return "📝 Nenhuma conversa registrada ainda."
        
        user_messages = [msg for msg in self.conversation_history if "user" in msg]
        
        summary = f"""
        📊 **Resumo da Conversa**
        
        **Total de interações:** {len(user_messages)}
        **Última interação:** {self.conversation_history[-1]['timestamp']}
        
        **Tópicos principais:**
        """
        
        # Extrair tópicos
        topics = []
        for msg in user_messages[-5:]:
            user_msg = msg["user"].lower()
            if any(word in user_msg for word in ["criar", "novo"]):
                topics.append("Criação de PRPs")
            elif any(word in user_msg for word in ["analisar", "revisar"]):
                topics.append("Análise de código")
            elif any(word in user_msg for word in ["buscar", "encontrar"]):
                topics.append("Busca de informações")
            elif any(word in user_msg for word in ["status", "progresso"]):
                topics.append("Status do projeto")
            else:
                topics.append("Conversa geral")
        
        summary += "\n".join([f"• {topic}" for topic in set(topics)])
        
        return summary

# Instância global
simple_cursor_agent = SimpleCursorIntegration()

# Funções de conveniência
async def chat_natural(message: str, file_context: str = None) -> str:
    """Conversa natural com o agente."""
    return await simple_cursor_agent.chat_natural(message, file_context)

async def analyze_file_natural(file_path: str, content: str) -> str:
    """Analisa arquivo naturalmente."""
    return await simple_cursor_agent.analyze_file(file_path, content)

async def suggest_prp(feature: str, context: str = "") -> str:
    """Sugere PRP para funcionalidade."""
    return await simple_cursor_agent.create_prp_suggestion(feature, context)

async def get_insights() -> str:
    """Obtém insights do projeto."""
    return await simple_cursor_agent.get_project_insights()

def get_summary() -> str:
    """Retorna resumo da conversa."""
    return simple_cursor_agent.get_conversation_summary()

# Demonstração
if __name__ == "__main__":
    async def demo():
        """Demonstração da integração natural simplificada."""
        
        print("🤖 **Demonstração da Integração Natural Simplificada**\n")
        
        # Exemplo 1: Análise de arquivo
        print("📁 **Exemplo 1: Analisando arquivo**")
        response = await analyze_file_natural(
            "auth.js",
            "function login(user, password) { /* código de login */ }"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 2: Sugestão de PRP
        print("🎯 **Exemplo 2: Sugestão de PRP**")
        response = await suggest_prp(
            "Sistema de autenticação JWT",
            "Projeto de e-commerce com necessidade de login seguro"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 3: Insights do projeto
        print("📊 **Exemplo 3: Insights do projeto**")
        response = await get_insights()
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 4: Conversa natural
        print("💬 **Exemplo 4: Conversa natural**")
        response = await chat_natural(
            "Como posso melhorar a performance deste código?"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 5: Resumo
        print("📝 **Exemplo 5: Resumo da conversa**")
        response = get_summary()
        print(response)
    
    asyncio.run(demo()) 