/**
 * Hybrid database client for local and cloud Turso databases
 */
import { createClient, type Client, type InStatement } from '@libsql/client';
import { get_hybrid_config, is_local_mode } from '../config-hybrid.js';
import type { DatabaseTool } from '../common/types.js';

export class HybridDatabaseClient {
	private local_client: Client | null = null;
	
	/**
	 * Get or create local database client
	 */
	private get_local_client(): Client {
		if (!this.local_client) {
			const config = get_hybrid_config();
			this.local_client = createClient({
				url: config.TURSO_LOCAL_URL,
			});
		}
		return this.local_client;
	}
	
	/**
	 * Execute a query (local or cloud)
	 */
	async execute_query(query: string, database?: string): Promise<DatabaseTool> {
		// For local mode, always use local client
		if (is_local_mode()) {
			const client = this.get_local_client();
			const result = await client.execute(query);
			
			return {
				rows: result.rows as Record<string, unknown>[],
				columns: result.columns || [],
				rowsAffected: result.rowsAffected || 0,
				lastInsertRowid: result.lastInsertRowid?.toString(),
			};
		}
		
		// For cloud mode, delegate to cloud implementation
		// This would need the cloud client implementation
		throw new Error('Cloud mode not implemented in hybrid client yet');
	}
	
	/**
	 * Execute a read-only query (safe for all modes)
	 */
	async execute_read_only_query(query: string, database?: string): Promise<DatabaseTool> {
		// Validate it's actually read-only
		const normalized = query.trim().toUpperCase();
		const allowed_starts = ['SELECT', 'PRAGMA', 'EXPLAIN', 'WITH'];
		
		if (!allowed_starts.some(start => normalized.startsWith(start))) {
			throw new Error('Query must be read-only (SELECT, PRAGMA, EXPLAIN, or WITH)');
		}
		
		return this.execute_query(query, database);
	}
	
	/**
	 * List databases (local mode returns fixed response)
	 */
	async list_databases(): Promise<Array<{ name: string; regions?: string[] }>> {
		if (is_local_mode()) {
			// For local mode, return a fixed local database
			return [{
				name: 'local',
				regions: ['local'],
			}];
		}
		
		// For cloud mode, would need to implement API call
		throw new Error('Cloud mode not implemented in hybrid client yet');
	}
	
	/**
	 * Get database info
	 */
	async get_database_info(database: string): Promise<any> {
		if (is_local_mode()) {
			const client = this.get_local_client();
			
			// Get table count
			const tables = await client.execute(`
				SELECT COUNT(*) as count 
				FROM sqlite_master 
				WHERE type='table' AND name NOT LIKE 'sqlite_%'
			`);
			
			// Get database size (approximate)
			const pages = await client.execute('PRAGMA page_count');
			const pageSize = await client.execute('PRAGMA page_size');
			
			const pageCount = Number(pages.rows[0]?.page_count || 0);
			const pageSizeBytes = Number(pageSize.rows[0]?.page_size || 0);
			const sizeBytes = pageCount * pageSizeBytes;
			
			return {
				name: 'local',
				tables: Number(tables.rows[0]?.count || 0),
				size: `${(sizeBytes / 1024 / 1024).toFixed(2)} MB`,
				location: 'Local (127.0.0.1:8080)',
			};
		}
		
		// For cloud mode, would need to implement API call
		throw new Error('Cloud mode not implemented in hybrid client yet');
	}
	
	/**
	 * Close connections
	 */
	close(): void {
		if (this.local_client) {
			this.local_client.close();
			this.local_client = null;
		}
	}
}