/**
 * Enhanced Token Manager for Turso MCP
 * Based on official Turso documentation
 */
import { TursoApiError } from '../common/errors.js';
import { get_config } from '../config.js';
import * as organization_client from './organization.js';

// Token cache with expiration
interface CachedToken {
  token: string;
  expiresAt: number;
  permission: 'full-access' | 'read-only';
}

const token_cache: Record<string, CachedToken> = {};

/**
 * Get a database token with automatic refresh
 */
export async function get_database_token(
  database_name: string,
  permission: 'full-access' | 'read-only' = 'full-access',
): Promise<string> {
  const cache_key = `${database_name}:${permission}`;
  const cached = token_cache[cache_key];

  // Check if we have a valid cached token
  if (cached && Date.now() < cached.expiresAt) {
    return cached.token;
  }

  try {
    // Generate a new token
    const token = await organization_client.generate_database_token(
      database_name,
      permission,
    );

    // Cache the token with expiration (1 hour)
    token_cache[cache_key] = {
      token,
      expiresAt: Date.now() + 60 * 60 * 1000, // 1 hour
      permission,
    };

    return token;
  } catch (error) {
    throw new TursoApiError(
      `Failed to get token for database ${database_name}: ${
        (error as Error).message
      }`,
      500,
    );
  }
}

/**
 * Clear token cache for a specific database
 */
export function clear_token_cache(database_name?: string): void {
  if (database_name) {
    // Clear specific database tokens
    Object.keys(token_cache).forEach(key => {
      if (key.startsWith(`${database_name}:`)) {
        delete token_cache[key];
      }
    });
  } else {
    // Clear all tokens
    Object.keys(token_cache).forEach(key => {
      delete token_cache[key];
    });
  }
}

/**
 * Get token cache status
 */
export function get_token_cache_status(): Record<string, any> {
  const status: Record<string, any> = {};
  
  Object.entries(token_cache).forEach(([key, cached]) => {
    const [database, permission] = key.split(':');
    status[database] = {
      permission,
      expiresAt: new Date(cached.expiresAt).toISOString(),
      isValid: Date.now() < cached.expiresAt,
      timeToExpiry: Math.max(0, cached.expiresAt - Date.now()),
    };
  });

  return status;
}

/**
 * Validate token permissions
 */
export function validate_token_permissions(
  required_permission: 'full-access' | 'read-only',
  current_permission: 'full-access' | 'read-only',
): boolean {
  if (required_permission === 'read-only') {
    return true; // read-only can access read-only
  }
  
  if (required_permission === 'full-access') {
    return current_permission === 'full-access'; // full-access required for full-access
  }
  
  return false;
}
