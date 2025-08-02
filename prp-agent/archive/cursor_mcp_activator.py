#!/usr/bin/env python3
"""
🔌 Ativador MCP Turso REAL para Cursor Agent.

Este arquivo detecta se as ferramentas MCP Turso estão disponíveis
no Cursor Agent e ativa automaticamente a persistência REAL.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPTursoActivator:
    """
    Detector e ativador automático das ferramentas MCP Turso no Cursor Agent.
    """
    
    def __init__(self):
        self.mcp_available = False
        self.available_tools = []
        self.database_name = "context-memory"
    
    async def detect_mcp_tools(self) -> bool:
        """
        Detecta se as ferramentas MCP Turso estão disponíveis no Cursor Agent.
        """
        
        try:
            # Tentar importar ferramentas MCP (disponíveis apenas no Cursor Agent)
            global mcp_turso_execute_query, mcp_turso_execute_read_only_query
            global mcp_turso_add_conversation, mcp_turso_list_tables
            
            # Estas importações só funcionarão no ambiente Cursor Agent
            try:
                from cursor_mcp_tools import (
                    mcp_turso_execute_query,
                    mcp_turso_execute_read_only_query, 
                    mcp_turso_add_conversation,
                    mcp_turso_list_tables
                )
                
                self.mcp_available = True
                self.available_tools = [
                    "mcp_turso_execute_query",
                    "mcp_turso_execute_read_only_query",
                    "mcp_turso_add_conversation", 
                    "mcp_turso_list_tables"
                ]
                
                print("🔌 **MCP Turso DETECTADO no Cursor Agent!**")
                print(f"✅ Ferramentas disponíveis: {len(self.available_tools)}")
                return True
                
            except ImportError:
                # MCP não disponível - usar simulação
                self.mcp_available = False
                print("⚠️ **MCP Turso não detectado - usando simulação**")
                print("💡 **Para ativar MCP real: Execute no Cursor Agent com servidor MCP ativo**")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao detectar MCP: {e}")
            return False
    
    async def execute_query_real(self, query: str, params: list = None) -> Dict[str, Any]:
        """
        Executa query REAL no Turso via MCP (se disponível).
        """
        
        if self.mcp_available:
            try:
                # Chamada MCP REAL
                result = await mcp_turso_execute_query({
                    "query": query,
                    "params": params or [],
                    "database": self.database_name
                })
                
                print(f"💾 **MCP REAL executado:** {query[:50]}...")
                return result
                
            except Exception as e:
                logger.error(f"Erro MCP real: {e}")
                return {"success": False, "error": str(e)}
        else:
            # Simulação para desenvolvimento
            print(f"🔧 **MCP Simulado:** {query[:50]}...")
            return {
                "success": True,
                "lastInsertId": hash(query) % 1000,
                "rowsAffected": 1,
                "simulated": True
            }
    
    async def execute_read_query_real(self, query: str, params: list = None) -> Dict[str, Any]:
        """
        Executa query de leitura REAL no Turso via MCP (se disponível).
        """
        
        if self.mcp_available:
            try:
                # Chamada MCP REAL
                result = await mcp_turso_execute_read_only_query({
                    "query": query,
                    "params": params or [],
                    "database": self.database_name
                })
                
                print(f"🔍 **MCP REAL consultado:** {query[:50]}...")
                return result
                
            except Exception as e:
                logger.error(f"Erro MCP real: {e}")
                return {"success": False, "error": str(e)}
        else:
            # Simulação para desenvolvimento
            print(f"🔧 **MCP Simulado:** {query[:50]}...")
            return {
                "success": True,
                "rows": [
                    {
                        "id": 1,
                        "session_id": "cursor-agent-20250802",
                        "message": "Exemplo de dados simulados",
                        "timestamp": datetime.now().isoformat()
                    }
                ],
                "columns": ["id", "session_id", "message", "timestamp"],
                "simulated": True
            }
    
    async def add_conversation_real(self, session_id: str, message: str, response: str, context: str = None) -> Dict[str, Any]:
        """
        Adiciona conversa REAL via MCP (se disponível).
        """
        
        if self.mcp_available:
            try:
                # Chamada MCP REAL
                result = await mcp_turso_add_conversation({
                    "session_id": session_id,
                    "message": message,
                    "response": response,
                    "context": context or "",
                    "database": self.database_name
                })
                
                print(f"💬 **Conversa REAL adicionada:** {message[:30]}...")
                return result
                
            except Exception as e:
                logger.error(f"Erro MCP real: {e}")
                return {"success": False, "error": str(e)}
        else:
            # Simulação para desenvolvimento
            print(f"🔧 **Conversa Simulada:** {message[:30]}...")
            return {
                "success": True,
                "conversation_id": hash(message) % 1000,
                "simulated": True
            }
    
    async def test_connection_real(self) -> Dict[str, Any]:
        """
        Testa conexão REAL com o banco Turso via MCP.
        """
        
        if self.mcp_available:
            try:
                # Testar com query simples
                result = await mcp_turso_list_tables({
                    "database": self.database_name
                })
                
                if result.get("success"):
                    tables = result.get("tables", [])
                    print(f"🎯 **Conexão MCP REAL confirmada!**")
                    print(f"📋 Tabelas encontradas: {len(tables)}")
                    return {"connected": True, "tables": len(tables), "real": True}
                else:
                    print(f"❌ **Erro na conexão MCP:** {result.get('error')}")
                    return {"connected": False, "error": result.get("error"), "real": True}
                    
            except Exception as e:
                logger.error(f"Erro ao testar conexão: {e}")
                return {"connected": False, "error": str(e), "real": True}
        else:
            # Simulação
            print("🔧 **Conexão simulada - MCP não disponível**")
            return {"connected": True, "tables": 6, "real": False, "simulated": True}
    
    def get_status_report(self) -> str:
        """
        Retorna relatório de status da integração MCP.
        """
        
        if self.mcp_available:
            return f"""
🎯 **STATUS: MCP Turso REAL ATIVO**

✅ **Integração Real Funcionando:**
- MCP Turso conectado ao Cursor Agent
- Banco: {self.database_name}
- Ferramentas: {len(self.available_tools)} disponíveis
- Persistência: REAL no Turso

🌐 **Verificar dados em:**
app.turso.tech/diegofornalha/databases/{self.database_name}

🚀 **Benefícios Ativos:**
- Dados realmente persistidos
- Histórico permanente
- Sincronização em tempo real
- Base de conhecimento crescente
"""
        else:
            return f"""
⚠️ **STATUS: MCP Turso SIMULADO**

🔧 **Modo Desenvolvimento:**
- MCP Turso não detectado
- Banco: {self.database_name} (simulado)
- Funcionamento: Interface completa
- Persistência: Simulada localmente

🎯 **Para Ativar MCP Real:**
1. Execute no Cursor Agent
2. Certifique-se que servidor MCP está ativo
3. Verifique configuração .cursor/mcp.json

📚 **Funcionalidades Disponíveis:**
- Conversas naturais ✅
- Análise de código ✅
- Criação de PRPs ✅
- Interface completa ✅
"""

# Instância global
mcp_activator = MCPTursoActivator()

# Função de inicialização automática
async def initialize_mcp() -> Dict[str, Any]:
    """
    Inicializa e detecta automaticamente MCP Turso.
    Retorna status da detecção.
    """
    
    print("🔍 **Detectando MCP Turso no Cursor Agent...**")
    
    # Detectar ferramentas MCP
    mcp_detected = await mcp_activator.detect_mcp_tools()
    
    # Testar conexão
    connection_status = await mcp_activator.test_connection_real()
    
    # Gerar relatório
    status_report = mcp_activator.get_status_report()
    
    return {
        "mcp_detected": mcp_detected,
        "connection_status": connection_status,
        "status_report": status_report,
        "activator": mcp_activator
    }

# Funções de conveniência que se adaptam automaticamente
async def smart_execute_query(query: str, params: list = None) -> Dict[str, Any]:
    """Executa query adaptando-se automaticamente ao ambiente (real ou simulado)."""
    return await mcp_activator.execute_query_real(query, params)

async def smart_read_query(query: str, params: list = None) -> Dict[str, Any]:
    """Executa query de leitura adaptando-se automaticamente ao ambiente."""
    return await mcp_activator.execute_read_query_real(query, params)

async def smart_add_conversation(session_id: str, message: str, response: str, context: str = None) -> Dict[str, Any]:
    """Adiciona conversa adaptando-se automaticamente ao ambiente."""
    return await mcp_activator.add_conversation_real(session_id, message, response, context)

# Demonstração
if __name__ == "__main__":
    async def demo_activation():
        """Demonstração da detecção e ativação automática do MCP."""
        
        print("🚀 **DEMONSTRAÇÃO: Ativação Automática MCP Turso**\n")
        
        # Inicializar MCP
        status = await initialize_mcp()
        
        print("\n" + "="*60)
        print(status["status_report"])
        print("="*60)
        
        # Testar funcionalidades
        print("\n📋 **Testando Funcionalidades:**")
        
        # Teste 1: Query
        result = await smart_execute_query(
            "INSERT INTO conversations (session_id, message) VALUES (?, ?)",
            ["test-session", "Teste de ativação MCP"]
        )
        print(f"1️⃣ Execute Query: {'✅ REAL' if not result.get('simulated') else '🔧 Simulado'}")
        
        # Teste 2: Leitura
        result = await smart_read_query(
            "SELECT COUNT(*) as total FROM conversations"
        )
        print(f"2️⃣ Read Query: {'✅ REAL' if not result.get('simulated') else '🔧 Simulado'}")
        
        # Teste 3: Conversa
        result = await smart_add_conversation(
            "demo-session", 
            "Teste de conversa", 
            "Resposta automática"
        )
        print(f"3️⃣ Add Conversation: {'✅ REAL' if not result.get('simulated') else '🔧 Simulado'}")
        
        print(f"\n🎯 **Resultado:** {'MCP REAL ativo!' if status['mcp_detected'] else 'Simulação funcionando!'}")
        
        if not status['mcp_detected']:
            print("\n💡 **Para ativar MCP REAL:**")
            print("   1. Execute este código no Cursor Agent")
            print("   2. Certifique-se que servidor MCP Turso está rodando")
            print("   3. Verifique .cursor/mcp.json está configurado")
    
    asyncio.run(demo_activation())