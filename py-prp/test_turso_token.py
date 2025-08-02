#!/usr/bin/env python3
"""
Script para testar o token do Turso
Data: 02/08/2025
"""

import os
import base64
import json
import requests
from datetime import datetime

def test_token():
    """Testa o token do Turso"""
    
    # Token do arquivo start-claude.sh
    token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NTQxMTcyNTYsImlkIjoiNDc4ZDI2ODYtYTEyZS00NmU3LWI3ZTAtZDBjZTljNjNmNDA1IiwicmlkIjoiZjY5OWI1YTYtY2VjYi00ODhkLTkwN2QtOGY4MWFmZmFmMGU4In0.8BV4FDPqJYKEScxnRYovO3Guj7MeXTKXgDgJMA7FiiJhzS0g67z8hGhbPciY4ZofylPBMbpDQaSWwIbBNqguBQ"
    
    print("🔍 Analisando token do Turso...")
    print("=" * 50)
    
    # Verificar formato JWT
    parts = token.split('.')
    if len(parts) != 3:
        print("❌ Token não está no formato JWT válido")
        return
    
    print("✅ Token está no formato JWT válido")
    
    # Decodificar header
    try:
        header_b64 = parts[0]
        # Adicionar padding se necessário
        header_b64 += '=' * (4 - len(header_b64) % 4)
        header = base64.b64decode(header_b64).decode('utf-8')
        header_data = json.loads(header)
        
        print(f"📋 Header JWT:")
        print(f"   Algorithm: {header_data.get('alg', 'N/A')}")
        print(f"   Type: {header_data.get('typ', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Erro ao decodificar header: {e}")
        return
    
    # Decodificar payload
    try:
        payload_b64 = parts[1]
        # Adicionar padding se necessário
        payload_b64 += '=' * (4 - len(payload_b64) % 4)
        payload = base64.b64decode(payload_b64).decode('utf-8')
        payload_data = json.loads(payload)
        
        print(f"📋 Payload JWT:")
        print(f"   ID: {payload_data.get('id', 'N/A')}")
        print(f"   Organization ID: {payload_data.get('rid', 'N/A')}")
        print(f"   Permissions: {payload_data.get('a', 'N/A')}")
        print(f"   Issued At: {payload_data.get('iat', 'N/A')}")
        
        # Converter timestamp para data
        if 'iat' in payload_data:
            from datetime import datetime
            iat = payload_data['iat']
            date = datetime.fromtimestamp(iat)
            print(f"   Data de Emissão: {date}")
        
    except Exception as e:
        print(f"❌ Erro ao decodificar payload: {e}")
        return
    
    # Testar token com API
    print(f"\n🌐 Testando token com API do Turso...")
    
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
            print(f"📋 Organizações encontradas: {len(data)}")
        else:
            print(f"❌ Token inválido - API retornou erro")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
    
    # Verificar se o token expirou
    if 'iat' in payload_data:
        current_time = datetime.now().timestamp()
        token_age = current_time - payload_data['iat']
        token_age_days = token_age / (24 * 3600)
        
        print(f"\n⏰ Idade do Token:")
        print(f"   Emitido há: {token_age_days:.1f} dias")
        
        if token_age_days > 30:
            print("⚠️  Token pode estar expirado (mais de 30 dias)")
        else:
            print("✅ Token parece estar válido")

if __name__ == "__main__":
    test_token() 