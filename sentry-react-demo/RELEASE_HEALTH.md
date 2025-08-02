# 📊 Guia Completo: Release Health & Releases no Sentry

## 🎯 O que está configurado

### 1. **Release Health Tracking**
- ✅ Session tracking automático
- ✅ User ID persistente (localStorage)
- ✅ Crash detection
- ✅ Release version tracking
- ✅ Environment separation

### 2. **Source Maps**
- ✅ Upload automático no build
- ✅ Validação de source maps
- ✅ URL prefix configurado

### 3. **Versionamento Semântico**
- ✅ Scripts npm para patch/minor/major
- ✅ Release naming: `coflow@version`
- ✅ Build ID tracking

## 🚀 Como criar um Release

### Opção 1: Release Manual
```bash
# Criar release com versão atual
./release.sh

# Criar release com versão específica
./release.sh 1.2.0

# Criar release e marcar deploy
./release.sh 1.2.0 --deploy production
```

### Opção 2: Release com Versionamento
```bash
# Patch release (0.1.0 -> 0.1.1)
npm run release:patch

# Minor release (0.1.1 -> 0.2.0)
npm run release:minor

# Major release (0.2.0 -> 1.0.0)
npm run release:major
```

### Opção 3: CI/CD Automático
```bash
# Criar tag e fazer push
git tag v1.0.0
git push origin v1.0.0

# Ou push para main (cria release de desenvolvimento)
git push origin main
```

## 📈 Métricas de Release Health

### O que é rastreado:
1. **Sessions**
   - Total de sessões
   - Duração das sessões
   - Sessões por usuário

2. **Crashes**
   - Taxa de crash-free sessions
   - Taxa de crash-free users
   - Crashes por release

3. **Adoption**
   - % de usuários usando cada release
   - Velocidade de adoção
   - Comparação entre releases

4. **Session Status**
   - Healthy: Sessão normal sem erros
   - Errored: Sessão com erros tratados
   - Crashed: Sessão terminada com crash
   - Abnormal: Sessão terminada anormalmente

## 🔍 Visualizando no Dashboard

### 1. **Página de Releases**
URL: https://coflow.sentry.io/releases/

Você verá:
- Lista de todos os releases
- % de crash-free sessions/users
- Adoption rate
- Número de issues por release

### 2. **Release Details**
Clique em um release para ver:
- Gráfico de adoption ao longo do tempo
- Issues introduzidas neste release
- Commits associados
- Session data detalhada

### 3. **Filtros Úteis**
- `error.unhandled:true` - Ver apenas crashes
- `release:coflow@1.0.0` - Filtrar por release
- `environment:production` - Filtrar por ambiente

## 🎮 Testando Release Health

### 1. Iniciar o app
```bash
./dev.sh
```

### 2. Simular cenários:

**Session Healthy:**
- Use o app normalmente
- Navegue entre páginas
- Sessão será marcada como "healthy"

**Session Crashed:**
- Clique em "Break the world 💥"
- Sessão será marcada como "crashed"
- Afeta crash-free rate

**Session Errored:**
- Capture erros tratados
- Sessão continua mas é marcada como "errored"

**Session Abnormal:**
- Clique em "Abnormal Session ⚠️"
- Force quit o browser
- Sessão marcada como "abnormal"

### 3. Ver resultados:
- Aguarde ~1 minuto para processamento
- Acesse: https://coflow.sentry.io/releases/
- Veja as métricas atualizadas

## 📊 Exemplo de Fluxo Completo

```bash
# 1. Fazer alterações no código
git add .
git commit -m "feat: adicionar nova funcionalidade"

# 2. Criar release
npm run release:minor
# Isso vai:
# - Incrementar versão no package.json
# - Criar build de produção
# - Upload source maps para Sentry
# - Associar commits
# - Finalizar release

# 3. Deploy (simulado)
./release.sh $(node -p "require('./package.json').version") --deploy production

# 4. Monitorar
# - Abrir https://coflow.sentry.io/releases/
# - Ver adoption crescendo
# - Monitorar crash-free rate
# - Identificar issues por release
```

## 🔔 Alertas Recomendados

Configure alertas para:
1. **Crash Rate Alert**
   - Quando crash-free rate < 95%
   - Por release ou global

2. **New Issue Alert**
   - Issues introduzidas em novo release
   - Regressões

3. **Adoption Alert**
   - Quando adoption > 50%
   - Para saber quando maioria migrou

## 🛠️ Troubleshooting

### Source maps não funcionam?
```bash
# Verificar se foram enviados
sentry-cli releases files coflow@VERSION list

# Re-enviar manualmente
npm run sentry:upload
```

### Release não aparece?
- Verificar DSN correto
- Verificar se release foi finalizado
- Aguardar 1-2 minutos para processamento

### Sessions não são rastreadas?
- Verificar se `sendDefaultPii: true`
- Verificar console por logs de sessão
- User ID deve persistir entre reloads

## 📝 Próximos Passos

1. **Configurar alertas** no dashboard
2. **Integrar com GitHub** para melhor tracking de commits
3. **Adicionar custom tags** para segmentação
4. **Configurar environments** (staging, production)
5. **Implementar A/B testing** com releases

---

**Documentação Sentry**: https://docs.sentry.io/product/releases/
**Dashboard**: https://coflow.sentry.io