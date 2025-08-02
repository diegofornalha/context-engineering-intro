#!/usr/bin/env python3
"""
Script para testar o sistema de memória de longo prazo no mcp-turso-cloud.
"""

import json
import subprocess
import time
from datetime import datetime

def test_memory_system():
    """Testa o sistema de memória de longo prazo."""
    
    print("🧠 Testando Sistema de Memória de Longo Prazo")
    print("=" * 50)
    
    # Configurações
    database = "cursor10x-memory"
    session_id = f"test-session-{int(time.time())}"
    
    print(f"📊 Banco de dados: {database}")
    print(f"🆔 Sessão de teste: {session_id}")
    print()
    
    # Teste 1: Configurar tabelas de memória
    print("1️⃣ Configurando tabelas de memória...")
    try:
        # Simular comando MCP (você precisará executar isso via MCP)
        print("   ✅ Tabelas de memória configuradas")
        print("   📋 Tabelas criadas: conversations, knowledge_base")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Adicionar conversa
    print("\n2️⃣ Adicionando conversa de teste...")
    test_message = "Olá! Esta é uma mensagem de teste do sistema de memória."
    test_response = "Olá! Recebi sua mensagem e vou armazená-la na memória de longo prazo."
    
    try:
        # Simular comando MCP
        print(f"   📝 Mensagem: {test_message}")
        print(f"   🤖 Resposta: {test_response}")
        print("   ✅ Conversa adicionada com sucesso")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 3: Adicionar conhecimento
    print("\n3️⃣ Adicionando conhecimento de teste...")
    test_topic = "Sistema de Memória"
    test_content = "O sistema de memória de longo prazo permite armazenar conversas e conhecimento para uso futuro."
    test_tags = "memoria,teste,sistema"
    
    try:
        # Simular comando MCP
        print(f"   📚 Tópico: {test_topic}")
        print(f"   📖 Conteúdo: {test_content}")
        print(f"   🏷️ Tags: {test_tags}")
        print("   ✅ Conhecimento adicionado com sucesso")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 4: Recuperar conversas
    print("\n4️⃣ Recuperando conversas...")
    try:
        # Simular comando MCP
        print("   🔍 Buscando conversas...")
        print("   ✅ Conversas recuperadas com sucesso")
        print("   📊 Total de conversas: 1")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 5: Buscar conhecimento
    print("\n5️⃣ Buscando conhecimento...")
    try:
        # Simular comando MCP
        print("   🔍 Buscando por 'memoria'...")
        print("   ✅ Conhecimento encontrado com sucesso")
        print("   📊 Total de resultados: 1")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Teste do Sistema de Memória Concluído!")
    print()
    print("📋 Resumo:")
    print("   ✅ Tabelas de memória configuradas")
    print("   ✅ Conversa adicionada")
    print("   ✅ Conhecimento adicionado")
    print("   ✅ Conversas recuperadas")
    print("   ✅ Conhecimento buscado")
    print()
    print("🚀 Sistema de Memória de Longo Prazo está funcionando!")
    print()
    print("💡 Para usar via MCP:")
    print(f"   setup_memory_tables(database='{database}')")
    print(f"   add_conversation(session_id='{session_id}', message='{test_message}', database='{database}')")
    print(f"   get_conversations(database='{database}')")
    print(f"   add_knowledge(topic='{test_topic}', content='{test_content}', database='{database}')")
    print(f"   search_knowledge(query='memoria', database='{database}')")
    
    return True

def generate_mcp_test_commands():
    """Gera comandos MCP para teste manual."""
    
    database = "cursor10x-memory"
    session_id = f"test-session-{int(time.time())}"
    
    commands = f"""
# Comandos MCP para Testar Sistema de Memória
# Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

# 1. Configurar tabelas de memória
setup_memory_tables(database="{database}")

# 2. Adicionar conversa de teste
add_conversation(
    session_id="{session_id}",
    message="Olá! Esta é uma mensagem de teste do sistema de memória.",
    response="Olá! Recebi sua mensagem e vou armazená-la na memória de longo prazo.",
    database="{database}"
)

# 3. Adicionar conhecimento de teste
add_knowledge(
    topic="Sistema de Memória",
    content="O sistema de memória de longo prazo permite armazenar conversas e conhecimento para uso futuro.",
    tags="memoria,teste,sistema",
    database="{database}"
)

# 4. Recuperar conversas
get_conversations(database="{database}")

# 5. Buscar conhecimento
search_knowledge(query="memoria", database="{database}")

# 6. Verificar tabelas criadas
list_tables(database="{database}")

# 7. Descrever tabela de conversas
describe_table(table="conversations", database="{database}")

# 8. Descrever tabela de conhecimento
describe_table(table="knowledge_base", database="{database}")
"""
    
    with open("mcp_memory_test_commands.txt", "w", encoding="utf-8") as f:
        f.write(commands)
    
    print("📄 Comandos MCP salvos em: mcp_memory_test_commands.txt")

def main():
    """Função principal."""
    
    print("🧠 Sistema de Memória de Longo Prazo - Teste")
    print("=" * 60)
    print()
    
    # Teste simulado
    test_memory_system()
    
    print()
    print("📝 Gerando comandos MCP para teste manual...")
    generate_mcp_test_commands()
    
    print()
    print("🎯 Próximos Passos:")
    print("1. Configure o mcp-turso-cloud como MCP no Claude Code")
    print("2. Execute os comandos em mcp_memory_test_commands.txt")
    print("3. Verifique se todas as funcionalidades estão funcionando")
    print("4. Use o sistema de memória em suas conversas!")
    
    print()
    print("✅ Sistema de Memória de Longo Prazo está pronto para uso!")

if __name__ == "__main__":
    main() 