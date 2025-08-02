#!/bin/bash

# Script de configuração do Sentry para projetos Coflow
# Este script automatiza a instalação e configuração do Sentry

echo "🚀 Configurando Sentry para Coflow..."

# Instalar Sentry CLI globalmente
echo "📦 Instalando Sentry CLI..."
npm install -g @sentry/cli

# Verificar se está em um projeto React
if [ -f "package.json" ]; then
    echo "✅ Projeto React detectado"
    
    # Instalar dependências do Sentry
    echo "📦 Instalando @sentry/react..."
    npm install --save @sentry/react
    
    # Criar arquivo .sentryclirc
    cat > .sentryclirc << EOF
[defaults]
url=https://sentry.io/
org=coflow
project=$1

[auth]
token=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
EOF
    
    echo "✅ Arquivo .sentryclirc criado"
    
    # Adicionar scripts ao package.json
    echo "📝 Atualizando package.json com scripts do Sentry..."
    npx json -I -f package.json -e 'this.scripts["sentry:releases"] = "sentry-cli releases"'
    npx json -I -f package.json -e 'this.scripts["sentry:sourcemaps"] = "sentry-cli releases files $npm_package_version upload-sourcemaps ./build"'
    
    # Criar arquivo de configuração do Sentry
    echo "📝 Criando arquivo de configuração do Sentry..."
    cat > src/sentry.js << 'EOF'
import * as Sentry from "@sentry/react";

export function initSentry() {
  Sentry.init({
    dsn: process.env.REACT_APP_SENTRY_DSN,
    integrations: [
      Sentry.browserTracingIntegration(),
      Sentry.replayIntegration({
        maskAllText: false,
        blockAllMedia: false,
      }),
    ],
    
    // Performance Monitoring
    tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
    
    // Session Replay
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
    
    // Release tracking
    release: process.env.REACT_APP_VERSION || "unknown",
    environment: process.env.NODE_ENV,
    
    // Debug mode
    debug: process.env.NODE_ENV === "development",
    
    beforeSend(event, hint) {
      // Filtrar erros em desenvolvimento se necessário
      if (process.env.NODE_ENV === "development") {
        console.log("Sentry Event:", event);
      }
      return event;
    },
  });
}
EOF
    
    echo "✅ Arquivo de configuração criado em src/sentry.js"
    
    # Criar exemplo de variáveis de ambiente
    echo "📝 Criando arquivo .env.example..."
    cat > .env.example << EOF
# Sentry Configuration
REACT_APP_SENTRY_DSN=your-dsn-here
REACT_APP_VERSION=1.0.0
EOF
    
    echo "✅ Arquivo .env.example criado"
    
    # Instruções finais
    echo ""
    echo "🎉 Configuração concluída!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Obtenha seu DSN no dashboard do Sentry"
    echo "2. Adicione o DSN ao arquivo .env"
    echo "3. Importe e chame initSentry() no seu index.js:"
    echo "   import { initSentry } from './sentry';"
    echo "   initSentry();"
    echo "4. Use o Error Boundary do Sentry em App.js"
    echo ""
    echo "🔗 Dashboard Sentry: https://coflow.sentry.io"
    echo ""
    
else
    echo "❌ Erro: package.json não encontrado"
    echo "Por favor, execute este script na raiz do seu projeto React"
    exit 1
fi

# Verificar se foi passado o nome do projeto
if [ -z "$1" ]; then
    echo ""
    echo "⚠️  Atenção: Nome do projeto não especificado"
    echo "Use: ./setup-sentry-coflow.sh nome-do-projeto"
fi