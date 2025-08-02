#!/usr/bin/env python3
"""
Turso Agent - Agente Especialista em Turso Database & MCP Integration

Baseado no PRP ID 6: Agente Especialista em Turso Database e MCP Integration
Implementa todos os padrões e funcionalidades especializadas em Turso.
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import sqlite3
import json
from datetime import datetime

# Adicionar diretórios ao path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from agents.turso_specialist_pydantic_new import (
    TursoContext,
    TursoSettings,
    chat_with_turso_agent,
    analyze_performance,
    security_audit,
    troubleshoot_issue,
    optimize_system,
    run_validation_gates,
    get_system_info
)
from tools.turso_manager import TursoManager
from tools.mcp_integrator import MCPTursoIntegrator

class TursoAgentCLI:
    """CLI principal para o Turso Agent Especialista"""
    
    def __init__(self):
        self.settings = TursoSettings()
        self.turso_manager = TursoManager(self.settings)
        self.mcp_integrator = MCPTursoIntegrator(self.settings)
        
        # Criar contexto para o agente PydanticAI
        self.context = TursoContext(
            session_id=f"cli-session-{datetime.now().isoformat()}",
            turso_manager=self.turso_manager,
            mcp_integrator=self.mcp_integrator,
            settings=self.settings
        )
        
    async def show_banner(self):
        """Mostra banner do Turso Agent"""
        print("\n" + "="*60)
        print("🎯 TURSO AGENT - ESPECIALISTA EM TURSO DATABASE & MCP")
        print("="*60)
        print("📊 Baseado no PRP ID 6: Agente Especialista Turso")
        print("🗄️ Turso Database | 🔌 MCP Integration | ⚡ Performance")
        print("🛡️ Security Expert | 🔧 Troubleshooting | 📈 Optimization")
        print("="*60)
        
        # Verificar status do sistema
        await self.check_system_status()
        print()
        
    async def check_system_status(self):
        """Verifica status do sistema Turso"""
        print("\n🔍 STATUS DO SISTEMA:")
        
        # Verificar PRP base
        prp_status = self.check_prp_availability()
        print(f"   📋 PRP Turso (ID 6): {prp_status}")
        
        # Verificar configurações Turso
        config_status = await self.turso_manager.check_configuration()
        print(f"   ⚙️ Configuração Turso: {config_status}")
        
        # Verificar MCP integration
        mcp_status = await self.mcp_integrator.check_mcp_status()
        print(f"   🔌 MCP Integration: {mcp_status}")
        
    def check_prp_availability(self) -> str:
        """Verifica se o PRP Turso está disponível"""
        try:
            db_path = Path(__file__).parent.parent / "context-memory.db"
            if not db_path.exists():
                return "❌ Context DB não encontrado"
                
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, title, status FROM prps WHERE id = 6')
            prp = cursor.fetchone()
            conn.close()
            
            if prp:
                return f"✅ {prp[1]} ({prp[2]})"
            else:
                return "❌ PRP Turso não encontrado"
                
        except Exception as e:
            return f"❌ Erro: {str(e)}"
    
    async def show_menu(self):
        """Mostra menu de opções"""
        print("\n🎯 OPÇÕES DISPONÍVEIS:")
        print("="*40)
        print("1. 🗄️  Database Operations")
        print("2. 🔌 MCP Integration")
        print("3. ⚡ Performance Analysis")
        print("4. 🛡️  Security Audit")
        print("5. 🔧 Troubleshooting")
        print("6. 📈 System Optimization")
        print("7. 📋 Validation Gates")
        print("8. 💬 Chat Interativo")
        print("9. ℹ️  System Info")
        print("0. 🚪 Sair")
        print("="*40)
        
    async def handle_database_operations(self):
        """Gerencia operações de database"""
        print("\n🗄️ DATABASE OPERATIONS:")
        print("1. Listar databases")
        print("2. Criar database")
        print("3. Executar query")
        print("4. Backup database")
        print("5. Migração de schema")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            await self.turso_manager.list_databases()
        elif choice == "2":
            name = input("Nome do database: ")
            await self.turso_manager.create_database(name)
        elif choice == "3":
            query = input("Query SQL: ")
            await self.turso_manager.execute_query(query)
        elif choice == "4":
            db_name = input("Database para backup: ")
            await self.turso_manager.backup_database(db_name)
        elif choice == "5":
            await self.turso_manager.run_migrations()
            
    async def handle_mcp_integration(self):
        """Gerencia integração MCP"""
        print("\n🔌 MCP INTEGRATION:")
        print("1. Setup MCP Server")
        print("2. Test MCP Connection")
        print("3. Generate Database Token")
        print("4. Configure LLM Integration")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            await self.mcp_integrator.setup_mcp_server()
        elif choice == "2":
            await self.mcp_integrator.test_connection()
        elif choice == "3":
            db_name = input("Database name: ")
            await self.mcp_integrator.generate_token(db_name)
        elif choice == "4":
            await self.mcp_integrator.configure_llm_integration()
            
    async def handle_performance_analysis(self):
        """Análise de performance"""
        print("\n⚡ PERFORMANCE ANALYSIS:")
        result = await analyze_performance(self.context)
        print(result)
        
    async def handle_security_audit(self):
        """Auditoria de segurança"""
        print("\n🛡️ SECURITY AUDIT:")
        result = await security_audit(self.context)
        print(result)
        
    async def handle_troubleshooting(self):
        """Troubleshooting do sistema"""
        print("\n🔧 TROUBLESHOOTING:")
        issue = input("Descreva o problema: ")
        result = await troubleshoot_issue(issue, self.context)
        print(result)
        
    async def handle_optimization(self):
        """Otimização do sistema"""
        print("\n📈 SYSTEM OPTIMIZATION:")
        result = await optimize_system(self.context)
        print(result)
        
    async def handle_validation_gates(self):
        """Executa validation gates do PRP"""
        print("\n📋 VALIDATION GATES:")
        result = await run_validation_gates(self.context)
        print(result)
        
    async def handle_interactive_chat(self):
        """Chat interativo com o agente"""
        print("\n💬 CHAT INTERATIVO:")
        print("Digite 'sair' para voltar ao menu principal")
        
        while True:
            user_input = input("\n👤 Você: ").strip()
            if user_input.lower() in ['sair', 'exit', 'quit']:
                break
                
            response = await chat_with_turso_agent(user_input, self.context)
            print(f"🤖 Turso Agent: {response}")
            
    async def show_system_info(self):
        """Mostra informações do sistema"""
        print("\n ℹ️ SYSTEM INFO:")
        info = await get_system_info(self.context)
        print(info)
        
    async def run(self):
        """Executa o CLI principal"""
        await self.show_banner()
        
        while True:
            await self.show_menu()
            choice = input("\nEscolha uma opção: ").strip()
            
            try:
                if choice == "1":
                    await self.handle_database_operations()
                elif choice == "2":
                    await self.handle_mcp_integration()
                elif choice == "3":
                    await self.handle_performance_analysis()
                elif choice == "4":
                    await self.handle_security_audit()
                elif choice == "5":
                    await self.handle_troubleshooting()
                elif choice == "6":
                    await self.handle_optimization()
                elif choice == "7":
                    await self.handle_validation_gates()
                elif choice == "8":
                    await self.handle_interactive_chat()
                elif choice == "9":
                    await self.show_system_info()
                elif choice == "0":
                    print("\n👋 Turso Agent encerrado. Até logo!")
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Turso Agent encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro: {str(e)}")
                print("Tente novamente ou escolha outra opção.")

def main():
    """Função principal"""
    try:
        cli = TursoAgentCLI()
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print("\n👋 Saindo...")
    except Exception as e:
        print(f"❌ Erro fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()