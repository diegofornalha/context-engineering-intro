#!/usr/bin/env python3
"""
Script simples para listar PRPs disponíveis
"""

import os
from pathlib import Path

def list_prps():
    """Lista todos os PRPs disponíveis"""
    
    print("📋 PRPs DISPONÍVEIS NO PRP-AGENT")
    print("=" * 60)
    
    # Diretório principal
    prps_dir = Path("PRPs")
    templates_dir = prps_dir / "templates"
    
    print("📁 Diretório Principal: /PRPs/")
    print("-" * 40)
    
    if prps_dir.exists():
        for file in prps_dir.iterdir():
            if file.is_file() and file.suffix == ".md":
                size = file.stat().st_size
                size_kb = size / 1024
                
                print(f"📄 {file.name} ({size_kb:.1f}KB)")
                
                # Descrição baseada no nome
                if "INITIAL" in file.name:
                    print("   • Template inicial para criação de PRPs")
                    print("   • Estrutura básica com seções: FEATURE, TOOLS, DEPENDENCIES")
                elif "UPDATED" in file.name:
                    print("   • ✅ PRP Atualizado - Com arquitetura flexível")
                    print("   • ✅ Core Obrigatório: PRP Agent (sempre), Turso (opcional), Sentry (opcional)")
                    print("   • ✅ Componentes Opcionais: CrewAI (opcional), A2A (opcional)")
                elif "PRP_AGENT" in file.name:
                    print("   • ❌ PRP Original - Agente PydanticAI para análise de PRPs")
                    print("   • ❌ NÃO inclui arquitetura flexível (Turso/Sentry opcionais)")
                else:
                    print("   • PRP customizado")
                
                print()
    
    print("📁 Diretório Templates: /PRPs/templates/")
    print("-" * 40)
    
    if templates_dir.exists():
        for file in templates_dir.iterdir():
            if file.is_file() and file.suffix == ".md":
                size = file.stat().st_size
                size_kb = size / 1024
                
                print(f"📄 {file.name} ({size_kb:.1f}KB)")
                
                if "pydantic_ai_base" in file.name:
                    print("   • Template base para criação de PRPs PydanticAI")
                    print("   • Estrutura completa com todas as seções necessárias")
                    print("   • Padrões e melhores práticas para desenvolvimento de agentes")
                
                print()
    
    # Contar total
    total_files = 0
    if prps_dir.exists():
        total_files += len([f for f in prps_dir.iterdir() if f.is_file() and f.suffix == ".md"])
    if templates_dir.exists():
        total_files += len([f for f in templates_dir.iterdir() if f.is_file() and f.suffix == ".md"])
    
    print("📊 RESUMO")
    print("=" * 60)
    print(f"📋 Total de PRPs: {total_files}")
    print()
    print("✅ RECOMENDADO: PRP_AGENT_UPDATED.md")
    print("   • Inclui arquitetura flexível completa")
    print("   • Componentes opcionais configuráveis")
    print("   • Melhor alinhamento com o sistema atual")
    print()
    print("🎯 DIFERENÇAS PRINCIPAIS:")
    print("   • PRP_AGENT.md: Original, sem arquitetura flexível")
    print("   • PRP_AGENT_UPDATED.md: Atualizado, com arquitetura flexível")
    print("   • INITIAL.md: Template inicial")
    print("   • prp_pydantic_ai_base.md: Template base PydanticAI")

def show_prp_details(prp_name):
    """Mostra detalhes de um PRP específico"""
    
    prp_path = Path("PRPs") / prp_name
    
    if not prp_path.exists():
        print(f"❌ PRP '{prp_name}' não encontrado")
        return
    
    print(f"📄 DETALHES DO PRP: {prp_name}")
    print("=" * 60)
    
    with open(prp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair informações básicas
    lines = content.split('\n')
    
    # Procurar por metadados
    metadata = {}
    for line in lines[:20]:  # Primeiras 20 linhas
        if line.startswith('name:') or line.startswith('description:'):
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip('"')
    
    if metadata:
        print("📋 METADADOS:")
        for key, value in metadata.items():
            print(f"   • {key}: {value}")
        print()
    
    # Contar seções
    sections = []
    for line in lines:
        if line.startswith('## '):
            sections.append(line[3:].strip())
    
    if sections:
        print("📑 SEÇÕES PRINCIPAIS:")
        for section in sections[:10]:  # Primeiras 10 seções
            print(f"   • {section}")
        print()
    
    # Estatísticas
    char_count = len(content)
    line_count = len(lines)
    word_count = len(content.split())
    
    print("📊 ESTATÍSTICAS:")
    print(f"   • Caracteres: {char_count:,}")
    print(f"   • Linhas: {line_count:,}")
    print(f"   • Palavras: {word_count:,}")
    print(f"   • Tamanho: {char_count/1024:.1f}KB")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Mostrar detalhes de um PRP específico
        prp_name = sys.argv[1]
        show_prp_details(prp_name)
    else:
        # Listar todos os PRPs
        list_prps() 