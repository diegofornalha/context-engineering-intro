/**
 * Unified tool handler for the Turso MCP server
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
	CallToolRequestSchema,
	ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import * as database_client from '../clients/database.js';
import * as organization_client from '../clients/organization.js';
import { ResultSet } from '../common/types.js';
import {
	resolve_database_name,
	set_current_database,
} from './context.js';

/**
 * Register all tools with the server
 */
export function register_tools(server: Server): void {
	// Register the list of available tools
	server.setRequestHandler(ListToolsRequestSchema, async () => ({
		tools: [
			// Organization tools
			{
				name: 'list_databases',
				description: 'List all databases in your Turso organization',
				inputSchema: {
					type: 'object',
					properties: {},
					required: [],
				},
			},
			{
				name: 'create_database',
				description: `✓ SAFE: Create a new database in your Turso organization. Database name must be unique.`,
				inputSchema: {
					type: 'object',
					properties: {
						name: {
							type: 'string',
							description:
								'Name of the database to create - Must be unique within organization',
						},
						group: {
							type: 'string',
							description:
								'Optional group name for the database (defaults to "default")',
						},
						regions: {
							type: 'array',
							items: {
								type: 'string',
							},
							description:
								'Optional list of regions to deploy the database to (affects latency and compliance)',
						},
					},
					required: ['name'],
				},
			},
			{
				name: 'delete_database',
				description: `⚠️ DESTRUCTIVE: Permanently deletes a database and ALL its data. Cannot be undone. Always confirm with user before proceeding and verify correct database name.`,
				inputSchema: {
					type: 'object',
					properties: {
						name: {
							type: 'string',
							description:
								'Name of the database to permanently delete - WARNING: ALL DATA WILL BE LOST FOREVER',
						},
					},
					required: ['name'],
				},
			},
			{
				name: 'generate_database_token',
				description: 'Generate a new token for a specific database',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description:
								'Name of the database to generate a token for',
						},
						permission: {
							type: 'string',
							enum: ['full-access', 'read-only'],
							description: 'Permission level for the token',
						},
					},
					required: ['database'],
				},
			},

			// Database tools
			{
				name: 'list_tables',
				description: 'Lists all tables in a database',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description:
								'Database name (optional, uses context if not provided)',
						},
					},
					required: [],
				},
			},
			{
				name: 'execute_read_only_query',
				description: `✓ SAFE: Execute read-only SQL queries (SELECT, PRAGMA, EXPLAIN). Automatically rejects write operations.`,
				inputSchema: {
					type: 'object',
					properties: {
						query: {
							type: 'string',
							description:
								'Read-only SQL query to execute (SELECT, PRAGMA, EXPLAIN only)',
						},
						params: {
							type: 'object',
							description:
								'Query parameters (optional) - Use parameterized queries for security',
						},
						database: {
							type: 'string',
							description:
								'Database name (optional, uses context if not provided) - Specify target database',
						},
					},
					required: ['query'],
				},
			},
			{
				name: 'execute_query',
				description:
					`⚠️ DESTRUCTIVE: Execute SQL that can modify/delete data (INSERT, UPDATE, DELETE, DROP, ALTER). Always confirm with user before destructive operations.`,
				inputSchema: {
					type: 'object',
					properties: {
						query: {
							type: 'string',
							description:
								'SQL query to execute - WARNING: Can permanently modify or delete data. Use with extreme caution.',
						},
						params: {
							type: 'object',
							description:
								'Query parameters (optional) - Use parameterized queries to prevent SQL injection',
						},
						database: {
							type: 'string',
							description:
								'Database name (optional, uses context if not provided) - Verify correct database before destructive operations',
						},
					},
					required: ['query'],
				},
			},
			{
				name: 'describe_table',
				description: 'Gets schema information for a table',
				inputSchema: {
					type: 'object',
					properties: {
						table: {
							type: 'string',
							description: 'Table name',
						},
						database: {
							type: 'string',
							description:
								'Database name (optional, uses context if not provided)',
						},
					},
					required: ['table'],
				},
			},
			{
				name: 'vector_search',
				description: 'Performs vector similarity search',
				inputSchema: {
					type: 'object',
					properties: {
						table: {
							type: 'string',
							description: 'Table name',
						},
						vector_column: {
							type: 'string',
							description: 'Column containing vectors',
						},
						query_vector: {
							type: 'array',
							items: {
								type: 'number',
							},
							description: 'Query vector for similarity search',
						},
						limit: {
							type: 'number',
							description:
								'Maximum number of results (optional, default 10)',
						},
						database: {
							type: 'string',
							description:
								'Database name (optional, uses context if not provided)',
						},
					},
					required: ['table', 'vector_column', 'query_vector'],
				},
			},

			// Memory System Tools (Migrated from mcp-turso)
			{
				name: 'add_conversation',
				description: 'Add a conversation to memory',
				inputSchema: {
					type: 'object',
					properties: {
						session_id: {
							type: 'string',
							description: 'Session identifier',
						},
						user_id: {
							type: 'string',
							description: 'User identifier (optional)',
						},
						message: {
							type: 'string',
							description: 'User message',
						},
						response: {
							type: 'string',
							description: 'AI response (optional)',
						},
						context: {
							type: 'string',
							description: 'Additional context (optional)',
						},
						database: {
							type: 'string',
							description: 'Database name (optional, uses context if not provided)',
						},
					},
					required: ['session_id', 'message'],
				},
			},
			{
				name: 'get_conversations',
				description: 'Get conversations from memory',
				inputSchema: {
					type: 'object',
					properties: {
						session_id: {
							type: 'string',
							description: 'Session identifier (optional)',
						},
						limit: {
							type: 'number',
							description: 'Number of conversations to retrieve (optional)',
						},
						database: {
							type: 'string',
							description: 'Database name (optional, uses context if not provided)',
						},
					},
					required: [],
				},
			},
			{
				name: 'add_knowledge',
				description: 'Add knowledge to the knowledge base',
				inputSchema: {
					type: 'object',
					properties: {
						topic: {
							type: 'string',
							description: 'Knowledge topic',
						},
						content: {
							type: 'string',
							description: 'Knowledge content',
						},
						source: {
							type: 'string',
							description: 'Source of knowledge (optional)',
						},
						tags: {
							type: 'string',
							description: 'Comma-separated tags (optional)',
						},
						database: {
							type: 'string',
							description: 'Database name (optional, uses context if not provided)',
						},
					},
					required: ['topic', 'content'],
				},
			},
			{
				name: 'search_knowledge',
				description: 'Search knowledge base',
				inputSchema: {
					type: 'object',
					properties: {
						query: {
							type: 'string',
							description: 'Search query',
						},
						tags: {
							type: 'string',
							description: 'Filter by tags (optional)',
						},
						limit: {
							type: 'number',
							description: 'Number of results (optional)',
						},
						database: {
							type: 'string',
							description: 'Database name (optional, uses context if not provided)',
						},
					},
					required: ['query'],
				},
			},
			{
				name: 'setup_memory_tables',
				description: 'Setup memory system tables (conversations and knowledge_base)',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name (optional, uses context if not provided)',
						},
					},
					required: [],
				},
			},

			// Enhanced Database Management Tools (Based on Turso Docs)
			{
				name: 'get_database_info',
				description: 'Get detailed information about a database',
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
			{
				name: 'list_database_tokens',
				description: 'List all tokens for a database',
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
			{
				name: 'create_database_token',
				description: 'Create a new token for a database',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name',
						},
						permission: {
							type: 'string',
							enum: ['full-access', 'read-only'],
							description: 'Permission level for the token',
						},
						expiration: {
							type: 'string',
							description: 'Token expiration (ISO format, optional)',
						},
					},
					required: ['database'],
				},
			},
			{
				name: 'revoke_database_token',
				description: 'Revoke a database token',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name',
						},
						token_id: {
							type: 'string',
							description: 'Token ID to revoke',
						},
					},
					required: ['database', 'token_id'],
				},
			},
			{
				name: 'get_database_usage',
				description: 'Get database usage metrics',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name',
						},
						period: {
							type: 'string',
							enum: ['1h', '24h', '7d', '30d'],
							description: 'Time period for metrics',
						},
					},
					required: ['database'],
				},
			},
			{
				name: 'backup_database',
				description: 'Create a backup of a database',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name',
						},
						backup_name: {
							type: 'string',
							description: 'Name for the backup (optional)',
						},
					},
					required: ['database'],
				},
			},
			{
				name: 'restore_database',
				description: 'Restore a database from backup',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name',
						},
						backup_id: {
							type: 'string',
							description: 'Backup ID to restore from',
						},
					},
					required: ['database', 'backup_id'],
				},
			},
			{
				name: 'get_token_cache_status',
				description: 'Get status of cached tokens',
				inputSchema: {
					type: 'object',
					properties: {},
					required: [],
				},
			},
			{
				name: 'clear_token_cache',
				description: 'Clear cached tokens',
				inputSchema: {
					type: 'object',
					properties: {
						database: {
							type: 'string',
							description: 'Database name (optional, clears all if not provided)',
						},
					},
					required: [],
				},
			},
		],
	}));

	// Register the unified tool handler
	server.setRequestHandler(CallToolRequestSchema, async (request) => {
		try {
			// Organization tools

			// Handle list_databases tool
			if (request.params.name === 'list_databases') {
				const databases = await organization_client.list_databases();

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify({ databases }, null, 2),
						},
					],
				};
			}

			// Handle create_database tool
			if (request.params.name === 'create_database') {
				const { name, group, regions } = request.params.arguments as {
					name: string;
					group?: string;
					regions?: string[];
				};

				const database = await organization_client.create_database(
					name,
					{
						group,
						regions,
					},
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify({ database }, null, 2),
						},
					],
				};
			}

			// Handle delete_database tool
			if (request.params.name === 'delete_database') {
				const { name } = request.params.arguments as { name: string };

				await organization_client.delete_database(name);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									success: true,
									message: `Database '${name}' deleted successfully`,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle generate_database_token tool
			if (request.params.name === 'generate_database_token') {
				const { database, permission = 'full-access' } = request
					.params.arguments as {
					database: string;
					permission?: 'full-access' | 'read-only';
				};

				const jwt = await organization_client.generate_database_token(
					database,
					permission,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									success: true,
									database,
									token: {
										jwt,
										permission,
										database,
									},
									message: `Token generated successfully for database '${database}' with '${permission}' permissions`,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Database tools

			// Handle list_tables tool
			if (request.params.name === 'list_tables') {
				const { database } = request.params.arguments as {
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				const tables = await database_client.list_tables(
					database_name,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									tables,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle execute_read_only_query tool
			if (request.params.name === 'execute_read_only_query') {
				const {
					query,
					params = {},
					database,
				} = request.params.arguments as {
					query: string;
					params?: Record<string, any>;
					database?: string;
				};

				// Validate that this is a read-only query
				const normalized_query = query.trim().toLowerCase();
				if (
					!normalized_query.startsWith('select') &&
					!normalized_query.startsWith('pragma')
				) {
					throw new Error(
						'Only SELECT and PRAGMA queries are allowed with execute_read_only_query',
					);
				}

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				const result = await database_client.execute_query(
					database_name,
					query,
					params,
				);

				// Format the result for better readability
				const formatted_result = format_query_result(result);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									query,
									result: formatted_result,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle execute_query tool
			if (request.params.name === 'execute_query') {
				const {
					query,
					params = {},
					database,
				} = request.params.arguments as {
					query: string;
					params?: Record<string, any>;
					database?: string;
				};

				// Validate that this is not a read-only query
				const normalized_query = query.trim().toLowerCase();
				if (
					normalized_query.startsWith('select') ||
					normalized_query.startsWith('pragma')
				) {
					throw new Error(
						'SELECT and PRAGMA queries should use execute_read_only_query',
					);
				}

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				const result = await database_client.execute_query(
					database_name,
					query,
					params,
				);

				// Format the result for better readability
				const formatted_result = format_query_result(result);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									query,
									result: formatted_result,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle describe_table tool
			if (request.params.name === 'describe_table') {
				const { table, database } = request.params.arguments as {
					table: string;
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				const columns = await database_client.describe_table(
					database_name,
					table,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									table,
									columns: columns.map((col) => ({
										name: col.name,
										type: col.type,
										nullable: col.notnull === 0,
										default_value: col.dflt_value,
										primary_key: col.pk === 1,
									})),
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle vector_search tool
			if (request.params.name === 'vector_search') {
				const {
					table,
					vector_column,
					query_vector,
					limit = 10,
					database,
				} = request.params.arguments as {
					table: string;
					vector_column: string;
					query_vector: number[];
					limit?: number;
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				// Construct a vector search query using SQLite's vector functions
				// This assumes the vector column is stored in a format compatible with SQLite's vector1 extension
				const vector_string = query_vector.join(',');
				const query = `
          SELECT *, vector_distance(${vector_column}, vector_from_json(?)) as distance
          FROM ${table}
          ORDER BY distance ASC
          LIMIT ?
        `;

				const params = {
					1: `[${vector_string}]`,
					2: limit,
				};

				const result = await database_client.execute_query(
					database_name,
					query,
					params,
				);

				// Format the result for better readability
				const formatted_result = format_query_result(result);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									table,
									vector_column,
									query_vector,
									results: formatted_result,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Memory System Tools

			// Handle setup_memory_tables tool
			if (request.params.name === 'setup_memory_tables') {
				const { database } = request.params.arguments as {
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				// Create conversations table
				const conversations_table_query = `
					CREATE TABLE IF NOT EXISTS conversations (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						session_id TEXT NOT NULL,
						user_id TEXT,
						message TEXT NOT NULL,
						response TEXT,
						context TEXT,
						timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
					)
				`;

				// Create knowledge_base table
				const knowledge_table_query = `
					CREATE TABLE IF NOT EXISTS knowledge_base (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						topic TEXT NOT NULL,
						content TEXT NOT NULL,
						source TEXT,
						tags TEXT,
						priority INTEGER DEFAULT 1,
						created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
						updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
					)
				`;

				await database_client.execute_query(database_name, conversations_table_query);
				await database_client.execute_query(database_name, knowledge_table_query);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									success: true,
									database: database_name,
									message: 'Memory system tables created successfully',
									tables: ['conversations', 'knowledge_base'],
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle add_conversation tool
			if (request.params.name === 'add_conversation') {
				const {
					session_id,
					user_id,
					message,
					response,
					context,
					database,
				} = request.params.arguments as {
					session_id: string;
					user_id?: string;
					message: string;
					response?: string;
					context?: string;
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				const insert_query = `
					INSERT INTO conversations (session_id, user_id, message, response, context)
					VALUES (:session_id, :user_id, :message, :response, :context)
				`;

				const params = {
					':session_id': session_id,
					':user_id': user_id || null,
					':message': message,
					':response': response || null,
					':context': context || null,
				};

				const result = await database_client.execute_query(
					database_name,
					insert_query,
					params,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									success: true,
									database: database_name,
									conversation_id: result.lastInsertRowid,
									message: 'Conversation added successfully',
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle get_conversations tool
			if (request.params.name === 'get_conversations') {
				const {
					session_id,
					limit,
					database,
				} = request.params.arguments as {
					session_id?: string;
					limit?: number;
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				let query = 'SELECT * FROM conversations';
				const params: Record<string, any> = {};

				if (session_id) {
					query += ` WHERE session_id = :session_id`;
					params[':session_id'] = session_id;
				}

				query += ' ORDER BY timestamp DESC';

				if (limit) {
					query += ' LIMIT :limit';
					params[':limit'] = limit;
				}

				const result = await database_client.execute_query(
					database_name,
					query,
					params,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									conversations: result.rows,
									total: result.rows.length,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle add_knowledge tool
			if (request.params.name === 'add_knowledge') {
				const {
					topic,
					content,
					source,
					tags,
					database,
				} = request.params.arguments as {
					topic: string;
					content: string;
					source?: string;
					tags?: string;
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				const insert_query = `
					INSERT INTO knowledge_base (topic, content, source, tags)
					VALUES (:topic, :content, :source, :tags)
				`;

				const params = {
					':topic': topic,
					':content': content,
					':source': source || null,
					':tags': tags || null,
				};

				const result = await database_client.execute_query(
					database_name,
					insert_query,
					params,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									success: true,
									database: database_name,
									knowledge_id: result.lastInsertRowid,
									message: 'Knowledge added successfully',
								},
								null,
								2,
							),
						},
					],
				};
			}

			// Handle search_knowledge tool
			if (request.params.name === 'search_knowledge') {
				const {
					query,
					tags,
					limit,
					database,
				} = request.params.arguments as {
					query: string;
					tags?: string;
					limit?: number;
					database?: string;
				};

				const database_name = resolve_database_name(database);

				// Update context if database is explicitly provided
				if (database) {
					set_current_database(database);
				}

				let search_query = `
					SELECT * FROM knowledge_base 
					WHERE topic LIKE :query1 OR content LIKE :query2
				`;
				const params: Record<string, any> = {
					':query1': `%${query}%`,
					':query2': `%${query}%`,
				};

				if (tags) {
					search_query += ' AND tags LIKE :tags';
					params[':tags'] = `%${tags}%`;
				}

				search_query += ' ORDER BY priority DESC, created_at DESC';

				if (limit) {
					search_query += ' LIMIT :limit';
					params[':limit'] = limit;
				}

				const result = await database_client.execute_query(
					database_name,
					search_query,
					params,
				);

				return {
					content: [
						{
							type: 'text',
							text: JSON.stringify(
								{
									database: database_name,
									query,
									results: result.rows,
									total: result.rows.length,
								},
								null,
								2,
							),
						},
					],
				};
			}

			// If we get here, it's not a recognized tool
			throw new Error(`Unknown tool: ${request.params.name}`);
		} catch (error) {
			console.error('Error executing tool:', error);
			return {
				content: [
					{
						type: 'text',
						text: `Error: ${(error as Error).message}`,
					},
				],
				isError: true,
			};
		}
	});
}

/**
 * Format a query result for better readability
 * Handles BigInt serialization
 */
function format_query_result(result: ResultSet): any {
	// Convert BigInt to string to avoid serialization issues
	const lastInsertRowid =
		result.lastInsertRowid !== null &&
		typeof result.lastInsertRowid === 'bigint'
			? result.lastInsertRowid.toString()
			: result.lastInsertRowid;

	return {
		rows: result.rows,
		rowsAffected: result.rowsAffected,
		lastInsertRowid: lastInsertRowid,
		columns: result.columns,
	};
}
