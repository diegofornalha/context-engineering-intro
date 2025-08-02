# Integração do Sentry com React

## Instalação e Configuração Básica

```jsx
import React from "react";
import ReactDOM from "react-dom/client";
import * as Sentry from "@sentry/react";
import App from "./App";

// Configuração do Sentry com Performance Monitoring
Sentry.init({
  dsn: "https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334",
  
  // Integração para rastreamento de performance
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration({
      maskAllText: false,
      blockAllMedia: false,
    }),
  ],

  // Release Health - importante para monitorar saúde dos releases
  release: "myapp@1.0.0",
  environment: process.env.NODE_ENV,

  // Performance Monitoring
  tracesSampleRate: 1.0, // Ajustar para produção (ex: 0.1 para 10%)
  
  // Session Replay
  replaysSessionSampleRate: 0.1, // 10% das sessões
  replaysOnErrorSampleRate: 1.0, // 100% quando há erro

  // Distributed Tracing
  tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
  
  // Configuração de sessão para Release Health
  autoSessionTracking: true, // Rastreia sessões automaticamente
  
  beforeSend(event) {
    // Filtrar informações sensíveis
    if (event.user) {
      delete event.user.email;
    }
    return event;
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## Componente com Error Boundary e Testes

```jsx
import React from 'react';
import * as Sentry from '@sentry/react';

// Error Boundary customizado para melhor UX
const CustomErrorFallback = ({ error, resetError }) => (
  <div style={{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    padding: '20px',
    textAlign: 'center',
  }}>
    <h1>Oops! Algo deu errado</h1>
    <p style={{ color: '#666', marginBottom: '20px' }}>
      {error.message}
    </p>
    <button
      onClick={resetError}
      style={{
        padding: '10px 20px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
      }}
    >
      Tentar Novamente
    </button>
  </div>
);

// Componente principal com monitoramento
function App() {
  return (
    <Sentry.ErrorBoundary 
      fallback={CustomErrorFallback} 
      showDialog={true}
      onError={(error, errorInfo) => {
        // Log adicional ou ações customizadas
        console.error('ErrorBoundary caught:', error, errorInfo);
      }}
    >
      <div className="App">
        <h1>Minha Aplicação React com Sentry</h1>
        
        {/* Componente de teste para Release Health */}
        <ReleaseHealthDemo />
        
        {/* Performance Monitoring */}
        <PerformanceDemo />
      </div>
    </Sentry.ErrorBoundary>
  );
}

// Componente para testar Release Health
function ReleaseHealthDemo() {
  const handleTestError = () => {
    throw new Error("This is your first error!");
  };

  const handleTestMessage = () => {
    Sentry.captureMessage("Test message from React app", "info");
  };

  const handleAbnormalSession = () => {
    // Simula uma sessão anormal
    Sentry.captureMessage("Session will end abnormally", "warning");
    setTimeout(() => {
      window.location.reload(); // Força reload (sessão anormal)
    }, 1000);
  };

  return (
    <div style={{ margin: '20px', padding: '20px', border: '1px solid #ddd' }}>
      <h2>Release Health Testing</h2>
      
      <button 
        onClick={handleTestError}
        style={{
          margin: '5px',
          padding: '10px 20px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Break the world (Crash Session)
      </button>
      
      <button 
        onClick={handleTestMessage}
        style={{
          margin: '5px',
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Send Test Message
      </button>
      
      <button 
        onClick={handleAbnormalSession}
        style={{
          margin: '5px',
          padding: '10px 20px',
          backgroundColor: '#ffc107',
          color: 'black',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Trigger Abnormal Session
      </button>
    </div>
  );
}

// Componente para testar Performance Monitoring
function PerformanceDemo() {
  const [loading, setLoading] = React.useState(false);
  const [data, setData] = React.useState(null);

  const fetchData = async () => {
    // Cria uma transação para monitorar performance
    const transaction = Sentry.startSpan(
      { name: "fetch-api-data", op: "http.client" },
      async () => {
        setLoading(true);
        
        try {
          // Simula chamada à API
          const response = await fetch('https://api.example.com/data');
          const result = await response.json();
          setData(result);
          
          // Adiciona breadcrumb para debugging
          Sentry.addBreadcrumb({
            message: 'API data fetched successfully',
            category: 'api',
            level: 'info',
            data: { itemCount: result.length },
          });
        } catch (error) {
          Sentry.captureException(error);
          throw error;
        } finally {
          setLoading(false);
        }
      }
    );
  };

  return (
    <div style={{ margin: '20px', padding: '20px', border: '1px solid #ddd' }}>
      <h2>Performance Monitoring</h2>
      
      <button 
        onClick={fetchData}
        disabled={loading}
        style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
          opacity: loading ? 0.6 : 1,
        }}
      >
        {loading ? 'Loading...' : 'Fetch Data (with Performance Tracking)'}
      </button>
      
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}

export default App;
```

## Configuração Avançada para Release Health

```jsx
// utils/sentry.js
import * as Sentry from '@sentry/react';

// Configuração customizada para diferentes ambientes
export const configureSentry = () => {
  const environment = process.env.REACT_APP_ENV || 'development';
  const release = process.env.REACT_APP_VERSION || 'unknown';
  
  Sentry.init({
    dsn: process.env.REACT_APP_SENTRY_DSN,
    environment,
    release: `myapp@${release}`,
    
    // Configurações específicas por ambiente
    tracesSampleRate: environment === 'production' ? 0.1 : 1.0,
    
    // Session tracking para Release Health
    autoSessionTracking: true,
    sessionTrackingIntervalMillis: 30000, // 30 segundos
    
    // Integrations
    integrations: [
      Sentry.browserTracingIntegration(),
      Sentry.replayIntegration({
        maskAllText: environment === 'production',
        blockAllMedia: environment === 'production',
      }),
    ],
    
    // Hooks para customização
    beforeSend(event, hint) {
      // Adiciona contexto de release health
      if (event.contexts) {
        event.contexts.releaseHealth = {
          sessionCount: getSessionCount(),
          crashFreeRate: getCrashFreeRate(),
        };
      }
      return event;
    },
  });
};

// Helpers para Release Health
function getSessionCount() {
  return parseInt(localStorage.getItem('session_count') || '0');
}

function getCrashFreeRate() {
  const sessions = getSessionCount();
  const crashes = parseInt(localStorage.getItem('crash_count') || '0');
  return sessions > 0 ? ((sessions - crashes) / sessions * 100).toFixed(2) : 100;
}

// Hook para rastrear sessões
export function useSessionTracking() {
  React.useEffect(() => {
    // Incrementa contador de sessão
    const count = getSessionCount() + 1;
    localStorage.setItem('session_count', count.toString());
    
    // Configura usuário para melhor tracking
    Sentry.setUser({
      id: getUserId(),
      username: getUsername(),
    });
    
    // Cleanup ao desmontar
    return () => {
      // Sessão termina normalmente
      Sentry.endSession();
    };
  }, []);
}

// Contexto para gerenciar Release Health
export const ReleaseHealthContext = React.createContext();

export function ReleaseHealthProvider({ children }) {
  const [sessionStatus, setSessionStatus] = React.useState('healthy');
  
  const markSessionAsErrored = () => {
    setSessionStatus('errored');
    Sentry.captureMessage('Session marked as errored', 'warning');
  };
  
  const markSessionAsCrashed = () => {
    setSessionStatus('crashed');
    const crashes = parseInt(localStorage.getItem('crash_count') || '0') + 1;
    localStorage.setItem('crash_count', crashes.toString());
    Sentry.captureException(new Error('Session crashed'));
  };
  
  return (
    <ReleaseHealthContext.Provider value={{
      sessionStatus,
      markSessionAsErrored,
      markSessionAsCrashed,
    }}>
      {children}
    </ReleaseHealthContext.Provider>
  );
}
```

## Scripts para Build com Release Tracking

```json
// package.json
{
  "scripts": {
    "build": "REACT_APP_VERSION=$(git describe --tags --always) react-scripts build",
    "build:sentry": "npm run build && npm run sentry:upload",
    "sentry:upload": "sentry-cli releases files $REACT_APP_VERSION upload-sourcemaps ./build"
  }
}
```

## Configuração do Sentry CLI

```bash
# .sentryclirc
[defaults]
url=https://sentry.io/
org=your-org
project=your-project

[auth]
token=your-auth-token
```

Este exemplo mostra uma integração completa do Sentry com React incluindo:
- ✅ Release Health monitoring
- ✅ Performance monitoring
- ✅ Session tracking
- ✅ Error boundaries customizados
- ✅ Distributed tracing
- ✅ Session replay
- ✅ Contexto de usuário
- ✅ Build scripts com versionamento