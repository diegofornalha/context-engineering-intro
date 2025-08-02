## FUNCIONALIDADE:

Queremos criar um servidor MCP usando o template deste repositório

O objetivo do servidor MCP é criar uma versão simples do taskmaster mcp que, em vez de analisar PRDs, analisa PRPs.

Funcionalidades adicionais:

- Extração de informações de PRP alimentada por LLM usando Anthropic
- Operações CRUD em tarefas, documentação, tags, etc. para e do banco de dados

Precisamos de ferramentas para analisar PRPs. Esta ferramenta deve pegar um PRP preenchido e usar Anthropic para extrair as tarefas em tarefas e salvá-las no banco de dados, incluindo documentação circundante do PRP como objetivos, porquês, usuários alvo, etc.

Precisamos:

- Ser capaz de realizar operações CRUD em tarefas, documentação, tags, etc.
- Uma ferramenta de busca de tarefas para obter as tarefas do banco
- Ser capaz de listar todas as tarefas
- Ser capaz de adicionar informações a uma tarefa
- Ser capaz de buscar a documentação adicional do banco de dados
- Ser capaz de modificar a documentação adicional
- Tabelas do banco de dados precisam ser atualizadas para corresponder aos nossos novos modelos de dados

## EXEMPLOS & DOCUMENTAÇÃO:

Todos os exemplos já estão referenciados em prp_mcp_base.md - faça qualquer pesquisa adicional conforme necessário.

## OUTRAS CONSIDERAÇÕES:

- Não use regex complexo ou padrões de análise complexos, usamos um LLM para analisar PRPs.
- Modelo e chave da API para Anthropic ambos precisam ser variáveis de ambiente - estes estão configurados em .dev.vars.example
- É muito importante que criemos uma tarefa por arquivo para manter as preocupações separadas