#!/bin/bash

# Script de Automação de Sincronização de Conhecimento Turso Agent
# Executa sync automático e mantém conhecimento atualizado

set -e

# Configurações
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SYNC_SCRIPT="$SCRIPT_DIR/sync-turso-knowledge.py"
LOG_DIR="$PROJECT_ROOT/logs"
LOCK_FILE="$LOG_DIR/sync.lock"
LAST_SYNC_FILE="$LOG_DIR/last_sync.txt"

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

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Criar diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Verificar se já está rodando
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        error "Sync já está rodando (PID: $PID)"
        exit 1
    else
        warning "Lock file encontrado mas processo não está rodando. Removendo..."
        rm -f "$LOCK_FILE"
    fi
fi

# Criar lock file
echo $$ > "$LOCK_FILE"

# Função de cleanup
cleanup() {
    log "Limpando arquivos temporários..."
    rm -f "$LOCK_FILE"
    log "Cleanup concluído"
}

# Trap para garantir cleanup
trap cleanup EXIT

# Verificar se deve executar sync
should_sync() {
    if [ ! -f "$LAST_SYNC_FILE" ]; then
        return 0  # Primeira execução
    fi
    
    last_sync=$(cat "$LAST_SYNC_FILE")
    current_time=$(date +%s)
    time_diff=$((current_time - last_sync))
    
    # Sync a cada 6 horas (21600 segundos)
    if [ $time_diff -gt 21600 ]; then
        return 0
    else
        return 1
    fi
}

# Função principal de sync
run_sync() {
    log "🔄 Iniciando sincronização automática de conhecimento..."
    
    # Verificar se arquivo Python existe
    if [ ! -f "$SYNC_SCRIPT" ]; then
        error "Script de sync não encontrado: $SYNC_SCRIPT"
        exit 1
    fi
    
    # Verificar se Python está disponível
    if ! command -v python3 &> /dev/null; then
        error "Python3 não encontrado"
        exit 1
    fi
    
    # Executar sync
    log "📁 Executando sync de conhecimento..."
    cd "$PROJECT_ROOT"
    
    # Executar com timeout de 10 minutos
    timeout 600 python3 "$SYNC_SCRIPT" 2>&1 | tee "$LOG_DIR/sync_$(date +%Y%m%d_%H%M%S).log"
    
    if [ $? -eq 0 ]; then
        success "Sincronização concluída com sucesso!"
        echo $(date +%s) > "$LAST_SYNC_FILE"
    else
        error "Erro durante sincronização"
        exit 1
    fi
}

# Função para verificar integridade
check_integrity() {
    log "🔍 Verificando integridade do conhecimento..."
    
    cd "$PROJECT_ROOT"
    python3 -c "
import sqlite3
import sys

try:
    conn = sqlite3.connect('context-memory.db')
    cursor = conn.cursor()
    
    # Verificar total de registros
    cursor.execute('SELECT COUNT(*) FROM turso_agent_knowledge')
    total = cursor.fetchone()[0]
    
    # Verificar registros recentes
    cursor.execute('''
        SELECT COUNT(*) FROM turso_agent_knowledge 
        WHERE updated_at >= datetime('now', '-1 day')
    ''')
    recent = cursor.fetchone()[0]
    
    # Verificar registros obsoletos
    cursor.execute('''
        SELECT COUNT(*) FROM turso_agent_knowledge 
        WHERE updated_at < datetime('now', '-30 days')
    ''')
    obsolete = cursor.fetchone()[0]
    
    print(f'📊 INTEGRIDADE:')
    print(f'   • Total de registros: {total}')
    print(f'   • Registros recentes (24h): {recent}')
    print(f'   • Registros obsoletos (>30d): {obsolete}')
    
    if obsolete > 0:
        print(f'⚠️  {obsolete} registros obsoletos encontrados')
        sys.exit(1)
    else:
        print('✅ Integridade OK')
        sys.exit(0)
        
except Exception as e:
    print(f'❌ Erro ao verificar integridade: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        success "Integridade verificada com sucesso!"
    else
        warning "Problemas de integridade detectados"
    fi
}

# Função para mostrar status
show_status() {
    log "📊 Status do sistema de sync:"
    
    if [ -f "$LAST_SYNC_FILE" ]; then
        last_sync=$(cat "$LAST_SYNC_FILE")
        last_sync_date=$(date -d "@$last_sync" '+%Y-%m-%d %H:%M:%S')
        echo "   • Última sincronização: $last_sync_date"
    else
        echo "   • Última sincronização: Nunca"
    fi
    
    # Verificar se há arquivos de log recentes
    recent_logs=$(find "$LOG_DIR" -name "sync_*.log" -mtime -1 | wc -l)
    echo "   • Logs recentes (24h): $recent_logs"
    
    # Verificar tamanho do banco
    if [ -f "$PROJECT_ROOT/context-memory.db" ]; then
        db_size=$(du -h "$PROJECT_ROOT/context-memory.db" | cut -f1)
        echo "   • Tamanho do banco: $db_size"
    fi
}

# Função para limpar logs antigos
cleanup_logs() {
    log "🧹 Limpando logs antigos..."
    
    # Remover logs mais antigos que 7 dias
    find "$LOG_DIR" -name "sync_*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Remover relatórios mais antigos que 30 dias
    find "$PROJECT_ROOT" -name "sync_report_*.txt" -mtime +30 -delete 2>/dev/null || true
    
    success "Limpeza de logs concluída"
}

# Função para mostrar ajuda
show_help() {
    echo "🔄 Sistema de Sincronização de Conhecimento Turso Agent"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos:"
    echo "  sync        - Executar sincronização"
    echo "  auto        - Executar sync automático (se necessário)"
    echo "  status      - Mostrar status do sistema"
    echo "  integrity   - Verificar integridade do conhecimento"
    echo "  cleanup     - Limpar logs antigos"
    echo "  help        - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 sync      # Forçar sync agora"
    echo "  $0 auto      # Sync automático (a cada 6h)"
    echo "  $0 status    # Ver status atual"
}

# Main
case "${1:-auto}" in
    "sync")
        run_sync
        ;;
    "auto")
        if should_sync; then
            run_sync
            check_integrity
        else
            log "⏰ Sync não necessário (executado recentemente)"
        fi
        ;;
    "status")
        show_status
        ;;
    "integrity")
        check_integrity
        ;;
    "cleanup")
        cleanup_logs
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        error "Comando inválido: $1"
        show_help
        exit 1
        ;;
esac

success "Script executado com sucesso!" 