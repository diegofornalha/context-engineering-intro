#!/bin/bash

# Script para configurar arquivo .env do MCP Turso
echo "🔧 Configurando arquivo .env para MCP Turso..."

# Verificar se já existe arquivo .env
if [ -f ".env" ]; then
    echo "⚠️  Arquivo .env já existe. Deseja sobrescrever? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Configuração cancelada."
        exit 0
    fi
fi

# Verificar se existe arquivo .env.example
if [ ! -f ".env.example" ]; then
    echo "❌ Arquivo .env.example não encontrado!"
    echo "📝 Criando arquivo .env.example..."
    
    cat > .env.example << 'EOF'
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://seu-banco-sua-org.aws-us-east-1.turso.io
TURSO_AUTH_TOKEN=seu-token-aqui

# MCP Server Configuration
MCP_SERVER_NAME=mcp-turso-memory
MCP_SERVER_VERSION=1.0.0

# Optional: Project Configuration
PROJECT_NAME=meu-projeto-memoria
PROJECT_VERSION=1.0.0
ENVIRONMENT=development
EOF
fi

# Verificar se existe arquivo .env na raiz do projeto
if [ -f "../.env.turso" ]; then
    echo "📝 Copiando configurações do arquivo .env.turso..."
    cp ../.env.turso .env
    echo "✅ Arquivo .env criado com configurações do projeto principal!"
else
    echo "📝 Criando arquivo .env com configurações padrão..."
    
    # Criar arquivo .env com configurações padrão
    cat > .env << 'EOF'
# Turso Database Configuration
TURSO_DATABASE_URL=libsql://context-memory-diegofornalha.aws-us-east-1.turso.io
TURSO_AUTH_TOKEN=eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTQxMTc5NjIsImlkIjoiOTUwY2ExMGUtN2EzMi00ODgwLTkyYjgtOTNkMTdmZTZjZTBkIiwicmlkIjoiZWU2YTJlNmYtMDViYy00NWIzLWEyOTgtN2Q0NzE3NTE0YjRiIn0.rnD-GZ4nA8dOvorMQ6GwM2yKSNT4KcKwwAzjdgzqK1ZUMoCOe_c23CusgnsBNr3m6WzejPMiy0HlrrMUfqZBCA

# MCP Server Configuration
MCP_SERVER_NAME=mcp-turso-memory
MCP_SERVER_VERSION=1.0.0

# Optional: Project Configuration
PROJECT_NAME=context-engineering-intro
PROJECT_VERSION=1.0.0
ENVIRONMENT=development
EOF
    
    echo "✅ Arquivo .env criado com configurações padrão!"
fi

# Verificar se as variáveis estão configuradas
echo "🔍 Verificando configurações..."
if [ -f ".env" ]; then
    echo "📊 Configurações atuais:"
    echo "   TURSO_DATABASE_URL: $(grep TURSO_DATABASE_URL .env | cut -d'=' -f2)"
    echo "   MCP_SERVER_NAME: $(grep MCP_SERVER_NAME .env | cut -d'=' -f2)"
    echo "   ENVIRONMENT: $(grep ENVIRONMENT .env | cut -d'=' -f2)"
else
    echo "❌ Erro: Arquivo .env não foi criado!"
    exit 1
fi

echo ""
echo "✅ Configuração concluída!"
echo "🚀 Para iniciar o servidor MCP:"
echo "   ./start.sh" 