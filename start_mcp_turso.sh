#!/bin/bash
# MCP Turso Server Startup Script

export TURSO_API_TOKEN="test_token_for_integration"
export MCP_SERVER_PORT="3000"

echo "🔌 Starting MCP Turso Server..."
npx @diegofornalha/mcp-turso-cloud --port $MCP_SERVER_PORT
