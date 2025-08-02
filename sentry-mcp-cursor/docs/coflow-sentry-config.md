# Configuração do Sentry para Projetos Coflow

## 🔐 Informações da Conta

- **Organização**: coflow
- **URL do Dashboard**: https://coflow.sentry.io
- **Region**: US (us.sentry.io)
- **Auth Token**: Configurado no `.sentryclirc`

## 🚀 Setup Rápido

### 1. Usando o Script Automatizado

```bash
# Baixar e executar o script de setup
curl -O https://raw.githubusercontent.com/your-repo/setup-sentry-coflow.sh
chmod +x setup-sentry-coflow.sh
./setup-sentry-coflow.sh nome-do-seu-projeto
```

### 2. Configuração Manual

#### Instalar Dependências

```bash
npm install --save @sentry/react
npm install -g @sentry/cli
```

#### Criar `.sentryclirc`

```ini
[defaults]
url=https://sentry.io/
org=coflow
project=seu-projeto

[auth]
token=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
```

#### Configurar Sentry no React

```jsx
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import * as Sentry from '@sentry/react';
import App from './App';

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  
  // Performance Monitoring
  tracesSampleRate: 1.0,
  
  // Session Replay
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  // Release & Environment
  release: process.env.REACT_APP_VERSION,
  environment: process.env.NODE_ENV,
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Sentry.ErrorBoundary fallback={ErrorFallback} showDialog>
      <App />
    </Sentry.ErrorBoundary>
  </React.StrictMode>
);

function ErrorFallback({ error }) {
  return (
    <div role="alert">
      <h2>Algo deu errado:</h2>
      <pre>{error.message}</pre>
    </div>
  );
}
```

## 📊 Recursos Disponíveis

### 1. Error Tracking
- Captura automática de erros JavaScript
- Stack traces com source maps
- Contexto de usuário e breadcrumbs

### 2. Performance Monitoring
- Rastreamento de transações
- Web Vitals (LCP, FID, CLS)
- Slow query detection

### 3. Session Replay
- Gravação de sessões de usuário
- Replay de erros
- Privacidade com masking

### 4. Release Health
- Crash free rate
- Session tracking
- Adoption metrics

## 🛠️ Comandos Úteis do Sentry CLI

```bash
# Listar projetos
sentry-cli projects list

# Criar novo release
sentry-cli releases new v1.0.0

# Upload de source maps
sentry-cli releases files v1.0.0 upload-sourcemaps ./build

# Finalizar release
sentry-cli releases finalize v1.0.0

# Associar commits ao release
sentry-cli releases set-commits v1.0.0 --auto
```

## 📝 Variáveis de Ambiente

```env
# .env.production
REACT_APP_SENTRY_DSN=https://your-key@o927801.ingest.us.sentry.io/your-project-id
REACT_APP_VERSION=1.0.0
REACT_APP_SENTRY_ENVIRONMENT=production

# .env.development
REACT_APP_SENTRY_DSN=https://your-key@o927801.ingest.us.sentry.io/your-project-id
REACT_APP_VERSION=dev
REACT_APP_SENTRY_ENVIRONMENT=development
```

## 🔧 Integração com CI/CD

### GitHub Actions

```yaml
name: Deploy with Sentry
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build
        run: |
          npm ci
          npm run build
        env:
          REACT_APP_VERSION: ${{ github.sha }}
          
      - name: Create Sentry release
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          SENTRY_ORG: coflow
          SENTRY_PROJECT: ${{ secrets.SENTRY_PROJECT }}
        run: |
          # Install sentry-cli
          npm install -g @sentry/cli
          
          # Create new release
          sentry-cli releases new ${{ github.sha }}
          
          # Upload source maps
          sentry-cli releases files ${{ github.sha }} upload-sourcemaps ./build
          
          # Set commits
          sentry-cli releases set-commits ${{ github.sha }} --auto
          
          # Finalize release
          sentry-cli releases finalize ${{ github.sha }}
```

## 🎯 Best Practices

1. **Use Release Tracking**: Sempre defina a versão do release
2. **Configure Source Maps**: Para stack traces legíveis
3. **Set User Context**: Para melhor debugging
4. **Use Breadcrumbs**: Para entender o fluxo do usuário
5. **Filter Sensitive Data**: Use beforeSend hook
6. **Monitor Performance**: Ative tracing para métricas
7. **Test in Development**: Mas filtre erros desnecessários

## 🔗 Links Úteis

- [Dashboard Coflow](https://coflow.sentry.io)
- [Documentação Sentry React](https://docs.sentry.io/platforms/javascript/guides/react/)
- [Sentry CLI Docs](https://docs.sentry.io/product/cli/)
- [Performance Monitoring](https://docs.sentry.io/product/performance/)
- [Session Replay](https://docs.sentry.io/product/session-replay/)