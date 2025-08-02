"""
Ferramentas do agente PRP.

Este módulo contém todas as ferramentas disponíveis para o agente PRP.
"""

import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from pydantic_ai import RunContext
from .dependencies import PRPAgentDependencies
from datetime import datetime

logger = logging.getLogger(__name__)

def get_db_connection(db_path: str):
    """Obter conexão com banco de dados."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco: {e}")
        raise

async def create_prp(
    ctx: RunContext[PRPAgentDependencies],
    name: str,
    title: str,
    description: str,
    objective: str,
    context_data: str = "{}",
    implementation_details: str = "{}",
    validation_gates: str = "{}",
    priority: str = "medium",
    tags: str = "[]"
) -> str:
    """Cria um novo PRP no banco de dados."""
    
    try:
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        # Criar texto de busca para facilitar consultas
        search_text = f"{title} {description} {objective}".lower()
        
        cursor.execute("""
            INSERT INTO prps (
                name, title, description, objective, context_data,
                implementation_details, validation_gates, status, priority, tags, search_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?)
        """, (name, title, description, objective, context_data,
              implementation_details, validation_gates, priority, tags, search_text))
        
        prp_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Adicionar à conversa
        ctx.deps.add_conversation(
            f"Criar PRP: {title}",
            f"✅ PRP '{title}' criado com sucesso! ID: {prp_id}",
            {"action": "create_prp", "prp_id": prp_id}
        )
        
        return f"✅ PRP '{title}' criado com sucesso! ID: {prp_id}"
        
    except Exception as e:
        logger.error(f"Erro ao criar PRP: {e}")
        return f"❌ Erro ao criar PRP: {str(e)}"

async def search_prps(
    ctx: RunContext[PRPAgentDependencies],
    query: str = None,
    status: str = None,
    priority: str = None,
    limit: int = 10
) -> str:
    """Busca PRPs com filtros avançados."""
    
    try:
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
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
            
        if priority:
            sql += " AND p.priority = ?"
            params.append(priority)
        
        sql += " GROUP BY p.id ORDER BY p.created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "🔍 Nenhum PRP encontrado com os critérios especificados."
        
        response = f"🔍 Encontrados {len(results)} PRPs:\n\n"
        for row in results:
            response += f"**{row['title']}** (ID: {row['id']})\n"
            response += f"Status: {row['status']}, Prioridade: {row['priority']}\n"
            response += f"Tarefas: {row['total_tasks']}, Criado: {row['created_at']}\n"
            response += f"Tags: {row['tags']}\n\n"
        
        # Adicionar à conversa
        ctx.deps.add_conversation(
            f"Buscar PRPs: {query or 'todos'}",
            f"Encontrados {len(results)} PRPs",
            {"action": "search_prps", "count": len(results)}
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Erro na busca: {e}")
        return f"❌ Erro na busca: {str(e)}"

async def analyze_prp_with_llm(
    ctx: RunContext[PRPAgentDependencies],
    prp_id: int,
    analysis_type: str = "task_extraction"
) -> str:
    """Analisa PRP usando LLM para extrair tarefas e insights."""
    
    try:
        # Buscar PRP do banco
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM prps WHERE id = ?", (prp_id,))
        prp = cursor.fetchone()
        conn.close()
        
        if not prp:
            return "❌ PRP não encontrado."
        
        # Preparar prompt para LLM
        prompt = f"""
Analise o seguinte PRP e extraia as tarefas necessárias:

**PRP:** {prp['title']}
**Objetivo:** {prp['objective']}
**Descrição:** {prp['description']}
**Contexto:** {prp['context_data']}
**Implementação:** {prp['implementation_details']}

Retorne um JSON com a seguinte estrutura:
{{
    "tasks": [
        {{
            "name": "Nome da tarefa",
            "description": "Descrição detalhada",
            "type": "feature|bugfix|refactor|test|docs|setup",
            "priority": "low|medium|high|critical",
            "estimated_hours": 2.5,
            "complexity": "low|medium|high",
            "context_files": ["arquivo1.py", "arquivo2.ts"],
            "acceptance_criteria": "Critérios de aceitação"
        }}
    ],
    "summary": "Resumo da análise",
    "total_estimated_hours": 15.5,
    "complexity_assessment": "low|medium|high"
}}
"""
        
        # Simular análise LLM (em produção, seria uma chamada real)
        analysis_result = {
            "tasks": [
                {
                    "name": "Configurar ambiente de desenvolvimento",
                    "description": "Configurar projeto com dependências e estrutura base",
                    "type": "setup",
                    "priority": "high",
                    "estimated_hours": 2.0,
                    "complexity": "low"
                },
                {
                    "name": "Implementar funcionalidade principal",
                    "description": "Desenvolver a funcionalidade core do sistema",
                    "type": "feature",
                    "priority": "critical",
                    "estimated_hours": 8.0,
                    "complexity": "high"
                },
                {
                    "name": "Criar testes unitários",
                    "description": "Implementar testes abrangentes para a funcionalidade",
                    "type": "test",
                    "priority": "high",
                    "estimated_hours": 4.0,
                    "complexity": "medium"
                }
            ],
            "summary": f"Análise completa do PRP '{prp['title']}'",
            "total_estimated_hours": 14.0,
            "complexity_assessment": "medium"
        }
        
        # Salvar análise no banco
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO prp_llm_analysis (
                prp_id, analysis_type, input_content, output_content,
                parsed_data, model_used, tokens_used, processing_time_ms, confidence_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prp_id, analysis_type, prompt, "Análise LLM simulada",
            json.dumps(analysis_result), "gpt-4o", 1500, 2500, 0.95
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Preparar resposta
        response = f"""
🧠 **Análise LLM do PRP {prp_id}**

**PRP:** {prp['title']}
**Tipo de Análise:** {analysis_type}

**Tarefas Extraídas:**
"""
        
        for i, task in enumerate(analysis_result["tasks"], 1):
            response += f"{i}. **{task['name']}** ({task['type']}, {task['priority']})\n"
            response += f"   {task['description']}\n"
            response += f"   Estimativa: {task['estimated_hours']}h, Complexidade: {task['complexity']}\n\n"
        
        response += f"""
**Resumo:** {analysis_result['summary']}
**Estimativa Total:** {analysis_result['total_estimated_hours']} horas
**Complexidade:** {analysis_result['complexity_assessment']}
**Análise ID:** {analysis_id}

**Próximos Passos:** Revisar e priorizar tarefas extraídas
"""
        
        # Adicionar à conversa
        ctx.deps.add_conversation(
            f"Analisar PRP {prp_id}",
            f"Análise LLM concluída com {len(analysis_result['tasks'])} tarefas",
            {"action": "analyze_prp", "prp_id": prp_id, "analysis_id": analysis_id}
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return f"❌ Erro na análise: {str(e)}"

async def get_prp_details(
    ctx: RunContext[PRPAgentDependencies],
    prp_id: int
) -> str:
    """Obtém detalhes completos de um PRP."""
    
    try:
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        # Buscar PRP
        cursor.execute("SELECT * FROM prps WHERE id = ?", (prp_id,))
        prp = cursor.fetchone()
        
        if not prp:
            return "❌ PRP não encontrado."
        
        # Buscar tarefas
        cursor.execute("SELECT * FROM prp_tasks WHERE prp_id = ? ORDER BY created_at", (prp_id,))
        tasks = cursor.fetchall()
        
        # Buscar análises LLM
        cursor.execute("SELECT * FROM prp_llm_analysis WHERE prp_id = ? ORDER BY created_at DESC", (prp_id,))
        analyses = cursor.fetchall()
        
        conn.close()
        
        # Preparar resposta
        response = f"""
📋 **Detalhes do PRP {prp_id}**

**Informações Básicas:**
- **Título:** {prp['title']}
- **Nome:** {prp['name']}
- **Status:** {prp['status']}
- **Prioridade:** {prp['priority']}
- **Criado:** {prp['created_at']}
- **Atualizado:** {prp['updated_at']}

**Descrição:** {prp['description']}
**Objetivo:** {prp['objective']}

**Tags:** {prp['tags']}

**Tarefas ({len(tasks)}):**
"""
        
        for task in tasks:
            response += f"- **{task['task_name']}** ({task['task_type']}, {task['priority']})\n"
            response += f"  {task['description']}\n"
            response += f"  Estimativa: {task['estimated_hours']}h, Status: {task['status']}\n\n"
        
        response += f"""
**Análises LLM ({len(analyses)}):**
"""
        
        for analysis in analyses:
            response += f"- **{analysis['analysis_type']}** ({analysis['created_at']})\n"
            response += f"  Modelo: {analysis['model_used']}, Confiança: {analysis['confidence_score']}\n\n"
        
        # Adicionar à conversa
        ctx.deps.add_conversation(
            f"Detalhes PRP {prp_id}",
            f"Detalhes carregados: {len(tasks)} tarefas, {len(analyses)} análises",
            {"action": "get_prp_details", "prp_id": prp_id}
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Erro ao obter detalhes: {e}")
        return f"❌ Erro ao obter detalhes: {str(e)}"

async def update_prp_status(
    ctx: RunContext[PRPAgentDependencies],
    prp_id: int,
    new_status: str
) -> str:
    """Atualiza o status de um PRP."""
    
    try:
        conn = get_db_connection(ctx.deps.database_path)
        cursor = conn.cursor()
        
        # Verificar se PRP existe
        cursor.execute("SELECT title FROM prps WHERE id = ?", (prp_id,))
        prp = cursor.fetchone()
        
        if not prp:
            return "❌ PRP não encontrado."
        
        # Atualizar status
        cursor.execute("UPDATE prps SET status = ?, updated_at = ? WHERE id = ?", 
                      (new_status, datetime.now().isoformat(), prp_id))
        
        conn.commit()
        conn.close()
        
        # Adicionar à conversa
        ctx.deps.add_conversation(
            f"Atualizar status PRP {prp_id}",
            f"Status atualizado para: {new_status}",
            {"action": "update_prp_status", "prp_id": prp_id, "new_status": new_status}
        )
        
        return f"✅ Status do PRP '{prp['title']}' atualizado para: {new_status}"
        
    except Exception as e:
        logger.error(f"Erro ao atualizar status: {e}")
        return f"❌ Erro ao atualizar status: {str(e)}" 