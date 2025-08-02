#!/usr/bin/env node
import { config } from "dotenv";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createClient } from "@libsql/client";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Load environment variables
config();

// Turso client
let tursoClient: any = null;

function getTursoClient() {
  if (!tursoClient) {
    const databaseUrl = process.env.TURSO_DATABASE_URL || "libsql://context-memory-diegofornalha.aws-us-east-1.turso.io";
    
    tursoClient = createClient({
      url: databaseUrl,
      authToken: process.env.TURSO_AUTH_TOKEN,
    });
  }
  return tursoClient;
}

// Create server instance
const server = new Server(
  {
    name: "mcp-turso-memory",
    version: "1.0.0",
  }
);

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "turso_list_databases",
        description: "List all databases in your Turso organization",
        inputSchema: {
          type: "object",
          properties: {
            random_string: {
              type: "string",
              description: "Dummy parameter for no-parameter tools",
            },
          },
          required: ["random_string"],
        },
      },
      {
        name: "turso_create_database",
        description: "Create a new database in your Turso organization",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Name of the database to create",
            },
            group: {
              type: "string",
              description: "Optional group name for the database",
            },
            regions: {
              type: "array",
              items: { type: "string" },
              description: "Optional list of regions to deploy the database to",
            },
          },
          required: ["name"],
        },
      },
      {
        name: "turso_execute_query",
        description: "Execute a SQL query on the Turso database",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "SQL query to execute",
            },
            params: {
              type: "object",
              description: "Query parameters (optional)",
            },
            database: {
              type: "string",
              description: "Database name (optional)",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "turso_list_tables",
        description: "List all tables in the database",
        inputSchema: {
          type: "object",
          properties: {
            database: {
              type: "string",
              description: "Database name (optional)",
            },
          },
        },
      },
      {
        name: "turso_describe_table",
        description: "Describe the structure of a table",
        inputSchema: {
          type: "object",
          properties: {
            table: {
              type: "string",
              description: "Table name to describe",
            },
            database: {
              type: "string",
              description: "Database name (optional)",
            },
          },
          required: ["table"],
        },
      },
      {
        name: "turso_add_conversation",
        description: "Add a conversation to memory",
        inputSchema: {
          type: "object",
          properties: {
            session_id: {
              type: "string",
              description: "Session identifier",
            },
            user_id: {
              type: "string",
              description: "User identifier",
            },
            message: {
              type: "string",
              description: "User message",
            },
            response: {
              type: "string",
              description: "AI response",
            },
            context: {
              type: "string",
              description: "Additional context",
            },
          },
          required: ["session_id", "message"],
        },
      },
      {
        name: "turso_get_conversations",
        description: "Get conversations from memory",
        inputSchema: {
          type: "object",
          properties: {
            session_id: {
              type: "string",
              description: "Session identifier (optional)",
            },
            limit: {
              type: "number",
              description: "Number of conversations to retrieve",
            },
          },
        },
      },
      {
        name: "turso_add_knowledge",
        description: "Add knowledge to the knowledge base",
        inputSchema: {
          type: "object",
          properties: {
            topic: {
              type: "string",
              description: "Knowledge topic",
            },
            content: {
              type: "string",
              description: "Knowledge content",
            },
            source: {
              type: "string",
              description: "Source of knowledge",
            },
            tags: {
              type: "string",
              description: "Comma-separated tags",
            },
          },
          required: ["topic", "content"],
        },
      },
      {
        name: "turso_search_knowledge",
        description: "Search knowledge base",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query",
            },
            tags: {
              type: "string",
              description: "Filter by tags",
            },
            limit: {
              type: "number",
              description: "Number of results",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    const client = getTursoClient();

    switch (name) {
      case "turso_list_databases":
        // Simulate listing databases
        return {
          content: [
            {
              type: "text",
              text: `Available databases: context-memory`,
            },
          ],
        };

      case "turso_create_database":
        return {
          content: [
            {
              type: "text",
              text: `Database creation would be handled by Turso CLI`,
            },
          ],
        };

      case "turso_execute_query":
        if (!args?.query) {
          throw new Error("Query parameter is required");
        }
        const result = await client.execute(args.query, args?.params || {});
        return {
          content: [
            {
              type: "text",
              text: `Query executed successfully:\n${JSON.stringify(result, null, 2)}`,
            },
          ],
        };

      case "turso_list_tables":
        const tablesResult = await client.execute(`
          SELECT name FROM sqlite_master 
          WHERE type='table' AND name NOT LIKE 'sqlite_%'
          ORDER BY name
        `);
        return {
          content: [
            {
              type: "text",
              text: `Tables in database:\n${JSON.stringify(tablesResult, null, 2)}`,
            },
          ],
        };

      case "turso_describe_table":
        if (!args?.table) {
          throw new Error("Table parameter is required");
        }
        const describeResult = await client.execute(`PRAGMA table_info(${args.table})`);
        return {
          content: [
            {
              type: "text",
              text: `Table structure for ${args.table}:\n${JSON.stringify(describeResult, null, 2)}`,
            },
          ],
        };

      case "turso_add_conversation":
        if (!args?.session_id || !args?.message) {
          throw new Error("session_id and message are required");
        }
        const insertResult = await client.execute(`
          INSERT INTO conversations (session_id, user_id, message, response, context)
          VALUES (?, ?, ?, ?, ?)
        `, [args.session_id, args.user_id || null, args.message, args.response || null, args.context || null]);
        return {
          content: [
            {
              type: "text",
              text: `Conversation added successfully. ID: ${insertResult.lastInsertRowid}`,
            },
          ],
        };

      case "turso_get_conversations":
        let query = "SELECT * FROM conversations";
        const params: any[] = [];
        
        if (args?.session_id) {
          query += " WHERE session_id = ?";
          params.push(args.session_id);
        }
        
        query += " ORDER BY timestamp DESC";
        
        if (args?.limit) {
          query += " LIMIT ?";
          params.push(args.limit);
        }
        
        const conversationsResult = await client.execute(query, params);
        return {
          content: [
            {
              type: "text",
              text: `Conversations:\n${JSON.stringify(conversationsResult, null, 2)}`,
            },
          ],
        };

      case "turso_add_knowledge":
        if (!args?.topic || !args?.content) {
          throw new Error("topic and content are required");
        }
        const knowledgeResult = await client.execute(`
          INSERT INTO knowledge_base (topic, content, source, tags)
          VALUES (?, ?, ?, ?)
        `, [args.topic, args.content, args.source || null, args.tags || null]);
        return {
          content: [
            {
              type: "text",
              text: `Knowledge added successfully. ID: ${knowledgeResult.lastInsertRowid}`,
            },
          ],
        };

      case "turso_search_knowledge":
        if (!args?.query) {
          throw new Error("query is required");
        }
        let searchQuery = "SELECT * FROM knowledge_base WHERE topic LIKE ? OR content LIKE ?";
        const searchParams = [`%${args.query}%`, `%${args.query}%`];
        
        if (args?.tags) {
          searchQuery += " AND tags LIKE ?";
          searchParams.push(`%${args.tags}%`);
        }
        
        searchQuery += " ORDER BY priority DESC, created_at DESC";
        
        if (args?.limit) {
          searchQuery += " LIMIT ?";
          searchParams.push(args.limit.toString());
        }
        
        const searchResult = await client.execute(searchQuery, searchParams);
        return {
          content: [
            {
              type: "text",
              text: `Search results:\n${JSON.stringify(searchResult, null, 2)}`,
            },
          ],
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error); 