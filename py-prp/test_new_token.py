#!/usr/bin/env python3
"""
Script para testar o novo token do Turso
Data: 02/08/2025
"""

import requests
import base64
import json
from datetime import datetime

def test_new_token():
    """Testa o novo token do Turso"""
    
    # Novo token gerado
    token = "eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDIyMkFBQSIsImtpZCI6Imluc18yYzA4R3ZNeEhYMlNCc3l0d2padm95cEdJeDUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3NTQ3MjU0ODUsImlhdCI6MTc1NDEyMDY4NSwiaXNzIjoiaHR0cHM6Ly9jbGVyay50dXJzby50ZWNoIiwianRpIjoiY2IwNDA3ZTdhNWFmMGJkZDU2NzAiLCJuYmYiOjE3NTQxMjA2ODAsInN1YiI6InVzZXJfMng5SlpMR2FHN2VuRjJMT0M1ZlQ1Q2NLeUlvIn0.va7_z4o_nsGYol3m90mxCnKURCE8ECnYfQq1KFJINJsLNBvRPRMsiuTb94sr_qr0C6NL6IGrZrCw_oj7lLKXK1MSWKyKIlgVjB1Q8Ms_TsCzEpzyzk2TLHU9jvPW35da4TfejcdBk_gC6WOAKptbsVuqq4VL06QmOlNCPNRh9FoPFcmE2ANGbkuuvzCdW-pBjM4w2dC0toYVXa7tUzHxD1vLoVvMuMrPu_TSghiGFM7K1nnJsNHr20TXwgtRYSWlmqNhznDvL_4S__xBhdpArp5oyNvjbsaibcwlWw0LhxDtgJaYzYRySWs0FTMxYaoz1Jbk3Avb2gbqYNfd1DCyKQ"
    
    print("🔍 Testando novo token do Turso...")
    print("=" * 50)
    
    # Decodificar payload
    parts = token.split('.')
    payload_b64 = parts[1]
    payload_b64 += '=' * (4 - len(payload_b64) % 4)
    payload = base64.b64decode(payload_b64).decode('utf-8')
    payload_data = json.loads(payload)
    
    print(f"📋 Payload JWT:")
    print(f"   Subject: {payload_data.get('sub', 'N/A')}")
    print(f"   Issuer: {payload_data.get('iss', 'N/A')}")
    print(f"   Issued At: {payload_data.get('iat', 'N/A')}")
    print(f"   Expires At: {payload_data.get('exp', 'N/A')}")
    
    # Testar com API
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
        
        print(f"\n📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Token válido!")
            data = response.json()
            print(f"📋 Organizações: {data}")
        else:
            print(f"❌ Token inválido: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_new_token() 