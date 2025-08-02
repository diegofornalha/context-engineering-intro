# 🤖 PRP Agent - FastAPI + Sentry

Aplicação FastAPI com monitoramento Sentry integrado para processamento de Product Requirement Prompts.

## 🚀 Uso Rápido

### Script Principal (Recomendado)
```bash
./prp-agent.sh
```
Menu interativo com todas as opções de gerenciamento.

### Scripts Individuais
```bash
./start.sh      # Iniciar servidor
./stop.sh       # Parar servidor  
./restart.sh    # Reiniciar
./status.sh     # Ver status
./logs.sh       # Ver logs
./test.sh       # Executar testes
```

## 📊 Endpoints

| Endpoint | Descrição |
|----------|-----------|
| `GET /` | Status da aplicação |
| `GET /sentry-debug` | Teste de erro (Sentry) |

## 🔧 Configuração

### Ambiente UV
```bash
# Já configurado! Mas se precisar recriar:
uv init --no-readme
uv add "sentry-sdk[fastapi]" fastapi uvicorn pydantic python-dotenv loguru
```

### Sentry DSN
Arquivo `.env`:
```env
SENTRY_DSN=https://d9fe4e8016424adebb7389d5df925764@o927801.ingest.us.sentry.io/4509774227832832
```

## 🧪 Testes

Execute testes automatizados:
```bash
./test.sh
```

Teste manual do Sentry:
```bash
curl http://localhost:8000/sentry-debug
```

## 📊 Monitoramento

### Sentry Dashboard
- **URL**: https://sentry.io/organizations/coflow/projects/
- **Buscar**: ZeroDivisionError, performance transactions
- **Issues**: Erros capturados automaticamente  
- **Performance**: Transações HTTP monitoradas

### Logs Locais
```bash
./logs.sh                    # Menu de opções
tail -f prp-agent.log       # Tempo real
grep ERROR prp-agent.log    # Filtrar erros
```

## 🔄 Modos de Execução

### Foreground (Desenvolvimento)
```bash
./start.sh
# Escolha opção 1
# Logs visíveis, Ctrl+C para parar
```

### Background (Produção)
```bash
./start.sh  
# Escolha opção 2
# Execução em daemon, use ./stop.sh para parar
```

## 📁 Estrutura

```
prp-agent/
├── main.py              # 🐍 Aplicação FastAPI
├── prp-agent.sh         # 🎯 Script principal
├── start.sh             # 🚀 Iniciar
├── stop.sh              # 🛑 Parar  
├── restart.sh           # 🔄 Reiniciar
├── status.sh            # 📊 Status
├── logs.sh              # 📄 Logs
├── test.sh              # 🧪 Testes
├── .env                 # 🔐 Configuração
├── pyproject.toml       # 📦 Dependências UV
├── .venv/               # 🐍 Ambiente virtual
└── prp-agent.log        # 📄 Logs (quando em background)
```

## 🆘 Solução de Problemas

### Servidor não inicia
```bash
# Verificar porta ocupada
lsof -i :8000

# Parar processo
./stop.sh

# Verificar ambiente
./status.sh
```

### Imports falhando
```bash
# Ativar ambiente UV
source .venv/bin/activate

# Verificar dependências  
uv list
```

### Sentry não funciona
```bash
# Verificar DSN
cat .env

# Testar conectividade
curl http://localhost:8000/sentry-debug

# Verificar logs
./logs.sh
```

## 🎯 Próximos Passos

1. **Testar Sentry Dashboard**
   - Execute `./test.sh`
   - Acesse dashboard Sentry
   - Verifique erros e performance

2. **Integrar PydanticAI**
   - Adicionar agents reais
   - Conectar LLM models
   - Implementar tools MCP

3. **Deploy Produção**
   - Configurar reverse proxy
   - SSL/HTTPS
   - Monitoring avançado

---

## 💡 Comandos Úteis

```bash
# Acesso rápido - execute de qualquer lugar
cd prp-agent && ./prp-agent.sh

# Background rápido
cd prp-agent && ./start.sh  # opção 2

# Status rápido
cd prp-agent && ./status.sh

# Parar rápido  
cd prp-agent && ./stop.sh
```

🎉 **PRP Agent está pronto para uso!**