#!/bin/bash

# Script para criar releases no Sentry com source maps
# Uso: ./release.sh [version]

echo "🚀 Sentry Release Management Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Obter versão
if [ -z "$1" ]; then
    # Se não passou versão, usar do package.json
    VERSION=$(node -p "require('./package.json').version")
else
    VERSION=$1
fi

RELEASE_NAME="coflow@$VERSION"
BUILD_ID=$(date +%s)

echo "📌 Release: $RELEASE_NAME"
echo "🏷️  Build ID: $BUILD_ID"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ]; then
    echo "❌ Erro: package.json não encontrado"
    exit 1
fi

# Criar build com variáveis de ambiente
echo "📦 Criando build de produção..."
REACT_APP_VERSION=$VERSION \
REACT_APP_BUILD_ID=$BUILD_ID \
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Erro no build"
    exit 1
fi

# Criar novo release no Sentry
echo ""
echo "📤 Criando release no Sentry..."
sentry-cli releases new $RELEASE_NAME

# Upload de source maps
echo "📤 Enviando source maps..."
sentry-cli releases files $RELEASE_NAME upload-sourcemaps ./build/static/js \
  --url-prefix "~/static/js" \
  --rewrite \
  --validate

# Associar commits (se estiver em um repositório git)
if [ -d ".git" ]; then
    echo "🔗 Associando commits..."
    sentry-cli releases set-commits $RELEASE_NAME --auto
fi

# Finalizar release
echo "✅ Finalizando release..."
sentry-cli releases finalize $RELEASE_NAME

# Deploy em ambiente (opcional)
if [ "$2" = "--deploy" ]; then
    ENVIRONMENT=${3:-"production"}
    echo "🌍 Marcando deploy em $ENVIRONMENT..."
    sentry-cli releases deploys $RELEASE_NAME new -e $ENVIRONMENT
fi

echo ""
echo "✅ Release criado com sucesso!"
echo "   Version: $RELEASE_NAME"
echo "   Build ID: $BUILD_ID"
echo ""
echo "📊 Visualizar em: https://coflow.sentry.io/releases/$RELEASE_NAME"
echo ""

# Criar arquivo de versão para referência
echo "{
  \"release\": \"$RELEASE_NAME\",
  \"version\": \"$VERSION\",
  \"buildId\": \"$BUILD_ID\",
  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"
}" > build/version.json

echo "📝 Arquivo version.json criado em build/"