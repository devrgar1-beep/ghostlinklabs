"""Example integration of automation policy into existing components.

This shows how to retrofit automation awareness into GhostLink components.
"""
from __future__ import annotations

from ..automation import policy


class ExampleComponent:
    """Example component with automation support."""
    
    def __init__(self, name: str):
        self.name = name
        self.auto_mode = policy.automate_all()
        self.approval_mode = policy.auto_approve()
    
    def perform_operation(self, operation_name: str, requires_approval: bool = False) -> dict:
        """Perform an operation with automation checks."""
        
        result = {
            "component": self.name,
            "operation": operation_name,
            "automation_enabled": self.auto_mode,
        }
        
        # Check if operation requires approval
        if requires_approval:
            if self.approval_mode:
                result["status"] = "auto_approved"
                result["executed"] = True
                print(f"[{self.name}] ✓ Auto-approved and executed: {operation_name}")
            else:
                result["status"] = "pending_approval"
                result["executed"] = False
                print(f"[{self.name}] ⚠ Awaiting manual approval: {operation_name}")
        else:
            # Non-sensitive operation
            if self.auto_mode:
                result["status"] = "auto_executed"
                result["executed"] = True
                print(f"[{self.name}] ✓ Automated execution: {operation_name}")
            else:
                result["status"] = "manual_execution"
                result["executed"] = False
                print(f"[{self.name}] ⚠ Manual execution required: {operation_name}")
        
        return result
    
    def experimental_feature(self, feature_name: str, required_level: str = "partial") -> dict:
        """Run an experimental feature if policy allows."""
        
        current_level = policy.experimental_level()
        enabled = policy.experimental_enabled()
        
        result = {
            "component": self.name,
            "feature": feature_name,
            "experimental_mode": current_level,
            "required_level": required_level,
        }
        
        if not enabled:
            result["status"] = "disabled"
            result["executed"] = False
            print(f"[{self.name}] ✗ Experimental features disabled: {feature_name}")
            return result
        
        # Check level requirements
        level_order = {"off": 0, "partial": 1, "full": 2}
        current_priority = level_order.get(current_level, 0)
        required_priority = level_order.get(required_level, 0)
        
        if current_priority >= required_priority:
            result["status"] = "enabled"
            result["executed"] = True
            print(f"[{self.name}] ✓ Experimental feature enabled ({current_level}): {feature_name}")
        else:
            result["status"] = "insufficient_level"
            result["executed"] = False
            print(f"[{self.name}] ⚠ Insufficient experimental level for: {feature_name}")
        
        return result


# Example usage patterns
def demonstrate_integration():
    """Show various integration patterns."""
    print("=" * 70)
    print("Component Automation Integration Examples")
    print("=" * 70)
    print()
    
    # Example 1: Core component with automation
    print("Example 1: Core Component Operations")
    print("-" * 70)
    component = ExampleComponent("CORE_PROCESSOR")
    component.perform_operation("process_data", requires_approval=False)
    component.perform_operation("sync_database", requires_approval=True)
    print()
    
    # Example 2: Daemon with experimental features
    print("Example 2: Daemon with Experimental Features")
    print("-" * 70)
    daemon = ExampleComponent("BACKGROUND_DAEMON")
    daemon.experimental_feature("neural_integration", required_level="full")
    daemon.experimental_feature("basic_monitoring", required_level="partial")
    print()
    
    # Example 3: Tool with mixed operations
    print("Example 3: Tool Chain with Mixed Operations")
    print("-" * 70)
    tool = ExampleComponent("TOOL_ORCHESTRATOR")
    tool.perform_operation("load_configuration", requires_approval=False)
    tool.experimental_feature("quantum_resolver", required_level="full")
    tool.perform_operation("deploy_changes", requires_approval=True)
    print()
    
    print("=" * 70)
    print("Integration demonstration complete")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_integration()
