#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { get_hybrid_config, is_local_mode } from './config-hybrid.js';
import { HybridDatabaseClient } from './clients/database-hybrid.js';
import { WebServer } from './web-server.js';
// import { ErrorCode } from './common/errors.js';

// Get configuration
const config = get_hybrid_config();

/**
 * Hybrid Turso MCP Server (Local + Cloud)
 */
class HybridTursoServer {
	private server: Server;
	private db_client: HybridDatabaseClient;
	
	constructor() {
		this.db_client = new HybridDatabaseClient();
		
		// Initialize server
		this.server = new Server({
			name: 'mcp-turso-hybrid',
			version: '1.0.0',
		}, {
			capabilities: {
				resources: {},
				tools: {},
			},
		});
		
		// Setup request handlers
		this.setup_handlers();
	}
	
	private setup_handlers(): void {
		// List available tools
		this.server.setRequestHandler(ListToolsRequestSchema, async () => {
			const tools = [
				{
					name: 'execute_read_only_query',
					description: 'Execute a read-only SQL query (SELECT, PRAGMA, etc)',
					inputSchema: {
						type: 'object',
						properties: {
							query: {
								type: 'string',
								description: 'The SQL query to execute',
							},
							database: {
								type: 'string',
								description: 'Database name (optional)',
							},
						},
						required: ['query'],
					},
				},
				{
					name: 'execute_query',
					description: 'Execute any SQL query (including destructive operations)',
					inputSchema: {
						type: 'object',
						properties: {
							query: {
								type: 'string',
								description: 'The SQL query to execute',
							},
							database: {
								type: 'string',
								description: 'Database name (optional)',
							},
						},
						required: ['query'],
					},
				},
				{
					name: 'list_databases',
					description: 'List all available databases',
					inputSchema: {
						type: 'object',
						properties: {},
					},
				},
				{
					name: 'get_database_info',
					description: 'Get information about a specific database',
					inputSchema: {
						type: 'object',
						properties: {
							database: {
								type: 'string',
								description: 'Database name',
							},
						},
						required: ['database'],
					},
				},
			];
			
			// Add mode info to descriptions
			const mode = config.TURSO_MODE;
			return {
				tools: tools.map(tool => ({
					...tool,
					description: `${tool.description} [Mode: ${mode}]`,
				})),
			};
		});
		
		// Handle tool calls
		this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
			const { name, arguments: args } = request.params as { name: string; arguments?: any };
			
			try {
				switch (name) {
					case 'execute_read_only_query':
						const readResult = await this.db_client.execute_read_only_query(
							args?.query || '',
							args?.database
						);
						return {
							content: [{
								type: 'text',
								text: JSON.stringify(readResult, null, 2),
							}],
						};
						
					case 'execute_query':
						const result = await this.db_client.execute_query(
							args?.query || '',
							args?.database
						);
						return {
							content: [{
								type: 'text',
								text: JSON.stringify(result, null, 2),
							}],
						};
						
					case 'list_databases':
						const databases = await this.db_client.list_databases();
						return {
							content: [{
								type: 'text',
								text: JSON.stringify(databases, null, 2),
							}],
						};
						
					case 'get_database_info':
						const info = await this.db_client.get_database_info(args?.database || 'local');
						return {
							content: [{
								type: 'text',
								text: JSON.stringify(info, null, 2),
							}],
						};
						
					default:
						throw new Error(`Unknown tool: ${name}`);
				}
			} catch (error: any) {
				return {
					content: [{
						type: 'text',
						text: `Error: ${error.message}`,
					}],
					isError: true,
				};
			}
		});
	}
	
	async start(): Promise<void> {
		const mode = config.TURSO_MODE;
		console.error(`Starting Hybrid Turso MCP Server in ${mode.toUpperCase()} mode...`);
		
		if (is_local_mode()) {
			console.error(`Local URL: ${config.TURSO_LOCAL_URL}`);
		} else {
			console.error(`Organization: ${config.TURSO_ORGANIZATION}`);
			console.error(`Default Database: ${config.TURSO_DEFAULT_DATABASE || 'not set'}`);
		}
		
		const transport = new StdioServerTransport();
		await this.server.connect(transport);
		console.error('Server started successfully');
	}
}

// Main entry point
async function main() {
	try {
		// Iniciar servidor web para página de status
		const webServer = new WebServer(3000);
		await webServer.start();
		
		// Iniciar servidor MCP
		const server = new HybridTursoServer();
		await server.start();
	} catch (error: any) {
		console.error('Failed to start server:', error.message);
		process.exit(1);
	}
}

// Start the server
main().catch(console.error);