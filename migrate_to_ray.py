#!/usr/bin/env python3
"""
GhostLink Ray Migration Script
Migrates from multi_agent_engine.py to ray_orchestrator.py
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def backup_current_engine():
    """Create backup of current multi_agent_engine.py"""
    engine_path = Path("src/multi_agent_engine.py")
    backup_path = Path("src/multi_agent_engine.py.backup")

    if engine_path.exists() and not backup_path.exists():
        import shutil
        shutil.copy2(engine_path, backup_path)
        print(f"📦 Backed up {engine_path} to {backup_path}")
        return True
    return False

def analyze_current_engine():
    """Analyze the current multi_agent_engine.py for migration insights"""
    engine_path = Path("src/multi_agent_engine.py")

    if not engine_path.exists():
        print("❌ multi_agent_engine.py not found")
        return None

    with open(engine_path, 'r') as f:
        content = f.read()

    analysis = {
        "classes": [],
        "functions": [],
        "imports": [],
        "async_methods": [],
        "threading_usage": [],
        "model_operations": []
    }

    lines = content.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()

        # Find classes
        if line.startswith('class '):
            class_name = line.split('(')[0].replace('class ', '')
            analysis["classes"].append(class_name)

        # Find functions/methods
        elif line.startswith('def ') or line.startswith('    def '):
            func_name = line.split('(')[0].replace('def ', '').replace('    ', '')
            if 'async def' in line:
                analysis["async_methods"].append(func_name)
            else:
                analysis["functions"].append(func_name)

        # Find imports
        elif line.startswith('import ') or line.startswith('from '):
            analysis["imports"].append(line)

        # Find threading usage
        elif 'threading' in line.lower() or 'Thread' in line:
            analysis["threading_usage"].append(f"Line {i+1}: {line}")

        # Find model operations
        elif any(keyword in line.lower() for keyword in ['compress', 'expand', 'model', 'train', 'inference']):
            analysis["model_operations"].append(f"Line {i+1}: {line}")

    return analysis

def create_migration_adapter():
    """Create an adapter class that bridges old and new orchestrators"""

    adapter_code = '''#!/usr/bin/env python3
"""
GhostLink Ray Migration Adapter
Provides backward compatibility during transition to Ray orchestrator
"""

import asyncio
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ray_orchestrator import RayOrchestrator, ModelSize, ModelMetrics, CompressionType, ExpansionType
    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False

class MigrationAdapter:
    """
    Adapter class that provides the old multi_agent_engine interface
    while delegating to the new Ray orchestrator
    """

    def __init__(self, use_ray: bool = True):
        self.use_ray = use_ray and RAY_AVAILABLE

        if self.use_ray:
            print("🚀 Using Ray orchestrator")
            self.orchestrator = RayOrchestrator(
                num_compression_agents=2,
                num_expansion_agents=2,
                num_consciousness_agents=1
            )
        else:
            print("⚠️  Ray not available, falling back to legacy engine")
            # Import legacy engine if Ray fails
            try:
                from multi_agent_engine import MultiAgentEngine
                self.orchestrator = MultiAgentEngine()
            except ImportError:
                raise RuntimeError("Neither Ray orchestrator nor legacy engine available")

        # Compatibility mappings
        self.model_registry = {}
        self.active_tasks = []

    def register_model(self, model_id: str, model_path: str, **kwargs):
        """Register a model (compatible with old interface)"""
        if self.use_ray:
            # Convert old format to new format
            size_category = ModelSize.MEDIUM  # Default
            if 'size' in kwargs:
                size_str = kwargs['size'].lower()
                if 'tiny' in size_str:
                    size_category = ModelSize.TINY
                elif 'small' in size_str:
                    size_category = ModelSize.SMALL
                elif 'large' in size_str:
                    size_category = ModelSize.LARGE
                elif 'huge' in size_str:
                    size_category = ModelSize.HUGE

            metrics = ModelMetrics(
                parameter_count=kwargs.get('parameter_count', 1000000),
                model_size_mb=kwargs.get('model_size_mb', 500.0),
                inference_time_ms=kwargs.get('inference_time_ms', 50.0),
                memory_usage_mb=kwargs.get('memory_usage_mb', 1000.0),
                accuracy_score=kwargs.get('accuracy_score', 0.85)
            )

            return self.orchestrator.register_model(model_id, model_path, size_category, metrics)
        else:
            # Legacy interface
            return self.orchestrator.register_model(model_id, model_path, **kwargs)

    def compress_model(self, model_id: str, compression_type: str = "pruning", **kwargs):
        """Compress a model (compatible with old interface)"""
        if self.use_ray:
            # Convert string to enum
            comp_type = CompressionType.PRUNING
            if compression_type.lower() == "quantization":
                comp_type = CompressionType.QUANTIZATION
            elif compression_type.lower() == "distillation":
                comp_type = CompressionType.DISTILLATION

            task_id = self.orchestrator.submit_compression_task(
                model_id, comp_type, kwargs
            )
            self.active_tasks.append(task_id)
            return task_id
        else:
            return self.orchestrator.compress_model(model_id, compression_type, **kwargs)

    def expand_model(self, model_id: str, expansion_type: str = "layer_expansion", **kwargs):
        """Expand a model (compatible with old interface)"""
        if self.use_ray:
            # Convert string to enum
            exp_type = ExpansionType.LAYER_EXPANSION
            if expansion_type.lower() == "width":
                exp_type = ExpansionType.WIDTH_EXPANSION
            elif expansion_type.lower() == "depth":
                exp_type = ExpansionType.DEPTH_EXPANSION

            task_id = self.orchestrator.submit_expansion_task(
                model_id, exp_type, kwargs
            )
            self.active_tasks.append(task_id)
            return task_id
        else:
            return self.orchestrator.expand_model(model_id, expansion_type, **kwargs)

    def evolve_consciousness(self, **kwargs):
        """Evolve consciousness (compatible with old interface)"""
        if self.use_ray:
            task_id = self.orchestrator.submit_consciousness_task(kwargs)
            self.active_tasks.append(task_id)
            return task_id
        else:
            return self.orchestrator.evolve_consciousness(**kwargs)

    async def process_tasks(self):
        """Process pending tasks"""
        if self.use_ray:
            await self.orchestrator.process_tasks()
        else:
            await self.orchestrator.process_tasks()

    def get_status(self):
        """Get orchestrator status"""
        if self.use_ray:
            return self.orchestrator.get_status()
        else:
            return self.orchestrator.get_status()

    def shutdown(self):
        """Shutdown the orchestrator"""
        if self.use_ray:
            self.orchestrator.shutdown()
        else:
            self.orchestrator.shutdown()

# Global instance for backward compatibility
migration_adapter = MigrationAdapter()

# Backward compatibility functions
def register_model(model_id: str, model_path: str, **kwargs):
    return migration_adapter.register_model(model_id, model_path, **kwargs)

def compress_model(model_id: str, compression_type: str = "pruning", **kwargs):
    return migration_adapter.compress_model(model_id, compression_type, **kwargs)

def expand_model(model_id: str, expansion_type: str = "layer_expansion", **kwargs):
    return migration_adapter.expand_model(model_id, expansion_type, **kwargs)

def evolve_consciousness(**kwargs):
    return migration_adapter.evolve_consciousness(**kwargs)

async def process_tasks():
    await migration_adapter.process_tasks()

def get_status():
    return migration_adapter.get_status()

def shutdown():
    migration_adapter.shutdown()

if __name__ == "__main__":
    print("🔄 GhostLink Ray Migration Adapter")
    print("This adapter provides backward compatibility during the transition to Ray")
    print(f"Ray Available: {RAY_AVAILABLE}")
    print(f"Using Ray: {migration_adapter.use_ray}")
'''

    adapter_path = Path("src/migration_adapter.py")
    with open(adapter_path, 'w') as f:
        f.write(adapter_code)

    print(f"📝 Created migration adapter at {adapter_path}")
    return adapter_path

def update_imports():
    """Update any files that import multi_agent_engine to use migration_adapter"""
    files_to_check = [
        "src/main.py",
        "src/ghostlink_api_server.py",
        "src/ghostlink_api_server_enhanced.py",
        "tests/test_*.py"
    ]

    updated_files = []

    for file_pattern in files_to_check:
        import glob
        for file_path in glob.glob(file_pattern):
            if not Path(file_path).exists():
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            original_content = content

            # Replace imports
            content = content.replace(
                "from multi_agent_engine import",
                "from migration_adapter import"
            )
            content = content.replace(
                "import multi_agent_engine",
                "import migration_adapter as multi_agent_engine"
            )

            if content != original_content:
                with open(file_path, 'w') as f:
                    f.write(content)
                updated_files.append(file_path)
                print(f"🔄 Updated imports in {file_path}")

    return updated_files

def create_migration_report(analysis: Dict[str, Any]):
    """Create a migration report"""
    report = {
        "migration_timestamp": str(Path(__file__).stat().st_mtime),
        "current_engine_analysis": analysis,
        "ray_orchestrator_created": True,
        "migration_adapter_created": True,
        "backwards_compatibility": "maintained",
        "recommendations": [
            "Test the migration adapter with existing workflows",
            "Monitor performance improvements with Ray",
            "Gradually phase out legacy multi_agent_engine.py",
            "Update any direct instantiations to use MigrationAdapter",
            "Consider using Ray Tune for hyperparameter optimization"
        ]
    }

    report_path = Path("RAY_MIGRATION_REPORT.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"📊 Migration report saved to {report_path}")
    return report

def main():
    """Main migration function"""
    print("🚀 Starting GhostLink Ray Migration")
    print("=" * 50)

    # Step 1: Backup current engine
    print("\\n1. Backing up current engine...")
    backup_created = backup_current_engine()

    # Step 2: Analyze current engine
    print("\\n2. Analyzing current multi_agent_engine.py...")
    analysis = analyze_current_engine()
    if analysis:
        print(f"   Found {len(analysis['classes'])} classes: {analysis['classes']}")
        print(f"   Found {len(analysis['functions'])} functions")
        print(f"   Found {len(analysis['async_methods'])} async methods")
        print(f"   Found {len(analysis['threading_usage'])} threading usages")
        print(f"   Found {len(analysis['model_operations'])} model operations")

    # Step 3: Create migration adapter
    print("\\n3. Creating migration adapter...")
    adapter_path = create_migration_adapter()

    # Step 4: Update imports in dependent files
    print("\\n4. Updating imports in dependent files...")
    updated_files = update_imports()
    if updated_files:
        print(f"   Updated {len(updated_files)} files")
    else:
        print("   No files needed import updates")

    # Step 5: Create migration report
    print("\\n5. Creating migration report...")
    if analysis:
        report = create_migration_report(analysis)

    print("\\n✅ Migration completed successfully!")
    print("\\nNext steps:")
    print("1. Test your application with the new Ray orchestrator")
    print("2. Monitor performance improvements")
    print("3. Gradually remove legacy code when confident")
    print("4. Consider implementing Ray Tune for hyperparameter optimization")

if __name__ == "__main__":
    main()
