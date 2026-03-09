#!/bin/bash
echo "启动 MCP Inspector..."
echo "在浏览器中打开 http://localhost:5173"
echo ""
npx @modelcontextprotocol/inspector /opt/homebrew/bin/python3.11 -m ketcher_mcp.server
