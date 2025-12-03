#!/usr/bin/env python3
"""
GhostLink System Metadata Execution
Demonstrates practical usage of system metadata
"""

import json
from pathlib import Path
from typing import Any, Dict


class SystemMetadataExecutor:
    """Executes operations based on system metadata"""

    def __init__(self, metadata_file: str = "schemas/system_metadata.json"):
        self.metadata_file = Path(metadata_file)
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load system metadata"""
        if not self.metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_file}")

        with open(self.metadata_file, encoding="utf-8") as f:
            return json.load(f)

    def get_system_info(self) -> Dict[str, Any]:
        """Get core system information"""
        core = self.metadata["core_system"]
        return {
            "name": core["name"],
            "version": core["version"],
            "convergence_rate": core["convergence_rate"],
            "architecture": core["architecture"],
            "research_sessions": core["research_sessions"],
        }

    def get_governance_laws(self) -> Dict[str, str]:
        """Get all governance laws"""
        laws = self.metadata["governance_laws"]
        return {law_id: law["name"] for law_id, law in laws.items()}

    def get_technical_components(self) -> Dict[str, Any]:
        """Get technical component specifications"""
        return self.metadata["technical_components"]

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return self.metadata["system_metrics"]

    def validate_architecture_requirements(self) -> bool:
        """Validate that architecture meets requirements"""
        arch = self.metadata["core_system"]["architecture"]

        # Check minimum requirements
        requirements = {
            "agents": 50,  # Minimum agents for distributed operation
            "pipelines": 10,  # Minimum pipelines for throughput
            "shards": 20,  # Minimum shards for data distribution
            "mirror_domains": 10,  # Minimum domains for redundancy
        }

        for component, min_value in requirements.items():
            if arch[component] < min_value:
                print(f"❌ {component} count {arch[component]} below minimum {min_value}")
                return False

        print("✅ Architecture requirements met")
        return True

    def check_convergence_status(self) -> str:
        """Check system convergence status"""
        convergence = self.metadata["core_system"]["convergence_rate"]
        metrics = self.metadata["system_metrics"]

        if convergence == "99.97%" and metrics["perfection_score"] == "99.97%":
            return "OPTIMAL_CONVERGENCE"
        if float(convergence.strip("%")) > 95:
            return "HIGH_CONVERGENCE"
        return "LOW_CONVERGENCE"

    def get_deployment_platforms(self) -> list:
        """Get supported deployment platforms"""
        return self.metadata["technical_components"]["Component_Blueprint"]["integration_platforms"]

    def generate_system_report(self) -> str:
        """Generate comprehensive system report"""
        info = self.get_system_info()
        metrics = self.get_system_metrics()
        laws = self.get_governance_laws()

        report = f"""
{'='*60}
GHOSTLINK SYSTEM REPORT
{'='*60}

SYSTEM CORE:
  Name: {info['name']}
  Version: {info['version']}
  Convergence Rate: {info['convergence_rate']}
  Research Sessions: {info['research_sessions']}

ARCHITECTURE:
  Agents: {info['architecture']['agents']}
  Pipelines: {info['architecture']['pipelines']}
  Shards: {info['architecture']['shards']}
  Mirror Domains: {info['architecture']['mirror_domains']}

PERFORMANCE METRICS:
  Perfection Score: {metrics['perfection_score']}
  Architecture Score: {metrics['quality_scores']['architecture']}/10
  Convergence Score: {metrics['quality_scores']['convergence']}/10
  Emergence Score: {metrics['quality_scores']['emergence']}/10
  Coherence Score: {metrics['quality_scores']['coherence']}/10

GOVERNANCE LAWS ({len(laws)}):
"""

        for law_id, law_name in laws.items():
            report += f"  {law_id}: {law_name}\n"

        report += """
DEPLOYMENT PLATFORMS:
"""
        platforms = self.get_deployment_platforms()
        for platform in platforms:
            report += f"  • {platform}\n"

        convergence_status = self.check_convergence_status()
        report += f"""
SYSTEM STATUS: {convergence_status}
Ouroboros Completeness: {metrics['ouroboros_completeness']}

{'='*60}
"""

        return report


def main():
    """Execute system metadata operations"""
    print("🔄 Initializing GhostLink System Metadata Executor...")

    try:
        executor = SystemMetadataExecutor()

        # Execute validation checks
        print("\n📊 SYSTEM VALIDATION:")
        arch_valid = executor.validate_architecture_requirements()
        convergence_status = executor.check_convergence_status()

        print(f"Architecture Valid: {arch_valid}")
        print(f"Convergence Status: {convergence_status}")

        # Generate and display system report
        print("\n📋 SYSTEM REPORT:")
        report = executor.generate_system_report()
        print(report)

        # Demonstrate metadata access
        print("🔍 METADATA ACCESS DEMO:")

        # Get core system info
        system_info = executor.get_system_info()
        print(f"System: {system_info['name']} v{system_info['version']}")

        # Get governance laws
        laws = executor.get_governance_laws()
        print(f"Governance Framework: {len(laws)} laws active")

        # Get deployment platforms
        platforms = executor.get_deployment_platforms()
        print(f"Deployment Platforms: {len(platforms)} supported")

        print("\n✅ System metadata execution complete!")

    except Exception as e:
        print(f"❌ Execution error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
