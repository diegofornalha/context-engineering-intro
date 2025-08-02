#!/usr/bin/env python3
"""
Script simples para gerar PRPs via agent
Sem dependências complexas de configuração
"""

import asyncio
import sys
import os
from pathlib import Path

# Configurar ambiente simples
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "true"

async def generate_prp_simple():
    """
    Gera um PRP de forma simples
    """
    
    print("🤖 GERANDO PRP VIA AGENT SIMPLES")
    print("=" * 60)
    print()
    
    try:
        # Importar o agente do archive (que funciona)
        sys.path.insert(0, str(Path(__file__).parent / "archive"))
        from cursor_turso_integration import CursorTursoIntegration
        
        # Criar instância do agente
        agent = CursorTursoIntegration()
        
        print("✅ Agente carregado com sucesso!")
        print()
        
        # Definir PRP para gerar
        feature = "Sistema de Gerenciamento de Projetos"
        context = """
        Preciso de um sistema completo para gerenciar projetos de desenvolvimento.
        O sistema deve incluir:
        - Gestão de projetos e equipes
        - Controle de tarefas e milestones
        - Dashboard de progresso
        - Integração com Git
        - Relatórios de performance
        - Notificações automáticas
        """
        
        print(f"📄 Gerando PRP para: {feature}")
        print(f"📋 Contexto: {context.strip()}")
        print()
        
        # Gerar PRP
        response = await agent.suggest_prp(feature, context)
        
        print("✅ PRP GERADO COM SUCESSO!")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Salvar no banco
        print("\n💾 Salvando PRP no banco Turso...")
        prp_id = await agent.store_prp_suggestion(
            feature=feature,
            context=context,
            prp_content=response
        )
        
        if prp_id > 0:
            print(f"✅ PRP salvo com ID: {prp_id}")
        else:
            print("❌ Erro ao salvar PRP no banco")
        
        print("\n🎉 PRP gerado e salvo com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PRP: {e}")
        print("💡 Verifique se o agente está configurado corretamente")

async def generate_prp_interactive():
    """
    Gera PRP de forma interativa
    """
    
    print("🤖 GERADOR DE PRP INTERATIVO")
    print("=" * 60)
    print()
    
    try:
        # Importar o agente
        sys.path.insert(0, str(Path(__file__).parent / "archive"))
        from cursor_turso_integration import CursorTursoIntegration
        
        agent = CursorTursoIntegration()
        
        print("✅ Agente carregado!")
        print()
        
        # Solicitar dados do usuário
        print("📝 Digite os dados do PRP:")
        feature = input("Nome do sistema/feature: ").strip()
        
        if not feature:
            feature = "Sistema de Exemplo"
        
        print("\n📋 Descreva o contexto (pressione Enter duas vezes para finalizar):")
        context_lines = []
        while True:
            line = input()
            if line == "" and context_lines and context_lines[-1] == "":
                break
            context_lines.append(line)
        
        context = "\n".join(context_lines[:-1]) if context_lines else """
        Sistema para gerenciar dados e processos.
        Inclui interface web, API REST e banco de dados.
        """
        
        print(f"\n📄 Gerando PRP para: {feature}")
        print(f"📋 Contexto: {context.strip()}")
        print()
        
        # Gerar PRP
        response = await agent.suggest_prp(feature, context)
        
        print("✅ PRP GERADO COM SUCESSO!")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Perguntar se quer salvar
        save = input("\n💾 Salvar PRP no banco? (s/n): ").strip().lower()
        
        if save in ['s', 'sim', 'y', 'yes']:
            print("💾 Salvando PRP no banco Turso...")
            prp_id = await agent.store_prp_suggestion(
                feature=feature,
                context=context,
                prp_content=response
            )
            
            if prp_id > 0:
                print(f"✅ PRP salvo com ID: {prp_id}")
            else:
                print("❌ Erro ao salvar PRP no banco")
        else:
            print("📄 PRP gerado mas não salvo no banco")
        
        print("\n🎉 PRP gerado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PRP: {e}")

async def show_available_commands():
    """
    Mostra comandos disponíveis
    """
    
    print("📋 COMANDOS DISPONÍVEIS PARA GERAR PRPs:")
    print("=" * 60)
    print()
    
    print("1. 🚀 Gerar PRP automático:")
    print("   python generate_prp_simple.py")
    print()
    
    print("2. 💬 Gerar PRP interativo:")
    print("   python generate_prp_simple.py --interactive")
    print()
    
    print("3. 📄 Usar PRP especialista Turso:")
    print("   python demo_turso_specialist_prp.py")
    print()
    
    print("4. 🔧 Usar PRP especialista Turso (com credenciais):")
    print("   python use_turso_specialist_prp.py")
    print()
    
    print("5. 📋 Listar PRPs existentes:")
    print("   python list_prps_final.py")
    print()
    
    print("6. 🎯 CLI principal do agente:")
    print("   python cli.py")
    print()
    
    print("7. 🗄️ CLI do Turso Agent:")
    print("   cd ../turso-agent && python main.py")
    print()

async def main():
    """
    Função principal
    """
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await generate_prp_interactive()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        await show_available_commands()
    else:
        await generate_prp_simple()
        print("\n" + "=" * 60)
        print("💡 Para gerar PRP interativo: python generate_prp_simple.py --interactive")
        print("💡 Para ver todos os comandos: python generate_prp_simple.py --help")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 