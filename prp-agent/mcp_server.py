#!/usr/bin/env python3
"""
Servidor MCP para o Agente PRP.

Este servidor expõe as funcionalidades do agente PRP como ferramentas MCP
que podem ser usadas pelo Cursor IDE.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List
from mcp import Server, StdioServerTransport
from mcp.types import (
    CallToolRequestSchema,
    ListToolsRequestSchema,
    Tool,
    TextContent,
    ImageContent
)

# Importar o agente PRP
from agents.agent import chat_with_prp_agent, PRPAgentDependencies
from agents.tools import create_prp, search_prps, analyze_prp_with_llm, get_prp_details

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar servidor MCP
server = Server(
    {
        "name": "mcp-prp-agent",
        "version": "1.0.0",
    }
)

# Dependências globais do agente
agent_deps = PRPAgentDependencies()

@server.setRequestHandler(ListToolsRequestSchema)
async def handle_list_tools() -> Dict[str, Any]:
    """Listar ferramentas disponíveis do agente PRP."""
    
    tools = [
        Tool(
            name="prp_create",
            description="Criar um novo PRP (Product Requirement Prompt)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Nome único do PRP"
                    },
                    "title": {
                        "type": "string", 
                        "description": "Título descritivo do PRP"
                    },
                    "description": {
                        "type": "string",
                        "description": "Descrição detalhada do PRP"
                    },
                    "objective": {
                        "type": "string",
                        "description": "Objetivo principal do PRP"
                    },
                    "context_data": {
                        "type": "string",
                        "description": "Dados de contexto (JSON)",
                        "default": "{}"
                    },
                    "implementation_details": {
                        "type": "string",
                        "description": "Detalhes de implementação (JSON)",
                        "default": "{}"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Prioridade (low/medium/high/critical)",
                        "default": "medium"
                    },
                    "tags": {
                        "type": "string",
                        "description": "Tags separadas por vírgula",
                        "default": ""
                    }
                },
                "required": ["name", "title", "description", "objective"]
            }
        ),
        Tool(
            name="prp_search",
            description="Buscar PRPs existentes com filtros",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Termo de busca"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filtrar por status (draft/active/completed/archived)"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Filtrar por prioridade (low/medium/high/critical)"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Número máximo de resultados",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="prp_analyze",
            description="Analisar PRP com LLM para extrair tarefas e insights",
            inputSchema={
                "type": "object",
                "properties": {
                    "prp_id": {
                        "type": "number",
                        "description": "ID do PRP para analisar"
                    },
                    "analysis_type": {
                        "type": "string",
                        "description": "Tipo de análise (task_extraction/complexity_assessment/risk_analysis)",
                        "default": "task_extraction"
                    }
                },
                "required": ["prp_id"]
            }
        ),
        Tool(
            name="prp_details",
            description="Obter detalhes completos de um PRP",
            inputSchema={
                "type": "object",
                "properties": {
                    "prp_id": {
                        "type": "number",
                        "description": "ID do PRP"
                    }
                },
                "required": ["prp_id"]
            }
        ),
        Tool(
            name="prp_chat",
            description="Conversar com o agente PRP sobre qualquer assunto relacionado a PRPs",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Mensagem para o agente"
                    },
                    "context": {
                        "type": "string",
                        "description": "Contexto adicional (opcional)"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="prp_update_status",
            description="Atualizar status de um PRP",
            inputSchema={
                "type": "object",
                "properties": {
                    "prp_id": {
                        "type": "number",
                        "description": "ID do PRP"
                    },
                    "new_status": {
                        "type": "string",
                        "description": "Novo status (draft/active/completed/archived)"
                    }
                },
                "required": ["prp_id", "new_status"]
            }
        )
    ]
    
    return {"tools": tools}

@server.setRequestHandler(CallToolRequestSchema)
async def handle_call_tool(request) -> Dict[str, Any]:
    """Executar ferramentas do agente PRP."""
    
    tool_name = request.params.name
    args = request.params.arguments or {}
    
    try:
        if tool_name == "prp_create":
            # Criar novo PRP
            result = await create_prp(
                agent_deps,
                name=args["name"],
                title=args["title"],
                description=args["description"],
                objective=args["objective"],
                context_data=args.get("context_data", "{}"),
                implementation_details=args.get("implementation_details", "{}"),
                priority=args.get("priority", "medium"),
                tags=args.get("tags", "[]")
            )
            
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=result
                    )
                ]
            }
            
        elif tool_name == "prp_search":
            # Buscar PRPs
            result = await search_prps(
                agent_deps,
                query=args.get("query"),
                status=args.get("status"),
                priority=args.get("priority"),
                limit=args.get("limit", 10)
            )
            
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=result
                    )
                ]
            }
            
        elif tool_name == "prp_analyze":
            # Analisar PRP com LLM
            result = await analyze_prp_with_llm(
                agent_deps,
                prp_id=args["prp_id"],
                analysis_type=args.get("analysis_type", "task_extraction")
            )
            
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=result
                    )
                ]
            }
            
        elif tool_name == "prp_details":
            # Obter detalhes do PRP
            result = await get_prp_details(
                agent_deps,
                prp_id=args["prp_id"]
            )
            
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=result
                    )
                ]
            }
            
        elif tool_name == "prp_chat":
            # Conversar com o agente
            context = args.get("context", "")
            full_message = args["message"]
            if context:
                full_message = f"Contexto: {context}\n\nMensagem: {args['message']}"
            
            result = await chat_with_prp_agent(full_message, agent_deps)
            
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=result
                    )
                ]
            }
            
        elif tool_name == "prp_update_status":
            # Atualizar status do PRP
            from agents.tools import update_prp_status
            
            result = await update_prp_status(
                agent_deps,
                prp_id=args["prp_id"],
                new_status=args["new_status"]
            )
            
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=result
                    )
                ]
            }
            
        else:
            raise ValueError(f"Ferramenta desconhecida: {tool_name}")
            
    except Exception as e:
        logger.error(f"Erro ao executar ferramenta {tool_name}: {e}")
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"❌ Erro ao executar {tool_name}: {str(e)}"
                )
            ]
        }

async def main():
    """Função principal do servidor MCP."""
    
    logger.info("🚀 Iniciando servidor MCP do Agente PRP...")
    
    # Configurar transporte stdio
    transport = StdioServerTransport()
    
    # Conectar servidor
    await server.connect(transport)
    
    logger.info("✅ Servidor MCP do Agente PRP iniciado!")

if __name__ == "__main__":
    asyncio.run(main()) 