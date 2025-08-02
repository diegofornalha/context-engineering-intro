#!/usr/bin/env python3
"""
Turso Agent - Testes Automatizados
Valida todas as funcionalidades do agente especialista Turso
"""

import asyncio
import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Adicionar path do turso-agent
sys.path.append(str(Path(__file__).parent.parent))

from config.turso_settings import TursoSettings
from tools.turso_manager import TursoManager
from tools.mcp_integrator import MCPTursoIntegrator
from agents.turso_specialist import TursoSpecialistAgent

class TestTursoSettings(unittest.TestCase):
    """Testes para configurações Turso"""
    
    def setUp(self):
        """Setup para cada teste"""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'TURSO_API_TOKEN': 'test_token_123456789',
            'TURSO_ORGANIZATION': 'test_org',
            'TURSO_DEFAULT_DATABASE': 'test_db'
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Cleanup após cada teste"""
        self.env_patcher.stop()
    
    def test_settings_initialization(self):
        """Testa inicialização das configurações"""
        settings = TursoSettings()
        
        self.assertEqual(settings.turso_api_token, 'test_token_123456789')
        self.assertEqual(settings.turso_organization, 'test_org')
        self.assertEqual(settings.default_database, 'test_db')
        self.assertEqual(settings.environment, 'development')
    
    def test_token_validation(self):
        """Testa validação de tokens"""
        settings = TursoSettings()
        
        # Token válido
        self.assertTrue(settings._is_valid_token_format('valid_token_123456789'))
        
        # Token muito curto
        self.assertFalse(settings._is_valid_token_format('short'))
        
        # Token EdDSA (formato antigo)
        self.assertFalse(settings._is_valid_token_format('eyJEdDSA'))
    
    def test_database_config_management(self):
        """Testa gerenciamento de configurações de database"""
        settings = TursoSettings()
        
        # Adicionar configuração
        settings.add_database_config('test_db', 'test_token', 'test_url')
        
        # Verificar recuperação
        self.assertEqual(settings.get_database_token('test_db'), 'test_token')
        self.assertEqual(settings.get_database_url('test_db'), 'test_url')
        
        # Connection string
        conn_str = settings.get_connection_string('test_db')
        self.assertEqual(conn_str, 'test_url?authToken=test_token')
    
    def test_environment_detection(self):
        """Testa detecção de ambiente"""
        settings = TursoSettings()
        
        self.assertTrue(settings.is_development())
        self.assertFalse(settings.is_production())
    
    def test_mcp_config_export(self):
        """Testa exportação de configuração MCP"""
        settings = TursoSettings()
        mcp_config = settings.export_mcp_config()
        
        self.assertIn('organizationToken', mcp_config)
        self.assertIn('defaultDatabase', mcp_config)
        self.assertIn('serverConfig', mcp_config)

class TestTursoManager(unittest.IsolatedAsyncioTestCase):
    """Testes para Turso Manager"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.env_patcher = patch.dict('os.environ', {
            'TURSO_API_TOKEN': 'test_token_123456789',
            'TURSO_ORGANIZATION': 'test_org',
            'TURSO_DEFAULT_DATABASE': 'test_db'
        })
        self.env_patcher.start()
        
        self.settings = TursoSettings()
        self.turso_manager = TursoManager(self.settings)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        self.env_patcher.stop()
    
    async def test_check_configuration(self):
        """Testa verificação de configuração"""
        with patch.object(self.turso_manager, '_check_turso_cli', return_value=True), \
             patch.object(self.turso_manager, '_check_authentication', return_value=True), \
             patch.object(self.turso_manager, '_check_connectivity', return_value=True):
            
            result = await self.turso_manager.check_configuration()
            self.assertIn('✅', result)
    
    async def test_query_type_detection(self):
        """Testa detecção de tipos de query"""
        # Query destrutiva
        self.assertTrue(self.turso_manager._is_destructive_query('INSERT INTO test VALUES (1)'))
        self.assertTrue(self.turso_manager._is_destructive_query('UPDATE test SET x = 1'))
        self.assertTrue(self.turso_manager._is_destructive_query('DELETE FROM test'))
        
        # Query read-only
        self.assertTrue(self.turso_manager._is_read_only_query('SELECT * FROM test'))
        self.assertTrue(self.turso_manager._is_read_only_query('PRAGMA table_info(test)'))
        
        # Query destrutiva não é read-only
        self.assertFalse(self.turso_manager._is_read_only_query('INSERT INTO test VALUES (1)'))
    
    @patch('subprocess.run')
    async def test_list_databases_cli(self, mock_subprocess):
        """Testa listagem de databases via CLI"""
        # Mock successful CLI response
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '[{"name": "test_db", "regions": ["lhr"], "status": "active"}]'
        mock_subprocess.return_value = mock_result
        
        # Mock API failure to force CLI usage
        with patch.object(self.turso_manager, '_list_databases_api', return_value=[]):
            databases = await self.turso_manager.list_databases()
            
            self.assertEqual(len(databases), 1)
            self.assertEqual(databases[0]['name'], 'test_db')
    
    @patch('subprocess.run')
    async def test_execute_query_cli(self, mock_subprocess):
        """Testa execução de query via CLI"""
        # Mock successful query execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'Query executed successfully'
        mock_subprocess.return_value = mock_result
        
        result = await self.turso_manager._execute_query_cli(
            'SELECT * FROM test', 'test_db'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], 'Query executed successfully')

class TestMCPIntegrator(unittest.IsolatedAsyncioTestCase):
    """Testes para MCP Integrator"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.env_patcher = patch.dict('os.environ', {
            'TURSO_API_TOKEN': 'test_token_123456789'
        })
        self.env_patcher.start()
        
        self.settings = TursoSettings()
        self.mcp_integrator = MCPTursoIntegrator(self.settings)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        self.env_patcher.stop()
    
    async def test_check_mcp_status(self):
        """Testa verificação de status MCP"""
        with patch.object(self.mcp_integrator, '_check_nodejs', return_value=True), \
             patch.object(self.mcp_integrator, '_check_mcp_package', return_value=True), \
             patch.object(self.mcp_integrator, '_check_mcp_configuration', return_value=True):
            
            status = await self.mcp_integrator.check_mcp_status()
            self.assertIn('✅', status)
    
    @patch('subprocess.run')
    async def test_nodejs_check(self, mock_subprocess):
        """Testa verificação do Node.js"""
        # Mock Node.js disponível
        mock_result = Mock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        result = await self.mcp_integrator._check_nodejs()
        self.assertTrue(result)
        
        # Mock Node.js não disponível
        mock_result.returncode = 1
        result = await self.mcp_integrator._check_nodejs()
        self.assertFalse(result)
    
    async def test_mcp_configuration_check(self):
        """Testa verificação de configuração MCP"""
        # Com token configurado
        result = await self.mcp_integrator._check_mcp_configuration()
        self.assertTrue(result)
        
        # Sem token
        self.settings.turso_api_token = None
        result = await self.mcp_integrator._check_mcp_configuration()
        self.assertFalse(result)
    
    async def test_security_checks(self):
        """Testa verificações de segurança"""
        # Token security
        self.assertTrue(self.mcp_integrator._check_token_security())
        
        # Environment security
        self.assertTrue(self.mcp_integrator._check_environment_security())
        
        # Network security
        self.assertTrue(self.mcp_integrator._check_network_security())
        
        # Access control
        self.assertTrue(self.mcp_integrator._check_access_control())

class TestTursoSpecialistAgent(unittest.IsolatedAsyncioTestCase):
    """Testes para Turso Specialist Agent"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.env_patcher = patch.dict('os.environ', {
            'TURSO_API_TOKEN': 'test_token_123456789',
            'TURSO_ORGANIZATION': 'test_org'
        })
        self.env_patcher.start()
        
        self.settings = TursoSettings()
        self.turso_manager = Mock(spec=TursoManager)
        self.mcp_integrator = Mock(spec=MCPTursoIntegrator)
        
        # Mock PRP context
        with patch.object(TursoSpecialistAgent, '_load_prp_context', return_value={
            'context_data': {
                'turso_ecosystem': {
                    'core_components': ['Turso Database', 'MCP Integration'],
                    'supported_languages': ['Python', 'JavaScript'],
                    'key_features': ['SQLite compatibility', 'Edge replication']
                }
            },
            'validation_gates': [
                {'nome': 'Setup Turso Environment', 'comando': 'turso auth whoami'},
                {'nome': 'Database Operations', 'comando': 'turso db list'}
            ]
        }):
            self.agent = TursoSpecialistAgent(
                turso_manager=self.turso_manager,
                mcp_integrator=self.mcp_integrator,
                settings=self.settings
            )
    
    def tearDown(self):
        """Cleanup após cada teste"""
        self.env_patcher.stop()
    
    def test_question_type_analysis(self):
        """Testa análise de tipos de questão"""
        # Database operations
        self.assertEqual(
            self.agent._analyze_question_type('how to create a database'),
            'database_operations'
        )
        
        # MCP integration
        self.assertEqual(
            self.agent._analyze_question_type('mcp integration setup'),
            'mcp_integration'
        )
        
        # Performance
        self.assertEqual(
            self.agent._analyze_question_type('slow query optimization'),
            'performance'
        )
        
        # Security
        self.assertEqual(
            self.agent._analyze_question_type('token security audit'),
            'security'
        )
        
        # Troubleshooting
        self.assertEqual(
            self.agent._analyze_question_type('error debugging help'),
            'troubleshooting'
        )
        
        # General
        self.assertEqual(
            self.agent._analyze_question_type('general turso info'),
            'general'
        )
    
    async def test_chat_database_question(self):
        """Testa chat com questão sobre database"""
        response = await self.agent._handle_database_question('how to create database')
        
        self.assertIn('DATABASE OPERATIONS', response)
        self.assertIn('turso db create', response)
    
    async def test_chat_mcp_question(self):
        """Testa chat com questão sobre MCP"""
        response = await self.agent._handle_mcp_question('mcp integration help')
        
        self.assertIn('MCP TURSO INTEGRATION', response)
        self.assertIn('Two-Level Authentication', response)
    
    async def test_chat_performance_question(self):
        """Testa chat com questão sobre performance"""
        response = await self.agent._handle_performance_question('performance optimization')
        
        self.assertIn('PERFORMANCE OPTIMIZATION', response)
        self.assertIn('Query Optimization', response)
    
    async def test_troubleshoot_connection_issue(self):
        """Testa troubleshooting de problema de conexão"""
        response = await self.agent.troubleshoot_issue('connection failed authentication error')
        
        self.assertIn('Problema de Conexão Detectado', response)
        self.assertIn('turso auth whoami', response)
    
    async def test_troubleshoot_performance_issue(self):
        """Testa troubleshooting de problema de performance"""
        response = await self.agent.troubleshoot_issue('queries are very slow timeout')
        
        self.assertIn('Problema de Performance Detectado', response)
        self.assertIn('EXPLAIN QUERY PLAN', response)
    
    async def test_analyze_performance(self):
        """Testa análise de performance"""
        # Mock turso_manager methods
        self.turso_manager.list_databases = AsyncMock(return_value=['db1', 'db2'])
        self.turso_manager.check_configuration = AsyncMock(return_value='✅ Configuration OK')
        
        result = await self.agent.analyze_performance()
        
        self.assertIn('PERFORMANCE ANALYSIS', result)
        self.assertIn('Databases ativos: 2', result)
    
    async def test_security_audit(self):
        """Testa auditoria de segurança"""
        # Mock methods
        self.mcp_integrator.check_security = AsyncMock(return_value='✅ Security OK')
        
        result = await self.agent.security_audit()
        
        self.assertIn('SECURITY AUDIT', result)
        self.assertIn('Security Checklist', result)
    
    async def test_validation_gates(self):
        """Testa execução de validation gates"""
        result = await self.agent.run_validation_gates()
        
        self.assertIn('VALIDATION GATES', result)
        self.assertIn('Setup Turso Environment', result)
        self.assertIn('Database Operations', result)
    
    async def test_get_system_info(self):
        """Testa obtenção de informações do sistema"""
        # Mock methods
        self.turso_manager.check_configuration = AsyncMock(return_value='✅ OK')
        self.mcp_integrator.check_mcp_status = AsyncMock(return_value='✅ OK')
        
        result = await self.agent.get_system_info()
        
        self.assertIn('SYSTEM INFO', result)
        self.assertIn('PRP Base', result)
        self.assertIn('Capabilities', result)

class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """Testes de integração completos"""
    
    def setUp(self):
        """Setup para testes de integração"""
        self.env_patcher = patch.dict('os.environ', {
            'TURSO_API_TOKEN': 'test_token_123456789',
            'TURSO_ORGANIZATION': 'test_org',
            'TURSO_DEFAULT_DATABASE': 'test_db'
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Cleanup após testes"""
        self.env_patcher.stop()
    
    async def test_full_agent_initialization(self):
        """Testa inicialização completa do agente"""
        settings = TursoSettings()
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Mock PRP loading
        with patch.object(TursoSpecialistAgent, '_load_prp_context', return_value={}):
            agent = TursoSpecialistAgent(
                turso_manager=turso_manager,
                mcp_integrator=mcp_integrator,
                settings=settings
            )
        
        self.assertIsNotNone(agent.settings)
        self.assertIsNotNone(agent.turso_manager)
        self.assertIsNotNone(agent.mcp_integrator)
    
    async def test_end_to_end_workflow(self):
        """Testa workflow completo end-to-end"""
        settings = TursoSettings()
        
        # Verificar configurações carregadas
        self.assertIsNotNone(settings.turso_api_token)
        self.assertEqual(settings.turso_organization, 'test_org')
        
        # Inicializar managers
        turso_manager = TursoManager(settings)
        mcp_integrator = MCPTursoIntegrator(settings)
        
        # Verificar status (sem executar operações reais)
        with patch.object(turso_manager, '_check_turso_cli', return_value=False), \
             patch.object(turso_manager, '_check_authentication', return_value=True), \
             patch.object(turso_manager, '_check_connectivity', return_value=True):
            
            config_status = await turso_manager.check_configuration()
            self.assertIn('API funcional', config_status)
        
        with patch.object(mcp_integrator, '_check_nodejs', return_value=True), \
             patch.object(mcp_integrator, '_check_mcp_package', return_value=False):
            
            mcp_status = await mcp_integrator.check_mcp_status()
            self.assertIn('Node.js disponível', mcp_status)

def run_tests():
    """Executa todos os testes"""
    
    print("🧪 **TURSO AGENT - TESTES AUTOMATIZADOS**")
    print("="*55)
    print("📊 Baseado no PRP ID 6: Agente Especialista Turso")
    print("🎯 Validando todas as funcionalidades")
    print("="*55)
    
    # Descobrir e executar testes
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Relatório final
    print("\\n" + "="*55)
    print("📊 **RELATÓRIO FINAL DE TESTES:**")
    print(f"🧪 Testes executados: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"💥 Erros: {len(result.errors)}")
    
    if result.failures:
        print("\\n⚠️ **FALHAS:**")
        for test, traceback in result.failures:
            print(f"   ❌ {test}: {traceback.split('\\n')[-2]}")
    
    if result.errors:
        print("\\n💥 **ERROS:**")
        for test, traceback in result.errors:
            print(f"   💥 {test}: {traceback.split('\\n')[-2]}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0
    
    print(f"\\n📈 **TAXA DE SUCESSO: {success_rate:.1f}%**")
    
    if success_rate >= 90:
        print("🎉 **EXCELENTE!** Turso Agent totalmente validado!")
    elif success_rate >= 75:
        print("✅ **BOM!** Turso Agent funcionando bem!")
    elif success_rate >= 50:
        print("⚠️ **ACEITÁVEL!** Algumas melhorias necessárias")
    else:
        print("❌ **CRÍTICO!** Problemas sérios encontrados")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)