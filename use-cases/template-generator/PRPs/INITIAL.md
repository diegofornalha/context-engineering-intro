# Solicitação de Geração de Template

## TECNOLOGIA/FRAMEWORK:

**Exemplo:** Agentes Pydantic AI  
**Exemplo:** Aplicações frontend Supabase  
**Exemplo:** Sistemas multi-agente CrewAI  

**Sua tecnologia:** [Especifique o framework, biblioteca ou tecnologia exata para a qual você quer criar um template de context engineering]

---

## PROPÓSITO DO TEMPLATE:

**Para qual caso de uso específico este template deve ser otimizado?**

**Exemplo para Pydantic AI:** "Construindo agentes de IA inteligentes com integração de ferramentas, manipulação de conversas e validação de dados estruturados usando o framework Pydantic AI"

**Exemplo para Supabase:** "Criando aplicações web full-stack com dados em tempo real, autenticação e funções serverless usando Supabase como backend"

**Seu propósito:** [Seja muito específico sobre o que os desenvolvedores devem ser capazes de construir facilmente com este template]

---

## FUNCIONALIDADES PRINCIPAIS:

**Quais são as funcionalidades essenciais que este template deve ajudar os desenvolvedores a implementar?**

**Exemplo para Pydantic AI:**
- Criação de agentes com diferentes provedores de modelo (OpenAI, Anthropic, Gemini)
- Padrões de integração de ferramentas (pesquisa web, operações de arquivo, chamadas de API)
- Memória de conversa e gerenciamento de contexto
- Validação de saída estruturada com modelos Pydantic
- Tratamento de erro e mecanismos de retry
- Padrões de teste para comportamento de agentes de IA

**Exemplo para Supabase:**
- Design de esquema de banco de dados e migrações
- Assinaturas em tempo real e atualizações de dados ao vivo
- Implementação de políticas de Row Level Security (RLS)
- Fluxos de autenticação (email, OAuth, magic links)
- Funções serverless edge para lógica de backend
- Integração de armazenamento de arquivos e CDN

**Suas funcionalidades principais:** [Liste as capacidades específicas que os desenvolvedores devem ser capazes de implementar facilmente]

---

## EXEMPLOS PARA INCLUIR:

**Quais exemplos funcionais devem ser fornecidos no template?**

**Exemplo para Pydantic AI:**
- Agente de chat básico com memória
- Agente habilitado para ferramentas (pesquisa web + calculadora)
- Agente de fluxo de trabalho multi-etapa
- Agente com modelos Pydantic personalizados para saídas estruturadas
- Exemplos de teste para respostas de agentes e uso de ferramentas

**Exemplo para Supabase:**
- Autenticação de usuário e gerenciamento de perfil
- Sistema de chat ou mensagens em tempo real
- Funcionalidade de upload e compartilhamento de arquivos
- Padrões de aplicação multi-tenant
- Triggers e funções de banco de dados

**Seus exemplos:** [Especifique exemplos concretos e funcionais que devem ser incluídos]

---

## DOCUMENTAÇÃO PARA PESQUISAR:

**Qual documentação específica deve ser pesquisada e referenciada?**

**Exemplo para Pydantic AI:**
- https://ai.pydantic.dev/ - Documentação oficial do Pydantic AI
- https://docs.pydantic.dev/ - Biblioteca de validação de dados Pydantic
- APIs de provedores de modelo (OpenAI, Anthropic) para padrões de integração
- Melhores práticas de integração de ferramentas e exemplos
- Frameworks de teste para aplicações de IA

**Exemplo para Supabase:**
- https://supabase.com/docs - Documentação completa do Supabase
- https://supabase.com/docs/guides/auth - Guia de autenticação
- https://supabase.com/docs/guides/realtime - Funcionalidades em tempo real
- Padrões de design de banco de dados e políticas RLS
- Desenvolvimento e implantação de funções edge

**Sua documentação:** [Liste URLs específicas e seções de documentação para pesquisar profundamente]

---

## PADRÕES DE DESENVOLVIMENTO:

**Quais padrões de desenvolvimento, estruturas de projeto ou fluxos de trabalho devem ser pesquisados e incluídos?**

**Exemplo para Pydantic AI:**
- Como estruturar módulos de agentes e definições de ferramentas
- Gerenciamento de configuração para diferentes provedores de modelo
- Configuração de ambiente para desenvolvimento vs produção
- Padrões de logging e monitoramento para agentes de IA
- Padrões de controle de versão para prompts e configurações de agentes

**Exemplo para Supabase:**
- Padrões de estrutura de projeto frontend + Supabase
- Fluxo de trabalho de desenvolvimento local com Supabase CLI
- Estratégias de migração e versionamento de banco de dados
- Gerenciamento de ambiente (local, staging, produção)
- Estratégias de teste para aplicações full-stack Supabase

**Seus padrões de desenvolvimento:** [Especifique os padrões de fluxo de trabalho e organizacionais para pesquisar]

---

## SEGURANÇA E MELHORES PRÁTICAS:

**Quais considerações de segurança e melhores práticas são críticas para esta tecnologia?**

**Exemplo para Pydantic AI:**
- Gerenciamento e rotação de chaves de API
- Validação e sanitização de entrada para entradas de agentes
- Limitação de taxa e monitoramento de uso
- Prevenção de injeção de prompt
- Controle de custo e monitoramento para uso de modelo

**Exemplo para Supabase:**
- Design de políticas de Row Level Security (RLS)
- Padrões de autenticação de chave de API vs JWT
- Segurança de banco de dados e controle de acesso
- Segurança de upload de arquivos e escaneamento de vírus
- Limitação de taxa e prevenção de abuso

**Suas considerações de segurança:** [Liste padrões de segurança específicos da tecnologia para pesquisar e documentar]

---

## ARMADILHAS COMUNS:

**Quais são as armadilhas típicas, casos extremos ou problemas complexos que os desenvolvedores enfrentam com esta tecnologia?**

**Exemplo para Pydantic AI:**
- Limitações de comprimento de contexto do modelo e gerenciamento
- Lidando com limites de taxa e erros de provedores de modelo
- Contagem de tokens e otimização de custo
- Gerenciando estado de conversa entre requisições
- Tratamento de erro de execução de ferramentas e retries

**Exemplo para Supabase:**
- Debugging e teste de políticas RLS
- Performance de assinatura em tempo real com grandes conjuntos de dados
- Cold starts e otimização de funções edge
- Pool de conexões de banco de dados em ambientes serverless
- Configuração CORS para diferentes domínios

**Suas armadilhas:** [Identifique os desafios específicos que os desenvolvedores enfrentam comumente]

---

## REQUISITOS DE VALIDAÇÃO:

**Quais validações, testes ou verificações de qualidade específicas devem ser incluídas no template?**

**Exemplo para Pydantic AI:**
- Teste de qualidade de resposta de agentes
- Teste de integração de ferramentas
- Teste de fallback de provedores de modelo
- Benchmarking de custo e performance
- Validação de fluxo de conversa

**Exemplo para Supabase:**
- Teste de migração de banco de dados
- Validação de políticas RLS
- Teste de funcionalidade em tempo real
- Teste de fluxo de autenticação
- Teste de integração de funções edge

**Seus requisitos de validação:** [Especifique os padrões de teste e validação necessários]

---

## FOCO DE INTEGRAÇÃO:

**Quais integrações ou serviços de terceiros são comumente usados com esta tecnologia?**

**Exemplo para Pydantic AI:**
- Integração com bancos de dados vetoriais (Pinecone, Weaviate)
- Ferramentas de web scraping e APIs
- Integrações de API externas para ferramentas
- Serviços de monitoramento (Weights & Biases, LangSmith)
- Plataformas de implantação (Modal, Replicate)

**Exemplo para Supabase:**
- Frameworks frontend (Next.js, React, Vue)
- Processamento de pagamento (Stripe)
- Serviços de email (SendGrid, Resend)
- Processamento de arquivos (otimização de imagem, parsing de documentos)
- Ferramentas de analytics e monitoramento

**Seu foco de integração:** [Liste as integrações principais para pesquisar e incluir]

---

## NOTAS ADICIONAIS:

**Quaisquer outros requisitos específicos, restrições ou considerações para este template?**

**Exemplo:** "Foque em padrões TypeScript e inclua definições de tipo abrangentes"  
**Exemplo:** "Enfatize padrões de implantação serverless e otimização de custo"  
**Exemplo:** "Inclua padrões para casos de uso tanto iniciantes quanto avançados"

**Suas notas adicionais:** [Quaisquer outras considerações importantes]

---

## NÍVEL DE COMPLEXIDADE DO TEMPLATE:

**Qual nível de complexidade este template deve visar?**

- [ ] **Amigável para iniciantes** - Padrões simples de começar
- [ ] **Intermediário** - Padrões prontos para produção com funcionalidades comuns  
- [ ] **Avançado** - Padrões abrangentes incluindo cenários complexos
- [ ] **Empresarial** - Padrões empresariais completos com monitoramento, escalabilidade, segurança

**Sua escolha:** [Selecione o nível de complexidade apropriado e explique por quê]

---

**LEMBRETE: Seja o mais específico possível em cada seção. Quanto mais detalhado você for aqui, melhor será o template gerado. Este arquivo INITIAL.md é onde você deve colocar todos os seus requisitos, não apenas informações básicas.**