#!/usr/bin/env python3
"""
Script para remover chaves de API dos arquivos antes do commit
"""

import os
import re

def clean_api_keys_in_file(filepath):
    """Remove chaves de API de um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remover chaves OpenAI
        content = re.sub(
            r'sk-proj-[A-Za-z0-9_-]+',
            'sua_chave_openai_aqui',
            content
        )
        
        # Remover outros tokens conhecidos
        content = re.sub(
            r'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
            'seu_token_aqui',
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Limpo: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Erro em {filepath}: {e}")
        return False

def main():
    """Limpar chaves de API de todos os arquivos relevantes"""
    print("🧹 Limpando chaves de API dos arquivos...")
    
    # Arquivos Python no prp-agent
    py_files = [
        'prp-agent/cursor_turso_integration.py',
        'prp-agent/cursor_final.py', 
        'prp-agent/cursor_real_mcp_integration.py',
        'prp-agent/cursor_agent_final.py',
        'prp-agent/configure_openai.py'
    ]
    
    # Arquivos de documentação
    doc_files = [
        'docs/CONFIGURACAO_CURSOR_MCP.md'
    ]
    
    all_files = py_files + doc_files
    cleaned = 0
    
    for filepath in all_files:
        if os.path.exists(filepath):
            if clean_api_keys_in_file(filepath):
                cleaned += 1
        else:
            print(f"⚠️ Arquivo não encontrado: {filepath}")
    
    print(f"\n✅ Concluído! {cleaned} arquivos limpos")

if __name__ == "__main__":
    main()