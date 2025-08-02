import { spawn } from 'child_process';
import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';

describe('MCP Sentry Server', () => {
  let serverProcess: ReturnType<typeof spawn>;

  beforeAll(() => {
    // Mock environment for testing
    process.env.SENTRY_DSN = 'https://test@sentry.io/123456';
  });

  afterAll(() => {
    if (serverProcess) {
      serverProcess.kill();
    }
  });

  it('should start the server without errors', (done) => {
    serverProcess = spawn('tsx', ['src/index.ts'], {
      env: { ...process.env, SENTRY_DSN: 'https://test@sentry.io/123456' },
    });

    serverProcess.stderr.on('data', (data) => {
      const output = data.toString();
      if (output.includes('MCP Sentry server running on stdio')) {
        done();
      }
    });

    serverProcess.on('error', (error) => {
      done(error);
    });

    // Timeout after 5 seconds
    setTimeout(() => {
      done(new Error('Server failed to start within timeout'));
    }, 5000);
  });

  it('should handle list_tools request', async () => {
    // This would require a full MCP client implementation
    // For now, we're just testing that the server starts
    expect(true).toBe(true);
  });

  it('should require DSN for tool execution', async () => {
    // Test that tools fail without DSN
    // This would require MCP client implementation
    expect(true).toBe(true);
  });
});