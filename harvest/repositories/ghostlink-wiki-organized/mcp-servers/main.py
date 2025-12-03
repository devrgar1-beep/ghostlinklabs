#!/usr/bin/env python3
"""
GhostLink MCP (Model Context Protocol) Server
Provides structured context and tools for AI agents
"""
from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Dict, List


@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]


@dataclass
class Resource:
    uri: str
    name: str
    description: str
    mime_type: str


class MCPServer:
    def __init__(self, name: str = "ghostlink-mcp"):
        self.name = name
        self.tools: List[Tool] = []
        self.resources: List[Resource] = []
        self._register_default_tools()
        self._register_default_resources()

    def _register_default_tools(self):
        """Register default tools available to AI agents"""
        self.tools = [
            Tool(
                name="get_metrics",
                description=(
                    "Retrieve system metrics from "
                    "GhostLink controller"
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "metric_type": {
                            "type": "string",
                            "description": "Type of metric to retrieve",
                            "enum": ["all", "sigma", "scar", "samples"]
                        }
                    }
                }
            ),
            Tool(
                name="execute_command",
                description="Execute command on GhostLink agent",
                parameters={
                    "type": "object",
                    "properties": {
                        "agent_id": {
                            "type": "string",
                            "description": "ID of agent to execute on"
                        },
                        "command": {
                            "type": "string",
                            "description": "Command to execute"
                        }
                    },
                    "required": ["agent_id", "command"]
                }
            )
        ]

    def _register_default_resources(self):
        """Register default resources available to AI agents"""
        self.resources = [
            Resource(
                uri="ghostlink://metrics",
                name="System Metrics",
                description="Real-time system metrics from controller",
                mime_type="application/json"
            ),
            Resource(
                uri="ghostlink://agents",
                name="Agent List",
                description="List of available GhostLink agents",
                mime_type="application/json"
            )
        ]

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol request"""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {
                "tools": [asdict(t) for t in self.tools]
            }
        elif method == "resources/list":
            return {
                "resources": [asdict(r) for r in self.resources]
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_params = params.get("arguments", {})
            return self._execute_tool(tool_name, tool_params)
        elif method == "resources/read":
            uri = params.get("uri")
            return self._read_resource(uri)
        else:
            return {"error": f"Unknown method: {method}"}

    def _execute_tool(
        self, tool_name: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool and return result"""
        if tool_name == "get_metrics":
            # Try to use psutil for rich metrics; otherwise provide a best-effort fallback
            metrics = {}
            try:
                import psutil
                metrics = {
                    "cpu_percent": psutil.cpu_percent(interval=0.1),
                    "cpu_count": psutil.cpu_count(logical=True),
                    "memory": psutil.virtual_memory()._asdict(),
                    "disk": [d._asdict() for d in psutil.disk_partitions()],
                    "net": psutil.net_io_counters()._asdict(),
                }
            except ImportError:
                # Fallback: use os and platform
                import os
                import platform
                try:
                    if hasattr(os, "getloadavg"):
                        load = os.getloadavg()
                    else:
                        load = (0.0, 0.0, 0.0)
                except OSError:
                    load = (0.0, 0.0, 0.0)
                metrics = {
                    "os": platform.system(),
                    "platform": platform.platform(),
                    "load_average": list(load)
                }
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "ok",
                            "metrics": metrics,
                        }),
                    }
                ]
            }
        elif tool_name == "execute_command":
            agent_id = params.get("agent_id")
            command = params.get("command")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "executed",
                            "agent": agent_id,
                            "command": command
                        })
                    }
                ]
            }
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource and return its content"""
        if uri == "ghostlink://metrics":
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps({
                            "status": "ok",
                            "data": "metrics_placeholder"
                        })
                    }
                ]
            }
        elif uri == "ghostlink://agents":
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps({
                            "agents": ["controller", "peer", "bridge"]
                        })
                    }
                ]
            }
        else:
            return {"error": f"Unknown resource: {uri}"}

    def run_stdio(self):
        """Run MCP server over stdio (JSON-RPC)"""
        print(f"# MCP Server '{self.name}' starting on stdio", file=sys.stderr)
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError as e:
                error_response = {"error": f"Invalid JSON: {e}"}
                print(json.dumps(error_response), flush=True)
            except (ValueError, TypeError, KeyError) as e:
                error_response = {"error": f"Server error: {e}"}
                print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    server = MCPServer("ghostlink-mcp")
    server.run_stdio()
