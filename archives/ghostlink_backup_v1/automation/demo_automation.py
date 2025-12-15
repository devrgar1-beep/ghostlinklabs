#!/usr/bin/env python3
"""Demonstration of automation policy usage in GhostLink components.

This script shows how components can check automation settings
to decide whether to run autonomously or require manual approval.
"""
from __future__ import annotations

from . import policy


class AutomatedTaskRunner:
    """Example component that respects automation policy."""
    
    def execute_sensitive_operation(self, operation: str) -> dict[str, str | bool]:
        """Execute an operation that may require approval."""
        
        # Check if auto-approval is enabled
        if policy.auto_approve():
            print(f"✓ Auto-approving: {operation}")
            return {
                "operation": operation,
                "approved": True,
                "mode": "auto",
                "executed": True,
            }
        else:
            print(f"⚠ Manual approval required for: {operation}")
            return {
                "operation": operation,
                "approved": False,
                "mode": "manual",
                "executed": False,
            }
    
    def run_experimental_feature(self, feature: str) -> dict[str, str | bool]:
        """Run an experimental feature if enabled."""
        
        if not policy.experimental_enabled():
            print(f"✗ Experimental features disabled, skipping: {feature}")
            return {
                "feature": feature,
                "enabled": False,
                "level": policy.experimental_level(),
                "executed": False,
            }
        
        level = policy.experimental_level()
        if level == "full":
            print(f"✓ Running experimental feature (full mode): {feature}")
            executed = True
        elif level == "partial":
            # In partial mode, only run certain features
            safe_features = ["feature_a", "feature_b"]
            if feature in safe_features:
                print(f"✓ Running experimental feature (partial mode): {feature}")
                executed = True
            else:
                print(f"⚠ Feature not allowed in partial mode: {feature}")
                executed = False
        else:
            executed = False
        
        return {
            "feature": feature,
            "enabled": True,
            "level": level,
            "executed": executed,
        }
    
    def automate_workflow(self, workflow: str) -> dict[str, str | bool]:
        """Execute a workflow with automation if enabled."""
        
        if policy.automate_all():
            print(f"✓ Automating workflow: {workflow}")
            return {
                "workflow": workflow,
                "automated": True,
                "executed": True,
            }
        else:
            print(f"⚠ Automation disabled, workflow requires manual steps: {workflow}")
            return {
                "workflow": workflow,
                "automated": False,
                "executed": False,
            }


def main() -> None:
    """Run automation demonstration."""
    print("=" * 60)
    print("GhostLink Automation Policy Demonstration")
    print("=" * 60)
    print()
    
    print("Current Settings:")
    print(f"  AUTOMATE_ALL: {policy.automate_all()}")
    print(f"  AUTO_APPROVE: {policy.auto_approve()}")
    print(f"  EXPERIMENTAL_MODE: {policy.experimental_level()}")
    print(f"  experimental_enabled(): {policy.experimental_enabled()}")
    print()
    
    runner = AutomatedTaskRunner()
    
    print("Testing sensitive operations:")
    print("-" * 60)
    runner.execute_sensitive_operation("deploy_to_production")
    runner.execute_sensitive_operation("delete_critical_data")
    print()
    
    print("Testing experimental features:")
    print("-" * 60)
    runner.run_experimental_feature("neural_lattice_integration")
    runner.run_experimental_feature("quantum_resolver")
    runner.run_experimental_feature("bio_feedback_loop")
    print()
    
    print("Testing workflow automation:")
    print("-" * 60)
    runner.automate_workflow("data_pipeline_sync")
    runner.automate_workflow("autonomous_repair")
    print()
    
    print("=" * 60)
    print("Demonstration complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
