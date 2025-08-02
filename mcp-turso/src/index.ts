#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createClient } from "@libsql/client";

// Turso client
let tursoClient: any = null;

function getTursoClient() {
  if (!tursoClient) {
    const url = process.env.TURSO_DATABASE_URL || "http://127.0.0.1:8080";
    tursoClient = createClient({ url });
  }
  return tursoClient;
}

// Create MCP server
const server = new Server(
  {
    name: "mcp-turso",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool handlers
server.setRequestHandler(
  { method: "tools/list" },
  async () => {
    return {
      tools: [
      {
        name: "turso_execute_query",
        description: "Execute a SQL query on the Turso database",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "SQL query to execute" },
            params: { type: "array", description: "Query parameters", items: { type: "string" } },
          },
          required: ["query"],
        },
      },
      {
        name: "turso_list_tables",
        description: "List all tables in the database",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "turso_create_table",
        description: "Create a new table in the database",
        inputSchema: {
          type: "object",
          properties: {
            tableName: { type: "string", description: "Name of the table to create" },
            schema: { type: "string", description: "SQL schema definition" },
          },
          required: ["tableName", "schema"],
        },
      },
    ],
  };
});

server.setRequestHandler(
  { method: "tools/call" },
  async (request: any) => {
    const { name, arguments: args } = request.params;

  try {
    const client = getTursoClient();

    switch (name) {
      case "turso_execute_query": {
        const { query, params = [] } = args;
        const result = await client.execute(query, params);
        return {
          content: [{
            type: "text",
            text: JSON.stringify(result, null, 2),
          }],
        };
      }

      case "turso_list_tables": {
        const result = await client.execute(`
          SELECT name FROM sqlite_master 
          WHERE type='table' AND name NOT LIKE 'sqlite_%'
          ORDER BY name
        `);
        return {
          content: [{
            type: "text",
            text: JSON.stringify(result, null, 2),
          }],
        };
      }

      case "turso_create_table": {
        const { tableName, schema } = args;
        await client.execute(`CREATE TABLE ${tableName} (${schema})`);
        return {
          content: [{
            type: "text",
            text: `Table ${tableName} created successfully`,
          }],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [{
        type: "text",
        text: `Error: ${error.message}`,
      }],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);