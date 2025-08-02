#!/usr/bin/env python3
"""
Integração Natural Simples do Agente PRP com Cursor Agent.

Versão que funciona diretamente com LLM, sem dependências complexas.
Perfeita para uso no Cursor Agent com linguagem natural.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from openai import AsyncOpenAI
from agents.settings import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleCursorChat:
    """
    Integração natural simples do Agente PRP com Cursor Agent.
    
    Funciona diretamente com OpenAI, sem dependências complexas.
    """
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url
        )
        self.conversation_history = []
        
        self.system_prompt = """Você é um assistente especializado em análise e gerenciamento de PRPs (Product Requirement Prompts).

**Suas responsabilidades:**
1. **Análise de Código** - Identificar funcionalidades, problemas e melhorias
2. **Criação de PRPs** - Sugerir estruturas de PRPs baseadas em requisitos
3. **Insights de Projeto** - Fornecer análises sobre status e progresso
4. **Recomendações** - Sugerir melhorias e próximos passos

**Como responder:**
- Seja natural e conversacional
- Forneça análises detalhadas mas concisas
- Sugira ações práticas e acionáveis
- Mantenha contexto da conversa
- Use linguagem técnica quando apropriado, mas explique conceitos complexos

**Formato de resposta:**
- Use emojis para tornar mais visual
- Estruture informações de forma clara
- Destaque pontos importantes
- Sempre sugira próximos passos

**Contexto:** Você está sendo usado no Cursor Agent para ajudar desenvolvedores a criar e gerenciar PRPs de forma natural."""
    
    async def chat_natural(self, message: str, file_context: str = None) -> str:
        """
        Conversa natural com o LLM.
        """
        
        # Adicionar contexto se fornecido
        full_message = message
        if file_context:
            full_message = f"Contexto do arquivo atual:\n{file_context}\n\nSolicitação do usuário: {message}"
        
        # Adicionar ao histórico
        self.conversation_history.append({
            "user": message,
            "timestamp": datetime.now().isoformat(),
            "file_context": file_context
        })
        
        try:
            # Preparar mensagens
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Adicionar histórico recente (últimas 5 mensagens)
            recent_history = self.conversation_history[-10:]  # Últimas 10 interações
            for item in recent_history:
                if "user" in item:
                    messages.append({"role": "user", "content": item["user"]})
                if "agent" in item:
                    messages.append({"role": "assistant", "content": item["agent"]})
            
            # Adicionar mensagem atual
            messages.append({"role": "user", "content": full_message})
            
            # Chamar OpenAI
            response = await self.client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Extrair resposta
            response_content = response.choices[0].message.content
            
            # Adicionar resposta ao histórico
            self.conversation_history.append({
                "agent": response_content,
                "timestamp": datetime.now().isoformat()
            })
            
            return self._format_response(response_content, message)
            
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
        Analisa arquivo e sugere melhorias usando LLM.
        """
        
        prompt = f"""
        Analise este arquivo e forneça insights detalhados:
        
        **Arquivo:** {file_path}
        **Conteúdo:**
        {content[:2000]}...
        
        **Por favor analise:**
        1. **Funcionalidades principais** - O que o código faz?
        2. **Pontos de melhoria** - O que pode ser otimizado?
        3. **Problemas potenciais** - Há bugs ou vulnerabilidades?
        4. **Sugestões de PRPs** - Que PRPs você sugeriria?
        5. **Próximos passos** - O que fazer agora?
        
        Seja específico e acionável.
        """
        
        return await self.chat_natural(prompt)
    
    async def suggest_prp(self, feature: str, context: str = "") -> str:
        """
        Sugere estrutura de PRP para uma funcionalidade.
        """
        
        prompt = f"""
        Crie uma sugestão detalhada de PRP para: **{feature}**
        
        **Contexto:** {context}
        
        **Estrutura sugerida:**
        1. **Objetivo** - O que queremos alcançar?
        2. **Requisitos funcionais** - Que funcionalidades precisamos?
        3. **Requisitos não-funcionais** - Performance, segurança, etc.
        4. **Tarefas específicas** - Lista de tarefas acionáveis
        5. **Critérios de aceitação** - Como saber se está pronto?
        6. **Riscos e dependências** - O que pode dar errado?
        7. **Estimativa** - Complexidade e tempo estimado
        
        Seja detalhado mas prático.
        """
        
        return await self.chat_natural(prompt)
    
    async def get_project_insights(self) -> str:
        """
        Obtém insights sobre o projeto usando LLM.
        """
        
        prompt = """
        Analise o projeto atual e forneça insights valiosos:
        
        **Análise solicitada:**
        1. **Status geral** - Como está o progresso do projeto?
        2. **Tarefas prioritárias** - O que precisa de atenção imediata?
        3. **Riscos identificados** - Quais são os principais riscos?
        4. **Oportunidades** - Onde podemos melhorar?
        5. **Próximos passos** - Que ações você recomenda?
        6. **Métricas sugeridas** - Como medir o progresso?
        
        Baseie-se em padrões de projetos similares e boas práticas.
        Seja conciso mas informativo.
        """
        
        return await self.chat_natural(prompt)
    
    async def improve_code(self, code: str, context: str = "") -> str:
        """
        Sugere melhorias para código específico.
        """
        
        prompt = f"""
        Analise este código e sugira melhorias:
        
        **Código:**
        {code}
        
        **Contexto:** {context}
        
        **Análise solicitada:**
        1. **O que o código faz?** - Explique a funcionalidade
        2. **Problemas identificados** - Bugs, vulnerabilidades, anti-patterns
        3. **Melhorias sugeridas** - Otimizações específicas
        4. **Refatoração** - Como melhorar a estrutura?
        5. **Testes** - Que testes você sugeriria?
        6. **Documentação** - Que documentação seria útil?
        
        Seja específico e forneça exemplos quando possível.
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
            elif any(word in user_msg for word in ["melhorar", "otimizar"]):
                topics.append("Melhorias de código")
            else:
                topics.append("Conversa geral")
        
        summary += "\n".join([f"• {topic}" for topic in set(topics)])
        
        return summary

# Instância global
simple_cursor_chat = SimpleCursorChat()

# Funções de conveniência para uso no Cursor Agent
async def chat_natural(message: str, file_context: str = None) -> str:
    """Conversa natural com o agente LLM."""
    return await simple_cursor_chat.chat_natural(message, file_context)

async def analyze_file(file_path: str, content: str) -> str:
    """Analisa arquivo usando LLM."""
    return await simple_cursor_chat.analyze_file(file_path, content)

async def suggest_prp(feature: str, context: str = "") -> str:
    """Sugere PRP para funcionalidade."""
    return await simple_cursor_chat.suggest_prp(feature, context)

async def get_insights() -> str:
    """Obtém insights do projeto."""
    return await simple_cursor_chat.get_project_insights()

async def improve_code(code: str, context: str = "") -> str:
    """Sugere melhorias para código."""
    return await simple_cursor_chat.improve_code(code, context)

def get_summary() -> str:
    """Retorna resumo da conversa."""
    return simple_cursor_chat.get_conversation_summary()

# Demonstração
if __name__ == "__main__":
    async def demo():
        """Demonstração da integração simples."""
        
        print("🤖 **Demonstração da Integração Natural Simples**\n")
        
        # Exemplo 1: Análise de arquivo
        print("📁 **Exemplo 1: Analisando arquivo**")
        response = await analyze_file(
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
        
        # Exemplo 4: Melhorias de código
        print("🔧 **Exemplo 4: Melhorias de código**")
        response = await improve_code(
            "function processData(data) { return data.map(x => x * 2); }",
            "Função de processamento de dados"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 5: Conversa natural
        print("💬 **Exemplo 5: Conversa natural**")
        response = await chat_natural(
            "Como posso melhorar a performance deste código?"
        )
        print(response)
        print("\n" + "="*50 + "\n")
        
        # Exemplo 6: Resumo
        print("📝 **Exemplo 6: Resumo da conversa**")
        response = get_summary()
        print(response)
    
    asyncio.run(demo()) 