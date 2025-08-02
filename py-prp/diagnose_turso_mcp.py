#!/usr/bin/env python3
"""
Script de diagnóstico para o MCP Turso
Data: 02/08/2025
"""

import os
import subprocess
import json
import requests
from datetime import datetime

def print_status(message, status="INFO"):
    """Imprime mensagem com status colorido"""
    colors = {
        "INFO": "\033[94m",    # Azul
        "SUCCESS": "\033[92m", # Verde
        "WARNING": "\033[93m", # Amarelo
        "ERROR": "\033[91m",   # Vermelho
    }
    color = colors.get(status, "\033[0m")
    reset = "\033[0m"
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {status}: {message}{reset}")

def run_command(command, capture_output=True):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=capture_output, 
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)

def check_turso_cli():
    """Verifica se o Turso CLI está instalado e funcionando"""
    print_status("Verificando Turso CLI...", "INFO")
    
    # Verificar se está instalado
    code, stdout, stderr = run_command("which turso")
    if code != 0:
        print_status("Turso CLI não encontrado no PATH", "ERROR")
        return False
    
    print_status(f"Turso CLI encontrado em: {stdout.strip()}", "SUCCESS")
    
    # Verificar versão
    code, stdout, stderr = run_command("turso --version")
    if code == 0:
        print_status(f"Versão: {stdout.strip()}", "SUCCESS")
    else:
        print_status(f"Erro ao verificar versão: {stderr}", "ERROR")
    
    return True

def check_authentication():
    """Verifica status da autenticação"""
    print_status("Verificando autenticação...", "INFO")
    
    # Verificar status
    code, stdout, stderr = run_command("turso auth status")
    if code == 0:
        if "You are logged in" in stdout:
            print_status("Usuário autenticado", "SUCCESS")
            return True
        else:
            print_status("Usuário não autenticado", "WARNING")
            return False
    else:
        print_status(f"Erro ao verificar status: {stderr}", "ERROR")
        return False

def check_tokens():
    """Verifica tokens de banco de dados"""
    print_status("Verificando tokens de banco de dados...", "INFO")
    
    # Listar tokens
    code, stdout, stderr = run_command("turso db tokens list")
    if code == 0:
        print_status("Tokens listados com sucesso", "SUCCESS")
        print(f"Output: {stdout}")
        return True
    else:
        print_status(f"Erro ao listar tokens: {stderr}", "ERROR")
        return False

def check_databases():
    """Verifica listagem de bancos de dados"""
    print_status("Verificando bancos de dados...", "INFO")
    
    # Listar bancos
    code, stdout, stderr = run_command("turso db list")
    if code == 0:
        print_status("Bancos listados com sucesso", "SUCCESS")
        print(f"Bancos encontrados:\n{stdout}")
        return True
    else:
        print_status(f"Erro ao listar bancos: {stderr}", "ERROR")
        return False

def check_environment_variables():
    """Verifica variáveis de ambiente"""
    print_status("Verificando variáveis de ambiente...", "INFO")
    
    env_vars = [
        "TURSO_API_TOKEN",
        "TURSO_ORGANIZATION", 
        "TURSO_DATABASE_URL",
        "TURSO_DEFAULT_DATABASE"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "token" in var.lower():
                # Mascarar tokens
                masked_value = value[:20] + "..." if len(value) > 20 else "***"
                print_status(f"{var}: {masked_value}", "SUCCESS")
            else:
                print_status(f"{var}: {value}", "SUCCESS")
        else:
            print_status(f"{var}: Não configurada", "WARNING")

def check_mcp_server():
    """Verifica se o servidor MCP está rodando"""
    print_status("Verificando servidor MCP Turso...", "INFO")
    
    # Verificar processos
    code, stdout, stderr = run_command("ps aux | grep -E 'mcp.*turso|turso.*mcp' | grep -v grep")
    if code == 0 and stdout.strip():
        print_status("Servidor MCP Turso encontrado", "SUCCESS")
        print(f"Processos:\n{stdout}")
        return True
    else:
        print_status("Servidor MCP Turso não encontrado", "WARNING")
        return False

def test_api_connection():
    """Testa conexão com a API do Turso"""
    print_status("Testando conexão com API do Turso...", "INFO")
    
    token = os.getenv("TURSO_API_TOKEN")
    if not token:
        print_status("TURSO_API_TOKEN não configurado", "ERROR")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Tentar acessar a API
        response = requests.get(
            "https://api.turso.tech/v1/organizations",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print_status("Conexão com API bem-sucedida", "SUCCESS")
            return True
        else:
            print_status(f"Erro na API: {response.status_code} - {response.text}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Erro ao conectar com API: {e}", "ERROR")
        return False

def check_token_validity():
    """Verifica se o token é válido"""
    print_status("Verificando validade do token...", "INFO")
    
    token = os.getenv("TURSO_API_TOKEN")
    if not token:
        print_status("Token não encontrado", "ERROR")
        return False
    
    # Verificar formato JWT
    parts = token.split('.')
    if len(parts) != 3:
        print_status("Token não está no formato JWT válido", "ERROR")
        return False
    
    print_status("Token está no formato JWT válido", "SUCCESS")
    
    # Tentar decodificar header (sem verificar assinatura)
    import base64
    try:
        header = base64.b64decode(parts[0] + "==").decode('utf-8')
        payload = base64.b64decode(parts[1] + "==").decode('utf-8')
        
        print_status("Header JWT decodificado com sucesso", "SUCCESS")
        print(f"Header: {header}")
        print(f"Payload: {payload}")
        
        return True
    except Exception as e:
        print_status(f"Erro ao decodificar JWT: {e}", "ERROR")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 DIAGNÓSTICO COMPLETO DO MCP TURSO")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Executar verificações
    checks = [
        ("Turso CLI", check_turso_cli),
        ("Autenticação", check_authentication),
        ("Tokens", check_tokens),
        ("Bancos de Dados", check_databases),
        ("Variáveis de Ambiente", check_environment_variables),
        ("Servidor MCP", check_mcp_server),
        ("API Connection", test_api_connection),
        ("Validade do Token", check_token_validity),
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        try:
            results[name] = check_func()
        except Exception as e:
            print_status(f"Erro durante verificação: {e}", "ERROR")
            results[name] = False
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 60)
    
    for name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name}: {status}")
    
    # Recomendações
    print("\n" + "=" * 60)
    print("💡 RECOMENDAÇÕES")
    print("=" * 60)
    
    if not results.get("Autenticação", False):
        print("1. Execute: turso auth login")
    
    if not results.get("Servidor MCP", False):
        print("2. Inicie o servidor MCP: cd mcp-turso-cloud && ./start-claude.sh")
    
    if not results.get("API Connection", False):
        print("3. Verifique o token da API: echo $TURSO_API_TOKEN")
    
    if not results.get("Bancos de Dados", False):
        print("4. Teste listagem manual: turso db list")
    
    print("\n" + "=" * 60)
    print("🏁 DIAGNÓSTICO CONCLUÍDO")
    print("=" * 60)

if __name__ == "__main__":
    main() 