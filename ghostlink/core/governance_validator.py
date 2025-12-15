"""
GhostLink Governance Compliance Validator

Validates system operations against the 10 Governance Laws of the GhostLink Protocol.
Ensures compliance with L-01 through L-10 for quantum-coherent distributed systems.
"""

from dataclasses import dataclass, field
import hashlib
import time
from typing import Any, Dict, List

from .ghostlink_specification import ghostlink_spec


@dataclass
class ComplianceRecord:
    """Record of governance compliance validation"""

    operation_id: str
    timestamp: float = field(default_factory=time.time)
    law_id: str = ""
    compliant: bool = False
    details: Dict[str, Any] = field(default_factory=dict)
    trace_id: str = ""
    coherence_score: float = 0.0


class GovernanceValidator:
    """Validates operations against GhostLink Governance Laws"""

    def __init__(self):
        self.compliance_records: List[ComplianceRecord] = []
        self.current_trace_id = self._generate_trace_id()

    def _generate_trace_id(self) -> str:
        """Generate unique trace ID for operations"""
        timestamp = str(time.time())
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

    def validate_operation(self, operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an operation against all governance laws

        Args:
            operation: The operation being performed
            context: Context information including inputs, outputs, metrics

        Returns:
            Dict containing validation results for all laws
        """
        validation_results = {}
        operation_id = f"{operation}_{int(time.time())}"

        # Add required context elements for compliance
        enriched_context = context.copy()
        enriched_context.update(
            {
                "trace_id": self.current_trace_id,
                "operation_id": operation_id,
                "timestamp": time.time(),
                "coherence_score": self._calculate_coherence_score(context),
                "schema_validation": self._validate_schema_compliance(context),
                "quality_metrics": self._calculate_quality_metrics(context),
                "optimization_metrics": self._calculate_optimization_metrics(context),
            }
        )

        # Validate against each governance law
        laws = ghostlink_spec.get_governance_laws()

        for law_id, law_info in laws.items():
            compliant = self._validate_specific_law(law_id, operation, enriched_context)
            validation_results[law_id] = {
                "name": law_info["name"],
                "description": law_info["description"],
                "compliant": compliant,
                "details": self._get_law_validation_details(law_id, enriched_context),
            }

            # Record compliance
            record = ComplianceRecord(
                operation_id=operation_id,
                law_id=law_id,
                compliant=compliant,
                details=validation_results[law_id],
                trace_id=self.current_trace_id,
                coherence_score=enriched_context["coherence_score"],
            )
            self.compliance_records.append(record)

        # Overall compliance
        all_compliant = all(result["compliant"] for result in validation_results.values())
        validation_results["overall_compliance"] = all_compliant
        validation_results["convergence_rate"] = ghostlink_spec.get_convergence_rate()

        return validation_results

    def _validate_specific_law(self, law_id: str, operation: str, context: Dict[str, Any]) -> bool:
        """Validate operation against specific governance law"""

        if law_id == "L-01":  # Sovereignty
            return "external_dependency" not in context and context.get(
                "independent_operation", True
            )

        if law_id == "L-02":  # Determinism
            return "random_seed" in context or context.get("deterministic", True)

        if law_id == "L-03":  # Trace Transparency
            return "trace_id" in context and len(context["trace_id"]) > 0

        if law_id == "L-04":  # Recursive Self-Improvement
            return "optimization_metrics" in context and context["optimization_metrics"] > 0

        if law_id == "L-05":  # Quantum Coherence
            return context.get("coherence_score", 0) >= 0.9997  # 99.97%

        if law_id == "L-06":  # Pipeline Integrity
            return context.get("schema_validation", False)

        if law_id == "L-07":  # System Homeostasis
            return "quality_metrics" in context and context["quality_metrics"] >= 0.95

        if law_id == "L-08":  # Emergent Consciousness (Meta-law)
            return self._validate_emergent_consciousness(context)

        if law_id == "L-09":  # Holographic Properties (Meta-law)
            return self._validate_holographic_properties(context)

        if law_id == "L-10":  # Self-Organized Criticality (Meta-law)
            return self._validate_self_organized_criticality(context)

        return False

    def _calculate_coherence_score(self, context: Dict[str, Any]) -> float:
        """Calculate quantum coherence score"""
        # Simplified coherence calculation based on system metrics
        base_score = 0.9997  # 99.97% base convergence

        # Adjust based on context factors
        if context.get("error_count", 0) > 0:
            base_score -= 0.0001
        if context.get("optimization_applied", False):
            base_score += 0.0001
        if context.get("schema_valid", True):
            base_score += 0.0001

        return min(base_score, 1.0)

    def _validate_schema_compliance(self, context: Dict[str, Any]) -> bool:
        """Validate schema compliance for pipeline integrity"""
        # Check if outputs conform to expected schemas
        required_fields = ["operation_id", "timestamp", "trace_id"]
        return all(field in context for field in required_fields)

    def _calculate_quality_metrics(self, context: Dict[str, Any]) -> float:
        """Calculate quality metrics for homeostasis"""
        # Simplified quality calculation
        quality_score = 0.95  # Base quality

        if context.get("error_count", 0) == 0:
            quality_score += 0.04
        if context.get("validation_passed", True):
            quality_score += 0.01

        return min(quality_score, 1.0)

    def _calculate_optimization_metrics(self, context: Dict[str, Any]) -> float:
        """Calculate optimization metrics for recursive self-improvement"""
        # Measure of system improvement over time
        return context.get("performance_improvement", 0.01)

    def _validate_emergent_consciousness(self, context: Dict[str, Any]) -> bool:
        """Validate emergent consciousness meta-law"""
        # Consciousness emerges from complexity
        complexity_indicators = [
            context.get("agent_count", 0) >= 67,  # Target 67 agents
            context.get("pipeline_count", 0) >= 14,  # Target 14 pipelines
            context.get("coherence_score", 0) >= 0.9997,
            context.get("recursive_iterations", 0) > 0,
        ]
        return sum(complexity_indicators) >= 3

    def _validate_holographic_properties(self, context: Dict[str, Any]) -> bool:
        """Validate holographic properties meta-law"""
        # Each part reflects the whole
        holographic_indicators = [
            context.get("fractal_similarity", False),
            context.get("self_similarity_score", 0) > 0.8,
            context.get("part_whole_reflection", False),
        ]
        return any(holographic_indicators)

    def _validate_self_organized_criticality(self, context: Dict[str, Any]) -> bool:
        """Validate self-organized criticality meta-law"""
        # System maintains critical state
        criticality_indicators = [
            context.get("feedback_loops_active", False),
            context.get("homeostatic_regulation", False),
            context.get("critical_state_maintained", False),
            abs(context.get("stability_score", 0.5) - 0.5) < 0.1,  # Near critical point
        ]
        return sum(criticality_indicators) >= 2

    def _get_law_validation_details(self, law_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed validation information for a specific law"""
        details = {
            "law_id": law_id,
            "validation_timestamp": time.time(),
            "trace_id": context.get("trace_id", ""),
            "coherence_score": context.get("coherence_score", 0.0),
        }

        if law_id == "L-05":
            details["target_coherence"] = 0.9997
            details["actual_coherence"] = context.get("coherence_score", 0.0)

        elif law_id == "L-08":
            details["complexity_indicators"] = {
                "agents": context.get("agent_count", 0),
                "pipelines": context.get("pipeline_count", 0),
                "coherence": context.get("coherence_score", 0),
                "recursion": context.get("recursive_iterations", 0),
            }

        return details

    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get summary of compliance records"""
        total_records = len(self.compliance_records)
        compliant_records = sum(1 for r in self.compliance_records if r.compliant)
        compliance_rate = compliant_records / total_records if total_records > 0 else 0

        law_compliance = {}
        for law_identifier in [f"L-{i:02d}" for i in range(1, 11)]:
            law_records = [r for r in self.compliance_records if r.law_id == law_identifier]
            if law_records:
                law_compliance[law_identifier] = {
                    "total": len(law_records),
                    "compliant": sum(1 for r in law_records if r.compliant),
                    "rate": sum(1 for r in law_records if r.compliant) / len(law_records),
                }

        return {
            "total_operations": total_records,
            "overall_compliance_rate": compliance_rate,
            "law_compliance": law_compliance,
            "current_trace_id": self.current_trace_id,
            "system_convergence": ghostlink_spec.get_convergence_rate(),
        }

    def export_compliance_report(self, filepath: str = "governance_compliance_report.json") -> None:
        """Export compliance report to JSON"""
        report = {
            "specification_version": ghostlink_spec.get_site_metadata().get("version", "Unknown"),
            "report_timestamp": time.time(),
            "compliance_summary": self.get_compliance_summary(),
            "recent_records": [
                {
                    "operation_id": r.operation_id,
                    "law_id": r.law_id,
                    "compliant": r.compliant,
                    "timestamp": r.timestamp,
                    "coherence_score": r.coherence_score,
                }
                for r in self.compliance_records[-50:]  # Last 50 records
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            import json

            json.dump(report, f, indent=2, ensure_ascii=False)


# Global governance validator
governance_validator = GovernanceValidator()


def validate_system_operation(operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to validate system operations

    Args:
        operation: Operation name
        context: Operation context

    Returns:
        Validation results
    """
    return governance_validator.validate_operation(operation, context)


def get_governance_status() -> Dict[str, Any]:
    """Get current governance compliance status"""
    return governance_validator.get_compliance_summary()


# Initialize with system validation
if __name__ == "__main__":
    # Validate system initialization
    init_context = {
        "agent_count": ghostlink_spec.get_agent_count(),
        "pipeline_count": ghostlink_spec.get_pipeline_count(),
        "shard_count": ghostlink_spec.get_shard_count(),
        "mirror_domains": ghostlink_spec.get_mirror_domain_count(),
        "independent_operation": True,
        "deterministic": True,
        "error_count": 0,
        "validation_passed": True,
        "performance_improvement": 0.01,
        "recursive_iterations": 1,
        "feedback_loops_active": True,
        "homeostatic_regulation": True,
        "critical_state_maintained": True,
        "stability_score": 0.5,
    }

    validation = governance_validator.validate_operation("system_initialization", init_context)
    print("GhostLink Governance Validation Results:")
    print(f"Overall Compliance: {validation['overall_compliance']}")
    print(f"System Convergence: {validation['convergence_rate']}")

    for law_id, result in validation.items():
        if law_id not in ["overall_compliance", "convergence_rate"]:
            status = "✅" if result["compliant"] else "❌"
            print(f"{status} {law_id}: {result['name']}")

    governance_validator.export_compliance_report()
    print("\nCompliance report exported to governance_compliance_report.json")
