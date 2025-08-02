#!/usr/bin/env python3
"""
CLI conversacional para o agente PRP.

Interface de linha de comando interativa para trabalhar com PRPs.
"""

import asyncio
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from agents.agent import chat_with_prp_agent, PRPAgentDependencies, get_agent_stats
from agents.settings import settings

console = Console()

def show_welcome():
    """Mostrar tela de boas-vindas."""
    welcome_text = """
[bold blue]🤖 Agente PRP - Assistente de Product Requirement Prompts[/bold blue]

[green]Análise LLM automática e gerenciamento de PRPs[/green]

[dim]Comandos disponíveis:[/dim]
• [bold]criar[/bold] - Criar novo PRP
• [bold]buscar[/bold] - Buscar PRPs existentes  
• [bold]analisar[/bold] - Analisar PRP com LLM
• [bold]detalhes[/bold] - Ver detalhes de um PRP
• [bold]status[/bold] - Atualizar status de PRP
• [bold]stats[/bold] - Ver estatísticas do agente
• [bold]ajuda[/bold] - Mostrar esta ajuda
• [bold]sair[/bold] - Sair do programa

[dim]Digite 'sair' para sair[/dim]
"""
    
    panel = Panel(
        welcome_text,
        title="[bold blue]Bem-vindo ao Agente PRP[/bold blue]",
        style="blue",
        padding=(1, 2)
    )
    console.print(panel)

def show_help():
    """Mostrar ajuda detalhada."""
    help_text = """
[bold]Comandos Disponíveis:[/bold]

[bold green]criar[/bold green] - Criar novo PRP
  Exemplo: "criar um PRP para sistema de autenticação"

[bold green]buscar[/bold green] - Buscar PRPs existentes
  Exemplo: "buscar PRPs sobre autenticação"
  Exemplo: "buscar PRPs com status draft"

[bold green]analisar[/bold green] - Analisar PRP com LLM
  Exemplo: "analisar PRP com ID 1"
  Exemplo: "extrair tarefas do PRP 1"

[bold green]detalhes[/bold green] - Ver detalhes de um PRP
  Exemplo: "detalhes do PRP 1"
  Exemplo: "mostrar PRP 1"

[bold green]status[/bold green] - Atualizar status de PRP
  Exemplo: "mudar status do PRP 1 para active"

[bold green]stats[/bold green] - Ver estatísticas do agente
  Mostra informações sobre sessão e conversas

[bold green]ajuda[/bold green] - Mostrar esta ajuda

[bold green]sair[/bold green] - Sair do programa

[dim]Você também pode conversar naturalmente com o agente![/dim]
"""
    
    panel = Panel(
        help_text,
        title="[bold green]Ajuda do Agente PRP[/bold green]",
        style="green",
        padding=(1, 2)
    )
    console.print(panel)

def show_stats(deps: PRPAgentDependencies):
    """Mostrar estatísticas do agente."""
    stats = get_agent_stats(deps)
    
    table = Table(title="📊 Estatísticas do Agente PRP")
    table.add_column("Métrica", style="cyan", no_wrap=True)
    table.add_column("Valor", style="magenta")
    
    table.add_row("Session ID", stats["session_id"])
    table.add_row("Conversas", str(stats["conversation_count"]))
    table.add_row("Banco de Dados", stats["database_path"])
    table.add_row("Max Tokens/Análise", str(stats["max_tokens_per_analysis"]))
    
    console.print(table)
    
    if stats["conversation_count"] > 0:
        console.print(f"\n[dim]Últimas conversas: {stats['conversation_count']}[/dim]")

async def handle_command(command: str, deps: PRPAgentDependencies) -> bool:
    """Processar comandos especiais."""
    
    command_lower = command.lower().strip()
    
    if command_lower == "sair" or command_lower == "quit" or command_lower == "exit":
        console.print("\n[yellow]👋 Até logo![/yellow]")
        return False
        
    elif command_lower == "ajuda" or command_lower == "help":
        show_help()
        return True
        
    elif command_lower == "stats" or command_lower == "estatisticas":
        show_stats(deps)
        return True
        
    elif command_lower == "limpar":
        if Confirm.ask("Deseja limpar o histórico de conversas?"):
            deps.conversation_history.clear()
            console.print("[green]✅ Histórico limpo![/green]")
        return True
        
    elif command_lower == "teste":
        console.print("[yellow]🧪 Modo de teste ativado![/yellow]")
        response = await chat_with_prp_agent("Olá! Teste de funcionamento.", deps, use_test_model=True)
        console.print(f"[bold blue]Agente:[/bold blue] {response}")
        return True
    
    # Se não for comando especial, processar normalmente
    return None

async def main():
    """Loop principal da conversação."""
    
    # Mostrar boas-vindas
    show_welcome()
    console.print()
    
    # Configurar dependências
    deps = PRPAgentDependencies(
        database_path=settings.database_path,
        session_id=f"cli-session-{os.getpid()}"
    )
    
    # Verificar configurações
    console.print(f"[dim]📁 Banco: {deps.database_path}[/dim]")
    console.print(f"[dim]🤖 Modelo: {settings.llm_model}[/dim]")
    console.print()
    
    while True:
        try:
            # Obter entrada do usuário
            user_input = Prompt.ask("[bold green]Você").strip()
            
            # Lidar com entrada vazia
            if not user_input:
                continue
            
            # Processar comandos especiais
            command_result = await handle_command(user_input, deps)
            if command_result is False:
                break
            elif command_result is True:
                continue
            
            # Processar com o agente
            console.print("[bold blue]Agente:[/bold blue] ", end="")
            
            # Mostrar indicador de processamento
            with console.status("[bold green]Processando..."):
                response = await chat_with_prp_agent(user_input, deps)
            
            # Formatar resposta
            if response.startswith("✅") or response.startswith("🔍") or response.startswith("🧠"):
                # Resposta de sucesso - usar cor verde
                console.print(f"[green]{response}[/green]")
            elif response.startswith("❌"):
                # Resposta de erro - usar cor vermelha
                console.print(f"[red]{response}[/red]")
            else:
                # Resposta normal
                console.print(response)
            
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'sair' para sair[/yellow]")
            continue
            
        except Exception as e:
            console.print(f"[red]❌ Erro: {e}[/red]")
            console.print("[dim]Tente novamente ou digite 'ajuda' para ver os comandos[/dim]")
            continue

def run_cli():
    """Executar CLI de forma síncrona."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Até logo![/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Erro fatal: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    run_cli() 