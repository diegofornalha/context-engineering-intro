#!/usr/bin/env python3
"""
Integração do Agente PRP com MCP Turso

Este script demonstra como usar o MCP Turso para armazenar:
- PRPs criados pelo agente
- Análises LLM realizadas
- Tarefas extraídas
- Histórico de conversas
- Conhecimento gerado
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

# Simulação das ferramentas MCP Turso
class MCPTursoClient:
    """Cliente para interagir com MCP Turso."""
    
    def __init__(self, database: str = "context-memory"):
        self.database = database
    
    async def execute_query(self, query: str, params: List[Any] = None) -> Dict[str, Any]:
        """Executa query no banco de dados."""
        # Simulação - em produção, isso seria uma chamada real para MCP Turso
        print(f"🔧 MCP Turso: Executando query: {query}")
        if params:
            print(f"   Parâmetros: {params}")
        
        # Simular resultado
        return {
            "success": True,
            "lastInsertId": 1,
            "rowsAffected": 1,
            "rows": []
        }
    
    async def execute_read_only_query(self, query: str, params: List[Any] = None) -> Dict[str, Any]:
        """Executa query de leitura no banco de dados."""
        print(f"🔍 MCP Turso: Executando leitura: {query}")
        if params:
            print(f"   Parâmetros: {params}")
        
        # Simular resultado
        return {
            "success": True,
            "rows": [],
            "columns": []
        }


class PRPMCPIntegration:
    """Integração entre Agente PRP e MCP Turso."""
    
    def __init__(self):
        self.mcp_client = MCPTursoClient("context-memory")
    
    async def store_prp(self, prp_data: Dict[str, Any]) -> int:
        """Armazena um PRP no banco via MCP Turso."""
        
        query = """
            INSERT INTO prps (
                name, title, description, objective, context_data,
                implementation_details, validation_gates, status, priority, tags, search_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        search_text = f"{prp_data['title']} {prp_data['description']} {prp_data['objective']}".lower()
        
        params = [
            prp_data['name'],
            prp_data['title'],
            prp_data['description'],
            prp_data['objective'],
            json.dumps(prp_data.get('context_data', {})),
            json.dumps(prp_data.get('implementation_details', {})),
            json.dumps(prp_data.get('validation_gates', {})),
            prp_data.get('status', 'draft'),
            prp_data.get('priority', 'medium'),
            json.dumps(prp_data.get('tags', [])),
            search_text
        ]
        
        result = await self.mcp_client.execute_query(query, params)
        prp_id = result.get('lastInsertId', 1)
        
        print(f"✅ PRP '{prp_data['title']}' armazenado com ID: {prp_id}")
        return prp_id
    
    async def store_llm_analysis(self, prp_id: int, analysis_data: Dict[str, Any]) -> int:
        """Armazena análise LLM no banco via MCP Turso."""
        
        query = """
            INSERT INTO prp_llm_analysis (
                prp_id, analysis_type, input_content, output_content,
                parsed_data, model_used, tokens_used, processing_time_ms, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = [
            prp_id,
            analysis_data.get('analysis_type', 'task_extraction'),
            analysis_data.get('input_content', ''),
            analysis_data.get('output_content', ''),
            json.dumps(analysis_data.get('parsed_data', {})),
            analysis_data.get('model_used', 'gpt-4o'),
            analysis_data.get('tokens_used', 0),
            analysis_data.get('processing_time_ms', 0),
            analysis_data.get('confidence_score', 0.9)
        ]
        
        result = await self.mcp_client.execute_query(query, params)
        analysis_id = result.get('lastInsertId', 1)
        
        print(f"🧠 Análise LLM armazenada com ID: {analysis_id}")
        return analysis_id
    
    async def store_tasks(self, prp_id: int, tasks: List[Dict[str, Any]]) -> List[int]:
        """Armazena tarefas extraídas no banco via MCP Turso."""
        
        task_ids = []
        
        for task in tasks:
            query = """
                INSERT INTO prp_tasks (
                    prp_id, task_name, description, task_type, priority,
                    estimated_hours, complexity, context_files, acceptance_criteria
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = [
                prp_id,
                task.get('name', ''),
                task.get('description', ''),
                task.get('type', 'feature'),
                task.get('priority', 'medium'),
                task.get('estimated_hours', 0),
                task.get('complexity', 'medium'),
                json.dumps(task.get('context_files', [])),
                task.get('acceptance_criteria', '')
            ]
            
            result = await self.mcp_client.execute_query(query, params)
            task_id = result.get('lastInsertId', 1)
            task_ids.append(task_id)
            
            print(f"📋 Tarefa '{task.get('name', '')}' armazenada com ID: {task_id}")
        
        return task_ids
    
    async def store_conversation(self, session_id: str, message: str, response: str, 
                               context: str = None) -> int:
        """Armazena conversa no banco via MCP Turso."""
        
        query = """
            INSERT INTO conversations (
                session_id, message, response, context, metadata
            ) VALUES (?, ?, ?, ?, ?)
        """
        
        metadata = json.dumps({
            "agent_type": "prp_agent",
            "timestamp": datetime.now().isoformat(),
            "tools_used": []
        })
        
        params = [session_id, message, response, context, metadata]
        
        result = await self.mcp_client.execute_query(query, params)
        conversation_id = result.get('lastInsertId', 1)
        
        print(f"💬 Conversa armazenada com ID: {conversation_id}")
        return conversation_id
    
    async def store_knowledge(self, topic: str, content: str, source: str = "prp_agent",
                            tags: List[str] = None) -> int:
        """Armazena conhecimento no banco via MCP Turso."""
        
        query = """
            INSERT INTO knowledge_base (
                topic, content, source, tags
            ) VALUES (?, ?, ?, ?)
        """
        
        tags_json = json.dumps(tags or [])
        params = [topic, content, source, tags_json]
        
        result = await self.mcp_client.execute_query(query, params)
        knowledge_id = result.get('lastInsertId', 1)
        
        print(f"📚 Conhecimento '{topic}' armazenado com ID: {knowledge_id}")
        return knowledge_id
    
    async def search_prps(self, query: str = None, status: str = None, 
                         limit: int = 10) -> List[Dict[str, Any]]:
        """Busca PRPs no banco via MCP Turso."""
        
        sql = """
            SELECT p.*, COUNT(t.id) as total_tasks
            FROM prps p
            LEFT JOIN prp_tasks t ON p.id = t.prp_id
            WHERE 1=1
        """
        params = []
        
        if query:
            sql += " AND p.search_text LIKE ?"
            params.append(f"%{query}%")
        
        if status:
            sql += " AND p.status = ?"
            params.append(status)
        
        sql += " GROUP BY p.id ORDER BY p.created_at DESC LIMIT ?"
        params.append(limit)
        
        result = await self.mcp_client.execute_read_only_query(sql, params)
        
        print(f"🔍 Busca retornou {len(result.get('rows', []))} PRPs")
        return result.get('rows', [])
    
    async def get_prp_with_tasks(self, prp_id: int) -> Dict[str, Any]:
        """Obtém PRP com suas tarefas via MCP Turso."""
        
        # Buscar PRP
        prp_query = "SELECT * FROM prps WHERE id = ?"
        prp_result = await self.mcp_client.execute_read_only_query(prp_query, [prp_id])
        
        if not prp_result.get('rows'):
            return None
        
        prp = prp_result['rows'][0]
        
        # Buscar tarefas
        tasks_query = "SELECT * FROM prp_tasks WHERE prp_id = ? ORDER BY created_at"
        tasks_result = await self.mcp_client.execute_read_only_query(tasks_query, [prp_id])
        
        # Buscar análises LLM
        analysis_query = "SELECT * FROM prp_llm_analysis WHERE prp_id = ? ORDER BY created_at DESC"
        analysis_result = await self.mcp_client.execute_read_only_query(analysis_query, [prp_id])
        
        return {
            "prp": prp,
            "tasks": tasks_result.get('rows', []),
            "analyses": analysis_result.get('rows', [])
        }


# Demonstração de uso
async def demo_prp_mcp_integration():
    """Demonstra a integração entre Agente PRP e MCP Turso."""
    
    print("🚀 DEMONSTRAÇÃO: Integração Agente PRP + MCP Turso")
    print("=" * 60)
    
    integration = PRPMCPIntegration()
    
    # 1. Criar e armazenar um PRP
    print("\n1️⃣ Criando PRP...")
    prp_data = {
        "name": "sistema-autenticacao-jwt",
        "title": "Sistema de Autenticação com JWT",
        "description": "Implementar sistema completo de autenticação usando JWT",
        "objective": "Criar sistema seguro de login/logout com tokens JWT",
        "context_data": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "frontend": "React"
        },
        "implementation_details": {
            "backend": "Python FastAPI",
            "authentication": "JWT tokens",
            "database": "PostgreSQL com SQLAlchemy"
        },
        "validation_gates": {
            "tests": "pytest",
            "security": "OWASP guidelines"
        },
        "tags": ["backend", "security", "authentication"]
    }
    
    prp_id = await integration.store_prp(prp_data)
    
    # 2. Simular análise LLM e armazenar
    print("\n2️⃣ Simulando análise LLM...")
    analysis_data = {
        "analysis_type": "task_extraction",
        "input_content": "PRP: Sistema de Autenticação com JWT...",
        "output_content": "Análise completa do PRP...",
        "parsed_data": {
            "tasks": [
                {
                    "name": "Configurar ambiente FastAPI",
                    "description": "Configurar projeto FastAPI com dependências",
                    "type": "setup",
                    "priority": "high",
                    "estimated_hours": 2.0,
                    "complexity": "low"
                },
                {
                    "name": "Implementar modelo de usuário",
                    "description": "Criar modelo User com SQLAlchemy",
                    "type": "feature",
                    "priority": "high",
                    "estimated_hours": 3.0,
                    "complexity": "medium"
                },
                {
                    "name": "Criar endpoints de autenticação",
                    "description": "Implementar login, logout e registro",
                    "type": "feature",
                    "priority": "critical",
                    "estimated_hours": 4.0,
                    "complexity": "high"
                }
            ],
            "summary": "Sistema de autenticação JWT completo",
            "total_estimated_hours": 9.0,
            "complexity_assessment": "medium"
        },
        "model_used": "gpt-4o",
        "tokens_used": 1500,
        "processing_time_ms": 2500,
        "confidence_score": 0.95
    }
    
    analysis_id = await integration.store_llm_analysis(prp_id, analysis_data)
    
    # 3. Armazenar tarefas extraídas
    print("\n3️⃣ Armazenando tarefas extraídas...")
    tasks = analysis_data["parsed_data"]["tasks"]
    task_ids = await integration.store_tasks(prp_id, tasks)
    
    # 4. Armazenar conversa
    print("\n4️⃣ Armazenando conversa...")
    conversation_id = await integration.store_conversation(
        session_id="demo-session-001",
        message="Crie um PRP para sistema de autenticação JWT",
        response="✅ PRP criado com sucesso! Análise LLM extraiu 3 tarefas principais.",
        context="Usuário solicitou criação de PRP para autenticação"
    )
    
    # 5. Armazenar conhecimento
    print("\n5️⃣ Armazenando conhecimento...")
    knowledge_id = await integration.store_knowledge(
        topic="Autenticação JWT com FastAPI",
        content="Padrões e melhores práticas para implementar autenticação JWT em FastAPI...",
        source="prp_agent_analysis",
        tags=["fastapi", "jwt", "authentication", "security"]
    )
    
    # 6. Buscar PRPs
    print("\n6️⃣ Buscando PRPs...")
    prps = await integration.search_prps(query="autenticação", limit=5)
    
    # 7. Obter PRP completo
    print("\n7️⃣ Obtendo PRP completo...")
    prp_complete = await integration.get_prp_with_tasks(prp_id)
    
    print("\n✅ Demonstração concluída!")
    print(f"📊 Resumo:")
    print(f"   - PRP criado: {prp_id}")
    print(f"   - Análise LLM: {analysis_id}")
    print(f"   - Tarefas: {len(task_ids)}")
    print(f"   - Conversa: {conversation_id}")
    print(f"   - Conhecimento: {knowledge_id}")
    print(f"   - PRPs encontrados: {len(prps)}")


# Função para uso real com agente PRP
async def store_agent_interaction(integration: PRPMCPIntegration, 
                                session_id: str,
                                user_message: str,
                                agent_response: str,
                                prp_data: Optional[Dict[str, Any]] = None,
                                analysis_data: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
    """Armazena interação completa do agente PRP."""
    
    results = {}
    
    # 1. Armazenar conversa
    results['conversation_id'] = await integration.store_conversation(
        session_id, user_message, agent_response
    )
    
    # 2. Se criou PRP, armazenar
    if prp_data:
        results['prp_id'] = await integration.store_prp(prp_data)
        
        # 3. Se tem análise LLM, armazenar
        if analysis_data and 'prp_id' in results:
            results['analysis_id'] = await integration.store_llm_analysis(
                results['prp_id'], analysis_data
            )
            
            # 4. Se tem tarefas, armazenar
            if 'tasks' in analysis_data.get('parsed_data', {}):
                results['task_ids'] = await integration.store_tasks(
                    results['prp_id'], 
                    analysis_data['parsed_data']['tasks']
                )
    
    return results


if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(demo_prp_mcp_integration()) 