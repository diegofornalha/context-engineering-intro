/**
 * Common type definitions for the Turso MCP server
 */
import { IntMode, ResultSet } from '@libsql/client';

// Organization-level types
export interface Database {
	name: string;
	id: string;
	region: string;
	group?: string;
	created_at: string;
}

// Token management types
export interface CachedToken {
	jwt: string;
	expiresAt: Date;
	permission: 'full-access' | 'read-only';
}

export interface TokenCache {
	[databaseName: string]: CachedToken;
}

// Context management
export interface DatabaseContext {
	currentDatabase?: string;
}

// Database tool response type
export interface DatabaseTool {
	rows: Record<string, unknown>[];
	columns: string[];
	rowsAffected: number;
	lastInsertRowid?: string;
}

// Re-export types from @libsql/client for consistency
export { IntMode, ResultSet };
