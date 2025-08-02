import { createServer, IncomingMessage, ServerResponse } from 'http';
import { get_hybrid_config, is_local_mode, is_cloud_mode, is_hybrid_mode } from './config-hybrid.js';

export class WebServer {
    private port: number;
    private config: any;
    
    constructor(port: number = 3000) {
        this.port = port;
        this.config = get_hybrid_config();
    }
    
    private getStatusPage(): string {
        const mode = this.config.TURSO_MODE;
        const modeEmoji = mode === 'local' ? '🏠' : mode === 'cloud' ? '☁️' : '🔄';
        
        return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Turso Server - Status</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #00d1b2;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }
        .status.online {
            background: #00d1b2;
            color: white;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .info-card {
            background: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        .info-card h3 {
            margin-top: 0;
            color: #555;
        }
        .tool {
            background: #fff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .tool-name {
            font-weight: bold;
            color: #00d1b2;
        }
        .tool-desc {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #e0e0e0;
        }
        .example {
            margin-top: 10px;
        }
        .endpoint {
            margin: 10px 0;
            padding: 10px;
            background: #f9f9f9;
            border-left: 3px solid #00d1b2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>
            ${modeEmoji} MCP Turso Server
            <span class="status online">● Online</span>
        </h1>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>📊 Informações do Servidor</h3>
                <p><strong>Modo:</strong> ${mode.toUpperCase()}</p>
                <p><strong>Versão:</strong> 1.0.0</p>
                ${is_local_mode() ? 
                    `<p><strong>URL Local:</strong> <code>${this.config.TURSO_LOCAL_URL}</code></p>` :
                    `<p><strong>Organização:</strong> <code>${this.config.TURSO_ORGANIZATION || 'não configurada'}</code></p>`
                }
                <p><strong>Status da Página:</strong> <code>http://localhost:${this.port}</code></p>
            </div>
            
            <div class="info-card">
                <h3>🔧 Ferramentas MCP Disponíveis</h3>
                <div class="tool">
                    <div class="tool-name">execute_read_only_query</div>
                    <div class="tool-desc">Executa queries SQL somente leitura (SELECT, PRAGMA)</div>
                </div>
                <div class="tool">
                    <div class="tool-name">execute_query</div>
                    <div class="tool-desc">Executa qualquer query SQL (incluindo operações destrutivas)</div>
                </div>
                <div class="tool">
                    <div class="tool-name">list_databases</div>
                    <div class="tool-desc">Lista todos os bancos de dados disponíveis</div>
                </div>
                <div class="tool">
                    <div class="tool-name">get_database_info</div>
                    <div class="tool-desc">Obtém informações sobre um banco específico</div>
                </div>
            </div>
        </div>
        
        <div class="info-card" style="margin-top: 20px;">
            <h3>🚀 Como Usar</h3>
            <p>Este servidor implementa o Model Context Protocol (MCP) para integração com LLMs. Para usar:</p>
            
            <div class="example">
                <h4>1. Adicionar ao Claude Desktop</h4>
                <pre>npx @diegofornalha/mcp-turso-cloud add</pre>
            </div>
            
            <div class="example">
                <h4>2. Configurar manualmente</h4>
                <pre>{
  "mcpServers": {
    "turso-local": {
      "command": "node",
      "args": ["${this.getServerPath()}/dist/index-hybrid.js"],
      "env": {
        "TURSO_MODE": "local"
      }
    }
  }
}</pre>
            </div>
        </div>
        
        <div class="info-card" style="margin-top: 20px;">
            <h3>🌐 Endpoints da API</h3>
            <div class="endpoint">
                <strong>GET /</strong> - Esta página de status
            </div>
            <div class="endpoint">
                <strong>GET /health</strong> - Health check (retorna JSON)
            </div>
            <div class="endpoint">
                <strong>GET /tools</strong> - Lista de ferramentas MCP disponíveis
            </div>
        </div>
    </div>
</body>
</html>`;
    }
    
    private getServerPath(): string {
        return process.cwd();
    }
    
    private async handleRequest(req: IncomingMessage, res: ServerResponse) {
        const url = new URL(req.url || '/', `http://localhost:${this.port}`);
        
        // CORS headers
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        
        if (req.method === 'OPTIONS') {
            res.writeHead(200);
            res.end();
            return;
        }
        
        switch (url.pathname) {
            case '/':
                res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end(this.getStatusPage());
                break;
                
            case '/health':
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: 'healthy',
                    mode: this.config.TURSO_MODE,
                    timestamp: new Date().toISOString()
                }));
                break;
                
            case '/tools':
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    tools: [
                        {
                            name: 'execute_read_only_query',
                            description: 'Execute a read-only SQL query (SELECT, PRAGMA, etc)',
                            mode: this.config.TURSO_MODE
                        },
                        {
                            name: 'execute_query',
                            description: 'Execute any SQL query (including destructive operations)',
                            mode: this.config.TURSO_MODE
                        },
                        {
                            name: 'list_databases',
                            description: 'List all available databases',
                            mode: this.config.TURSO_MODE
                        },
                        {
                            name: 'get_database_info',
                            description: 'Get information about a specific database',
                            mode: this.config.TURSO_MODE
                        }
                    ]
                }));
                break;
                
            default:
                res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
                res.end('<h1>404 - Página não encontrada</h1>');
        }
    }
    
    start(): Promise<void> {
        return new Promise((resolve, reject) => {
            const server = createServer((req, res) => this.handleRequest(req, res));
            
            server.listen(this.port, () => {
                console.error(`📄 Página de status disponível em: http://localhost:${this.port}`);
                resolve();
            });
            
            server.on('error', (err: any) => {
                if (err.code === 'EADDRINUSE') {
                    console.error(`⚠️  Porta ${this.port} já está em uso. Página web não será iniciada.`);
                    resolve(); // Não falhar se a porta estiver em uso
                } else {
                    reject(err);
                }
            });
        });
    }
}