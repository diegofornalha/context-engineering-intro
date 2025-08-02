#!/usr/bin/env python3
"""
Script de configuração de idioma para PRPs.

Este script permite configurar e testar o idioma padrão para criação de PRPs.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório prp-agent ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "prp-agent"))

from prp_agent.agents.settings import settings

def show_current_config():
    """Mostra a configuração atual de idioma."""
    print("🌍 **CONFIGURAÇÃO ATUAL DE IDIOMA:**")
    print("=" * 50)
    print(f"📍 Idioma padrão: {settings.default_language}")
    print(f"🏷️ Nome do idioma: {settings.language_name}")
    print(f"🔄 Usar automaticamente: {'✅ SIM' if settings.use_default_language else '❌ NÃO'}")
    print()

def configure_portuguese():
    """Configura o sistema para português do Brasil."""
    print("🇧🇷 **CONFIGURANDO PARA PORTUGUÊS DO BRASIL...**")
    
    # Criar/atualizar arquivo .env com configurações de idioma
    env_path = Path(".env")
    
    # Ler conteúdo existente se houver
    existing_content = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_content = f.readlines()
    
    # Remover linhas de idioma existentes
    filtered_content = [
        line for line in existing_content 
        if not any(prefix in line for prefix in [
            'DEFAULT_LANGUAGE=', 'LANGUAGE_NAME=', 'USE_DEFAULT_LANGUAGE='
        ])
    ]
    
    # Adicionar configurações de idioma em português
    language_config = [
        '\n# Configurações de Idioma\n',
        'DEFAULT_LANGUAGE=pt-br\n',
        'LANGUAGE_NAME=Português do Brasil\n',
        'USE_DEFAULT_LANGUAGE=true\n'
    ]
    
    # Escrever novo conteúdo
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(filtered_content)
        f.writelines(language_config)
    
    print("✅ Configuração salva no arquivo .env")
    print("✅ Todos os novos PRPs serão criados em português do Brasil automaticamente")
    
def configure_english():
    """Configura o sistema para inglês."""
    print("🇺🇸 **CONFIGURANDO PARA INGLÊS...**")
    
    env_path = Path(".env")
    
    # Ler conteúdo existente se houver
    existing_content = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_content = f.readlines()
    
    # Remover linhas de idioma existentes
    filtered_content = [
        line for line in existing_content 
        if not any(prefix in line for prefix in [
            'DEFAULT_LANGUAGE=', 'LANGUAGE_NAME=', 'USE_DEFAULT_LANGUAGE='
        ])
    ]
    
    # Adicionar configurações de idioma em inglês
    language_config = [
        '\n# Language Configuration\n',
        'DEFAULT_LANGUAGE=en\n',
        'LANGUAGE_NAME=English\n',
        'USE_DEFAULT_LANGUAGE=true\n'
    ]
    
    # Escrever novo conteúdo
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(filtered_content)
        f.writelines(language_config)
    
    print("✅ Configuration saved to .env file")
    print("✅ All new PRPs will be created in English automatically")

def disable_auto_language():
    """Desabilita a aplicação automática de idioma."""
    print("⚠️ **DESABILITANDO IDIOMA AUTOMÁTICO...**")
    
    env_path = Path(".env")
    
    # Ler conteúdo existente se houver
    existing_content = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            existing_content = f.readlines()
    
    # Remover linhas de idioma existentes
    filtered_content = [
        line for line in existing_content 
        if not any(prefix in line for prefix in [
            'DEFAULT_LANGUAGE=', 'LANGUAGE_NAME=', 'USE_DEFAULT_LANGUAGE='
        ])
    ]
    
    # Desabilitar idioma automático
    language_config = [
        '\n# Language Configuration (DISABLED)\n',
        'DEFAULT_LANGUAGE=pt-br\n',
        'LANGUAGE_NAME=Português do Brasil\n',
        'USE_DEFAULT_LANGUAGE=false\n'
    ]
    
    # Escrever novo conteúdo
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(filtered_content)
        f.writelines(language_config)
    
    print("✅ Idioma automático desabilitado")
    print("ℹ️ PRPs serão criados no idioma original informado")

def main():
    """Função principal do script."""
    print("🌍 **CONFIGURADOR DE IDIOMA - PRP AGENT**")
    print("=" * 50)
    
    show_current_config()
    
    print("🎯 **OPÇÕES DISPONÍVEIS:**")
    print("1. 🇧🇷 Configurar para Português do Brasil (RECOMENDADO)")
    print("2. 🇺🇸 Configurar para Inglês")
    print("3. ⚠️ Desabilitar idioma automático")
    print("4. 📊 Mostrar configuração atual")
    print("5. 🚪 Sair")
    
    while True:
        try:
            choice = input("\n👉 Escolha uma opção (1-5): ").strip()
            
            if choice == "1":
                configure_portuguese()
                print("\n🎉 **CONFIGURAÇÃO CONCLUÍDA!**")
                print("🔄 Reinicie o agente para aplicar as mudanças.")
                break
            elif choice == "2":
                configure_english()
                print("\n🎉 **CONFIGURATION COMPLETED!**")
                print("🔄 Restart the agent to apply changes.")
                break
            elif choice == "3":
                disable_auto_language()
                print("\n✅ **CONFIGURAÇÃO ATUALIZADA!**")
                print("🔄 Reinicie o agente para aplicar as mudanças.")
                break
            elif choice == "4":
                print()
                show_current_config()
            elif choice == "5":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()