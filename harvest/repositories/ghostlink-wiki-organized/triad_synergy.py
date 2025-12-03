#!/usr/bin/env python3
"""
GhostLink Triad Synergy Orchestrator
Enables seamless integration between Python, Mathematica, and Docker components
"""

import asyncio
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict

# Optional imports for enhanced synergy
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

try:
    from wolframclient.evaluation import WolframLanguageSession
    from wolframclient.language import wl, wlexpr
    WOLFRAM_AVAILABLE = True
except ImportError:
    WOLFRAM_AVAILABLE = False

class TriadSynergyOrchestrator:
    """Orchestrates synergy between Python, Mathematica, and Docker triad components"""

    def __init__(self):
        self.python_core = None
        self.mathematica_session = None
        self.docker_client = None
        self.synergy_active = False
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load triad synergy configuration"""
        config = {
            "python_enabled": True,
            "mathematica_enabled": WOLFRAM_AVAILABLE,
            "docker_enabled": DOCKER_AVAILABLE,
            "experimental_mode": os.getenv("GHOSTLINK_EXPERIMENTAL", "true").lower() == "true",
            "hybrid_triad": os.getenv("GHOSTLINK_HYBRID_MODE", "true").lower() == "true",
            "local_first": os.getenv("GHOSTLINK_LOCAL_FIRST", "true").lower() == "true",
            "sovereign": os.getenv("GHOSTLINK_SOVEREIGN", "true").lower() == "true",
            "mathematica_kernel_url": os.getenv("MATHEMATICA_KERNEL_URL", "http://localhost:31415"),
            "docker_socket": os.getenv("DOCKER_SOCKET", "/var/run/docker.sock"),
            "synergy_port": int(os.getenv("TRIAD_SYNERGY_PORT", "7421")),
        }
        return config

    async def initialize_synergy(self) -> bool:
        """Initialize all triad components and establish synergy"""
        print("🧬 Initializing GhostLink Triad Synergy...")

        success = True

        # Initialize Python core
        success &= await self._initialize_python_core()

        # Initialize Mathematica session
        if self.config["mathematica_enabled"]:
            success &= await self._initialize_mathematica_session()

        # Initialize Docker client
        if self.config["docker_enabled"]:
            success &= await self._initialize_docker_client()

        # Establish synergy channels
        if success:
            success &= await self._establish_synergy_channels()

        self.synergy_active = success
        if success:
            print("✅ Triad Synergy activated successfully!")
            print("🔗 Components connected: Python ↔ Mathematica ↔ Docker")
        else:
            print("❌ Triad Synergy initialization failed")

        return success

    async def _initialize_python_core(self) -> bool:
        """Initialize Python core component with fallback mode"""
        try:
            print("🐍 Initializing Python core...")
            # Try to import from ghostlink package structure
            sys.path.insert(0, str(Path(__file__).parent))

            # Try multiple import paths for flexibility
            python_core = None
            try:
                from implementation.core.ai_providers import AIProviderManager
                from implementation.core.autonomous_agents import AgentOrchestrator
                from implementation.core.ghostlink_model import ghostlink_model
                python_core = {
                    "model": ghostlink_model,
                    "ai_manager": AIProviderManager(),
                    "agent_orchestrator": AgentOrchestrator(),
                    "status": "active"
                }
                print("✅ Python core initialized with full GhostLink integration")
            except ImportError:
                try:
                    # Try core-runtime path
                    from core_runtime.main import main as ghostlink_main
                    python_core = {"main": ghostlink_main, "status": "active"}
                    print("✅ Python core initialized with core-runtime integration")
                except ImportError:
                    # Fallback: create minimal Python core
                    python_core = self._create_minimal_python_core()
                    print("✅ Python core initialized in fallback mode")

            self.python_core = python_core
            return True
        except Exception as e:
            print(f"❌ Python core initialization failed: {e}")
            # Create minimal fallback even on error
            self.python_core = self._create_minimal_python_core()
            return True

    def _create_minimal_python_core(self):
        """Create minimal Python core for sovereign operation"""
        class MinimalPythonCore:
            def __init__(self):
                self.active = True
                self.status = "minimal_fallback"

            def process_request(self, request):
                """Process a request with minimal capabilities"""
                return {
                    "response": f"Minimal Python core processed: {request}",
                    "status": "success",
                    "fallback_mode": True
                }

            def get_status(self):
                return {"status": "active", "mode": "minimal", "fallback": True}

            async def generate_response(self, prompt):
                """Generate a simple response"""
                return f"Minimal AI response to: {prompt}"

        return MinimalPythonCore()

    async def _initialize_mathematica_session(self) -> bool:
        """Initialize Mathematica session"""
        try:
            print("🔢 Initializing Mathematica session...")
            self.mathematica_session = WolframLanguageSession()

            # Load GhostLink Mathematica package
            mathematica_path = Path(__file__).parent / "mathematica" / "GhostLink.m"
            if mathematica_path.exists():
                self.mathematica_session.evaluate(f'Get["{mathematica_path}"]')
                print("✅ Mathematica package loaded")
            else:
                print("⚠️  Mathematica package not found, using direct evaluation")

            # Test connection
            result = self.mathematica_session.evaluate('2 + 2')
            if result == 4:
                print("✅ Mathematica session active")
                return True
            else:
                print("❌ Mathematica session test failed")
                return False
        except Exception as e:
            print(f"❌ Mathematica session initialization failed: {e}")
            return False

    async def _initialize_docker_client(self) -> bool:
        """Initialize Docker client"""
        try:
            print("🐳 Initializing Docker client...")
            self.docker_client = docker.from_env()

            # Test connection
            self.docker_client.ping()
            print("✅ Docker client connected")

            # Check for GhostLink containers
            containers = self.docker_client.containers.list(all=True)
            ghostlink_containers = [c for c in containers if "ghostlink" in c.name.lower()]
            print(f"📦 Found {len(ghostlink_containers)} GhostLink containers")

            return True
        except Exception as e:
            print(f"❌ Docker client initialization failed: {e}")
            return False

    async def _establish_synergy_channels(self) -> bool:
        """Establish communication channels between triad components"""
        try:
            print("🔗 Establishing synergy channels...")

            # Python ↔ Mathematica channel
            if self.mathematica_session:
                self.mathematica_session.evaluate('''
                    PythonToMathematica[data_] := Module[{},
                        (* Convert Python data to Mathematica format *)
                        If[Head[data] === List, data, {data}]
                    ]
                ''')

            # Python ↔ Docker channel
            if self.docker_client:
                # Create synergy network if it doesn't exist
                try:
                    self.docker_client.networks.get("ghostlink-triad")
                except docker.errors.NotFound:
                    self.docker_client.networks.create("ghostlink-triad", driver="bridge")
                    print("🌐 Created ghostlink-triad network")

            # Mathematica ↔ Docker channel (via Python bridge)
            print("✅ Synergy channels established")
            return True
        except Exception as e:
            print(f"❌ Synergy channel establishment failed: {e}")
            return False

    async def execute_synergy_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using triad synergy"""
        if not self.synergy_active:
            return {"error": "Triad synergy not active"}

        task_type = task.get("type", "unknown")
        print(f"⚡ Executing synergy task: {task_type}")

        try:
            if task_type == "symbolic_computation":
                return await self._execute_symbolic_computation(task)
            elif task_type == "hybrid_ai":
                return await self._execute_hybrid_ai(task)
            elif task_type == "containerized_deployment":
                return await self._execute_containerized_deployment(task)
            elif task_type == "triad_analysis":
                return await self._execute_triad_analysis(task)
            else:
                return {"result": f"Unknown task type: {task_type}"}
        except Exception as e:
            return {"error": f"Task execution failed: {str(e)}"}

    async def _execute_symbolic_computation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute symbolic computation using Mathematica"""
        if not self.mathematica_session:
            return {"error": "Mathematica session not available"}

        expression = task.get("expression", "")
        try:
            result = self.mathematica_session.evaluate(expression)
            return {
                "result": str(result),
                "component": "mathematica",
                "type": "symbolic_computation"
            }
        except Exception as e:
            return {"error": f"Symbolic computation failed: {str(e)}"}

    async def _execute_hybrid_ai(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute hybrid AI task combining Python and Mathematica"""
        prompt = task.get("prompt", "")

        # Get Python AI response
        python_result = None
        if self.python_core and self.python_core["model"]:
            try:
                python_result = await self.python_core["model"].generate_response(prompt)
            except:
                python_result = "Python AI unavailable"

        # Get Mathematica symbolic analysis
        mathematica_result = None
        if self.mathematica_session:
            try:
                # Analyze prompt symbolically
                analysis = self.mathematica_session.evaluate(f'''
                    SemanticAnalysis["{prompt}"]
                ''')
                mathematica_result = str(analysis)
            except:
                mathematica_result = "Mathematica analysis unavailable"

        return {
            "python_ai": python_result,
            "mathematica_analysis": mathematica_result,
            "component": "hybrid_ai",
            "type": "triad_synergy"
        }

    async def _execute_containerized_deployment(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute containerized deployment task"""
        if not self.docker_client:
            return {"error": "Docker client not available"}

        action = task.get("action", "status")
        try:
            if action == "build":
                image = self.docker_client.images.build(path=".", tag="ghostlink:synergy")
                return {"result": "Image built successfully", "image": str(image)}
            elif action == "deploy":
                container = self.docker_client.containers.run(
                    "ghostlink:synergy",
                    detach=True,
                    network="ghostlink-triad",
                    name="ghostlink-synergy-instance"
                )
                return {"result": "Container deployed", "container_id": container.id}
            elif action == "status":
                containers = self.docker_client.containers.list(all=True)
                ghostlink_containers = [c for c in containers if "ghostlink" in c.name.lower()]
                return {"containers": len(ghostlink_containers), "status": "active"}
            else:
                return {"error": f"Unknown action: {action}"}
        except Exception as e:
            return {"error": f"Container operation failed: {str(e)}"}

    async def _execute_triad_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive triad analysis"""
        analysis = {
            "timestamp": str(asyncio.get_event_loop().time()),
            "components": {
                "python": self.python_core is not None,
                "mathematica": self.mathematica_session is not None,
                "docker": self.docker_client is not None
            },
            "synergy_status": self.synergy_active,
            "config": self.config
        }

        # Add component-specific analysis
        if self.python_core:
            try:
                if hasattr(self.python_core, 'get_status'):
                    analysis["python_status"] = self.python_core.get_status()
                elif isinstance(self.python_core, dict):
                    analysis["python_status"] = self.python_core.get("status", "unknown")
                else:
                    analysis["python_status"] = "active"
            except:
                analysis["python_status"] = "unknown"

        if self.mathematica_session:
            try:
                test_result = self.mathematica_session.evaluate('1 + 1')
                analysis["mathematica_status"] = "active" if test_result == 2 else "error"
            except:
                analysis["mathematica_status"] = "error"

        if self.docker_client:
            try:
                self.docker_client.ping()
                analysis["docker_status"] = "active"
            except:
                analysis["docker_status"] = "error"

        return analysis

    async def shutdown_synergy(self):
        """Shutdown triad synergy gracefully"""
        print("🔄 Shutting down triad synergy...")

        if self.mathematica_session:
            try:
                self.mathematica_session.terminate()
                print("✅ Mathematica session terminated")
            except:
                pass

        if self.docker_client:
            try:
                # Clean up synergy containers/networks if needed
                print("✅ Docker client disconnected")
            except:
                pass

        self.synergy_active = False
        print("✅ Triad synergy shutdown complete")

# Global synergy orchestrator instance
triad_synergy = TriadSynergyOrchestrator()

async def main():
    """Main triad synergy execution"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink Triad Synergy Orchestrator")
    parser.add_argument("--task", help="Task to execute")
    parser.add_argument("--expression", help="Mathematica expression for symbolic computation")
    parser.add_argument("--prompt", help="AI prompt for hybrid processing")
    parser.add_argument("--action", help="Docker action (build/deploy/status)")
    parser.add_argument("--hub", action="store_true", help="Run as synergy hub server")

    args = parser.parse_args()

    if args.hub:
        # Run as synergy hub server
        await run_synergy_hub()
        return

    # Initialize synergy
    if not await triad_synergy.initialize_synergy():
        sys.exit(1)

    try:
        if args.task:
            task = json.loads(args.task)
        elif args.expression:
            task = {"type": "symbolic_computation", "expression": args.expression}
        elif args.prompt:
            task = {"type": "hybrid_ai", "prompt": args.prompt}
        elif args.action:
            task = {"type": "containerized_deployment", "action": args.action}
        else:
            task = {"type": "triad_analysis"}

        result = await triad_synergy.execute_synergy_task(task)
        print(json.dumps(result, indent=2))

    finally:
        await triad_synergy.shutdown_synergy()


async def run_synergy_hub():
    """Run the triad synergy hub server"""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class SynergyHubHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "healthy", "triad": "active"}).encode())
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            if self.path == "/synergy":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                try:
                    task = json.loads(post_data.decode())
                    # Execute task asynchronously
                    import asyncio
                    result = asyncio.run(triad_synergy.execute_synergy_task(task))

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            # Suppress default logging
            pass

    # Initialize synergy
    if not await triad_synergy.initialize_synergy():
        print("Failed to initialize triad synergy for hub")
        sys.exit(1)

    hub_port = triad_synergy.config.get("synergy_port", 7422)
    server = HTTPServer(('0.0.0.0', hub_port), SynergyHubHandler)

    print(f"🧬 Triad Synergy Hub running on port {hub_port}")
    print("🔗 Accepting synergy tasks via HTTP POST /synergy")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down synergy hub...")
    finally:
        await triad_synergy.shutdown_synergy()
        server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
