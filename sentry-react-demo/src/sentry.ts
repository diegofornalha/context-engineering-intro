import * as Sentry from "@sentry/react";

// Obter versão do package.json ou usar timestamp
const getAppVersion = () => {
  const version = process.env.REACT_APP_VERSION || 
                  process.env.npm_package_version || 
                  `1.0.0-dev.${Date.now()}`;
  return `coflow@${version}`;
};

export function initSentry() {
  Sentry.init({
    dsn: "https://782bbb46ddaa4e64a9a705e64f513985@o927801.ingest.us.sentry.io/5877334",
    
    // Integrations
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
    replaysSessionSampleRate: 0.1, // 10% das sessões
    replaysOnErrorSampleRate: 1.0, // 100% quando há erro
    
    // Release tracking - IMPORTANTE para Release Health
    release: getAppVersion(),
    environment: process.env.NODE_ENV || "development",
    dist: process.env.REACT_APP_BUILD_ID || undefined,
    
    // Session tracking é habilitado por padrão no browser
    // Isso é essencial para Release Health funcionar
    
    // Debug mode
    debug: process.env.NODE_ENV === "development",
    
    // Envia dados PII (endereço IP, etc) para melhor contexto
    sendDefaultPii: true,
    
    // Tags padrão para todos os eventos
    initialScope: {
      tags: {
        component: "frontend",
        project: "coflow",
      },
      user: {
        id: localStorage.getItem("userId") || `anon-${Math.random().toString(36).substr(2, 9)}`,
      },
    },
    
    beforeSend(event, hint) {
      // Adicionar release info em todos os eventos
      if (!event.release) {
        event.release = getAppVersion();
      }
      
      // Log em desenvolvimento
      if (process.env.NODE_ENV === "development") {
        console.log("📊 Sentry Event:", {
          type: event.type,
          release: event.release,
          environment: event.environment,
          error: hint.originalException,
        });
      }
      
      return event;
    },
    
    // Callback quando sessão inicia
    beforeSendSession(session) {
      console.log("📊 Session started:", session);
      return session;
    },
  });
  
  // Salvar userId no localStorage para persistir entre sessões
  const userId = localStorage.getItem("userId");
  if (!userId) {
    const newUserId = `user-${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem("userId", newUserId);
    Sentry.setUser({ id: newUserId });
  }
}