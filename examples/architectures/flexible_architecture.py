#!/usr/bin/env python3
"""
Arquitetura Flexível: Core Obrigatório + Componentes Opcionais
Demonstra como o sistema funciona com diferentes configurações
"""

import sys
import os
from pathlib import Path
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import time

def show_flexible_architecture():
    """Mostra a arquitetura flexível"""
    print("\n" + "="*80)
    print("🎯 ARQUITETURA FLEXÍVEL - CORE + OPCIONAL")
    print("="*80)
    print()
    print("✅ CORE OBRIGATÓRIO:")
    print("   • PRP Agent - Metodologia principal")
    print("   • Turso - Memória (quando necessário)")
    print("   • Sentry - Monitoramento (quando necessário)")
    print()
    print("🔄 COMPONENTES OPCIONAIS:")
    print("   • CrewAI - Framework de orquestração (opcional)")
    print("   • A2A - Interoperabilidade entre agentes (opcional)")
    print()
    print("📋 PRP - METODOLOGIA (Sempre presente)")
    print("   • Análise de requisitos")
    print("   • Engenharia de contexto")
    print("   • Prompts estruturados")
    print("="*80)
    print()

@dataclass
class CoreSystem:
    """Sistema Core - Sempre presente"""
    
    def __init__(self):
        self.prp_agent_active = True
        self.turso_available = False
        self.sentry_available = False
        self.crewai_available = False
        self.a2a_available = False
    
    def configure_turso(self, enable: bool = True):
        """Configura Turso (opcional)"""
        self.turso_available = enable
        if enable:
            print("🗄️ Turso: Sistema de memória ativado")
        else:
            print("🗄️ Turso: Sistema de memória desativado")
    
    def configure_sentry(self, enable: bool = True):
        """Configura Sentry (opcional)"""
        self.sentry_available = enable
        if enable:
            print("🔧 Sentry: Sistema de monitoramento ativado")
        else:
            print("🔧 Sentry: Sistema de monitoramento desativado")
    
    def configure_crewai(self, enable: bool = False):
        """Configura CrewAI (opcional)"""
        self.crewai_available = enable
        if enable:
            print("🤖 CrewAI: Framework de orquestração ativado")
        else:
            print("🤖 CrewAI: Framework de orquestração desativado")
    
    def configure_a2a(self, enable: bool = False):
        """Configura A2A (opcional)"""
        self.a2a_available = enable
        if enable:
            print("🔗 A2A: Interoperabilidade entre agentes ativada")
        else:
            print("🔗 A2A: Interoperabilidade entre agentes desativada")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Status do sistema"""
        return {
            "core": {
                "prp_agent": "✅ Ativo (Sempre)",
                "turso": "✅ Ativo" if self.turso_available else "❌ Desativado",
                "sentry": "✅ Ativo" if self.sentry_available else "❌ Desativado"
            },
            "optional": {
                "crewai": "✅ Ativo" if self.crewai_available else "❌ Desativado",
                "a2a": "✅ Ativo" if self.a2a_available else "❌ Desativado"
            }
        }

class PRPAgent:
    """PRP Agent - Sempre presente"""
    
    def __init__(self):
        self.name = "PRP Agent"
        self.methodology = "Product Requirement Prompts"
    
    def analyze_requirements(self, requirements: str) -> str:
        """Analisa requisitos (sempre disponível)"""
        return f"📋 PRP Agent: Análise de requisitos concluída\n{requirements[:100]}..."
    
    def create_context(self, context_data: str) -> str:
        """Cria contexto estruturado"""
        return f"📋 PRP Agent: Contexto criado\n{context_data[:100]}..."
    
    def generate_tasks(self, analysis: str) -> List[str]:
        """Gera tarefas baseadas na análise"""
        return [
            "Tarefa 1: Implementar funcionalidade core",
            "Tarefa 2: Configurar dependências",
            "Tarefa 3: Testar integração"
        ]

class TursoMemory:
    """Turso - Sistema de Memória (Opcional)"""
    
    def __init__(self):
        self.active = False
        self.memory_data = {}
    
    def activate(self):
        """Ativa o sistema de memória"""
        self.active = True
        print("🗄️ Turso: Sistema de memória ativado")
    
    def deactivate(self):
        """Desativa o sistema de memória"""
        self.active = False
        print("🗄️ Turso: Sistema de memória desativado")
    
    def store_data(self, key: str, data: Any) -> bool:
        """Armazena dados (se ativo)"""
        if self.active:
            self.memory_data[key] = data
            print(f"💾 Turso: Dados armazenados ({key})")
            return True
        else:
            print(f"💾 Turso: Sistema desativado, dados não armazenados")
            return False
    
    def retrieve_data(self, key: str) -> Any:
        """Recupera dados (se ativo)"""
        if self.active:
            return self.memory_data.get(key)
        else:
            return None

class SentryMonitoring:
    """Sentry - Sistema de Monitoramento (Opcional)"""
    
    def __init__(self):
        self.active = False
        self.monitoring_data = []
    
    def activate(self):
        """Ativa o sistema de monitoramento"""
        self.active = True
        print("🔧 Sentry: Sistema de monitoramento ativado")
    
    def deactivate(self):
        """Desativa o sistema de monitoramento"""
        self.active = False
        print("🔧 Sentry: Sistema de monitoramento desativado")
    
    def track_event(self, event_type: str, data: Dict[str, Any]) -> bool:
        """Rastreia evento (se ativo)"""
        if self.active:
            event = {
                "type": event_type,
                "data": data,
                "timestamp": time.time()
            }
            self.monitoring_data.append(event)
            print(f"🔧 Sentry: Evento rastreado ({event_type})")
            return True
        else:
            print(f"🔧 Sentry: Sistema desativado, evento não rastreado")
            return False

class FlexibleSystem:
    """Sistema Flexível com Componentes Opcionais"""
    
    def __init__(self):
        self.core = CoreSystem()
        self.prp_agent = PRPAgent()
        self.turso = TursoMemory()
        self.sentry = SentryMonitoring()
    
    def configure_system(self, 
                        turso_enabled: bool = False,
                        sentry_enabled: bool = False,
                        crewai_enabled: bool = False,
                        a2a_enabled: bool = False):
        """Configura o sistema com componentes opcionais"""
        print("\n🔧 CONFIGURANDO SISTEMA:")
        print("-" * 40)
        
        # Configurar componentes opcionais
        self.core.configure_turso(turso_enabled)
        self.core.configure_sentry(sentry_enabled)
        self.core.configure_crewai(crewai_enabled)
        self.core.configure_a2a(a2a_enabled)
        
        # Ativar/desativar sistemas
        if turso_enabled:
            self.turso.activate()
        else:
            self.turso.deactivate()
        
        if sentry_enabled:
            self.sentry.activate()
        else:
            self.sentry.deactivate()
        
        print("-" * 40)
        print("✅ Configuração concluída!")
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """Processa requisição com componentes disponíveis"""
        print(f"\n🎯 PROCESSANDO REQUISIÇÃO:")
        print(f"Request: {request[:50]}...")
        
        # 1. PRP Agent (sempre disponível)
        analysis = self.prp_agent.analyze_requirements(request)
        context = self.prp_agent.create_context(request)
        tasks = self.prp_agent.generate_tasks(analysis)
        
        result = {
            "analysis": analysis,
            "context": context,
            "tasks": tasks,
            "components_used": ["prp_agent"]
        }
        
        # 2. Turso (se ativo)
        if self.turso.active:
            self.turso.store_data("last_request", request)
            self.turso.store_data("analysis", analysis)
            result["components_used"].append("turso")
            result["memory_stored"] = True
        
        # 3. Sentry (se ativo)
        if self.sentry.active:
            self.sentry.track_event("request_processed", {
                "request": request,
                "analysis_length": len(analysis),
                "tasks_count": len(tasks)
            })
            result["components_used"].append("sentry")
            result["monitoring_active"] = True
        
        return result
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Resumo do sistema"""
        return {
            "core_status": self.core.get_system_status(),
            "prp_agent": "✅ Sempre ativo",
            "turso_status": "✅ Ativo" if self.turso.active else "❌ Desativado",
            "sentry_status": "✅ Ativo" if self.sentry.active else "❌ Desativado",
            "total_components": len(self.core.get_system_status()["core"]) + 
                              len(self.core.get_system_status()["optional"])
        }

async def demonstrate_flexible_architecture():
    """Demonstra arquitetura flexível"""
    show_flexible_architecture()
    
    # Criar sistema flexível
    system = FlexibleSystem()
    
    # Cenário 1: Sistema mínimo (apenas PRP Agent)
    print("📋 CENÁRIO 1: SISTEMA MÍNIMO")
    print("=" * 50)
    system.configure_system(
        turso_enabled=False,
        sentry_enabled=False,
        crewai_enabled=False,
        a2a_enabled=False
    )
    
    result1 = system.process_request("Criar um sistema de login simples")
    print(f"✅ Resultado: {len(result1['tasks'])} tarefas geradas")
    print(f"📊 Componentes usados: {result1['components_used']}")
    
    # Cenário 2: Com memória (PRP + Turso)
    print("\n📋 CENÁRIO 2: COM MEMÓRIA")
    print("=" * 50)
    system.configure_system(
        turso_enabled=True,
        sentry_enabled=False,
        crewai_enabled=False,
        a2a_enabled=False
    )
    
    result2 = system.process_request("Adicionar autenticação OAuth")
    print(f"✅ Resultado: {len(result2['tasks'])} tarefas geradas")
    print(f"📊 Componentes usados: {result2['components_used']}")
    print(f"💾 Memória: {result2.get('memory_stored', False)}")
    
    # Cenário 3: Com monitoramento (PRP + Sentry)
    print("\n📋 CENÁRIO 3: COM MONITORAMENTO")
    print("=" * 50)
    system.configure_system(
        turso_enabled=False,
        sentry_enabled=True,
        crewai_enabled=False,
        a2a_enabled=False
    )
    
    result3 = system.process_request("Implementar dashboard de usuários")
    print(f"✅ Resultado: {len(result3['tasks'])} tarefas geradas")
    print(f"📊 Componentes usados: {result3['components_used']}")
    print(f"🔧 Monitoramento: {result3.get('monitoring_active', False)}")
    
    # Cenário 4: Sistema completo (PRP + Turso + Sentry)
    print("\n📋 CENÁRIO 4: SISTEMA COMPLETO")
    print("=" * 50)
    system.configure_system(
        turso_enabled=True,
        sentry_enabled=True,
        crewai_enabled=True,
        a2a_enabled=True
    )
    
    result4 = system.process_request("Criar sistema completo de e-commerce")
    print(f"✅ Resultado: {len(result4['tasks'])} tarefas geradas")
    print(f"📊 Componentes usados: {result4['components_used']}")
    print(f"💾 Memória: {result4.get('memory_stored', False)}")
    print(f"🔧 Monitoramento: {result4.get('monitoring_active', False)}")
    
    # Resumo final
    print("\n📊 RESUMO FINAL:")
    print("=" * 50)
    summary = system.get_system_summary()
    
    print("✅ CORE OBRIGATÓRIO:")
    print(f"   • PRP Agent: {summary['prp_agent']}")
    print(f"   • Turso: {summary['turso_status']}")
    print(f"   • Sentry: {summary['sentry_status']}")
    
    print("\n🔄 COMPONENTES OPCIONAIS:")
    print(f"   • CrewAI: {summary['core_status']['optional']['crewai']}")
    print(f"   • A2A: {summary['core_status']['optional']['a2a']}")
    
    print(f"\n🎯 Total de componentes: {summary['total_components']}")
    
    print("\n🎉 ARQUITETURA FLEXÍVEL FUNCIONANDO!")
    print("=" * 80)
    print("✅ PRP Agent - Sempre presente")
    print("✅ Turso - Opcional (memória)")
    print("✅ Sentry - Opcional (monitoramento)")
    print("✅ CrewAI - Opcional (orquestração)")
    print("✅ A2A - Opcional (interoperabilidade)")

if __name__ == "__main__":
    asyncio.run(demonstrate_flexible_architecture()) 