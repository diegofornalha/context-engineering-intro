### Exemplo de uso da API Anthropic para Claude (modelo e chave da API são ambos variáveis de ambiente)

const response = await fetch('https://api.anthropic.com/v1/messages', {
method: 'POST',
headers: {
    'Content-Type': 'application/json',
    'x-api-key': this.apiKey,
    'anthropic-version': '2023-06-01'
},
body: JSON.stringify({
    model: this.model,
    max_tokens: 3000,
    messages: [{
    role: 'user',
    content: this.buildPRPParsingPrompt(prpContent, projectContext, config)
    }]
})
});

if (!response.ok) {
throw new Error(`Erro da API Anthropic: ${response.status} ${response.statusText}`);
}

const result = await response.json();
const content = (result as any).content[0].text;

// Analisar a resposta JSON
const aiTasks = JSON.parse(content);