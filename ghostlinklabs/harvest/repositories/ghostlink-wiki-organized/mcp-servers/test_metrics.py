#!/usr/bin/env python3
from mcp_server.main import MCPServer


s = MCPServer()
res = s.handle_request({
	"method": "tools/call",
	"params": {"name": "get_metrics"},
})
print(res)
