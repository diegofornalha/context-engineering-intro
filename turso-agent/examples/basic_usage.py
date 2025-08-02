#!/usr/bin/env python3
"""
Turso Agent - Exemplo de Uso Básico
Demonstra funcionalidades essenciais do agente especialista Turso
"""

import asyncio
import sys
from pathlib import Path

# Adicionar path do turso-agent
sys.path.append(str(Path(__file__).parent.parent))

from config.turso_settings import TursoSettings
from tools.turso_manager import TursoManager
from tools.mcp_integrator import MCPTursoIntegrator
from agents.turso_specialist import TursoSpecialistAgent

async def exemplo_configuracao_basica():
    """Exemplo 1: Configuração básica do Turso Agent"""
    
    print("🎯 **EXEMPLO 1: CONFIGURAÇÃO BÁSICA**")
    print("="*45)
    
    # Criar configurações
    settings = TursoSettings()
    
    # Mostrar resumo de configuração
    print(settings.summary())
    
    print("✅ Configuração básica completa!")

async def exemplo_operacoes_database():
    """Exemplo 2: Operações básicas de database"""
    
    print("\\n🎯 **EXEMPLO 2: OPERAÇÕES DE DATABASE**")
    print("="*50)
    
    try:
        # Inicializar componentes
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        
        # Verificar configuração
        config_status = await turso_manager.check_configuration()
        print(f"📊 Status da configuração: {config_status}")
        
        # Listar databases
        print("\\n📋 Listando databases...")
        databases = await turso_manager.list_databases()
        
        if databases:
            print(f"✅ Encontrados {len(databases)} databases")
        else:
            print("ℹ️ Nenhum database encontrado ou erro na listagem")
        
        # Exemplo de query read-only
        if settings.default_database:
            print(f"\\n💻 Testando query no database: {settings.default_database}")
            result = await turso_manager.execute_read_only_query(
                "SELECT name FROM sqlite_master WHERE type='table';",
                settings.default_database
            )
            
            if result.get('success'):
                print("✅ Query executada com sucesso!")
                print(f"📊 Resultado: {result.get('result', '')[:100]}...")
            else:
                print(f"❌ Erro na query: {result.get('error')}")
        
        print("✅ Operações de database completas!")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")

async def exemplo_integracao_mcp():
    """Exemplo 3: Integração MCP"""
    
    print("\\n🎯 **EXEMPLO 3: INTEGRAÇÃO MCP**")
    print("="*40)
    
    try:
        # Inicializar MCP integrator
        settings = TursoSettings()
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Verificar status MCP
        mcp_status = await mcp_integrator.check_mcp_status()
        print(f"🔌 Status MCP: {mcp_status}")
        
        # Testar conexão MCP
        print("\\n🧪 Testando conexão MCP...")
        test_results = await mcp_integrator.test_connection()
        
        if test_results.get('overall_status') == 'success':
            print("✅ Todos os testes MCP passaram!")
        else:
            print("⚠️ Alguns testes MCP falharam")
            for test_name, result in test_results.get('tests', {}).items():
                icon = "✅" if result else "❌"
                print(f"   {icon} {test_name}")
        
        print("✅ Teste MCP completo!")
        
    except Exception as e:
        print(f"❌ Erro no teste MCP: {e}")

async def exemplo_chat_especialista():
    """Exemplo 4: Chat com agente especialista"""
    
    print("\\n🎯 **EXEMPLO 4: CHAT ESPECIALISTA**")
    print("="*45)
    
    try:
        # Inicializar agente completo
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Perguntas de exemplo
        perguntas = [
            "Como criar um novo database Turso?",
            "Como configurar integração MCP?",
            "Quais são as best practices de performance?",
            "Como resolver problemas de conexão?",
            "Como implementar security policies?"
        ]
        
        print("💬 Testando chat especialista:")
        
        for i, pergunta in enumerate(perguntas, 1):
            print(f"\\n{i}. 👤 Pergunta: {pergunta}")
            
            resposta = await agent.chat(pergunta)
            print(f"🤖 Resposta: {resposta[:200]}...")
            
            # Pequena pausa entre perguntas
            await asyncio.sleep(0.5)
        
        print("\\n✅ Chat especialista testado!")
        
    except Exception as e:
        print(f"❌ Erro no chat: {e}")

async def exemplo_analise_performance():
    """Exemplo 5: Análise de performance"""
    
    print("\\n🎯 **EXEMPLO 5: ANÁLISE DE PERFORMANCE**")
    print("="*50)
    
    try:
        # Inicializar agente
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Executar análise de performance
        print("⚡ Executando análise de performance...")
        analysis_result = await agent.analyze_performance()
        print(analysis_result)
        
        print("✅ Análise de performance completa!")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")

async def exemplo_security_audit():
    """Exemplo 6: Auditoria de segurança"""
    
    print("\\n🎯 **EXEMPLO 6: AUDITORIA DE SEGURANÇA**")
    print("="*50)
    
    try:
        # Inicializar agente
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Executar auditoria de segurança
        print("🛡️ Executando auditoria de segurança...")
        audit_result = await agent.security_audit()
        print(audit_result)
        
        print("✅ Auditoria de segurança completa!")
        
    except Exception as e:
        print(f"❌ Erro na auditoria: {e}")

async def exemplo_validation_gates():
    """Exemplo 7: Validation Gates do PRP"""
    
    print("\\n🎯 **EXEMPLO 7: VALIDATION GATES**")
    print("="*45)
    
    try:
        # Inicializar agente
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Executar validation gates
        print("📋 Executando validation gates do PRP...")
        validation_result = await agent.run_validation_gates()
        print(validation_result)
        
        print("✅ Validation gates completos!")
        
    except Exception as e:
        print(f"❌ Erro nos validation gates: {e}")

async def main():
    """Executa todos os exemplos"""
    
    print("🚀 **TURSO AGENT - EXEMPLOS DE USO**")
    print("="*50)
    print("📊 Baseado no PRP ID 6: Agente Especialista Turso")
    print("🎯 Demonstrando todas as funcionalidades principais")
    print("="*50)
    
    exemplos = [
        exemplo_configuracao_basica,
        exemplo_operacoes_database,
        exemplo_integracao_mcp,
        exemplo_chat_especialista,
        exemplo_analise_performance,
        exemplo_security_audit,
        exemplo_validation_gates
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        try:
            await exemplo()
            
            if i < len(exemplos):
                input("\\n⏳ Pressione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\\n👋 Exemplos interrompidos pelo usuário")
            break
        except Exception as e:
            print(f"\\n❌ Erro no exemplo {i}: {e}")
            continue
    
    print("\\n🎉 **EXEMPLOS COMPLETOS!**")
    print("🎯 Turso Agent está pronto para uso!")

if __name__ == "__main__":
    asyncio.run(main())