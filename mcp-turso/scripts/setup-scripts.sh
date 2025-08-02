#!/bin/bash

# Script de Setup dos Scripts MCP Turso
# Configura e testa todos os scripts de sincronização

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    error "Execute este script de dentro da pasta mcp-turso/scripts/"
    exit 1
fi

echo "🚀 Setup dos Scripts MCP Turso"
echo "================================"

# 1. Verificar dependências
log "1. Verificando dependências..."

# Verificar Python
if command -v python3 &> /dev/null; then
    success "Python3 encontrado: $(python3 --version)"
else
    error "Python3 não encontrado"
    exit 1
fi

# Verificar permissões
log "2. Configurando permissões..."
chmod +x *.sh
success "Permissões configuradas"

# 3. Testar scripts individuais
log "3. Testando scripts..."

# Testar scan de conhecimento
echo ""
log "Testando scan de conhecimento..."
python3 sync-knowledge-via-mcp.py
if [ $? -eq 0 ]; then
    success "Scan de conhecimento funcionando"
else
    error "Erro no scan de conhecimento"
fi

# Testar integrador MCP
echo ""
log "Testando integrador MCP..."
python3 integrate-with-mcp.py
if [ $? -eq 0 ]; then
    success "Integrador MCP funcionando"
else
    error "Erro no integrador MCP"
fi

# 4. Criar diretório de logs
log "4. Criando estrutura de logs..."
mkdir -p ../logs
success "Diretório de logs criado"

# 5. Testar automação
log "5. Testando automação..."
./auto-sync-knowledge.sh status
if [ $? -eq 0 ]; then
    success "Automação funcionando"
else
    error "Erro na automação"
fi

# 6. Criar arquivo de configuração
log "6. Criando arquivo de configuração..."
cat > config.json << 'EOF'
{
  "sync": {
    "enabled": true,
    "interval_hours": 6,
    "max_files_per_batch": 10,
    "log_level": "info"
  },
  "mcp": {
    "database": "context-memory",
    "table": "turso_agent_knowledge",
    "timeout_seconds": 30
  },
  "paths": {
    "docs_turso": "../../docs-turso",
    "logs": "../logs",
    "reports": "."
  }
}
EOF
success "Arquivo de configuração criado"

# 7. Criar script de execução rápida
log "7. Criando script de execução rápida..."
cat > quick-sync.sh << 'EOF'
#!/bin/bash
# Script de execução rápida para sincronização

echo "🔄 Executando sincronização rápida..."

# Executar scan
python3 sync-knowledge-via-mcp.py

# Executar integrador
python3 integrate-with-mcp.py

echo "✅ Sincronização rápida concluída!"
EOF

chmod +x quick-sync.sh
success "Script de execução rápida criado"

# 8. Mostrar resumo
echo ""
echo "📊 RESUMO DO SETUP"
echo "=================="
echo "✅ Dependências verificadas"
echo "✅ Permissões configuradas"
echo "✅ Scripts testados"
echo "✅ Estrutura de logs criada"
echo "✅ Automação configurada"
echo "✅ Configuração salva"
echo "✅ Script de execução rápida criado"

echo ""
echo "🚀 SCRIPTS DISPONÍVEIS:"
echo "========================"
echo "• python3 sync-knowledge-via-mcp.py    # Scan de conhecimento"
echo "• python3 integrate-with-mcp.py        # Integração com MCP"
echo "• ./auto-sync-knowledge.sh auto        # Automação"
echo "• ./quick-sync.sh                      # Execução rápida"

echo ""
echo "📋 COMANDOS ÚTEIS:"
echo "=================="
echo "• ./auto-sync-knowledge.sh status      # Ver status"
echo "• ./auto-sync-knowledge.sh integrity   # Verificar integridade"
echo "• ./auto-sync-knowledge.sh cleanup     # Limpar logs"

echo ""
success "Setup concluído com sucesso!"
echo ""
echo "💡 PRÓXIMOS PASSOS:"
echo "1. Configure o MCP Turso no Cursor/Claude"
echo "2. Execute: ./quick-sync.sh"
echo "3. Configure automação: ./auto-sync-knowledge.sh auto"
echo "4. Monitore logs em: ../logs/" 