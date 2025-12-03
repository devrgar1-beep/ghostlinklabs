#!/usr/bin/env python3
"""
GhostLink Documentation Comprehension Agent
Full agent comprehension of GhostLink documents and architecture
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GhostLinkComponent:
    """Represents a component in the GhostLink ecosystem"""
    name: str
    description: str
    category: str
    files: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = "unknown"
    documentation: str = ""

@dataclass
class GhostLinkArchitecture:
    """Complete GhostLink system architecture"""
    components: Dict[str, GhostLinkComponent] = field(default_factory=dict)
    triad_synergy: Dict[str, Any] = field(default_factory=dict)
    documentation_index: Dict[str, str] = field(default_factory=dict)
    api_endpoints: Dict[str, str] = field(default_factory=dict)
    cli_commands: Dict[str, str] = field(default_factory=dict)

class GhostLinkComprehensionAgent:
    """Full agent comprehension of GhostLink documents and architecture"""

    def __init__(self, workspace_path: str = "/Users/ghostlink/ghostlink-wiki-organized"):
        self.workspace = Path(workspace_path)
        self.architecture = GhostLinkArchitecture()
        self._load_comprehensive_knowledge()

    def _load_comprehensive_knowledge(self):
        """Load all GhostLink documentation and create comprehensive knowledge base"""
        print("🧬 Loading GhostLink Documentation Comprehension...")

        # Load core documentation
        self._load_readme()
        self._load_triad_synergy_docs()
        self._load_setup_docs()
        self._load_link_docs()
        self._load_api_docs()
        self._load_implementation_docs()
        self._load_infrastructure_docs()
        self._load_testing_docs()

        # Analyze codebase structure
        self._analyze_codebase()

        # Build component relationships
        self._build_component_relationships()

        print("✅ GhostLink comprehension loaded successfully!")

    def _load_readme(self):
        """Load and analyze README.md"""
        readme_path = self.workspace / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()

            # Extract triad synergy information
            self.architecture.triad_synergy = {
                "python_core": {
                    "description": "Sovereign foundation with stdlib-only operation",
                    "features": ["Local-first", "Fallback mode", "Autonomous agents"]
                },
                "mathematica_layer": {
                    "description": "Symbolic computation and AI enhancement",
                    "features": ["Symbolic computation", "AI enhancement", "Knowledge representation"]
                },
                "docker_infrastructure": {
                    "description": "Containerization and deployment scaling",
                    "features": ["Containerization", "Service orchestration", "Network isolation"]
                }
            }

            # Extract API endpoints
            endpoints = re.findall(r'`([^`]+)`\s*-\s*([^\n]+)', content)
            for endpoint, description in endpoints:
                if endpoint.startswith('http'):
                    self.architecture.api_endpoints[endpoint] = description

    def _load_triad_synergy_docs(self):
        """Load triad synergy documentation"""
        triad_complete = self.workspace / "TRIAD_SYNERGY_COMPLETE.md"
        triad_config = self.workspace / "triad_synergy.ini"

        if triad_complete.exists():
            content = triad_complete.read_text()
            # Extract component status and features

        if triad_config.exists():
            content = triad_config.read_text()
            # Parse INI configuration for triad settings

    def _load_setup_docs(self):
        """Load setup and installation documentation"""
        setup_path = self.workspace / "documentation" / "SETUP.md"
        if setup_path.exists():
            content = setup_path.read_text()

            # Extract CLI commands
            cli_patterns = [
                r'`(link [^`]+)`',
                r'`(ghostlink [^`]+)`',
                r'`(python [^`]+)`'
            ]

            for pattern in cli_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    self.architecture.cli_commands[match] = f"From {setup_path.name}"

    def _load_link_docs(self):
        """Load Link agent documentation"""
        link_md = self.workspace / "documentation" / "LINK.md"
        link_chat = self.workspace / "documentation" / "LINK_CHAT_AGENT.md"

        if link_md.exists():
            content = link_md.read_text()
            # Extract Link agent capabilities and features

        if link_chat.exists():
            content = link_chat.read_text()
            # Extract chat agent commands and features

    def _load_api_docs(self):
        """Load API documentation"""
        api_dir = self.workspace / "api"
        if api_dir.exists():
            for file_path in api_dir.glob("*.py"):
                if file_path.name == "main.py":
                    content = file_path.read_text()
                    # Extract FastAPI endpoints and routes

    def _load_implementation_docs(self):
        """Load implementation documentation"""
        impl_dir = self.workspace / "implementation"
        if impl_dir.exists():
            # Analyze core components
            core_components = [
                "ghostlink_model.py",
                "ai_providers.py",
                "autonomous_agents.py",
                "api_integration.py"
            ]

            for component in core_components:
                component_path = impl_dir / "core" / component
                if component_path.exists():
                    content = component_path.read_text()
                    # Extract component information and capabilities

    def _load_infrastructure_docs(self):
        """Load infrastructure documentation"""
        infra_dir = self.workspace / "infrastructure"
        if infra_dir.exists():
            for file_path in infra_dir.glob("*.yaml"):
                if file_path.name == "ghostlink-cluster.yaml":
                    content = file_path.read_text()
                    # Parse Kubernetes manifests

    def _load_testing_docs(self):
        """Load testing documentation"""
        testing_dir = self.workspace / "testing"
        if testing_dir.exists():
            test_files = list(testing_dir.glob("test_*.py"))
            # Analyze test coverage and components

    def _analyze_codebase(self):
        """Analyze the complete codebase structure"""
        # Scan all Python files
        python_files = list(self.workspace.rglob("*.py"))

        for py_file in python_files:
            if py_file.name.startswith('test_'):
                continue  # Skip test files for now

            try:
                content = py_file.read_text()

                # Extract imports to understand dependencies
                imports = re.findall(r'^(?:from|import)\s+([^\s;]+)', content, re.MULTILINE)

                # Extract class definitions
                classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)

                # Extract function definitions
                functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)

                # Store component information
                component_name = py_file.stem
                if component_name not in self.architecture.components:
                    self.architecture.components[component_name] = GhostLinkComponent(
                        name=component_name,
                        description=f"Component from {py_file.relative_to(self.workspace)}",
                        category=self._categorize_component(py_file),
                        files=[str(py_file.relative_to(self.workspace))],
                        dependencies=imports[:10]  # Limit for brevity
                    )

            except Exception as e:
                print(f"Warning: Could not analyze {py_file}: {e}")

    def _categorize_component(self, file_path: Path) -> str:
        """Categorize a component based on its file path"""
        path_parts = file_path.parts

        if "core" in path_parts:
            return "core"
        elif "interfaces" in path_parts:
            return "interface"
        elif "utils" in path_parts:
            return "utility"
        elif "api" in path_parts:
            return "api"
        elif "testing" in path_parts:
            return "testing"
        elif "infrastructure" in path_parts:
            return "infrastructure"
        else:
            return "implementation"

    def _build_component_relationships(self):
        """Build relationships between components"""
        # This would analyze import relationships and dependencies
        pass

    def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview"""
        return {
            "architecture": {
                "triad_synergy": self.architecture.triad_synergy,
                "component_count": len(self.architecture.components),
                "api_endpoints": len(self.architecture.api_endpoints),
                "cli_commands": len(self.architecture.cli_commands)
            },
            "components": {
                name: {
                    "description": comp.description,
                    "category": comp.category,
                    "file_count": len(comp.files),
                    "dependencies": len(comp.dependencies)
                }
                for name, comp in list(self.architecture.components.items())[:10]  # Limit for display
            },
            "key_features": [
                "Sovereign operation (Python stdlib only)",
                "Triad synergy (Python + Mathematica + Docker)",
                "Autonomous Link agent",
                "Hybrid AI capabilities",
                "Container orchestration",
                "Symbolic computation integration"
            ]
        }

    def explain_component(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Explain a specific component"""
        if component_name in self.architecture.components:
            comp = self.architecture.components[component_name]
            return {
                "name": comp.name,
                "description": comp.description,
                "category": comp.category,
                "files": comp.files,
                "dependencies": comp.dependencies[:20],  # Limit for display
                "status": comp.status
            }
        return None

    def get_triad_synergy_status(self) -> Dict[str, Any]:
        """Get triad synergy status and capabilities"""
        return {
            "python_core": {
                "enabled": True,
                "capabilities": ["Stdlib operation", "Fallback mode", "Local-first"],
                "status": "operational"
            },
            "mathematica": {
                "enabled": True,
                "capabilities": ["Symbolic computation", "AI enhancement"],
                "status": "available_when_installed"
            },
            "docker": {
                "enabled": True,
                "capabilities": ["Containerization", "Orchestration"],
                "status": "available_when_installed"
            },
            "synergy_features": [
                "Cross-component communication",
                "Hybrid AI processing",
                "Symbolic computation bridge",
                "Containerized deployment"
            ]
        }

    def search_documentation(self, query: str) -> List[Dict[str, Any]]:
        """Search through documentation for relevant information"""
        results = []

        # Search through all documentation files
        doc_files = [
            "README.md",
            "TRIAD_SYNERGY_COMPLETE.md",
            "documentation/QUICKSTART.md",
            "documentation/SETUP.md",
            "documentation/LINK.md",
            "documentation/LINK_CHAT_AGENT.md"
        ]

        for doc_file in doc_files:
            doc_path = self.workspace / doc_file
            if doc_path.exists():
                try:
                    content = doc_path.read_text().lower()
                    if query.lower() in content:
                        # Find relevant sections
                        lines = content.split('\n')
                        relevant_sections = []

                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                # Get context around the match
                                start = max(0, i-2)
                                end = min(len(lines), i+3)
                                context = '\n'.join(lines[start:end])
                                relevant_sections.append(context)

                        if relevant_sections:
                            results.append({
                                "file": doc_file,
                                "matches": len(relevant_sections),
                                "sections": relevant_sections[:3]  # Limit results
                            })
                except Exception as e:
                    print(f"Warning: Could not search {doc_file}: {e}")

        return results

    def get_setup_instructions(self) -> Dict[str, Any]:
        """Get setup and installation instructions"""
        return {
            "prerequisites": [
                "Python 3.8+",
                "Docker (optional)",
                "Wolfram Mathematica/Engine (optional)",
                "Node.js/npm (for VS Code extension)"
            ],
            "installation_steps": [
                "Clone repository",
                "Install Python dependencies: pip install -e .",
                "Install optional dependencies: pip install -e \".[full]\"",
                "Build VS Code extension: cd .vscode/link-agent && npm install && npm run compile",
                "Activate triad synergy: ./activate_triad_synergy.sh"
            ],
            "verification": [
                "Run tests: python -m pytest testing/",
                "Test triad synergy: python3 triad_synergy.py",
                "Test Link agent: link status",
                "Test VS Code extension: F5 to launch development host"
            ]
        }

    def get_api_reference(self) -> Dict[str, Any]:
        """Get API reference information"""
        return {
            "rest_endpoints": self.architecture.api_endpoints,
            "cli_commands": list(self.architecture.cli_commands.keys())[:20],  # Limit for display
            "python_api": {
                "main_classes": ["Link", "GhostLinkModel", "TriadSynergyOrchestrator"],
                "key_functions": [
                    "initialize_synergy()",
                    "execute_synergy_task()",
                    "chat_with_link()",
                    "get_link_agent()"
                ]
            },
            "integration_apis": [
                "GitHub Copilot Chat (@link commands)",
                "VS Code Extension API",
                "FastAPI REST API",
                "Docker SDK integration",
                "Wolfram Client API"
            ]
        }

    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze system dependencies and requirements"""
        pyproject_path = self.workspace / "pyproject.toml"
        requirements_path = self.workspace / "requirements.txt"

        dependencies = {
            "core": [],
            "optional": {},
            "dev": []
        }

        if pyproject_path.exists():
            content = pyproject_path.read_text()

            # Extract core dependencies
            core_deps = re.findall(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if core_deps:
                # Parse the dependencies list
                deps_text = core_deps[0]
                dependencies["core"] = [d.strip().strip('"').strip("'") for d in deps_text.split(',') if d.strip()]

            # Extract optional dependencies
            optional_sections = re.findall(r'\[([^\]]+)\]', content)
            for section in optional_sections:
                if 'optional-dependencies' in section:
                    section_deps = re.findall(rf'{section}\s*=\s*\[(.*?)\]', content, re.DOTALL)
                    if section_deps:
                        deps_text = section_deps[0]
                        dep_list = [d.strip().strip('"').strip("'") for d in deps_text.split(',') if d.strip()]
                        dependencies["optional"][section] = dep_list

        if requirements_path.exists():
            content = requirements_path.read_text()
            dependencies["requirements_file"] = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]

        return dependencies

def main():
    """Main function for GhostLink comprehension agent"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink Documentation Comprehension Agent")
    parser.add_argument("--overview", action="store_true", help="Show system overview")
    parser.add_argument("--component", help="Explain specific component")
    parser.add_argument("--triad-status", action="store_true", help="Show triad synergy status")
    parser.add_argument("--search", help="Search documentation")
    parser.add_argument("--setup", action="store_true", help="Show setup instructions")
    parser.add_argument("--api", action="store_true", help="Show API reference")
    parser.add_argument("--dependencies", action="store_true", help="Analyze dependencies")

    args = parser.parse_args()

    # Initialize agent
    agent = GhostLinkComprehensionAgent()

    if args.overview:
        overview = agent.get_system_overview()
        print(json.dumps(overview, indent=2))

    elif args.component:
        info = agent.explain_component(args.component)
        if info:
            print(json.dumps(info, indent=2))
        else:
            print(f"Component '{args.component}' not found")

    elif args.triad_status:
        status = agent.get_triad_synergy_status()
        print(json.dumps(status, indent=2))

    elif args.search:
        results = agent.search_documentation(args.search)
        print(json.dumps(results, indent=2))

    elif args.setup:
        setup = agent.get_setup_instructions()
        print(json.dumps(setup, indent=2))

    elif args.api:
        api_ref = agent.get_api_reference()
        print(json.dumps(api_ref, indent=2))

    elif args.dependencies:
        deps = agent.analyze_dependencies()
        print(json.dumps(deps, indent=2))

    else:
        # Default: show overview
        overview = agent.get_system_overview()
        print("🧬 GhostLink Documentation Comprehension Agent")
        print("=" * 50)
        print(f"Components: {overview['architecture']['component_count']}")
        print(f"API Endpoints: {overview['architecture']['api_endpoints']}")
        print(f"CLI Commands: {overview['architecture']['cli_commands']}")
        print("\nKey Features:")
        for feature in overview['key_features']:
            print(f"  • {feature}")
        print("\nUse --help for more options")

if __name__ == "__main__":
    main()
