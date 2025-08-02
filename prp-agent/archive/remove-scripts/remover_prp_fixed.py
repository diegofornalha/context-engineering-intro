#!/usr/bin/env python3
"""
🗑️ Script CORRIGIDO para remover PRPs via CLI do agente

USO: python remover_prp_fixed.py <ID_DO_PRP>
"""

import sys
import sqlite3
from agents.dependencies import PRPAgentDependencies
from agents.tools import get_db_connection


def listar_prps():
    """Lista todos os PRPs disponíveis para remoção."""
    
    deps = PRPAgentDependencies()
    
    try:
        conn = get_db_connection(deps.database_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, title, status, priority, created_at
            FROM prps 
            ORDER BY created_at DESC
        """)
        
        prps = cursor.fetchall()
        conn.close()
        
        if not prps:
            print("📭 Nenhum PRP encontrado.")
            return
        
        print("🗂️ **PRPs DISPONÍVEIS:**")
        print("=" * 60)
        
        for prp in prps:
            print(f"**ID {prp[0]}:** {prp[2]}")
            print(f"   Nome: {prp[1]}")
            print(f"   Status: {prp[3]} | Prioridade: {prp[4]}")
            print(f"   Criado: {prp[5]}")
            print("-" * 40)
        
        print(f"\n🗑️ Para remover: python remover_prp_fixed.py <ID>")
        
    except Exception as e:
        print(f"❌ Erro ao listar PRPs: {e}")


def remover_prp(prp_id):
    """Remove um PRP específico."""
    
    deps = PRPAgentDependencies()
    
    try:
        conn = get_db_connection(deps.database_path)
        cursor = conn.cursor()
        
        # Verificar se existe
        cursor.execute("SELECT id, name, title, status FROM prps WHERE id = ?", (prp_id,))
        prp = cursor.fetchone()
        
        if not prp:
            print(f"❌ PRP com ID {prp_id} não encontrado.")
            conn.close()
            return
        
        print(f"🎯 **PRP ENCONTRADO:**")
        print(f"   ID: {prp[0]}")
        print(f"   Título: {prp[2]}")
        print(f"   Status: {prp[3]}")
        
        # Contar relacionamentos (com tratamento de erro)
        task_count = 0
        analysis_count = 0
        
        try:
            cursor.execute("SELECT COUNT(*) FROM prp_tasks WHERE prp_id = ?", (prp_id,))
            result = cursor.fetchone()
            task_count = result[0] if result else 0
        except:
            task_count = 0
        
        try:
            cursor.execute("SELECT COUNT(*) FROM prp_llm_analysis WHERE prp_id = ?", (prp_id,))
            result = cursor.fetchone()
            analysis_count = result[0] if result else 0
        except:
            analysis_count = 0
        
        print(f"   📝 Tarefas relacionadas: {task_count}")
        print(f"   🧠 Análises LLM: {analysis_count}")
        
        # Confirmação
        print(f"\n⚠️ **ATENÇÃO:** Esta ação é irreversível!")
        confirm = input("Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirm != "CONFIRMAR":
            print("🚫 Remoção cancelada.")
            conn.close()
            return
        
        # Executar remoção (com tratamento de erro para tabelas que podem não existir)
        try:
            cursor.execute("DELETE FROM prp_llm_analysis WHERE prp_id = ?", (prp_id,))
        except:
            pass  # Tabela pode não existir
            
        try:
            cursor.execute("DELETE FROM prp_tasks WHERE prp_id = ?", (prp_id,))
        except:
            pass  # Tabela pode não existir
            
        # Remover PRP principal
        cursor.execute("DELETE FROM prps WHERE id = ?", (prp_id,))
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ **PRP {prp_id} REMOVIDO COM SUCESSO!**")
        print(f"   🗑️ PRP principal: removido")
        print(f"   📝 Tarefas: {task_count} removidas")
        print(f"   🧠 Análises: {analysis_count} removidas")
        
    except Exception as e:
        print(f"❌ Erro ao remover PRP: {e}")
        if 'conn' in locals():
            conn.close()


def main():
    """Função principal."""
    
    if len(sys.argv) < 2:
        print("🗑️ GERENCIADOR DE REMOÇÃO DE PRPs")
        print("=" * 40)
        print("USO:")
        print("  python remover_prp_fixed.py list       # Listar PRPs")
        print("  python remover_prp_fixed.py <ID>       # Remover PRP")
        print()
        listar_prps()
        return
    
    comando = sys.argv[1]
    
    if comando.lower() == "list":
        listar_prps()
    else:
        try:
            prp_id = int(comando)
            remover_prp(prp_id)
        except ValueError:
            print("❌ ID inválido. Use um número ou 'list'.")


if __name__ == "__main__":
    main()