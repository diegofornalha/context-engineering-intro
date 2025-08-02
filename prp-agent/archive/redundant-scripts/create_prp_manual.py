#!/usr/bin/env python3
"""
Script que cria PRPs manualmente sem depender da API do OpenAI
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório archive ao path
sys.path.insert(0, str(Path(__file__).parent / "archive"))

async def create_prp_manual():
    """
    Cria PRPs manualmente usando o agente real
    """
    
    print("🤖 CRIANDO PRPs MANUALMENTE VIA AGENTE REAL")
    print("=" * 60)
    print()
    
    try:
        # Importar o agente real
        from cursor_turso_integration import CursorTursoIntegration
        
        # Criar instância do agente
        agent = CursorTursoIntegration()
        
        # Lista de PRPs para criar manualmente
        prps_to_create = [
            {
                "feature": "Sistema de Autenticação Multi-Fator",
                "context": "Implementar sistema de login seguro com autenticação de dois fatores, suporte a OAuth2 e JWT tokens",
                "content": """
# PRP: Sistema de Autenticação Multi-Fator

## Objetivo
Implementar um sistema de autenticação robusto e seguro com múltiplas camadas de proteção.

## Funcionalidades Principais
- Login com email/senha
- Autenticação de dois fatores (2FA)
- Suporte a OAuth2 (Google, GitHub, etc.)
- JWT tokens para sessões
- Refresh tokens
- Logout seguro

## Requisitos Técnicos
- Backend: Node.js/Express ou Python/FastAPI
- Banco de dados: PostgreSQL ou MongoDB
- Redis para cache de sessões
- Biblioteca de JWT
- Integração com provedores OAuth2

## Critérios de Sucesso
- Login funcional com 2FA
- Integração com pelo menos 2 provedores OAuth2
- Tokens JWT válidos e seguros
- Logout que invalida tokens
- Testes automatizados cobrindo 90% do código
                """
            },
            {
                "feature": "Dashboard de Analytics em Tempo Real",
                "context": "Criar dashboard interativo com métricas em tempo real, gráficos dinâmicos e exportação de relatórios",
                "content": """
# PRP: Dashboard de Analytics em Tempo Real

## Objetivo
Desenvolver um dashboard interativo que exibe métricas e análises em tempo real.

## Funcionalidades Principais
- Gráficos dinâmicos (Chart.js, D3.js)
- Métricas em tempo real
- Filtros avançados
- Exportação de relatórios (PDF, Excel)
- Notificações de alertas
- Personalização de dashboards

## Requisitos Técnicos
- Frontend: React/Vue.js
- Backend: API REST
- WebSockets para dados em tempo real
- Biblioteca de gráficos
- Sistema de exportação

## Critérios de Sucesso
- Dashboard responsivo e funcional
- Gráficos atualizando em tempo real
- Exportação funcionando
- Performance adequada (< 2s de carregamento)
                """
            },
            {
                "feature": "API REST com Documentação Automática",
                "context": "Desenvolver API RESTful com documentação OpenAPI automática, testes automatizados e rate limiting",
                "content": """
# PRP: API REST com Documentação Automática

## Objetivo
Criar uma API RESTful bem documentada e testada com funcionalidades avançadas.

## Funcionalidades Principais
- Endpoints RESTful
- Documentação OpenAPI/Swagger
- Rate limiting
- Autenticação JWT
- Validação de dados
- Logs estruturados
- Monitoramento

## Requisitos Técnicos
- Framework: FastAPI, Express.js ou similar
- Documentação automática
- Middleware de rate limiting
- Validação com Pydantic/Joi
- Logs com Winston/Morgan
- Testes com Jest/Pytest

## Critérios de Sucesso
- Documentação OpenAPI completa
- Rate limiting funcionando
- Testes com cobertura > 90%
- Performance adequada
- Logs estruturados
                """
            },
            {
                "feature": "Sistema de Notificações Push",
                "context": "Implementar sistema de notificações push e email com templates personalizáveis e agendamento",
                "content": """
# PRP: Sistema de Notificações Push

## Objetivo
Desenvolver um sistema completo de notificações com suporte a push e email.

## Funcionalidades Principais
- Notificações push (web/mobile)
- Emails transacionais
- Templates personalizáveis
- Agendamento de notificações
- Preferências do usuário
- Relatórios de entrega

## Requisitos Técnicos
- Backend: Node.js/Python
- Push: Firebase Cloud Messaging
- Email: SendGrid/Mailgun
- Templates: Handlebars/Jinja2
- Agendamento: Redis/Bull
- Banco: PostgreSQL

## Critérios de Sucesso
- Push notifications funcionando
- Emails sendo enviados
- Templates personalizáveis
- Agendamento funcionando
- Relatórios de entrega
                """
            }
        ]
        
        created_count = 0
        
        for i, prp_data in enumerate(prps_to_create, 1):
            print(f"📄 Criando PRP {i}: {prp_data['feature']}")
            
            # Salvar PRP no banco
            prp_id = await agent.store_prp_suggestion(
                feature=prp_data["feature"],
                context=prp_data["context"],
                prp_content=prp_data["content"]
            )
            
            if prp_id > 0:
                print(f"✅ PRP {i} criado com ID: {prp_id}")
                created_count += 1
            else:
                print(f"❌ Erro ao criar PRP {i}")
            
            print()
        
        print(f"📊 Total de PRPs criados: {created_count}/{len(prps_to_create)}")
        
        # Criar algumas conversas de exemplo
        print("\n💬 Criando conversas de exemplo...")
        
        conversations = [
            {
                "message": "Crie um PRP para sistema de autenticação",
                "response": "PRP criado com sucesso! Sistema de autenticação multi-fator implementado.",
                "context": "auth_system.py"
            },
            {
                "message": "Liste todos os PRPs disponíveis",
                "response": "Aqui estão os PRPs disponíveis: Sistema de Autenticação Multi-Fator, Dashboard Analytics, API REST, Sistema de Notificações",
                "context": "prp_list.py"
            },
            {
                "message": "Analise o PRP do dashboard",
                "response": "Análise do PRP Dashboard Analytics: Complexidade alta, estimativa de 3-4 semanas, requer integração com WebSockets.",
                "context": "dashboard_analysis.py"
            }
        ]
        
        conversation_count = 0
        
        for conv in conversations:
            success = await agent.store_conversation(
                user_message=conv["message"],
                agent_response=conv["response"],
                file_context=conv["context"]
            )
            
            if success:
                conversation_count += 1
                print(f"✅ Conversa criada: {conv['message'][:30]}...")
            else:
                print(f"❌ Erro ao criar conversa")
        
        print(f"📊 Total de conversas criadas: {conversation_count}/{len(conversations)}")
        
        print("\n" + "=" * 60)
        print("✅ PRPs criados manualmente com sucesso!")
        print("🤖 Agente real funcionando com MCP Turso")
        
    except Exception as e:
        print(f"❌ Erro ao criar PRPs manualmente: {e}")

async def main():
    """
    Função principal
    """
    await create_prp_manual()

if __name__ == "__main__":
    asyncio.run(main()) 