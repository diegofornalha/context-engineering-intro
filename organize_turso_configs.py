#!/usr/bin/env python3
"""
Script para organizar configurações do Turso
Data: 02/08/2025
"""

import base64
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple

def decode_jwt_payload(token: str) -> Dict:
    """Decodifica o payload de um JWT"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        
        payload_b64 = parts[1]
        payload_b64 += '=' * (4 - len(payload_b64) % 4)
        payload = base64.b64decode(payload_b64).decode('utf-8')
        return json.loads(payload)
    except Exception as e:
        print(f"Erro ao decodificar JWT: {e}")
        return {}

def test_token_with_api(token: str) -> Tuple[bool, str]:
    """Testa token com a API do Turso"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.turso.tech/v1/organizations",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "✅ Válido"
        else:
            return False, f"❌ Erro {response.status_code}: {response.text}"
            
    except Exception as e:
        return False, f"❌ Erro de conexão: {e}"

def analyze_token(token: str, name: str) -> Dict:
    """Analisa um token específico"""
    print(f"\n🔍 Analisando {name}...")
    print("-" * 50)
    
    payload = decode_jwt_payload(token)
    
    if not payload:
        return {
            "name": name,
            "token": token[:20] + "...",
            "valid": False,
            "error": "Token inválido"
        }
    
    # Extrair informações
    iat = payload.get('iat', 0)
    exp = payload.get('exp', 0)
    sub = payload.get('sub', 'N/A')
    rid = payload.get('rid', 'N/A')
    alg = payload.get('alg', 'N/A')
    
    # Converter timestamps
    issued_at = datetime.fromtimestamp(iat) if iat else None
    expires_at = datetime.fromtimestamp(exp) if exp else None
    current_time = datetime.now()
    
    # Calcular idade
    age_days = (current_time - issued_at).days if issued_at else None
    
    # Verificar se expirou
    is_expired = expires_at and current_time > expires_at if expires_at else False
    
    print(f"📋 Informações:")
    print(f"   Subject: {sub}")
    print(f"   Organization ID: {rid}")
    print(f"   Algorithm: {alg}")
    print(f"   Emitido em: {issued_at}")
    print(f"   Expira em: {expires_at}")
    print(f"   Idade: {age_days} dias")
    print(f"   Expirado: {'Sim' if is_expired else 'Não'}")
    
    # Testar com API
    is_valid, api_result = test_token_with_api(token)
    print(f"   API Test: {api_result}")
    
    return {
        "name": name,
        "token": token,
        "payload": payload,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "age_days": age_days,
        "is_expired": is_expired,
        "api_valid": is_valid,
        "api_result": api_result,
        "valid": is_valid and not is_expired
    }

def main():
    """Função principal"""
    print("🔧 ORGANIZAÇÃO DE CONFIGURAÇÕES DO TURSO")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Tokens para análise
    tokens = {
        "Token Novo (Gerado Agora)": "eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDIyMkFBQSIsImtpZCI6Imluc18yYzA4R3ZNeEhYMlNCc3l0d2padm95cEdJeDUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3NTQ3MjU0ODUsImlhdCI6MTc1NDEyMDY4NSwiaXNzIjoiaHR0cHM6Ly9jbGVyay50dXJzby50ZWNoIiwianRpIjoiY2IwNDA3ZTdhNWFmMGJkZDU2NzAiLCJuYmYiOjE3NTQxMjA2ODAsInN1YiI6InVzZXJfMng5SlpMR2FHN2VuRjJMT0M1ZlQ1Q2NLeUlvIn0.va7_z4o_nsGYol3m90mxCnKURCE8ECnYfQq1KFJINJsLNBvRPRMsiuTb94sr_qr0C6NL6IGrZrCw_oj7lLKXK1MSWKyKIlgVjB1Q8Ms_TsCzEpzyzk2TLHU9jvPW35da4TfejcdBk_gC6WOAKptbsVuqq4VL06QmOlNCPNRh9FoPFcmE2ANGbkuuvzCdW-pBjM4w2dC0toYVXa7tUzHxD1vLoVvMuMrPu_TSghiGFM7K1nnJsNHr20TXwgtRYSWlmqNhznDvL_4S__xBhdpArp5oyNvjbsaibcwlWw0LhxDtgJaYzYRySWs0FTMxYaoz1Jbk3Avb2gbqYNfd1DCyKQ",
        
        "Token Antigo (start-claude.sh)": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NTQxMTcyNTYsImlkIjoiNDc4ZDI2ODYtYTEyZS00NmU3LWI3ZTAtZDBjZTljNjNmNDA1IiwicmlkIjoiZjY5OWI1YTYtY2VjYi00ODhkLTkwN2QtOGY4MWFmZmFmMGU4In0.8BV4FDPqJYKEScxnRYovO3Guj7MeXTKXgDgJMA7FiiJhzS0g67z8hGhbPciY4ZofylPBMbpDQaSWwIbBNqguBQ",
        
        "Token Usuário (Mencionado)": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJleHAiOjE3NTQ3MTQyNDQsImdpZCI6IjhmNTA5ODk3LWJmYjEtNGRiNS05YWZjLWRjZTVhYjIyNTk2MyIsImlhdCI6MTc1NDEwOTQ0NCwicmlkIjoiOWY2OGU4OWItYTc3Zi00ODVmLWFlY2YtMDg5YWE2NTBiNjE0In0.fwn_9RJL7tNz77_XcKUAidGWvDSCP50guqx-YXEEA0KhXRS20zjpbFgBxVwuhh83-HAKFCBzByPX8ewrSjvzDg",
        
        "Token AUTH_TOKEN": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTQxMTc5NjIsImlkIjoiOTUwY2ExMGUtN2EzMi00ODgwLTkyYjgtOTNkMTdmZTZjZTBkIiwicmlkIjoiZWU2YTJlNmYtMDViYy00NWIzLWEyOTgtN2Q0NzE3NTE0YjRiIn0.rnD-GZ4nA8dOvorMQ6GwM2yKSNT4KcKwwAzjdgzqK1ZUMoCOe_c23CusgnsBNr3m6WzejPMiy0HlrrMUfqZBCA"
    }
    
    # Analisar todos os tokens
    results = []
    for name, token in tokens.items():
        result = analyze_token(token, name)
        results.append(result)
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DA ANÁLISE")
    print("=" * 60)
    
    valid_tokens = [r for r in results if r["valid"]]
    expired_tokens = [r for r in results if r["is_expired"]]
    invalid_tokens = [r for r in results if not r["valid"] and not r["is_expired"]]
    
    print(f"✅ Tokens Válidos: {len(valid_tokens)}")
    print(f"⏰ Tokens Expirados: {len(expired_tokens)}")
    print(f"❌ Tokens Inválidos: {len(invalid_tokens)}")
    
    if valid_tokens:
        print(f"\n🎯 MELHOR TOKEN RECOMENDADO:")
        best_token = max(valid_tokens, key=lambda x: x["issued_at"] if x["issued_at"] else datetime.min)
        print(f"   Nome: {best_token['name']}")
        print(f"   Emitido: {best_token['issued_at']}")
        print(f"   Idade: {best_token['age_days']} dias")
        print(f"   Token: {best_token['token'][:50]}...")
    
    # Configurações de banco de dados
    print(f"\n🗄️ CONFIGURAÇÕES DE BANCO DE DADOS:")
    databases = {
        "cursor10x-memory": "libsql://cursor10x-memory-diegofornalha.aws-us-east-1.turso.io",
        "context-memory": "libsql://context-memory-diegofornalha.aws-us-east-1.turso.io",
        "sentry-errors-doc": "libsql://sentry-errors-doc-diegofornalha.aws-us-east-1.turso.io"
    }
    
    for name, url in databases.items():
        print(f"   {name}: {url}")
    
    # Gerar arquivo de configuração recomendado
    if valid_tokens:
        print(f"\n📝 GERANDO CONFIGURAÇÃO RECOMENDADA...")
        generate_config_file(best_token, databases)
    
    print(f"\n" + "=" * 60)
    print("🏁 ANÁLISE CONCLUÍDA")
    print("=" * 60)

def generate_config_file(best_token: Dict, databases: Dict):
    """Gera arquivo de configuração recomendado"""
    
    config_content = f"""# Configuração Turso Recomendada
# Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

# Token API (Mais recente e válido)
TURSO_API_TOKEN="{best_token['token']}"

# Organização
TURSO_ORGANIZATION="diegofornalha"

# Banco de dados padrão (recomendado: cursor10x-memory)
TURSO_DEFAULT_DATABASE="cursor10x-memory"
TURSO_DATABASE_URL="{databases['cursor10x-memory']}"

# Outros bancos disponíveis
TURSO_CONTEXT_MEMORY_URL="{databases['context-memory']}"
TURSO_SENTRY_ERRORS_URL="{databases['sentry-errors-doc']}"

# Configurações MCP
MCP_SERVER_NAME="mcp-turso-cloud"
MCP_SERVER_VERSION="1.0.0"

# Configurações do Projeto
PROJECT_NAME="context-engineering-intro"
PROJECT_VERSION="1.0.0"
ENVIRONMENT="development"

# Informações do Token
# Nome: {best_token['name']}
# Emitido: {best_token['issued_at']}
# Válido até: {best_token['expires_at']}
# Idade: {best_token['age_days']} dias
"""
    
    with open("turso_config_recommended.env", "w") as f:
        f.write(config_content)
    
    print("   ✅ Arquivo gerado: turso_config_recommended.env")

if __name__ == "__main__":
    main() 