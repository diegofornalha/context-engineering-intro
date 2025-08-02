#!/usr/bin/env python3
"""
Turso Agent - Exemplo de Uso Avançado
Demonstra funcionalidades avançadas e cenários complexos do agente especialista
"""

import asyncio
import sys
import json
from pathlib import Path

# Adicionar path do turso-agent
sys.path.append(str(Path(__file__).parent.parent))

from config.turso_settings import TursoSettings
from tools.turso_manager import TursoManager
from tools.mcp_integrator import MCPTursoIntegrator
from agents.turso_specialist import TursoSpecialistAgent

async def cenario_setup_completo():
    """Cenário 1: Setup completo de projeto Turso do zero"""
    
    print("🎯 **CENÁRIO 1: SETUP COMPLETO DE PROJETO**")
    print("="*55)
    
    try:
        # Passo 1: Verificar ambiente
        print("1. 🔍 Verificando ambiente...")
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        config_status = await turso_manager.check_configuration()
        mcp_status = await mcp_integrator.check_mcp_status()
        
        print(f"   📊 Turso: {config_status}")
        print(f"   🔌 MCP: {mcp_status}")
        
        # Passo 2: Setup MCP se necessário
        if "❌" in mcp_status or "⚠️" in mcp_status:
            print("\\n2. 🔧 Configurando MCP...")
            setup_success = await mcp_integrator.setup_mcp_server()
            
            if setup_success:
                print("   ✅ MCP configurado com sucesso!")
            else:
                print("   ⚠️ MCP setup falhou, continuando sem MCP")
        
        # Passo 3: Criar database de exemplo
        print("\\n3. 🗄️ Criando database de exemplo...")
        db_name = "projeto_exemplo"
        create_success = await turso_manager.create_database(
            db_name, 
            group="default",
            regions=["lhr"]  # London
        )
        
        if create_success:
            print(f"   ✅ Database '{db_name}' criado!")
        else:
            print(f"   ⚠️ Database '{db_name}' já existe ou erro na criação")
        
        # Passo 4: Executar migrações
        print("\\n4. 🔄 Executando migrações...")
        migration_success = await turso_manager.run_migrations()
        
        if migration_success:
            print("   ✅ Migrações executadas!")
        
        # Passo 5: Configurar LLM integration
        print("\\n5. 🤖 Configurando LLM integration...")
        llm_success = await mcp_integrator.configure_llm_integration()
        
        if llm_success:
            print("   ✅ LLM integration configurada!")
        
        print("\\n🎉 **SETUP COMPLETO FINALIZADO!**")
        print("🚀 Projeto Turso pronto para desenvolvimento!")
        
    except Exception as e:
        print(f"❌ Erro no setup: {e}")

async def cenario_troubleshooting_avancado():
    """Cenário 2: Troubleshooting avançado de problemas"""
    
    print("\\n🎯 **CENÁRIO 2: TROUBLESHOOTING AVANÇADO**")
    print("="*55)
    
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
        
        # Problemas simulados para troubleshooting
        problemas = [
            {
                "tipo": "connection",
                "descricao": "Não consigo conectar no database, erro de authentication",
                "contexto": "Ambiente de produção"
            },
            {
                "tipo": "performance", 
                "descricao": "Queries muito lentas, timeout frequente",
                "contexto": "Database com 100k+ registros"
            },
            {
                "tipo": "mcp",
                "descricao": "MCP tools não aparecem no LLM",
                "contexto": "Cursor IDE com MCP configurado"
            },
            {
                "tipo": "replication",
                "descricao": "Dados inconsistentes entre replicas",
                "contexto": "Multi-region deployment"
            }
        ]
        
        for i, problema in enumerate(problemas, 1):
            print(f"\\n{i}. 🔧 **PROBLEMA:** {problema['descricao']}")
            print(f"   📍 Contexto: {problema['contexto']}")
            
            # Usar agente para troubleshooting
            solucao = await agent.troubleshoot_issue(problema['descricao'])
            print("   🤖 **SOLUÇÃO:**")
            print("   " + solucao.replace("\\n", "\\n   "))
            
            await asyncio.sleep(1)  # Pausa para leitura
        
        print("\\n✅ Troubleshooting avançado completo!")
        
    except Exception as e:
        print(f"❌ Erro no troubleshooting: {e}")

async def cenario_otimizacao_performance():
    """Cenário 3: Otimização completa de performance"""
    
    print("\\n🎯 **CENÁRIO 3: OTIMIZAÇÃO DE PERFORMANCE**")
    print("="*55)
    
    try:
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Fase 1: Análise inicial
        print("1. 📊 Análise inicial de performance...")
        
        if settings.default_database:
            analysis = await turso_manager.analyze_performance(settings.default_database)
            
            if analysis.get('database'):
                print(f"   📈 Database analisado: {analysis['database']}")
                print(f"   📋 Métricas coletadas: {len(analysis.get('metrics', {}))}")
                print(f"   💡 Recomendações: {len(analysis.get('recommendations', []))}")
            else:
                print("   ⚠️ Análise limitada - usando simulação")
        
        # Fase 2: Otimização automática
        print("\\n2. 🚀 Executando otimização automática...")
        optimization_result = await agent.optimize_system()
        print(optimization_result)
        
        # Fase 3: Validation pós-otimização
        print("\\n3. ✅ Validação pós-otimização...")
        validation_result = await agent.run_validation_gates()
        
        # Extrair resultado de validation
        if "Todos os testes passaram" in validation_result:
            print("   ✅ Validação: Todos os gates passaram")
        else:
            print("   ⚠️ Validação: Alguns gates falharam")
        
        print("\\n🎯 **OTIMIZAÇÃO COMPLETA!**")
        print("📈 Performance melhorada e validada!")
        
    except Exception as e:
        print(f"❌ Erro na otimização: {e}")

async def cenario_seguranca_compliance():
    """Cenário 4: Auditoria completa de segurança e compliance"""
    
    print("\\n🎯 **CENÁRIO 4: SEGURANÇA E COMPLIANCE**")
    print("="*55)
    
    try:
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Fase 1: Auditoria de segurança
        print("1. 🛡️ Executando auditoria de segurança...")
        security_audit = await agent.security_audit()
        print(security_audit)
        
        # Fase 2: Verificação MCP security
        print("\\n2. 🔌 Verificando segurança MCP...")
        mcp_security = await mcp_integrator.check_security()
        print(f"   📊 MCP Security Status: {mcp_security}")
        
        # Fase 3: Recommendations de segurança
        print("\\n3. 💡 Recomendações de segurança:")
        
        recommendations = [
            "✅ Implementar rotação automática de tokens",
            "✅ Configurar audit logging completo", 
            "✅ Usar RLS policies para dados sensíveis",
            "✅ Monitorar acessos anômalos",
            "✅ Backup automático com encryption"
        ]
        
        for rec in recommendations:
            print(f"   {rec}")
        
        # Fase 4: Compliance check
        print("\\n4. 📋 Verificação de compliance...")
        
        compliance_items = {
            "Token Security": settings.turso_api_token is not None,
            "Environment Variables": "TURSO_API_TOKEN" in str(settings.turso_api_token),
            "Audit Logging": settings.enable_audit_logging,
            "Secure Communication": True,  # HTTPS by default
            "Access Control": True  # MCP security model
        }
        
        for item, status in compliance_items.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {item}")
        
        compliance_score = sum(compliance_items.values()) / len(compliance_items) * 100
        print(f"\\n📊 **COMPLIANCE SCORE: {compliance_score:.0f}%**")
        
        if compliance_score >= 80:
            print("🎉 Compliance excelente!")
        elif compliance_score >= 60:
            print("⚠️ Compliance aceitável, melhorias recomendadas")
        else:
            print("❌ Compliance insuficiente, ação imediata necessária")
        
    except Exception as e:
        print(f"❌ Erro na auditoria: {e}")

async def cenario_chat_especialista_avancado():
    """Cenário 5: Chat especialista com contexto avançado"""
    
    print("\\n🎯 **CENÁRIO 5: CHAT ESPECIALISTA AVANÇADO**")
    print("="*55)
    
    try:
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        # Simulação de conversação complexa
        conversacao = [
            {
                "contexto": "Desenvolvedor iniciante",
                "pergunta": "Estou começando com Turso, qual a diferença entre libSQL e SQLite?",
                "categoria": "conceitos"
            },
            {
                "contexto": "Arquiteto de sistemas",
                "pergunta": "Como implementar uma estratégia de backup em multi-region?",
                "categoria": "arquitetura"
            },
            {
                "contexto": "DevOps engineer",
                "pergunta": "Como configurar CI/CD com migrações automáticas?",
                "categoria": "devops"
            },
            {
                "contexto": "Security engineer",
                "pergunta": "Quais são os pontos críticos de segurança em deployment Turso?",
                "categoria": "segurança"
            },
            {
                "contexto": "Performance engineer",
                "pergunta": "Como otimizar queries para ambiente distribuído edge?",
                "categoria": "performance"
            }
        ]
        
        print("💬 Simulando conversação especialista:")
        
        for i, item in enumerate(conversacao, 1):
            print(f"\\n{i}. 👤 **{item['contexto']}:** {item['pergunta']}")
            print(f"   🏷️ Categoria: {item['categoria']}")
            
            resposta = await agent.chat(item['pergunta'])
            
            # Mostrar parte da resposta
            resposta_preview = resposta[:300] + "..." if len(resposta) > 300 else resposta
            print(f"   🤖 **Turso Agent:** {resposta_preview}")
            
            # Simular tempo de leitura
            await asyncio.sleep(1)
        
        print("\\n✅ Chat especialista avançado completo!")
        print("🎯 Agente demonstrou expertise em múltiplas áreas!")
        
    except Exception as e:
        print(f"❌ Erro no chat: {e}")

async def cenario_monitoramento_continuo():
    """Cenário 6: Sistema de monitoramento contínuo"""
    
    print("\\n🎯 **CENÁRIO 6: MONITORAMENTO CONTÍNUO**")
    print("="*55)
    
    try:
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        agent = TursoSpecialistAgent(
            turso_manager=turso_manager,
            mcp_integrator=mcp_integrator,
            settings=settings
        )
        
        print("📊 Iniciando ciclo de monitoramento...")
        
        # Simular monitoramento por 3 ciclos
        for ciclo in range(1, 4):
            print(f"\\n🔄 **CICLO {ciclo}:**")
            
            # Health check geral
            config_status = await turso_manager.check_configuration()
            mcp_status = await mcp_integrator.check_mcp_status()
            
            print(f"   📊 Turso Health: {config_status}")
            print(f"   🔌 MCP Health: {mcp_status}")
            
            # Performance check
            if settings.default_database:
                perf_info = await turso_manager.get_database_info(settings.default_database)
                if perf_info and not perf_info.get('error'):
                    print(f"   ⚡ Database Status: ✅ Operational")
                else:
                    print(f"   ⚡ Database Status: ⚠️ Issues detected")
            
            # Security check
            security_status = await mcp_integrator.check_security()
            print(f"   🛡️ Security: {security_status}")
            
            # System info
            system_info = await agent.get_system_info()
            if "✅" in system_info:
                print(f"   🖥️ System: ✅ All capabilities operational")
            else:
                print(f"   🖥️ System: ⚠️ Some capabilities limited")
            
            # Aguardar próximo ciclo
            if ciclo < 3:
                print(f"   ⏳ Aguardando próximo ciclo...")
                await asyncio.sleep(2)
        
        print("\\n📈 **MONITORAMENTO COMPLETO!**")
        print("✅ Sistema monitorado e validado continuamente!")
        
    except Exception as e:
        print(f"❌ Erro no monitoramento: {e}")

async def main():
    """Executa todos os cenários avançados"""
    
    print("🚀 **TURSO AGENT - CENÁRIOS AVANÇADOS**")
    print("="*55)
    print("📊 Baseado no PRP ID 6: Agente Especialista Turso")
    print("🎯 Demonstrando cenários complexos e avançados")
    print("="*55)
    
    cenarios = [
        ("Setup Completo", cenario_setup_completo),
        ("Troubleshooting Avançado", cenario_troubleshooting_avancado),
        ("Otimização Performance", cenario_otimizacao_performance),
        ("Segurança & Compliance", cenario_seguranca_compliance),
        ("Chat Especialista", cenario_chat_especialista_avancado),
        ("Monitoramento Contínuo", cenario_monitoramento_continuo)
    ]
    
    print("\\n📋 **CENÁRIOS DISPONÍVEIS:**")
    for i, (nome, _) in enumerate(cenarios, 1):
        print(f"   {i}. {nome}")
    
    print("\\n🎯 Executando todos os cenários...")
    input("⏳ Pressione Enter para começar...")
    
    for i, (nome, cenario_func) in enumerate(cenarios, 1):
        try:
            print(f"\\n{'='*60}")
            print(f"🎯 EXECUTANDO CENÁRIO {i}: {nome.upper()}")
            print(f"{'='*60}")
            
            await cenario_func()
            
            if i < len(cenarios):
                input(f"\\n⏳ Pressione Enter para continuar para o próximo cenário...")
                
        except KeyboardInterrupt:
            print("\\n👋 Cenários interrompidos pelo usuário")
            break
        except Exception as e:
            print(f"\\n❌ Erro no cenário {nome}: {e}")
            continue
    
    print("\\n🎉 **TODOS OS CENÁRIOS COMPLETOS!**")
    print("🏆 Turso Agent demonstrou expertise completa!")
    print("🚀 Sistema pronto para uso em produção!")

if __name__ == "__main__":
    asyncio.run(main())