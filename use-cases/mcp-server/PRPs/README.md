# Conceito de Product Requirement Prompt (PRP)

"Especificar demais o que construir enquanto sub-especifica o contexto, e como construí-lo, é por que tantas tentativas de codificação dirigidas por IA param em 80%. Um Product Requirement Prompt (PRP) corrige isso fundindo o escopo disciplinado de um Product Requirements Document (PRD) clássico com a mentalidade 'contexto-é-rei' da engenharia de prompts moderna."

## O que é um PRP?

Product Requirement Prompt (PRP)
Um PRP é um prompt estruturado que fornece a um agente de codificação de IA tudo o que ele precisa para entregar uma fatia vertical de software funcional—nada mais, nada menos.

### Como difere de um PRD

Um PRD tradicional esclarece o que o produto deve fazer e por que os clientes precisam dele, mas deliberadamente evita como será construído.

Um PRP mantém as seções de objetivo e justificativa de um PRD, mas adiciona três camadas críticas para IA:

### Contexto

- Caminhos de arquivo e conteúdo precisos, versões de biblioteca e contexto de biblioteca, exemplos de trechos de código. LLMs geram código de qualidade superior quando recebem referências diretas no prompt em vez de descrições amplas. Uso de um diretório ai_docs/ para canalizar documentação de biblioteca e outras.

### Detalhes de Implementação e Estratégia

- Em contraste com um PRD tradicional, um PRP declara explicitamente como o produto será construído. Isso inclui o uso de endpoints de API, executores de teste ou padrões de agente (ReAct, Plan-and-Execute) para usar. Uso de typehints, dependências, padrões arquiteturais e outras ferramentas para garantir que o código seja construído corretamente.

### Portões de Validação

- Verificações determinísticas como pytest, ruff ou passes de tipo estático. Controles de qualidade "Shift-left" capturam defeitos cedo e são mais baratos que retrabalho tardio.
  Exemplo: Cada nova função deve ser testada individualmente, Portão de validação = todos os testes passam.

### Por que a Camada PRP Existe

- A pasta PRP é usada para preparar e canalizar PRPs para o codificador agentico.

## Por que contexto é não-negociável

Saídas de modelos de linguagem grandes são limitadas por sua janela de contexto; contexto irrelevante ou ausente literalmente espreme tokens úteis

O mantra da indústria "Lixo Dentro → Lixo Fora" se aplica duplamente à engenharia de prompts e especialmente na engenharia agentica: entrada descuidada produz código frágil

## Em resumo

Um PRP é PRD + inteligência de codebase curada + agente/runbook—o pacote mínimo viável que uma IA precisa para plausivelmente enviar código pronto para produção na primeira tentativa.

O PRP pode ser pequeno e focado em uma única tarefa ou grande e cobrindo múltiplas tarefas.
O verdadeiro poder do PRP está na capacidade de encadear tarefas juntas em um PRP para construir, auto-validar e enviar funcionalidades complexas.
