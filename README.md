# Context Engineering Intro

Um projeto introdutório sobre engenharia de contexto, demonstrando diferentes padrões e técnicas para trabalhar com IAs generativas.

## 📋 Descrição

Este projeto contém exemplos práticos de como implementar e trabalhar com diferentes padrões de engenharia de contexto, incluindo:

- **MCP Server**: Implementação de um servidor Model Context Protocol
- **Pydantic AI**: Exemplos de uso do Pydantic AI para validação de dados
- **Template Generator**: Gerador de templates para projetos de IA

## 🚀 Estrutura do Projeto

```
context-engineering-intro/
├── use-cases/
│   ├── mcp-server/          # Servidor MCP com autenticação e banco de dados
│   ├── pydantic-ai/         # Exemplos de uso do Pydantic AI
│   └── template-generator/  # Gerador de templates
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Pydantic AI** - Para validação e estruturação de dados
- **FastAPI** - Para APIs web
- **SQLAlchemy** - Para ORM
- **TypeScript/Node.js** - Para o servidor MCP
- **Vitest** - Para testes

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/context-engineering-intro.git
cd context-engineering-intro
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Casos de Uso

### MCP Server
O servidor MCP demonstra como implementar o Model Context Protocol com:
- Autenticação OAuth
- Operações de banco de dados
- Ferramentas customizadas
- Testes unitários

### Pydantic AI
Exemplos de como usar o Pydantic AI para:
- Agentes estruturados
- Validação de dados
- Integração com diferentes provedores de IA

### Template Generator
Gerador de templates para acelerar o desenvolvimento de projetos de IA.

## 🧪 Testes

Para executar os testes:

```bash
# Testes Python
pytest

# Testes TypeScript (no diretório mcp-server)
cd use-cases/mcp-server
npm test
```

## 📚 Documentação

Cada caso de uso possui sua própria documentação:
- [MCP Server](use-cases/mcp-server/README.md)
- [Pydantic AI](use-cases/pydantic-ai/README.md)
- [Template Generator](use-cases/template-generator/README.md)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- Seu Nome - [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- [Pydantic AI](https://github.com/jxnl/pydantic-ai) pela biblioteca incrível
- [Model Context Protocol](https://modelcontextprotocol.io/) pela especificação
- Comunidade de engenharia de contexto