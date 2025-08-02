# Instruções para Sincronização com Turso

## 📊 Resumo
- Total de documentos: 48
- Arquivos SQL gerados: 6

## 🚀 Execute no Claude Code:

### 1. Criar estrutura das tabelas:
```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/01-create-tables.sql no banco context-memory
```

### 2. Inserir documentos (execute cada batch):

```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/02-insert-batch-01.sql no banco context-memory
```

```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/02-insert-batch-02.sql no banco context-memory
```

```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/02-insert-batch-03.sql no banco context-memory
```

```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/02-insert-batch-04.sql no banco context-memory
```

```
Use mcp__turso__execute_query para executar o conteúdo do arquivo docs/sync-parts/02-insert-batch-05.sql no banco context-memory
```


## ✅ Verificar sincronização:
```
Use mcp__turso__execute_read_only_query com a query "SELECT COUNT(*) as total, cluster, COUNT(DISTINCT category) as categories FROM docs GROUP BY cluster ORDER BY cluster" no banco context-memory
```
