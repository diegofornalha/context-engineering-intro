/**
 * Configuration management for the Turso MCP server
 */
import dotenv from 'dotenv';
import { z } from 'zod';
import { join } from 'path';

// Load multiple .env files with fallback
function loadMultipleEnvFiles(): void {
	// Define paths to try (in order of priority)
	const envPaths = [
		'.env',                    // Root project .env
		'.env.turso',              // Turso-specific .env
		'turso-config.env',        // Turso config file
		'env.turso',               // Turso environment file
		'mcp-turso-cloud/.env',    // MCP-specific .env
		'../.env',                 // Parent directory .env
		'../../.env',              // Grandparent directory .env
	];

	console.error('[Config] Loading environment files...');

	// Try to load each .env file
	for (const envPath of envPaths) {
		try {
			const result = dotenv.config({ path: envPath });
			if (result.parsed) {
				console.error(`[Config] ✅ Loaded: ${envPath}`);
			}
		} catch (error) {
			// Silently ignore if file doesn't exist
			console.error(`[Config] ⚠️ Skipped: ${envPath} (not found)`);
		}
	}

	// Also load the default .env in current directory
	try {
		dotenv.config();
		console.error('[Config] ✅ Loaded: default .env');
	} catch (error) {
		console.error('[Config] ⚠️ No default .env found');
	}
}

// Load environment variables from multiple .env files
loadMultipleEnvFiles();

// Define configuration schema as specified in the plan
export const ConfigSchema = z.object({
	// Organization-level authentication
	TURSO_API_TOKEN: z.string().min(1),
	TURSO_ORGANIZATION: z.string().min(1),

	// Optional default database
	TURSO_DEFAULT_DATABASE: z.string().optional(),

	// Database-specific authentication token
	TURSO_AUTH_TOKEN: z.string().optional(),

	// Token management settings
	TOKEN_EXPIRATION: z.string().default('7d'),
	TOKEN_PERMISSION: z
		.enum(['full-access', 'read-only'])
		.default('full-access'),
});

// Configuration type derived from schema
export type Config = z.infer<typeof ConfigSchema>;

// Parse environment variables using the schema
export function load_config(): Config {
	try {
		const config = ConfigSchema.parse({
			TURSO_API_TOKEN: process.env.TURSO_API_TOKEN,
			TURSO_ORGANIZATION: process.env.TURSO_ORGANIZATION,
			TURSO_DEFAULT_DATABASE: process.env.TURSO_DEFAULT_DATABASE,
			TURSO_AUTH_TOKEN: process.env.TURSO_AUTH_TOKEN,
			TOKEN_EXPIRATION: process.env.TOKEN_EXPIRATION || '7d',
			TOKEN_PERMISSION: process.env.TOKEN_PERMISSION || 'full-access',
		});

		console.error('[Config] ✅ Configuration loaded successfully');
		console.error(`[Config] Organization: ${config.TURSO_ORGANIZATION}`);
		console.error(`[Config] Default Database: ${config.TURSO_DEFAULT_DATABASE || 'not set'}`);

		return config;
	} catch (error) {
		if (error instanceof z.ZodError) {
			const missing_fields = error.issues
				.filter(
					(err: any) =>
						err.code === 'invalid_type' &&
						err.received === 'undefined',
				)
				.map((err: any) => err.path.join('.'));

			console.error('[Config] ❌ Missing required configuration:', missing_fields);
			console.error('[Config] Available environment variables:', Object.keys(process.env).filter(key => key.startsWith('TURSO_')));

			throw new Error(
				`Missing required configuration: ${missing_fields.join(
					', ',
				)}\n` +
					'Please set these environment variables or add them to your .env file.\n' +
					'Checked files: .env, .env.turso, mcp-turso-cloud/.env',
			);
		}
		throw error;
	}
}

// Singleton instance of the configuration
let config: Config | null = null;

// Get the configuration, loading it if necessary
export function get_config(): Config {
	if (!config) {
		config = load_config();
	}
	return config;
}
