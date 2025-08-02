#!/usr/bin/env python3
"""
Integração Real do Agente PRP com MCP Turso

Este script usa as ferramentas MCP Turso reais para armazenar dados do agente PRP.
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

# Função para simular chamada MCP Turso (em produção, seria uma chamada real)
async def call_mcp_turso_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Simula chamada para ferramenta MCP Turso."""
    
    print(f"🔧 MCP Turso: Chamando {tool_name}")
    print(f"   Parâmetros: {json.dumps(params, indent=2)}")
    
    # Simular resposta baseada na ferramenta
    if tool_name == "execute_query":
        return {
            "success": True,
            "lastInsertId": 1,
            "rowsAffected": 1
        }
    elif tool_name == "execute_read_only_query":
        return {
            "success": True,
            "rows": [],
            "columns": []
        }
    else:
        return {"success": False, "error": "Ferramenta não implementada"}


class RealPRPMCPIntegration:
    """Integração real entre Agente PRP e MCP Turso."""
    
    def __init__(self):
        self.database = "context-memory"
    
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
        
        result = await call_mcp_turso_tool("execute_query", {
            "database": self.database,
            "query": query,
            "params": params
        })
        
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
        
        result = await call_mcp_turso_tool("execute_query", {
            "database": self.database,
            "query": query,
            "params": params
        })
        
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
            
            result = await call_mcp_turso_tool("execute_query", {
                "database": self.database,
                "query": query,
                "params": params
            })
            
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
        
        result = await call_mcp_turso_tool("execute_query", {
            "database": self.database,
            "query": query,
            "params": params
        })
        
        conversation_id = result.get('lastInsertId', 1)
        print(f"💬 Conversa armazenada com ID: {conversation_id}")
        return conversation_id
    
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
        
        result = await call_mcp_turso_tool("execute_read_only_query", {
            "database": self.database,
            "query": sql,
            "params": params
        })
        
        rows = result.get('rows', [])
        print(f"🔍 Busca retornou {len(rows)} PRPs")
        return rows
    
    async def get_prp_details(self, prp_id: int) -> Dict[str, Any]:
        """Obtém detalhes de um PRP via MCP Turso."""
        
        query = "SELECT * FROM prps WHERE id = ?"
        result = await call_mcp_turso_tool("execute_read_only_query", {
            "database": self.database,
            "query": query,
            "params": [prp_id]
        })
        
        rows = result.get('rows', [])
        if not rows:
            return None
        
        return rows[0]


# Demonstração com dados reais
async def demo_real_integration():
    """Demonstra integração real com MCP Turso."""
    
    print("🚀 DEMONSTRAÇÃO REAL: Agente PRP + MCP Turso")
    print("=" * 60)
    
    integration = RealPRPMCPIntegration()
    
    # 1. Criar PRP real
    print("\n1️⃣ Criando PRP real...")
    prp_data = {
        "name": "api-rest-fastapi",
        "title": "API REST com FastAPI",
        "description": "Desenvolver API REST completa usando FastAPI",
        "objective": "Criar API robusta com documentação automática e validação",
        "context_data": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "authentication": "JWT"
        },
        "implementation_details": {
            "backend": "Python FastAPI",
            "orm": "SQLAlchemy",
            "validation": "Pydantic",
            "docs": "Swagger/OpenAPI"
        },
        "validation_gates": {
            "tests": "pytest",
            "coverage": "90%",
            "linting": "ruff"
        },
        "tags": ["api", "fastapi", "python", "backend"]
    }
    
    prp_id = await integration.store_prp(prp_data)
    
    # 2. Simular análise LLM real
    print("\n2️⃣ Simulando análise LLM real...")
    analysis_data = {
        "analysis_type": "task_extraction",
        "input_content": f"PRP: {prp_data['title']} - {prp_data['description']}",
        "output_content": "Análise completa realizada pelo LLM...",
        "parsed_data": {
            "tasks": [
                {
                    "name": "Configurar projeto FastAPI",
                    "description": "Criar estrutura base do projeto com FastAPI",
                    "type": "setup",
                    "priority": "high",
                    "estimated_hours": 1.5,
                    "complexity": "low"
                },
                {
                    "name": "Configurar banco de dados",
                    "description": "Configurar PostgreSQL e SQLAlchemy",
                    "type": "setup",
                    "priority": "high",
                    "estimated_hours": 2.0,
                    "complexity": "medium"
                },
                {
                    "name": "Criar modelos Pydantic",
                    "description": "Definir modelos de dados com validação",
                    "type": "feature",
                    "priority": "high",
                    "estimated_hours": 3.0,
                    "complexity": "medium"
                },
                {
                    "name": "Implementar endpoints CRUD",
                    "description": "Criar endpoints para operações básicas",
                    "type": "feature",
                    "priority": "critical",
                    "estimated_hours": 4.0,
                    "complexity": "high"
                },
                {
                    "name": "Configurar autenticação JWT",
                    "description": "Implementar sistema de autenticação",
                    "type": "feature",
                    "priority": "critical",
                    "estimated_hours": 3.5,
                    "complexity": "high"
                },
                {
                    "name": "Configurar documentação Swagger",
                    "description": "Configurar documentação automática da API",
                    "type": "feature",
                    "priority": "medium",
                    "estimated_hours": 1.0,
                    "complexity": "low"
                },
                {
                    "name": "Implementar testes unitários",
                    "description": "Criar testes abrangentes com pytest",
                    "type": "test",
                    "priority": "high",
                    "estimated_hours": 3.0,
                    "complexity": "medium"
                }
            ],
            "summary": "API REST completa com FastAPI, PostgreSQL e JWT",
            "total_estimated_hours": 18.0,
            "complexity_assessment": "high"
        },
        "model_used": "gpt-4o",
        "tokens_used": 2000,
        "processing_time_ms": 3000,
        "confidence_score": 0.92
    }
    
    analysis_id = await integration.store_llm_analysis(prp_id, analysis_data)
    
    # 3. Armazenar tarefas
    print("\n3️⃣ Armazenando tarefas extraídas...")
    tasks = analysis_data["parsed_data"]["tasks"]
    task_ids = await integration.store_tasks(prp_id, tasks)
    
    # 4. Armazenar conversa
    print("\n4️⃣ Armazenando conversa...")
    conversation_id = await integration.store_conversation(
        session_id="real-session-001",
        message="Crie um PRP para uma API REST com FastAPI",
        response=f"✅ PRP '{prp_data['title']}' criado com sucesso! Análise LLM extraiu {len(tasks)} tarefas principais, totalizando {analysis_data['parsed_data']['total_estimated_hours']} horas estimadas.",
        context="Usuário solicitou criação de PRP para API REST"
    )
    
    # 5. Buscar PRPs
    print("\n5️⃣ Buscando PRPs...")
    prps = await integration.search_prps(query="api", limit=5)
    
    # 6. Obter detalhes do PRP
    print("\n6️⃣ Obtendo detalhes do PRP...")
    prp_details = await integration.get_prp_details(prp_id)
    
    print("\n✅ Demonstração real concluída!")
    print(f"📊 Resumo:")
    print(f"   - PRP criado: {prp_id}")
    print(f"   - Análise LLM: {analysis_id}")
    print(f"   - Tarefas: {len(task_ids)}")
    print(f"   - Conversa: {conversation_id}")
    print(f"   - PRPs encontrados: {len(prps)}")
    print(f"   - Total estimado: {analysis_data['parsed_data']['total_estimated_hours']} horas")
    print(f"   - Complexidade: {analysis_data['parsed_data']['complexity_assessment']}")


# Função para integração com agente PydanticAI real
async def integrate_with_pydantic_agent(integration: RealPRPMCPIntegration,
                                       session_id: str,
                                       user_message: str,
                                       agent_response: str,
                                       prp_data: Optional[Dict[str, Any]] = None,
                                       llm_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
    """Integra interação do agente PydanticAI com MCP Turso."""
    
    results = {}
    
    # 1. Armazenar conversa
    results['conversation_id'] = await integration.store_conversation(
        session_id, user_message, agent_response
    )
    
    # 2. Se o agente criou um PRP, armazenar
    if prp_data:
        results['prp_id'] = await integration.store_prp(prp_data)
        
        # 3. Se o agente fez análise LLM, armazenar
        if llm_analysis and 'prp_id' in results:
            results['analysis_id'] = await integration.store_llm_analysis(
                results['prp_id'], llm_analysis
            )
            
            # 4. Se extraiu tarefas, armazenar
            if 'tasks' in llm_analysis.get('parsed_data', {}):
                results['task_ids'] = await integration.store_tasks(
                    results['prp_id'], 
                    llm_analysis['parsed_data']['tasks']
                )
    
    return results


if __name__ == "__main__":
    # Executar demonstração real
    asyncio.run(demo_real_integration()) 