#!/usr/bin/env python3
"""
CLI direto para integração com Cursor Agent.

Uso:
    python cursor_cli.py "mensagem aqui"
    python cursor_cli.py "criar prp para login" --file="código.py"
    python cursor_cli.py "analisar projeto" --insights
"""

import asyncio
import sys
import argparse
from agents.agent import chat_with_prp_agent_sync, PRPAgentDependencies
from agents.tools import search_prps, create_prp, analyze_prp_with_llm


def process_message(message: str, file_context: str = None, action: str = "chat") -> str:
    """Processa mensagem via agente PRP."""
    
    try:
        # Configurar dependências
        deps = PRPAgentDependencies(
            session_id="cursor-agent-session"
        )
        
        if action == "chat":
            # Chat normal
            response = chat_with_prp_agent_sync(message, deps)
            return response
            
        elif action == "insights":
            # Insights do projeto
            insight_prompt = f"Forneça insights sobre o projeto atual. Contexto: {message}"
            if file_context:
                insight_prompt += f"\n\nArquivo analisado:\n{file_context}"
            
            response = chat_with_prp_agent_sync(insight_prompt, deps)
            return response
            
        elif action == "create_prp":
            # Criar PRP
            prp_prompt = f"Crie um PRP detalhado para: {message}"
            if file_context:
                prp_prompt += f"\n\nBasear no código:\n{file_context}"
            
            response = chat_with_prp_agent_sync(prp_prompt, deps)
            return response
            
        else:
            return f"❌ Ação desconhecida: {action}"
            
    except Exception as e:
        return f"❌ Erro: {str(e)}"


def main():
    """CLI principal."""
    
    parser = argparse.ArgumentParser(description="PRP Agent CLI para Cursor")
    parser.add_argument("message", help="Mensagem para o agente")
    parser.add_argument("--file", help="Contexto de arquivo", default=None)
    parser.add_argument("--insights", action="store_true", help="Obter insights do projeto")
    parser.add_argument("--create-prp", action="store_true", help="Criar novo PRP")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    
    args = parser.parse_args()
    
    # Determinar ação
    action = "chat"
    if args.insights:
        action = "insights"
    elif args.create_prp:
        action = "create_prp"
    
    # Processar
    response = process_message(args.message, args.file, action)
    
    # Saída
    if args.json:
        import json
        result = {
            "success": not response.startswith("❌"),
            "response": response,
            "action": action,
            "message": args.message
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(response)


if __name__ == "__main__":
    main()