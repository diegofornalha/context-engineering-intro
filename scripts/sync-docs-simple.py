#!/usr/bin/env python3
"""
Script simplificado para sincronizar documentos com Turso
"""

import json
from pathlib import Path

def main():
    # Carregar dados de sincronização
    sync_data_path = Path("/Users/agents/Desktop/context-engineering-intro/docs/.sync-data.json")
    
    with open(sync_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = data['documents']
    
    print(f"📊 Total de documentos para sincronizar: {len(documents)}")
    print("\n📝 Documentos por cluster:")
    
    # Agrupar por cluster
    clusters = {}
    for doc in documents:
        cluster = doc['cluster']
        if cluster not in clusters:
            clusters[cluster] = []
        clusters[cluster].append(doc)
    
    # Mostrar resumo
    for cluster, docs in sorted(clusters.items()):
        print(f"\n🗂️  {cluster}: {len(docs)} documentos")
        for doc in docs[:3]:  # Mostrar apenas os 3 primeiros
            print(f"  - {doc['file_path']}")
        if len(docs) > 3:
            print(f"  ... e mais {len(docs) - 3} documentos")
    
    # Criar script SQL simplificado
    sql_file = Path("/Users/agents/Desktop/context-engineering-intro/docs/sync-organized-docs.sql")
    
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write("-- Sincronização de documentos organizados\n\n")
        
        # Inserir documentos um por um
        for i, doc in enumerate(documents):
            if i > 0 and i % 5 == 0:
                f.write("\n-- Batch " + str(i//5 + 1) + "\n\n")
            
            # Escapar aspas simples
            content = doc['content'].replace("'", "''")
            title = doc['title'].replace("'", "''")
            summary = doc['summary'].replace("'", "''")
            
            f.write(f"""
INSERT OR REPLACE INTO docs_organized (
    file_path, title, content, summary, cluster, category,
    file_hash, size, last_modified, metadata
) VALUES (
    '{doc['file_path']}',
    '{title}',
    '{content}',
    '{summary}',
    '{doc['cluster']}',
    '{doc['category']}',
    '{doc['file_hash']}',
    {doc['size']},
    '{doc['last_modified']}',
    '{doc['metadata']}'
);
""")
    
    print(f"\n✅ Script SQL criado: {sql_file}")
    print("\n🎯 Para sincronizar, execute as queries no Turso")

if __name__ == "__main__":
    main()