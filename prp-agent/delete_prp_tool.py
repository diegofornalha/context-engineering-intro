#!/usr/bin/env python3
"""
🗑️ Ferramenta para deletar PRPs do PRP Agent

Esta ferramenta adiciona capacidade de remoção segura de PRPs com confirmação.
"""

import asyncio
import sqlite3
import logging
from typing import Optional
from agents.dependencies import PRPAgentDependencies
from agents.tools import get_db_connection

logger = logging.getLogger(__name__)


async def delete_prp(
    deps: PRPAgentDependencies,
    prp_id: int,
    confirm: bool = False
) -> str:
    """
    Remove um PRP do banco de dados.
    
    Args:
        deps: Dependências do agente
        prp_id: ID do PRP a ser removido
        confirm: Confirmação de remoção (segurança)
    
    Returns:
        Resultado da operação
    """
    
    try:
        conn = get_db_connection(deps.database_path)
        cursor = conn.cursor()
        
        # Verificar se PRP existe
        cursor.execute("SELECT id, name, title, status FROM prps WHERE id = ?", (prp_id,))
        prp = cursor.fetchone()
        
        if not prp:
            conn.close()
            return f"❌ PRP com ID {prp_id} não encontrado."
        
        prp_info = {
            "id": prp[0],
            "name": prp[1], 
            "title": prp[2],
            "status": prp[3]
        }
        
        if not confirm:
            conn.close()
            return f"""
⚠️ **CONFIRMAÇÃO NECESSÁRIA**

Você está prestes a remover o PRP:
- **ID:** {prp_info['id']}
- **Nome:** {prp_info['name']}
- **Título:** {prp_info['title']}
- **Status:** {prp_info['status']}

⚠️ **ATENÇÃO:** Esta ação é irreversível e removerá:
- O PRP principal
- Todas as tarefas relacionadas
- Todas as análises LLM do PRP

Para confirmar, execute novamente com confirm=True
"""
        
        # Contar relacionamentos
        cursor.execute("SELECT COUNT(*) FROM prp_tasks WHERE prp_id = ?", (prp_id,))
        task_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM prp_llm_analysis WHERE prp_id = ?", (prp_id,))
        analysis_count = cursor.fetchone()[0]
        
        # Remover em ordem (relacionamentos primeiro)
        # 1. Remover análises LLM
        cursor.execute("DELETE FROM prp_llm_analysis WHERE prp_id = ?", (prp_id,))
        
        # 2. Remover tarefas
        cursor.execute("DELETE FROM prp_tasks WHERE prp_id = ?", (prp_id,))
        
        # 3. Remover PRP principal
        cursor.execute("DELETE FROM prps WHERE id = ?", (prp_id,))
        
        conn.commit()
        conn.close()
        
        # Registrar no histórico
        deps.add_conversation(
            f"Deletar PRP {prp_id}",
            f"PRP '{prp_info['title']}' removido com sucesso",
            {
                "action": "delete_prp",
                "prp_id": prp_id,
                "tasks_removed": task_count,
                "analyses_removed": analysis_count
            }
        )
        
        return f"""
✅ **PRP REMOVIDO COM SUCESSO**

**PRP Removido:**
- **ID:** {prp_info['id']}
- **Título:** {prp_info['title']}

**Itens Removidos:**
- 📝 Tarefas relacionadas: {task_count}
- 🧠 Análises LLM: {analysis_count}
- 🗂️ PRP principal: 1

🗑️ **Operação concluída irreversivelmente.**
"""
        
    except Exception as e:
        logger.error(f"Erro ao deletar PRP: {e}")
        return f"❌ Erro ao deletar PRP: {str(e)}"


async def list_prps_for_deletion(deps: PRPAgentDependencies) -> str:
    """Lista PRPs disponíveis para remoção."""
    
    try:
        conn = get_db_connection(deps.database_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, title, status, priority, created_at,
                   (SELECT COUNT(*) FROM prp_tasks WHERE prp_id = prps.id) as task_count,
                   (SELECT COUNT(*) FROM prp_llm_analysis WHERE prp_id = prps.id) as analysis_count
            FROM prps 
            ORDER BY created_at DESC
        """)
        
        prps = cursor.fetchall()
        conn.close()
        
        if not prps:
            return "📭 Nenhum PRP encontrado no banco de dados."
        
        response = "🗂️ **PRPs DISPONÍVEIS PARA REMOÇÃO:**\n\n"
        
        for prp in prps:
            response += f"""
**ID {prp[0]}:** {prp[2]}
- **Nome:** {prp[1]}
- **Status:** {prp[3]} | **Prioridade:** {prp[4]}
- **Criado:** {prp[5]}
- **Itens relacionados:** {prp[6]} tarefas, {prp[7]} análises
---"""
        
        response += """

🗑️ **Para remover um PRP:**
`python delete_prp_example.py <ID_DO_PRP>`

⚠️ **ATENÇÃO:** Remoção é irreversível!
"""
        
        return response
        
    except Exception as e:
        logger.error(f"Erro ao listar PRPs: {e}")
        return f"❌ Erro ao listar PRPs: {str(e)}"


async def main():
    """Interface principal para gerenciar remoção de PRPs."""
    
    deps = PRPAgentDependencies(session_id="delete-prp-session")
    
    print("🗑️ GERENCIADOR DE REMOÇÃO DE PRPs")
    print("=" * 50)
    
    # Listar PRPs
    prp_list = await list_prps_for_deletion(deps)
    print(prp_list)
    
    # Interface interativa
    while True:
        print("\n🎯 OPÇÕES:")
        print("1. Listar PRPs novamente")
        print("2. Remover PRP específico")
        print("3. Sair")
        
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == "1":
            prp_list = await list_prps_for_deletion(deps)
            print(prp_list)
            
        elif choice == "2":
            try:
                prp_id = int(input("Digite o ID do PRP para remover: ").strip())
                
                # Primeira chamada - mostrar confirmação
                result = await delete_prp(deps, prp_id, confirm=False)
                print(result)
                
                # Pedir confirmação
                if "CONFIRMAÇÃO NECESSÁRIA" in result:
                    confirm = input("\nTem certeza? Digite 'CONFIRMAR' para prosseguir: ").strip()
                    
                    if confirm == "CONFIRMAR":
                        # Segunda chamada - executar remoção
                        final_result = await delete_prp(deps, prp_id, confirm=True)
                        print(final_result)
                    else:
                        print("🚫 Remoção cancelada.")
                        
            except ValueError:
                print("❌ ID inválido. Digite um número.")
            except Exception as e:
                print(f"❌ Erro: {e}")
                
        elif choice == "3":
            print("👋 Saindo...")
            break
            
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    asyncio.run(main())