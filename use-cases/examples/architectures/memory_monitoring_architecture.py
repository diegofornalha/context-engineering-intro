#!/usr/bin/env python3
"""
Arquitetura Correta: Turso (Memória) + Sentry (Monitoramento)
Demonstra as responsabilidades específicas de cada componente
"""

import sys
import os
from pathlib import Path
import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass
import json
import time

def show_responsibilities():
    """Mostra as responsabilidades específicas"""
    print("\n" + "="*80)
    print("🎯 ARQUITETURA COM RESPONSABILIDADES ESPECÍFICAS")
    print("="*80)
    print()
    print("🗄️ TURSO - SISTEMA DE MEMÓRIA")
    print("   • Armazenamento persistente de contexto")
    print("   • Base de conhecimento estruturada")
    print("   • Histórico de conversas")
    print("   • Dados de sessão")
    print("   • Cache inteligente")
    print()
    print("🔧 SENTRY - SISTEMA DE MONITORAMENTO")
    print("   • Error tracking em tempo real")
    print("   • Performance monitoring")
    print("   • Release health tracking")
    print("   • Session tracking")
    print("   • Observabilidade completa")
    print()
    print("🤖 AGENTES - LÓGICA DE PROCESSAMENTO")
    print("   • PRP Agent - Análise de requisitos")
    print("   • Turso Agent - Operações de memória")
    print("   • Sentry Agent - Monitoramento")
    print("   • CrewAI - Orquestração")
    print("="*80)
    print()

@dataclass
class TursoMemorySystem:
    """Turso - Sistema de Memória"""
    
    def __init__(self):
        self.memory_tables = {
            "conversations": [],
            "knowledge_base": [],
            "context_cache": {},
            "session_data": {},
            "structured_data": {}
        }
    
    def store_conversation(self, session_id: str, user_input: str, agent_response: str, metadata: Dict[str, Any]):
        """Armazena conversa na memória"""
        conversation = {
            "session_id": session_id,
            "timestamp": time.time(),
            "user_input": user_input,
            "agent_response": agent_response,
            "metadata": metadata
        }
        self.memory_tables["conversations"].append(conversation)
        print(f"💾 Turso: Conversa armazenada (session: {session_id})")
    
    def store_knowledge(self, topic: str, content: str, source: str = "agent"):
        """Armazena conhecimento na base"""
        knowledge = {
            "topic": topic,
            "content": content,
            "source": source,
            "timestamp": time.time()
        }
        self.memory_tables["knowledge_base"].append(knowledge)
        print(f"📚 Turso: Conhecimento armazenado (tópico: {topic})")
    
    def cache_context(self, key: str, context: Dict[str, Any]):
        """Cache de contexto para reutilização"""
        self.memory_tables["context_cache"][key] = {
            "context": context,
            "timestamp": time.time(),
            "ttl": 3600  # 1 hora
        }
        print(f"⚡ Turso: Contexto cacheado (key: {key})")
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Recupera histórico de conversas"""
        history = [
            conv for conv in self.memory_tables["conversations"]
            if conv["session_id"] == session_id
        ]
        return history[-limit:] if history else []
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Busca na base de conhecimento"""
        results = []
        for knowledge in self.memory_tables["knowledge_base"]:
            if query.lower() in knowledge["content"].lower():
                results.append(knowledge)
        return results
    
    def get_cached_context(self, key: str) -> Dict[str, Any]:
        """Recupera contexto cacheado"""
        cached = self.memory_tables["context_cache"].get(key)
        if cached and (time.time() - cached["timestamp"]) < cached["ttl"]:
            print(f"⚡ Turso: Contexto recuperado do cache (key: {key})")
            return cached["context"]
        return {}

@dataclass
class SentryMonitoringSystem:
    """Sentry - Sistema de Monitoramento"""
    
    def __init__(self):
        self.monitoring_data = {
            "errors": [],
            "performance": [],
            "sessions": [],
            "releases": [],
            "metrics": {}
        }
    
    def track_error(self, error_type: str, message: str, context: Dict[str, Any], severity: str = "error"):
        """Rastreia erro"""
        error_data = {
            "type": error_type,
            "message": message,
            "context": context,
            "severity": severity,
            "timestamp": time.time()
        }
        self.monitoring_data["errors"].append(error_data)
        print(f"🚨 Sentry: Erro rastreado ({error_type}: {message})")
    
    def track_performance(self, operation: str, duration: float, metadata: Dict[str, Any]):
        """Rastreia performance"""
        perf_data = {
            "operation": operation,
            "duration": duration,
            "metadata": metadata,
            "timestamp": time.time()
        }
        self.monitoring_data["performance"].append(perf_data)
        print(f"⚡ Sentry: Performance rastreada ({operation}: {duration:.3f}s)")
    
    def track_session(self, session_id: str, user_id: str, agent_name: str, action: str):
        """Rastreia sessão"""
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "agent_name": agent_name,
            "action": action,
            "timestamp": time.time()
        }
        self.monitoring_data["sessions"].append(session_data)
        print(f"👤 Sentry: Sessão rastreada ({agent_name}: {action})")
    
    def track_release_health(self, release: str, environment: str, health_status: str):
        """Rastreia saúde do release"""
        release_data = {
            "release": release,
            "environment": environment,
            "health_status": health_status,
            "timestamp": time.time()
        }
        self.monitoring_data["releases"].append(release_data)
        print(f"🏥 Sentry: Release health rastreado ({release}: {health_status})")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Resumo de erros"""
        errors = self.monitoring_data["errors"]
        return {
            "total_errors": len(errors),
            "error_types": list(set(e["type"] for e in errors)),
            "recent_errors": errors[-5:] if errors else []
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Resumo de performance"""
        perf = self.monitoring_data["performance"]
        if perf:
            avg_duration = sum(p["duration"] for p in perf) / len(perf)
            return {
                "total_operations": len(perf),
                "average_duration": avg_duration,
                "slowest_operation": max(perf, key=lambda x: x["duration"])
            }
        return {"total_operations": 0, "average_duration": 0}

class IntegratedMemoryMonitoringSystem:
    """Sistema Integrado: Memória + Monitoramento"""
    
    def __init__(self):
        self.memory = TursoMemorySystem()
        self.monitoring = SentryMonitoringSystem()
        self.session_counter = 0
    
    def process_agent_request(self, user_input: str, agent_name: str, user_id: str = "anonymous"):
        """Processa requisição com memória e monitoramento"""
        session_id = f"session_{self.session_counter}"
        self.session_counter += 1
        
        print(f"\n🎯 PROCESSANDO REQUISIÇÃO:")
        print(f"Session: {session_id}")
        print(f"Agent: {agent_name}")
        print(f"Input: {user_input[:50]}...")
        
        # 1. Monitoramento - Início da sessão
        self.monitoring.track_session(session_id, user_id, agent_name, "start")
        
        # 2. Memória - Recuperar contexto
        context = self.memory.get_cached_context(f"{agent_name}_{user_id}")
        if context:
            print(f"📚 Contexto recuperado: {len(context)} itens")
        
        # 3. Processamento (simulado)
        start_time = time.time()
        try:
            # Simular processamento
            response = self._simulate_agent_processing(user_input, agent_name)
            duration = time.time() - start_time
            
            # 4. Monitoramento - Performance
            self.monitoring.track_performance(
                f"{agent_name}_processing",
                duration,
                {"input_length": len(user_input), "response_length": len(response)}
            )
            
            # 5. Memória - Armazenar conversa
            self.memory.store_conversation(
                session_id,
                user_input,
                response,
                {"agent": agent_name, "duration": duration}
            )
            
            # 6. Memória - Armazenar conhecimento
            if "database" in user_input.lower():
                self.memory.store_knowledge(
                    "database_operations",
                    "Usuário solicitou operações de banco de dados",
                    "user_interaction"
                )
            
            # 7. Monitoramento - Fim da sessão
            self.monitoring.track_session(session_id, user_id, agent_name, "complete")
            
            return {
                "session_id": session_id,
                "response": response,
                "duration": duration,
                "context_used": bool(context)
            }
            
        except Exception as e:
            # Monitoramento - Erro
            self.monitoring.track_error(
                "agent_processing_error",
                str(e),
                {"agent": agent_name, "input": user_input},
                "error"
            )
            raise
    
    def _simulate_agent_processing(self, user_input: str, agent_name: str) -> str:
        """Simula processamento do agente"""
        if "turso" in user_input.lower():
            return "Operação Turso executada com sucesso"
        elif "sentry" in user_input.lower():
            return "Monitoramento Sentry ativo"
        else:
            return f"Resposta do {agent_name}: Processamento concluído"
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Resumo do sistema"""
        return {
            "memory": {
                "conversations": len(self.memory.memory_tables["conversations"]),
                "knowledge_items": len(self.memory.memory_tables["knowledge_base"]),
                "cached_contexts": len(self.memory.memory_tables["context_cache"])
            },
            "monitoring": {
                "errors": self.monitoring.get_error_summary(),
                "performance": self.monitoring.get_performance_summary(),
                "sessions": len(self.monitoring.monitoring_data["sessions"])
            }
        }

async def demonstrate_memory_monitoring():
    """Demonstra sistema de memória e monitoramento"""
    show_responsibilities()
    
    # Criar sistema integrado
    system = IntegratedMemoryMonitoringSystem()
    
    # Simular requisições
    requests = [
        ("Criar operações CRUD no Turso", "turso_agent"),
        ("Configurar monitoramento Sentry", "sentry_agent"),
        ("Analisar requisitos de sistema", "prp_agent"),
        ("Erro de teste para monitoramento", "test_agent")
    ]
    
    print("🔄 SIMULANDO REQUISIÇÕES:")
    print("-" * 50)
    
    for i, (user_input, agent_name) in enumerate(requests, 1):
        print(f"\n📝 Requisição {i}:")
        try:
            result = system.process_agent_request(user_input, agent_name)
            print(f"   ✅ Concluída em {result['duration']:.3f}s")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    # Mostrar resumo
    print("\n📊 RESUMO DO SISTEMA:")
    print("=" * 50)
    
    summary = system.get_system_summary()
    
    print("🗄️ TURSO (Memória):")
    print(f"   • Conversas armazenadas: {summary['memory']['conversations']}")
    print(f"   • Itens de conhecimento: {summary['memory']['knowledge_items']}")
    print(f"   • Contextos cacheados: {summary['memory']['cached_contexts']}")
    
    print("\n🔧 SENTRY (Monitoramento):")
    print(f"   • Total de erros: {summary['monitoring']['errors']['total_errors']}")
    print(f"   • Operações monitoradas: {summary['monitoring']['performance']['total_operations']}")
    print(f"   • Sessões rastreadas: {summary['monitoring']['sessions']}")
    
    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print("✅ Turso (Memória) - Funcionando")
    print("✅ Sentry (Monitoramento) - Funcionando")
    print("✅ Sistema Integrado - Funcionando")
    print("✅ Responsabilidades Específicas - Implementadas")

if __name__ == "__main__":
    asyncio.run(demonstrate_memory_monitoring()) 