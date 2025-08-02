# 📁 Scripts - Organização Recomendada

## Status Atual

Esta pasta contém scripts de manutenção que foram usados para:
- ✅ Organizar documentação em clusters (concluído)
- ✅ Sincronizar com Turso Database (concluído)
- ✅ Processar 48 documentos em batches (concluído)

## 🎯 Recomendação de Reorganização

### 1. **Mover para `/py-prp/tools/`**
Scripts que podem ser reutilizados:
- `organize-docs-clusters.py` → Útil para futuras reorganizações
- `sync-docs-to-turso.py` → Útil para sincronizações

### 2. **Arquivar em `/scripts/archive/`**
Scripts específicos desta migração:
- `batch-sync-*.py` → Específicos para os 48 docs
- `execute-*.py` → Scripts de execução única
- `*.sh` → Scripts bash temporários

### 3. **Documentar em `/docs/`**
- Criar documento sobre o processo de migração
- Explicar como foi feita a organização
- Guardar para referência futura

## 📋 Proposta de Estrutura Final

```
context-engineering-intro/
├── py-prp/
│   ├── integration/      # Scripts de integração
│   ├── memory/          # Sistema de memória
│   ├── tools/           # Ferramentas reutilizáveis
│   │   ├── organize_docs.py
│   │   └── sync_to_turso.py
│   └── diagnostics/     # Diagnóstico e testes
│
├── scripts/
│   ├── README.md        # Este arquivo
│   └── archive/         # Scripts de migração única
│       ├── batch-sync-*.py
│       └── *.sh
│
└── sql-db/              # Mantém como está
    ├── schemas/
    └── migrations/
```

## ⚠️ Importante

Antes de mover/arquivar, certifique-se de que:
1. A sincronização está completa
2. Não há processos pendentes
3. A documentação foi atualizada

---
*Scripts utilizados na migração de documentação em 02/08/2025*