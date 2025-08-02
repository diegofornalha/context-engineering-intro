#!/usr/bin/env python3
"""
Teste direto do Turso para verificar se o problema está no token ou no servidor MCP
Data: 02/08/2025
"""

import requests
import json
import subprocess
import os

def test_token_direct():
    """Testa o token diretamente com a API do Turso"""
    
    token = "eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDIyMkFBQSIsImtpZCI6Imluc18yYzA4R3ZNeEhYMlNCc3l0d2padm95cEdJeDUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3NTQ3MjU0ODUsImlhdCI6MTc1NDEyMDY4NSwiaXNzIjoiaHR0cHM6Ly9jbGVyay50dXJzby50ZWNoIiwianRpIjoiY2IwNDA3ZTdhNWFmMGJkZDU2NzAiLCJuYmYiOjE3NTQxMjA2ODAsInN1YiI6InVzZXJfMng5SlpMR2FHN2VuRjJMT0M1ZlQ1Q2NLeUlvIn0.va7_z4o_nsGYol3m90mxCnKURCE8ECnYfQq1KFJINJsLNBvRPRMsiuTb94sr_qr0C6NL6IGrZrCw_oj7lLKXK1MSWKyKIlgVjB1Q8Ms_TsCzEpzyzk2TLHU9jvPW35da4TfejcdBk_gC6WOAKptbsVuqq4VL06QmOlNCPNRh9FoPFcmE2ANGbkuuvzCdW-pBjM4w2dC0toYVXa7tUzHxD1vLoVvMuMrPu_TSghiGFM7K1nnJsNHr20TXwgtRYSWlmqNhznDvL_4S__xBhdpArp5oyNvjbsaibcwlWw0LhxDtgJaYzYRySWs0FTMxYaoz1Jbk3Avb2gbqYNfd1DCyKQ"
    
    print("🔍 Testando token diretamente com API do Turso...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Testar endpoint de organizações
        response = requests.get(
            "https://api.turso.tech/v1/organizations",
            headers=headers,
            timeout=10
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Token válido - API respondeu com sucesso")
            data = response.json()
            print(f"📋 Organizações: {data}")
            
            # Testar endpoint de bancos de dados
            org_slug = data[0]['slug'] if data else 'diegofornalha'
            print(f"\n🗄️ Testando bancos da organização: {org_slug}")
            
            db_response = requests.get(
                f"https://api.turso.tech/v1/organizations/{org_slug}/databases",
                headers=headers,
                timeout=10
            )
            
            print(f"📡 Status Code (DBs): {db_response.status_code}")
            
            if db_response.status_code == 200:
                dbs = db_response.json()
                print(f"✅ Bancos encontrados: {len(dbs)}")
                for db in dbs:
                    print(f"   - {db.get('name', 'N/A')}: {db.get('url', 'N/A')}")
            else:
                print(f"❌ Erro ao listar bancos: {db_response.text}")
                
        else:
            print(f"❌ Token inválido: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_cli_direct():
    """Testa o CLI do Turso diretamente"""
    
    print("\n🔍 Testando CLI do Turso diretamente...")
    
    try:
        # Testar listagem de bancos
        result = subprocess.run(
            ["turso", "db", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"📡 Exit Code: {result.returncode}")
        print(f"📋 Output: {result.stdout}")
        
        if result.stderr:
            print(f"❌ Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro ao executar CLI: {e}")

def test_mcp_server():
    """Testa o servidor MCP diretamente"""
    
    print("\n🔍 Testando servidor MCP diretamente...")
    
    # Configurar variáveis de ambiente
    env = os.environ.copy()
    env['TURSO_API_TOKEN'] = "eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDIyMkFBQSIsImtpZCI6Imluc18yYzA4R3ZNeEhYMlNCc3l0d2padm95cEdJeDUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3NTQ3MjU0ODUsImlhdCI6MTc1NDEyMDY4NSwiaXNzIjoiaHR0cHM6Ly9jbGVyay50dXJzby50ZWNoIiwianRpIjoiY2IwNDA3ZTdhNWFmMGJkZDU2NzAiLCJuYmYiOjE3NTQxMjA2ODAsInN1YiI6InVzZXJfMng5SlpMR2FHN2VuRjJMT0M1ZlQ1Q2NLeUlvIn0.va7_z4o_nsGYol3m90mxCnKURCE8ECnYfQq1KFJINJsLNBvRPRMsiuTb94sr_qr0C6NL6IGrZrCw_oj7lLKXK1MSWKyKIlgVjB1Q8Ms_TsCzEpzyzk2TLHU9jvPW35da4TfejcdBk_gC6WOAKptbsVuqq4VL06QmOlNCPNRh9FoPFcmE2ANGbkuuvzCdW-pBjM4w2dC0toYVXa7tUzHxD1vLoVvMuMrPu_TSghiGFM7K1nnJsNHr20TXwgtRYSWlmqNhznDvL_4S__xBhdpArp5oyNvjbsaibcwlWw0LhxDtgJaYzYRySWs0FTMxYaoz1Jbk3Avb2gbqYNfd1DCyKQ"
    env['TURSO_ORGANIZATION'] = "diegofornalha"
    
    try:
        # Executar servidor MCP
        result = subprocess.run(
            ["node", "dist/index.js"],
            cwd="mcp-turso-cloud",
            env=env,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"📡 Exit Code: {result.returncode}")
        print(f"📋 Output: {result.stdout}")
        
        if result.stderr:
            print(f"❌ Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Servidor MCP iniciado (timeout esperado)")
    except Exception as e:
        print(f"❌ Erro ao executar servidor MCP: {e}")

def main():
    """Função principal"""
    print("🔧 TESTE DIRETO DO TURSO")
    print("=" * 50)
    
    # Testar token diretamente
    test_token_direct()
    
    # Testar CLI diretamente
    test_cli_direct()
    
    # Testar servidor MCP
    test_mcp_server()
    
    print("\n" + "=" * 50)
    print("🏁 TESTE CONCLUÍDO")
    print("=" * 50)

if __name__ == "__main__":
    main() 