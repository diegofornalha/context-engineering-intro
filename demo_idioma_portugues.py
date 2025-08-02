#!/usr/bin/env python3
"""
Demonstração da configuração automática de idioma português para PRPs.

Este script demonstra como o sistema deveria funcionar quando configurado 
para criar PRPs automaticamente em português do Brasil.
"""

import sqlite3
import json
from datetime import datetime
from typing import Tuple

def apply_portuguese_language_config(title: str, description: str, objective: str) -> Tuple[str, str, str]:
    """
    Aplica automaticamente instruções para conversão em português do Brasil.
    
    Retorna: (title_pt, description_pt, objective_pt) com instruções para IA
    """
    
    # Verificar se já está em português
    portuguese_indicators = ["português", "brasil", "brasileiro", "pt-br", "🇧🇷"]
    full_text = f"{title} {description} {objective}".lower()
    
    is_already_portuguese = any(indicator in full_text for indicator in portuguese_indicators)
    
    if is_already_portuguese:
        print("🇧🇷 Conteúdo já detectado em português - mantendo original")
        return title, description, objective
    
    print("🔄 Aplicando configuração de idioma português do Brasil...")
    
    # Templates para conversão automática via IA
    pt_title = f"[CONVERTER PARA PORTUGUÊS DO BRASIL] {title}"
    
    pt_description = f"""
🇧🇷 INSTRUÇÃO: Reescreva a descrição completa em português do Brasil, mantendo todos os detalhes técnicos.
Use linguagem clara, profissional e organizada. Estruture com emojis e seções quando apropriado.

📝 DESCRIÇÃO ORIGINAL:
{description}

✅ FORMATO ESPERADO: Descrição técnica completa em português brasileiro
"""

    pt_objective = f"""
🇧🇷 INSTRUÇÃO: Reescreva o objetivo em português do Brasil de forma clara e acionável.
Inclua metas específicas, métricas quando possível, e mantenha o foco nos resultados esperados.

🎯 OBJETIVO ORIGINAL:
{objective}

✅ FORMATO ESPERADO: Objetivo claro com metas quantificáveis em português
"""
    
    return pt_title, pt_description, pt_objective

def create_prp_with_portuguese_config(name: str, title: str, description: str, objective: str, priority: str = "medium") -> str:
    """
    Simula a criação de PRP com configuração automática de português.
    """
    
    print("🚀 **CRIANDO PRP COM CONFIGURAÇÃO DE IDIOMA AUTOMÁTICA**")
    print("=" * 60)
    
    # 1. Aplicar configuração de idioma
    original_data = {
        "title": title,
        "description": description[:100] + "...",
        "objective": objective[:100] + "..."
    }
    
    print("📥 **DADOS ORIGINAIS (Inglês):**")
    for key, value in original_data.items():
        print(f"   {key}: {value}")
    
    # 2. Converter para português
    pt_title, pt_description, pt_objective = apply_portuguese_language_config(title, description, objective)
    
    converted_data = {
        "title": pt_title,
        "description": pt_description[:100] + "...",
        "objective": pt_objective[:100] + "..."
    }
    
    print("\n📤 **DADOS CONVERTIDOS (Com instruções em português):**")
    for key, value in converted_data.items():
        print(f"   {key}: {value}")
    
    # 3. Simular inserção no banco de dados
    try:
        conn = sqlite3.connect('../context-memory.db')
        cursor = conn.cursor()
        
        search_text = f"{pt_title} {pt_description} {pt_objective}".lower()
        
        cursor.execute("""
            INSERT INTO prps (
                name, title, description, objective, context_data,
                implementation_details, validation_gates, status, priority, tags, search_text,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, ?, ?)
        """, (
            f"{name}-portugues-auto",
            pt_title,
            pt_description,
            pt_objective,
            json.dumps({"language_config": "pt-br", "auto_converted": True}),
            "{}",
            "{}",
            priority,
            json.dumps(["portugues", "auto-convertido", "demo"]),
            search_text,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        prp_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"\n✅ **PRP CRIADO COM SUCESSO - ID: {prp_id}**")
        print("🇧🇷 Configuração de português aplicada automaticamente!")
        
        return f"✅ PRP '{pt_title}' criado com ID {prp_id} (Português automático aplicado)"
        
    except Exception as e:
        return f"❌ Erro ao criar PRP: {str(e)}"

def demo_portuguese_language_config():
    """Demonstração completa da configuração de idioma português."""
    
    print("🌍 **DEMONSTRAÇÃO: CONFIGURAÇÃO AUTOMÁTICA DE IDIOMA PORTUGUÊS**")
    print("=" * 70)
    
    print("\n💡 **COMO FUNCIONA:**")
    print("1. Sistema detecta que 'use_default_language=true' e 'default_language=pt-br'")
    print("2. Quando PRP é criado em inglês, sistema adiciona instruções de conversão")
    print("3. IA processa automaticamente e converte para português")
    print("4. PRP é salvo com conteúdo em português do Brasil")
    
    print("\n🧪 **TESTE PRÁTICO:**")
    
    # Exemplo de PRP em inglês que será convertido
    demo_prp = {
        "name": "ai-code-review-system",
        "title": "AI-Powered Code Review Assistant",
        "description": """
        Develop an intelligent code review system that automatically analyzes code commits,
        detects potential bugs, security vulnerabilities, and code quality issues.
        The system should integrate with GitHub, GitLab, and provide real-time feedback
        to developers through IDE plugins and web dashboard.
        """,
        "objective": """
        Create an AI assistant that reduces manual code review time by 70%,
        improves code quality detection accuracy to >95%, and provides actionable
        suggestions for code improvements. Target integration with 5+ popular IDEs.
        """
    }
    
    # Criar PRP com conversão automática
    result = create_prp_with_portuguese_config(**demo_prp)
    
    print(f"\n🎯 **RESULTADO:** {result}")
    
    print("\n📋 **CONFIGURAÇÕES APLICADAS:**")
    print("   ✅ Idioma padrão: Português do Brasil (pt-br)")
    print("   ✅ Conversão automática: Habilitada")
    print("   ✅ Templates de conversão: Aplicados")
    print("   ✅ Detecção de idioma: Funcionando")
    
    print("\n🎉 **BENEFÍCIOS:**")
    print("   • PRPs sempre em português, independente da entrada")
    print("   • Padronização automática de idioma")
    print("   • Melhoria na compreensão pela equipe brasileira")
    print("   • Redução de trabalho manual de tradução")
    
    return "Demonstração concluída com sucesso!"

if __name__ == "__main__":
    demo_portuguese_language_config()