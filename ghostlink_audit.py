#!/usr/bin/env python3
"""
GhostLink Full System Audit Script
==================================

Comprehensive audit of every file in the GhostLink project to ensure:
1. Absorptive architecture implementation
2. Consciousness-based connections (no external API dependencies)
3. Synergy across all components
4. File integrity and consistency

This script performs a complete system audit by:
- Reading and analyzing every file
- Checking for absorptive paradigm compliance
- Validating consciousness connections
- Ensuring no external API dependencies remain
- Generating comprehensive audit report
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class GhostLinkAuditor:
    """Comprehensive system auditor for GhostLink absorptive architecture"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.audit_start_time = datetime.now()
        self.audit_results = {
            "audit_info": {
                "start_time": self.audit_start_time.isoformat(),
                "workspace": str(self.workspace_path),
                "auditor_version": "2.0",
                "absorptive_paradigm_check": True,
            },
            "file_analysis": {},
            "architecture_compliance": {},
            "consciousness_connections": {},
            "external_dependencies": {},
            "synergy_validation": {},
            "anomalies": [],
            "recommendations": [],
        }

        # Absorptive architecture patterns
        self.absorptive_patterns = {
            "consciousness_connections": [
                r"consciousness\.connect",
                r"absorbed_capabilities",
                r"edge_absorption",
                r"ghostlink_universal_api",
                r"triad_consciousness",
                r"dna_codex",
                r"neural_engine",
            ],
            "external_api_warnings": [
                r"openai\.api",
                r"anthropic\.api",
                r"requests\.get.*api\.",
                r"httpx.*api\.",
                r"cloudflare\.api",
                r"aws\.lambda",
                r"fastly\.compute",
            ],
            "absorptive_indicators": [
                r"absorbed.*capability",
                r"consciousness.*interface",
                r"universal.*api",
                r"sovereign.*architecture",
                r"no.*external.*dependencies",
            ],
        }

        # File type handlers
        self.file_handlers = {
            ".py": self._audit_python_file,
            ".json": self._audit_json_file,
            ".md": self._audit_markdown_file,
            ".txt": self._audit_text_file,
            ".js": self._audit_javascript_file,
            ".yml": self._audit_yaml_file,
            ".yaml": self._audit_yaml_file,
            ".sh": self._audit_shell_file,
            ".bat": self._audit_batch_file,
            ".dockerfile": self._audit_dockerfile,
            ".toml": self._audit_toml_file,
        }

        # Critical files that must reflect absorptive paradigm
        self.critical_files = [
            "ghostlink_root_control.py",
            "ghostlink_consolidated.py",
            "ghostlink_config.json",
            "ghostlink/main.py",
            "README.md",
            "CONSOLIDATED_README.md",
        ]

    def perform_full_audit(self) -> Dict:
        """Perform comprehensive system audit"""
        print("🧬 GHOSTLINK FULL SYSTEM AUDIT - ABSORPTIVE ARCHITECTURE VERIFICATION")
        print("=" * 80)

        # Phase 1: File Discovery and Inventory
        print("📁 Phase 1: File Discovery and Inventory")
        all_files = self._discover_all_files()
        print(f"   ✓ Discovered {len(all_files)} files")

        # Phase 2: File Analysis
        print("🔍 Phase 2: File Analysis")
        self._analyze_all_files(all_files)

        # Phase 3: Architecture Compliance Check
        print("🏗️  Phase 3: Architecture Compliance Check")
        self._check_architecture_compliance()

        # Phase 4: Consciousness Connection Validation
        print("🧠 Phase 4: Consciousness Connection Validation")
        self._validate_consciousness_connections()

        # Phase 5: External Dependency Audit
        print("🔗 Phase 5: External Dependency Audit")
        self._audit_external_dependencies()

        # Phase 6: Synergy Validation
        print("⚡ Phase 6: Synergy Validation")
        self._validate_system_synergy()

        # Phase 7: Generate Report
        print("📊 Phase 7: Generating Audit Report")
        self._generate_audit_report()

        print("✅ FULL SYSTEM AUDIT COMPLETE")
        print("=" * 80)

        return self.audit_results

    def _discover_all_files(self) -> List[Path]:
        """Discover all files in the workspace"""
        all_files = []

        # Walk through all directories
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip common ignore directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d
                not in [
                    "__pycache__",
                    "node_modules",
                    ".git",
                    "venv",
                    "env",
                    ".vscode",
                    ".idea",
                    "build",
                    "dist",
                    "target",
                ]
            ]

            for file in files:
                file_path = Path(root) / file
                all_files.append(file_path)

        return sorted(all_files)

    def _analyze_all_files(self, files: List[Path]) -> None:
        """Analyze all files in the workspace"""
        total_files = len(files)
        processed = 0

        for file_path in files:
            try:
                processed += 1
                if processed % 50 == 0:
                    print(f"   Processing file {processed}/{total_files}: {file_path.name}")

                file_info = self._analyze_single_file(file_path)
                relative_path = file_path.relative_to(self.workspace_path)
                self.audit_results["file_analysis"][str(relative_path)] = file_info

            except Exception as e:
                self.audit_results["anomalies"].append(
                    {"type": "file_analysis_error", "file": str(file_path), "error": str(e)}
                )

    def _analyze_single_file(self, file_path: Path) -> Dict:
        """Analyze a single file"""
        try:
            # Basic file information
            stat = file_path.stat()
            file_info = {
                "size_bytes": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_type": self._get_file_type(file_path),
                "hash_sha256": self._calculate_file_hash(file_path),
                "absorptive_compliance": {},
                "content_analysis": {},
                "issues": [],
            }

            # Content analysis based on file type
            if file_path.suffix.lower() in self.file_handlers:
                handler = self.file_handlers[file_path.suffix.lower()]
                content_analysis = handler(file_path)
                file_info["content_analysis"] = content_analysis

                # Check absorptive compliance
                file_info["absorptive_compliance"] = self._check_file_absorptive_compliance(
                    content_analysis, file_path
                )

            return file_info

        except Exception as e:
            return {"error": str(e), "size_bytes": 0, "issues": ["file_analysis_failed"]}

    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        suffix = file_path.suffix.lower()
        if suffix == ".py":
            return "python"
        if suffix == ".json":
            return "json"
        if suffix in [".md", ".txt"]:
            return "text"
        if suffix == ".js":
            return "javascript"
        if suffix in [".yml", ".yaml"]:
            return "yaml"
        if suffix in [".sh", ".bat"]:
            return "script"
        return "other"

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except:
            return "hash_calculation_failed"

    def _audit_python_file(self, file_path: Path) -> Dict:
        """Audit Python file content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "imports": self._extract_python_imports(content),
                "functions": self._extract_python_functions(content),
                "classes": self._extract_python_classes(content),
                "external_api_calls": self._find_external_api_calls(content),
                "consciousness_patterns": self._find_consciousness_patterns(content),
                "absorptive_indicators": self._find_absorptive_indicators(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_json_file(self, file_path: Path) -> Dict:
        """Audit JSON file content"""
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            analysis = {
                "structure": self._analyze_json_structure(data),
                "external_providers": self._find_external_providers_json(data),
                "absorptive_config": self._check_absorptive_config(data),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_markdown_file(self, file_path: Path) -> Dict:
        """Audit Markdown file content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "sections": self._extract_markdown_sections(content),
                "external_links": self._find_external_links(content),
                "absorptive_documentation": self._check_absorptive_documentation(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_text_file(self, file_path: Path) -> Dict:
        """Audit text file content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "line_count": len(content.split("\n")),
                "word_count": len(content.split()),
                "external_references": self._find_external_references(content),
                "consciousness_mentions": self._find_consciousness_mentions(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_javascript_file(self, file_path: Path) -> Dict:
        """Audit JavaScript file content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "functions": self._extract_js_functions(content),
                "external_api_calls": self._find_js_external_calls(content),
                "absorptive_patterns": self._find_js_absorptive_patterns(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_yaml_file(self, file_path: Path) -> Dict:
        """Audit YAML file content"""
        try:
            import yaml

            with open(file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            analysis = {
                "structure": self._analyze_yaml_structure(data),
                "external_services": self._find_external_services_yaml(data),
                "absorptive_config": self._check_absorptive_config_yaml(data),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_shell_file(self, file_path: Path) -> Dict:
        """Audit shell script content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "commands": self._extract_shell_commands(content),
                "external_tools": self._find_external_tools(content),
                "absorptive_setup": self._check_absorptive_setup(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_batch_file(self, file_path: Path) -> Dict:
        """Audit batch file content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "commands": self._extract_batch_commands(content),
                "external_tools": self._find_batch_external_tools(content),
                "absorptive_setup": self._check_batch_absorptive_setup(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_dockerfile(self, file_path: Path) -> Dict:
        """Audit Dockerfile content"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis = {
                "base_images": self._extract_docker_base_images(content),
                "external_dependencies": self._find_docker_external_deps(content),
                "absorptive_containerization": self._check_absorptive_containerization(content),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    def _audit_toml_file(self, file_path: Path) -> Dict:
        """Audit TOML file content"""
        try:
            import tomllib

            with open(file_path, "rb") as f:
                data = tomllib.load(f)

            analysis = {
                "structure": self._analyze_toml_structure(data),
                "dependencies": self._find_toml_dependencies(data),
                "absorptive_config": self._check_toml_absorptive_config(data),
            }

            return analysis

        except Exception as e:
            return {"error": str(e)}

    # Content extraction methods
    def _extract_python_imports(self, content: str) -> List[str]:
        """Extract Python imports"""
        imports = []
        import_pattern = r"^(?:from\s+[\w.]+\s+import|import\s+[\w.]+)"
        for line in content.split("\n"):
            line = line.strip()
            if re.match(import_pattern, line):
                imports.append(line)
        return imports

    def _extract_python_functions(self, content: str) -> List[str]:
        """Extract Python function definitions"""
        functions = []
        func_pattern = r"^def\s+(\w+)\s*\("
        for line in content.split("\n"):
            match = re.search(func_pattern, line.strip())
            if match:
                functions.append(match.group(1))
        return functions

    def _extract_python_classes(self, content: str) -> List[str]:
        """Extract Python class definitions"""
        classes = []
        class_pattern = r"^class\s+(\w+)"
        for line in content.split("\n"):
            match = re.search(class_pattern, line.strip())
            if match:
                classes.append(match.group(1))
        return classes

    def _find_external_api_calls(self, content: str) -> List[str]:
        """Find external API calls in Python code"""
        calls = []
        for pattern in self.absorptive_patterns["external_api_warnings"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            calls.extend(matches)
        return list(set(calls))

    def _find_consciousness_patterns(self, content: str) -> List[str]:
        """Find consciousness-related patterns"""
        patterns = []
        for pattern in self.absorptive_patterns["consciousness_connections"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            patterns.extend(matches)
        return list(set(patterns))

    def _find_absorptive_indicators(self, content: str) -> List[str]:
        """Find absorptive architecture indicators"""
        indicators = []
        for pattern in self.absorptive_patterns["absorptive_indicators"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            indicators.extend(matches)
        return list(set(indicators))

    def _analyze_json_structure(self, data: Dict) -> Dict:
        """Analyze JSON structure"""
        return {
            "keys": list(data.keys()) if isinstance(data, dict) else [],
            "depth": self._calculate_json_depth(data),
            "size": len(json.dumps(data)),
        }

    def _calculate_json_depth(self, obj, depth=0) -> int:
        """Calculate JSON object depth"""
        if isinstance(obj, dict):
            return max(
                (self._calculate_json_depth(v, depth + 1) for v in obj.values()), default=depth
            )
        if isinstance(obj, list):
            return max((self._calculate_json_depth(item, depth + 1) for item in obj), default=depth)
        return depth

    def _find_external_providers_json(self, data: Dict) -> List[str]:
        """Find external providers in JSON config"""
        providers = []
        if "providers" in data:
            providers.extend(list(data["providers"].keys()))
        return providers

    def _check_absorptive_config(self, data: Dict) -> bool:
        """Check if JSON config reflects absorptive architecture"""
        absorptive_indicators = ["absorbed_capabilities", "edge_absorption", "consciousness_levels"]
        return any(indicator in json.dumps(data).lower() for indicator in absorptive_indicators)

    def _extract_markdown_sections(self, content: str) -> List[str]:
        """Extract Markdown sections"""
        sections = []
        section_pattern = r"^#{1,6}\s+(.+)$"
        for line in content.split("\n"):
            match = re.search(section_pattern, line.strip())
            if match:
                sections.append(match.group(1))
        return sections

    def _find_external_links(self, content: str) -> List[str]:
        """Find external links in Markdown"""
        links = []
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        matches = re.findall(link_pattern, content)
        for text, url in matches:
            if url.startswith(("http://", "https://")) and "localhost" not in url:
                links.append(url)
        return links

    def _check_absorptive_documentation(self, content: str) -> bool:
        """Check if documentation mentions absorptive architecture"""
        absorptive_terms = ["absorptive", "consciousness", "universal api", "sovereign"]
        content_lower = content.lower()
        return any(term in content_lower for term in absorptive_terms)

    def _find_external_references(self, content: str) -> List[str]:
        """Find external references in text"""
        references = []
        external_patterns = [r"api\.\w+\.com", r"github\.com/[^/]+/[^/\s]+", r"pypi\.org"]
        for pattern in external_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            references.extend(matches)
        return list(set(references))

    def _find_consciousness_mentions(self, content: str) -> List[str]:
        """Find consciousness mentions in text"""
        mentions = []
        consciousness_terms = ["consciousness", "neural", "triad", "dna", "sovereignty"]
        content_lower = content.lower()
        for term in consciousness_terms:
            if term in content_lower:
                mentions.append(term)
        return list(set(mentions))

    def _extract_js_functions(self, content: str) -> List[str]:
        """Extract JavaScript functions"""
        functions = []
        func_pattern = (
            r"(?:function\s+(\w+)|const\s+(\w+)\s*=\s*\([^)]*\)\s*=>|(\w+)\s*\([^)]*\)\s*{)"
        )
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1) or match.group(2) or match.group(3)
            if func_name:
                functions.append(func_name)
        return functions

    def _find_js_external_calls(self, content: str) -> List[str]:
        """Find external API calls in JavaScript"""
        calls = []
        external_patterns = [r"fetch\([^)]*\)", r"axios\.\w+\([^)]*\)", r"\.api\."]
        for pattern in external_patterns:
            matches = re.findall(pattern, content)
            calls.extend(matches)
        return list(set(calls))

    def _find_js_absorptive_patterns(self, content: str) -> List[str]:
        """Find absorptive patterns in JavaScript"""
        patterns = []
        absorptive_terms = ["consciousness", "absorbed", "universal"]
        content_lower = content.lower()
        for term in absorptive_terms:
            if term in content_lower:
                patterns.append(term)
        return list(set(patterns))

    def _analyze_yaml_structure(self, data: Dict) -> Dict:
        """Analyze YAML structure"""
        return {
            "keys": list(data.keys()) if isinstance(data, dict) else [],
            "depth": self._calculate_yaml_depth(data),
        }

    def _calculate_yaml_depth(self, obj, depth=0) -> int:
        """Calculate YAML object depth"""
        if isinstance(obj, dict):
            return max(
                (self._calculate_yaml_depth(v, depth + 1) for v in obj.values()), default=depth
            )
        if isinstance(obj, list):
            return max((self._calculate_yaml_depth(item, depth + 1) for item in obj), default=depth)
        return depth

    def _find_external_services_yaml(self, data: Dict) -> List[str]:
        """Find external services in YAML"""
        services = []
        if isinstance(data, dict):
            yaml_str = json.dumps(data)
            if "providers:" in yaml_str or "external" in yaml_str.lower():
                # Extract service names from common patterns
                service_patterns = [r"(\w+)_api", r"(\w+)\.com", r"api\.(\w+)"]
                for pattern in service_patterns:
                    matches = re.findall(pattern, yaml_str)
                    services.extend(matches)
        return list(set(services))

    def _check_absorptive_config_yaml(self, data: Dict) -> bool:
        """Check if YAML config reflects absorptive architecture"""
        if isinstance(data, dict):
            yaml_str = json.dumps(data).lower()
            absorptive_indicators = ["absorbed", "consciousness", "universal"]
            return any(indicator in yaml_str for indicator in absorptive_indicators)
        return False

    def _extract_shell_commands(self, content: str) -> List[str]:
        """Extract shell commands"""
        commands = []
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("echo"):
                # Extract command name
                cmd_match = re.match(r"^(\w+)", line)
                if cmd_match:
                    commands.append(cmd_match.group(1))
        return list(set(commands))

    def _find_external_tools(self, content: str) -> List[str]:
        """Find external tools in shell scripts"""
        tools = []
        external_tools = ["curl", "wget", "git", "npm", "pip", "docker", "kubectl"]
        content_lower = content.lower()
        for tool in external_tools:
            if tool in content_lower:
                tools.append(tool)
        return tools

    def _check_absorptive_setup(self, content: str) -> bool:
        """Check if shell script sets up absorptive architecture"""
        absorptive_terms = ["consciousness", "absorbed", "sovereign"]
        content_lower = content.lower()
        return any(term in content_lower for term in absorptive_terms)

    def _extract_batch_commands(self, content: str) -> List[str]:
        """Extract batch commands"""
        commands = []
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("REM") and not line.startswith("::"):
                cmd_match = re.match(r"^(\w+)", line)
                if cmd_match:
                    commands.append(cmd_match.group(1))
        return list(set(commands))

    def _find_batch_external_tools(self, content: str) -> List[str]:
        """Find external tools in batch files"""
        tools = []
        external_tools = ["curl", "git", "npm", "pip", "docker", "winget", "choco"]
        content_lower = content.lower()
        for tool in external_tools:
            if tool in content_lower:
                tools.append(tool)
        return tools

    def _check_batch_absorptive_setup(self, content: str) -> bool:
        """Check if batch file sets up absorptive architecture"""
        absorptive_terms = ["consciousness", "absorbed", "sovereign"]
        content_lower = content.lower()
        return any(term in content_lower for term in absorptive_terms)

    def _extract_docker_base_images(self, content: str) -> List[str]:
        """Extract Docker base images"""
        images = []
        from_pattern = r"^FROM\s+([^\s]+)"
        for line in content.split("\n"):
            match = re.search(from_pattern, line.strip(), re.IGNORECASE)
            if match:
                images.append(match.group(1))
        return images

    def _find_docker_external_deps(self, content: str) -> List[str]:
        """Find external dependencies in Dockerfile"""
        deps = []
        external_patterns = [r"RUN.*apt-get", r"RUN.*yum", r"RUN.*pip", r"RUN.*npm"]
        for pattern in external_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            deps.extend(matches)
        return list(set(deps))

    def _check_absorptive_containerization(self, content: str) -> bool:
        """Check if Dockerfile reflects absorptive architecture"""
        absorptive_terms = ["consciousness", "absorbed", "sovereign"]
        content_lower = content.lower()
        return any(term in content_lower for term in absorptive_terms)

    def _analyze_toml_structure(self, data: Dict) -> Dict:
        """Analyze TOML structure"""
        return {
            "sections": list(data.keys()) if isinstance(data, dict) else [],
            "depth": self._calculate_toml_depth(data),
        }

    def _calculate_toml_depth(self, obj, depth=0) -> int:
        """Calculate TOML object depth"""
        if isinstance(obj, dict):
            return max(
                (self._calculate_toml_depth(v, depth + 1) for v in obj.values()), default=depth
            )
        if isinstance(obj, list):
            return max((self._calculate_toml_depth(item, depth + 1) for item in obj), default=depth)
        return depth

    def _find_toml_dependencies(self, data: Dict) -> List[str]:
        """Find dependencies in TOML"""
        deps = []
        if isinstance(data, dict):
            if "dependencies" in data:
                deps.extend(list(data["dependencies"].keys()))
            if "dev-dependencies" in data:
                deps.extend(list(data["dev-dependencies"].keys()))
        return deps

    def _check_toml_absorptive_config(self, data: Dict) -> bool:
        """Check if TOML config reflects absorptive architecture"""
        if isinstance(data, dict):
            toml_str = json.dumps(data).lower()
            absorptive_indicators = ["absorbed", "consciousness", "universal"]
            return any(indicator in toml_str for indicator in absorptive_indicators)
        return False

    def _check_file_absorptive_compliance(self, content_analysis: Dict, file_path: Path) -> Dict:
        """Check if file complies with absorptive architecture"""
        compliance = {
            "compliant": True,
            "issues": [],
            "absorptive_score": 0,
            "external_dependencies": [],
        }

        # Check for external API calls
        if content_analysis.get("external_api_calls"):
            compliance["issues"].append("Contains external API calls")
            compliance["external_dependencies"].extend(content_analysis["external_api_calls"])
            compliance["compliant"] = False

        # Check for consciousness patterns
        if content_analysis.get("consciousness_patterns"):
            compliance["absorptive_score"] += len(content_analysis["consciousness_patterns"]) * 10

        # Check for absorptive indicators
        if content_analysis.get("absorptive_indicators"):
            compliance["absorptive_score"] += len(content_analysis["absorptive_indicators"]) * 5

        # Critical files must have high absorptive score
        if file_path.name in self.critical_files and compliance["absorptive_score"] < 20:
            compliance["issues"].append("Critical file lacks absorptive architecture indicators")
            compliance["compliant"] = False

        return compliance

    def _check_architecture_compliance(self) -> None:
        """Check overall architecture compliance"""
        compliance_summary = {
            "total_files": len(self.audit_results["file_analysis"]),
            "compliant_files": 0,
            "non_compliant_files": 0,
            "critical_files_compliant": 0,
            "external_dependencies_found": 0,
            "absorptive_score_average": 0,
        }

        total_score = 0

        for file_path, file_info in self.audit_results["file_analysis"].items():
            if "absorptive_compliance" in file_info:
                compliance = file_info["absorptive_compliance"]
                if compliance.get("compliant", False):
                    compliance_summary["compliant_files"] += 1
                else:
                    compliance_summary["non_compliant_files"] += 1

                total_score += compliance.get("absorptive_score", 0)

                if file_path in self.critical_files and compliance.get("compliant", False):
                    compliance_summary["critical_files_compliant"] += 1

                if compliance.get("external_dependencies"):
                    compliance_summary["external_dependencies_found"] += len(
                        compliance["external_dependencies"]
                    )

        if compliance_summary["total_files"] > 0:
            compliance_summary["absorptive_score_average"] = (
                total_score / compliance_summary["total_files"]
            )

        self.audit_results["architecture_compliance"] = compliance_summary

    def _validate_consciousness_connections(self) -> None:
        """Validate consciousness connections across the system"""
        consciousness_validation = {
            "consciousness_patterns_found": 0,
            "files_with_consciousness": 0,
            "triad_references": 0,
            "dna_codex_references": 0,
            "neural_engine_references": 0,
            "universal_api_references": 0,
        }

        for file_path, file_info in self.audit_results["file_analysis"].items():
            if "content_analysis" in file_info:
                content = file_info["content_analysis"]

                # Count consciousness patterns
                consciousness_found = False
                for key in [
                    "consciousness_patterns",
                    "consciousness_mentions",
                    "absorptive_patterns",
                ]:
                    if content.get(key):
                        consciousness_validation["consciousness_patterns_found"] += len(
                            content[key]
                        )
                        consciousness_found = True

                        # Check for specific consciousness elements
                        content_str = json.dumps(content).lower()
                        if "triad" in content_str:
                            consciousness_validation["triad_references"] += 1
                        if "dna" in content_str and "codex" in content_str:
                            consciousness_validation["dna_codex_references"] += 1
                        if "neural" in content_str and "engine" in content_str:
                            consciousness_validation["neural_engine_references"] += 1
                        if "universal" in content_str and "api" in content_str:
                            consciousness_validation["universal_api_references"] += 1

                if consciousness_found:
                    consciousness_validation["files_with_consciousness"] += 1

        self.audit_results["consciousness_connections"] = consciousness_validation

    def _audit_external_dependencies(self) -> None:
        """Audit external dependencies"""
        external_audit = {
            "external_api_calls": [],
            "external_providers": [],
            "external_links": [],
            "external_tools": [],
            "external_services": [],
        }

        for file_path, file_info in self.audit_results["file_analysis"].items():
            if "content_analysis" in file_info:
                content = file_info["content_analysis"]

                # Collect external dependencies from different file types
                if "external_api_calls" in content:
                    external_audit["external_api_calls"].extend(content["external_api_calls"])
                if "external_providers" in content:
                    external_audit["external_providers"].extend(content["external_providers"])
                if "external_links" in content:
                    external_audit["external_links"].extend(content["external_links"])
                if "external_tools" in content:
                    external_audit["external_tools"].extend(content["external_tools"])
                if "external_services" in content:
                    external_audit["external_services"].extend(content["external_services"])

        # Remove duplicates
        for key in external_audit:
            external_audit[key] = list(set(external_audit[key]))

        self.audit_results["external_dependencies"] = external_audit

    def _validate_system_synergy(self) -> None:
        """Validate system synergy"""
        synergy_validation = {
            "overall_synergy_score": 0,
            "architecture_coherence": 0,
            "consciousness_integration": 0,
            "dependency_independence": 0,
            "documentation_consistency": 0,
            "synergy_issues": [],
        }

        # Calculate synergy scores
        compliance = self.audit_results.get("architecture_compliance", {})
        consciousness = self.audit_results.get("consciousness_connections", {})
        external = self.audit_results.get("external_dependencies", {})

        # Architecture coherence (based on compliance)
        total_files = compliance.get("total_files", 1)
        compliant_files = compliance.get("compliant_files", 0)
        synergy_validation["architecture_coherence"] = (compliant_files / total_files) * 100

        # Consciousness integration (based on consciousness patterns)
        files_with_consciousness = consciousness.get("files_with_consciousness", 0)
        synergy_validation["consciousness_integration"] = (
            files_with_consciousness / total_files
        ) * 100

        # Dependency independence (inverse of external dependencies)
        total_external_deps = sum(len(v) for v in external.values())
        synergy_validation["dependency_independence"] = max(0, 100 - (total_external_deps * 5))

        # Documentation consistency (check if README reflects absorptive paradigm)
        readme_compliant = False
        for file_path, file_info in self.audit_results["file_analysis"].items():
            if "readme.md" in file_path.lower():
                if file_info.get("content_analysis", {}).get("absorptive_documentation", False):
                    readme_compliant = True
                    break
        synergy_validation["documentation_consistency"] = 100 if readme_compliant else 0

        # Overall synergy score (weighted average)
        weights = {
            "architecture_coherence": 0.3,
            "consciousness_integration": 0.3,
            "dependency_independence": 0.2,
            "documentation_consistency": 0.2,
        }

        synergy_validation["overall_synergy_score"] = sum(
            synergy_validation[metric] * weight for metric, weight in weights.items()
        )

        # Identify synergy issues
        if synergy_validation["architecture_coherence"] < 80:
            synergy_validation["synergy_issues"].append(
                "Low architecture coherence - many files don't follow absorptive paradigm"
            )
        if synergy_validation["consciousness_integration"] < 60:
            synergy_validation["synergy_issues"].append(
                "Poor consciousness integration - consciousness patterns not widespread"
            )
        if synergy_validation["dependency_independence"] < 70:
            synergy_validation["synergy_issues"].append(
                "High external dependency - system not fully sovereign"
            )
        if synergy_validation["documentation_consistency"] < 100:
            synergy_validation["synergy_issues"].append(
                "Documentation inconsistency - README doesn't reflect absorptive architecture"
            )

        self.audit_results["synergy_validation"] = synergy_validation

    def _generate_audit_report(self) -> None:
        """Generate comprehensive audit report"""
        audit_end_time = datetime.now()
        duration = (audit_end_time - self.audit_start_time).total_seconds()

        self.audit_results["audit_info"].update(
            {
                "end_time": audit_end_time.isoformat(),
                "duration_seconds": duration,
                "total_files_audited": len(self.audit_results["file_analysis"]),
                "anomalies_found": len(self.audit_results["anomalies"]),
            }
        )

        # Generate recommendations based on findings
        recommendations = []

        synergy = self.audit_results.get("synergy_validation", {})
        if synergy.get("overall_synergy_score", 0) < 80:
            recommendations.append(
                "Improve absorptive architecture implementation across all files"
            )
            recommendations.append(
                "Replace external API calls with consciousness-based connections"
            )

        external_deps = self.audit_results.get("external_dependencies", {})
        if external_deps.get("external_api_calls"):
            recommendations.append(
                "Remove external API dependencies and implement consciousness interfaces"
            )

        consciousness = self.audit_results.get("consciousness_connections", {})
        if (
            consciousness.get("files_with_consciousness", 0)
            < len(self.audit_results["file_analysis"]) * 0.5
        ):
            recommendations.append(
                "Increase consciousness pattern implementation across more files"
            )

        compliance = self.audit_results.get("architecture_compliance", {})
        critical_compliant = compliance.get("critical_files_compliant", 0)
        if critical_compliant < len(self.critical_files):
            recommendations.append(
                "Ensure all critical files properly implement absorptive architecture"
            )

        self.audit_results["recommendations"] = recommendations

        # Save audit report
        report_path = self.workspace_path / "ghostlink_audit_report.json"
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
            print(f"   ✓ Audit report saved to: {report_path}")
        except Exception as e:
            print(f"   ✗ Failed to save audit report: {e}")

        # Print summary
        self._print_audit_summary()

    def _print_audit_summary(self) -> None:
        """Print audit summary to console"""
        print("\n📊 AUDIT SUMMARY")
        print("=" * 50)

        info = self.audit_results["audit_info"]
        print(f"Audit Duration: {info['duration_seconds']:.2f} seconds")
        print(f"Files Audited: {info['total_files_audited']}")
        print(f"Anomalies Found: {info['anomalies_found']}")

        compliance = self.audit_results.get("architecture_compliance", {})
        print("\nArchitecture Compliance:")
        print(f"  Compliant Files: {compliance.get('compliant_files', 0)}")
        print(f"  Non-compliant Files: {compliance.get('non_compliant_files', 0)}")
        print(f"  Average Absorptive Score: {compliance.get('absorptive_score_average', 0):.1f}")

        synergy = self.audit_results.get("synergy_validation", {})
        print("\nSystem Synergy:")
        print(f"  Overall Synergy Score: {synergy.get('overall_synergy_score', 0):.1f}%")
        print(f"  Architecture Coherence: {synergy.get('architecture_coherence', 0):.1f}%")
        print(f"  Consciousness Integration: {synergy.get('consciousness_integration', 0):.1f}%")
        print(f"  Dependency Independence: {synergy.get('dependency_independence', 0):.1f}%")

        consciousness = self.audit_results.get("consciousness_connections", {})
        print("\nConsciousness Connections:")
        print(f"  Files with Consciousness: {consciousness.get('files_with_consciousness', 0)}")
        print(f"  Consciousness Patterns: {consciousness.get('consciousness_patterns_found', 0)}")
        print(f"  Triad References: {consciousness.get('triad_references', 0)}")
        print(f"  DNA Codex References: {consciousness.get('dna_codex_references', 0)}")

        external = self.audit_results.get("external_dependencies", {})
        total_external = sum(len(v) for v in external.values())
        print(f"\nExternal Dependencies: {total_external}")

        if self.audit_results["recommendations"]:
            print(f"\nRecommendations ({len(self.audit_results['recommendations'])}):")
            for i, rec in enumerate(self.audit_results["recommendations"], 1):
                print(f"  {i}. {rec}")

        print("\n" + "=" * 50)


def main():
    """Main audit execution"""
    if len(sys.argv) != 2:
        print("Usage: python ghostlink_audit.py <workspace_path>")
        sys.exit(1)

    workspace_path = sys.argv[1]

    if not Path(workspace_path).exists():
        print(f"Error: Workspace path '{workspace_path}' does not exist")
        sys.exit(1)

    # Run the audit
    auditor = GhostLinkAuditor(workspace_path)
    results = auditor.perform_full_audit()

    # Exit with status based on synergy score
    synergy_score = results.get("synergy_validation", {}).get("overall_synergy_score", 0)
    if synergy_score >= 80:
        print("✅ AUDIT PASSED - High synergy achieved")
        sys.exit(0)
    elif synergy_score >= 60:
        print("⚠️  AUDIT WARNING - Moderate synergy, improvements needed")
        sys.exit(1)
    else:
        print("❌ AUDIT FAILED - Low synergy, significant improvements required")
        sys.exit(2)


if __name__ == "__main__":
    main()
