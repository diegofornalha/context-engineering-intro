import React from 'react';
import * as Sentry from '@sentry/react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [crashCount, setCrashCount] = React.useState(0);

  const handleTestError = () => {
    setCrashCount(prev => prev + 1);
    throw new Error("This is your first error!");
  };

  const handleTestMessage = () => {
    Sentry.captureMessage("Test message from React app", "info");
    alert("Mensagem enviada para o Sentry!");
  };

  const handleTestTransaction = async () => {
    await Sentry.startSpan(
      { name: "test-api-call", op: "http.client" },
      async () => {
        // Simular chamada de API
        await new Promise(resolve => setTimeout(resolve, 1000));
        alert("Transação registrada no Sentry!");
      }
    );
  };

  const handleAbnormalSession = () => {
    Sentry.captureMessage("Session will end abnormally", "warning");
    setTimeout(() => {
      window.location.reload();
    }, 1000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>Sentry React Demo</h1>
        <p>Projeto: coflow | DSN configurado</p>
        
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
          <button 
            onClick={handleTestError}
            style={{
              padding: '10px 20px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
            }}
          >
            Break the world 💥
          </button>
          
          <button 
            onClick={handleTestMessage}
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
            }}
          >
            Send Test Message 📨
          </button>
          
          <button 
            onClick={handleTestTransaction}
            style={{
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
            }}
          >
            Test Performance 📊
          </button>
          
          <button 
            onClick={handleAbnormalSession}
            style={{
              padding: '10px 20px',
              backgroundColor: '#ffc107',
              color: 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
            }}
          >
            Abnormal Session ⚠️
          </button>
        </div>
        
        <p style={{ marginTop: '20px', fontSize: '14px' }}>
          Crashes nesta sessão: {crashCount}
        </p>
        
        <a
          className="App-link"
          href="https://coflow.sentry.io"
          target="_blank"
          rel="noopener noreferrer"
        >
          Ver no Dashboard do Sentry
        </a>
      </header>
    </div>
  );
}

export default App;