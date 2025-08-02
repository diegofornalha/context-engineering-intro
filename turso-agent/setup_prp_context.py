#!/usr/bin/env python3
"""
Setup do contexto PRP para o Turso Agent
Cria o banco de dados e insere o PRP ID 6
"""

import sqlite3
import json
from pathlib import Path

def create_prp_database():
    """Cria banco de dados com o PRP ID 6"""
    
    # Criar diretório se não existir
    db_path = Path(__file__).parent.parent / "context-memory.db"
    db_path.parent.mkdir(exist_ok=True)
    
    # Conectar ao banco
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Criar tabela prps
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prps (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        objective TEXT,
        context_data TEXT,
        implementation_details TEXT,
        validation_gates TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Dados do PRP ID 6 - Agente Especialista em Turso Database
    prp_data = {
        'id': 6,
        'title': 'Agente Especialista em Turso Database & MCP Integration',
        'description': '''Agente especializado em Turso Database, libSQL e MCP Integration.
        Expert em operações distribuídas, otimização de performance, segurança e troubleshooting.
        Domina completamente a stack Turso e suas integrações com LLMs via MCP.''',
        'objective': '''Fornecer expertise completa em Turso Database incluindo:
        - Database lifecycle management
        - MCP server integration
        - Performance optimization
        - Security auditing
        - Automated troubleshooting
        - Developer experience enhancement''',
        'context_data': json.dumps({
            'expertise_areas': [
                'Turso Database Operations',
                'libSQL Compatibility',
                'MCP Protocol Implementation',
                'Distributed Database Architecture',
                'Edge Computing with Turso',
                'Vector Search Integration',
                'Memory System Design',
                'Security Best Practices',
                'Performance Optimization',
                'Developer Experience'
            ],
            'key_features': {
                'database_management': [
                    'Create/manage databases',
                    'Execute SQL queries',
                    'Schema migrations',
                    'Backup and restore',
                    'Replication management'
                ],
                'mcp_integration': [
                    'Two-level authentication',
                    'Token management',
                    'LLM integration',
                    'Security compliance',
                    'Tool development'
                ],
                'performance': [
                    'Query optimization',
                    'Index management',
                    'Connection pooling',
                    'Cache strategies',
                    'Latency reduction'
                ],
                'security': [
                    'Authentication setup',
                    'Token rotation',
                    'Access control',
                    'Audit logging',
                    'Compliance checks'
                ]
            },
            'turso_specifics': {
                'protocols': ['HTTP', 'WebSocket', 'libSQL'],
                'deployment': ['Edge', 'Multi-region', 'Local development'],
                'features': ['SQLite compatibility', 'Distributed reads', 'Embedded replicas'],
                'integrations': ['MCP', 'REST API', 'SDKs']
            }
        }),
        'implementation_details': json.dumps({
            'required_tools': [
                'TursoManager - Database operations',
                'MCPTursoIntegrator - MCP integration',
                'TursoSettings - Configuration management'
            ],
            'validation_process': {
                'level_1': 'Configuration validation',
                'level_2': 'Connection testing',
                'level_3': 'Security audit',
                'level_4': 'Performance benchmarking'
            },
            'best_practices': [
                'Always use two-level authentication',
                'Implement connection pooling',
                'Enable audit logging',
                'Regular token rotation',
                'Monitor performance metrics',
                'Use read replicas for scaling',
                'Implement proper error handling',
                'Follow security guidelines'
            ],
            'common_patterns': {
                'authentication': {
                    'organization_level': 'API token for management',
                    'database_level': 'Database tokens for queries'
                },
                'optimization': {
                    'indexes': 'Create based on query patterns',
                    'caching': 'Implement at application level',
                    'pooling': 'Use connection pools'
                },
                'troubleshooting': {
                    'connection_issues': 'Check tokens and network',
                    'performance': 'Analyze query plans',
                    'errors': 'Check logs and permissions'
                }
            }
        }),
        'validation_gates': json.dumps([
            {
                'level': 1,
                'name': 'Configuration Check',
                'checks': [
                    'API token present',
                    'Organization configured',
                    'Valid environment'
                ]
            },
            {
                'level': 2,
                'name': 'Connection Validation',
                'checks': [
                    'Can list databases',
                    'Can connect to database',
                    'Token permissions valid'
                ]
            },
            {
                'level': 3,
                'name': 'Security Audit',
                'checks': [
                    'Token scope minimal',
                    'Audit logging enabled',
                    'Access controls configured'
                ]
            },
            {
                'level': 4,
                'name': 'Performance Verification',
                'checks': [
                    'Query performance acceptable',
                    'Connection pooling optimized',
                    'Caching strategy effective'
                ]
            }
        ]),
        'status': 'active'
    }
    
    # Inserir PRP
    cursor.execute('''
    INSERT OR REPLACE INTO prps 
    (id, title, description, objective, context_data, implementation_details, validation_gates, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        prp_data['id'],
        prp_data['title'],
        prp_data['description'],
        prp_data['objective'],
        prp_data['context_data'],
        prp_data['implementation_details'],
        prp_data['validation_gates'],
        prp_data['status']
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Banco de dados criado: {db_path}")
    print("✅ PRP ID 6 inserido com sucesso!")
    
    # Verificar inserção
    verify_prp_insertion(db_path)

def verify_prp_insertion(db_path):
    """Verifica se o PRP foi inserido corretamente"""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, title, status FROM prps WHERE id = 6')
    result = cursor.fetchone()
    
    if result:
        print(f"\n📊 Verificação:")
        print(f"   ID: {result[0]}")
        print(f"   Título: {result[1]}")
        print(f"   Status: {result[2]}")
    else:
        print("❌ PRP não encontrado!")
    
    conn.close()

if __name__ == "__main__":
    print("🚀 Configurando contexto PRP para Turso Agent...")
    print("=" * 60)
    create_prp_database()
    print("\n✅ Setup concluído! O agente agora tem acesso ao PRP completo.")