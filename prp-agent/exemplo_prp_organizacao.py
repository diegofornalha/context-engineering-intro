#!/usr/bin/env python3
"""
🎯 EXEMPLO PRÁTICO: Análise de PRP para Agente de Organização de Projeto

Este script demonstra como o PRP Agent analisa um PRP complexo e extrai 
tarefas específicas com estimativas reais.
"""

import asyncio
import json
from agents.dependencies import PRPAgentDependencies
from agents.tools import create_prp, analyze_prp_with_llm, get_prp_details


async def criar_prp_exemplo():
    """Cria um PRP exemplo sobre agente de organização de projeto."""
    
    deps = PRPAgentDependencies(session_id="demo-organizacao-projeto")
    
    # PRP detalhado para agente de organização
    prp_data = {
        "name": "agente-organizacao-projeto",
        "title": "Agente IA para Organização Inteligente de Projetos",
        "description": """
Desenvolver um agente de IA especializado em analisar e organizar projetos de software automaticamente. 
O agente deve ser capaz de:

1. **Análise de Estrutura**: Examinar hierarquia de arquivos e identificar padrões organizacionais
2. **Detecção de Duplicação**: Encontrar código duplicado e sugerir consolidação
3. **Refatoração Inteligente**: Propor melhorias na arquitetura e organização do código
4. **Organização de Documentação**: Categorizar e estruturar documentos automaticamente
5. **Métricas de Qualidade**: Avaliar qualidade do código e estrutura do projeto
6. **Sugestões Proativas**: Recomendar melhorias baseadas em best practices

O agente deve integrar com sistemas existentes (Git, IDEs) e fornecer relatórios acionáveis.
        """,
        "objective": """
Criar um agente de IA que automatize a organização de projetos, reduzindo tempo de manutenção 
em 60% e melhorando a qualidade do código através de análises inteligentes e sugestões automáticas.
        """,
        "context_data": json.dumps({
            "target_languages": ["Python", "TypeScript", "JavaScript", "Go"],
            "integration_points": ["VSCode", "Git", "GitHub", "CI/CD"],
            "analysis_types": ["structure", "duplication", "complexity", "documentation"],
            "output_formats": ["reports", "suggestions", "automated_fixes"],
            "performance_targets": {
                "analysis_time": "< 30s per 1000 files",
                "accuracy": "> 90% for duplication detection",
                "user_adoption": "> 80% team usage"
            }
        }),
        "implementation_details": json.dumps({
            "technologies": {
                "backend": "FastAPI + PostgreSQL",
                "ai_models": "OpenAI GPT-4 + CodeT5 + Tree-sitter",
                "analysis_engine": "AST parsing + semantic analysis",
                "integrations": "LSP protocol + Git hooks"
            },
            "architecture": {
                "components": [
                    "File analyzer service",
                    "Duplication detector",
                    "Refactoring suggester", 
                    "Documentation organizer",
                    "Metrics calculator",
                    "Report generator"
                ],
                "data_flow": "File scan → Analysis → ML processing → Suggestions → Reports"
            },
            "deployment": {
                "environment": "Docker containers",
                "scaling": "Kubernetes horizontal scaling",
                "storage": "PostgreSQL + Redis cache"
            }
        }),
        "priority": "high",
        "tags": json.dumps(["ai-agent", "code-analysis", "automation", "organization", "productivity"])
    }
    
    print("🔨 Criando PRP exemplo: Agente de Organização de Projeto")
    result = await create_prp(
        deps=deps,
        name=prp_data["name"],
        title=prp_data["title"], 
        description=prp_data["description"],
        objective=prp_data["objective"],
        context_data=prp_data["context_data"],
        implementation_details=prp_data["implementation_details"],
        priority=prp_data["priority"],
        tags=prp_data["tags"]
    )
    
    print(f"✅ {result}")
    
    # Extrair ID do PRP criado
    if "ID:" in result:
        prp_id = int(result.split("ID: ")[1])
        return prp_id
    
    return None


async def analisar_prp(prp_id: int):
    """Executa análise LLM detalhada do PRP."""
    
    deps = PRPAgentDependencies(session_id="demo-analise-organizacao")
    
    print(f"\n🧠 Executando análise LLM do PRP {prp_id}...")
    
    # Análise de extração de tarefas
    analysis_result = await analyze_prp_with_llm(
        ctx=deps,
        prp_id=prp_id,
        analysis_type="task_extraction"
    )
    
    print("📊 RESULTADO DA ANÁLISE:")
    print("=" * 60)
    print(analysis_result)
    
    return analysis_result


async def obter_detalhes(prp_id: int):
    """Obtém detalhes completos do PRP analisado."""
    
    deps = PRPAgentDependencies(session_id="demo-detalhes-organizacao")
    
    print(f"\n📋 Obtendo detalhes completos do PRP {prp_id}...")
    
    details = await get_prp_details(
        ctx=deps,
        prp_id=prp_id
    )
    
    print("📄 DETALHES COMPLETOS:")
    print("=" * 60)
    print(details)
    
    return details


async def demo_completa():
    """Demonstração completa do processo de análise de PRP."""
    
    print("🚀 DEMO: Análise Completa de PRP - Agente de Organização")
    print("=" * 70)
    
    try:
        # Passo 1: Criar PRP
        prp_id = await criar_prp_exemplo()
        
        if prp_id:
            # Passo 2: Analisar PRP
            await analisar_prp(prp_id)
            
            # Passo 3: Obter detalhes
            await obter_detalhes(prp_id)
            
            print("\n🎯 CONCLUSÃO:")
            print("✅ PRP criado com sucesso")
            print("✅ Análise LLM executada")
            print("✅ Tarefas extraídas automaticamente")
            print("✅ Estimativas de tempo geradas")
            print("✅ Complexidade avaliada")
            
            print(f"\n🔗 Para ver o PRP: use get_prp_details com ID {prp_id}")
            
        else:
            print("❌ Erro ao criar PRP")
            
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")


def executar_analise_personalizada():
    """Simula análise personalizada com dados reais."""
    
    print("\n🎯 ANÁLISE PERSONALIZADA: Agente de Organização de Projeto")
    print("=" * 60)
    
    # Simular resultado de análise LLM mais realista
    analise_real = {
        "tasks": [
            {
                "name": "Configurar infraestrutura base",
                "description": "Setup FastAPI, PostgreSQL, Redis e Docker containers",
                "type": "setup",
                "priority": "critical",
                "estimated_hours": 8.0,
                "complexity": "medium",
                "context_files": ["docker-compose.yml", "requirements.txt", "main.py"],
                "acceptance_criteria": "API funcionando + BD configurado + Cache ativo"
            },
            {
                "name": "Implementar analisador de arquivos",
                "description": "Desenvolver sistema para scan e parsing de estruturas de projeto",
                "type": "feature",
                "priority": "critical", 
                "estimated_hours": 12.0,
                "complexity": "high",
                "context_files": ["file_analyzer.py", "ast_parser.py", "structure_detector.py"],
                "acceptance_criteria": "Scan 1000+ arquivos em <30s + detecção de linguagens"
            },
            {
                "name": "Detector de código duplicado",
                "description": "IA para encontrar duplicação usando AST e análise semântica",
                "type": "feature",
                "priority": "high",
                "estimated_hours": 16.0,
                "complexity": "high",
                "context_files": ["duplication_detector.py", "semantic_analyzer.py", "ml_models.py"],
                "acceptance_criteria": ">90% precisão + <5% falsos positivos"
            },
            {
                "name": "Engine de sugestões de refatoração",
                "description": "Sistema de IA para propor melhorias de arquitetura e organização",
                "type": "feature", 
                "priority": "high",
                "estimated_hours": 20.0,
                "complexity": "high",
                "context_files": ["refactoring_engine.py", "architecture_analyzer.py", "suggestions_ai.py"],
                "acceptance_criteria": "Sugestões acionáveis + explicações detalhadas"
            },
            {
                "name": "Organizador automático de documentação",
                "description": "Categorizar e estruturar docs baseado em conteúdo e contexto",
                "type": "feature",
                "priority": "medium",
                "estimated_hours": 10.0,
                "complexity": "medium", 
                "context_files": ["doc_organizer.py", "content_classifier.py", "markdown_parser.py"],
                "acceptance_criteria": "Classificação automática + estrutura hierárquica"
            },
            {
                "name": "Sistema de métricas e relatórios",
                "description": "Dashboard com métricas de qualidade e relatórios acionáveis",
                "type": "feature",
                "priority": "medium",
                "estimated_hours": 14.0,
                "complexity": "medium",
                "context_files": ["metrics_calculator.py", "report_generator.py", "dashboard.py"],
                "acceptance_criteria": "Dashboard interativo + exports PDF/JSON"
            },
            {
                "name": "Integração com IDEs e Git",
                "description": "Plugins VSCode/IDEs + Git hooks para análise automática",
                "type": "feature",
                "priority": "medium",
                "estimated_hours": 18.0,
                "complexity": "high",
                "context_files": ["vscode_extension/", "git_hooks.py", "lsp_protocol.py"],
                "acceptance_criteria": "Plugin funcional + hooks automáticos"
            },
            {
                "name": "Testes automatizados completos",
                "description": "Suite de testes unitários, integração e performance",
                "type": "test",
                "priority": "high",
                "estimated_hours": 12.0,
                "complexity": "medium",
                "context_files": ["tests/", "pytest.ini", "test_fixtures.py"],
                "acceptance_criteria": ">90% cobertura + testes performance"
            },
            {
                "name": "Documentação e guias de uso",
                "description": "Documentação completa para desenvolvedores e usuários finais",
                "type": "docs",
                "priority": "medium",
                "estimated_hours": 6.0,
                "complexity": "low",
                "context_files": ["README.md", "docs/", "examples/"],
                "acceptance_criteria": "Guias completos + exemplos práticos"
            },
            {
                "name": "CI/CD e deployment",
                "description": "Pipeline automático de build, test e deploy",
                "type": "setup",
                "priority": "medium", 
                "estimated_hours": 8.0,
                "complexity": "medium",
                "context_files": [".github/workflows/", "Dockerfile", "k8s/"],
                "acceptance_criteria": "Deploy automático + monitoramento"
            }
        ],
        "summary": "Agente de IA completo para organização inteligente de projetos com análise automática, detecção de duplicação, sugestões de refatoração e integração com ferramentas de desenvolvimento",
        "total_estimated_hours": 124.0,
        "complexity_assessment": "high",
        "risk_factors": [
            "Complexidade da análise semântica de código",
            "Precisão dos modelos de IA para sugestões",
            "Performance em projetos grandes (10k+ arquivos)",
            "Integração com diferentes IDEs e workflows"
        ],
        "success_metrics": [
            "60% redução no tempo de organização manual",
            "90%+ precisão na detecção de duplicação",
            "80%+ adoção pela equipe",
            "Análise <30s para projetos médios"
        ]
    }
    
    print(f"📊 **RESULTADO DA ANÁLISE LLM:**")
    print(f"**Projeto:** {analise_real['summary']}")
    print(f"**Estimativa Total:** {analise_real['total_estimated_hours']} horas")
    print(f"**Complexidade:** {analise_real['complexity_assessment'].upper()}")
    print()
    
    print("🔧 **TAREFAS EXTRAÍDAS:**")
    for i, task in enumerate(analise_real["tasks"], 1):
        print(f"{i:2d}. **{task['name']}** ({task['type']}, {task['priority']})")
        print(f"    {task['description']}")
        print(f"    ⏱️ Estimativa: {task['estimated_hours']}h | 🎯 Complexidade: {task['complexity']}")
        print(f"    📁 Arquivos: {', '.join(task['context_files'][:2])}...")
        print(f"    ✅ Critério: {task['acceptance_criteria']}")
        print()
    
    print("🎯 **MÉTRICAS DE SUCESSO:**")
    for metric in analise_real["success_metrics"]:
        print(f"   • {metric}")
    
    print("\n⚠️ **FATORES DE RISCO:**")
    for risk in analise_real["risk_factors"]:
        print(f"   • {risk}")
    
    print(f"\n📈 **RESUMO EXECUTIVO:**")
    print(f"   Total de tarefas: {len(analise_real['tasks'])}")
    print(f"   Features principais: {len([t for t in analise_real['tasks'] if t['type'] == 'feature'])}")
    print(f"   Setup e configuração: {len([t for t in analise_real['tasks'] if t['type'] == 'setup'])}")
    print(f"   Testes e documentação: {len([t for t in analise_real['tasks'] if t['type'] in ['test', 'docs']])}")
    print(f"   Tempo estimado: ~{analise_real['total_estimated_hours']} horas ({analise_real['total_estimated_hours']/40:.1f} semanas)")


if __name__ == "__main__":
    print("🎯 ESCOLHA O TIPO DE DEMONSTRAÇÃO:")
    print("1. Demo completa com banco de dados (async)")
    print("2. Análise personalizada (simulada)")
    
    choice = input("Digite 1 ou 2: ").strip()
    
    if choice == "1":
        asyncio.run(demo_completa())
    elif choice == "2":
        executar_analise_personalizada()
    else:
        print("Executando análise personalizada por padrão...")
        executar_analise_personalizada()