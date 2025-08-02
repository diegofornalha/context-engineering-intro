/**
 * Hybrid configuration for Turso MCP server (Local + Cloud)
 */
import dotenv from 'dotenv';
import { z } from 'zod';

// Load environment variables
dotenv.config();

// Define hybrid configuration schema
export const HybridConfigSchema = z.object({
	// Mode selection
	TURSO_MODE: z.enum(['local', 'cloud', 'hybrid']).default('hybrid'),
	
	// Local configuration
	TURSO_LOCAL_URL: z.string().default('http://127.0.0.1:8080'),
	
	// Cloud configuration (optional for local mode)
	TURSO_API_TOKEN: z.string().optional(),
	TURSO_ORGANIZATION: z.string().optional(),
	TURSO_DEFAULT_DATABASE: z.string().optional(),
	
	// Token management settings
	TOKEN_EXPIRATION: z.string().default('7d'),
	TOKEN_PERMISSION: z.enum(['full-access', 'read-only']).default('full-access'),
});

export type HybridConfig = z.infer<typeof HybridConfigSchema>;

// Parse environment variables for hybrid mode
export function load_hybrid_config(): HybridConfig {
	const mode = process.env.TURSO_MODE || 'hybrid';
	
	try {
		// For local mode, we don't need cloud credentials
		if (mode === 'local') {
			return HybridConfigSchema.parse({
				TURSO_MODE: 'local',
				TURSO_LOCAL_URL: process.env.TURSO_LOCAL_URL || 'http://127.0.0.1:8080',
				TOKEN_EXPIRATION: process.env.TOKEN_EXPIRATION || '7d',
				TOKEN_PERMISSION: process.env.TOKEN_PERMISSION || 'full-access',
			});
		}
		
		// For cloud or hybrid mode, we need cloud credentials
		const config = HybridConfigSchema.parse({
			TURSO_MODE: mode,
			TURSO_LOCAL_URL: process.env.TURSO_LOCAL_URL || 'http://127.0.0.1:8080',
			TURSO_API_TOKEN: process.env.TURSO_API_TOKEN,
			TURSO_ORGANIZATION: process.env.TURSO_ORGANIZATION,
			TURSO_DEFAULT_DATABASE: process.env.TURSO_DEFAULT_DATABASE,
			TOKEN_EXPIRATION: process.env.TOKEN_EXPIRATION || '7d',
			TOKEN_PERMISSION: process.env.TOKEN_PERMISSION || 'full-access',
		});
		
		// Validate cloud credentials for cloud/hybrid mode
		if (mode !== 'local' && (!config.TURSO_API_TOKEN || !config.TURSO_ORGANIZATION)) {
			throw new Error('Cloud credentials required for cloud/hybrid mode');
		}
		
		return config;
	} catch (error) {
		if (error instanceof z.ZodError) {
			const missing = error.issues.map(i => i.path.join('.')).join(', ');
			throw new Error(`Configuration error: ${missing}`);
		}
		throw error;
	}
}

// Get hybrid config singleton
let hybridConfig: HybridConfig | null = null;

export function get_hybrid_config(): HybridConfig {
	if (!hybridConfig) {
		hybridConfig = load_hybrid_config();
	}
	return hybridConfig;
}

// Check if we should use local mode
export function is_local_mode(): boolean {
	const config = get_hybrid_config();
	return config.TURSO_MODE === 'local';
}

// Check if we should use cloud mode
export function is_cloud_mode(): boolean {
	const config = get_hybrid_config();
	return config.TURSO_MODE === 'cloud';
}

// Check if we should use hybrid mode
export function is_hybrid_mode(): boolean {
	const config = get_hybrid_config();
	return config.TURSO_MODE === 'hybrid';
}