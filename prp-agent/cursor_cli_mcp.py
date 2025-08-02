#!/usr/bin/env python3
"""
CLI com integração MCP REAL para Cursor Agent.

Este script usa MCP Turso REAL ao invés de simulações.
"""

import asyncio
import sys
import argparse
import json
from typing import Dict, Any
from agents.agent import chat_with_prp_agent_sync, PRPAgentDependencies


def call_mcp_turso_real(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chama MCP Turso REAL disponível no Cursor Agent.
    
    NOTA: Esta função usa as ferramentas MCP reais do Cursor
    ao invés das simulações usadas nos outros arquivos.
    """
    
    try:
        # Importar ferramentas MCP Turso reais (disponíveis no Cursor Agent)
        # Estas devem estar disponíveis quando executado no ambiente Cursor
        
        if tool_name == "add_conversation":
            # Usar MCP real para adicionar conversa
            from mcp_turso import add_conversation
            return add_conversation(
                session_id=params.get("session_id", "cursor-agent"),
                message=params.get("message", ""),
                response=params.get("response", ""),
                context=params.get("context", None),
                database=params.get("database", "context-memory")
            )
            
        elif tool_name == "execute_query":
            # Usar MCP real para queries
            from mcp_turso import execute_query
            return execute_query(
                query=params.get("query", ""),
                params=params.get("params", []),
                database=params.get("database", "context-memory")
            )
            
        elif tool_name == "execute_read_only_query":
            # Usar MCP real para leitura
            from mcp_turso import execute_read_only_query
            return execute_read_only_query(
                query=params.get("query", ""),
                params=params.get("params", []),
                database=params.get("database", "context-memory")
            )
            
        else:
            print(f"⚠️ Ferramenta MCP desconhecida: {tool_name}")
            return {"success": False, "error": f"Ferramenta {tool_name} não implementada"}
            
    except ImportError as e:
        # MCP não disponível - fallback para o agente normal
        print(f"🔧 MCP não disponível: {e}")
        print("💡 Usando agente padrão sem persistência MCP")
        return {"success": False, "error": "MCP não disponível", "fallback": True}
        
    except Exception as e:
        print(f"❌ Erro MCP: {e}")
        return {"success": False, "error": str(e)}


def process_message_with_mcp(message: str, file_context: str = None, action: str = "chat") -> str:
    """Processa mensagem usando MCP real quando disponível."""
    
    try:
        # Configurar dependências
        deps = PRPAgentDependencies(
            session_id="cursor-agent-mcp-session"
        )
        
        # Processar com agente
        if action == "chat":
            response = chat_with_prp_agent_sync(message, deps)
        elif action == "insights":
            insight_prompt = f"Forneça insights sobre o projeto. Contexto: {message}"
            if file_context:
                insight_prompt += f"\n\nArquivo:\n{file_context}"
            response = chat_with_prp_agent_sync(insight_prompt, deps)
        elif action == "create_prp":
            prp_prompt = f"Crie um PRP detalhado para: {message}"
            if file_context:
                prp_prompt += f"\n\nCódigo base:\n{file_context}"
            response = chat_with_prp_agent_sync(prp_prompt, deps)
        else:
            response = f"❌ Ação desconhecida: {action}"
        
        # Tentar salvar no MCP real
        mcp_result = call_mcp_turso_real("add_conversation", {
            "session_id": deps.session_id,
            "message": message,
            "response": response,
            "context": file_context,
            "database": "context-memory"
        })
        
        if mcp_result.get("success"):
            print(f"💾 MCP: Conversa salva com ID {mcp_result.get('conversation_id', 'N/A')}")
        elif not mcp_result.get("fallback"):
            print(f"⚠️ MCP falhou: {mcp_result.get('error')}")
        
        return response
        
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def main():
    """CLI principal com MCP real."""
    
    parser = argparse.ArgumentParser(description="PRP Agent CLI com MCP Real")
    parser.add_argument("message", nargs="?", help="Mensagem para o agente")
    parser.add_argument("--file", help="Contexto de arquivo", default=None)
    parser.add_argument("--insights", action="store_true", help="Obter insights")
    parser.add_argument("--create-prp", action="store_true", help="Criar PRP")
    parser.add_argument("--json", action="store_true", help="Saída JSON")
    parser.add_argument("--test-mcp", action="store_true", help="Testar conexão MCP")
    
    args = parser.parse_args()
    
    # Testar MCP se solicitado
    if args.test_mcp:
        mcp_test = call_mcp_turso_real("execute_read_only_query", {
            "query": "SELECT COUNT(*) as total FROM conversations",
            "database": "context-memory"
        })
        
        result = {
            "mcp_available": mcp_test.get("success", False),
            "error": mcp_test.get("error") if not mcp_test.get("success") else None,
            "test_query": "SELECT COUNT(*) as total FROM conversations"
        }
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # Verificar se message foi fornecido
    if not args.message:
        parser.error("message é obrigatório quando não usando --test-mcp")
    
    # Determinar ação
    action = "chat"
    if args.insights:
        action = "insights"
    elif args.create_prp:
        action = "create_prp"
    
    # Processar com MCP
    response = process_message_with_mcp(args.message, args.file, action)
    
    # Saída
    if args.json:
        result = {
            "success": not response.startswith("❌"),
            "response": response,
            "action": action,
            "message": args.message,
            "mcp_enabled": True
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(response)


if __name__ == "__main__":
    main()