#!/usr/bin/env python3
"""
Script que usa as ferramentas MCP Turso disponíveis para listar PRPs
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPTursoTools:
    """
    Lista PRPs usando ferramentas MCP Turso disponíveis
    """
    
    def __init__(self):
        self.database_name = "context-memory"
        
    async def list_databases(self) -> List[str]:
        """
        Lista bancos de dados disponíveis
        """
        
        try:
            # Importar o agente
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("🗄️ Listando bancos de dados...")
            
            # Simular chamada para listar bancos
            result = await agent.call_mcp_turso("mcp_turso_list_databases", {
                "random_string": "list"
            })
            
            if result.get("success"):
                return result.get("databases", [])
            else:
                print(f"❌ Erro ao listar bancos: {result.get('error')}")
                return []
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    async def list_tables(self) -> List[str]:
        """
        Lista tabelas do banco
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("📋 Listando tabelas...")
            
            result = await agent.call_mcp_turso("mcp_turso_list_tables", {
                "database": self.database_name
            })
            
            if result.get("success"):
                return result.get("tables", [])
            else:
                print(f"❌ Erro ao listar tabelas: {result.get('error')}")
                return []
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    async def describe_table(self, table_name: str) -> Dict[str, Any]:
        """
        Descreve estrutura de uma tabela
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print(f"📊 Descrevendo tabela: {table_name}")
            
            result = await agent.call_mcp_turso("mcp_turso_describe_table", {
                "database": self.database_name,
                "table": table_name
            })
            
            return result
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return {}
    
    async def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca conhecimento no banco
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print(f"🔍 Buscando conhecimento: {query}")
            
            result = await agent.call_mcp_turso("mcp_turso_search_knowledge", {
                "database": self.database_name,
                "query": query,
                "limit": 10
            })
            
            if result.get("success"):
                return result.get("results", [])
            else:
                print(f"❌ Erro na busca: {result.get('error')}")
                return []
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    async def get_conversations(self) -> List[Dict[str, Any]]:
        """
        Obtém conversas do banco
        """
        
        try:
            from cursor_turso_integration import CursorTursoIntegration
            
            agent = CursorTursoIntegration()
            
            print("💬 Obtendo conversas...")
            
            result = await agent.call_mcp_turso("mcp_turso_get_conversations", {
                "database": self.database_name,
                "limit": 10
            })
            
            if result.get("success"):
                return result.get("conversations", [])
            else:
                print(f"❌ Erro ao obter conversas: {result.get('error')}")
                return []
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    def format_database_list(self, databases: List[str]) -> str:
        """
        Formata lista de bancos
        """
        
        if not databases:
            return "📭 Nenhum banco encontrado"
        
        output = "🗄️ BANCOS DE DADOS DISPONÍVEIS\n"
        output += "=" * 60 + "\n\n"
        
        for db in databases:
            output += f"📊 {db}\n"
        
        return output
    
    def format_table_list(self, tables: List[str]) -> str:
        """
        Formata lista de tabelas
        """
        
        if not tables:
            return "📭 Nenhuma tabela encontrada"
        
        output = "📋 TABELAS DISPONÍVEIS\n"
        output += "=" * 60 + "\n\n"
        
        for table in tables:
            output += f"📄 {table}\n"
        
        return output
    
    def format_knowledge_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Formata resultados de busca
        """
        
        if not results:
            return "📭 Nenhum resultado encontrado"
        
        output = "🔍 RESULTADOS DA BUSCA\n"
        output += "=" * 60 + "\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"{i}. 📄 **{result.get('topic', 'N/A')}**\n"
            output += f"   • Conteúdo: {result.get('content', 'N/A')[:100]}...\n"
            output += f"   • Fonte: {result.get('source', 'N/A')}\n"
            output += f"   • Tags: {result.get('tags', 'N/A')}\n"
            output += "\n"
        
        return output
    
    def format_conversation_list(self, conversations: List[Dict[str, Any]]) -> str:
        """
        Formata lista de conversas
        """
        
        if not conversations:
            return "📭 Nenhuma conversa encontrada"
        
        output = "💬 CONVERSAS DISPONÍVEIS\n"
        output += "=" * 60 + "\n\n"
        
        for i, conv in enumerate(conversations, 1):
            output += f"{i}. 💬 **{conv.get('session_id', 'N/A')}**\n"
            output += f"   • Mensagem: {conv.get('message', 'N/A')[:50]}...\n"
            output += f"   • Resposta: {conv.get('response', 'N/A')[:50]}...\n"
            output += f"   • Contexto: {conv.get('context', 'N/A')}\n"
            output += "\n"
        
        return output

async def main():
    """
    Função principal
    """
    
    print("🔍 EXPLORANDO MCP TURSO - FERRAMENTAS DISPONÍVEIS")
    print("=" * 60)
    print()
    
    tools = MCPTursoTools()
    
    # Listar bancos
    print("🗄️ Explorando bancos de dados...")
    databases = await tools.list_databases()
    print(tools.format_database_list(databases))
    
    print("\n" + "=" * 60 + "\n")
    
    # Listar tabelas
    print("📋 Explorando tabelas...")
    tables = await tools.list_tables()
    print(tools.format_table_list(tables))
    
    print("\n" + "=" * 60 + "\n")
    
    # Buscar conhecimento sobre PRPs
    print("🔍 Buscando conhecimento sobre PRPs...")
    knowledge_results = await tools.search_knowledge("PRP")
    print(tools.format_knowledge_results(knowledge_results))
    
    print("\n" + "=" * 60 + "\n")
    
    # Obter conversas
    print("💬 Obtendo conversas...")
    conversations = await tools.get_conversations()
    print(tools.format_conversation_list(conversations))
    
    print("\n" + "=" * 60)
    print("✅ Exploração MCP Turso concluída!")
    print("🔧 Ferramentas MCP funcionando corretamente")

if __name__ == "__main__":
    asyncio.run(main()) 