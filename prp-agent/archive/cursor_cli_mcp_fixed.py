#!/usr/bin/env python3
"""
🎯 CLI CORRIGIDO: PRP Agent com MCP Turso Integration

Este CLI usa MCP Turso CORRETAMENTE:
1. Busca contexto antes de responder
2. Inclui contexto na resposta  
3. Salva conversa no MCP Turso

USO: python cursor_cli_mcp_fixed.py "sua pergunta" [--insights] [--create-prp] [--json]
"""

import asyncio
import sys
import argparse
import json
import os
from typing import Dict, Any

# Import do agente CORRETO com MCP Turso
from agents.agent_with_mcp_turso import chat_with_prp_agent_mcp_sync
from agents.dependencies import PRPAgentDependencies


def process_message_with_mcp_context(message: str, file_context: str = None, action: str = "chat") -> Dict[str, Any]:
    """
    Processa mensagem usando MCP Turso para contexto.
    
    ESTE é o método correto que busca contexto antes de responder!
    """
    
    try:
        # Configurar dependências
        deps = PRPAgentDependencies(
            session_id=f"cursor-mcp-session-{os.getpid()}"
        )
        
        # Preparar mensagem com contexto de arquivo se fornecido
        full_message = message
        if file_context:
            full_message = f"CONTEXTO DO ARQUIVO:\n{file_context}\n\nPERGUNTA: {message}"
        
        # Processar baseado na ação
        if action == "chat":
            # 🧠 Conversa normal COM contexto MCP Turso
            response = chat_with_prp_agent_mcp_sync(full_message, deps)
            
        elif action == "insights":
            # 📊 Insights sobre projeto COM contexto MCP
            insight_prompt = f"Forneça insights detalhados sobre o projeto. Analise especificamente: {message}"
            if file_context:
                insight_prompt += f"\n\nContexto adicional do arquivo:\n{file_context}"
            response = chat_with_prp_agent_mcp_sync(insight_prompt, deps)
            
        elif action == "create_prp":
            # 🎯 Criação de PRP COM contexto do projeto
            prp_prompt = f"""Crie um PRP (Product Requirement Prompt) detalhado para: {message}

Baseie-se no contexto do projeto existente e siga as melhores práticas de PRPs.
Inclua: objetivo, requisitos, implementação, validação e critérios de sucesso."""
            if file_context:
                prp_prompt += f"\n\nCódigo/contexto de referência:\n{file_context}"
            response = chat_with_prp_agent_mcp_sync(prp_prompt, deps)
            
        else:
            response = f"❌ Ação desconhecida: {action}"
        
        return {
            "success": True,
            "response": response,
            "action": action,
            "message": message,
            "mcp_enabled": True,
            "session_id": deps.session_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "action": action,
            "message": message,
            "mcp_enabled": False
        }


def main():
    """CLI principal com MCP Turso habilitado."""
    
    parser = argparse.ArgumentParser(
        description="🎯 PRP Agent CLI com MCP Turso - Contexto Inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS DE USO:

Conversa normal:
  python cursor_cli_mcp_fixed.py "O que é este projeto?"

Insights do projeto:
  python cursor_cli_mcp_fixed.py "Status do projeto" --insights

Criar PRP:
  python cursor_cli_mcp_fixed.py "Sistema de autenticação" --create-prp

Com contexto de arquivo:
  python cursor_cli_mcp_fixed.py "Analise este código" --file "conteúdo do arquivo"

Saída JSON:
  python cursor_cli_mcp_fixed.py "Como começar?" --json

🧠 DIFERENCIAL: Este CLI busca contexto no MCP Turso antes de responder!
        """
    )
    
    parser.add_argument("message", help="Mensagem/pergunta para o agente")
    parser.add_argument("--file", help="Contexto de arquivo (conteúdo)", default=None)
    parser.add_argument("--insights", action="store_true", help="Obter insights do projeto")
    parser.add_argument("--create-prp", action="store_true", help="Criar novo PRP")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON")
    parser.add_argument("--debug", action="store_true", help="Modo debug com informações detalhadas")
    
    args = parser.parse_args()
    
    # Determinar ação
    action = "chat"
    if args.insights:
        action = "insights"
    elif args.create_prp:
        action = "create_prp"
    
    # Debug info
    if args.debug:
        print(f"🔍 DEBUG: Ação={action}, MCP=Enabled, Arquivo={'Sim' if args.file else 'Não'}")
    
    # Processar com MCP Turso
    result = process_message_with_mcp_context(args.message, args.file, action)
    
    # Saída
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Saída formatada para humanos
        if result["success"]:
            print(result["response"])
            
            if args.debug:
                print(f"\n🔧 DEBUG: Session ID: {result.get('session_id', 'N/A')}")
                print(f"🧠 MCP Habilitado: {result.get('mcp_enabled', False)}")
        else:
            print(f"❌ Erro: {result['error']}")
            
            if args.debug:
                print(f"🔧 DEBUG: MCP Status: {result.get('mcp_enabled', 'Unknown')}")


def demo_mcp_cli():
    """Demo do CLI com MCP Turso."""
    
    print("🧪 DEMO: CLI com MCP Turso Integration")
    print("=" * 50)
    
    demo_commands = [
        {
            "command": "Como alguém novo no projeto, o que preciso saber?",
            "action": "chat",
            "description": "Pergunta básica com contexto do projeto"
        },
        {
            "command": "Status atual do desenvolvimento",
            "action": "insights",
            "description": "Insights sobre progresso do projeto"
        },
        {
            "command": "Sistema de notificações em tempo real",
            "action": "create_prp", 
            "description": "Criação de PRP com contexto"
        }
    ]
    
    for i, demo in enumerate(demo_commands, 1):
        print(f"\n{i}️⃣ **{demo['description']}:**")
        print(f"   Comando: python cursor_cli_mcp_fixed.py \"{demo['command']}\" --{demo['action']}")
        print(f"   🧠 MCP Turso: Busca contexto relevante antes de responder")
        
        # Simular execução
        result = process_message_with_mcp_context(demo['command'], action=demo['action'])
        if result['success']:
            print(f"   ✅ Resposta: {result['response'][:100]}...")
        else:
            print(f"   ❌ Erro: {result['error']}")
    
    print(f"\n🎯 **RESULTADO:** Todas as respostas incluem contexto do projeto!")


if __name__ == "__main__":
    # Verificar se é chamada para demo
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mcp_cli()
    else:
        main()