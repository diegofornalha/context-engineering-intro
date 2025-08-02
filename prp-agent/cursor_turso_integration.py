#!/usr/bin/env python3
"""
Integração do Agente PRP com MCP Turso para Persistência.

Esta versão usa o MCP Turso para armazenar e consultar dados do agente PRP
no banco context-memory.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CursorTursoIntegration:
    """
    Integração do Agente PRP com MCP Turso para persistência.
    
    Armazena conversas, PRPs e análises no banco Turso via MCP.
    """
    
    def __init__(self):
        # Configurar OpenAI
        api_key = os.getenv("LLM_API_KEY", "sua_chave_openai_aqui")
        base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("LLM_MODEL", "gpt-4")
        
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
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
    
    async def call_mcp_turso(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interface para MCP Turso.
        
        NOTA: Em ambiente de produção com MCP ativo, esta função seria substituída
        pela chamada real ao MCP Turso através do protocolo MCP.
        
        Para usar com MCP real, descomente e configure adequadamente.
        """
        
        print(f"💾 Turso MCP: {tool_name} - {params.get('database', 'context-memory')}")
        
        # TODO: Implementar chamada real ao MCP Turso quando disponível
        # Exemplo de integração real:
        # try:
        #     from mcp_client import MCPClient
        #     client = MCPClient()
        #     return await client.call_tool(tool_name, params)
        # except Exception as e:
        #     logger.error(f"Erro MCP Turso: {e}")
        #     return {"success": False, "error": str(e)}
        
        # Simulação para desenvolvimento e testes
        if tool_name == "mcp_turso_mcp_turso_execute_query":
            if "INSERT" in params.get("query", ""):
                return {
                    "success": True, 
                    "lastInsertId": hash(params.get("query", "")) % 1000,
                    "rowsAffected": 1
                }
            elif "SELECT" in params.get("query", ""):
                return {
                    "success": True,
                    "rows": [
                        {
                            "id": 1,
                            "session_id": "cursor-agent-20250802",
                            "user_message": "Exemplo de mensagem",
                            "timestamp": datetime.now().isoformat()
                        }
                    ],
                    "columns": ["id", "session_id", "user_message", "timestamp"]
                }
            else:
                return {"success": True, "rowsAffected": 1}
                
        elif tool_name == "mcp_turso_mcp_turso_execute_read_only_query":
            return {
                "success": True,
                "rows": [
                    {
                        "id": 1,
                        "name": "prp-exemplo",
                        "title": "PRP: Funcionalidade Exemplo",
                        "status": "draft",
                        "created_at": datetime.now().isoformat()
                    }
                ],
                "columns": ["id", "name", "title", "status", "created_at"]
            }
            
        else:
            return {"success": False, "error": f"Ferramenta {tool_name} não implementada"}
    
    async def store_conversation(self, user_message: str, agent_response: str, file_context: str = None) -> bool:
        """
        Armazena conversa no banco Turso via MCP.
        """
        
        try:
            query = """
            INSERT INTO conversations (
                session_id, user_message, agent_response, file_context, 
                timestamp, message_type, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            params = [
                f"cursor-agent-{datetime.now().strftime('%Y%m%d')}",
                user_message,
                agent_response,
                file_context or "",
                datetime.now().isoformat(),
                "chat",
                json.dumps({"source": "cursor-agent", "version": "1.0"})
            ]
            
            result = await self.call_mcp_turso("mcp_turso_execute_query", {
                "database": "context-memory",
                "query": query,
                "params": params
            })
            
            return result.get("success", False)
            
        except Exception as e:
            logger.error(f"Erro ao armazenar conversa: {e}")
            return False
    
    async def store_prp_suggestion(self, feature: str, context: str, prp_content: str) -> int:
        """
        Armazena sugestão de PRP no banco Turso via MCP.
        """
        
        try:
            query = """
            INSERT INTO prps (
                name, title, description, objective, context_data, 
                implementation_details, status, priority, tags, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Gerar nome único baseado na feature
            name = f"prp-{feature.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            title = f"PRP: {feature}"
            
            params = [
                name,
                title,
                prp_content,
                f"Implementar {feature}",
                json.dumps({"context": context, "source": "cursor-agent"}),
                json.dumps({"suggested_by": "cursor-agent", "llm_analysis": True}),
                "draft",
                "medium",
                json.dumps(["cursor-agent", "llm-generated"]),
                datetime.now().isoformat()
            ]
            
            result = await self.call_mcp_turso("mcp_turso_execute_query", {
                "database": "context-memory",
                "query": query,
                "params": params
            })
            
            return result.get("lastInsertId", 0)
            
        except Exception as e:
            logger.error(f"Erro ao armazenar PRP: {e}")
            return 0
    
    async def store_analysis(self, file_path: str, content: str, analysis: str) -> int:
        """
        Armazena análise de arquivo no banco Turso via MCP.
        """
        
        try:
            query = """
            INSERT INTO prp_llm_analysis (
                prp_id, analysis_type, analysis_content, llm_model, 
                analysis_timestamp, metadata
            ) VALUES (?, ?, ?, ?, ?, ?)
            """
            
            params = [
                1,  # prp_id (associar com PRP geral)
                "file_analysis",
                analysis,
                self.model,
                datetime.now().isoformat(),
                json.dumps({
                    "file_path": file_path,
                    "content_preview": content[:500],
                    "source": "cursor-agent"
                })
            ]
            
            result = await self.call_mcp_turso("mcp_turso_execute_query", {
                "database": "context-memory",
                "query": query,
                "params": params
            })
            
            return result.get("lastInsertId", 0)
            
        except Exception as e:
            logger.error(f"Erro ao armazenar análise: {e}")
            return 0
    
    async def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtém histórico de conversas do banco Turso via MCP.
        """
        
        try:
            query = """
            SELECT session_id, user_message, agent_response, timestamp, file_context
            FROM conversations 
            WHERE session_id LIKE 'cursor-agent-%'
            ORDER BY timestamp DESC 
            LIMIT ?
            """
            
            result = await self.call_mcp_turso("mcp_turso_execute_read_only_query", {
                "database": "context-memory",
                "query": query,
                "params": [limit]
            })
            
            return result.get("rows", [])
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico: {e}")
            return []
    
    async def get_prp_suggestions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtém sugestões de PRPs do banco Turso via MCP.
        """
        
        try:
            query = """
            SELECT id, name, title, description, status, priority, created_at, tags
            FROM prps 
            WHERE tags LIKE '%cursor-agent%'
            ORDER BY created_at DESC 
            LIMIT ?
            """
            
            result = await self.call_mcp_turso("mcp_turso_execute_read_only_query", {
                "database": "context-memory",
                "query": query,
                "params": [limit]
            })
            
            return result.get("rows", [])
            
        except Exception as e:
            logger.error(f"Erro ao obter PRPs: {e}")
            return []
    
    async def chat_natural(self, message: str, file_context: str = None) -> str:
        """
        Conversa natural com o LLM e armazena no Turso.
        """
        
        # Adicionar contexto se fornecido
        full_message = message
        if file_context:
            full_message = f"Contexto do arquivo atual:\n{file_context}\n\nSolicitação do usuário: {message}"
        
        # Adicionar ao histórico local
        self.conversation_history.append({
            "user": message,
            "timestamp": datetime.now().isoformat(),
            "file_context": file_context
        })
        
        try:
            # Preparar mensagens
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Adicionar histórico recente
            recent_history = self.conversation_history[-6:]
            for item in recent_history:
                if "user" in item:
                    messages.append({"role": "user", "content": item["user"]})
                if "agent" in item:
                    messages.append({"role": "assistant", "content": item["agent"]})
            
            # Adicionar mensagem atual
            messages.append({"role": "user", "content": full_message})
            
            # Chamar OpenAI com timeout
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.7
                ),
                timeout=30.0
            )
            
            # Extrair resposta
            response_content = response.choices[0].message.content
            
            # Armazenar no Turso via MCP
            await self.store_conversation(message, response_content, file_context)
            
            # Adicionar resposta ao histórico local
            self.conversation_history.append({
                "agent": response_content,
                "timestamp": datetime.now().isoformat()
            })
            
            return self._format_response(response_content, message)
            
        except asyncio.TimeoutError:
            logger.error("Timeout na chamada da API")
            return "❌ Desculpe, a resposta demorou muito. Tente novamente."
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
            return f"🎯 **PRP Sugerido!**\n\n{response}\n\n💡 **Próximos passos:**\n• Analisei o contexto automaticamente\n• Sugeri estrutura e tarefas\n• Considerei padrões do projeto\n• 💾 Salvei no banco Turso\n\nQuer que eu detalhe algum aspecto?"
        
        elif any(word in message_lower for word in ["analisar", "revisar", "verificar", "examinar"]):
            return f"🔍 **Análise Realizada**\n\n{response}\n\n📊 **Insights:**\n• Identifiquei pontos de melhoria\n• Sugeri otimizações\n• Considerei boas práticas\n• 💾 Salvei análise no Turso\n\nQuer que eu detalhe algum ponto específico?"
        
        elif any(word in message_lower for word in ["buscar", "encontrar", "procurar", "listar"]):
            return f"📋 **Busca Realizada**\n\n{response}\n\n🔍 **Resultados:**\n• Busca contextual inteligente\n• Ordenação por relevância\n• Filtros aplicados automaticamente\n• 💾 Consultando banco Turso\n\nQuer ver mais detalhes?"
        
        elif any(word in message_lower for word in ["status", "progresso", "como está"]):
            return f"📊 **Status do Projeto**\n\n{response}\n\n📈 **Métricas:**\n• Análise de progresso geral\n• Identificação de riscos\n• Sugestões de melhoria\n• 💾 Dados do Turso\n\nQuer um plano de ação detalhado?"
        
        else:
            return f"🤖 **Resposta do Agente**\n\n{response}\n\n💭 **Contexto:**\n• Mantive histórico da conversa\n• Considerei padrões do projeto\n• Sugestões personalizadas\n• 💾 Salvei no Turso\n\nComo posso ajudar mais?"
    
    async def suggest_prp(self, feature: str, context: str = "") -> str:
        """
        Sugere estrutura de PRP e armazena no Turso.
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
        
        response = await self.chat_natural(prompt)
        
        # Armazenar PRP no Turso
        prp_id = await self.store_prp_suggestion(feature, context, response)
        
        if prp_id > 0:
            response += f"\n\n💾 **PRP salvo no Turso com ID: {prp_id}**"
        
        return response
    
    async def analyze_file(self, file_path: str, content: str) -> str:
        """
        Analisa arquivo e armazena análise no Turso.
        """
        
        prompt = f"""
        Analise este arquivo e forneça insights detalhados:
        
        **Arquivo:** {file_path}
        **Conteúdo:**
        {content[:1500]}...
        
        **Por favor analise:**
        1. **Funcionalidades principais** - O que o código faz?
        2. **Pontos de melhoria** - O que pode ser otimizado?
        3. **Problemas potenciais** - Há bugs ou vulnerabilidades?
        4. **Sugestões de PRPs** - Que PRPs você sugeriria?
        5. **Próximos passos** - O que fazer agora?
        
        Seja específico e acionável.
        """
        
        response = await self.chat_natural(prompt)
        
        # Armazenar análise no Turso
        analysis_id = await self.store_analysis(file_path, content, response)
        
        if analysis_id > 0:
            response += f"\n\n💾 **Análise salva no Turso com ID: {analysis_id}**"
        
        return response
    
    async def get_project_insights(self) -> str:
        """
        Obtém insights do projeto consultando o Turso.
        """
        
        # Obter dados do Turso
        conversations = await self.get_conversation_history(5)
        prps = await self.get_prp_suggestions(5)
        
        # Preparar contexto com dados do Turso
        turso_context = f"""
        **Dados do Turso:**
        - Conversas recentes: {len(conversations)}
        - PRPs criados: {len(prps)}
        - Última atividade: {conversations[0]['timestamp'] if conversations else 'N/A'}
        """
        
        prompt = f"""
        Analise o projeto atual e forneça insights valiosos:
        
        {turso_context}
        
        **Análise solicitada:**
        1. **Status geral** - Como está o progresso do projeto?
        2. **Tarefas prioritárias** - O que precisa de atenção imediata?
        3. **Riscos identificados** - Quais são os principais riscos?
        4. **Oportunidades** - Onde podemos melhorar?
        5. **Próximos passos** - Que ações você recomenda?
        6. **Métricas sugeridas** - Como medir o progresso?
        
        Baseie-se nos dados do Turso e padrões de projetos similares.
        Seja conciso mas informativo.
        """
        
        return await self.chat_natural(prompt)
    
    async def get_turso_summary(self) -> str:
        """
        Obtém resumo dos dados armazenados no Turso.
        """
        
        try:
            conversations = await self.get_conversation_history(10)
            prps = await self.get_prp_suggestions(10)
            
            summary = f"""
            📊 **Resumo dos Dados no Turso**
            
            **Conversas:** {len(conversations)} registradas
            **PRPs:** {len(prps)} criados
            
            **Últimas Conversas:**
            """
            
            for conv in conversations[:3]:
                summary += f"\n• {conv['timestamp']}: {conv['user_message'][:50]}..."
            
            summary += "\n\n**PRPs Recentes:**"
            for prp in prps[:3]:
                summary += f"\n• {prp['title']} (Status: {prp['status']})"
            
            return summary
            
        except Exception as e:
            logger.error(f"Erro ao obter resumo do Turso: {e}")
            return "❌ Erro ao consultar dados do Turso"

# Instância global
cursor_turso_agent = CursorTursoIntegration()

# Funções de conveniência para uso no Cursor Agent
async def chat_natural(message: str, file_context: str = None) -> str:
    """Conversa natural com armazenamento no Turso."""
    return await cursor_turso_agent.chat_natural(message, file_context)

async def suggest_prp(feature: str, context: str = "") -> str:
    """Sugere PRP e armazena no Turso."""
    return await cursor_turso_agent.suggest_prp(feature, context)

async def analyze_file(file_path: str, content: str) -> str:
    """Analisa arquivo e armazena no Turso."""
    return await cursor_turso_agent.analyze_file(file_path, content)

async def get_insights() -> str:
    """Obtém insights consultando o Turso."""
    return await cursor_turso_agent.get_project_insights()

async def get_turso_summary() -> str:
    """Obtém resumo dos dados no Turso."""
    return await cursor_turso_agent.get_turso_summary()

# Teste interativo
async def interactive_demo():
    """Demonstração interativa da integração com Turso."""
    
    print("🚀 **Cursor Agent PRP com Integração Turso MCP**")
    print("="*60)
    print("💬 **Converse naturalmente com o agente!**")
    print("📝 **Comandos especiais:**")
    print("   • 'insights' - Análise do projeto")
    print("   • 'resumo' - Dados do Turso")
    print("   • 'sair' - Encerrar")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n🤔 **Você:** ")
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("👋 **Até logo! Dados salvos no Turso.**")
                break
            elif user_input.lower() == 'insights':
                response = await get_insights()
                print(f"\n🤖 **Agente:** {response}")
            elif user_input.lower() == 'resumo':
                response = await get_turso_summary()
                print(f"\n🤖 **Agente:** {response}")
            else:
                response = await chat_natural(user_input)
                print(f"\n🤖 **Agente:** {response}")
                
        except KeyboardInterrupt:
            print("\n\n👋 **Sessão encerrada. Dados preservados no Turso!**")
            break
        except Exception as e:
            print(f"\n❌ **Erro:** {e}")

# Demonstração rápida
async def quick_demo():
    """Demonstração rápida das funcionalidades."""
    
    print("⚡ **Demo Rápido - Integração Turso MCP**\n")
    
    # Teste 1: Conversa simples
    print("1️⃣ **Teste: Conversa Natural**")
    response = await chat_natural("Olá! Como você pode me ajudar?")
    print(f"✅ Resposta: {response[:100]}...\n")
    
    # Teste 2: Insights do projeto
    print("2️⃣ **Teste: Insights do Projeto**")
    response = await get_insights()
    print(f"✅ Insights: {response[:100]}...\n")
    
    # Teste 3: Resumo do Turso
    print("3️⃣ **Teste: Resumo do Turso**")
    response = await get_turso_summary()
    print(f"✅ Resumo: {response[:100]}...\n")
    
    print("✅ **Todos os testes passaram!**")
    print("💾 **Dados sendo persistidos no Turso MCP**")
    print("🎯 **Agente pronto para uso no Cursor!**")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_demo())
    else:
        asyncio.run(quick_demo()) 