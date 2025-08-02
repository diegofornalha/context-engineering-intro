#!/bin/bash

# Script para build de produção com source maps
# Uso: ./build.sh

echo "🏗️  Iniciando build de produção..."

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ]; then
    echo "❌ Erro: package.json não encontrado"
    exit 1
fi

# Definir versão
VERSION=${1:-"1.0.0"}
echo "📌 Versão: $VERSION"

# Criar build
echo "📦 Criando build otimizada..."
REACT_APP_VERSION=$VERSION npm run build

if [ $? -ne 0 ]; then
    echo "❌ Erro no build"
    exit 1
fi

# Verificar se Sentry CLI está instalado
if ! command -v sentry-cli &> /dev/null; then
    echo "📦 Instalando Sentry CLI..."
    npm install -g @sentry/cli
fi

# Upload de source maps
echo "📤 Enviando source maps para o Sentry..."
sentry-cli releases new $VERSION
sentry-cli releases files $VERSION upload-sourcemaps ./build --rewrite
sentry-cli releases finalize $VERSION

echo ""
echo "✅ Build completo!"
echo "   Versão: $VERSION"
echo "   Source maps enviados para o Sentry"
echo ""
echo "📁 Arquivos em: ./build"