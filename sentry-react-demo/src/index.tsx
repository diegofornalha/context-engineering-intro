import React from 'react';
import ReactDOM from 'react-dom/client';
import * as Sentry from '@sentry/react';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { initSentry } from './sentry';

// Inicializar Sentry antes de renderizar
initSentry();

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Sentry.ErrorBoundary fallback={ErrorFallback} showDialog>
      <App />
    </Sentry.ErrorBoundary>
  </React.StrictMode>
);

function ErrorFallback({ error, resetError }: { error: unknown; resetError: () => void }) {
  return (
    <div role="alert" style={{ padding: '20px', textAlign: 'center' }}>
      <h2>Oops! Algo deu errado</h2>
      <pre style={{ color: 'red' }}>
        {error instanceof Error ? error.message : 'Erro desconhecido'}
      </pre>
      <button onClick={resetError}>Tentar Novamente</button>
    </div>
  );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
