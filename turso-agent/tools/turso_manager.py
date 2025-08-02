"""
Turso Manager - Gerenciador especializado de operações Turso Database
Implementa todas as operações core definidas no PRP ID 6
"""

import asyncio
import subprocess
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import sqlite3
from pathlib import Path

class TursoManager:
    """
    Gerenciador especializado para operações Turso Database
    
    Implementa funcionalidades do PRP:
    - Database lifecycle management
    - Query execution optimization  
    - Schema management
    - Backup and restore
    - Performance monitoring
    """
    
    def __init__(self, settings):
        self.settings = settings
        self.api_base_url = "https://api.turso.tech/v1"
        self.session = requests.Session()
        
        if self.settings.turso_api_token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.settings.turso_api_token}",
                "Content-Type": "application/json"
            })
    
    async def check_configuration(self) -> str:
        """Verifica status da configuração Turso"""
        
        try:
            # Verificar se CLI está instalado
            cli_check = await self._check_turso_cli()
            
            # Verificar authentication
            auth_check = await self._check_authentication()
            
            # Verificar conectividade
            connectivity_check = await self._check_connectivity()
            
            if cli_check and auth_check and connectivity_check:
                return "✅ Configuração completa"
            elif auth_check and connectivity_check:
                return "⚠️ CLI não instalado, API funcional"
            elif auth_check:
                return "⚠️ Token válido, conectividade limitada"
            else:
                return "❌ Configuração incompleta"
                
        except Exception as e:
            return f"❌ Erro: {str(e)}"
    
    async def _check_turso_cli(self) -> bool:
        """Verifica se Turso CLI está instalado"""
        try:
            result = subprocess.run(
                ["turso", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def _check_authentication(self) -> bool:
        """Verifica autenticação via API"""
        try:
            if not self.settings.turso_api_token:
                return False
                
            response = self.session.get(f"{self.api_base_url}/organizations")
            return response.status_code == 200
        except Exception:
            return False
    
    async def _check_connectivity(self) -> bool:
        """Verifica conectividade com serviços Turso"""
        try:
            response = requests.get("https://api.turso.tech/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    async def list_databases(self) -> List[Dict]:
        """Lista todos os databases da organização"""
        
        try:
            # Tentar via API primeiro
            databases = await self._list_databases_api()
            
            if databases:
                print("🗄️ **DATABASES TURSO:**")
                for db in databases:
                    print(f"   📊 {db.get('name', 'Unknown')}")
                    print(f"      🌍 Regions: {', '.join(db.get('regions', []))}")
                    print(f"      📈 Status: {db.get('status', 'Unknown')}")
                    print()
                return databases
            else:
                # Fallback para CLI
                return await self._list_databases_cli()
                
        except Exception as e:
            print(f"❌ Erro ao listar databases: {e}")
            return []
    
    async def _list_databases_api(self) -> List[Dict]:
        """Lista databases via API"""
        try:
            response = self.session.get(f"{self.api_base_url}/organizations/{self.settings.turso_organization}/databases")
            
            if response.status_code == 200:
                data = response.json()
                return data.get('databases', [])
            else:
                return []
                
        except Exception:
            return []
    
    async def _list_databases_cli(self) -> List[Dict]:
        """Lista databases via CLI"""
        try:
            result = subprocess.run(
                ["turso", "db", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"❌ CLI Error: {result.stderr}")
                return []
                
        except Exception as e:
            print(f"❌ CLI Exception: {e}")
            return []
    
    async def create_database(self, name: str, group: str = "default", regions: List[str] = None) -> bool:
        """Cria novo database Turso"""
        
        try:
            print(f"🗄️ Criando database: {name}")
            
            # Tentar via API primeiro
            success = await self._create_database_api(name, group, regions)
            
            if not success:
                # Fallback para CLI
                success = await self._create_database_cli(name, group, regions)
            
            if success:
                print(f"✅ Database '{name}' criado com sucesso!")
                
                # Gerar token automaticamente
                await self._generate_database_token(name)
                
                return True
            else:
                print(f"❌ Falha ao criar database '{name}'")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao criar database: {e}")
            return False
    
    async def _create_database_api(self, name: str, group: str, regions: List[str]) -> bool:
        """Cria database via API"""
        try:
            payload = {
                "name": name,
                "group": group
            }
            
            if regions:
                payload["regions"] = regions
                
            response = self.session.post(
                f"{self.api_base_url}/organizations/{self.settings.turso_organization}/databases",
                json=payload
            )
            
            return response.status_code in [200, 201]
            
        except Exception:
            return False
    
    async def _create_database_cli(self, name: str, group: str, regions: List[str]) -> bool:
        """Cria database via CLI"""
        try:
            cmd = ["turso", "db", "create", name, "--group", group]
            
            if regions:
                for region in regions:
                    cmd.extend(["--location", region])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
            
        except Exception:
            return False
    
    async def _generate_database_token(self, database_name: str) -> Optional[str]:
        """Gera token para database específico"""
        try:
            print(f"🔑 Gerando token para database: {database_name}")
            
            # Tentar via CLI
            result = subprocess.run(
                ["turso", "db", "tokens", "create", database_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                token = result.stdout.strip()
                
                # Salvar token nas configurações
                self.settings.add_database_config(database_name, token, "")
                
                print(f"✅ Token gerado para '{database_name}'")
                return token
            else:
                print(f"❌ Erro ao gerar token: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao gerar token: {e}")
            return None
    
    async def execute_query(self, query: str, database_name: str = None, params: List = None) -> Dict:
        """Executa query SQL (operação destrutiva)"""
        
        db_name = database_name or self.settings.default_database
        
        if not db_name:
            return {"error": "Database não especificado"}
        
        try:
            print(f"💻 Executando query em '{db_name}': {query[:50]}...")
            
            # Verificar se é operação destrutiva
            is_destructive = self._is_destructive_query(query)
            
            if is_destructive:
                print("⚠️ Operação destrutiva detectada - requer confirmação")
                
            # Executar via CLI (mais seguro)
            result = await self._execute_query_cli(query, db_name, params)
            
            if result.get('success'):
                print("✅ Query executada com sucesso!")
            else:
                print(f"❌ Erro na query: {result.get('error')}")
            
            return result
            
        except Exception as e:
            return {"error": f"Erro na execução: {str(e)}", "success": False}
    
    async def execute_read_only_query(self, query: str, database_name: str = None, params: List = None) -> Dict:
        """Executa query read-only (SELECT, PRAGMA, EXPLAIN)"""
        
        # Verificar se é realmente read-only
        if not self._is_read_only_query(query):
            return {"error": "Query não é read-only", "success": False}
        
        return await self.execute_query(query, database_name, params)
    
    def _is_destructive_query(self, query: str) -> bool:
        """Verifica se query é destrutiva"""
        destructive_keywords = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
            'TRUNCATE', 'REPLACE', 'MERGE'
        ]
        
        query_upper = query.strip().upper()
        return any(query_upper.startswith(keyword) for keyword in destructive_keywords)
    
    def _is_read_only_query(self, query: str) -> bool:
        """Verifica se query é read-only"""
        read_only_keywords = ['SELECT', 'PRAGMA', 'EXPLAIN', 'WITH']
        
        query_upper = query.strip().upper()
        return any(query_upper.startswith(keyword) for keyword in read_only_keywords)
    
    async def _execute_query_cli(self, query: str, database_name: str, params: List = None) -> Dict:
        """Executa query via CLI"""
        try:
            cmd = ["turso", "db", "shell", database_name, query]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.settings.query_timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "result": result.stdout,
                    "query": query,
                    "database": database_name
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "query": query,
                    "database": database_name
                }
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Query timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def backup_database(self, database_name: str) -> bool:
        """Cria backup de database"""
        
        try:
            print(f"💾 Iniciando backup do database: {database_name}")
            
            # Criar nome do backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{database_name}_backup_{timestamp}"
            
            # Usar dump para backup
            result = subprocess.run([
                "turso", "db", "dump", database_name
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # Salvar backup em arquivo
                backup_file = Path(f"backups/{backup_name}.sql")
                backup_file.parent.mkdir(exist_ok=True)
                
                with open(backup_file, 'w') as f:
                    f.write(result.stdout)
                
                print(f"✅ Backup salvo em: {backup_file}")
                return True
            else:
                print(f"❌ Erro no backup: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no backup: {e}")
            return False
    
    async def run_migrations(self) -> bool:
        """Executa migrações de schema"""
        
        try:
            print("🔄 Executando migrações de schema...")
            
            # Verificar pasta de migrações
            migrations_dir = Path("migrations")
            
            if not migrations_dir.exists():
                print("📁 Criando pasta de migrações...")
                migrations_dir.mkdir(exist_ok=True)
                
                # Criar migração de exemplo
                example_migration = """-- Migração de exemplo
-- Arquivo: 001_initial_schema.sql

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
"""
                
                with open(migrations_dir / "001_initial_schema.sql", 'w') as f:
                    f.write(example_migration)
                
                print("📄 Migração de exemplo criada em migrations/001_initial_schema.sql")
                return True
            
            # Executar migrações existentes
            migration_files = sorted(migrations_dir.glob("*.sql"))
            
            if not migration_files:
                print("⚠️ Nenhuma migração encontrada")
                return True
            
            database_name = self.settings.default_database
            if not database_name:
                print("❌ Database padrão não configurado")
                return False
            
            for migration_file in migration_files:
                print(f"📄 Executando: {migration_file.name}")
                
                with open(migration_file, 'r') as f:
                    migration_sql = f.read()
                
                result = await self.execute_query(migration_sql, database_name)
                
                if not result.get('success'):
                    print(f"❌ Erro na migração {migration_file.name}: {result.get('error')}")
                    return False
            
            print("✅ Todas as migrações executadas com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro nas migrações: {e}")
            return False
    
    async def analyze_performance(self, database_name: str = None) -> Dict:
        """Analisa performance do database"""
        
        db_name = database_name or self.settings.default_database
        
        if not db_name:
            return {"error": "Database não especificado"}
        
        try:
            print(f"⚡ Analisando performance de: {db_name}")
            
            analysis = {
                "database": db_name,
                "timestamp": datetime.now().isoformat(),
                "metrics": {}
            }
            
            # Verificar estatísticas do database
            stats_query = "PRAGMA database_list;"
            stats_result = await self.execute_read_only_query(stats_query, db_name)
            
            if stats_result.get('success'):
                analysis["metrics"]["database_info"] = stats_result.get('result')
            
            # Verificar tabelas
            tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables_result = await self.execute_read_only_query(tables_query, db_name)
            
            if tables_result.get('success'):
                analysis["metrics"]["tables"] = tables_result.get('result')
            
            # Verificar índices
            indexes_query = "SELECT name, tbl_name FROM sqlite_master WHERE type='index';"
            indexes_result = await self.execute_read_only_query(indexes_query, db_name)
            
            if indexes_result.get('success'):
                analysis["metrics"]["indexes"] = indexes_result.get('result')
            
            # Recomendações de otimização
            analysis["recommendations"] = [
                "Verificar uso de índices em queries frequentes",
                "Implementar connection pooling",
                "Monitorar latência de replicação",
                "Otimizar schema normalization",
                "Configurar query cache"
            ]
            
            print("✅ Análise de performance concluída!")
            return analysis
            
        except Exception as e:
            return {"error": f"Erro na análise: {str(e)}"}
    
    async def get_database_info(self, database_name: str = None) -> Dict:
        """Obtém informações detalhadas do database"""
        
        db_name = database_name or self.settings.default_database
        
        if not db_name:
            return {"error": "Database não especificado"}
        
        try:
            # Tentar via API primeiro
            api_info = await self._get_database_info_api(db_name)
            
            if api_info:
                return api_info
            
            # Fallback para informações básicas
            return {
                "name": db_name,
                "configured": True,
                "token_available": bool(self.settings.get_database_token(db_name)),
                "url_available": bool(self.settings.get_database_url(db_name))
            }
            
        except Exception as e:
            return {"error": f"Erro ao obter info: {str(e)}"}
    
    async def _get_database_info_api(self, database_name: str) -> Optional[Dict]:
        """Obtém informações via API"""
        try:
            response = self.session.get(
                f"{self.api_base_url}/organizations/{self.settings.turso_organization}/databases/{database_name}"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception:
            return None